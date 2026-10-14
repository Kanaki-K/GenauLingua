"""
Игровая логика викторины.

Не привязана к конкретному языку: что показывать и на каком языке давать
варианты, решает LanguagePair (изучаемый язык, язык значения, направление).

Учёт точности идёт по фактически отвеченным вопросам — answered_questions
пишется на каждый ответ. Плановое total_questions для точности не годится:
брошенная сессия иначе выглядит как сплошные ошибки.
"""

import html
import logging
from typing import Optional

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, CallbackQuery, Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.buttons import BTN_LEARN_WORDS, menu_texts, pressed
from app.bot.keyboards import get_answer_keyboard
from app.bot.states import QuizStates
from app.bot.handlers.quiz.card import STATE_CARD_HAS_AUDIO, STATE_CARD_ID, show_card
from app.bot.handlers.quiz.lesson_state import (
    DEFAULT_QUIZ_LENGTH,
    S_BOARD_DONE,
    S_REPEAT_FROM,
    S_SPEECH_TRIES,
    SPEECH_ATTEMPTS,
    _claim_advance,
    _claim_answer,
    _claim_lock,
    _recover,
    _release_answer,
    _remember_stray,
    _reset_round_state,
    _sweep_stray,
)
from app.bot.handlers.quiz.listen import _as_text_question, _clip_or_text, _question_clip
from app.bot.handlers.quiz.question import (
    _answer_text,
    _build_state,
    _question_keyboard,
    _question_text,
    get_next_question_keyboard,
)
from app.bot.handlers.quiz.sources import SOURCE_MENU, SOURCE_REPEAT
from app.bot.utils import delete_messages_fast, ensure_anchor
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
from app.services.speech_check import check_pronunciation
from app.core.clock import utcnow
from app.database.enums import QuizChannel, QuizMode
from app.database.models import QuizQuestion, QuizSession, User, Word
from app.bot.handlers.quiz.summary import _finish_quiz
from app.locales import DEFAULT_LOCALE, get_text
from app.services.language_service import (
    pair_for_channel,
    LanguagePair,
    option_label,
    legacy_mode_name,
    pair_from_user,
)
from app.services.quiz_service import (
    OPTIONS_TOTAL,
    build_options,
    count_difficult_words,
    generate_question,
    get_distractors,
    update_word_progress,
)

logger = logging.getLogger(__name__)


router = Router()

# Сколько раз пытаться подобрать слово, прежде чем признать, что подходящих нет
QUESTION_ATTEMPTS = 10


# ============================================================================
# УТИЛИТЫ
# ============================================================================


async def _close_abandoned_sessions(session: AsyncSession, user_id: int) -> None:
    """
    Помечать незавершённые сессии как брошенные при старте новой.

    Раньше exit_reason не записывался никогда, поэтому по данным нельзя было
    отличить брошенную викторину от незакрытой. answered_questions у такой
    сессии уже показывает, на каком вопросе человек ушёл.
    """
    result = await session.execute(
        select(QuizSession).where(
            QuizSession.user_id == user_id,
            QuizSession.is_completed.is_(False),
            QuizSession.exit_reason.is_(None),
        )
    )
    for stale in result.scalars():
        stale.exit_reason = "abandoned"
        stale.exit_at_question = stale.answered_questions
    await session.commit()


def _new_quiz_session(
    user: User, pair: LanguagePair, total: int, quiz_mode: str,
    source: str = SOURCE_MENU,
) -> QuizSession:
    return QuizSession(
        user_id=user.id,
        level=user.level,
        learning_lang=pair.learning,
        native_lang=pair.native,
        is_reverse=pair.reverse,
        # Устаревшее поле: заполняем только для пар с немецким, ради прежней аналитики
        translation_mode=legacy_mode_name(pair),
        total_questions=total,
        answered_questions=0,
        correct_answers=0,
        quiz_mode=quiz_mode,
        quiz_category=user.quiz_category,
        start_source=source,
    )


# ============================================================================
# СТАРТ ВИКТОРИНЫ
# ============================================================================

@router.message(Command("quiz"))
@router.message(pressed(BTN_LEARN_WORDS))
async def start_quiz(message: Message, state: FSMContext, session: AsyncSession):
    """
    Кнопка «📚 Учить» и команда `/quiz` — занятие начинается СРАЗУ.

    Домашний экран между ними не встаёт, хотя три шкалы живут именно на нём.
    Поставить его здесь значило бы добавить нажатие перед каждым занятием —
    тем самым 96%, которые ни разу не меняли ни одной настройки. Своя дверь
    у домашнего экрана есть: `/start` и `/home`.
    """
    await start_lesson(message, state, session, source=SOURCE_MENU)


