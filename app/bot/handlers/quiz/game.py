"""
Игровая логика викторины.

Не привязана к конкретному языку: что показывать и на каком языке давать
варианты, решает LanguagePair (изучаемый язык, язык значения, направление).

Учёт точности идёт по фактически отвеченным вопросам — answered_questions
пишется на каждый ответ. Плановое total_questions для точности не годится:
брошенная сессия иначе выглядит как сплошные ошибки.
"""

import asyncio
import html
import logging
from datetime import date, timedelta
from typing import Optional

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    BufferedInputFile, CallbackQuery, InlineKeyboardButton,
    InlineKeyboardMarkup, Message,
)
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.buttons import BTN_LEARN_WORDS, menu_texts, pressed
from app.bot.keyboards import get_answer_keyboard
from app.bot.states import QuizStates
from app.bot.handlers.quiz.card import STATE_CARD_HAS_AUDIO, STATE_CARD_ID, show_card
from app.bot.utils import delete_messages_fast, ensure_anchor
from app.services.audio_service import (
    KIND_BLIND,
    KIND_FULL,
    KIND_SLOW,
    KIND_WORD,
    clip_for_user,
    clip_kind_for_question,
    forget,
    reobtain,
    remember,
    spoken_for,
)
from app.services.speech_check import check_pronunciation
from app.core.clock import utcnow, utctoday
from app.database.enums import QuizChannel, QuizMode
from app.database.models import QuizQuestion, QuizSession, User, UserWord, Word
from app.bot.handlers.quiz.settings import RESULT_SETTINGS
from app.locales import DEFAULT_LOCALE, get_text
from app.services.language_service import (
    pair_for_channel,
    LanguagePair,
    option_label,
    example_text,
    flag,
    legacy_mode_name,
    pair_from_user,
    word_text,
)
from app.bot.handlers.quiz.settings import get_level_offer_keyboard
from app.bot.handlers.reminders import get_reminder_offer_keyboard
from app.services.level_service import should_offer_next_level
from app.services.match_service import BOARD_CHANNEL
from app.services.monthly_leaderboard_service import update_monthly_stats
from app.services.reminder_service import mark_reminders_offered, should_offer_reminders
from app.services.quiz_service import (
    OPTIONS_TOTAL,
    build_options,
    count_difficult_words,
    generate_question,
    get_distractors,
    get_user_progress_stats,
    update_word_progress,
)

logger = logging.getLogger(__name__)


# ============================================================================
# ОДИН ВОПРОС — ОДИН ОТВЕТ
# ============================================================================

# Номер вопроса, на который ответ УЖЕ принят. Пока он равен текущему,
# второй ответ не считается.
S_ANSWERED = "answered_question"

# Замки по чатам. Нужны потому, что отметка «ответ принят» читается и
# пишется двумя отдельными await, а aiogram обрабатывает обновления
# ПАРАЛЛЕЛЬНО: два нажатия, пришедшие в один миг, успели бы оба прочитать
# «ещё не отвечено». Замок на чат сводит решение к одному потоку.
#
# Словарь НЕ чистится. Прежде `_finish_quiz` выбрасывал замок, пока второе
# «Далее» его ещё ждало, — и следующий вызов получал НОВЫЙ замок, то есть
# два обработчика шли параллельно. Замок — несколько сотен байт на чат,
# у бота 233 человека: держать их все дешевле, чем ловить такую гонку.
_claim_locks: dict[int, asyncio.Lock] = {}


def _claim_lock(chat_id: int) -> asyncio.Lock:
    lock = _claim_locks.get(chat_id)
    if lock is None:
        lock = asyncio.Lock()
        _claim_locks[chat_id] = lock
    return lock


async def _claim_answer(state: FSMContext, chat_id: int) -> bool:
    """
    Принять ответ на текущий вопрос РОВНО ОДИН РАЗ.

    ЗАЧЕМ. Один вопрос умел записаться дважды, и замер по рабочей копии это
    подтвердил: 31 вопрос получил по две строки и больше, 50 лишних строк в
    30 занятиях. Разрыв между двойными ответами — от 0.00 с до 78 с, то
    есть беда приходила двумя разными путями:

        0.00 с   двойной тык: оба нажатия пришли раньше, чем карточка
                 успела перерисоваться и спрятать варианты
        78 с     правка карточки не удалась, варианты остались на экране,
                 и человек нажал снова

    Следствие в обоих случаях одно: балл за вопрос начисляется дважды,
    прогресс по слову двигается дважды, а в занятии оказывается больше
    отвеченных, чем было запланировано (таких занятий 14).

    Возвращает False, если ответ на этот вопрос уже принят, — тогда
    вызывающий молча гасит нажатие. Ругаться не за что: человек не
    виноват, что карточка не поспела.
    """
    async with _claim_lock(chat_id):
        data = await state.get_data()
        current = data.get("current_question")
        if current is None:
            # Круги, начатые до этой правки: номера в состоянии нет, и
            # отказывать им значило бы сломать уже идущее занятие
            return True
        if data.get(S_ANSWERED) == current:
            return False
        await state.update_data(**{S_ANSWERED: current})
        return True


