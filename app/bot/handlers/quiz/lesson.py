"""
Игровая логика викторины.

Не привязана к конкретному языку: что показывать и на каком языке давать
варианты, решает LanguagePair (изучаемый язык, язык значения, направление).

Учёт точности идёт по фактически отвеченным вопросам — answered_questions
пишется на каждый ответ. Плановое total_questions для точности не годится:
брошенная сессия иначе выглядит как сплошные ошибки.
"""

import logging
from datetime import timedelta
from typing import Optional

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from sqlalchemy import func, select

from app.services import journal
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.buttons import BTN_LEARN_WORDS, pressed
from app.bot.handlers.quiz.card import STATE_CARD_HAS_AUDIO, STATE_CARD_ID, show_card
from app.bot.handlers.quiz.lesson_state import (
    DEFAULT_QUIZ_LENGTH,
    S_ADVANCED,
    S_ANSWERED,
    S_BOARD_DONE,
    lesson_length,
    S_REPEAT_FROM,
    S_SPEECH_TRIES,
    _claim_advance,
    _claim_lock,
    _recover,
    _reset_round_state,
    _sweep_stray,
    shown_for,
    shown_state,
)
from app.bot.handlers.quiz.listen import _as_text_question, _clip_or_text, _question_clip
from app.bot.handlers.quiz.match import _board_due
from app.bot.handlers.quiz.question import (
    _answer_text,
    _build_state,
    _question_keyboard,
    _question_text,
    answer_keyboard,
)
from app.bot.handlers.quiz.sources import SOURCE_MENU, SOURCE_REPEAT, source_from_callback
from app.bot.handlers.quiz.summary import _finish_quiz
from app.bot.keyboards import get_answer_keyboard
from app.bot.states import QuizStates
from app.bot.utils import delete_messages_fast, ensure_anchor
from app.core.clock import utcnow
from app.database.enums import QuizChannel, QuizMode
from app.database.models import QuizQuestion, QuizSession, User, Word
from app.locales import DEFAULT_LOCALE, get_text
from app.services.audio_service import KIND_FULL, clip_for_user
from app.services.language_service import LanguagePair, legacy_mode_name, pair_from_user
from app.services.quiz_service import (
    FIRST_LESSON_LENGTH,
    OPTIONS_TOTAL,
    build_options,
    count_difficult_words,
    generate_question,
    get_distractors,
    update_word_progress,
)
from app.services.word_level import level_of

logger = logging.getLogger(__name__)


async def _level_note(session: AsyncSession, user: User, word: Word, pair: LanguagePair) -> dict:
    """
    Уровень слова в изучаемом языке и уровень человека — к вопросу в журнал.

    2.2.4: разбор 20.10 нашёл людям уровня A2 слова вроде verblüfft и
    Schlitzohr (38–50% верных против 88% у соседей). Как часто приходят слова
    чужого уровня, без этой пары не измерить.
    """
    own = await level_of(session, word, pair.learning)
    return {"lvl": getattr(own, "value", own),
            "ulvl": getattr(user.level, "value", user.level)}


router = Router()

# Сколько раз пытаться подобрать слово, прежде чем признать, что подходящих нет
QUESTION_ATTEMPTS = 10


# ============================================================================
# УТИЛИТЫ
# ============================================================================


# Пустое занятие моложе этого при новом старте — перезапуск, а не отвал
RESTART_WINDOW = timedelta(minutes=10)


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
        # БЕЗ ЕДИНОГО ОТВЕТА — НЕ ОТВАЛ, А ПЕРЕЗАПУСК. Прод 15.10: занятия,
        # начатые повторно через 1–4 секунды (карточка грузилась, человек
        # нажал ещё раз), считались брошенными на нулевом вопросе и
        # завышали отвалы новичков втрое. Блокировать второе нажатие нельзя:
        # человек мог уйти в меню и вернуться — владелец: «по логике верно,
        # новая игра». Поэтому новое занятие начинается как всегда, а
        # прежнее пустое помечается честно
        # Свежее — моложе десяти минут: открыл первую карточку и ушёл на
        # три дня — это настоящий отвал на нулевом вопросе, а не перезапуск
        fresh = stale.started_at and stale.started_at >= utcnow() - RESTART_WINDOW
        stale.exit_reason = (
            "restarted" if not stale.answered_questions and fresh else "abandoned"
        )
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



