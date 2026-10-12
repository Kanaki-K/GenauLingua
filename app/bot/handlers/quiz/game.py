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
from typing import Optional

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    BufferedInputFile, CallbackQuery, InlineKeyboardButton,
    InlineKeyboardMarkup, Message,
)
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.buttons import BTN_LEARN_WORDS, menu_texts, pressed
from app.bot.keyboards import get_answer_keyboard
from app.bot.states import QuizStates
from app.bot.handlers.quiz.card import STATE_CARD_HAS_AUDIO, STATE_CARD_ID, show_card
from app.bot.utils import delete_messages_fast, ensure_anchor
from app.services.audio_service import (
    AUDIO_PERFORMER,
    KIND_FULL,
    KIND_WORD,
    clip_for_user,
    clip_kind_for_question,
    remember,
    spoken_for,
)
from app.services.speech_check import check_pronunciation
from app.core.clock import utcnow, utctoday
from app.database.enums import QuizChannel, QuizMode
from app.database.models import QuizQuestion, QuizSession, User, UserWord, Word
from app.locales import DEFAULT_LOCALE, get_text
from app.services.language_service import (
    LanguagePair,
    option_label,
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

DEFAULT_QUIZ_LENGTH = 15
# Сколько раз пытаться подобрать слово, прежде чем признать, что подходящих нет
QUESTION_ATTEMPTS = 10


# ============================================================================
# ОТОБРАЖЕНИЕ ВОПРОСА И ОТВЕТА
# ============================================================================

async def _question_clip(
    session, user: User, word: Word, pair: LanguagePair,
    channel: QuizChannel = QuizChannel.TEXT,
):
    """
    Озвучка для вопроса.

    НА СЛУХ КЛИП — ЭТО И ЕСТЬ ВОПРОС, и направление на него не влияет.
    Обратного порядка у слушания не существует: звучит изучаемый язык, из
    него и выбирают. Поэтому ветка `pair.reverse` сюда не распространяется —
    без клипа такой вопрос попросту пуст.

    В текстовом вопросе в обратном направлении звука нет: вопрос задан на
    языке значения, а произнести изучаемое слово означало бы назвать ответ.

    В прямом направлении звучит слово. Исключение — гетероним: произнесённый
    отдельно, он читается наугад («modern», «umfahren» имеют по два чтения),
    и управлять этим нельзя, SSML движку недоступен. Такому слову ставится
    клип с примером, где контекст задаёт чтение однозначно.
    """
    if channel is QuizChannel.AUDIO:
        # ВСЕГДА ОДНО СЛОВО, даже для гетеронима.
        #
        # Карточке клип с примером нужен: там слово видно, и прочитанное
        # наугад («live» как /lɪv/ или /laɪv/) учило бы неверному
        # произношению. На слух этой беды нет — оба чтения ПИШУТСЯ
        # одинаково, а спрашивают тут именно написание.
        #
        # Зато вред от примера настоящий: 109 рядов проигрывали бы целое
        # предложение — «to live … We like living in this city» — при
        # вариантах из одного слова. Это другая задача, заметно более
        # лёгкая, и соседние вопросы круга оказывались бы разной трудности
        # без всякой причины.
        return await clip_for_user(session, user, word, pair.learning, KIND_WORD)
    if pair.reverse:
        return None
    return await clip_for_user(
        session, user, word, pair.learning, clip_kind_for_question(word, pair.learning)
    )


async def _clip_or_text(
    session, user: User, word: Word, pair: LanguagePair, channel: QuizChannel,
    options: list,
):
    """
    Клип для вопроса, а если его нет — ПЕРЕСОБРАТЬ вопрос текстом.

    Вопрос на слух держится на звуке: самого слова на экране нет, его
    заменяет клип. Если клип не пришёл, на экране остаётся «Послушай и
    выбери» и четыре варианта — вопрос без вопроса, на который можно только
    ткнуть наугад.

    Клип не приходит по трём причинам, и все три настоящие: ученик выключил
    озвучку (это уже отсекается составом занятия), клипа нет на диске для
    выбранного голоса, синтез не ответил. Последние две предсказать нельзя:
    на неосновных голосах синтез срывается примерно в одном случае из
    десяти, а голос ученик выбирает сам.

    Поэтому решение принимается ЗДЕСЬ, после попытки получить звук, а не
    при сборке вопроса: только здесь известно, есть он или нет.

    Возвращает (клип, канал, варианты). Канал в ответе может отличаться от
    запрошенного — тогда и засчитан ответ будет текстовым, что верно: на
    слух ученик его не давал.
    """
    clip = await _question_clip(session, user, word, pair, channel)
    if channel is not QuizChannel.AUDIO or clip is not None:
        return clip, channel, options

    logger.info(
        "клип для вопроса на слух не получен (ряд %s, %s) — спрашиваю текстом",
        word.id, pair.learning,
    )
    distractors = await get_distractors(word, session, pair, user=user)
    if len(distractors) < OPTIONS_TOTAL - 1:
        # Текстом тоже не собрать — отдаём как есть, звука не будет.
        # Случай крайний: четырёх различимых вариантов не нашлось ни так, ни так
        return clip, channel, options

    text_options, _ = build_options(word, distractors, pair)
    fallback_clip = await _question_clip(session, user, word, pair, QuizChannel.TEXT)
    return fallback_clip, QuizChannel.TEXT, text_options


def _question_text(
    word: Word,
    pair: LanguagePair,
    lang: str,
    current: int,
    total: int,
    *,
    is_repeat: bool = False,
    channel: QuizChannel = QuizChannel.TEXT,
) -> str:
    """
    Вопрос: слово на языке вопроса + пример на том же языке.

    При прямом направлении спрашиваем значение изучаемого слова, при
    обратном — само слово по значению.

    В ЗАГОЛОВКЕ ВСЕГДА ОДНО ЗНАЧЕНИЕ — в обоих направлениях.

    В прямом направлении так было с самого начала: клип «только слово»
    озвучивает одно значение, а в заголовке стоял весь список — выходило
    «Zakłócenia, interferencja» на экране и одно слово в звуке. Человек
    слышит не то, что видит.

    В обратном направлении заголовок раньше оставался полным, и довод был
    такой: звука там нет, а по одному значению слово не опознать —
    «Происхождение» подходит сразу нескольким немецким словам. Владелец
    этот довод отклонил, увидев живую карточку:

        🏴 Записывать, принимать, брать к себе, начинать, поднимать,
           подбирать, впитывать, усваивать
        📝 Ты можешь записать разговор?

    Восемь значений в заголовке при одном в примере — это и есть то, на что
    он жаловался: «одно слово, один пример, один ответ». Довод про
    неопознаваемость снимается самим примером: он стоит строкой ниже и
    показывает, в каком значении спрашивают. А подбор дистракторов сравнивает
    ВСЕ значения (`meaning_variants`), так что ложный вариант не может втайне
    значить то же самое.

    Какое именно значение берётся — решает `main_meaning`: то, что стоит в
    примере. Полный набор значений виден на экране «Помилка перекладу».
    """
    prefix = f"{get_text('quiz_repeat_title', lang)}\n" if is_repeat else ""
    number = get_text("quiz_question_number", lang, current=current, total=total)

    # ВОПРОС НА СЛУХ: самого слова на экране НЕТ, иначе слушать незачем.
    #
    # Это и отличает его от карточки с озвучкой, которая была всегда: там
    # звук идёт ПРИ слове и лишь подсказывает произношение. Здесь звук —
    # единственный источник вопроса, а варианты стоят на изучаемом языке,
    # потому что спрашивают «что услышал», а не «что это значит».
    #
    # Примера тоже нет: он содержит само слово и выдал бы ответ.
    if channel is QuizChannel.AUDIO:
        return (
            f"{prefix}{number} · 🎧\n\n"
            f"{get_text('quiz_question_listen', lang)}"
        )

    # ВОПРОС ВСЛУХ: слово показано, но вариантов нет — ответ приходит
    # голосовым сообщением.
    #
    # Слово ОБЯЗАНО быть на экране: произнести можно только то, что видишь.
    # Этим вопрос вслух противоположен вопросу на слух, где слово спрятано.
    #
    # Пример не показывается: задание — одно слово, и предложение рядом
    # подталкивало бы прочитать его целиком.
    #
    # Звук в вопросе НЕ играет. Эталон есть, но по кнопке: услышав слово
    # перед ответом, человек его просто повторит, а это проверяет слух и
    # подражание, тогда как спрашивают умение произнести по написанному.
    if channel is QuizChannel.SPEECH:
        word_shown = option_label(word, pair.learning)
        return (
            f"{prefix}{number} · 🎤\n\n"
            f"{flag(pair.learning)} <b>{word_shown}</b>\n\n"
            f"{get_text('quiz_question_speak', lang)}"
        )

    prompt = option_label(word, pair.prompt_lang)
    example = example_text(word, pair.prompt_lang)
    task_key = "quiz_question_choose_word" if pair.reverse else "quiz_question_choose_translation"

    parts = [
        prefix,
        number,
        "\n\n",
        f"{pair.prompt_flag} <b>{prompt}</b>\n\n",
    ]
    if example:
        parts.append(f"📝 {example}\n\n")
    parts.append(get_text(task_key, lang))

    return "".join(parts)


def _answer_text(
    word: Word, pair: LanguagePair, lang: str, is_correct: bool,
    channel: QuizChannel = QuizChannel.TEXT,
) -> str:
    """
    Разбор ответа: пара «вопрос = ответ» и примеры на оба языка.

    Порядок сторон совпадает с направлением вопроса — сначала то, что
    спрашивали, потом ответ.

    У ВОПРОСА НА СЛУХ СВОЙ ПОРЯДОК. Там спрашивал не язык значения, а ЗВУК
    на изучаемом языке, и варианты стояли на нём же. Показать разбор как
    «Опыт = die Erfahrung» значило бы начать с того, чего ученик вообще не
    видел. Поэтому для слуха порядок всегда «изучаемый → значение»,
    независимо от направления занятия.
    """
    if channel is QuizChannel.AUDIO:
        prompt_lang, answer_lang = pair.learning, pair.native
    else:
        prompt_lang, answer_lang = pair.prompt_lang, pair.answer_lang

    header = (
        get_text("quiz_correct", lang)
        if is_correct
        else f"{get_text('quiz_wrong', lang)}\n\n{get_text('quiz_correct_answer', lang)}"
    )

    lines = [
        header,
        "\n\n",
        # Одно значение, а не весь список: ровно то, что показано в вопросе,
        # произнесено голосом и стоит в примере. Полный перечень значений
        # владелец просил убрать — «Cywilizowany, kulturalny» рядом с примером
        # про одно из них читается как ошибка
        f"{flag(prompt_lang)} <b>{option_label(word, prompt_lang)}</b>"
        f" = {flag(answer_lang)} <b>{option_label(word, answer_lang)}</b>",
    ]

    # Примеры всегда в порядке «изучаемый язык, затем язык значения»
    learning_example = example_text(word, pair.learning)
    native_example = example_text(word, pair.native)
    if learning_example:
        lines.append(f"\n\n{flag(pair.learning)} {learning_example}")
    if native_example:
        # Пустая строка между примерами, а не перенос: вплотную они читаются
        # как одна фраза в две строки, особенно когда перевод длинный
        lines.append(f"\n\n{flag(pair.native)} {native_example}")

    return "".join(lines)


def _question_keyboard(channel: QuizChannel, options, lang: str) -> InlineKeyboardMarkup:
    """
    Клавиатура вопроса. У вопроса вслух она другая: вариантов нет.

    Ответ там приходит голосовым сообщением, поэтому кнопок всего две —
    послушать эталон и пропустить.

    ПРОПУСК ОБЯЗАТЕЛЕН, и это не поблажка. Человек бывает в транспорте, в
    библиотеке, рядом со спящим ребёнком. Без пропуска он бросит круг
    целиком, и мы потеряем не один вопрос, а всё занятие.
    """
    if channel is not QuizChannel.SPEECH:
        return get_answer_keyboard(options)

    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text=get_text("speech_btn_reference", lang),
            callback_data="speech_reference",
        ),
        InlineKeyboardButton(
            text=get_text("speech_btn_skip", lang),
            callback_data="speech_skip",
        ),
    ]])


