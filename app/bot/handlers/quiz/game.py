"""
Игровая логика викторины.

Не привязана к конкретному языку: что показывать и на каком языке давать
варианты, решает LanguagePair (изучаемый язык, язык значения, направление).

Учёт точности идёт по фактически отвеченным вопросам — answered_questions
пишется на каждый ответ. Плановое total_questions для точности не годится:
брошенная сессия иначе выглядит как сплошные ошибки.
"""

import logging
from datetime import date, timedelta

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.buttons import BTN_LEARN_WORDS, pressed
from app.bot.keyboards import get_answer_keyboard
from app.bot.states import QuizStates
from app.bot.handlers.quiz.card import show_card
from app.bot.utils import delete_messages_fast, ensure_anchor
from app.services.audio_service import (
    KIND_FULL,
    clip_for_user,
    clip_kind_for_question,
)
from app.core.clock import utcnow
from app.database.enums import QuizMode
from app.database.models import QuizQuestion, QuizSession, User, UserWord, Word
from app.locales import get_text
from app.services.language_service import (
    LanguagePair,
    display_text,
    example_text,
    flag,
    legacy_mode_name,
    pair_from_user,
    word_text,
)
from app.services.monthly_leaderboard_service import update_monthly_stats
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

DEFAULT_QUIZ_LENGTH = 25
# Сколько раз пытаться подобрать слово, прежде чем признать, что подходящих нет
QUESTION_ATTEMPTS = 10


# ============================================================================
# ОТОБРАЖЕНИЕ ВОПРОСА И ОТВЕТА
# ============================================================================

async def _question_clip(session, user: User, word: Word, pair: LanguagePair):
    """
    Озвучка для вопроса.

    В обратном направлении звука нет: вопрос задан на языке значения, а
    произнести изучаемое слово означало бы назвать ответ.

    В прямом направлении звучит слово. Исключение — гетероним: произнесённый
    отдельно, он читается наугад («modern», «umfahren» имеют по два чтения),
    и управлять этим нельзя, SSML движку недоступен. Такому слову ставится
    клип с примером, где контекст задаёт чтение однозначно.
    """
    if pair.reverse:
        return None
    return await clip_for_user(
        session, user, word, pair.learning, clip_kind_for_question(word, pair.learning)
    )


def _question_text(
    word: Word,
    pair: LanguagePair,
    lang: str,
    current: int,
    total: int,
    *,
    is_repeat: bool = False,
) -> str:
    """
    Вопрос: слово на языке вопроса + пример на том же языке.

    При прямом направлении спрашиваем значение изучаемого слова, при
    обратном — само слово по значению.
    """
    prompt = display_text(word, pair.prompt_lang)
    example = example_text(word, pair.prompt_lang)

    prefix = f"{get_text('quiz_repeat_title', lang)}\n" if is_repeat else ""
    task_key = "quiz_question_choose_word" if pair.reverse else "quiz_question_choose_translation"

    parts = [
        prefix,
        get_text("quiz_question_number", lang, current=current, total=total),
        "\n\n",
        f"{pair.prompt_flag} <b>{prompt}</b>\n\n",
    ]
    if example:
        parts.append(f"📝 {example}\n\n")
    parts.append(get_text(task_key, lang))

    return "".join(parts)


def _answer_text(word: Word, pair: LanguagePair, lang: str, is_correct: bool) -> str:
    """
    Разбор ответа: пара «вопрос = ответ» и примеры на оба языка.

    Порядок сторон совпадает с направлением вопроса — сначала то, что
    спрашивали, потом ответ.
    """
    prompt_lang, answer_lang = pair.prompt_lang, pair.answer_lang

    header = (
        get_text("quiz_correct", lang)
        if is_correct
        else f"{get_text('quiz_wrong', lang)}\n\n{get_text('quiz_correct_answer', lang)}"
    )

    lines = [
        header,
        "\n\n",
        f"{flag(prompt_lang)} <b>{display_text(word, prompt_lang)}</b>"
        f" = {flag(answer_lang)} <b>{display_text(word, answer_lang)}</b>",
    ]

    # Примеры всегда в порядке «изучаемый язык, затем язык значения»
    learning_example = example_text(word, pair.learning)
    native_example = example_text(word, pair.native)
    if learning_example:
        lines.append(f"\n\n{flag(pair.learning)} {learning_example}")
    if native_example:
        lines.append(f"\n{flag(pair.native)} {native_example}")

    return "".join(lines)


