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
from app.bot.handlers.quiz.lesson_state import _claim_answer
from app.core.clock import utcnow
from app.database.enums import QuizChannel
from app.database.models import User, Word
from app.locales import DEFAULT_LOCALE
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

