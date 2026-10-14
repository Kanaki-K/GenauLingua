"""
Как выглядит вопрос и разбор ответа — у всех игр круга.

«Читаю», «Вспоминаю», «Слышу», «Говорю» и «Собираю» различаются здесь
ветками по каналу: текст вопроса, текст разбора, клавиатура. Знаки игр
(`_CHANNEL_MARKS`) заданы тоже здесь, и только здесь.

Вынесено из `game.py` переносом, без правок поведения.
"""

from typing import Optional

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.bot.keyboards import get_answer_keyboard
from app.database.enums import QuizChannel
from app.database.models import Word
from app.locales import DEFAULT_LOCALE, get_text
from app.services.language_service import (
    LanguagePair,
    example_text,
    option_label,
    pair_for_channel,
)
from app.services.match_service import BOARD_CHANNEL


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
                       word_id: Optional[int] = None,
                       slots: int = 0) -> InlineKeyboardMarkup:
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

        # `slots` — длина фразы: сверху сразу видно, сколько мест заполнить
        return grid_keyboard([tile for _, tile in options], [], word_id or 0, 0, lang,
                             slots=slots)

    if channel is QuizChannel.AUDIO:
        # ПЯТАЯ КНОПКА — «ПРОПУСТИТЬ», по той же причине, что у речи.
        # Владелец, 14.10: «не всегда люди играют со звуком, может ночью.
        # Нужно дать такую возможность». Без неё человек без наушников
        # жмёт наугад — и ошибка ложится на слово, которое он знает
        keyboard = get_answer_keyboard(options)
        keyboard.inline_keyboard.append([InlineKeyboardButton(
            text=get_text("speech_btn_skip", lang),
            callback_data="listen_skip",
        )])
        return keyboard

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
