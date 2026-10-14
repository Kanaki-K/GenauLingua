"""
🎤 «Говорю»: ответ голосом, эталон по кнопке, пропуск, подсказка «пришлите голос».

Вынесено из `game.py` переносом, без правок поведения.
"""

import html
import logging

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.buttons import menu_texts
from app.bot.handlers.quiz.card import STATE_CARD_ID, show_card
from app.bot.handlers.quiz.lesson import _record_answer
from app.bot.handlers.quiz.lesson_state import (
    S_SPEECH_TRIES,
    SPEECH_ATTEMPTS,
    _claim_answer,
    _release_answer,
    _remember_stray,
)
from app.bot.handlers.quiz.question import _answer_text, get_next_question_keyboard
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
    if not await _claim_answer(state, message.chat.id):
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
    try:
        audio = await message.bot.download(message.voice.file_id)
        verdict = await check_pronunciation(audio.read(), target, pair.learning)
    except Exception:
        logger.exception("не удалось обработать голосовой ответ")

    try:
        await thinking.delete()
    except Exception:
        logger.debug("сообщение «слушаю» не удалилось", exc_info=True)

    # НЕ РАЗОБРАЛ — НЕ ОШИБКА УЧЕНИКА. Тишина, шум, чужой микрофон:
    # засчитывать это промахом значит наказывать за чужую беду, и человек
    # бросит игру. Предлагаем записать ещё раз, вопрос остаётся прежним.
    if verdict is None or verdict.failed or verdict.empty:
        await _release_answer(state, message.chat.id)
        retry = await message.answer(get_text("speech_not_understood", lang))
        await _remember_stray(state, message.message_id, retry.message_id)
        return

    # ТРИ ПОПЫТКИ, И ТРЕТЬЯ ЗАСЧИТЫВАЕТСЯ. Владелец, 14 октября: «почему бы
    # не дать возможность юзеру перезаписать? и если уж 3 раза неправильно —
    # не давать 4-ю… давай на 3-тий раз точно правильно засчитываем, он ведь
    # старался! я думаю это ошибка будет точно бота, а не человека». Живой
    # пример: «der Streit» распознавалось как «Verstrahlt!». Первые две
    # неудачи не записываются — человек видит, что услышано, и пишет снова;
    # третья засчитывается верной. Неразобранная запись (выше) попытку не
    # тратит: там нечего сравнивать.
    attempt = int(data.get(S_SPEECH_TRIES) or 0) + 1
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

    asked_at = data.get("asked_at")
    response_seconds = (
        max(0, int(utcnow().timestamp() - float(asked_at))) if asked_at else None
    )

    await _record_answer(
        bot=message.bot, chat_id=message.chat.id, state=state, session=session,
        user=user, pair=pair, lang=lang, correct_word=correct_word,
        is_correct=verdict.matched or attempt >= SPEECH_ATTEMPTS, channel=channel,
        answer_text=verdict.heard,
        session_id=data["session_id"], correct_answers=data["correct_answers"],
        errors=data["errors"], response_seconds=response_seconds,
        card_message_id=data.get(STATE_CARD_ID),
        # Засчитано ПО ПОПЫТКАМ, а не по услышанному
        forgiven=not verdict.matched,
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


@router.callback_query(F.data == "speech_skip", QuizStates.answering)
async def skip_speech(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    """
    Пропустить вопрос вслух.

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
    if channel is not QuizChannel.SPEECH:
        return

    # ПРОПУСК ТОЖЕ ЗАНИМАЕТ ВОПРОС, хотя и не засчитывается ни верным, ни
    # неверным. Иначе остаётся дыра: пропуск ПОКАЗЫВАЕТ правильный ответ, и
    # записанное после него голосовое пришло бы на вопрос с ответом на
    # экране — то есть на даровой балл.
    if not await _claim_answer(state, callback.message.chat.id):
        return

    lang = user.interface_language or DEFAULT_LOCALE
    pair = pair_from_user(user)
    skipped = get_text("speech_skipped", lang)
    breakdown = _answer_text(correct_word, pair, lang, True, channel)

    await show_card(
        callback.bot, callback.message.chat.id, state, session,
        text=f"{skipped}\n\n{breakdown}",
        keyboard=get_next_question_keyboard(lang),
        clip=await clip_for_user(session, user, correct_word, pair.learning, KIND_FULL),
        word_id=correct_word.id, lang=pair.learning,
        message=callback.message,
    )


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
