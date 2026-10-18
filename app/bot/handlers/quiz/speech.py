"""
🎤 «Говорю»: ответ голосом, эталон по кнопке, пропуск, подсказка «пришлите голос».

Вынесено из `game.py` переносом, без правок поведения.
"""

import asyncio
import html
import time
import logging

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.buttons import menu_texts
from app.bot.handlers.quiz.card import STATE_CARD_HAS_AUDIO, STATE_CARD_ID, show_card
from app.bot.handlers.quiz.lesson import _record_answer
from app.services import journal
from app.bot.handlers.quiz.lesson_state import (
    S_SPEECH_TRIES,
    SPEECH_ATTEMPTS,
    _claim_answer,
    _release_answer,
    _remember_stray,
)
from app.bot.handlers.quiz.question import _answer_text, answer_keyboard
from app.bot.states import QuizStates
from app.core.clock import utcnow
from app.database.enums import QuizChannel
from app.database.models import User, Word
from app.locales import DEFAULT_LOCALE, get_text
from app.services.audio_service import (
    KIND_FULL,
    KIND_SLOW,
    KIND_WORD,
    clip_for_user,
    forget,
    reobtain,
    remember,
    spoken_for,
)
from app.services.language_service import option_label, pair_from_user
from app.services.speech_check import check_pronunciation

logger = logging.getLogger(__name__)


router = Router()

TYPING_EVERY = 4.0


async def _keep_typing(bot, chat_id: int) -> None:
    """«печатает…», пока бот слушает голосовое. Сбой знака ничему не мешает."""
    try:
        while True:
            try:
                await bot.send_chat_action(chat_id, "typing")
            except Exception:
                return
            await asyncio.sleep(TYPING_EVERY)
    except asyncio.CancelledError:
        return


# ============================================================================
# ОТВЕТ ГОЛОСОМ
# ============================================================================

async def _speech_context(message_or_cb, state, session):
    """Общая подготовка для голосового ответа, эталона и пропуска."""
    data = await state.get_data()
    user = await session.get(User, message_or_cb.from_user.id)
    correct_word = await session.get(Word, data.get("correct_word_id"))
    if not user or not correct_word:
        return None
    try:
        channel = QuizChannel(data.get("channel") or QuizChannel.TEXT.value)
    except ValueError:
        channel = QuizChannel.TEXT
    return data, user, correct_word, channel


