"""
Домашний экран: три шкалы — узнаю на глаз, узнаю на слух, произношу.

Зачем он нужен. Три игры дали три РАЗНЫХ измеримых навыка, но показать их
было негде: статистика считает слова одной цифрой, и из неё не видно, что
человек узнаёт четыре сотни слов глазами и шесть десятков вслух.

Самое ценное здесь — не сами числа, а РАЗРЫВ между ними. «342 узнаю глазами,
а произношу 64» говорит о человеке правду, которую он сам о себе не знает, и
мотивирует сильнее любого бейджа: это не награда, а зеркало.

Почему экран НЕ встал перед кнопкой «Учить». Соблазн был: домашний экран —
естественное место, чтобы начинать занятие. Но это нажатие перед КАЖДЫМ
занятием, а в этом проекте уже измерено, чего стоит лишний выбор: 223
пользователя из 233 ни разу не сменили режим викторины, стоящий первым
пунктом настроек. Поэтому «📚 Учить» по-прежнему начинает круг сразу, а
домашний экран открывается своей дверью — `/start` и `/home`.
"""

from __future__ import annotations

import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.enums import CEFRLevel, QuizChannel, QuizMode
from app.database.models import User
from app.locales import DEFAULT_LOCALE, get_text
from app.services.language_service import flag, pair_from_user, language_word
from app.services.monthly_leaderboard_service import ALL_LANGS, get_user_monthly_rank
from app.services.quiz_service import (
    CHANNEL_UNLOCK,
    NEEDS_AUDIO,
    get_channel_progress,
)

logger = logging.getLogger(__name__)

router = Router()

# Длина полосы. Десять знаков — столько же, сколько в наброске экрана, и
# столько влезает в одну строку мобильного Telegram рядом с подписью.
BAR_LENGTH = 10

# Сколько слов должно быть допущено к каналу, чтобы прямой вход им имел смысл.
# Четыре — не круглое число, а размер набора вариантов (OPTIONS_TOTAL): пока
# допущенных меньше, занятие всё равно свалилось бы в текст почти целиком, и
# кнопка «только слух» выглядела бы сломанной. Честнее сказать, чего не
# хватает, чем выдать круг не того канала.
CHANNEL_ENTRY_MIN = 4

# Порядок шкал: от самого лёгкого навыка к самому трудному. Он же порядок
# кнопок прямого входа, и он же порядок порогов допуска — так разрыв между
# шкалами читается сверху вниз как убывающая лестница.
#
# ИЗ ПЕРЕЧИСЛЕНИЯ, а не списком руками: `QuizChannel` и так выстроен от
# лёгкого к трудному (пятая игра стоит второй по замеру точности 87.9% и
# 87.1%, шестая — последней), и шкала новой игры встаёт на место сама.
# Подпись — `home_scale_<имя>`, число — по тому же имени из
# `get_channel_progress`.
_SCALES = tuple(
    (channel, f"home_scale_{channel.key}", channel.key) for channel in QuizChannel
)


# Какое число готовности смотреть у какого канала — по имени, как и шкалы.
# Прежде таблицей на три канала: шестой игры в ней не было бы, и прямой
# вход «Собираю» падал бы на KeyError.
_READY_KEYS = {
    channel: f"ready_{channel.key}"
    for channel in QuizChannel if channel is not QuizChannel.TEXT
}


def _bar(current: int, total: int, length: int = BAR_LENGTH) -> str:
    """
    Полоса без процентов: число стоит рядом отдельно.

    Процент тут лишний и даже вредит. Шкал три, и сравнивать их человек будет
    между собой, а не с сотней; три процента в столбик превращают зеркало в
    отчёт. Полоса показывает долю, число — размер.
    """
    if total <= 0:
        return "░" * length
    filled = min(length, max(0, round(current / total * length)))
    return "▓" * filled + "░" * (length - filled)


def _scope(user: User) -> tuple[CEFRLevel | None, str | None]:
    """
    Чем ограничен набор слов, по которому считаются шкалы.

    Числитель и знаменатель обязаны прийти ИЗ ОДНОГО набора, поэтому ограничение
    тут одно на оба запроса. Разойдись они — и у всякого, кто сменил уровень,
    полоса ушла бы за край: освоенных слов больше, чем слов в наборе.

    Режим «сложные» нарочно считается по всей базе, а не по текущему списку
    трудных слов. Список этот сжимается по мере успехов, и шкала, привязанная
    к нему, росла бы вдвое быстрее настоящего прогресса, а под конец делила бы
    на ноль.
    """
    if user.quiz_mode == QuizMode.CATEGORY and user.quiz_category:
        return None, user.quiz_category
    if user.quiz_mode in (QuizMode.ALL_WORDS, QuizMode.DIFFICULT):
        return None, None
    return user.level, None


