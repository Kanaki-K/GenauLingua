"""
Настройки викторины с поддержкой локализации
Режим викторины, изучаемый язык, режим перевода, язык интерфейса

Относительно прежней версии добавлен ровно один экран — выбор изучаемого языка.
Остальное на месте: экран «Режим перевода» по-прежнему переключает направление,
а язык значения следует за языком интерфейса, как и раньше.

Клавиатуры собираются из реестра языков вместо четырёх почти одинаковых
ветвей if lang == ...: пять языков дают двадцать упорядоченных пар, руками
их не выписать.
"""

import logging
from typing import Optional

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import (
    BufferedInputFile,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.buttons import BTN_SETTINGS, pressed
from app.bot.utils import delete_messages_fast, ensure_anchor
from app.database.enums import CEFRLevel, QuizChannel, QuizMode, WordCategory
from app.database.models import User
from app.locales import DEFAULT_LOCALE, get_text
from app.services.audio_service import (
    set_voice_for_user,
    synthesize_preview,
    voice_for_user,
)
from app.services.audio_store import voice_is_ready
from app.services.quiz_service import enabled_channels, NEEDS_AUDIO
from app.services.tts_voices import by_gender, is_valid_voice, voices_for
from app.services.language_service import (
    INTERFACE_LANGS,
    LEARNABLE_LANGS,
    LanguagePair,
    fallback_native_for,
    is_learnable,
    language_name_key,
    legacy_mode_name,
    pair_from_user,
    pair_label,
)

logger = logging.getLogger(__name__)

router = Router()


@router.callback_query.middleware()
async def _require_user(handler, event: CallbackQuery, data: dict):
    """
    Нажатие от человека, которого нет в базе, — ответ, а не падение.

    Все обработчики ниже начинаются с `session.get(User, ...)` и сразу
    читают `user.interface_language`. Стёртый из базы человек со старым
    экраном в переписке получал AttributeError на любой кнопке настроек —
    воспроизведено аудитом 14 октября на `settings_group_what`. Проверка
    одна на роутер, а не двадцать копий в каждом обработчике.
    """
    session = data.get("session")
    if session is not None and await session.get(User, event.from_user.id) is None:
        await event.answer(get_text("user_not_found", DEFAULT_LOCALE), show_alert=True)
        return None
    return await handler(event, data)


# ============================================================================
# ОТКУДА ПРИШЛИ И СВЕЖИЙ ЯКОРЬ
# ============================================================================

def _origin(data: str) -> str:
    """Пометка после двоеточия: `qmode_level:result` → `result`."""
    return data.partition(":")[2]


def _tail(origin: str) -> str:
    """Та же пометка, готовая к приклейке к следующей кнопке."""
    return f":{origin}" if origin else ""


async def _renew_anchor(callback: CallbackQuery, session: AsyncSession, user: User) -> bool:
    """
    Пересоздать якорь, чтобы нижнее меню и строка состояния стали свежими.

    ПРАВКОЙ ЭТО НЕ СДЕЛАТЬ. Здесь стояла `edit_message_reply_markup` с
    реплай-клавиатурой, а Telegram (и aiogram ещё до сети) правит только
    инлайн-разметку: вызов падал на проверке типа, `except` глушил ошибку,
    и после смены языка меню оставалось на прежнем — аудит 14 октября.
    Строка якоря («Немецкий → Русский · A1») при этом тоже не менялась ни
    после смены языка, ни после смены уровня.

    Возвращает, появился ли новый якорь: тогда экран надо прислать ПОД ним,
    иначе якорь окажется ниже экрана.
    """
    old_id, new_id = await ensure_anchor(callback.message, session, user)
    if not new_id:
        return False
    # ЗАЧИЩАЕТСЯ ВСЁ ОТ ПРЕЖНЕГО ЯКОРЯ ДО НОВОГО, а не один прежний якорь —
    # тем же правилом, что у каждого входа в бот. Удаление одного якоря
    # оставляло выше нового итог круга и «Уровень A2…»: якорь — закладка
    # зачистки, и, переехав вниз, он уводил закладку из-под старых
    # сообщений. Живой тест владельца 14 октября: «должно быть всегда одно
    # меню».
    if old_id and old_id != new_id:
        await delete_messages_fast(
            callback.bot, callback.message.chat.id, old_id, new_id
        )
    return True


async def _show_after_change(
    callback: CallbackQuery, session: AsyncSession, user: User,
    origin: str = "", renew_anchor: bool = False,
) -> None:
    """
    Куда ведёт выбор значения: домой, если пришли из итога круга, иначе в
    настройки. При смене того, что видно в якоре, — под свежим якорем.
    """
    lang = user.interface_language or DEFAULT_LOCALE
    if origin == RESULT_ORIGIN:
        from app.bot.handlers.quiz.home import build_home

        text, keyboard = await build_home(user, session)
    else:
        text, keyboard = _settings_text(user, lang), get_settings_keyboard(lang)

    if renew_anchor and await _renew_anchor(callback, session, user):
        try:
            await callback.message.delete()
        except Exception:
            logger.debug("Не удалось удалить прежний экран", exc_info=True)
        await callback.message.answer(text, reply_markup=keyboard)
        return

    await callback.message.edit_text(text, reply_markup=keyboard)


# ============================================================================
# КАТЕГОРИИ: списки для пагинации (20 категорий, 10 на страницу)
# ============================================================================

CATEGORIES_PAGE_1 = [
    WordCategory.ARBEIT_BERUF,
    WordCategory.BILDUNG_LERNEN,
    WordCategory.EINKAUFEN_GELD,
    WordCategory.EMOTIONEN_CHARAKTER,
    WordCategory.ESSEN_TRINKEN,
    WordCategory.FREIZEIT_SPORT,
    WordCategory.GESUNDHEIT_MEDIZIN,
    WordCategory.GRAMMATIK,
    WordCategory.KLEIDUNG_MODE,
    WordCategory.KOMMUNIKATION,
]

CATEGORIES_PAGE_2 = [
    WordCategory.KULTUR_KUNST,
    WordCategory.MENSCH_FAMILIE,
    WordCategory.NATUR_WETTER,
    WordCategory.RECHT_STAAT,
    WordCategory.REISEN_TRANSPORT,
    WordCategory.TECHNIK_DIGITAL,
    WordCategory.WIRTSCHAFT,
    WordCategory.WISSENSCHAFT,
    WordCategory.WOHNEN_HAUS,
    WordCategory.ZEIT_ALLTAG,
]


def get_category_display(cat_value: str, lang: str) -> str:
    """Получить локализованное название категории через систему локализации"""
    # Arbeit & Beruf -> cat_arbeit_beruf
    key = "cat_" + cat_value.lower().replace(" & ", "_").replace(" ", "_").replace("ä", "ae").replace("ö", "oe").replace("ü", "ue")
    result = get_text(key, lang)
    # Если ключ не найден — вернуть оригинал
    if result.startswith("[MISSING:"):
        return cat_value
    return result


def language_name(code: str, lang: str) -> str:
    return get_text(language_name_key(code), lang)


def _back_row(lang: str, callback_data: str = "back_to_settings") -> list[InlineKeyboardButton]:
    return [InlineKeyboardButton(text=get_text("btn_back", lang), callback_data=callback_data)]


def _grid(buttons: list[InlineKeyboardButton], per_row: int = 2) -> list[list[InlineKeyboardButton]]:
    return [buttons[i:i + per_row] for i in range(0, len(buttons), per_row)]


def _sync_legacy_mode(user: User) -> None:
    """
    Поддержать устаревшее translation_mode в согласии с парой языков.
    Для пар без немецкого значения нет — остаётся NULL.
    """
    user.translation_mode = legacy_mode_name(pair_from_user(user))


# ============================================================================
# ГЛАВНОЕ МЕНЮ НАСТРОЕК
# ============================================================================

# ТРИ ГРУППЫ ВМЕСТО ВОСЬМИ РАВНЫХ ПУНКТОВ.
#
# Восемь кнопок в одном списке перемешивали вещи разной природы: «что я
# учу» человек меняет часто, «как мне удобно» ставит один раз и забывает, а
# лежали они вперемешку и выглядели равно важными. Первым пунктом стоял
# режим викторины, которым не пользуются 96% (223 из 233 не меняли его ни
# разу) — то есть самое заметное место занимал самый невостребованный
# экран.
#
# Состав описан ТАБЛИЦЕЙ, а не тремя клавиатурами руками: девятый пункт
# иначе пришлось бы вписывать и в группу, и в её обработчик, и в возврат.
#
# Длины круга в списке нет нарочно: колонка `quiz_word_count` есть, а
# экрана к ней не существует, и обещать кнопку, которой нет, нельзя.
_GROUPS: dict[str, tuple[str, str, tuple[tuple[str, str], ...]]] = {
    # ключ группы: (ключ надписи кнопки, ключ заголовка экрана, пункты)
    # ПУНКТА «НАПРАВЛЕНИЕ» БОЛЬШЕ НЕТ. Он переворачивал ВСЕ пятнадцать
    # вопросов круга, и включили его 10 человек из 233. Теперь обратная
    # сторона — пятая игра в составе занятия, и два рычага на одно и то же
    # оставлять нельзя: человек не поймёт, какой из них главнее.
    "what": ("settings_group_what", "settings_group_what_title", (
        ("settings_btn_learning_lang", "settings_learning"),
        ("settings_btn_goal", "settings_goal"),
        ("settings_btn_quiz_mode", "settings_quiz_mode"),
    )),
    "how": ("settings_group_how", "settings_group_how_title", (
        ("settings_btn_channels", "settings_channels"),
        ("settings_btn_match", "settings_match"),
        ("settings_btn_audio", "settings_audio"),
    )),
    # Помощь ушла из главного меню — владелец назвал её неактуальной, — но
    # исчезнуть совсем не должна: человек, которому нужны правила игры,
    # ищет их в настройках
    "bot": ("settings_group_bot", "settings_group_bot_title", (
        ("settings_btn_change_language", "settings_language"),
        ("settings_btn_notifications", "settings:notifications"),
        ("btn_help", "settings_help"),
    )),
}

# Куда возвращает «Назад» с каждого экрана. Собирается из той же таблицы,
# чтобы возврат не мог разойтись с составом групп.
_PARENT_GROUP = {
    data: f"settings_group_{key}"
    for key, (_, _, items) in _GROUPS.items()
    for _, data in items
}


def get_settings_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=get_text(btn_key, lang),
                callback_data=f"settings_group_{key}",
            )]
            for key, (btn_key, _, _) in _GROUPS.items()
        ]
    )


