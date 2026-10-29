"""
Ответ кнопкой: «📖 Читаю», «💭 Вспоминаю», «🎧 Слышу».

Три игры обслуживает ОДИН обработчик: различаются они видом вопроса и
разбора (`question.py`), а нажатие на вариант у всех одно и то же.

Вынесено из `game.py` переносом, без правок поведения.
"""

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.states import QuizStates
from app.bot.handlers.quiz.lesson import _record_answer
from app.bot.handlers.quiz.lesson_state import _claim_answer, answered_by_dead_process
from app.core.clock import utcnow
from app.database.enums import QuizChannel
from app.database.models import User, Word
from app.locales import DEFAULT_LOCALE, get_text
from app.bot.handlers.quiz.question import _answer_text, get_next_question_keyboard
from app.services.language_service import (
    pair_for_channel,
    option_label,
    pair_from_user,
)

router = Router()


# ============================================================================
# ОБРАБОТКА ОТВЕТА
# ============================================================================

@router.callback_query(F.data.startswith("answer_"), QuizStates.answering)
async def process_answer(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    selected_word_id = int(callback.data.split("_")[1])

    # ОДИН ВОПРОС — ОДИН ОТВЕТ. Разбор у `_claim_answer`: двойной тык и
    # нажатие по не перерисовавшейся карточке записывали вопрос дважды, и
    # балл начислялся дважды
    if not await _claim_answer(state, callback.message.chat.id, session):
        await callback.answer()
        # Ответ записан процессом, умершим до разбора: «Далее» на экране нет
        if await answered_by_dead_process(state, session):
            user = await session.get(User, callback.from_user.id)
            lang = (user.interface_language if user else None) or DEFAULT_LOCALE
            await callback.message.answer(get_text("quiz_answer_already_counted", lang),
                                          reply_markup=get_next_question_keyboard(lang))
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
        chosen_word_id=selected_word_id,
        session_id=session_id, correct_answers=correct_answers, errors=errors,
        response_seconds=response_seconds,
    )
    await callback.answer()



# ============================================================================
# DER / DIE / DAS
# ============================================================================

@router.callback_query(F.data.startswith("art_"), QuizStates.answering)
async def process_article(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    """
    Ответ на вопрос об артикле (`quiz_service.wants_article`). Это карточка
    «Читаю» знакомого существительного: засчитывается как она, а выбранный
    вариант — артикль, не слово, поэтому `chosen_word_id` пуст и путаница
    слов (`note_confusion`) здесь не считается.
    """
    picked = callback.data.removeprefix("art_")
    if not await _claim_answer(state, callback.message.chat.id, session):
        await callback.answer()
        if await answered_by_dead_process(state, session):
            user = await session.get(User, callback.from_user.id)
            lang = (user.interface_language if user else None) or DEFAULT_LOCALE
            await callback.message.answer(get_text("quiz_answer_already_counted", lang),
                                          reply_markup=get_next_question_keyboard(lang))
        return

    data = await state.get_data()
    correct_word = await session.get(Word, data["correct_word_id"])
    user = await session.get(User, callback.from_user.id)
    if not correct_word or not user or not data.get("article"):
        await callback.answer("Error", show_alert=True)
        await state.clear()
        return

    asked_at = data.get("asked_at")
    await _record_answer(
        bot=callback.bot, chat_id=callback.message.chat.id, state=state,
        session=session, user=user, pair=pair_from_user(user),
        lang=user.interface_language or DEFAULT_LOCALE,
        correct_word=correct_word, is_correct=picked == correct_word.article,
        channel=QuizChannel.TEXT, answer_text=picked, card_message=callback.message,
        session_id=data["session_id"], correct_answers=data["correct_answers"],
        errors=data["errors"],
        response_seconds=max(0, int(utcnow().timestamp() - float(asked_at))) if asked_at else None,
    )
    await callback.answer()


# ============================================================================
# ОТВЕТ ВВОДОМ
# ============================================================================

async def process_typed(message, state: FSMContext, session: AsyncSession) -> None:
    """
    Слово, написанное в «Вспоминаю» выученного слова (`quiz_service.wants_typed`).

    Вызывается из общего обработчика текста во время вопроса
    (`speech.hint_to_speak`): подписка на любой текст там уже стоит и
    пропускает нажатия меню, и вторая такая же подписка в другом роутере
    гасила бы их снова.

    Сравнение — `typed_answer.judge`: опечатка в длинном слове засчитывается,
    неверный артикль — нет. Верные — все варианты ячейки изучаемого языка.
    """
    from app.bot.handlers.quiz.card import STATE_CARD_ID
    from app.services.language_service import meaning_variants, word_text
    from app.services.typed_answer import Verdict, judge, mark_mistakes

    if not await _claim_answer(state, message.chat.id, session):
        return
    data = await state.get_data()
    word = await session.get(Word, data.get("correct_word_id"))
    user = await session.get(User, message.from_user.id)
    if not word or not user:
        return
    pair = pair_from_user(user)
    written = word_text(word, pair.learning, with_article=False)
    variants = set(meaning_variants(written, pair.learning)) or {written}
    article = word.article if pair.learning == "de" else None
    verdict = judge(message.text or "", variants, pair.learning, article)
    lang = user.interface_language or DEFAULT_LOCALE
    # Ошибка или опечатка — в разборе написанное с подчёркнутыми ошибками,
    # как во фразе сборки (владелец, 29.10.2026)
    breakdown = None
    if verdict is not Verdict.EXACT:
        breakdown = _answer_text(
            word, pair, lang, verdict is Verdict.CLOSE, QuizChannel.REVERSE,
            yours=mark_mistakes(message.text or "", variants, pair.learning, article),
            typo=verdict is Verdict.CLOSE,
        )
    asked_at = data.get("asked_at")
    await _record_answer(
        bot=message.bot, chat_id=message.chat.id, state=state, session=session,
        user=user, pair=pair, lang=lang,
        correct_word=word, is_correct=verdict is not Verdict.WRONG,
        channel=QuizChannel.REVERSE, answer_text=(message.text or "")[:255],
        session_id=data["session_id"], correct_answers=data["correct_answers"],
        errors=data["errors"],
        response_seconds=max(0, int(utcnow().timestamp() - float(asked_at))) if asked_at else None,
        card_message_id=data.get(STATE_CARD_ID), breakdown=breakdown,
    )


@router.callback_query(F.data == "typed_skip", QuizStates.answering)
async def typed_skip(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    """«Не помню» в ответе вводом — честный промах: слово вернётся первым."""
    if not await _claim_answer(state, callback.message.chat.id, session):
        await callback.answer()
        return
    data = await state.get_data()
    word = await session.get(Word, data.get("correct_word_id"))
    user = await session.get(User, callback.from_user.id)
    if not word or not user or not data.get("typed"):
        await callback.answer("Error", show_alert=True)
        return
    asked_at = data.get("asked_at")
    await _record_answer(
        bot=callback.bot, chat_id=callback.message.chat.id, state=state, session=session,
        user=user, pair=pair_from_user(user), lang=user.interface_language or DEFAULT_LOCALE,
        correct_word=word, is_correct=False, channel=QuizChannel.REVERSE, answer_text=None,
        card_message=callback.message,
        session_id=data["session_id"], correct_answers=data["correct_answers"],
        errors=data["errors"],
        response_seconds=max(0, int(utcnow().timestamp() - float(asked_at))) if asked_at else None,
    )
    await callback.answer()