def scales_block(
    channels: dict[str, int], lang: str, *, always: bool = False
) -> str:
    """
    Три шкалы одним блоком — он же в напоминании.

    Вынесен нарочно: напоминание показывает те же три шкалы, и будь блок
    собран там отдельно, два экрана об одном разошлись бы при первой же
    правке. Разошёлся бы тот, который реже открывают, — а открывают реже
    как раз напоминание.

    `always` разводит два случая, и разводит по делу. На ДОМАШНЕМ экране
    полосы нужны всегда: человек пришёл смотреть на прогресс, и «пока
    ничего» — честный ответ на его вопрос. В НАПОМИНАНИИ три пустые полосы
    не говорят ничего и гасят: это сообщение пришло звать заниматься, а не
    отчитываться. Поэтому там при пустом счёте блок опускается целиком.
    """
    if not always and not any(channels[field] for _, _, field in _SCALES):
        return ""

    # ЗНАМЕНАТЕЛЬ — СЛОВА, КОТОРЫЕ ЧЕЛОВЕК УЖЕ ВСТРЕЧАЛ, а не весь уровень.
    #
    # Сперва здесь стояло число слов уровня, и это замерено как негодное: у
    # самого продвинутого человека базы вышло «Написанное ░░░░░░░░░░ 107» —
    # сто семь освоенных слов и ПУСТАЯ полоса, потому что на уровне их
    # тысячи. Шкала, которая у всех нулевая, не показывает ничего.
    #
    # От встреченных она отвечает на вопрос, который человек себе и задаёт:
    # «слова, с которыми я уже знаком, — в каких каналах они мои?» Разрыв
    # между тремя шкалами при этом сохраняется полностью: знаменатель у них
    # общий.
    #
    # Цена честная и известна: встретив десяток новых слов, человек увидит
    # полосу чуть короче. Это правда о нём — знакомых слов стало больше, а
    # освоенных пока нет, — и ближайшее же занятие её выправляет.
    total = channels["touched"]

    # Подписи выравниваются по самой длинной из ТРЁХ на этом языке, а не по
    # зашитому числу: по-немецки «Erkenne ich im Schriftbild» вдвое длиннее
    # русского «Узнаю на глаз», и любая зашитая ширина разъехалась бы на
    # каком-нибудь из шести языков.
    labels = {key: get_text(key, lang) for _, key, _ in _SCALES}
    width = max(len(text) for text in labels.values())

    rows = "\n".join(
        f"{labels[key]:<{width}}  {_bar(channels[field], total)}  {channels[field]:>4}"
        for _, key, field in _SCALES
    )
    return f"<code>{rows}</code>"