def _group_keyboard(key: str, lang: str) -> InlineKeyboardMarkup:
    _, _, items = _GROUPS[key]
    rows = [
        [InlineKeyboardButton(text=get_text(name, lang), callback_data=data)]
        for name, data in items
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows + [_back_row(lang)])


@router.callback_query(F.data.startswith("settings_group_"))
async def show_settings_group(callback: CallbackQuery, session: AsyncSession):
    """Экран одной группы настроек."""
    key = callback.data.removeprefix("settings_group_")
    if key not in _GROUPS:
        await callback.answer("Error", show_alert=True)
        return

    await callback.answer()
    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or DEFAULT_LOCALE
    _, title_key, items = _GROUPS[key]

    # Состояние остаётся на виду, но ТОЛЬКО своё: человек, зашедший менять
    # уровень, должен видеть текущий, не возвращаясь назад, — а напоминания
    # и язык бота ему тут ни к чему.
    #
    # У группы «🔧 Бот» своя строка одна, и это нормально: часть её пунктов
    # состояния не имеет вовсе.
    # ОДНА СТРОКА ПОЯСНЕНИЯ — устав внешности, правило пятое: пояснение
    # там, где без него непонятно. Группа «Что учу» объединяет язык,
    # цель и уровень, и это не очевидно из названия.
    state = _settings_state(user, lang, only=tuple(d for _, d in items))
    text = get_text(title_key, lang)
    about = get_text(f"settings_group_{key}_about", lang)
    if about and not about.startswith("["):
        text += f"\n\n<i>{about}</i>"
    if state:
        text += f"\n\n{state}"

    await callback.message.edit_text(
        text, reply_markup=_group_keyboard(key, lang)
    )


def _quiz_mode_display(user: User, lang: str) -> str:
    """Текстовое описание текущего режима викторины"""
    if user.quiz_mode == QuizMode.LEVEL:
        return get_text("qmode_level_short", lang, level=user.level.value)
    elif user.quiz_mode == QuizMode.CATEGORY:
        cat_value = user.quiz_category or "—"
        display_name = get_category_display(cat_value, lang)
        return get_text("qmode_category_short", lang, category=display_name)
    elif user.quiz_mode == QuizMode.ALL_WORDS:
        return get_text("qmode_all_short", lang)
    elif user.quiz_mode == QuizMode.DIFFICULT:
        return get_text("qmode_difficult_short", lang)
    return "—"


# ============================================================================
# СТРОКА СОСТОЯНИЯ ПРИНАДЛЕЖИТ СВОЕМУ ПУНКТУ
#
# Первая редакция групп печатала внутри каждой все шесть строк, и в группе
# «🔧 Бот» висело «📝 Режим: Уровень B1» с «🎮 Занятие: Карточка · На слух» —
# то есть та же простыня, трижды. Группировка затевалась ровно против этого.
#
# Поэтому строка привязана к ПУНКТУ, а не к экрану: группа печатает строки
# своих пунктов, главный экран — все по порядку. Девятый пункт добавляется
# в одном месте, и его строка приезжает в свою группу сама.
#
# У напоминаний и помощи строки нет: показывать там нечего, и ставить
# заглушку значило бы занять строку ничем.
# ============================================================================

def _line_quiz_mode(user: User, lang: str) -> str:
    return get_text(
        "settings_quiz_mode_line", lang, mode=_quiz_mode_display(user, lang)
    )


def _line_channels(user: User, lang: str) -> str:
    return get_text(
        "settings_channels_line", lang, channels=_channels_display(user, lang)
    )


def _line_learning(user: User, lang: str) -> str:
    name = language_name(pair_from_user(user).learning, lang)
    return get_text("settings_learning_lang_line", lang, language=name)


def _line_audio(user: User, lang: str) -> str:
    state = get_text(
        "audio_state_on" if user.audio_enabled else "audio_state_off", lang
    )
    return get_text("settings_audio_line", lang, state=state)



def _line_interface(user: User, lang: str) -> str:
    display = (
        get_text(f"lang_{user.interface_language}", lang)
        if user.interface_language else "—"
    )
    return get_text("settings_language", lang, language=display)


def _line_goal(user: User, lang: str) -> str:
    goal = (
        get_text(f"goal_{user.learning_goal}", lang)
        if user.learning_goal else get_text("settings_goal_none", lang)
    )
    return get_text("settings_goal_line", lang, goal=goal)