# Что переживает круг: ошибки для повтора и слова для жалобы на перевод
# относятся к ПРОШЛОМУ итогу и нужны его кнопкам.
#
# И отметка «повтор с этого итога уже начат» (`S_REPEAT_FROM`): повтор сам
# начинается со сброса состояния, и без неё второе нажатие той же кнопки
# не узнало бы, что первое уже прошло.
S_REPEAT_FROM = "repeat_started_from"
_KEEP_BETWEEN_ROUNDS = ("saved_errors", "report_session_id", "report_word_ids",
                        S_REPEAT_FROM)


async def _reset_round_state(state: FSMContext) -> dict:
    """
    Начать круг с чистого состояния. Возвращает то, что сохранено.

    Прежде новый круг ДОПИСЫВАЛ своё поверх прежнего. Из брошенного круга
    оставались `answered_question`, `board_shown` и ключи доски: бросил на
    первом вопросе, нажал «Учить» — и первый ответ нового круга гасился как
    повтор, человек застревал. Оставшийся `board_shown` к тому же убирал
    доску из нового круга.
    """
    data = await state.get_data()
    kept = {k: data[k] for k in _KEEP_BETWEEN_ROUNDS if k in data}
    await state.clear()
    if kept:
        await state.update_data(**kept)
    return kept


# Сообщения вокруг вопроса «Говорю», которые убираются при переходе дальше:
# голосовые человека, «Не разобрал…», присланный эталон.
S_STRAY = "stray_message_ids"

# Попытки голосом на текущем вопросе: третья засчитывается верной
S_SPEECH_TRIES = "speech_tries"
SPEECH_ATTEMPTS = 3


async def _remember_stray(state: FSMContext, *message_ids: int) -> None:
    # Под замком чата: две записи, пришедшие разом, дописывают список
    # одновременно, и без замка одна из них терялась бы. Вызывающие замок
    # не держат — иначе здесь была бы взаимная блокировка
    async with _claim_lock(state.key.chat_id):
        data = await state.get_data()
        stray = list(data.get(S_STRAY) or [])
        stray.extend(i for i in message_ids if i)
        await state.update_data(**{S_STRAY: stray})


async def _sweep_stray(bot, chat_id: int, state: FSMContext) -> None:
    """
    Убрать голосовые и служебные сообщения прошлого вопроса.

    Живой тест владельца 14 октября: «после голосового ответа — новый
    вопрос не удаляет сообщения юзера, и его аудио просто висит в чате».
    Карточка круга одна и правится на месте, а голосовое человек присылает
    сам — его карточка не накрывает. Пока виден разбор, голосовое остаётся:
    его можно сравнить с эталоном. Уходит оно при переходе дальше.
    """
    data = await state.get_data()
    stray = data.get(S_STRAY) or []
    if not stray:
        return
    await state.update_data(**{S_STRAY: []})
    for message_id in stray:
        try:
            await bot.delete_message(chat_id, message_id)
        except Exception:
            logger.debug("сообщение %s не удалилось", message_id, exc_info=True)


async def _recover(session: AsyncSession, *objects) -> None:
    """
    Откатить сессию после упавшей записи и перечитать нужные дальше объекты.

    Откат помечает все объекты сессии просроченными, а ленивая подгрузка в
    асинхронной сессии невозможна: первое же чтение поля упало бы. Поэтому
    перечитываем явно.
    """
    await session.rollback()
    for obj in objects:
        if obj is not None:
            await session.refresh(obj)