@router.message(QuizStates.answering, F.voice)
async def process_voice_answer(message: Message, state: FSMContext, session: AsyncSession):
    """
    Ответ голосом: услышал ли бот нужное слово.

    ОЦЕНКИ ПРОИЗНОШЕНИЯ ЗДЕСЬ НЕТ, и это осознанно. Распознаватель обучен
    ПОНИМАТЬ акцент, а не судить его: сильный акцент он расшифрует верно, и
    любой процент, выведенный из его ответа, был бы выдумкой. Ученику
    показывается то, что бот действительно услышал, и эталон для сравнения —
    этого хватает, чтобы услышать разницу самому.
    """
    ctx = await _speech_context(message, state, session)
    if ctx is None:
        return
    data, user, correct_word, channel = ctx

    if channel is not QuizChannel.SPEECH:
        # Голосовое пришло не на тот вопрос — молча пропускаем: человек мог
        # записать его случайно, и ругаться тут не за что
        return

    # ОДИН ВОПРОС — ОДИН ОТВЕТ, и для голоса это нужно не меньше: две
    # записи подряд посчитались бы обе. Проверка стоит ДО распознавания —
    # оно занимает секунды и стоит денег
    if not await _claim_answer(state, message.chat.id, session):
        # Лишняя запись — после засчитанного ответа или пока распознаётся
        # прежняя — не считается, но и висеть в чате не должна: уйдёт с
        # остальными при переходе дальше
        await _remember_stray(state, message.message_id)
        return

    # Счёт попыток читается ПОСЛЕ занятия вопроса: прочитанный до него мог
    # устареть, пока распознавалась прежняя запись
    data = await state.get_data()

    lang = user.interface_language or DEFAULT_LOCALE
    pair = pair_from_user(user)
    target = spoken_for(correct_word, pair.learning, KIND_WORD) or option_label(
        correct_word, pair.learning
    )

    # Распознавание занимает несколько секунд — человек должен видеть, что
    # его услышали, а не гадать, дошло ли сообщение
    thinking = await message.answer(get_text("speech_listening", lang))

    verdict = None
    started = time.perf_counter()
    downloaded = started
    # Пока бот слушает — «печатает…» в шапке чата (2.2.1): распознавание
    # идёт 5 с обычно и до 18 с, и неподвижное «Проверяю…» читалось как
    # зависание. Telegram держит знак 5 секунд — обновляем каждые четыре
    typing = asyncio.create_task(_keep_typing(message.bot, message.chat.id))
    try:
        audio = await message.bot.download(message.voice.file_id)
        downloaded = time.perf_counter()
        verdict = await check_pronunciation(audio.read(), target, pair.learning)
    except asyncio.CancelledError:
        # Остановка бота посреди распознавания (выкатка): вопрос занят, а
        # ответа нет. Состояние в Redis переживёт процесс — без возврата
        # вопрос остался бы запертым на двое суток (аудит 2.1)
        await _release_answer(state, message.chat.id)
        raise
    except Exception:
        logger.exception("не удалось обработать голосовой ответ")
    finally:
        typing.cancel()
    # Разбивка времени: прод 15.10 — один голосовой ответ шёл 21,5 с при
    # обычных пяти, и по журналу было не понять, на что ушло время
    recognized = time.perf_counter() - downloaded
    logger.info("голосовой ответ: скачивание %.1f с, распознавание %.1f с",
                downloaded - started, recognized)

    # КАЖДАЯ ПОПЫТКА — В ЖУРНАЛ (владелец 16.10: «записывать попытки про
    # голосовое — это важно для анализа»). Прежде в базу шёл только
    # засчитанный ответ, и с какой попытки бот понял человека, было не
    # узнать; неразобранные записи и пропуски не оставляли следа вовсе
    def attempt_note(outcome: str, attempt_no: int) -> None:
        journal.note(
            session, user.id, "speech", outcome, session_id=data.get("session_id"),
            word_id=correct_word.id, channel=QuizChannel.SPEECH.value,
            attempt=attempt_no, heard=getattr(verdict, "heard", None) or None,
            similarity=(round(verdict.similarity, 2)
                        if getattr(verdict, "similarity", None) is not None else None),
            target=target, recognize_s=round(recognized, 1),
        )

    try:
        await thinking.delete()
    except Exception:
        logger.debug("сообщение «слушаю» не удалилось", exc_info=True)

    # НЕ РАЗОБРАЛ — НЕ ОШИБКА УЧЕНИКА. Тишина, шум, чужой микрофон:
    # засчитывать это промахом значит наказывать за чужую беду, и человек
    # бросит игру. Предлагаем записать ещё раз, вопрос остаётся прежним.
    if verdict is None or verdict.failed or verdict.empty:
        attempt_note("not_understood", int(data.get(S_SPEECH_TRIES) or 0) + 1)
        await _release_answer(state, message.chat.id)
        retry = await message.answer(get_text("speech_not_understood", lang))
        await _remember_stray(state, message.message_id, retry.message_id)
        return

    # ДВЕ ПОПЫТКИ; ВТОРАЯ НЕУДАЧА — ПРОПУСК. Прежде попыток было три, и
    # третья засчитывалась верной («он ведь старался»). Живой тест владельца
    # 14.10 показал цену: две записи издалека не разобраны («3D-Site um.»,
    # «Dietze und Tonk»), а третью он «вообще обматерил — и засчитало».
    # Владелец: «он так заебет людей. Давай сделаем 2 попытки… нужно
    # адекватное решение».
    #
    # Решение — как у кнопки «Пропустить»: ни балла, ни ошибки. Балл за мат
    # был бы даровым, а ошибка — наказанием за микрофон, а не за
    # произношение: распознаватель ошибается чаще, чем человек. Слово
    # показывается со звуком, расписание не трогается, занятие идёт дальше.
    # Неразобранная запись (выше) попытку не тратит: там нечего сравнивать.
    attempt = int(data.get(S_SPEECH_TRIES) or 0) + 1
    attempt_note("matched" if verdict.matched
                 else ("retry" if attempt < SPEECH_ATTEMPTS else "give_up"), attempt)
    if not verdict.matched and attempt < SPEECH_ATTEMPTS:
        # Счёт попыток — ДО освобождения вопроса: иначе следующая запись,
        # успевшая занять вопрос в этот промежуток, прочла бы старый счёт
        await state.update_data(**{S_SPEECH_TRIES: attempt})
        await _release_answer(state, message.chat.id)
        # Значения — до вызова: вложенный вызов внутри аргументов рвёт разбор
        # в `test_format_parameters_match`
        heard = html.escape(verdict.heard)
        following = attempt + 1
        retry = await message.answer(get_text(
            "speech_try_again", lang, heard=heard,
            attempt=following, total=SPEECH_ATTEMPTS,
        ))
        await _remember_stray(state, message.message_id, retry.message_id)
        return

    await _remember_stray(state, message.message_id)

    if not verdict.matched:
        await _give_up(message, state, session, user, correct_word, channel,
                       data, html.escape(verdict.heard))
        return

    asked_at = data.get("asked_at")
    response_seconds = (
        max(0, int(utcnow().timestamp() - float(asked_at))) if asked_at else None
    )

    await _record_answer(
        bot=message.bot, chat_id=message.chat.id, state=state, session=session,
        user=user, pair=pair, lang=lang, correct_word=correct_word,
        is_correct=True, channel=channel,
        answer_text=verdict.heard,
        session_id=data["session_id"], correct_answers=data["correct_answers"],
        errors=data["errors"], response_seconds=response_seconds,
        card_message_id=data.get(STATE_CARD_ID),
    )