_STATE_LINES = {
    "settings_quiz_mode": _line_quiz_mode,
    "settings_channels": _line_channels,
    "settings_learning": _line_learning,
    # Цель встаёт СРАЗУ ЗА изучаемым языком, а не первой строкой: порядок
    # остальных сохранён ровно тем, каким был, — люди запомнили этот экран,
    # и перетряхивать его ради новой строки не за что.
    "settings_goal": _line_goal,
    "settings_audio": _line_audio,
    "settings_language": _line_interface,
}


# Короткие значения для строки группы на верхнем экране. Берутся из тех же
# функций, что печатают состояние внутри группы, — но без подписи: на
# верхнем экране подпись одна на всю группу.
#
# Пункты без значения (напоминания, помощь) в строку не попадают: ставить
# там заглушку значило бы занять место ничем.
# Чего в сводке НЕ показывать, хотя пункт в группе есть.
#
# Изучаемый язык назван внутри направления («Немецкий → Русский»), и
# отдельным значением он повторялся: «Немецкий, B1, Немецкий → Русский».
# Внутри самой группы строка остаётся — там она принадлежит своей кнопке.
_SUMMARY_SKIP = {
    "what": ("settings_learning",),
}

_SUMMARY_VALUES = {
    "settings_learning": lambda user, lang: language_name(
        pair_from_user(user).learning, lang
    ),
    "settings_quiz_mode": lambda user, lang: _quiz_mode_display(user, lang),
    "settings_goal": lambda user, lang: (
        get_text(f"goal_{user.learning_goal}", lang) if user.learning_goal else ""
    ),
    # Числом способов, а не перечнем: перечень несёт свой разделитель `·`
    # и в сводке сливался с разделителем между значениями
    "settings_channels": lambda user, lang: _channels_short(user, lang),
    # «Со звуком», а не «включена»: в сводке подлежащего нет, и одинокое
    # «включена» не говорит, что именно включено
    "settings_audio": lambda user, lang: get_text(
        "settings_audio_short_on" if user.audio_enabled
        else "settings_audio_short_off", lang
    ),
    # Короткое значение, а не пояснение: `match_state_on` — целая фраза
    # «Доска включена: придёт в середине круга», и в сводке группы она
    # занимала строку целиком
    "settings_match": lambda user, lang: get_text(
        "settings_match_short_on" if user.match_in_round
        else "settings_match_short_off", lang
    ),
    "settings_language": lambda user, lang: (
        get_text(f"lang_{user.interface_language}", lang)
        if user.interface_language else ""
    ),
}

def _channels_short(user: User, lang: str) -> str:
    """
    Состав занятия числом способов: «три способа», «только карточка».

    Перечень `Карточка · 🎧 На слух · 🎤 Речь` в сводке группы занимал
    строку целиком и нёс свой разделитель, который сливался с разделителем
    между значениями.
    """
    # Сравнение с числом игр, а не с тройкой: игр стало четыре, и сводка
    # «все три способа» при трёх включённых из четырёх говорила неправду
    enabled = len(enabled_channels(user))
    if enabled >= len(QuizChannel):
        return get_text("settings_channels_short_all", lang)
    if enabled == 1:
        return get_text("settings_channels_short_one", lang)
    return get_text("settings_channels_short_some", lang, count=enabled)

def _settings_state(user: User, lang: str, only: tuple[str, ...] | None = None) -> str:
    """
    Что сейчас выставлено. `only` — ограничить пунктами одной группы.

    Порядок на главном экране остаётся прежним: он задан порядком
    `_STATE_LINES`, а не порядком групп, — люди запомнили этот экран, и
    перетряхивать строки без нужды не за что.
    """
    keys = [k for k in _STATE_LINES if only is None or k in only]
    return "\n".join(_STATE_LINES[k](user, lang) for k in keys)


def _group_summary(key: str, user: User, lang: str) -> str:
    """
    Что лежит ЗА кнопкой группы — её собственные значения, в одну строку.

    Прежде верхний экран печатал все семь строк состояния простынёй, и
    группировка затевалась ровно против этого: человек видел «Режим: Уровень
    B1», «Занятие: Карточка · На слух», «Цель: не выбрана» и ещё четыре — а
    кнопок было три, и какая из них ведёт к нужному, оставалось угадывать.

    Теперь у каждой группы своя строка, собранная из ЕЁ пунктов. Значения
    берутся из тех же функций, что печатают их внутри группы: второй сборки
    нет, и разойтись им негде.
    """
    _, _, items = _GROUPS[key]
    values = []
    for _, data in items:
        if data in _SUMMARY_SKIP.get(key, ()):
            continue
        make_value = _SUMMARY_VALUES.get(data)
        if make_value:
            value = make_value(user, lang)
            if value:
                values.append(value)
    return " · ".join(values)


def _settings_text(user: User, lang: str) -> str:
    """
    Верхний экран настроек: три группы, у каждой — что за ней.

    ВЫРАВНИВАНИЯ В ДВА СТОЛБЦА ЗДЕСЬ НЕТ, хотя набросок экрана его рисовал.
    В пропорциональном шрифте Telegram добивка пробелами не выравнивает —
    выходит хуже, чем без выравнивания вовсе; моноширинный блок, каким
    сделана админка, превратил бы настройки в таблицу, а это не приборная
    панель. Поэтому название группы полужирным, значения за разделителем.

    «Выбери, что хочешь изменить» убрано: под текстом три кнопки с
    названиями групп, и другого прочтения у экрана нет.
    """
    lines = [get_text("settings_title", lang), ""]
    for key, (btn_key, _, _) in _GROUPS.items():
        summary = _group_summary(key, user, lang)
        name = get_text(btn_key, lang)
        lines.append(f"<b>{name}</b> · {summary}" if summary else f"<b>{name}</b>")
    return "\n".join(lines)


@router.message(Command("settings"))
@router.message(pressed(BTN_SETTINGS))
async def show_settings(message: Message, session: AsyncSession):
    """Показ меню настроек"""
    user = await session.get(User, message.from_user.id)

    if not user:
        # Язык неизвестен — пользователя в базе нет совсем, спросить не у кого
        await message.answer(get_text("user_not_found", DEFAULT_LOCALE))
        return

    lang = user.interface_language or DEFAULT_LOCALE

    try:
        await message.delete()
    except Exception:
        logger.debug("Не удалось удалить сообщение пользователя", exc_info=True)

    old_anchor_id, _ = await ensure_anchor(message, session, user, emoji="")
    if old_anchor_id:
        await delete_messages_fast(message.bot, message.chat.id, old_anchor_id, message.message_id)

    await message.answer(_settings_text(user, lang), reply_markup=get_settings_keyboard(lang))


async def show_settings_callback(callback: CallbackQuery, session: AsyncSession):
    """Показ настроек после изменения (для callback)"""
    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or DEFAULT_LOCALE
    await callback.message.edit_text(
        _settings_text(user, lang), reply_markup=get_settings_keyboard(lang)
    )


@router.callback_query(F.data == "settings_open")
async def open_settings(callback: CallbackQuery, session: AsyncSession):
    """
    Открыть настройки с чужого экрана — например со вступительного блока.

    Отдельно от `back_to_settings`: тот означает «вернуться туда, откуда
    пришёл», и привязан к возврату из подменю. Смысл разный, и сводить их в
    одно нажатие значило бы связать навигацию настроек с экранами, которые
    к ней отношения не имеют.
    """
    await callback.answer()
    await show_settings_callback(callback, session)