async def build_home(user: User, session: AsyncSession) -> tuple[str, InlineKeyboardMarkup]:
    """Собрать текст и клавиатуру домашнего экрана."""
    lang = user.interface_language or DEFAULT_LOCALE
    pair = pair_from_user(user)
    level, category = _scope(user)

    channels = await get_channel_progress(
        user.id, session, pair, level=level, category=category
    )

    # ОБА ЯЗЫКА СЛОВАМИ. Прежде второй стоял одним флагом — «Немецкий → 🏴»,
    # то есть без названия вовсе, и человеку оставалось узнавать свой язык по
    # цвету. Флаг при этом работал в боте тремя разными способами на трёх
    # экранах; решение владельца снимает вопрос целиком: языки пишутся
    # словами, и обозначать их символом не надо нигде.
    # БЕЗ ПОВТОРА ЯКОРЯ (владелец, 17.10: «если дублируется — убираем,
    # экономим место»). Якорь прямо над экраном уже говорит пару, уровень и
    # серию. Заголовок остаётся, только когда занятие ограничено не уровнем
    # (тема, все слова, трудные) — этого якорь не говорит
    lines = []
    if user.quiz_mode != QuizMode.LEVEL:
        learning_name = language_word(pair.learning, lang)
        answer_name = language_word(pair.answer_lang, lang)
        lines += [f"<b>{learning_name}</b> → {answer_name} · {_mode_label(user, lang)}", ""]
    lines += [scales_block(channels, lang, always=True), ""]

    # Место — повод вернуться завтра; серия — в якоре. Показывается только
    # когда есть что показать
    footer = []
    # Место — как на первой вкладке рейтинга: месяц со всеми (17.10)
    rank = await get_user_monthly_rank(user.id, session, learning_lang=ALL_LANGS)
    if rank:
        footer.append(get_text("home_rank", lang, rank=rank["rank"]))
    if footer:
        lines.append(" · ".join(footer))
        lines.append("")

    # ЛЕГЕНДЫ К ШКАЛАМ НЕТ. Прежде под ними стояло «Полоса — доля от слов,
    # которые ты уже встречал: три верных ответа каналом, и слово идёт в
    # его счёт» — три строки, которых владелец не смог прочесть дословно:
    # «как понять вообще?». Если к картинке нужна легенда, плоха картинка:
    # три полосы с подписями «Читаю · Слушаю · Говорю» и числами рядом
    # объяснения не требуют.
    hint = get_text('home_hint', lang)
    if hint:
        lines.append(f"<i>{hint}</i>")

    return "\n".join(lines).strip(), _home_keyboard(user, lang, channels)


def _mode_label(user: User, lang: str) -> str:
    """Чем ограничено занятие — уровнем, категорией или ничем."""
    from app.bot.handlers.quiz.stats import _get_mode_title

    return _get_mode_title(user, lang)


def _home_keyboard(
    user: User, lang: str, channels: dict[str, int]
) -> InlineKeyboardMarkup:
    """
    ОДНА КНОПКА: «Подробнее». Этот экран — числа о себе, и ничего больше.

    Решение владельца складывалось в три шага, и каждый сужал экран:

        «не понимаю, для чего нам в статистике 5 кнопок запуска разных
        режимов нашего бота» — сняты четыре прямых входа по играм;
        «в статистике может быть только информация по статистике, но никак
        не выбор игр или какие-то отдельные режимы» — снята и доска;
        «у статистики 1 кнопка — подробнее. Зачем нам на экране 2 раза
        учить слова, не понимаю» — снято и само занятие.

    Последнее — самое верное из трёх. «Учить слова» стоит на НИЖНЕЙ
    клавиатуре, она висит под каждым экраном всегда; та же кнопка внутри
    сообщения — это одно действие в двух местах, и человек ищет разницу,
    которой нет.

    Петля возврата от этого не рвётся: следующее действие предлагает итог
    круга («Ещё круг») и нижняя клавиатура. Числа о себе никого никуда не
    гонят — они отвечают на «где я сейчас».
    """
    rows: list[list[InlineKeyboardButton]] = []

    # ПРЯМЫХ ВХОДОВ ПО ИГРАМ ЗДЕСЬ БОЛЬШЕ НЕТ — четыре кнопки сняты.
    #
    # Решение владельца, дословно: «не понимаю, для чего нам в статистике
    # 5 кнопок запуска разных режимов нашего бота. Это странно и не понимаю
    # цели этого». Прежде он уже сказал то же про их близнецов под итогом
    # круга: «любую тыкаешь — начинаешь игру. И не ясно, выбралось что-то
    # отдельное или нет».
    #
    # И это сходится с главным решением о составе: ОДНА кнопка, игры
    # смешиваются внутри занятия. Четыре кнопки рядом с ней требовали
    # выбора — той самой работы, которой мы избегаем, — и обещали, что
    # выбор что-то настраивает, хотя он запускал круг немедленно.
    #
    # Шкалы остались: они отвечают на «где я сейчас», а не предлагают
    # решение. Кому всё же нужен один канал — он есть в составе занятия
    # (настройки → как учу), и там это НАСТРОЙКА, а не кнопка-ловушка.
    #
    # Обработчик `home_learn_<канал>` не удаляется НАРОЧНО: у 233 человек в
    # переписке остались прежние экраны с этими кнопками, и нажатие по
    # старой клавиатуре должно по-прежнему вести в занятие, а не в тишину.

    # КНОПКИ «НАЙДИ ПАРЫ» ЗДЕСЬ ТОЖЕ НЕТ — и по той же причине.
    #
    # Этот экран открывается кнопкой «Статистика», а решение владельца о
    # статистике не оставляет места толкованию: «В статистике может быть
    # только информация по статистике, но никак не выбор игр или какие-то
    # отдельные режимы». Доска — отдельная игра, значит ей тут не место.
    #
    # ЧТО ИЗ ЭТОГО СЛЕДУЕТ, И ЭТО НАДО ЗНАТЬ: отдельного входа в доску
    # больше НЕТ НИГДЕ. Внутри круга она остаётся — восьмым вопросом из
    # пятнадцати, по правилу из ROADMAP §5а, — но сыграть её одну нельзя.
    # Если такой вход понадобится, его место рядом с «Учить слова» или в
    # составе занятия, а не в числах о себе.
    #
    # Обработчик `match_start` жив: доска приходит в круге, и у людей в
    # переписке остались прежние экраны с этой кнопкой.

    # Подробная статистика — последним рядом. Этот экран отвечает на «где я
    # сейчас»; простыня на сорок строк отвечает на то же, но дольше, и
    # кончается объяснением, а не действием.
    rows.append([InlineKeyboardButton(
        text=get_text("home_btn_stats", lang),
        callback_data="stats_full",
    )])
    return InlineKeyboardMarkup(inline_keyboard=rows)