def get_next_question_keyboard(lang: str = DEFAULT_LOCALE) -> InlineKeyboardMarkup:
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
    today = utctoday()

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
    """
    Кнопка «📚 Учить» и команда `/quiz` — занятие начинается СРАЗУ.

    Домашний экран между ними не встаёт, хотя три шкалы живут именно на нём.
    Поставить его здесь значило бы добавить нажатие перед каждым занятием —
    тем самым 96%, которые ни разу не меняли ни одной настройки. Своя дверь
    у домашнего экрана есть: `/start` и `/home`.
    """
    await start_lesson(message, state, session)


async def start_lesson(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
    *,
    prefer_channel: Optional[QuizChannel] = None,
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
        )
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
    channel = question["channel"]
    clip, channel, question["options"] = await _clip_or_text(
        session, user, word, pair, channel, question["options"]
    )

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
        text=_question_text(word, pair, lang, 1, quiz_total, channel=channel),
        keyboard=_question_keyboard(channel, question["options"], lang),
        clip=clip,
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
    # на языке ответа.
    options_lang = pair.learning if channel is QuizChannel.AUDIO else pair.answer_lang
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
    card_message=None, card_message_id=None,
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
        )
    except Exception:
        logger.exception("Ошибка обновления прогресса (user=%s word=%s)", user.id, correct_word_id)

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
        text=_answer_text(correct_word, pair, lang, is_correct, channel),
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
        await message.answer(get_text("speech_not_understood", lang))
        return

    asked_at = data.get("asked_at")
    response_seconds = (
        max(0, int(utcnow().timestamp() - float(asked_at))) if asked_at else None
    )

    await _record_answer(
        bot=message.bot, chat_id=message.chat.id, state=state, session=session,
        user=user, pair=pair, lang=lang, correct_word=correct_word,
        is_correct=verdict.matched, channel=channel,
        answer_text=verdict.heard,
        session_id=data["session_id"], correct_answers=data["correct_answers"],
        errors=data["errors"], response_seconds=response_seconds,
        card_message_id=data.get(STATE_CARD_ID),
    )