# ============================================================================
# ИЗУЧАЕМЫЙ ЯЗЫК
# ============================================================================

@router.callback_query(F.data == "settings_learning")
async def show_learning_lang(callback: CallbackQuery, session: AsyncSession):
    """Показать выбор изучаемого языка"""
    await callback.answer()

    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or DEFAULT_LOCALE
    pair = pair_from_user(user)

    buttons = [
        InlineKeyboardButton(
            text=("✓ " if code == pair.learning else "") + language_name(code, lang),
            callback_data=f"set_learning_{code}",
        )
        for code in LEARNABLE_LANGS
    ]

    text = (
        f"{get_text('learning_lang_title', lang)}\n\n"
        f"{get_text('learning_lang_description', lang)}"
    )

    await callback.message.edit_text(
        text, reply_markup=InlineKeyboardMarkup(inline_keyboard=_grid(buttons) + [_back_row(lang, _PARENT_GROUP["settings_learning"])])
    )


@router.callback_query(F.data.startswith("set_learning_"))
async def set_learning_lang(callback: CallbackQuery, session: AsyncSession):
    """Установить изучаемый язык"""
    code = callback.data.removeprefix("set_learning_")

    if not is_learnable(code):
        await callback.answer("Error", show_alert=True)
        return

    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or DEFAULT_LOCALE

    user.learning_lang = code
    # Язык значения не может совпадать с изучаемым, иначе вопрос выродится
    # в «слово = слово»
    if user.native_lang == code:
        user.native_lang = fallback_native_for(code, preferred=user.interface_language)
    _sync_legacy_mode(user)
    await session.commit()

    await callback.answer(
        get_text("learning_lang_set", lang, language=language_name(code, lang)),
        show_alert=True
    )
    # Изучаемый язык написан в якоре — якорь пересоздаётся
    await _show_after_change(callback, session, user, renew_anchor=True)


# ============================================================================
# СОСТАВ ЗАНЯТИЯ: какими каналами задавать вопросы
# ============================================================================

# Порядок показа и ключ названия. Берётся из QuizChannel, чтобы четвёртый
# канал не пришлось вписывать в трёх местах.
_CHANNEL_NAMES = {
    QuizChannel.TEXT: "channel_text",
    QuizChannel.REVERSE: "channel_reverse",
    QuizChannel.AUDIO: "channel_audio",
    QuizChannel.SPEECH: "channel_speech",
}


def _channels_display(user: User, lang: str) -> str:
    """Строка состояния для меню настроек: какие каналы включены."""
    return " · ".join(
        get_text(_CHANNEL_NAMES[c], lang) for c in enabled_channels(user)
    )


def _channel_available(channel: QuizChannel, user: User) -> bool:
    """
    Можно ли вообще включить этот канал.

    Слух требует включённой озвучки: без звука вопрос на слух неотвечаем —
    слова на экране нет, его заменяет клип.

    Речь тоже требует озвучки, но по другой причине: сам вопрос без звука
    обойдётся (слово показано), а вот эталон послушать будет нечем, и
    сравнить себя станет не с чем. Упражнение превратится в «скажи что-то, я
    угадаю», а в этом половина пользы теряется.
    """
    # Припоминания здесь нет нарочно: оно текстовое, просто в другую
    # сторону, и человеку с выключенной озвучкой доступно полностью.
    # Список звуковых каналов один на проект — `NEEDS_AUDIO`
    if channel in NEEDS_AUDIO:
        return bool(user.audio_enabled)
    return True


@router.callback_query(F.data == "settings_channels")
async def show_channels(callback: CallbackQuery, session: AsyncSession):
    """
    Экран состава занятия.

    До него колонка `quiz_channels` была НЕДОСТИЖИМА из бота: выключить
    вопросы на слух можно было только выключив озвучку целиком, то есть
    заодно лишившись звука в карточках.

    Текст не выключается никогда — занятие без единого канала это пустой
    экран, и настройка не имеет права им кончаться.
    """
    await callback.answer()
    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or DEFAULT_LOCALE
    on = set(enabled_channels(user))

    rows = []
    for channel, name_key in _CHANNEL_NAMES.items():
        available = _channel_available(channel, user)
        if channel is QuizChannel.TEXT:
            mark = "✓ "          # всегда включён, нажатие ничего не меняет
        elif not available:
            mark = "✗ "
        else:
            mark = "✓ " if channel in on else ""
        rows.append([InlineKeyboardButton(
            text=mark + get_text(name_key, lang),
            callback_data=f"channel_toggle_{channel.value}",
        )])

    notes = [get_text("channels_text_always", lang)]
    if not user.audio_enabled:
        notes.append(get_text("channels_audio_blocked", lang))

    text = (
        f"{get_text('channels_title', lang)}\n\n"
        f"{get_text('channels_description', lang)}\n\n"
        + "\n".join(f"<i>{n}</i>" for n in notes)
    )

    await callback.message.edit_text(
        text, reply_markup=InlineKeyboardMarkup(inline_keyboard=rows + [_back_row(lang, _PARENT_GROUP["settings_channels"])])
    )


@router.callback_query(F.data.startswith("channel_toggle_"))
async def toggle_channel(callback: CallbackQuery, session: AsyncSession):
    """Включить или выключить канал."""
    code = callback.data.removeprefix("channel_toggle_")
    try:
        channel = QuizChannel(code)
    except ValueError:
        await callback.answer("Error", show_alert=True)
        return

    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or DEFAULT_LOCALE

    if channel is QuizChannel.TEXT:
        await callback.answer(get_text("channels_text_always", lang), show_alert=True)
        return
    if not _channel_available(channel, user):
        # Причина теперь одна на оба канала — выключенная озвучка. Пока речи
        # не существовало, у неё была своя («скоро»); эта ветка осталась бы
        # врать, если её не свести к настоящей причине.
        await callback.answer(
            get_text("channels_audio_blocked", lang), show_alert=True
        )
        return

    # Хранится строка из букв, а не набор флагов: порядок в ней не значим,
    # но держим его тем же, что в перечислении, — так значение читаемо
    current = {c.value for c in enabled_channels(user)}
    if channel.value in current:
        current.discard(channel.value)
    else:
        current.add(channel.value)
    current.add(QuizChannel.TEXT.value)

    user.quiz_channels = "".join(c.value for c in QuizChannel if c.value in current)
    await session.commit()

    await show_channels(callback, session)


# ============================================================================
# 🧩 ДОСКА В КРУГЕ — ВЫКЛЮЧАТЕЛЬ
#
# Доска не канал: каналы задают вопрос про ОДНО слово, а она берёт пять
# сразу. Поэтому у неё своя колонка и свой экран, а не буква в составе
# занятия. По умолчанию включена — спрячь за переключателем, и не увидит
# никто, это в проекте измерено.
# ============================================================================

@router.callback_query(F.data == "settings_match")
async def show_match_setting(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()
    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or DEFAULT_LOCALE

    state_key = "match_state_on" if user.match_in_round else "match_state_off"
    rows = [[InlineKeyboardButton(
        text=("✓ " if user.match_in_round else "")
        + get_text("settings_btn_match", lang),
        callback_data="match_toggle",
    )]]

    text = (
        f"{get_text('settings_match_title', lang)}\n\n"
        f"{get_text('settings_match_description', lang)}\n\n"
        f"<i>{get_text(state_key, lang)}</i>"
    )
    await callback.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=rows + [_back_row(lang, _PARENT_GROUP["settings_match"])]
        ),
    )