# ============================================================================
# НЕЗАКОНЧЕННОЕ ЗАНЯТИЕ: ПРОДОЛЖИТЬ ИЛИ НАЧАТЬ НОВОЕ
# ============================================================================

CB_RESUME = "lesson_resume"
CB_NEW = "lesson_new"


async def _open_lesson(state: FSMContext, session: AsyncSession,
                       user_id: int) -> Optional[tuple[int, int]]:
    """
    (пройдено, всего) открытого занятия, если его стоит предложить продолжить.

    Открытое — то, что живёт в состоянии (Redis, двое суток) и в базе ещё не
    закрыто. Предлагается, только если в нём есть хотя бы один ответ:
    пустое начинается заново, как раньше. Повтор ошибок не предлагается —
    он короткий и начинается из итога.
    """
    if await state.get_state() != QuizStates.answering.state:
        return None
    data = await state.get_data()
    session_id = data.get("session_id")
    current = data.get("current_question")
    total = data.get("total_questions")
    if not session_id or not current or not total or data.get("is_error_repeat"):
        return None
    quiz_session = await session.get(QuizSession, session_id)
    if (quiz_session is None or quiz_session.user_id != user_id
            or quiz_session.is_completed or quiz_session.exit_reason is not None
            or not quiz_session.answered_questions):
        return None
    # Текущий вопрос отвечен — пройден и он; нет — пройдено до него
    done = current if data.get(S_ANSWERED) == current else current - 1
    return min(max(done, 0), total), total


async def _offer_resume(message: Message, user: User, lang: str,
                        progress: tuple[int, int], source: str) -> None:
    """
    «У Вас незаконченное занятие: 5 из 15» и две кнопки. Ничего не закрыто:
    решает человек. Число вопросов — из самого круга (в «сложных» он короче
    настройки). Нажатие «Учить» человеком убирается, как и при обычном старте.
    """
    done, total = progress
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text("btn_lesson_resume", lang), callback_data=CB_RESUME)],
        [InlineKeyboardButton(text=get_text("btn_lesson_new", lang),
                              callback_data=f"{CB_NEW}:{source}")],
    ])
    await message.bot.send_message(
        message.chat.id, get_text("lesson_resume_prompt", lang, done=done, total=total),
        reply_markup=keyboard,
    )
    if message.from_user is not None and not message.from_user.is_bot:
        try:
            await message.delete()
        except Exception:
            logger.debug("Не удалось удалить сообщение пользователя", exc_info=True)