async def _give_up(message: Message, state: FSMContext, session: AsyncSession,
                   user: User, correct_word: Word, channel: QuizChannel,
                   data: dict, heard: str) -> None:
    """
    Вторая неудача голосом — вопрос проходит ПРОПУСКОМ.

    Ничего не записывается: ни строки ответа, ни прогресса, ни ошибки —
    ровно как у кнопки «Пропустить». Показ — как у разбора: карточка
    вопроса выше в переписке (под ней уже голосовые), поэтому она
    удаляется, а ответ приходит новым сообщением со звуком слова и примера.
    """
    lang = user.interface_language or DEFAULT_LOCALE
    pair = pair_from_user(user)

    card_id = data.get(STATE_CARD_ID)
    if card_id:
        try:
            await message.bot.delete_message(message.chat.id, card_id)
        except Exception:
            logger.debug("карточка вопроса не удалилась", exc_info=True)
        await state.update_data(**{STATE_CARD_HAS_AUDIO: False})

    # Значения — до вызова: вложенный вызов внутри аргументов рвёт разбор
    # в `test_format_parameters_match`
    gave_up = get_text("speech_not_counted", lang, heard=heard)
    breakdown = _answer_text(correct_word, pair, lang, True, channel)
    await show_card(
        message.bot, message.chat.id, state, session,
        text=f"{gave_up}\n\n{breakdown}",
        keyboard=answer_keyboard(lang, correct_word, pair, channel, heard=True),
        clip=await clip_for_user(session, user, correct_word, pair.learning, KIND_FULL),
        word_id=correct_word.id, lang=pair.learning,
    )


async def _send_reference(bot, chat_id: int, clip):
    """Отправить эталон. None — клипа нет или Telegram его отверг."""
    if clip is None:
        return None
    media = clip.file_id or BufferedInputFile(clip.data, filename=clip.filename)
    try:
        return await bot.send_audio(chat_id, media, title=clip.title)
    except TelegramBadRequest:
        logger.warning("эталон отвергнут Telegram (%s)", clip.kind, exc_info=True)
        return None