@router.callback_query(F.data == "match_toggle")
async def toggle_match(callback: CallbackQuery, session: AsyncSession):
    user = await session.get(User, callback.from_user.id)
    user.match_in_round = not user.match_in_round
    await session.commit()
    await show_match_setting(callback, session)


# ============================================================================
# ЗАЧЕМ УЧУ — ЭКРАН, БЕЗ КОТОРОГО ЦЕЛЬ БЫЛА БЫ НЕДОСТИЖИМА
#
# Опрос «зачем учишь» задаётся в онбординге, и этого МАЛО: у всех 233
# нынешних пользователей онбординг давно позади, и цель осталась бы у них
# пустой навсегда — а менять свою они не смогли бы вовсе. Ровно та же
# дыра, что была у состава занятия: колонка есть, экрана нет.
# ============================================================================

@router.callback_query(F.data == "settings_goal")
async def show_goal(callback: CallbackQuery, session: AsyncSession):
    """Выбор цели. Отмеченная галочкой — текущая."""
    from app.services.goal_service import GOAL_ORDER

    await callback.answer()
    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or DEFAULT_LOCALE

    rows = [
        [InlineKeyboardButton(
            text=("✓ " if code == user.learning_goal else "")
            + get_text(f"goal_{code}", lang),
            callback_data=f"set_goal_{code}",
        )]
        for code in GOAL_ORDER
    ]

    text = (
        f"{get_text('settings_goal_title', lang)}\n\n"
        f"{get_text('settings_goal_description', lang)}"
    )
    await callback.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=rows + [_back_row(lang, _PARENT_GROUP["settings_goal"])]
        ),
    )


@router.callback_query(F.data.startswith("set_goal_"))
async def set_goal(callback: CallbackQuery, session: AsyncSession):
    """
    Сменить цель.

    Прежний прогресс НЕ ТРОГАЕТСЯ: цель влияет только на то, какие слова
    придут НОВЫМИ. Выученное в прошлой теме продолжит возвращаться на
    повторение — иначе смена цели выглядела бы как потеря сделанного.
    """
    from app.services.goal_service import is_goal

    code = callback.data.removeprefix("set_goal_")
    if not is_goal(code):
        await callback.answer("Error", show_alert=True)
        return

    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or DEFAULT_LOCALE
    user.learning_goal = code
    await session.commit()

    await callback.answer(get_text("settings_goal_set", lang), show_alert=False)
    await show_goal(callback, session)


# ============================================================================
# ПРЕДЛОЖЕНИЕ ПОДНЯТЬ УРОВЕНЬ
#
# Бот замечает, что нынешний уровень стал лёгким, и СПРАШИВАЕТ. Молча
# менять то, что человек выставил руками, нельзя: это читается как
# поломка, а не как забота (`ROADMAP.md` §3.5 дословно: «Не переключать
# молча, а СПРОСИТЬ»).
#
# Признак — не охват уровня, а точность последних ответов. Почему пришлось
# поменять — разобрано в `level_service`: прежнее правило «90% слов уровня
# освоены» не сработало бы ни разу, лучший человек базы на 9.5%.
# ============================================================================