def get_next_question_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=get_text("quiz_btn_next", lang), callback_data="next_question")]
        ]
    )


def get_results_keyboard(has_errors: bool, lang: str = "ru") -> InlineKeyboardMarkup:
    buttons = []

    if has_errors:
        buttons.append([
            InlineKeyboardButton(
                text=get_text("quiz_btn_repeat_errors", lang),
                callback_data="repeat_errors",
            )
        ])

    buttons.append([
        InlineKeyboardButton(
            text=get_text("quiz_btn_change_mode", lang),
            callback_data="settings_quiz_mode",
        )
    ])
    buttons.append([
        InlineKeyboardButton(
            text=get_text("quiz_btn_report_error", lang),
            callback_data="report_translation_error",
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


# ============================================================================
# УТИЛИТЫ
# ============================================================================

async def update_user_activity(session: AsyncSession, user_id: int) -> None:
    """Стрик активных дней — обновляется при завершении викторины."""
    user = await session.get(User, user_id)
    today = date.today()

    if user.last_active_date == today:
        return
    if user.last_active_date == today - timedelta(days=1):
        user.streak_days += 1
    else:
        user.streak_days = 1

    user.last_active_date = today
    await session.commit()


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


def _new_quiz_session(user: User, pair: LanguagePair, total: int, quiz_mode: str) -> QuizSession:
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
        start_source="menu",
    )


# ============================================================================
# СТАРТ ВИКТОРИНЫ
# ============================================================================

@router.message(Command("quiz"))
@router.message(pressed(BTN_LEARN_WORDS))
async def start_quiz(message: Message, state: FSMContext, session: AsyncSession):
    user = await session.get(User, message.from_user.id)

    if not user or not user.level:
        lang = user.interface_language if user else "ru"
        await message.answer(get_text("quiz_no_level", lang))
        return

    lang = user.interface_language or "ru"
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
        question = await generate_question(session, user, exclude_ids=[], pair=pair)
    except Exception:
        logger.exception("Ошибка генерации первого вопроса (user=%s)", user.id)
        await message.answer(get_text("quiz_error_generation", lang))
        return

    if not question:
        await message.answer(get_text("quiz_no_words", lang))
        return

    quiz_session = _new_quiz_session(
        user, pair, quiz_total, user.quiz_mode.value if user.quiz_mode else "level"
    )
    session.add(quiz_session)
    await session.commit()

    word = question["correct_word"]

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
    )

    try:
        await message.delete()
    except Exception:
        logger.debug("Не удалось удалить сообщение пользователя", exc_info=True)

    old_anchor_id, _ = await ensure_anchor(message, session, user, emoji="📚")
    if old_anchor_id:
        await delete_messages_fast(message.bot, message.chat.id, old_anchor_id, message.message_id)

    await show_card(
        message.bot, message.chat.id, state, session,
        text=_question_text(word, pair, lang, 1, quiz_total),
        keyboard=get_answer_keyboard(question["options"]),
        clip=await _question_clip(session, user, word, pair),
        word_id=word.id, lang=pair.learning,
    )
    await state.set_state(QuizStates.answering)


# ============================================================================
# ОБРАБОТКА ОТВЕТА
# ============================================================================

@router.callback_query(F.data.startswith("answer_"), QuizStates.answering)
async def process_answer(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    selected_word_id = int(callback.data.split("_")[1])

    data = await state.get_data()
    correct_word_id = data["correct_word_id"]
    session_id = data["session_id"]
    correct_answers = data["correct_answers"]
    errors = data["errors"]

    correct_word = await session.get(Word, correct_word_id)
    user = await session.get(User, callback.from_user.id)

    if not correct_word or not user:
        await callback.answer("❌ Error", show_alert=True)
        await state.clear()
        return

    lang = user.interface_language or "ru"
    pair = pair_from_user(user)
    is_correct = selected_word_id == correct_word_id

    # Что именно выбрал пользователь — по этому видно, какие неверные варианты
    # притягивают. Прежде колонка не заполнялась, и разбирать ошибки было нечем.
    selected_word = correct_word if is_correct else await session.get(Word, selected_word_id)
    selected_text = word_text(selected_word, pair.answer_lang) if selected_word else None

    asked_at = data.get("asked_at")
    response_seconds = None
    if asked_at:
        response_seconds = max(0, int(utcnow().timestamp() - float(asked_at)))

    session.add(
        QuizQuestion(
            session_id=session_id,
            word_id=correct_word_id,
            user_answer=(selected_text or "")[:255] or None,
            is_correct=is_correct,
            answered_at=utcnow(),
            response_time_seconds=response_seconds,
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
        )
    except Exception:
        logger.exception("Ошибка обновления прогресса (user=%s word=%s)", user.id, correct_word_id)

    if is_correct:
        correct_answers += 1
    else:
        errors.append(correct_word_id)

    await state.update_data(correct_answers=correct_answers, errors=errors)

    # На разборе звучит слово с примером: значение уже известно, и теперь
    # слышно, как слово живёт в живой речи. В вопросе примера в звуке нет —
    # там его было бы не разобрать.
    await show_card(
        callback.bot, callback.message.chat.id, state, session,
        text=_answer_text(correct_word, pair, lang, is_correct),
        keyboard=get_next_question_keyboard(lang),
        clip=await clip_for_user(session, user, correct_word, pair.learning, KIND_FULL),
        word_id=correct_word.id, lang=pair.learning,
        message=callback.message,
    )
    await callback.answer()


# ============================================================================
# СЛЕДУЮЩИЙ ВОПРОС / ЗАВЕРШЕНИЕ
# ============================================================================

@router.callback_query(F.data == "next_question", QuizStates.answering)
async def show_next_question(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    await callback.answer()

    data = await state.get_data()
    current_question = data["current_question"] + 1
    total_questions = data["total_questions"]
    used_word_ids = data.get("used_word_ids", [])

    is_error_repeat = data.get("is_error_repeat", False)
    error_words = data.get("error_words", [])
    current_error_index = data.get("current_error_index", 0)

    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or "ru"
    pair = pair_from_user(user)

    if current_question > total_questions:
        await _finish_quiz(callback, state, session, user, pair, lang, data)
        return

    if is_error_repeat:
        current_error_index += 1
        if current_error_index >= len(error_words):
            logger.warning("error_repeat: индекс вышел за пределы списка ошибок")
            await state.clear()
            return

        word = await session.get(Word, error_words[current_error_index])
        if not word:
            await callback.message.answer(get_text("quiz_error_generate", lang))
            await state.clear()
            return

        distractors = await get_distractors(word, session, pair, user=user)
        if len(distractors) < OPTIONS_TOTAL - 1:
            await callback.message.answer(get_text("quiz_error_generate", lang))
            await state.clear()
            return

        options, _ = build_options(word, distractors, pair)
        await state.update_data(
            current_question=current_question,
            correct_word_id=word.id,
            current_error_index=current_error_index,
            asked_at=utcnow().timestamp(),
        )
    else:
        question = None
        for _ in range(QUESTION_ATTEMPTS):
            try:
                question = await generate_question(
                    session, user, exclude_ids=used_word_ids, pair=pair
                )
            except Exception:
                logger.exception("Ошибка генерации вопроса (user=%s)", user.id)
                question = None
            if question:
                break

        if not question:
            await callback.message.answer(get_text("quiz_error_generate", lang))
            await state.clear()
            return

        word = question["correct_word"]
        options = question["options"]
        used_word_ids.append(word.id)

        await state.update_data(
            current_question=current_question,
            correct_word_id=word.id,
            used_word_ids=used_word_ids,
            asked_at=utcnow().timestamp(),
        )

    await show_card(
        callback.bot, callback.message.chat.id, state, session,
        text=_question_text(
            word, pair, lang, current_question, total_questions, is_repeat=is_error_repeat
        ),
        keyboard=get_answer_keyboard(options),
        clip=await _question_clip(session, user, word, pair),
        word_id=word.id, lang=pair.learning,
        message=callback.message,
    )


async def _finish_quiz(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
    user: User,
    pair: LanguagePair,
    lang: str,
    data: dict,
) -> None:
    """Завершение викторины: итоги, статистика, кнопки."""
    session_id = data["session_id"]
    correct_answers = data["correct_answers"]
    errors = data.get("errors", [])
    is_error_repeat = data.get("is_error_repeat", False)

    quiz_session = await session.get(QuizSession, session_id)
    if quiz_session:
        quiz_session.completed_at = utcnow()
        quiz_session.is_completed = True
        quiz_session.exit_reason = "completed"
        quiz_session.exit_at_question = quiz_session.answered_questions
        await session.commit()

    answered = quiz_session.answered_questions if quiz_session else 0

    if not is_error_repeat:
        user.quizzes_passed = (user.quizzes_passed or 0) + 1
        user.last_quiz_date = date.today()
        if user.first_quiz_at is None:
            user.first_quiz_at = utcnow()

        learned_count = await session.execute(
            select(func.count())
            .select_from(UserWord)
            .where(
                UserWord.user_id == user.id,
                UserWord.learning_lang == pair.learning,
                UserWord.learned.is_(True),
            )
        )
        user.words_learned = int(learned_count.scalar() or 0)

        # Общая точность — по фактически отвеченным вопросам
        totals = await session.execute(
            select(
                func.coalesce(func.sum(QuizSession.answered_questions), 0),
                func.coalesce(func.sum(QuizSession.correct_answers), 0),
            ).where(
                QuizSession.user_id == user.id,
                QuizSession.completed_at.isnot(None),
            )
        )
        total_answered, total_correct = totals.one()
        user.success_rate = int(total_correct / total_answered * 100) if total_answered else 0

        await session.commit()

        try:
            await update_monthly_stats(
                user_id=user.id, session=session, quiz_session_id=session_id
            )
        except Exception:
            logger.exception("Ошибка обновления месячной статистики (user=%s)", user.id)

        await update_user_activity(session, user.id)

    # Разбор по словам
    result_items = await session.execute(
        select(QuizQuestion, Word)
        .join(Word, QuizQuestion.word_id == Word.id)
        .where(QuizQuestion.session_id == session_id)
        .order_by(QuizQuestion.answered_at)
    )
    items = result_items.all()

    details = []
    for item, word in items:
        icon = "✅" if item.is_correct else "❌"
        details.append(
            f"{icon} {display_text(word, pair.learning)} — {display_text(word, pair.native)}"
        )

    percentage = (correct_answers / answered * 100) if answered else 0.0

    prefix = "🔄 " if is_error_repeat else ""
    result_text = (
        f"{prefix}{get_text('quiz_completed', lang)}\n\n"
        f"{get_text('quiz_result_correct', lang, correct=correct_answers, total=answered)}\n"
        f"{get_text('quiz_result_percentage', lang, percentage=f'{percentage:.1f}')}\n\n"
        f"{get_text('quiz_result_details', lang)}\n" + "\n".join(details)
    )

    if errors and not is_error_repeat:
        result_text += "\n\n" + get_text("quiz_result_errors", lang, count=len(errors))

    try:
        await callback.message.delete()
    except Exception:
        logger.debug("Не удалось удалить сообщение с вопросом", exc_info=True)

    await callback.bot.send_message(
        chat_id=callback.message.chat.id,
        text=result_text,
        reply_markup=get_results_keyboard(has_errors=bool(errors), lang=lang),
    )

    # Данные для повтора ошибок и репорта. После повтора ошибок сохраняем
    # список слов ОСНОВНОЙ викторины — репортить нужно её содержимое.
    saved_errors = list(errors)
    old_report_word_ids = data.get("report_word_ids", [])
    old_report_session_id = data.get("report_session_id")

    await state.clear()

    if is_error_repeat:
        await state.update_data(
            saved_errors=saved_errors,
            report_session_id=old_report_session_id,
            report_word_ids=old_report_word_ids,
        )
    else:
        await state.update_data(
            saved_errors=saved_errors,
            report_session_id=session_id,
            report_word_ids=[w.id for _, w in items],
        )


# ============================================================================
# ПОВТОР ОШИБОК
# ============================================================================

@router.callback_query(F.data == "repeat_errors")
async def repeat_errors(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    errors = data.get("saved_errors", [])

    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or "ru"
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

    quiz_session = _new_quiz_session(user, pair, len(errors), "error_repeat")
    session.add(quiz_session)
    await session.commit()

    options, _ = build_options(first_word, distractors, pair)

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
        clip=await _question_clip(session, user, first_word, pair),
        word_id=first_word.id, lang=pair.learning,
    )

    await state.set_state(QuizStates.answering)
    await callback.answer()