async def start_lesson(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
    *,
    prefer_channel: Optional[QuizChannel] = None,
    source: str = SOURCE_MENU,
) -> None:
    """
    Начать занятие. Отсюда два входа, и оба нужны.

    Обычный — кнопка «📚 Учить» и команда `/quiz`: каналы смешиваются внутри
    круга по правилу допуска.

    Прямой одним каналом — кнопки 🔤 🎧 🎤 домашнего экрана. Желание
    передаётся как `prefer_channel`, то есть порог допуска НЕ обходится:
    слово, до канала не доросшее, придёт текстом.

    `message` — то, на что отвечать и что убрать с экрана. От кнопки меню это
    сообщение человека, с домашнего экрана — сам домашний экран: занятие
    встаёт на его место, и лишнего сообщения в переписке не остаётся.
    """
    user = await session.get(User, message.chat.id)

    if not user or not user.level:
        lang = user.interface_language if user else DEFAULT_LOCALE
        await message.answer(get_text("quiz_no_level", lang))
        return

    lang = user.interface_language or DEFAULT_LOCALE
    pair = pair_from_user(user)

    await _close_abandoned_sessions(session, user.id)

    quiz_total = user.quiz_word_count or DEFAULT_QUIZ_LENGTH

    if user.quiz_mode == QuizMode.DIFFICULT:
        difficult = await count_difficult_words(user.id, session, pair)
        if difficult == 0:
            await message.answer(get_text("qmode_difficult_empty", lang))
            return
        if difficult < OPTIONS_TOTAL:
            await message.answer(get_text("qmode_difficult_few", lang, count=difficult))
            return
        quiz_total = min(difficult, quiz_total)

    try:
        # Канал выбирает сам generate_question — после того, как SRS отдал
        # слово: правило допуска к слуху смотрит на прогресс по КОНКРЕТНОМУ
        # слову, и до выбора слова решать нечего.
        question = await generate_question(
            session, user, exclude_ids=[], pair=pair, recent_channels=[],
            prefer_channel=prefer_channel,
            round_length=quiz_total, question_number=1,
        )
    except Exception:
        logger.exception("Ошибка генерации первого вопроса (user=%s)", user.id)
        await message.answer(get_text("quiz_error_generation", lang))
        return

    if not question:
        await message.answer(get_text("quiz_no_words", lang))
        return

    quiz_session = _new_quiz_session(
        user, pair, quiz_total, user.quiz_mode.value if user.quiz_mode else "level",
        source=source,
    )
    session.add(quiz_session)
    await session.commit()

    word = question["correct_word"]
    channel = question["channel"]
    clip, channel, question["options"] = await _clip_or_text(
        session, user, word, pair, channel, question["options"]
    )

    await _reset_round_state(state)
    await state.update_data(
        session_id=quiz_session.id,
        current_question=1,
        total_questions=quiz_total,
        correct_answers=0,
        errors=[],
        correct_word_id=word.id,
        used_word_ids=[word.id],
        is_error_repeat=False,
        asked_at=utcnow().timestamp(),
        channel=channel.value,
        recent_channels=[channel.value],
        # Желание держится весь круг, а не один вопрос: вход «только слух»,
        # сменившийся на втором вопросе общим правилом, выглядел бы поломкой
        prefer_channel=prefer_channel.value if prefer_channel else None,
        # 🧱 Сборке — своё состояние сетки (пусто для остальных игр)
        **_build_state(question, channel),
    )

    try:
        await message.delete()
    except Exception:
        logger.debug("Не удалось удалить сообщение пользователя", exc_info=True)

    old_anchor_id, _ = await ensure_anchor(message, session, user, emoji="")
    if old_anchor_id:
        await delete_messages_fast(message.bot, message.chat.id, old_anchor_id, message.message_id)

    await show_card(
        message.bot, message.chat.id, state, session,
        text=_question_text(word, pair, lang, 1, quiz_total, channel=channel),
        keyboard=_question_keyboard(channel, question["options"], lang, word.id),
        clip=clip,
        word_id=word.id, lang=pair.learning,
        without_audio=_as_text_question(
            session, user, word, pair, state, lang, 1, quiz_total, channel
        ),
    )
    await state.set_state(QuizStates.answering)