def get_level_offer_keyboard(following: CEFRLevel, lang: str) -> InlineKeyboardMarkup:
    """Согласие и отказ, оба одним нажатием."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=get_text("level_offer_yes", lang, following=following.value),
            callback_data=f"level_up_{following.value}",
        )],
        [InlineKeyboardButton(
            text=get_text("level_offer_no", lang),
            callback_data="level_up_no",
        )],
    ])


@router.callback_query(F.data.startswith("level_up_"))
async def answer_level_offer(callback: CallbackQuery, session: AsyncSession):
    """
    Ответ на предложение. Отказ запоминается, согласие поднимает уровень.

    Отказ относится к КОНКРЕТНОМУ уровню, а не к предложениям вообще: не
    запомни его — и оно вернулось бы после следующего же круга, и так
    после каждого, пока человек не уйдёт.
    """
    from app.services.level_service import decline_level, raise_level

    user = await session.get(User, callback.from_user.id)
    lang = (user.interface_language if user else None) or DEFAULT_LOCALE
    if not user:
        await callback.answer("Error", show_alert=True)
        return

    code = callback.data.removeprefix("level_up_")

    if code == "no":
        await decline_level(user, session)
        await callback.answer()
        try:
            await callback.message.delete()
        except Exception:
            pass
        return

    try:
        following = CEFRLevel(code)
    except ValueError:
        await callback.answer("Error", show_alert=True)
        return

    await raise_level(user, session, following)
    await callback.answer()

    # ОДИН ЭКРАН ПОСЛЕ СОГЛАСИЯ: свежий якорь (уровень написан в нём) и под
    # ним главный экран с подтверждением сверху. Прежде предложение
    # правилось в голое «Уровень A2. Слова будут потруднее.» без единой
    # кнопки, а итог круга и это сообщение оставались висеть выше якоря.
    from app.bot.handlers.quiz.home import build_home

    done = get_text("level_offer_done", lang, following=following.value)
    text, keyboard = await build_home(user, session)
    if await _renew_anchor(callback, session, user):
        await callback.message.answer(f"{done}\n\n{text}", reply_markup=keyboard)
        return
    try:
        await callback.message.edit_text(f"{done}\n\n{text}", reply_markup=keyboard)
    except Exception:
        await callback.message.answer(f"{done}\n\n{text}", reply_markup=keyboard)


# ============================================================================
# РЕЖИМ ВИКТОРИНЫ — главное подменю (4 кнопки 2x2)
# ============================================================================

# Куда ведёт «Назад» с экрана уровня и тем, когда на него пришли ИЗ ИТОГА
# КРУГА, а не из настроек.
#
# Находка владельца: «В конце викторины — уровень и темы. Потом выбираю
# назад — оно в меню настроек возвращает. Неправильно». И правда: человек
# шёл не в настройки — он только что закончил занятие и поправил трудность.
# Возврат «туда, где эта кнопка живёт» — это возврат в чужое место.
#
# Домашний экран — верный ответ: там шкалы и кнопка занятия, то есть то,
# ради чего человек трудность и правил.
#
# ВТОРАЯ ПОПРАВКА ВЛАДЕЛЬЦА, 14 октября: «Уровень и темы — нажимаю,
# попадаю в настройки, а когда нажимаю назад — попадаю в статистику.
# Почему не возвращает на прошлое сообщение круга, ведь назад должно было
# туда попасть?» Домашний экран был неверным ответом: экран уровня
# ЗАМЕНЯЛ итог круга правкой, и вернуться к итогу было некуда — его уже
# не существовало. Теперь из итога экран открывается НОВЫМ сообщением под
# ним, а «Назад» это сообщение убирает: итог с «Ещё круг» снова последний.
# Если же уровень или тему поменяли, итог устарел — тогда, как и прежде,
# свежий якорь и домашний экран (`_show_after_change`).
RESULT_ORIGIN = "result"
BACK_FROM_RESULT = "result_back"
RESULT_SETTINGS = "result_settings"


def get_quiz_mode_keyboard(lang: str, origin: str = "") -> InlineKeyboardMarkup:
    """
    Четыре режима и возврат. `origin` приклеивается к КАЖДОЙ кнопке.

    Прежде пометка «пришёл из итога круга» жила ровно на один экран: уже
    с экрана уровня «Назад» вёл на голый `settings_quiz_mode`, оттуда — в
    группу настроек, а выбор уровня выкидывал на корень настроек. То есть
    находка владельца была закрыта на первом шаге и открыта на втором —
    аудит 14 октября, воспроизведено нажатиями.
    """
    tail = _tail(origin)
    back_to = BACK_FROM_RESULT if origin == RESULT_ORIGIN else _PARENT_GROUP["settings_quiz_mode"]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=get_text("qmode_btn_level", lang),
                    callback_data=f"qmode_level{tail}"
                ),
                InlineKeyboardButton(
                    text=get_text("qmode_btn_category", lang),
                    callback_data=f"qmode_category_page_1{tail}"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_text("qmode_btn_all", lang),
                    callback_data=f"qmode_all{tail}"
                ),
                InlineKeyboardButton(
                    text=get_text("qmode_btn_difficult", lang),
                    callback_data=f"qmode_difficult{tail}"
                ),
            ],
            _back_row(lang, back_to)
        ]
    )


def _quiz_mode_text(user: User, lang: str) -> str:
    return (
        f"{get_text('qmode_title', lang)}\n\n"
        f"{get_text('qmode_current', lang, mode=_quiz_mode_display(user, lang))}\n\n"
        f"{get_text('qmode_choose', lang)}"
    )


@router.callback_query(F.data == RESULT_SETTINGS)
async def open_quiz_mode_from_result(callback: CallbackQuery, session: AsyncSession):
    """«Уровень и темы» под итогом круга: новым сообщением, итог остаётся."""
    await callback.answer()
    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or DEFAULT_LOCALE
    await callback.message.answer(
        _quiz_mode_text(user, lang),
        reply_markup=get_quiz_mode_keyboard(lang, RESULT_ORIGIN),
    )


@router.callback_query(F.data == BACK_FROM_RESULT)
async def back_to_result(callback: CallbackQuery):
    """«Назад» к итогу круга: убрать экран настроек — итог под ним на месте."""
    await callback.answer()
    try:
        await callback.message.delete()
    except Exception:
        logger.debug("экран настроек над итогом не удалился", exc_info=True)


@router.callback_query(F.data.startswith("settings_quiz_mode"))
async def show_quiz_mode(callback: CallbackQuery, session: AsyncSession):
    """
    Уровень и темы. Возврат зависит от того, ОТКУДА пришли.

    Приставка в `callback_data` — единственное, что отличает приход из
    итога круга (`settings_quiz_mode:result`) от прихода из настроек.
    Состояние тут не годится: экран живёт на сообщении, а сообщений у
    человека несколько, и «откуда пришли» у каждого своё.
    """
    await callback.answer()

    origin = _origin(callback.data)

    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or DEFAULT_LOCALE

    await callback.message.edit_text(
        _quiz_mode_text(user, lang), reply_markup=get_quiz_mode_keyboard(lang, origin)
    )


# ============================================================================
# РЕЖИМ: ПО УРОВНЮ (A1–C2)
# ============================================================================

# По НАЧАЛУ строки, а не по равенству: за именем едет пометка
# («qmode_level:result»). Других нажатий с этим началом нет, а равенство
# не пропустило бы помеченное — и приёмка `verify_buttons` проверяет
# f-строки именно по приставке.
@router.callback_query(F.data.startswith("qmode_level"))
async def show_level_selection(callback: CallbackQuery, session: AsyncSession):
    """Показать выбор уровня для режима 'По уровню'"""
    await callback.answer()

    tail = _tail(_origin(callback.data))
    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or DEFAULT_LOCALE

    text = (
        f"{get_text('qmode_level_title', lang)}\n\n"
        f"{get_text('qmode_level_desc', lang)}"
    )

    levels = [
        InlineKeyboardButton(text=level.value, callback_data=f"qmode_set_level_{level.value}{tail}")
        for level in CEFRLevel
    ]
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=_grid(levels, per_row=3) + [_back_row(lang, f"settings_quiz_mode{tail}")]
    )

    await callback.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(F.data.startswith("qmode_set_level_"))
async def set_quiz_mode_level(callback: CallbackQuery, session: AsyncSession):
    """Установить режим 'По уровню' с конкретным уровнем"""
    level_str, _, origin = callback.data.removeprefix("qmode_set_level_").partition(":")

    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or DEFAULT_LOCALE

    try:
        user.level = CEFRLevel(level_str)
    except ValueError:
        await callback.answer("Error", show_alert=True)
        return

    user.quiz_mode = QuizMode.LEVEL
    user.quiz_category = None
    await session.commit()

    await callback.answer(get_text("qmode_level_set", lang, level=level_str), show_alert=True)

    # Уровень написан в якоре — якорь пересоздаётся
    await _show_after_change(callback, session, user, origin, renew_anchor=True)


# ============================================================================
# РЕЖИМ: ПО КАТЕГОРИИ (пагинация 10 на страницу)
# ============================================================================

def get_category_keyboard(page: int, lang: str, origin: str = "") -> InlineKeyboardMarkup:
    """Клавиатура категорий с пагинацией. `origin` едет на каждой кнопке."""
    categories = CATEGORIES_PAGE_1 if page == 1 else CATEGORIES_PAGE_2
    total_pages = 2
    tail = _tail(origin)

    buttons = [
        InlineKeyboardButton(
            text=get_category_display(cat.value, lang),
            callback_data=f"qmode_set_cat_{cat.name}{tail}",
        )
        for cat in categories
    ]
    rows = _grid(buttons)

    # Пагинация
    nav_row = []
    if page > 1:
        nav_row.append(InlineKeyboardButton(text="<", callback_data=f"qmode_category_page_{page - 1}{tail}"))
    nav_row.append(InlineKeyboardButton(text=f"{page} / {total_pages}", callback_data="noop"))
    if page < total_pages:
        nav_row.append(InlineKeyboardButton(text=">", callback_data=f"qmode_category_page_{page + 1}{tail}"))
    rows.append(nav_row)

    rows.append(_back_row(lang, f"settings_quiz_mode{tail}"))

    return InlineKeyboardMarkup(inline_keyboard=rows)


@router.callback_query(F.data.startswith("qmode_category_page_"))
async def show_category_page(callback: CallbackQuery, session: AsyncSession):
    """Показать страницу категорий"""
    await callback.answer()

    page_str, _, origin = callback.data.removeprefix("qmode_category_page_").partition(":")
    page = int(page_str)
    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or DEFAULT_LOCALE

    text = (
        f"{get_text('qmode_category_title', lang)}\n\n"
        f"{get_text('qmode_category_desc', lang)}"
    )

    await callback.message.edit_text(text, reply_markup=get_category_keyboard(page, lang, origin))


@router.callback_query(F.data.startswith("qmode_set_cat_"))
async def set_quiz_mode_category(callback: CallbackQuery, session: AsyncSession):
    """Установить режим 'По категории'"""
    cat_name, _, origin = callback.data.removeprefix("qmode_set_cat_").partition(":")

    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or DEFAULT_LOCALE

    try:
        cat = WordCategory[cat_name]
    except KeyError:
        await callback.answer("Error", show_alert=True)
        return

    user.quiz_mode = QuizMode.CATEGORY
    user.quiz_category = cat.value
    await session.commit()

    display_name = get_category_display(cat.value, lang)
    await callback.answer(
        get_text("qmode_category_set", lang, category=display_name),
        show_alert=True
    )

    await _show_after_change(callback, session, user, origin)


# ============================================================================
# РЕЖИМ: ТОП 10К (ВСЕ СЛОВА)
# ============================================================================

@router.callback_query(F.data.startswith("qmode_all"))
async def set_quiz_mode_all(callback: CallbackQuery, session: AsyncSession):
    """Установить режим 'Все слова'"""
    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or DEFAULT_LOCALE

    user.quiz_mode = QuizMode.ALL_WORDS
    user.quiz_category = None
    await session.commit()

    await callback.answer(get_text("qmode_all_set", lang), show_alert=True)
    await _show_after_change(callback, session, user, _origin(callback.data))


# ============================================================================
# РЕЖИМ: СЛОЖНЫЕ СЛОВА
# ============================================================================

@router.callback_query(F.data.startswith("qmode_difficult"))
async def set_quiz_mode_difficult(callback: CallbackQuery, session: AsyncSession):
    """Установить режим 'Сложные слова'"""
    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or DEFAULT_LOCALE

    user.quiz_mode = QuizMode.DIFFICULT
    user.quiz_category = None
    await session.commit()

    await callback.answer(get_text("qmode_difficult_set", lang), show_alert=True)
    await _show_after_change(callback, session, user, _origin(callback.data))


# ============================================================================
# NOOP (для неактивных кнопок типа "1/2")
# ============================================================================

@router.callback_query(F.data == "noop")
async def noop_handler(callback: CallbackQuery):
    await callback.answer()


# ============================================================================
# ИЗМЕНЕНИЕ РЕЖИМА ПЕРЕВОДА (направление вопроса)
# ============================================================================

# ============================================================================
# ИЗМЕНЕНИЕ ЯЗЫКА ИНТЕРФЕЙСА
# ============================================================================

@router.callback_query(F.data == "settings_language")
async def change_interface_language(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()

    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or DEFAULT_LOCALE

    text = (
        f"{get_text('settings_language_title', lang)}\n\n"
        f"{get_text('settings_language_description', lang)}"
    )

    buttons = [
        InlineKeyboardButton(
            text=get_text(f"lang_{code}", lang),
            callback_data=f"iface_lang_{code}",
        )
        for code in INTERFACE_LANGS
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=_grid(buttons) + [_back_row(lang, _PARENT_GROUP["settings_language"])])

    await callback.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(F.data.startswith("iface_lang_"))
async def set_interface_language(callback: CallbackQuery, session: AsyncSession):
    new_lang = callback.data.removeprefix("iface_lang_")

    if new_lang not in INTERFACE_LANGS:
        await callback.answer("Error", show_alert=True)
        return

    user = await session.get(User, callback.from_user.id)

    user.interface_language = new_lang
    # Язык значения следует за интерфейсом, как и в прежней версии.
    # Исключение — если он совпал бы с изучаемым языком.
    if new_lang != user.learning_lang:
        user.native_lang = new_lang
    _sync_legacy_mode(user)
    await session.commit()

    lang_display = get_text(f"lang_{new_lang}", new_lang)

    await callback.answer(
        get_text("language_changed", new_lang, language=lang_display),
        show_alert=True
    )

    # Новый язык нужен и нижнему меню, и строке якоря — якорь пересоздаётся
    await _show_after_change(callback, session, user, renew_anchor=True)


# ============================================================================
# НАВИГАЦИЯ
# ============================================================================

# Прежняя `_refresh_anchor_keyboard` удалена: см. `_renew_anchor` выше.


# ============================================================================
# ОЗВУЧКА: выключатель и выбор голоса с прослушиванием
# ============================================================================

def _audio_text(user: User, lang: str, voice_name: str) -> str:
    state_key = "audio_state_on" if user.audio_enabled else "audio_state_off"
    lines = [
        get_text("audio_title", lang),
        "",
        get_text("audio_description", lang),
        "",
        get_text("settings_audio_line", lang, state=get_text(state_key, lang)),
    ]
    # Голос показываем только когда озвучка включена: иначе это мёртвая строка
    if user.audio_enabled:
        lines.append(get_text("audio_current_voice", lang, voice=voice_name))
    return "\n".join(lines)


def _voice_label(code: str, voice_name: str) -> str:
    """Подпись голоса: имя и пол. Реестр — единственный источник имён."""
    for voice in voices_for(code):
        if voice.name == voice_name:
            return voice.label
    return voice_name


@router.callback_query(F.data == "settings_audio")
async def settings_audio(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()
    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or DEFAULT_LOCALE
    pair = pair_from_user(user)

    chosen = await voice_for_user(session, user.id, pair.learning)

    buttons = [
        InlineKeyboardButton(
            text=get_text(
                "audio_btn_turn_off" if user.audio_enabled else "audio_btn_turn_on", lang
            ),
            callback_data="audio_toggle",
        )
    ]
    if user.audio_enabled:
        buttons.append(
            InlineKeyboardButton(
                text=get_text("audio_btn_choose_voice", lang),
                callback_data="audio_voices",
            )
        )

    await callback.message.edit_text(
        _audio_text(user, lang, _voice_label(pair.learning, chosen)),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[b] for b in buttons] + [_back_row(lang, _PARENT_GROUP["settings_audio"])]
        ),
    )


@router.callback_query(F.data == "audio_toggle")
async def audio_toggle(callback: CallbackQuery, session: AsyncSession):
    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or DEFAULT_LOCALE

    user.audio_enabled = not user.audio_enabled
    await session.commit()

    await callback.answer(
        get_text("audio_turned_on" if user.audio_enabled else "audio_turned_off", lang)
    )
    await settings_audio(callback, session)


async def _voice_probes(session: AsyncSession, learning: str) -> list[tuple[str, str]]:
    """
    Несколько частотных слов языка — по ним судим, готов ли голос.

    БЕРУТСЯ ТОЛЬКО КАНОНИЧЕСКИЕ РЯДЫ, и это не формальность. Клип нужен не
    каждому ряду, а каждому каноническому в своём языке: ряды, дающие на
    этом языке одно и то же слово, схлопнуты в группу и делят один клип.
    Синтез обходил именно канонические.

    Первая редакция брала просто четыре самых частотных ряда — и два из
    четырёх («sie», «ist») оказались неканоническими для немецкого, клипов
    у них нет ни у одного голоса. Основная Катя с её двадцатью четырьмя
    тысячами клипов получала отметку «синтез на лету».

    Это уже второй раз, когда забытая каноничность даёт ложный ответ:
    первый был в `state_report`, где счёт по всем рядам показал
    семнадцать тысяч несуществующих пропаж.

    ПРОБЫ БЕРУТСЯ С ДВУХ КОНЦОВ ЧАСТОТНОГО СПИСКА. Синтез идёт от частотных
    к редким, поэтому у начатого, но не доведённого голоса частотные слова
    уже есть, а редких нет. Пробуй только частотные — и русский Дмитрий с
    2 704 клипами из 19 689 получит отметку «мгновенно», хотя не хватает
    восьмидесяти шести процентов.

    Редкое слово отвечает на вопрос «досинтезирован ли голос ДО КОНЦА», и
    только такой ответ честен перед учеником.
    """
    from app.database.models import Word, WordLangGroup

    from app.services.audio_service import KIND_WORD, spoken_for

    def query(order):
        return (
            select(Word)
            .join(
                WordLangGroup,
                (WordLangGroup.word_id == Word.id)
                & (WordLangGroup.lang == learning)
                & (WordLangGroup.is_canonical.is_(True)),
            )
            .order_by(order)
            .limit(2)
        )

    probes: list[tuple[str, str]] = []
    for order in (Word.frequency_rank, Word.frequency_rank.desc()):
        rows = await session.execute(query(order))
        for word in rows.scalars():
            spoken = spoken_for(word, learning, KIND_WORD)
            if spoken:
                probes.append((KIND_WORD, spoken))
    return probes


async def _voices_screen(
    session: AsyncSession, user: User, lang: str, pair,
    listening: Optional[str] = None,
) -> tuple[str, InlineKeyboardMarkup]:
    """
    Экран голосов: слушать — одно, выбрать — другое.

    ПОЧЕМУ ОНИ РАЗДЕЛЕНЫ. Прежде нажатие на голос СРАЗУ его и сохраняло,
    а образец присылало заодно. Выглядело разумно, пока владелец не
    перебрал голоса подряд, чтобы сравнить: Катя, Амала, Серафина, Конрад,
    Килиан — и получил последний, а не понравившийся. Дословно: «выбрал
    Серафину — в настройках бота один голос, а в игре другой». В логе
    видно ровно это: пять сохранений за двадцать восемь секунд.

    Текст экрана при этом всё время обещал правду: «нажми на голос, чтобы
    послушать; галочкой отмечен выбранный». Врал не текст, а код.

    Теперь так и есть:
        нажатие на голос     присылает образец, ничего не меняя
        🎧 у голоса          его слушаешь сейчас
        ✓ у голоса           он выбран и звучит в занятии
        кнопка «Выбрать»     единственное, что сохраняет

    `listening` — голос, образец которого только что отправлен. Нигде не
    хранится: он нужен ровно на один показ экрана, и помнить его между
    нажатиями значило бы завести состояние ради подписи кнопки.
    """
    chosen = await voice_for_user(session, user.id, pair.learning)
    probes = await _voice_probes(session, pair.learning)

    rows: list[list[InlineKeyboardButton]] = []
    for gender, header_key in (("female", "voice_female"), ("male", "voice_male")):
        group = by_gender(pair.learning, gender)
        if not group:
            continue
        rows.append([InlineKeyboardButton(
            text=f"— {get_text(header_key, lang)} —", callback_data="noop"
        )])
        rows.extend(_grid(
            [
                InlineKeyboardButton(
                    # Точка у голосов БЕЗ готовых клипов. Предсинтезированы
                    # не все: это гигабайты и часы на каждый, а у остальных
                    # слово синтезируется на лету и примерно в одном случае
                    # из пяти приходит без звука. Пока все голоса выглядели
                    # одинаково, узнать причину немоты было неоткуда
                    text=("✓ " if v.name == chosen
                          else "🎧 " if v.name == listening else "")
                         + v.label
                         + ("" if voice_is_ready(pair.learning, v.name, probes) else " ·"),
                    callback_data=f"audio_voice_{v.name}",
                )
                for v in group
            ],
            per_row=3,
        ))

    # Кнопка выбора появляется только после прослушивания, и только если
    # слушали НЕ тот голос, который уже стоит: «выбрать выбранное» —
    # кнопка без действия.
    if listening and listening != chosen:
        rows.append([InlineKeyboardButton(
            text=get_text("voice_use", lang,
                          voice=_voice_label(pair.learning, listening)),
            callback_data=f"voice_use_{listening}",
        )])

    text = (
        f"{get_text('voice_title', lang)}\n\n"
        f"{get_text('voice_description', lang)}"
    )
    # Там, где выбора почти нет, честнее это сказать, чем делать вид,
    # что голосов много
    if len(voices_for(pair.learning)) <= 2:
        text += f"\n\n<i>{get_text('voice_only_one', lang)}</i>"

    return text, InlineKeyboardMarkup(
        inline_keyboard=rows + [_back_row(lang, "settings_audio")]
    )


async def _show_voices(callback: CallbackQuery, session: AsyncSession,
                       listening: Optional[str] = None) -> None:
    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or DEFAULT_LOCALE
    pair = pair_from_user(user)
    text, keyboard = await _voices_screen(session, user, lang, pair, listening)
    try:
        await callback.message.edit_text(text, reply_markup=keyboard)
    except TelegramBadRequest:
        # «message is not modified»: повторное нажатие на тот же голос
        # ничего в экране не меняет. Это не ошибка, и в журнал она попадать
        # не должна — у живого человека таких записей набралось две за
        # четыре минуты.
        pass


@router.callback_query(F.data == "audio_voices")
async def audio_voices(callback: CallbackQuery, session: AsyncSession):
    """
    Список голосов изучаемого языка, отдельно мужские и женские.

    Голоса берутся из реестра, а не выписываются: их число на язык разное —
    для немецкого шесть, для польского и остальных два, потому что больше
    у синтезатора не существует.
    """
    await callback.answer()
    await _show_voices(callback, session)


@router.callback_query(F.data.startswith("voice_use_"))
async def audio_voice_use(callback: CallbackQuery, session: AsyncSession):
    """ВЫБОР голоса — единственное место, где он сохраняется."""
    voice_name = callback.data.removeprefix("voice_use_")

    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or DEFAULT_LOCALE
    pair = pair_from_user(user)

    if not is_valid_voice(voice_name, pair.learning):
        await callback.answer(get_text("voice_preview_failed", lang), show_alert=True)
        return

    await set_voice_for_user(session, user.id, pair.learning, voice_name)
    await session.commit()

    label = _voice_label(pair.learning, voice_name)
    await callback.answer(get_text("voice_set", lang, voice=label))
    await _show_voices(callback, session)


@router.callback_query(F.data.startswith("audio_voice_"))
async def audio_voice_preview(callback: CallbackQuery, session: AsyncSession):
    """
    ПРОСЛУШИВАНИЕ голоса. Ничего не сохраняет.

    Порядок обработчиков тут значим: `voice_use_` объявлен ВЫШЕ и имеет
    свою приставку, иначе `audio_voice_` перехватывал бы и выбор.
    """
    voice_name = callback.data.removeprefix("audio_voice_")

    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or DEFAULT_LOCALE
    pair = pair_from_user(user)

    if not is_valid_voice(voice_name, pair.learning):
        await callback.answer(get_text("voice_preview_failed", lang), show_alert=True)
        return

    label = _voice_label(pair.learning, voice_name)
    await callback.answer(get_text("voice_listening", lang, voice=label))
    await _show_voices(callback, session, listening=voice_name)

    # Образец — отдельным сообщением: карточка настроек остаётся на месте,
    # и её не приходится превращать в медийную ради прослушивания
    sample = await synthesize_preview(pair.learning, voice_name)
    if sample is None:
        await callback.message.answer(get_text("voice_preview_failed", lang))
    else:
        await callback.bot.send_audio(
            callback.message.chat.id,
            BufferedInputFile(sample, filename=f"{label}.mp3"),
            title=label,
        )
    # Экран уже перерисован ВЫШЕ, до синтеза: пометка 🎧 должна появиться
    # сразу по нажатию, а образец приходит через секунду. Повторная
    # перерисовка здесь стирала бы её и вдобавок вызывала `callback.answer`
    # второй раз.


@router.callback_query(F.data == "back_to_settings")
async def back_to_settings(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()
    await show_settings_callback(callback, session)


@router.callback_query(F.data == "back_to_menu")
async def back_to_main_menu(callback: CallbackQuery):
    await callback.answer()
    try:
        await callback.message.delete()
    except Exception:
        logger.debug("Не удалось удалить сообщение", exc_info=True)