# ============================================================================
# ПОКАЗ
# ============================================================================

async def show_home(message: Message, session: AsyncSession, user: User) -> None:
    """Показать домашний экран новым сообщением."""
    text, keyboard = await build_home(user, session)
    await message.answer(text, reply_markup=keyboard)


@router.message(Command("home"))
async def cmd_home(message: Message, session: AsyncSession):
    user = await session.get(User, message.from_user.id)
    try:
        await message.delete()
    except Exception:
        logger.debug("Не удалось удалить сообщение пользователя", exc_info=True)

    if not user or not user.level:
        lang = (user.interface_language if user else None) or DEFAULT_LOCALE
        await message.answer(get_text("quiz_no_level", lang))
        return

    await show_home(message, session, user)


# ============================================================================
# ЗАПУСК ЗАНЯТИЯ С ДОМАШНЕГО ЭКРАНА
# ============================================================================

# «Начать занятие сейчас» — одно нажатие на несколько мест: домашний экран,
# напоминание, предложение после круга. Обработчик один нарочно: разойдись
# они, и занятие с напоминания стало бы вести себя иначе, чем с экрана.
#
# `home_learn` оставлен ради сообщений, УЖЕ ОТПРАВЛЕННЫХ людям: у них в
# переписке живёт прежняя кнопка, и убери фильтр — она молча перестанет
# работать. Та же причина, по которой в help.py остался фильтр на надпись
# исчезнувшей кнопки «Помощь».
@router.callback_query(F.data.startswith("learn_now"))
@router.callback_query(F.data == "home_learn")
async def learn_now(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    """
    Обычное занятие: каналы смешиваются по правилу допуска.

    ОДНА КНОПКА, НЕСКОЛЬКО ДВЕРЕЙ. Это нажатие приходит с домашнего экрана,
    из самого напоминания, из итога прошлого круга и из вступительного
    блока — и обработчик у них нарочно один: занятие с напоминания не
    должно вести себя иначе, чем занятие с экрана.

    Но ЗАПИСАТЬСЯ они обязаны по-разному, иначе петлю возврата нечем
    измерить. Поэтому дверь передаётся пометкой после двоеточия
    («learn_now:reminder»), а фильтр ловит их по началу строки. Прежде все
    четыре несли одинаковое `learn_now`, и источник был неразличим даже в
    принципе — а в базу писалось «menu» независимо ни от чего.

    `home_learn` оставлен ради сообщений, УЖЕ ОТПРАВЛЕННЫХ людям: у них в
    переписке живёт прежняя кнопка, и убери фильтр — она молча перестанет
    работать.
    """
    from app.bot.handlers.quiz.lesson import start_lesson
    from app.bot.handlers.quiz.sources import SOURCE_HOME, source_from_callback

    await callback.answer()
    source = source_from_callback(callback.data or "", default=SOURCE_HOME)
    await start_lesson(callback.message, state, session, source=source)


@router.callback_query(F.data.startswith("home_learn_"))
async def home_learn_channel(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
):
    """
    Занятие одним каналом.

    Перед запуском спрашиваем, есть ли чем его наполнить. Проверка не
    формальность: канал следует за СЛОВОМ, и слово, не доросшее до порога,
    придёт текстом — то есть на свежем счёте «только слух» выдало бы круг
    сплошного текста, и кнопка читалась бы как сломанная. Лучше назвать
    причину и число, которого не хватает.
    """
    from app.bot.handlers.quiz.lesson import start_lesson

    code = callback.data.removeprefix("home_learn_")
    try:
        channel = QuizChannel(code)
    except ValueError:
        await callback.answer("Error", show_alert=True)
        return

    user = await session.get(User, callback.from_user.id)
    if not user or not user.level:
        lang = (user.interface_language if user else None) or DEFAULT_LOCALE
        await callback.answer(get_text("quiz_no_level", lang), show_alert=True)
        return

    lang = user.interface_language or DEFAULT_LOCALE

    # Слух и речь обойтись без озвучки не могут: у вопроса на слух самого
    # слова на экране нет, а у вопроса вслух нечем послушать эталон.
    # ПРИПОМИНАНИЕ ЗВУКА НЕ ТРЕБУЕТ: оно текстовое, просто в другую сторону.
    if channel in NEEDS_AUDIO and not user.audio_enabled:
        await callback.answer(get_text("channels_audio_blocked", lang), show_alert=True)
        return

    if channel is not QuizChannel.TEXT:
        pair = pair_from_user(user)
        level, category = _scope(user)
        progress = await get_channel_progress(
            user.id, session, pair, level=level, category=category
        )
        # Готовность берётся по КАНАЛУ из таблицы, а не тернарником на два:
        # с появлением пятой игры тернарник отдал бы ей готовность речи
        ready = progress[_READY_KEYS[channel]]
        if ready < CHANNEL_ENTRY_MIN:
            # Название канала считается ДО вызова: test_format_parameters_match
            # разбирает get_text регулярным выражением, и вложенный вызов
            # внутри аргумента рвёт разбор — проверка перестаёт видеть
            # остальные параметры и падает на них.
            channel_name = get_text(_channel_name_key(channel), lang)
            await callback.answer(
                get_text(
                    "home_channel_not_ready", lang,
                    channel=channel_name,
                    ready=ready,
                    minimum=CHANNEL_ENTRY_MIN,
                ),
                show_alert=True,
            )
            return

    from app.bot.handlers.quiz.sources import SOURCE_CHANNEL

    await callback.answer()
    await start_lesson(
        callback.message, state, session,
        prefer_channel=channel, source=SOURCE_CHANNEL,
    )


def _channel_name_key(channel: QuizChannel) -> str:
    """Название канала — то же, что на экране состава занятия."""
    from app.bot.handlers.quiz.settings import _CHANNEL_NAMES

    return _CHANNEL_NAMES[channel]


# ============================================================================
# ПОДРОБНАЯ СТАТИСТИКА — ОДНИМ ТАПОМ ГЛУБЖЕ
# ============================================================================

@router.callback_query(F.data == "stats_full")
async def show_full_stats(callback: CallbackQuery, session: AsyncSession):
    """
    Простыня статистики под кнопкой домашнего экрана.

    Обработчик стоит ЗДЕСЬ, а не в `stats.py`, нарочно: это кнопка
    домашнего экрана, и все его кнопки должны ловиться одним роутером —
    тогда проверка «у каждой кнопки есть обработчик» видит их все сразу.
    Текст при этом собирает `stats.py`, который за статистику и отвечает.
    """
    from app.bot.handlers.quiz.stats import build_stats_text

    await callback.answer()
    user = await session.get(User, callback.from_user.id)
    if not user or not user.level:
        lang = (user.interface_language if user else None) or DEFAULT_LOCALE
        await callback.answer(get_text("stats_no_level", lang), show_alert=True)
        return

    lang = user.interface_language or DEFAULT_LOCALE
    text = await build_stats_text(user, session)

    await callback.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(
                text=get_text("btn_back", lang), callback_data="home_back"
            )
        ]]),
    )


@router.callback_query(F.data == "home_back")
async def home_back(callback: CallbackQuery, session: AsyncSession):
    """Вернуться с подробной статистики на домашний экран."""
    await callback.answer()
    user = await session.get(User, callback.from_user.id)
    if not user:
        return

    text, keyboard = await build_home(user, session)
    await callback.message.edit_text(text, reply_markup=keyboard)