@router.callback_query(F.data == CB_RESUME)
async def resume_lesson(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    """
    «Продолжить» — тот же круг с того же места.

    Текущий вопрос отвечен — следующий; не отвечен — вопрос с тем же номером
    заново (слово подберётся новое: неотвеченное не в счёт). Прежняя карточка
    убирается ДО продвижения: её «Далее» иначе сдвинуло бы круг ещё раз.
    Занятие успело закрыться (двое суток, другой вход) — новое, как обычно.
    """
    await callback.answer()
    user_id = callback.from_user.id
    if await _open_lesson(state, session, user_id) is None:
        await start_lesson(callback.message, state, session, offer_resume=False)
        return
    data = await state.get_data()
    current = data["current_question"]
    old_card = data.get(STATE_CARD_ID)
    if old_card and old_card != callback.message.message_id:
        try:
            await callback.bot.delete_message(callback.message.chat.id, old_card)
        except Exception:
            logger.debug("прежняя карточка не удалилась", exc_info=True)
    # И ЭКРАНЫ МЕНЮ, ОТКРЫТЫЕ ПОСРЕДИ ЗАНЯТИЯ. Прод 18.10, владелец: начал
    # занятие, открыл «Статистику», нажал «Учить» → «Продолжить» — экран
    # статистики остался висеть над вопросом. Новое занятие убирает всё от
    # якоря до нажатия (`start_lesson`), продолжение не убирало ничего,
    # кроме своей карточки. Якорь остаётся: на нём живёт нижняя клавиатура;
    # «Продолжить?» — тоже: на его месте встанет вопрос
    user = await session.get(User, user_id)
    anchor_id = getattr(user, "anchor_message_id", None)
    if anchor_id:
        await delete_messages_fast(callback.bot, callback.message.chat.id,
                                   anchor_id + 1, callback.message.message_id)
    if data.get(S_ANSWERED) != current:
        # Неотвеченный вопрос показывается заново под тем же номером
        await state.update_data(current_question=current - 1, **{S_ADVANCED: None})
    if not await _claim_advance(state, callback.message.chat.id):
        return
    journal.note(session, user_id, "lesson", "resume", session_id=data.get("session_id"),
                 n=current)
    await _advance(callback, state, session)


@router.callback_query(F.data.startswith(CB_NEW))
async def new_lesson_instead(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    """«Начать новое» — прежнее закрывается как брошенное, новое с той же двери."""
    await callback.answer()
    source = source_from_callback(callback.data or "", default=SOURCE_MENU)
    journal.note(session, callback.from_user.id, "lesson", "new_instead")
    await start_lesson(callback.message, state, session, source=source, offer_resume=False)


def _build_slots(question: dict) -> int:
    """Сколько мест у фразы 🧱 — для верхней зоны сетки; у других игр 0."""
    puzzle = (question or {}).get("build")
    return len(puzzle.target) if puzzle is not None else 0

async def start_lesson(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
    *,
    prefer_channel: Optional[QuizChannel] = None,
    source: str = SOURCE_MENU,
    offer_resume: bool = True,
) -> None:
    """
    Начать занятие. Отсюда два входа, и оба нужны.

    НАЧАТОЕ НЕ ПРОПАДАЕТ (2.2.1). Если открыто занятие хотя бы с одним
    ответом, вместо нового — «Продолжить / Начать новое»: прод 14–18.10,
    28 из 84 «брошенных» — человек нажал «Учить» и начал заново за две
    минуты, а начатое пропадало без итога. Без ответов — новое сразу, как
    было (владелец: «если не было начатого — просто как сейчас»).
    `offer_resume=False` — это сама кнопка «Начать новое».

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

    if offer_resume:
        unfinished = await _open_lesson(state, session, user.id)
        if unfinished is not None:
            await _offer_resume(message, user, lang, unfinished, source)
            return

    await _close_abandoned_sessions(session, user.id)

    quiz_total = lesson_length(user)

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
        # Варианты, как их видел человек; у «Говорю» вариантов на экране нет
        **shown_state(word.id, question["options"] if channel is not QuizChannel.SPEECH else None,
                      ids=channel is not QuizChannel.BUILD),
    )

    old_anchor_id, _ = await ensure_anchor(message, session, user, emoji="")

    # Начало занятия — отдельной строкой (2.2.1): с какой двери и какой длины
    # круг, первый ли это урок. Пара к «finished» в итоге
    journal.note(session, user.id, "lesson", "started", session_id=quiz_session.id,
                 source=source, total=quiz_total,
                 first=quiz_total == FIRST_LESSON_LENGTH and not user.onboarded_at or None)
    journal.note(session, user.id, "question", channel.value, session_id=quiz_session.id,
                 word_id=word.id, channel=channel.value, n=1, total=quiz_total,
                 **await _level_note(session, user, word, pair))
    await show_card(
        message.bot, message.chat.id, state, session,
        text=_question_text(word, pair, lang, 1, quiz_total, channel=channel),
        keyboard=_question_keyboard(channel, question["options"], lang, word.id,
                                    slots=_build_slots(question)),
        clip=clip,
        word_id=word.id, lang=pair.learning,
        without_audio=_as_text_question(
            session, user, word, pair, state, lang, 1, quiz_total, channel
        ),
    )
    # Прежние сообщения убираются ПОСЛЕДНИМИ, когда новый экран уже на
    # месте: иначе, пока он готовится (статистика — запросы к базе,
    # занятие — загрузка звука), на экране один якорь. Владелец, 15.10:
    # «рейтинг и настройки более плавно работают». Диапазон удаления —
    # от прежнего якоря до нажатия человека, новых сообщений он не задевает
    if old_anchor_id:
        await delete_messages_fast(message.bot, message.chat.id, old_anchor_id, message.message_id)
    # И само сообщение, с которого начали: нажатие «Учить» или домашний
    # экран / напоминание, на месте которого встаёт занятие, — тоже после
    try:
        await message.delete()
    except Exception:
        logger.debug("Не удалось удалить сообщение пользователя", exc_info=True)
    await state.set_state(QuizStates.answering)


async def _record_answer(
    *, bot, chat_id, state, session, user, pair, lang,
    correct_word, is_correct, channel, answer_text,
    session_id, correct_answers, errors, response_seconds,
    card_message=None, card_message_id=None, forgiven: bool = False,
    breakdown: Optional[str] = None,
    chosen_word_id: Optional[int] = None,
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
    # Варианты — из состояния ЭТОГО вопроса: `shown_for` сверяет номер слова
    shown = shown_for(await state.get_data(), correct_word_id)

    session.add(
        QuizQuestion(
            session_id=session_id,
            word_id=correct_word_id,
            user_answer=(answer_text or "")[:255] or None,
            options=shown,
            chosen_word_id=chosen_word_id,
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

    # ПЕРВЫЙ УРОК КОНЧАЕТСЯ И БЕЗ ЗАКОНЧЕННОГО ЗАНЯТИЯ — на 7-м ответе всего,
    # в каких бы занятиях они ни были. Владелец: «даже если он его сбросит —
    # чтобы открывалась полноценная игра после первого круга»
    if getattr(user, "onboarded_at", None) is None:
        answered = (await session.execute(
            select(func.count()).select_from(QuizQuestion)
            .join(QuizSession, QuizSession.id == QuizQuestion.session_id)
            .where(QuizSession.user_id == user.id)
        )).scalar() or 0
        if answered >= FIRST_LESSON_LENGTH:
            user.onboarded_at = utcnow()

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
    clip = await clip_for_user(session, user, correct_word, pair.learning, KIND_FULL)
    await show_card(
        bot, chat_id, state, session,
        text=breakdown or _answer_text(correct_word, pair, lang, is_correct, channel),
        keyboard=answer_keyboard(lang, correct_word, pair, channel, heard=clip is not None),
        clip=clip,
        word_id=correct_word.id, lang=pair.learning,
        message=card_message,
    )


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

    # Сначала новое, потом удаление прежнего: иначе между ними на экране
    # один якорь (владелец, 15.10: «пропадает карточка и остаётся якорь,
    # как в начале, так и в конце»)
    shown = await start_board(callback.message, state, session, user, quiet=True,
                              in_round=True)
    if shown:
        try:
            await callback.message.delete()
        except Exception:
            logger.debug("карточка перед доской не удалилась", exc_info=True)
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


async def _errors_of_last_lesson(session: AsyncSession, user_id: int) -> list[int]:
    """Слова с неверным ответом в последнем законченном занятии, по порядку."""
    last = (await session.execute(
        select(QuizSession.id).where(QuizSession.user_id == user_id,
                                     QuizSession.is_completed.is_(True))
        .order_by(QuizSession.completed_at.desc()).limit(1)
    )).scalar()
    if last is None:
        return []
    rows = (await session.execute(
        select(QuizQuestion.word_id).where(QuizQuestion.session_id == last,
                                           QuizQuestion.is_correct.is_(False))
        .order_by(QuizQuestion.id)
    )).scalars().all()
    return list(dict.fromkeys(rows))


@router.callback_query(F.data == "next_question", QuizStates.answering)
async def show_next_question(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    await callback.answer()
    # «ДАЛЕЕ» — ТОЛЬКО С ОТВЕЧЕННОГО ВОПРОСА. Прод 18.10, владелец: «Далее»
    # грузилось 5,6 с (карточка «Говорю»), он нажал ещё раз — и вопрос 12
    # пропустился, не показавшись. Номер вопроса в состоянии уже стал 12, а
    # `_claim_advance` помнил лишь «с 11 уже шли», и второе нажатие той же
    # старой кнопки продвинуло круг с 12. Кнопка «Далее» бывает только под
    # разбором, то есть после ответа, пропуска или доски — все они отмечают
    # вопрос (`S_ANSWERED`); неотвеченный текущий значит, что нажата
    # прежняя кнопка. «Продолжить» сюда не ходит: у него своя проверка
    data = await state.get_data()
    current = data.get("current_question")
    if current is not None and data.get(S_ANSWERED) != current:
        return
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
        # Вопроса-словаря у повтора нет: `_build_slots` читает его ниже
        question = None
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
            **shown_state(word.id, options),
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
            # Варианты, как их видел человек; у «Говорю» вариантов на экране нет
        **shown_state(word.id, options if channel is not QuizChannel.SPEECH else None,
                      ids=channel is not QuizChannel.BUILD),
        )

    journal.note(session, user.id, "question", channel.value, session_id=data.get("session_id"),
                 word_id=word.id, channel=channel.value, n=current_question,
                 total=total_questions, repeat=is_error_repeat or None,
                 **await _level_note(session, user, word, pair))
    await show_card(
        callback.bot, callback.message.chat.id, state, session,
        text=_question_text(
            word, pair, lang, current_question, total_questions,
            is_repeat=is_error_repeat, channel=channel,
        ),
        keyboard=_question_keyboard(channel, options, lang, word.id,
                                    slots=_build_slots(question)),
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
    errors = data.get("saved_errors")
    if errors is None:
        # Состояния нет (Redis хранит его 2 дня, итог мог быть старше) —
        # ошибки берутся из базы, из последнего законченного занятия.
        # Прежде отвечалось «У Вас не было ошибок!» — неправда (аудит 2.1)
        errors = await _errors_of_last_lesson(session, callback.from_user.id)

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
        **shown_state(first_word.id, options),
    )

    # Повтор ошибок начинается с новой карточки (message не передаём), и
    # итог удаляется ПОСЛЕ неё.
    # Сначала новое, потом удаление прежнего: иначе между ними на экране
    # один якорь (владелец, 15.10: «пропадает карточка и остаётся якорь,
    # как в начале, так и в конце»)
    journal.note(session, user.id, "question", QuizChannel.TEXT.value, session_id=quiz_session.id,
                 word_id=first_word.id, channel=QuizChannel.TEXT.value, n=1,
                 total=len(errors), repeat=True,
                 **await _level_note(session, user, first_word, pair))
    await show_card(
        callback.bot, callback.message.chat.id, state, session,
        text=_question_text(first_word, pair, lang, 1, len(errors), is_repeat=True),
        keyboard=get_answer_keyboard(options),
        clip=await _question_clip(session, user, first_word, pair, QuizChannel.TEXT),
        word_id=first_word.id, lang=pair.learning,
    )
    try:
        await callback.message.delete()
    except Exception:
        logger.debug("Не удалось удалить сообщение с итогами", exc_info=True)

    await state.set_state(QuizStates.answering)
    await callback.answer()