async def _release_answer(state: FSMContext, chat_id: int) -> None:
    """
    Вернуть вопрос в «не отвечен», если ответ на него так и не записан.

    Нужна речи: голосовое занимает вопрос ДО распознавания, а неразобранная
    запись ответом не считается — бот просит записать ещё раз. Без возврата
    вопрос оставался занятым навсегда: следующее голосовое и «Пропустить»
    гасились как повтор, и выйти из круга было нельзя.
    """
    async with _claim_lock(chat_id):
        data = await state.get_data()
        if data.get(S_ANSWERED) == data.get("current_question"):
            await state.update_data(**{S_ANSWERED: None})

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
    него и выбирают.

    У ПЯТОЙ ИГРЫ ЗВУКА НЕТ, И ЭТО НЕ МЕЛОЧЬ. Она спрашивает значением —
    «металл по-немецки?» — а произнести при этом само слово означало бы
    назвать ответ голосом. Проверка эта была и прежде, но смотрела на
    `pair.reverse`, то есть на НАСТРОЙКУ человека; направление стало
    свойством игры, и смотреть надо на канал. Иначе озвучка выдавала бы
    ответ в каждом обратном вопросе — а их теперь получают все.

    В прямом направлении звучит слово. Исключение — гетероним: произнесённый
    отдельно, он читается наугад («modern», «umfahren» имеют по два чтения),
    и управлять этим нельзя, SSML движку недоступен. Такому слову ставится
    клип с примером, где контекст задаёт чтение однозначно.
    """
    pair = pair_for_channel(pair, channel)

    # 🧱 У СБОРКИ ЗВУКА В ВОПРОСЕ НЕТ — решение владельца: «на экране
    # вопроса озвучка не нужна». Клип слова с примером назвал бы ответ
    # голосом, а клип одного слова — подсказал бы, какое из него собирать.
    # Звук — на разборе, как у остальных игр
    if channel is QuizChannel.BUILD:
        return None

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
        #
        # И ВСЛЕПУЮ: у клипа слова название — само слово, и плеер Telegram
        # показывал ответ прямо над вариантами (`KIND_BLIND`).
        return await clip_for_user(session, user, word, pair.learning, KIND_BLIND)
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


def _as_text_question(
    session, user: User, word: Word, pair: LanguagePair, state: FSMContext,
    lang: str, current: int, total: int, channel: QuizChannel,
):
    """
    Пересборка вопроса на слух в «Читаю», если звук пропал ПРИ ОТПРАВКЕ.

    `_clip_or_text` решает то же при сборке, но file_id может умереть уже в
    Telegram: тогда клип отвергается на отправке, и вопрос уходил текстом
    «Послушай и выбери» без слова. Канал в состоянии меняется на текст —
    засчитан ответ будет так, как его давали.
    """
    if channel is not QuizChannel.AUDIO:
        return None

    async def rebuild():
        distractors = await get_distractors(word, session, pair, user=user)
        if len(distractors) < OPTIONS_TOTAL - 1:
            return None
        options, _ = build_options(word, distractors, pair)
        await state.update_data(channel=QuizChannel.TEXT.value)
        return (
            _question_text(word, pair, lang, current, total,
                           channel=QuizChannel.TEXT),
            _question_keyboard(QuizChannel.TEXT, options, lang),
        )

    return rebuild


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
    # НАПРАВЛЕНИЕ ПО КАНАЛУ, и считается здесь, а не в вызывающем коде:
    # вопрос рисуется из четырёх мест, и каждое могло бы забыть перевернуть
    # пару для пятой игры
    pair = pair_for_channel(pair, channel)

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
            f"{prefix}{number} · {channel_mark(channel)}\n\n"
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
    # 🧱 СБОРКА: экран целиком — в своём модуле (`build.py`), здесь только
    # вход. Пропуски «▢» по числу слов, ничего ещё не собрано
    if channel is QuizChannel.BUILD:
        from app.bot.handlers.quiz.build import question_text_for

        return question_text_for(word, pair, lang, current, total)

    if channel is QuizChannel.SPEECH:
        word_shown = option_label(word, pair.learning)
        return (
            f"{prefix}{number} · {channel_mark(channel)}\n\n"
            f"<b>{word_shown}</b>\n\n"
            f"{get_text('quiz_question_speak', lang)}"
        )

    prompt = option_label(word, pair.prompt_lang)
    example = example_text(word, pair.prompt_lang)

    # НИ ФЛАГА, НИ ЗНАЧКА, НИ УКАЗАНИЯ — устав внешности §4.2.
    #
    # Флаг перед словом не нужен: язык виден по самому слову, а пара языков
    # стоит в якоре над экраном. `📝` перед примером тоже: пример отличается
    # от слова тем, что он предложение, и значок этого не добавляет.
    #
    # «Выбери правильный перевод» убрано: под текстом четыре кнопки с
    # переводами, и другого прочтения у экрана нет. Указание, которое
    # повторяет очевидное, человек перестаёт читать — а вместе с ним и те
    # указания, которые однажды будут нужны.
    #
    # Иерархия типографикой: слово полужирным, пример курсивом.
    # ЗНАК ИГРЫ СТОИТ И ЗДЕСЬ. Прежде карточка и припоминание шли без него,
    # и человек не видел, какой игрой его спросили, — а они отличаются
    # направлением, то есть самым важным: в одной показано слово, в другой
    # его значение. Знак берётся из той же таблицы, что в разборе круга.
    parts = [prefix, number, f" · {channel_mark(channel)}", "\n\n",
             f"<b>{prompt}</b>"]
    if example:
        parts.append(f"\n\n<i>{example}</i>")

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
    # Пара по каналу — по той же причине, что у карточки. У слуха поверх
    # этого свой порядок: спрашивал не язык значения, а ЗВУК на изучаемом
    pair = pair_for_channel(pair, channel)

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
        #
        # ТИРЕ, А НЕ РАВЕНСТВО: `=` между словом и переводом читается как
        # математика. Флагов нет — пара языков очевидна из порядка строк,
        # а четыре флага на коротком экране давали только рябь
        f"<b>{option_label(word, prompt_lang)}</b>"
        f" — <b>{option_label(word, answer_lang)}</b>",
    ]

    # Примеры всегда в порядке «изучаемый язык, затем язык значения»
    learning_example = example_text(word, pair.learning)
    native_example = example_text(word, pair.native)
    if learning_example:
        lines.append(f"\n\n<i>{learning_example}</i>")
    if native_example:
        # ПУСТАЯ СТРОКА МЕЖДУ ПРИМЕРАМИ — решение владельца, дословно: «в
        # ответах правильно\неправильно… хочу между примерами 1 язык и
        # язык 2 разрыв 1 строку (ентер)».
        #
        # Прежде здесь стоял один перенос, и довод был такой: вплотную
        # строки читаются как пара «фраза и её перевод», а пустая строка
        # разрывает эту пару. Довод не выдержал встречи с глазами: на
        # телефоне две строки курсивом подряд сливаются в одну кашу, и
        # понять, где кончился немецкий и начался русский, труднее, чем
        # связать их через пробел.
        lines.append(f"\n\n<i>{native_example}</i>")

    return "".join(lines)


def _question_keyboard(channel: QuizChannel, options, lang: str,
                       word_id: Optional[int] = None) -> InlineKeyboardMarkup:
    """
    Клавиатура вопроса. У вопроса вслух она другая: вариантов нет.

    Ответ там приходит голосовым сообщением, поэтому кнопок всего две —
    послушать эталон и пропустить.

    ПРОПУСК ОБЯЗАТЕЛЕН, и это не поблажка. Человек бывает в транспорте, в
    библиотеке, рядом со спящим ребёнком. Без пропуска он бросит круг
    целиком, и мы потеряем не один вопрос, а всё занятие.

    У сборки — сетка кнопок-слов (`build.py`); `word_id` нужен ей, чтобы
    нажатие по сетке прошлого вопроса не попало в нынешний.
    """
    if channel is QuizChannel.BUILD:
        from app.bot.handlers.quiz.build import grid_keyboard

        return grid_keyboard([tile for _, tile in options], [], word_id or 0, 0, lang)

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


def _build_state(question: Optional[dict], channel: QuizChannel) -> dict:
    """
    Состояние сетки 🧱 для вопроса-сборки; для остальных игр — пусто.

    Одна точка встраивания на оба места, где круг задаёт вопрос (первый
    вопрос и следующий): сама сетка, нажатия и разбор — в `build.py`.
    """
    if channel is not QuizChannel.BUILD or not question or not question.get("build"):
        return {}
    from app.bot.handlers.quiz.build import initial_state

    return initial_state(question["build"], question["correct_word"].id)


def get_next_question_keyboard(lang: str = DEFAULT_LOCALE) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=get_text("quiz_btn_next", lang), callback_data="next_question")]
        ]
    )


def get_results_keyboard(has_errors: bool, lang: str = "ru") -> InlineKeyboardMarkup:
    """
    Итог круга. ПЕРВАЯ КНОПКА — «ещё круг», и это главное в этом экране.

    Прежде её не было вовсе. В самый высокий момент мотивации за день —
    человек только что закончил круг и видит результат — бот предлагал
    «изменить режим викторины» (экран настроек) и «сообщить об ошибке»
    (форму жалобы). Чтобы сыграть второй раз, надо было уйти из сообщения
    и найти клавиатуру внизу.

    Замер объясняет, чего это стоило: 79% тех, кто вообще играл, ни разу не
    занимались два дня подряд. Экран, которым кончается действие, обязан
    предлагать следующее действие первой кнопкой — а не настройки.

    Порядок дальше: сперва ошибки (они про только что пройденное), потом
    режим, и жалоба последней. Жалоба нужна редко и не должна стоять выше
    того, зачем человек здесь.
    """
    buttons = [[
        InlineKeyboardButton(
            text=get_text("quiz_btn_one_more", lang),
            # «:again» — это кнопка «ещё круг» в итоге. Петля возврата
            # считается по этой пометке, и без неё круг-повтор
            # неотличим от входа с домашнего экрана
            callback_data="learn_now:again",
        )
    ]]

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
            # «:result» говорит экрану уровня, ОТКУДА пришли: его «Назад»
            # ведёт на домашний экран, а не в настройки. Прежде человек,
            # поправив трудность после круга, оказывался в чужом месте —
            # находка владельца
            # Новым сообщением под итогом, и «Назад» его убирает
            # (`settings.RESULT_SETTINGS`): итог круга остаётся на месте
            callback_data=RESULT_SETTINGS,
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
    """
    Отметить день занятий. Правило и лучшая серия — в `streak_service`.

    Логика переехала туда целиком: серию ЧИТАЮТ пять мест (домашний экран,
    напоминание, статистика, админка, месячный зачёт), а считало её это
    единственное. Из-за этого колонка врала всем, кто перестал заниматься:
    серия пересчитывается только на завершении круга, а значит у
    остановившегося навсегда остаётся последнее значение. Замер: устарела у
    128 человек из 128, последняя активность 236 дней назад.
    """
    from app.services.streak_service import register_activity

    user = await session.get(User, user_id)
    register_activity(user)
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


# ============================================================================
# ОТКУДА НАЧАЛОСЬ ЗАНЯТИЕ
# ============================================================================

# Прежде в `start_source` ВСЕГДА писалось «menu», какой бы дверью человек
# ни вошёл. Следствие измерено: 2 295 занятий с пустым источником и 25 с
# «menu» на 2 320 всего, а метрика админки «Из напоминаний» искала
# `start_source == 'notification'` — значение, которого не писал НИКТО, и
# потому не могла стать ненулевой никогда.
#
# Это не мелочь учёта. Петля возврата — напоминание → занятие → итог →
# «ещё круг» — то, что по замеру оказалось главным рычагом (6.85 дней
# занятий против 1.59). И прямой её замер был невозможен: нельзя отличить
# круг, начатый с напоминания, от круга с домашнего экрана.
#
# Мешала этому и одна подробность: кнопка напоминания, кнопка домашнего
# экрана и кнопка «ещё круг» несли ОДИН И ТОТ ЖЕ `callback_data`
# («learn_now»), то есть источник был неразличим даже в принципе. Поэтому
# у каждой двери теперь своя пометка после двоеточия.
SOURCE_MENU = "menu"            # реплай-кнопка «📚 Учить» и /quiz
SOURCE_HOME = "home"            # главная кнопка домашнего экрана
SOURCE_CHANNEL = "channel"      # прямой вход 🔤 🎧 🎤 с домашнего экрана
SOURCE_REMINDER = "reminder"    # кнопка в самом напоминании
SOURCE_AGAIN = "again"          # «▶️ Ещё круг» в итоге прошлого
SOURCE_START = "start"          # вступительный блок /start
SOURCE_BOARD = "board"          # итог отдельно открытой доски
SOURCE_REPEAT = "repeat"        # повтор ошибок
SOURCE_RELEASE = "release"      # кнопка под патчноутом (send_release_notes)

KNOWN_SOURCES = frozenset({
    SOURCE_MENU, SOURCE_HOME, SOURCE_CHANNEL, SOURCE_REMINDER,
    SOURCE_AGAIN, SOURCE_START, SOURCE_BOARD, SOURCE_REPEAT, SOURCE_RELEASE,
})

# Подписи дверей для админки живут ЗДЕСЬ, рядом с самими пометками. Прежде
# они были выписаны в трёх местах по-разному: в «Играх» со значками, в
# «Аналитике» — там искалось значение 'notification', которого не пишет
# никто, а остальные двери выводились сырым тегом, в карточке человека —
# тоже сырым. Подпись рядом с пометкой разъехаться не может.
SOURCE_LABELS: dict[str, str] = {
    SOURCE_MENU: "кнопка «Учить»",
    SOURCE_HOME: "домашний экран",
    SOURCE_CHANNEL: "прямой вход",
    SOURCE_REMINDER: "напоминание",
    SOURCE_AGAIN: "ещё круг",
    SOURCE_START: "вступление",
    SOURCE_BOARD: "итог доски",
    SOURCE_REPEAT: "повтор ошибок",
    SOURCE_RELEASE: "патчноут",
}


def source_label(source: Optional[str]) -> str:
    """Подпись двери. Незнакомая пометка показывается как есть, а не прячется."""
    if not source:
        return "без пометки (история)"
    return SOURCE_LABELS.get(source, source)


def source_from_callback(data: str, default: str = SOURCE_HOME) -> str:
    """
    Пометка источника из `callback_data` вида «learn_now:reminder».

    Неизвестное значение сводится к `default` молча: в переписке у людей
    живут кнопки, отправленные прежними версиями, и ронять занятие из-за
    незнакомой пометки нельзя.
    """
    _, _, tail = data.partition(":")
    return tail if tail in KNOWN_SOURCES else default


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

# Ключ состояния: доска в этом круге уже была. Один круг — одна доска:
# вторая превратила бы занятие в сопоставление с довеском из вопросов.
S_BOARD_DONE = "board_shown"


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

# С какого номера круг уже продвинут кнопкой «Далее»
S_ADVANCED = "advanced_from"


async def _claim_advance(state: FSMContext, chat_id: int) -> bool:
    """
    Продвинуть круг с текущего номера РОВНО ОДИН РАЗ.

    Двойное «Далее» на последнем вопросе завершало круг дважды: два экрана
    итога, `quizzes_passed` +2, а однажды второй обработчик упал на
    уникальном ключе месячного счёта. На середине круга двойной тык
    пропускал вопрос. Замок тот же, что у ответа: оба решения про один чат.
    """
    async with _claim_lock(chat_id):
        data = await state.get_data()
        current = data.get("current_question")
        if current is None:
            return True
        if data.get(S_ADVANCED) == current:
            return False
        await state.update_data(**{S_ADVANCED: current})
        return True


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


# ПО ОДНОМУ ЗНАКУ НА КАЖДУЮ ИГРУ — и это единственное место, где они
# заданы. Отсюда их берут вопрос, разбор круга и настройки.
#
# ЧТО ИЗМЕНИЛОСЬ И ПОЧЕМУ. Прежде знак был только у слуха и речи, а
# карточка и припоминание помечались `←` или ничем: «текстовый вопрос
# основной, помечать его значило бы зарябить список». Довод был не
# бессмысленный, но владелец посмотрел на готовое и попросил иначе:
# «можно для карточки и вспомнить сделать свой эмодзи. И чтобы в круге
# обучения на конкретную игру было своё эмодзи».
#
# И это сходится с другим его замечанием — о том, что бот вышел слишком
# холодным: «стиль холодный минимализм мне нравится, единственное, что
# прям очень холодно». Знак игры — ровно то место, где тепло не мешает:
# он не украшение, а ИМЯ игры в один символ, и человек узнаёт по нему,
# чем его спросили, не читая строки.
#
# Выбраны знаки, которые СОВПАДАЮТ С ДЕЙСТВИЕМ, а не с настроением:
#   📖 читаешь написанное        💭 тянешь из памяти
#   🎧 слушаешь                  🎤 говоришь
#   🧱 собираешь фразу           🧩 складываешь пары
_CHANNEL_MARKS = {
    QuizChannel.TEXT.value: "📖",
    QuizChannel.REVERSE.value: "💭",
    QuizChannel.AUDIO.value: "🎧",
    QuizChannel.SPEECH.value: "🎤",
    QuizChannel.BUILD.value: "🧱",
    # Доска — не канал, но в разборе круга её подвопросы надо отличать:
    # иначе пять строк подряд выглядят как пять обычных карточек. Знак у
    # неё был и в документах — тот же.
    BOARD_CHANNEL: "🧩",
}


def channel_mark(channel) -> str:
    """Знак игры. Принимает и канал, и его букву."""
    value = getattr(channel, "value", channel)
    return _CHANNEL_MARKS.get(value, "")


# Строка итога «сколько пришло этой игрой» — у каждой игры, кроме карточки.
# Таблицей, потому что подписи разные по смыслу («Вспомнили», «На слух»), но
# счётчики строятся по ней же: игра без строки здесь не уронит итог.
_RESULT_LINES = {
    QuizChannel.REVERSE.value: "quiz_result_recalled",
    QuizChannel.AUDIO.value: "quiz_result_by_ear",
    QuizChannel.SPEECH.value: "quiz_result_spoken",
    QuizChannel.BUILD.value: "quiz_result_built",
}


def _round_breakdown(
    items: list, pair: LanguagePair, lang: str
) -> tuple[list[str], list[str]]:
    """
    Разбор круга по словам и строки «сколько пришло каждым каналом».

    Канал берётся у ВОПРОСА, а не у слова: одно и то же слово в разных
    кругах приходит разными каналами, и отметка у слова врала бы про круг.

    Строка канала показывается ТОЛЬКО если такие вопросы были. «🎤 Вслух: 0»
    у человека с выключенной речью напоминало бы о неудаче там, где её нет.

    Прежде обе строки существовали в шести локалях и не печатались ни разу:
    счётчик слуха считался и НЕ ИСПОЛЬЗОВАЛСЯ, а речь не считалась вовсе.
    Новая игра растворялась в списке, и человек не замечал, что уже узнаёт
    слова ушами и произносит их, — то есть ровно того, за чем и затевались
    три канала.
    """
    details: list[str] = []
    counts = {value: 0 for value in _RESULT_LINES}

    # ЗНАК ИГРЫ — ТОЛЬКО ЕСЛИ ИГР БЫЛО БОЛЬШЕ ОДНОЙ.
    #
    # Знак здесь РАЗЛИЧАЕТ, а значит нужен там, где есть что различать.
    # У новичка весь круг идёт карточкой (слово допускается к остальным
    # играм после одного верного ответа глазами), и пятнадцать одинаковых
    # 📖 подряд — это рябь, которая ничего не говорит. В смешанном круге
    # тот же знак отвечает на «чем меня сейчас спросили».
    mixed = len({item.channel for item, _ in items}) > 1

    for item, word in items:
        icon = "✓" if item.is_correct else "✗"
        mark = _CHANNEL_MARKS.get(item.channel) if mixed else ""
        if mark:
            icon += f" {mark}"
        # Значок есть у четырёх каналов, а СЧЁТЧИК только у трёх: доска
        # значком помечается, но своей строки «сколько пришло» не имеет —
        # она не навык. Прибавлять по значку, а не по наличию ключа, значило бы
        # KeyError на первом же круге с доской, то есть падение ИТОГА, когда
        # круг уже пройден и записан. Хуже места для падения нет
        if item.channel in counts:
            counts[item.channel] += 1
        details.append(
            f"{icon} {option_label(word, pair.learning)} — {option_label(word, pair.native)}"
        )

    channel_lines: list[str] = []
    for value, key in _RESULT_LINES.items():
        if counts[value]:
            count = counts[value]
            channel_lines.append(get_text(key, lang, count=count))

    return details, channel_lines


async def _offer_what_fits(
    callback: CallbackQuery, session: AsyncSession, user: User, lang: str
) -> None:
    """
    Предложить человеку одно — и не больше одного за круг.

    После круга у бота бывает что сказать сверх результата: включить
    напоминания, поднять уровень. Два предложения подряд превращают конец
    круга в допрос, и человек отмахивается от обоих — поэтому здесь
    очередь, а не список.

    ПОРЯДОК НЕ ПРОИЗВОЛЕН. Напоминания идут первыми, потому что это
    единственный замеренный рычаг возврата (6.85 дней против 1.59) и
    предлагаются они ровно один раз в жизни — упустив этот круг, второго
    случая не будет. Уровень подождёт: признак, по которому он предлагается,
    никуда не денется и к следующему кругу будет тот же.
    """
    if should_offer_reminders(user):
        try:
            await callback.bot.send_message(
                chat_id=callback.message.chat.id,
                text=get_text("reminder_offer", lang),
                reply_markup=get_reminder_offer_keyboard(lang),
            )
            # Отметка ТОЛЬКО после удачной отправки: не дошло — предложим в
            # следующий раз, а не потеряем единственную попытку
            await mark_reminders_offered(user, session)
        except Exception:
            logger.warning("не удалось предложить напоминания", exc_info=True)
        return

    following = await should_offer_next_level(user, session)
    if following is not None:
        try:
            await callback.bot.send_message(
                chat_id=callback.message.chat.id,
                text=get_text(
                    "level_offer", lang,
                    current=user.level.value, following=following.value,
                ),
                reply_markup=get_level_offer_keyboard(following, lang),
            )
        except Exception:
            logger.warning("не удалось предложить уровень", exc_info=True)



# ============================================================================
# ПООЩРЕНИЕ В КОНЦЕ КРУГА
# ============================================================================

def _days_since_last_round(user: User) -> int:
    """
    Сколько дней человек не заходил ДО этого круга.

    Нужно одному поводу — «с возвращением». Берётся `last_quiz_date`, пока
    она не перезаписана сегодняшним числом.
    """
    last = getattr(user, "last_quiz_date", None)
    if last is None:
        return 0
    return max(0, (utctoday() - last).days)


async def _season_score(
    session: AsyncSession, user: User, pair: LanguagePair, on: date,
) -> int:
    """
    Месячный балл человека по ЭТОМУ языку в сезоне месяца `on`.

    По языку, а не вообще: ряды сезона ведутся отдельно на каждый
    изучаемый язык, и балл из чужого ряда дал бы бессмысленную разность.

    СЕЗОН — ПО ДАТЕ ЗАВЕРШЕНИЯ ЗАНЯТИЯ, а не «какой сейчас активен». Так
    занятие относит к сезону и месячный счёт (`update_monthly_stats`).
    Прежде «до» и «после» брались из активного сезона, а он меняется ровно
    на границе месяца: занятие, законченное 1-го в 00:01, «до» читало
    октябрь, запись открывала ноябрь, «после» читало ноябрь — разность
    уходила в минус, и итог показывал «+0» за честно заработанные баллы.
    """
    from app.database.models import MonthlySeason, MonthlyStats

    row = (await session.execute(
        select(MonthlyStats.monthly_score)
        .join(MonthlySeason, MonthlySeason.id == MonthlyStats.season_id)
        .where(
            MonthlyStats.user_id == user.id,
            MonthlyStats.learning_lang == pair.learning,
            MonthlySeason.year == on.year,
            MonthlySeason.month == on.month,
        )
    )).scalar()
    return int(row or 0)


async def _praise_lines(
    session: AsyncSession,
    user: User,
    pair: LanguagePair,
    lang: str,
    items: list,
    *,
    quiz_session: Optional[QuizSession],
    answered: int,
    correct: int,
    learned_before: int,
    score_before: int,
    days_away: int,
    season_day: Optional[date] = None,
) -> list[str]:
    """
    Собрать факты круга и отдать готовые строки поощрения.

    Решение «за что хвалить» живёт в `praise_service` и проверяется без
    базы; здесь только ЗАМЕРЫ. Разделение нарочное: выбор повода — правило,
    и спорить о нём надо на числах, а не гоняя круги.
    """
    from app.services.praise_service import RoundFacts, build_lines

    progress = await get_user_progress_stats(user.id, session, pair)
    words_in_work = int(progress["seen_words"])

    word_ids = [word.id for _, word in items]
    started = quiz_session.started_at if quiz_session else None

    new_words = 0
    returned_right = 0
    if word_ids:
        rows = (await session.execute(
            select(UserWord.word_id, UserWord.created_at)
            .where(
                UserWord.user_id == user.id,
                UserWord.learning_lang == pair.learning,
                UserWord.word_id.in_(word_ids),
            )
        )).all()
        # Слово считается новым, если его ряд прогресса создан В ЭТОМ круге
        fresh = {
            word_id for word_id, created in rows
            if started is not None and created is not None and created >= started
        }
        new_words = len(fresh)
        returned_right = sum(
            1 for question, word in items
            if question.is_correct and word.id not in fresh
        )

    # Первый в жизни верный ответ каналом: сумма по всем словам равна
    # числу верных этим каналом в этом круге — значит прежде их не было
    first_audio, first_speech = False, False
    for channel, column, flag in (
        (QuizChannel.AUDIO.value, UserWord.correct_audio, "audio"),
        (QuizChannel.SPEECH.value, UserWord.correct_speech, "speech"),
    ):
        here = sum(
            1 for question, _ in items
            if question.is_correct and question.channel == channel
        )
        if not here:
            continue
        total = int((await session.execute(
            select(func.coalesce(func.sum(column), 0)).where(
                UserWord.user_id == user.id,
                UserWord.learning_lang == pair.learning,
            )
        )).scalar() or 0)
        if total == here:
            if flag == "audio":
                first_audio = True
            else:
                first_speech = True

    # Серия читается через `streak_service`, а не из колонки: колонка
    # пересчитывается только на завершении круга, и у остановившегося в ней
    # навсегда остаётся последнее значение
    from app.services.streak_service import current_streak

    facts = RoundFacts(
        points=max(0, await _season_score(
            session, user, pair, season_day or utctoday()
        ) - score_before),
        answered=answered,
        correct=correct,
        rounds_total=int(user.quizzes_passed or 0),
        learned_before=learned_before,
        learned_now=int(user.words_learned or 0),
        streak_days=current_streak(user),
        best_streak=int(getattr(user, "best_streak_days", 0) or 0),
        words_in_work=words_in_work,
        words_in_work_before=max(0, words_in_work - new_words),
        new_words=new_words,
        returned_right=returned_right,
        days_away=days_away,
        first_audio=first_audio,
        first_speech=first_speech,
    )
    return build_lines(facts, lang)


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

    # ЗАВЕРШИТЬ МОЖНО ОДИН РАЗ — и это решает база, а не память процесса.
    # Двойное «Далее» гасит `_claim_advance`, но состояние живёт в памяти и
    # не переживает двух экземпляров бота или повтора обновления после
    # перезапуска. Условное обновление атомарно: второй вызов не получит
    # строки и уйдёт, не прибавив `quizzes_passed` и не прислав второй итог.
    claimed = await session.execute(
        update(QuizSession)
        .where(QuizSession.id == session_id, QuizSession.is_completed.isnot(True))
        .values(
            completed_at=utcnow(), is_completed=True, exit_reason="completed",
            exit_at_question=QuizSession.answered_questions,
        )
        .returning(QuizSession.id)
    )
    if claimed.first() is None:
        await session.rollback()
        logger.info("круг %s уже завершён — повтор завершения пропущен", session_id)
        return
    await session.commit()
    quiz_session = await session.get(QuizSession, session_id)
    if quiz_session is not None:
        await session.refresh(quiz_session)

    answered = quiz_session.answered_questions if quiz_session else 0

    # ЧТО БЫЛО ДО КРУГА. Поощрение должно хвалить за то, что случилось
    # ИМЕННО СЕЙЧАС, а оба числа — накопительные: «выучено» пересчитывается
    # целиком, месячный балл считается по формуле от всех занятий сезона.
    # Прирост виден только разностью, и снять «до» надо раньше записи.
    learned_before = int(user.words_learned or 0)
    days_away = _days_since_last_round(user)
    # Сезон занятия — по его завершению, как его относит месячный счёт
    season_day = (quiz_session.completed_at
                  if quiz_session is not None and quiz_session.completed_at
                  else utcnow()).date()
    score_before = await _season_score(session, user, pair, season_day)

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

    # Общая точность — по фактически отвеченным вопросам ВСЕХ завершённых
    # занятий, повторы ошибок включительно. Сумма их включала и прежде, а
    # пересчёт стоял только после обычного круга: круг 0/4, потом повтор
    # 4/4 — по данным 50%, у человека оставалось 0%.
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

    if not is_error_repeat:
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

    details, channel_lines = _round_breakdown(items, pair, lang)

    percentage = (correct_answers / answered * 100) if answered else 0.0

    prefix = "" if is_error_repeat else ""
    result_text = (
        f"{prefix}{get_text('quiz_completed', lang)}\n\n"
        f"{get_text('quiz_result_correct', lang, correct=correct_answers, total=answered)}\n"
        # Без десятой доли: «25.0%» обещает точность, которой в четырёх
        # вопросах нет
        f"{get_text('quiz_result_percentage', lang, percentage=round(percentage))}\n\n"
    )
    if channel_lines:
        result_text += "\n".join(channel_lines) + "\n\n"
    result_text += (
        f"{get_text('quiz_result_details', lang)}\n" + "\n".join(details)
    )

    if errors and not is_error_repeat:
        result_text += "\n\n" + get_text("quiz_result_errors", lang, count=len(errors))

    # ПООЩРЕНИЕ. Отдельным блоком в конце итога: разбор отвечает «что
    # вышло», поощрение — «ради чего возвращаться». Правило одно: хвалить
    # только за измеренное, иначе похвала обесценивает остальные числа.
    #
    # Круг-повтор поощрения НЕ получает: он не платит баллов, не двигает
    # серию и не считается пройденным кругом — сказать «+0 баллов» значило
    # бы сообщить о награде, которой нет.
    if not is_error_repeat:
        praise = await _praise_lines(
            session, user, pair, lang, items,
            quiz_session=quiz_session,
            answered=answered,
            correct=correct_answers,
            learned_before=learned_before,
            score_before=score_before,
            days_away=days_away,
            season_day=season_day,
        )
        if praise:
            result_text += "\n\n" + "\n".join(praise)

    try:
        await callback.message.delete()
    except Exception:
        logger.debug("Не удалось удалить сообщение с вопросом", exc_info=True)

    await callback.bot.send_message(
        chat_id=callback.message.chat.id,
        text=result_text,
        reply_markup=get_results_keyboard(has_errors=bool(errors), lang=lang),
    )

    # ПРЕДЛОЖИТЬ НАПОМИНАНИЯ — ЗДЕСЬ И БОЛЬШЕ НИГДЕ.
    #
    # Момент выбран не случайно: человек только что ЗАКОНЧИЛ круг, то есть
    # у нас есть доказательство, что бот ему годится, и это единственная
    # точка, где предложение не выглядит выпрашиванием. В онбординге
    # спрашивать нельзя — там он ещё не знает, нужны ли мы ему, и ответит
    # «нет», а второго раза правило не даёт.
    #
    # Отдельным сообщением, а не строкой в итоге: итог человек читает, а
    # предложение требует ответа, и смешивать их значит потерять либо
    # внимание к разбору, либо ответ.
    #
    # Отказ предложения не ломает ничего: круг уже засчитан и показан.
    if not is_error_repeat:
        await _offer_what_fits(callback, session, user, lang)

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