@router.callback_query(F.data == "speech_reference", QuizStates.answering)
async def play_reference(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    """
    Эталон по кнопке: услышать, как это звучит у носителя.

    Приходит ОТДЕЛЬНЫМ сообщением, а не заменяет карточку: задание должно
    остаться на экране, иначе человек забудет, что произносить.
    """
    ctx = await _speech_context(callback, state, session)
    if ctx is None:
        await callback.answer()
        return
    _, user, correct_word, _ = ctx
    lang = user.interface_language or DEFAULT_LOCALE
    pair = pair_from_user(user)

    # На нажатие отвечают ОДИН раз: прежде `answer()` стоял в начале, и
    # окно «клипа нет» шло вторым ответом, которого Telegram не показывает.
    # Да и текст был чужой — «Не разобрал», будто человек что-то записал.
    # МЕДЛЕННО, а не то же самое: обычная озвучка уже на карточке
    clip = await clip_for_user(session, user, correct_word, pair.learning, KIND_SLOW)
    sent = await _send_reference(callback.bot, callback.message.chat.id, clip)

    # МЁРТВЫЙ file_id — как на карточке (`show_card`): запись кэша
    # выбрасывается, звук берётся заново с диска или синтезом. Прежде отказ
    # Telegram уходил наружу, и кнопка на этом слове не работала НИКОГДА:
    # мёртвая запись оставалась в кэше
    if sent is None and clip is not None and clip.file_id:
        await forget(session, correct_word.id, pair.learning, clip.kind, clip.voice)
        clip = await reobtain(clip, pair.learning)
        sent = await _send_reference(callback.bot, callback.message.chat.id, clip)

    if sent is None:
        await callback.answer(get_text("voice_preview_failed", lang), show_alert=True)
        return
    await callback.answer()

    await _remember_stray(state, sent.message_id)
    if clip.needs_remembering and getattr(sent, "audio", None):
        await remember(
            session, correct_word.id, pair.learning, clip,
            sent.audio.file_id, getattr(sent.audio, "duration", None),
        )
        await session.commit()


@router.callback_query(F.data.in_({"speech_skip", "listen_skip"}), QuizStates.answering)
async def skip_speech(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    """
    Пропустить вопрос вслух — или на слух («Слушаю»: звук включить нельзя).

    Пропуск НЕ засчитывается ошибкой: человек мог оказаться в транспорте или
    рядом со спящим ребёнком, и наказывать за это значит потерять не вопрос,
    а всё занятие. Верным он тоже не считается — показ просто не учитывается
    нигде, ни в прогрессе, ни в точности.
    """
    await callback.answer()
    ctx = await _speech_context(callback, state, session)
    if ctx is None:
        return
    data, user, correct_word, channel = ctx
    # Кнопка своей игры: «speech_skip» — у речи, «listen_skip» — у слуха.
    # Чужая (старая карточка в переписке) ничего не пропускает
    allowed = (QuizChannel.SPEECH if callback.data == "speech_skip"
               else QuizChannel.AUDIO)
    if channel is not allowed:
        return

    # ПРОПУСК ТОЖЕ ЗАНИМАЕТ ВОПРОС, хотя и не засчитывается ни верным, ни
    # неверным. Иначе остаётся дыра: пропуск ПОКАЗЫВАЕТ правильный ответ, и
    # записанное после него голосовое пришло бы на вопрос с ответом на
    # экране — то есть на даровой балл.
    if not await _claim_answer(state, callback.message.chat.id, session):
        return

    data = await state.get_data()
    journal.note(session, user.id, "skip", callback.data, session_id=data.get("session_id"),
                 word_id=correct_word.id, channel=channel.value,
                 attempt=int(data.get(S_SPEECH_TRIES) or 0) or None)
    lang = user.interface_language or DEFAULT_LOCALE
    pair = pair_from_user(user)
    skipped = get_text("speech_skipped", lang)
    breakdown = _answer_text(correct_word, pair, lang, True, channel)

    await show_card(
        callback.bot, callback.message.chat.id, state, session,
        text=f"{skipped}\n\n{breakdown}",
        keyboard=answer_keyboard(lang, correct_word, pair, channel, heard=True),
        clip=await clip_for_user(session, user, correct_word, pair.learning, KIND_FULL),
        word_id=correct_word.id, lang=pair.learning,
        message=callback.message,
    )
    if (channel is QuizChannel.SPEECH and _may_ask_again(user)
            and await _skips_in_a_row(session, user.id)):
        await _offer_speech_off(callback, state, session, user, lang)


# ============================================================================
# «ГОВОРЮ» ПРОПУСКАЮТ ПОДРЯД — СПРОСИТЬ, УБРАТЬ ЛИ (2.2.1)
# ============================================================================

# Прод 14–18.10: «Говорю» показан 78 раз, пропущен 42; одному человеку — 23
# показа и 21 пропуск, ещё двоим 6 из 6 и 4 из 4. Бот пропусков не замечал
# и просил снова. После стольких пропусков ПОДРЯД — один раз спросить.
SKIPS_BEFORE_OFFER = 3
# «Убрать?» — не чаще раза в две недели: «Оставить» — тоже ответ (2.2.1)
ASK_OFF_AGAIN_DAYS = 14


def _may_ask_again(user) -> bool:
    from datetime import timedelta

    asked = getattr(user, "speech_asked_at", None)
    return asked is None or utcnow() - asked >= timedelta(days=ASK_OFF_AGAIN_DAYS)
CB_SPEECH_OFF = "speech_off"
CB_SPEECH_KEEP = "speech_keep"


async def _skips_in_a_row(session: AsyncSession, user_id: int) -> bool:
    """
    Последние `SKIPS_BEFORE_OFFER` событий «Говорю» — все пропуски.

    Считаются пропуск (`skip` по речи), голосовой ответ (`speech`) и само
    предложение (`speech_offer`): голос между пропусками сбрасывает счёт, а
    сделанное предложение — откладывает следующее до новых трёх пропусков.
    """
    from sqlalchemy import and_, or_, select

    from app.database.models import UserEvent

    kinds = (await session.execute(
        select(UserEvent.kind).where(
            UserEvent.user_id == user_id,
            or_(and_(UserEvent.kind == "skip", UserEvent.channel == QuizChannel.SPEECH.value),
                UserEvent.kind.in_(("speech", "speech_offer"))),
        ).order_by(UserEvent.at.desc(), UserEvent.id.desc()).limit(SKIPS_BEFORE_OFFER)
    )).scalars().all()
    return len(kinds) == SKIPS_BEFORE_OFFER and all(k == "skip" for k in kinds)


async def _offer_speech_off(callback: CallbackQuery, state: FSMContext,
                            session: AsyncSession, user: User, lang: str) -> None:
    """Вопрос под карточкой; уходит сам со следующим вопросом, как подсказки голоса."""
    from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=get_text("btn_speech_off", lang), callback_data=CB_SPEECH_OFF),
        InlineKeyboardButton(text=get_text("btn_speech_keep", lang), callback_data=CB_SPEECH_KEEP),
    ]])
    offer = await callback.bot.send_message(
        callback.message.chat.id, get_text("speech_offer_text", lang), reply_markup=keyboard,
    )
    await _remember_stray(state, offer.message_id)
    user.speech_asked_at = utcnow()
    journal.note(session, user.id, "speech_offer", "shown")
    await session.commit()