@router.callback_query(F.data == "speech_reference", QuizStates.answering)
async def play_reference(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    """
    Эталон по кнопке: услышать, как это звучит у носителя.

    Приходит ОТДЕЛЬНЫМ сообщением, а не заменяет карточку: задание должно
    остаться на экране, иначе человек забудет, что произносить.
    """
    await callback.answer()
    ctx = await _speech_context(callback, state, session)
    if ctx is None:
        return
    _, user, correct_word, _ = ctx
    lang = user.interface_language or DEFAULT_LOCALE
    pair = pair_from_user(user)

    clip = await clip_for_user(session, user, correct_word, pair.learning, KIND_WORD)
    if clip is None:
        await callback.answer(get_text("speech_not_understood", lang), show_alert=True)
        return

    media = clip.file_id or BufferedInputFile(clip.data, filename=clip.filename)
    sent = await callback.bot.send_audio(
        callback.message.chat.id, media, title=clip.title,
        performer=AUDIO_PERFORMER,
    )
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
# СЛЕДУЮЩИЙ ВОПРОС / ЗАВЕРШЕНИЕ
# ============================================================================

@router.callback_query(F.data == "next_question", QuizStates.answering)
async def show_next_question(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    await callback.answer()

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
        channel = question["channel"]
        clip, channel, options = await _clip_or_text(
            session, user, word, pair, channel, options
        )
        used_word_ids.append(word.id)

        # Хвост истории каналов: нужен только чтобы не ставить три
        # одинаковых подряд, поэтому двух последних достаточно
        recent_channels = (recent_channels + [channel.value])[-2:]

        await state.update_data(
            current_question=current_question,
            correct_word_id=word.id,
            used_word_ids=used_word_ids,
            asked_at=utcnow().timestamp(),
            channel=channel.value,
            recent_channels=recent_channels,
        )

    await show_card(
        callback.bot, callback.message.chat.id, state, session,
        text=_question_text(
            word, pair, lang, current_question, total_questions,
            is_repeat=is_error_repeat, channel=channel,
        ),
        keyboard=_question_keyboard(channel, options, lang),
        clip=clip,
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
        user.last_quiz_date = utctoday()
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
    by_ear = 0
    for item, word in items:
        icon = "✅" if item.is_correct else "❌"
        # Вопросы на слух помечены в разборе: иначе новая игра растворяется
        # в списке и человек не замечает, что уже узнаёт слова ушами.
        # Отметка ставится у ВОПРОСА, а не у слова: одно и то же слово в
        # разных кругах приходит разными каналами.
        if item.channel == QuizChannel.AUDIO.value:
            by_ear += 1
            icon += " 🎧"
        details.append(
            f"{icon} {option_label(word, pair.learning)} — {option_label(word, pair.native)}"
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
        clip=await _question_clip(session, user, first_word, pair, QuizChannel.TEXT),
        word_id=first_word.id, lang=pair.learning,
    )

    await state.set_state(QuizStates.answering)
    await callback.answer()
