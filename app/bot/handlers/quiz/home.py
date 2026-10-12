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
from app.services.language_service import flag, pair_from_user
from app.services.monthly_leaderboard_service import get_user_monthly_rank
from app.services.quiz_service import (
    CHANNEL_UNLOCK,
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
_SCALES = (
    (QuizChannel.TEXT, "home_scale_text", "text"),
    (QuizChannel.AUDIO, "home_scale_audio", "audio"),
    (QuizChannel.SPEECH, "home_scale_speech", "speech"),
)

_CHANNEL_SHORT = {
    QuizChannel.TEXT: "🔤",
    QuizChannel.AUDIO: "🎧",
    QuizChannel.SPEECH: "🎤",
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


async def build_home(user: User, session: AsyncSession) -> tuple[str, InlineKeyboardMarkup]:
    """Собрать текст и клавиатуру домашнего экрана."""
    lang = user.interface_language or DEFAULT_LOCALE
    pair = pair_from_user(user)
    level, category = _scope(user)

    channels = await get_channel_progress(
        user.id, session, pair, level=level, category=category
    )

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

    # Флага перед названием НЕТ нарочно: `langname_*` уже содержит его, и
    # первая редакция печатала «🇩🇪 🇩🇪 Немецкий». Замечено не чтением кода, а
    # показом настоящего экрана живого пользователя.
    learning_name = get_text(f"langname_{pair.learning}", lang)
    header = (
        f"<b>{learning_name}</b> → {flag(pair.answer_lang)}"
        f" · {_mode_label(user, lang)}"
    )

    lines = [header, "", f"<code>{rows}</code>", ""]

    # Серия и место — два повода вернуться завтра, и оба показываются только
    # когда есть что показать: «🔥 0 дней» гасит, а не подгоняет.
    footer = []
    if user.streak_days:
        footer.append(get_text("home_streak", lang, days=user.streak_days))
    rank = await get_user_monthly_rank(user.id, session, learning_lang=pair.learning)
    if rank:
        footer.append(get_text("home_rank", lang, rank=rank["rank"]))
    if footer:
        lines.append(" · ".join(footer))
        lines.append("")

    lines.append(f"<i>{get_text('home_hint', lang)}</i>")

    return "\n".join(lines), _home_keyboard(user, lang, channels)


def _mode_label(user: User, lang: str) -> str:
    """Чем ограничено занятие — уровнем, категорией или ничем."""
    from app.bot.handlers.quiz.stats import _get_mode_title

    return _get_mode_title(user, lang)


def _home_keyboard(
    user: User, lang: str, channels: dict[str, int]
) -> InlineKeyboardMarkup:
    """
    Кнопка занятия и три прямых входа по каналам.

    Прямые входы стоят ПОД главной кнопкой и мелкими: это путь для того, кто
    точно знает, чего хочет. Остальным достаточно верхней.
    """
    # Длина круга берётся оттуда же, откуда её берёт само занятие: кнопка,
    # обещающая пятнадцать слов там, где их будет двадцать, врёт.
    from app.bot.handlers.quiz.game import DEFAULT_QUIZ_LENGTH

    count = user.quiz_word_count or DEFAULT_QUIZ_LENGTH
    rows = [[InlineKeyboardButton(
        text=get_text("home_btn_learn", lang, count=count),
        callback_data="home_learn",
    )]]

    shortcuts = [
        InlineKeyboardButton(
            text=_CHANNEL_SHORT[channel],
            callback_data=f"home_learn_{channel.value}",
        )
        for channel, _, _ in _SCALES
    ]
    rows.append(shortcuts)
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

@router.callback_query(F.data == "home_learn")
async def home_learn(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    """Обычное занятие: каналы смешиваются по правилу допуска."""
    from app.bot.handlers.quiz.game import start_lesson

    await callback.answer()
    await start_lesson(callback.message, state, session)


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
    from app.bot.handlers.quiz.game import start_lesson

    code = callback.data.removeprefix("home_learn_")
    try:
        channel = QuizChannel(code)
    except ValueError:
        await callback.answer("❌ Error", show_alert=True)
        return

    user = await session.get(User, callback.from_user.id)
    if not user or not user.level:
        lang = (user.interface_language if user else None) or DEFAULT_LOCALE
        await callback.answer(get_text("quiz_no_level", lang), show_alert=True)
        return

    lang = user.interface_language or DEFAULT_LOCALE

    # Слух и речь обойтись без озвучки не могут: у вопроса на слух самого
    # слова на экране нет, а у вопроса вслух нечем послушать эталон.
    if channel is not QuizChannel.TEXT and not user.audio_enabled:
        await callback.answer(get_text("channels_audio_blocked", lang), show_alert=True)
        return

    if channel is not QuizChannel.TEXT:
        pair = pair_from_user(user)
        level, category = _scope(user)
        progress = await get_channel_progress(
            user.id, session, pair, level=level, category=category
        )
        ready = progress["ready_audio" if channel is QuizChannel.AUDIO else "ready_speech"]
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

    await callback.answer()
    await start_lesson(callback.message, state, session, prefer_channel=channel)


def _channel_name_key(channel: QuizChannel) -> str:
    """Название канала — то же, что на экране состава занятия."""
    from app.bot.handlers.quiz.settings import _CHANNEL_NAMES

    return _CHANNEL_NAMES[channel]