# ============================================================================
# ОБРАБОТКА ОТВЕТА
# ============================================================================

@router.callback_query(F.data.startswith("answer_"), QuizStates.answering)
async def process_answer(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    selected_word_id = int(callback.data.split("_")[1])

    # ОДИН ВОПРОС — ОДИН ОТВЕТ. Разбор у `_claim_answer`: двойной тык и
    # нажатие по не перерисовавшейся карточке записывали вопрос дважды, и
    # балл начислялся дважды
    if not await _claim_answer(state, callback.message.chat.id):
        await callback.answer()
        return

    data = await state.get_data()
    correct_word_id = data["correct_word_id"]
    session_id = data["session_id"]
    correct_answers = data["correct_answers"]
    errors = data["errors"]

    correct_word = await session.get(Word, correct_word_id)
    user = await session.get(User, callback.from_user.id)

    if not correct_word or not user:
        await callback.answer("Error", show_alert=True)
        await state.clear()
        return

    lang = user.interface_language or DEFAULT_LOCALE
    pair = pair_from_user(user)
    is_correct = selected_word_id == correct_word_id

    # Канал берётся из состояния, а не вычисляется заново по номеру вопроса.
    # Пересчёт дал бы неверный ответ в двух случаях: при повторе ошибок (там
    # канал всегда текстовый независимо от номера) и если человек поменяет
    # состав занятия, не ответив на уже заданный вопрос.
    #
    # Значение по умолчанию TEXT нужно для занятий, начатых до этой правки:
    # у них в состоянии канала нет, а все их вопросы были текстовыми.
    try:
        channel = QuizChannel(data.get("channel") or QuizChannel.TEXT.value)
    except ValueError:
        channel = QuizChannel.TEXT

    # Что именно выбрал пользователь — по этому видно, какие неверные варианты
    # притягивают. Прежде колонка не заполнялась, и разбирать ошибки было нечем.
    #
    # ЗАПИСЫВАЕТСЯ НАДПИСЬ С КНОПКИ, А НЕ ЯЧЕЙКА, и на языке ТЕХ САМЫХ
    # вариантов. Прежде бралось `word_text(..., pair.answer_lang)`, и после
    # вопроса на слух выходило вот что: ученик нажал «die Erfrischung», а в
    # базу шло «прохладительный напиток, освежение, освежающая закуска» —
    # другой язык и вся ячейка вместо одного значения. Разбирать по такой
    # записи, какие варианты притягивают, нельзя: там не то, что видели.
    # Поле к тому же обрезано до 255 знаков, и длинные ячейки усекались.
    #
    # Язык вариантов задаёт канал: на слух они на ИЗУЧАЕМОМ языке, иначе —
    # на языке ответа ЭТОЙ ИГРЫ. В «Вспоминаю» пара перевёрнута, и варианты
    # — слова изучаемого языка: прежде бралась неперевёрнутая пара, и
    # нажатое «der Drink» записывалось как «Напиток».
    options_lang = (pair.learning if channel is QuizChannel.AUDIO
                    else pair_for_channel(pair, channel).answer_lang)
    selected_word = correct_word if is_correct else await session.get(Word, selected_word_id)
    selected_text = option_label(selected_word, options_lang) if selected_word else None

    asked_at = data.get("asked_at")
    response_seconds = None
    if asked_at:
        response_seconds = max(0, int(utcnow().timestamp() - float(asked_at)))

    await _record_answer(
        bot=callback.bot, chat_id=callback.message.chat.id, state=state,
        session=session, user=user, pair=pair, lang=lang,
        correct_word=correct_word, is_correct=is_correct, channel=channel,
        answer_text=selected_text, card_message=callback.message,
        session_id=session_id, correct_answers=correct_answers, errors=errors,
        response_seconds=response_seconds,
    )
    await callback.answer()


async def _record_answer(
    *, bot, chat_id, state, session, user, pair, lang,
    correct_word, is_correct, channel, answer_text,
    session_id, correct_answers, errors, response_seconds,
    card_message=None, card_message_id=None, forgiven: bool = False,
    breakdown: Optional[str] = None,
) -> None:
    """
    Общая часть любого ответа: запись, прогресс, показ разбора.

    Вынесена потому, что ответов теперь ДВА ВИДА: нажатие на вариант и
    голосовое сообщение. Держать для них две копии этой тридцатистрочной
    последовательности значило бы гарантировать расхождение — одну поправят,
    вторую забудут.

    `card_message` — сообщение карточки, если оно под рукой (так при
    нажатии). При голосовом ответе карточка остаётся выше в переписке, и
    у обработчика есть только её `card_message_id`: прежняя карточка
    удаляется по нему, а разбор приходит новым сообщением.

    `forgiven` — ответ засчитан верным не по существу, а по попыткам
    (третья запись голосом). Решение владельца: балл за него положен, а
    расписание он двигать НЕ должен — как досрочный ответ: слово человек
    не произнёс, и «повторить через три дня» было бы неправдой.

    `breakdown` — готовый текст разбора, если у игры он свой: у сборки это
    фраза человека с отметками по словам и эталон (`build.py`). Без него —
    общий разбор «слово — значение» с примерами.
    """
    correct_word_id = correct_word.id

    session.add(
        QuizQuestion(
            session_id=session_id,
            word_id=correct_word_id,
            user_answer=(answer_text or "")[:255] or None,
            is_correct=is_correct,
            answered_at=utcnow(),
            response_time_seconds=response_seconds,
            # Канал хранится у ВОПРОСА: круг смешанный, и у занятия канала
            # нет — есть состав. Отсюда же считаются баллы: верный ответ на
            # слух стоит дороже прочитанного.
            channel=channel.value,
        )
    )

    # Точность считается по отвеченным вопросам, поэтому счётчик
    # инкрементируется сразу — брошенная сессия остаётся корректной
    quiz_session = await session.get(QuizSession, session_id)
    if quiz_session:
        quiz_session.answered_questions = (quiz_session.answered_questions or 0) + 1
        if is_correct:
            quiz_session.correct_answers = (quiz_session.correct_answers or 0) + 1

    await session.commit()

    try:
        await update_word_progress(
            user_id=user.id,
            word_id=correct_word_id,
            is_correct=is_correct,
            session=session,
            learning_lang=pair.learning,
            channel=channel,
            # Засчитанное по попыткам — верно и с баллами, но срок не двигает
            advance_schedule=not forgiven,
        )
    except Exception:
        logger.exception("Ошибка обновления прогресса (user=%s word=%s)", user.id, correct_word_id)
        # ОТКАТ ОБЯЗАТЕЛЕН. Упавший коммит оставляет сессию в состоянии
        # «нужен откат», и следующий же запрос — клип разбора — падал бы
        # уже без перехвата: человек оставался без экрана. Строка вопроса и
        # счётчики занятия закоммичены выше и откатом не задеваются; объекты,
        # которые нужны дальше, перечитываются
        await _recover(session, user, correct_word)

    if is_correct:
        correct_answers += 1
    else:
        errors.append(correct_word_id)

    await state.update_data(correct_answers=correct_answers, errors=errors)

    # Голосовой ответ пришёл отдельным сообщением, и карточка вопроса
    # осталась выше в переписке. Править её на месте нельзя — между ней и
    # низом чата уже стоит запись ученика, — поэтому удаляем по id, а разбор
    # приходит новым сообщением под голосовым.
    if card_message is None and card_message_id:
        try:
            await bot.delete_message(chat_id, card_message_id)
        except Exception:
            logger.debug("карточка вопроса не удалилась", exc_info=True)
        await state.update_data(**{STATE_CARD_HAS_AUDIO: False})

    # На разборе звучит слово с примером: значение уже известно, и теперь
    # слышно, как слово живёт в живой речи. В вопросе примера в звуке нет —
    # там его было бы не разобрать.
    await show_card(
        bot, chat_id, state, session,
        text=breakdown or _answer_text(correct_word, pair, lang, is_correct, channel),
        keyboard=get_next_question_keyboard(lang),
        clip=await clip_for_user(session, user, correct_word, pair.learning, KIND_FULL),
        word_id=correct_word.id, lang=pair.learning,
        message=card_message,
    )


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


# ============================================================================
# 🧩 ДОСКА ВНУТРИ КРУГА
# ============================================================================


async def record_board_answers(
    state: FSMContext, session: AsyncSession, user: User, pair: LanguagePair,
    words: list[Word], matched: list[int], counted: set[int],
) -> bool:
    """
    Записать подвопросы доски как ОБЫЧНЫЕ ответы круга.

    ЗАЧЕМ ЭТО ОТДЕЛЬНОЙ ФУНКЦИЕЙ И ПОЧЕМУ ОНА ВАЖНА. Первая редакция доски
    звала только `update_word_progress` — то есть двигала прогресс по
    словам (три шкалы) и НИЧЕГО больше. Следствий было четыре, и все
    тихие:

        баллов НЕТ        счёт берётся из `quiz_questions`, а строк там
                          не появлялось
        точности НЕТ      `answered_questions` не росло
        репорта НЕТ       жаловаться на перевод не на что: репорт ищет
                          слова круга по тем же строкам
        повтора ошибок НЕТ промахи не попадали в список ошибок круга

    Человек решал доску, видел «зачтено 4 из 5» и не получал за это ни
    балла. Снаружи это выглядело бы как обман.

    Теперь каждая пара пишется ровно как ответ на вопрос: своя строка
    `QuizQuestion`, свой инкремент счётчиков, своя запись в прогресс. Канал
    — `BOARD_CHANNEL`, и один балл за верный подвопрос получается сам,
    вычитанием в месячном счёте.

    Возвращает False, если доска открыта САМА ПО СЕБЕ, а не в круге: тогда
    записывать некуда, и прогресс по словам двигает уже вызывающий.
    """
    from app.bot.handlers.quiz.match import S_ROUND_AT
    from app.services.match_service import BOARD_CHANNEL

    data = await state.get_data()
    session_id = data.get("session_id")
    # В КРУГЕ — ЭТО ДОСКА, КОТОРУЮ ПОСТАВИЛ КРУГ, а не любая доска при
    # живом `session_id`. Прежде `/match` посреди круга писал свои пять пар
    # в этот круг: шесть строк в занятии вместо одной, план 15 — отвечено
    # больше. Брошенный круг держал `session_id` до перезапуска бота.
    if not session_id or not data.get(S_ROUND_AT):
        return False

    quiz_session = await session.get(QuizSession, session_id)
    correct_answers = data.get("correct_answers", 0)
    errors = list(data.get("errors", []))
    # Номера слов — заранее: после отката (ниже) объекты слов просрочены, а
    # подгрузить их лениво асинхронная сессия не умеет
    word_ids = [w.id for w in words]

    for index in matched:
        word = words[index]
        is_correct = index in counted

        session.add(QuizQuestion(
            session_id=session_id,
            word_id=word.id,
            # Что человек выбрал, в доске совпадает с верным ответом: пара
            # сходится только тогда, когда он нажал правильную половину.
            # Неверные нажатия это промахи, и они не создают строк — иначе
            # одна пара дала бы их столько, сколько человек перебирал
            user_answer=option_label(word, pair.answer_lang)[:255] or None,
            is_correct=is_correct,
            answered_at=utcnow(),
            channel=BOARD_CHANNEL,
        ))

        if quiz_session:
            quiz_session.answered_questions = (quiz_session.answered_questions or 0) + 1
            if is_correct:
                quiz_session.correct_answers = (quiz_session.correct_answers or 0) + 1

        if is_correct:
            correct_answers += 1
        else:
            # Промах идёт в ошибки круга — значит «повторить ошибки» его
            # разберёт, и разберёт ТЕКСТОМ, как все прочие ошибки
            errors.append(word.id)

        # Строка и счётчики — В БАЗУ ДО ПРОГРЕССА: упади прогресс, откат
        # ниже не должен унести уже засчитанный подвопрос
        await session.commit()

        try:
            await update_word_progress(
                user_id=user.id, word_id=word_ids[index], is_correct=is_correct,
                session=session, learning_lang=pair.learning,
                channel=QuizChannel.TEXT,
            )
        except Exception:
            logger.exception(
                "ошибка прогресса на доске (user=%s word=%s)", user.id, word_ids[index]
            )
            # Без отката следующий же запрос упал бы — разбор в `_recover`
            await _recover(session, user, quiz_session, *words)

    await session.commit()

    # СЛОВА ДОСКИ — ЗАДЕЙСТВОВАННЫЕ, и остаток круга их больше не возьмёт.
    #
    # Без этого слово, только что найденное на доске, приходило обычным
    # вопросом через два хода: прогресс по нему двигался дважды за круг, а
    # человек видел одно и то же. Доска читает тот же список при сборке —
    # так что запрет работает в обе стороны.
    used = list(data.get("used_word_ids") or [])
    used.extend(word_ids[index] for index in matched
                if word_ids[index] not in used)

    await state.update_data(
        correct_answers=correct_answers, errors=errors, used_word_ids=used
    )
    return True


async def _board_due(
    state: FSMContext, session: AsyncSession, user: User, pair: LanguagePair,
    current_question: int, total_questions: int,
) -> bool:
    """
    Пора ли показать доску на этом вопросе.

    Проверки идут от дешёвых к дорогим: сперва состояние и номер вопроса,
    и только потом запрос к базе за годными словами. Обратный порядок
    стоил бы запроса на КАЖДОМ вопросе круга.
    """
    from app.services.match_service import (
        BOARD_SIZE, board_slot, pick_words, should_insert_board,
    )

    data = await state.get_data()
    if data.get(S_BOARD_DONE):
        return False

    if current_question != board_slot(total_questions):
        return False

    # Годных слов берём с запасом: `should_insert_board` требует вдвое
    # больше доски, иначе доски пошли бы одним набором
    #
    # УЖЕ ЗАДАННЫЕ СЛОВА ИСКЛЮЧАЮТСЯ И ЗДЕСЬ — тем же списком, что у самой
    # доски. Без этого проверка насчитывала десять годных, доска после
    # исключения находила меньше пяти, и посреди круга появлялось «Пока
    # рано: поучи карточками».
    eligible = await pick_words(
        user, session, pair, size=BOARD_SIZE * 2,
        exclude_ids=list(data.get("used_word_ids") or []),
    )
    return should_insert_board(user, total_questions, len(eligible))


async def _show_board_in_round(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession,
    user: User, current_question: int,
) -> None:
    """
    Показать доску вместо вопроса и запомнить, куда вернуться.

    Прежняя карточка удаляется: доска — отдельное сообщение со своей
    клавиатурой, и правкой карточку в неё не превратить.
    """
    from app.bot.handlers.quiz.match import S_ROUND_AT, start_board

    await state.update_data(**{S_BOARD_DONE: True})
    try:
        await callback.message.delete()
    except Exception:
        logger.debug("карточка перед доской не удалилась", exc_info=True)

    shown = await start_board(callback.message, state, session, user, quiet=True)
    if shown:
        # Номер вопроса, на котором доска встала: по нему она и вернёт круг
        await state.update_data(**{S_ROUND_AT: current_question})
        return

    # Доска не собралась — круг не должен встать. Отдаём обычный вопрос с
    # того же номера, как будто доски и не было
    logger.info("доска в круге не собралась (user=%s), продолжаю вопросами", user.id)
    await _advance(callback, state, session)


# ============================================================================
# СЛЕДУЮЩИЙ ВОПРОС / ЗАВЕРШЕНИЕ
# ============================================================================


@router.callback_query(F.data == "next_question", QuizStates.answering)
async def show_next_question(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    await callback.answer()
    if not await _claim_advance(state, callback.message.chat.id):
        return
    await _advance(callback, state, session)


async def _advance(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    """Следующий вопрос, доска или итог. На нажатие уже ответили."""
    await _sweep_stray(callback.bot, callback.message.chat.id, state)
    # Новый вопрос — попытки голосом снова с первой
    await state.update_data(**{S_SPEECH_TRIES: 0})
    data = await state.get_data()
    current_question = data["current_question"] + 1
    total_questions = data["total_questions"]
    used_word_ids = data.get("used_word_ids", [])
    recent_channels = data.get("recent_channels", [])

    # Прямой вход одним каналом держится весь круг. Значение берётся из
    # состояния, а не вычисляется заново: занятия, начатые до этой правки,
    # ключа не имеют, и у них желания нет — как и было.
    try:
        prefer_channel = (
            QuizChannel(data["prefer_channel"]) if data.get("prefer_channel") else None
        )
    except ValueError:
        prefer_channel = None

    is_error_repeat = data.get("is_error_repeat", False)
    error_words = data.get("error_words", [])
    current_error_index = data.get("current_error_index", 0)

    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or DEFAULT_LOCALE
    pair = pair_from_user(user)

    if current_question > total_questions:
        await _finish_quiz(callback, state, session, user, pair, lang, data)
        return

    # 🧩 ДОСКА — ЭТО ОДИН ВОПРОС КРУГА, внутри которого пять подвопросов.
    #
    # Один, а не пять, и это поправка владельца к моей ошибке. Первая
    # редакция отдавала доске пять слотов — ради правила «15 вопросов = 15
    # слов». Владелец: «Зачем ломать юзеру порядок 6 7 8?» Счёт
    # перескакивал с пятого на одиннадцатый, то есть ломалось то, что
    # человек ВИДИТ, ради правила, которого ему никто не обещал.
    #
    # В повтор ошибок доска НЕ вставляется: там человек разбирает то, с чем
    # не справился, и подмешивать упражнение другого рода значит мешать две
    # трудности в одной попытке. То же правило, по которому повтор идёт
    # только текстом.
    if not is_error_repeat and await _board_due(
        state, session, user, pair, current_question, total_questions
    ):
        await _show_board_in_round(callback, state, session, user, current_question)
        return

    if is_error_repeat:
        current_error_index += 1
        if current_error_index >= len(error_words):
            logger.warning("error_repeat: индекс вышел за пределы списка ошибок")
            await state.clear()
            return

        word = await session.get(Word, error_words[current_error_index])
        distractors = (await get_distractors(word, session, pair, user=user)
                       if word else [])
        if len(distractors) < OPTIONS_TOTAL - 1:
            # Вопрос не собрать — повтор кончается ИТОГОМ по отвеченному,
            # а не обрывом (разбор — у ветки обычного круга ниже)
            logger.warning("повтор ошибок: слово %s не собрать, завершаю итогом",
                           error_words[current_error_index])
            await _finish_quiz(callback, state, session, user, pair, lang, data)
            return

        # Повтор ошибок идёт текстом: человек уже не справился с этими
        # словами, и добавлять к разбору ещё и слух значит мешать две
        # трудности в одной попытке
        channel = QuizChannel.TEXT
        options, _ = build_options(word, distractors, pair)
        # Клип считается и здесь: без него ветка повтора ошибок падала бы на
        # `clip=clip` ниже с NameError — переменная задавалась только во
        # второй ветке. Ошибка такого рода не видна ни тестам на функции, ни
        # приёмке генератора: она живёт в потоке обработчика, а повтор ошибок
        # начинается лишь после круга, в котором ошибки были.
        clip = await _question_clip(session, user, word, pair, channel)
        await state.update_data(
            current_question=current_question,
            correct_word_id=word.id,
            current_error_index=current_error_index,
            asked_at=utcnow().timestamp(),
            channel=channel.value,
        )
    else:
        question = None
        for _ in range(QUESTION_ATTEMPTS):
            try:
                question = await generate_question(
                    session, user, exclude_ids=used_word_ids, pair=pair,
                    recent_channels=recent_channels,
                    prefer_channel=prefer_channel,
                    # Длина ЭТОГО круга и настоящий номер вопроса: в
                    # «сложных» круг короче настройки, а доска добавляет
                    # слов больше, чем вопросов
                    round_length=total_questions,
                    question_number=current_question,
                )
            except Exception:
                logger.exception("Ошибка генерации вопроса (user=%s)", user.id)
                # Упавший запрос оставляет сессию в состоянии «нужен
                # откат», и без него падало бы уже и завершение итогом
                await _recover(session, user)
                question = None
            if question:
                break

        if not question:
            # СЛОВА КОНЧИЛИСЬ — ЗАНЯТИЕ КОНЧАЕТСЯ ИТОГОМ, а не обрывом.
            # Прежде здесь было «Не удалось подготовить следующий вопрос» и
            # очистка состояния: отвеченное оставалось в базе, но ни итога,
            # ни баллов, ни повтора ошибок человек не получал, а на экране
            # висела мёртвая кнопка «Далее». Так обрывался круг «сложных
            # слов» (проверено исполнением: план 6, отвечено 3). Итог честен
            # и здесь: в нём ровно то, что отвечено.
            logger.warning(
                "вопрос %s из %s не собрать (user=%s) — завершаю итогом",
                current_question, total_questions, user.id,
            )
            await _finish_quiz(callback, state, session, user, pair, lang, data)
            return

        word = question["correct_word"]
        options = question["options"]
        channel = question["channel"]
        clip, channel, options = await _clip_or_text(
            session, user, word, pair, channel, options
        )
        used_word_ids.append(word.id)

        # ИСТОРИЯ КАНАЛОВ КРУГА ЦЕЛИКОМ, а не два последних.
        #
        # Прежде хранился хвост из двух: больше и не требовалось, правило
        # умело только «не три одинаковых подряд». Теперь состав круга
        # сходится к ДОЛЯМ (`place_in_round`), а доля — это «сколько уже
        # было», то есть вся история. Оставь хвост — и правило считало бы
        # долю по двум последним вопросам, то есть ни по чему.
        #
        # Обрезка по длине САМОГО КРУГА: дольше истории не бывает, а расти
        # бесконечно ей нельзя, если занятие почему-то не кончилось.
        recent_channels = (
            recent_channels + [channel.value]
        )[-max(1, total_questions):]

        await state.update_data(
            current_question=current_question,
            correct_word_id=word.id,
            used_word_ids=used_word_ids,
            asked_at=utcnow().timestamp(),
            channel=channel.value,
            recent_channels=recent_channels,
            **_build_state(question, channel),
        )

    await show_card(
        callback.bot, callback.message.chat.id, state, session,
        text=_question_text(
            word, pair, lang, current_question, total_questions,
            is_repeat=is_error_repeat, channel=channel,
        ),
        keyboard=_question_keyboard(channel, options, lang, word.id),
        clip=clip,
        word_id=word.id, lang=pair.learning,
        message=callback.message,
        without_audio=_as_text_question(
            session, user, word, pair, state, lang,
            current_question, total_questions, channel,
        ),
    )


# ============================================================================
# ПОВТОР ОШИБОК
# ============================================================================

@router.callback_query(F.data == "repeat_errors")
async def repeat_errors(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    # ОДИН ПОВТОР С ОДНОГО ИТОГА. Двойное нажатие заводило два занятия-
    # повтора, и первое оставалось брошенным (проверено исполнением: две
    # сессии `error_repeat`). Итог — своё сообщение, и его номер отмечается
    # под тем же замком чата, что ответы: второе нажатие по нему молча
    # гасится. Новый итог — новое сообщение, и его кнопка снова работает.
    async with _claim_lock(callback.message.chat.id):
        data = await state.get_data()
        if data.get(S_REPEAT_FROM) == callback.message.message_id:
            await callback.answer()
            return
        await state.update_data(**{S_REPEAT_FROM: callback.message.message_id})
    data = await state.get_data()
    errors = data.get("saved_errors", [])

    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or DEFAULT_LOCALE
    pair = pair_from_user(user)

    if not errors:
        await callback.message.answer(get_text("quiz_no_errors", lang))
        await callback.answer()
        return

    first_word = await session.get(Word, errors[0])
    if not first_word:
        await callback.message.answer(get_text("quiz_error_next", lang))
        await callback.answer()
        return

    distractors = await get_distractors(first_word, session, pair, user=user)
    if len(distractors) < OPTIONS_TOTAL - 1:
        await callback.message.answer(get_text("quiz_error_next", lang))
        await callback.answer()
        return

    quiz_session = _new_quiz_session(
        user, pair, len(errors), "error_repeat", source=SOURCE_REPEAT
    )
    session.add(quiz_session)
    await session.commit()

    options, _ = build_options(first_word, distractors, pair)

    await _reset_round_state(state)
    await state.update_data(
        session_id=quiz_session.id,
        current_question=1,
        total_questions=len(errors),
        correct_answers=0,
        errors=[],
        correct_word_id=first_word.id,
        error_words=errors,
        current_error_index=0,
        is_error_repeat=True,
        asked_at=utcnow().timestamp(),
        # Данные основной викторины нужны для репорта после повтора
        report_word_ids=data.get("report_word_ids", []),
        report_session_id=data.get("report_session_id"),
    )

    try:
        await callback.message.delete()
    except Exception:
        logger.debug("Не удалось удалить сообщение с итогами", exc_info=True)

    # Карточка с итогами уже удалена, поэтому message не передаём:
    # повтор ошибок начинается с новой карточки
    await show_card(
        callback.bot, callback.message.chat.id, state, session,
        text=_question_text(first_word, pair, lang, 1, len(errors), is_repeat=True),
        keyboard=get_answer_keyboard(options),
        clip=await _question_clip(session, user, first_word, pair, QuizChannel.TEXT),
        word_id=first_word.id, lang=pair.learning,
    )

    await state.set_state(QuizStates.answering)
    await callback.answer()