@router.callback_query(F.data == CB_SPEECH_OFF)
async def speech_off(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    """Убрать «Говорю» из набора игр — та же настройка, что в «Игры занятия»."""
    await callback.answer()
    user = await session.get(User, callback.from_user.id)
    if user is None:
        return
    lang = user.interface_language or DEFAULT_LOCALE
    current = user.quiz_channels or "tasrb"
    user.quiz_channels = "".join(c for c in current if c != QuizChannel.SPEECH.value) or "t"
    user.speech_choice = "off"
    journal.note(session, user.id, "speech_offer", "off")
    await session.commit()
    try:
        await callback.message.edit_text(get_text("speech_off_done", lang))
    except Exception:
        logger.debug("предложение не поправилось", exc_info=True)


@router.callback_query(F.data == CB_SPEECH_KEEP)
async def speech_keep(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    """Оставить — и не спрашивать, пока не наберутся новые три пропуска подряд."""
    await callback.answer()
    user = await session.get(User, callback.from_user.id)
    if user is not None:
        user.speech_asked_at = utcnow()
    journal.note(session, callback.from_user.id, "speech_offer", "keep")
    await session.commit()
    try:
        await callback.message.delete()
    except Exception:
        logger.debug("предложение не удалилось", exc_info=True)


@router.message(
    QuizStates.answering,
    F.text,
    ~F.text.startswith("/"),
    # Отсев стоит В ФИЛЬТРЕ, а не в теле обработчика, и это существенно:
    # совпавший обработчик ГАСИТ событие, даже если ничего не сделал.
    # Проверка внутри тела не вернула бы нажатие следующим роутерам —
    # «Настройки» и «Статистика» так и остались бы мёртвыми во время вопроса.
    ~F.text.in_(menu_texts()),
)
async def hint_to_speak(message: Message, state: FSMContext, session: AsyncSession):
    """
    Написал текстом там, где ждут голос — подсказать, а не промолчать.

    НАЖАТИЯ ГЛАВНОГО МЕНЮ И КОМАНДЫ СЮДА НЕ ДОЛЖНЫ ПОПАДАТЬ, и это не
    предосторожность, а исправление внесённой регрессии. Роутер игры
    подключён в main.py РАНЬШЕ настроек и статистики, а подписка на
     ловит любое сообщение. В состоянии ответа кнопки «🦾
    Настройки» и «📊 Статистика» переставали работать молча: обработчик
    срабатывал, ничего не делал и гасил событие.

    Отсюда два отсева — команды по ведущей косой черте и надписи кнопок
    меню на ВСЕХ языках интерфейса. Второй берётся из локалей, а не
    выписывается руками: иначе добавление языка молча вернуло бы ту же
    беду, но только для его пользователей.
    """
    ctx = await _speech_context(message, state, session)
    if ctx is None:
        return
    _, user, _, channel = ctx
    if channel is not QuizChannel.SPEECH:
        return
    lang = user.interface_language or DEFAULT_LOCALE
    await message.answer(get_text("speech_send_voice", lang))
