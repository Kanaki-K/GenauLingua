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

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import (
    BufferedInputFile,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.buttons import BTN_SETTINGS, pressed
from app.bot.keyboards import get_main_menu_keyboard
from app.bot.utils import delete_messages_fast, ensure_anchor
from app.database.enums import CEFRLevel, QuizMode, WordCategory
from app.database.models import User
from app.locales import get_text
from app.services.audio_service import (
    set_voice_for_user,
    synthesize_preview,
    voice_for_user,
)
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

def get_settings_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=get_text("settings_btn_quiz_mode", lang),
                callback_data="settings_quiz_mode"
            )],
            [InlineKeyboardButton(
                text=get_text("settings_btn_learning_lang", lang),
                callback_data="settings_learning"
            )],
            [InlineKeyboardButton(
                text=get_text("settings_btn_audio", lang),
                callback_data="settings_audio"
            )],
            [InlineKeyboardButton(
                text=get_text("settings_btn_change_mode", lang),
                callback_data="settings_mode"
            )],
            [InlineKeyboardButton(
                text=get_text("settings_btn_change_language", lang),
                callback_data="settings_language"
            )],
            [InlineKeyboardButton(
                text=get_text("settings_btn_notifications", lang),
                callback_data="settings:notifications"
            )]
        ]
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


def _settings_text(user: User, lang: str) -> str:
    pair = pair_from_user(user)
    mode_display = pair_label(pair)
    lang_display = get_text(f"lang_{user.interface_language}", lang) if user.interface_language else "—"
    audio_state_key = "audio_state_on" if user.audio_enabled else "audio_state_off"

    return (
        f"{get_text('settings_title', lang)}\n\n"
        f"{get_text('settings_quiz_mode_line', lang, mode=_quiz_mode_display(user, lang))}\n"
        f"{get_text('settings_learning_lang_line', lang, language=language_name(pair.learning, lang))}\n"
        f"{get_text('settings_audio_line', lang, state=get_text(audio_state_key, lang))}\n"
        f"{get_text('settings_mode', lang, mode=mode_display)}\n"
        f"{get_text('settings_language', lang, language=lang_display)}\n\n"
        f"{get_text('settings_choose', lang)}"
    )


@router.message(Command("settings"))
@router.message(pressed(BTN_SETTINGS))
async def show_settings(message: Message, session: AsyncSession):
    """Показ меню настроек"""
    user = await session.get(User, message.from_user.id)

    if not user:
        await message.answer(get_text("user_not_found", "ru"))
        return

    lang = user.interface_language or "ru"

    try:
        await message.delete()
    except Exception:
        logger.debug("Не удалось удалить сообщение пользователя", exc_info=True)

    old_anchor_id, _ = await ensure_anchor(message, session, user, emoji="🦾")
    if old_anchor_id:
        await delete_messages_fast(message.bot, message.chat.id, old_anchor_id, message.message_id)

    await message.answer(_settings_text(user, lang), reply_markup=get_settings_keyboard(lang))


async def show_settings_callback(callback: CallbackQuery, session: AsyncSession):
    """Показ настроек после изменения (для callback)"""
    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or "ru"
    await callback.message.edit_text(
        _settings_text(user, lang), reply_markup=get_settings_keyboard(lang)
    )


# ============================================================================
# ИЗУЧАЕМЫЙ ЯЗЫК
# ============================================================================

@router.callback_query(F.data == "settings_learning")
async def show_learning_lang(callback: CallbackQuery, session: AsyncSession):
    """Показать выбор изучаемого языка"""
    await callback.answer()

    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or "ru"
    pair = pair_from_user(user)

    buttons = [
        InlineKeyboardButton(
            text=("✅ " if code == pair.learning else "") + language_name(code, lang),
            callback_data=f"set_learning_{code}",
        )
        for code in LEARNABLE_LANGS
    ]

    text = (
        f"{get_text('learning_lang_title', lang)}\n\n"
        f"{get_text('learning_lang_description', lang)}"
    )

    await callback.message.edit_text(
        text, reply_markup=InlineKeyboardMarkup(inline_keyboard=_grid(buttons) + [_back_row(lang)])
    )


@router.callback_query(F.data.startswith("set_learning_"))
async def set_learning_lang(callback: CallbackQuery, session: AsyncSession):
    """Установить изучаемый язык"""
    code = callback.data.removeprefix("set_learning_")

    if not is_learnable(code):
        await callback.answer("❌ Error", show_alert=True)
        return

    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or "ru"

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
    await show_settings_callback(callback, session)


# ============================================================================
# РЕЖИМ ВИКТОРИНЫ — главное подменю (4 кнопки 2x2)
# ============================================================================

def get_quiz_mode_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=get_text("qmode_btn_level", lang),
                    callback_data="qmode_level"
                ),
                InlineKeyboardButton(
                    text=get_text("qmode_btn_category", lang),
                    callback_data="qmode_category_page_1"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_text("qmode_btn_all", lang),
                    callback_data="qmode_all"
                ),
                InlineKeyboardButton(
                    text=get_text("qmode_btn_difficult", lang),
                    callback_data="qmode_difficult"
                ),
            ],
            _back_row(lang)
        ]
    )


@router.callback_query(F.data == "settings_quiz_mode")
async def show_quiz_mode(callback: CallbackQuery, session: AsyncSession):
    """Показать меню выбора режима викторины"""
    await callback.answer()

    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or "ru"

    text = (
        f"{get_text('qmode_title', lang)}\n\n"
        f"{get_text('qmode_current', lang, mode=_quiz_mode_display(user, lang))}\n\n"
        f"{get_text('qmode_choose', lang)}"
    )

    await callback.message.edit_text(text, reply_markup=get_quiz_mode_keyboard(lang))


# ============================================================================
# РЕЖИМ: ПО УРОВНЮ (A1–C2)
# ============================================================================

@router.callback_query(F.data == "qmode_level")
async def show_level_selection(callback: CallbackQuery, session: AsyncSession):
    """Показать выбор уровня для режима 'По уровню'"""
    await callback.answer()

    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or "ru"

    text = (
        f"{get_text('qmode_level_title', lang)}\n\n"
        f"{get_text('qmode_level_desc', lang)}"
    )

    levels = [
        InlineKeyboardButton(text=level.value, callback_data=f"qmode_set_level_{level.value}")
        for level in CEFRLevel
    ]
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=_grid(levels, per_row=3) + [_back_row(lang, "settings_quiz_mode")]
    )

    await callback.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(F.data.startswith("qmode_set_level_"))
async def set_quiz_mode_level(callback: CallbackQuery, session: AsyncSession):
    """Установить режим 'По уровню' с конкретным уровнем"""
    level_str = callback.data.removeprefix("qmode_set_level_")

    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or "ru"

    try:
        user.level = CEFRLevel(level_str)
    except ValueError:
        await callback.answer("❌ Error", show_alert=True)
        return

    user.quiz_mode = QuizMode.LEVEL
    user.quiz_category = None
    await session.commit()

    await callback.answer(get_text("qmode_level_set", lang, level=level_str), show_alert=True)

    await _refresh_anchor_keyboard(callback, user, lang)
    await show_settings_callback(callback, session)


# ============================================================================
# РЕЖИМ: ПО КАТЕГОРИИ (пагинация 10 на страницу)
# ============================================================================

def get_category_keyboard(page: int, lang: str) -> InlineKeyboardMarkup:
    """Клавиатура категорий с пагинацией"""
    categories = CATEGORIES_PAGE_1 if page == 1 else CATEGORIES_PAGE_2
    total_pages = 2

    buttons = [
        InlineKeyboardButton(
            text=get_category_display(cat.value, lang),
            callback_data=f"qmode_set_cat_{cat.name}",
        )
        for cat in categories
    ]
    rows = _grid(buttons)

    # Пагинация
    nav_row = []
    if page > 1:
        nav_row.append(InlineKeyboardButton(text="◀", callback_data=f"qmode_category_page_{page - 1}"))
    nav_row.append(InlineKeyboardButton(text=f"{page} / {total_pages}", callback_data="noop"))
    if page < total_pages:
        nav_row.append(InlineKeyboardButton(text="▶", callback_data=f"qmode_category_page_{page + 1}"))
    rows.append(nav_row)

    rows.append(_back_row(lang, "settings_quiz_mode"))

    return InlineKeyboardMarkup(inline_keyboard=rows)


@router.callback_query(F.data.startswith("qmode_category_page_"))
async def show_category_page(callback: CallbackQuery, session: AsyncSession):
    """Показать страницу категорий"""
    await callback.answer()

    page = int(callback.data.removeprefix("qmode_category_page_"))
    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or "ru"

    text = (
        f"{get_text('qmode_category_title', lang)}\n\n"
        f"{get_text('qmode_category_desc', lang)}"
    )

    await callback.message.edit_text(text, reply_markup=get_category_keyboard(page, lang))


@router.callback_query(F.data.startswith("qmode_set_cat_"))
async def set_quiz_mode_category(callback: CallbackQuery, session: AsyncSession):
    """Установить режим 'По категории'"""
    cat_name = callback.data.removeprefix("qmode_set_cat_")

    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or "ru"

    try:
        cat = WordCategory[cat_name]
    except KeyError:
        await callback.answer("❌ Error", show_alert=True)
        return

    user.quiz_mode = QuizMode.CATEGORY
    user.quiz_category = cat.value
    await session.commit()

    display_name = get_category_display(cat.value, lang)
    await callback.answer(
        get_text("qmode_category_set", lang, category=display_name),
        show_alert=True
    )

    await show_settings_callback(callback, session)


# ============================================================================
# РЕЖИМ: ТОП 10К (ВСЕ СЛОВА)
# ============================================================================

@router.callback_query(F.data == "qmode_all")
async def set_quiz_mode_all(callback: CallbackQuery, session: AsyncSession):
    """Установить режим 'Все слова'"""
    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or "ru"

    user.quiz_mode = QuizMode.ALL_WORDS
    user.quiz_category = None
    await session.commit()

    await callback.answer(get_text("qmode_all_set", lang), show_alert=True)
    await show_settings_callback(callback, session)


# ============================================================================
# РЕЖИМ: СЛОЖНЫЕ СЛОВА
# ============================================================================

@router.callback_query(F.data == "qmode_difficult")
async def set_quiz_mode_difficult(callback: CallbackQuery, session: AsyncSession):
    """Установить режим 'Сложные слова'"""
    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or "ru"

    user.quiz_mode = QuizMode.DIFFICULT
    user.quiz_category = None
    await session.commit()

    await callback.answer(get_text("qmode_difficult_set", lang), show_alert=True)
    await show_settings_callback(callback, session)


# ============================================================================
# NOOP (для неактивных кнопок типа "1/2")
# ============================================================================

@router.callback_query(F.data == "noop")
async def noop_handler(callback: CallbackQuery):
    await callback.answer()


# ============================================================================
# ИЗМЕНЕНИЕ РЕЖИМА ПЕРЕВОДА (направление вопроса)
# ============================================================================

@router.callback_query(F.data == "settings_mode")
async def change_translation_mode(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()

    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or "ru"
    pair = pair_from_user(user)

    forward = LanguagePair(learning=pair.learning, native=pair.native, reverse=False)
    reverse = LanguagePair(learning=pair.learning, native=pair.native, reverse=True)

    # Подсказки заведены только для пар с немецким; для остальных опускаем
    hints = ""
    for candidate in (forward, reverse):
        key = f"settings_mode_hint_{candidate.prompt_lang}_{candidate.answer_lang}"
        hint = get_text(key, lang)
        if not hint.startswith("[MISSING:"):
            hints += f"\n{hint}"

    text = (
        f"{get_text('settings_mode_title', lang)}\n\n"
        f"{get_text('settings_mode_description', lang)}"
        f"{hints}"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=("✅ " if not pair.reverse else "") + pair_label(forward),
                callback_data="set_dir_forward"
            )],
            [InlineKeyboardButton(
                text=("✅ " if pair.reverse else "") + pair_label(reverse),
                callback_data="set_dir_reverse"
            )],
            _back_row(lang)
        ]
    )

    await callback.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(F.data.startswith("set_dir_"))
async def set_translation_direction(callback: CallbackQuery, session: AsyncSession):
    reverse = callback.data.removeprefix("set_dir_") == "reverse"

    user = await session.get(User, callback.from_user.id)

    user.reverse_mode = reverse
    _sync_legacy_mode(user)
    await session.commit()

    await callback.answer(f"✅ {pair_label(pair_from_user(user))}", show_alert=True)
    await show_settings_callback(callback, session)


# ============================================================================
# ИЗМЕНЕНИЕ ЯЗЫКА ИНТЕРФЕЙСА
# ============================================================================

@router.callback_query(F.data == "settings_language")
async def change_interface_language(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()

    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or "ru"

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
    keyboard = InlineKeyboardMarkup(inline_keyboard=_grid(buttons) + [_back_row(lang)])

    await callback.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(F.data.startswith("iface_lang_"))
async def set_interface_language(callback: CallbackQuery, session: AsyncSession):
    new_lang = callback.data.removeprefix("iface_lang_")

    if new_lang not in INTERFACE_LANGS:
        await callback.answer("❌ Error", show_alert=True)
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

    await _refresh_anchor_keyboard(callback, user, new_lang)

    await callback.answer(
        get_text("language_changed", new_lang, language=lang_display),
        show_alert=True
    )

    await show_settings_callback(callback, session)


# ============================================================================
# НАВИГАЦИЯ
# ============================================================================

async def _refresh_anchor_keyboard(callback: CallbackQuery, user: User, lang: str) -> None:
    """Обновить главное меню в якорном сообщении под новый язык"""
    if not user.anchor_message_id:
        return
    try:
        await callback.bot.edit_message_reply_markup(
            chat_id=callback.message.chat.id,
            message_id=user.anchor_message_id,
            reply_markup=get_main_menu_keyboard(lang)
        )
    except Exception:
        logger.debug("Не удалось обновить якорную клавиатуру", exc_info=True)


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
    lang = user.interface_language or "ru"
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
            inline_keyboard=[[b] for b in buttons] + [_back_row(lang)]
        ),
    )


@router.callback_query(F.data == "audio_toggle")
async def audio_toggle(callback: CallbackQuery, session: AsyncSession):
    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or "ru"

    user.audio_enabled = not user.audio_enabled
    await session.commit()

    await callback.answer(
        get_text("audio_turned_on" if user.audio_enabled else "audio_turned_off", lang)
    )
    await settings_audio(callback, session)


@router.callback_query(F.data == "audio_voices")
async def audio_voices(callback: CallbackQuery, session: AsyncSession):
    """
    Список голосов изучаемого языка, отдельно мужские и женские.

    Голоса берутся из реестра, а не выписываются: их число на язык разное —
    для немецкого шесть, для польского и остальных два, потому что больше
    у синтезатора не существует.
    """
    await callback.answer()
    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or "ru"
    pair = pair_from_user(user)

    chosen = await voice_for_user(session, user.id, pair.learning)

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
                    text=("✅ " if v.name == chosen else "") + v.label,
                    callback_data=f"audio_voice_{v.name}",
                )
                for v in group
            ],
            per_row=3,
        ))

    text = (
        f"{get_text('voice_title', lang)}\n\n"
        f"{get_text('voice_description', lang)}"
    )
    # Там, где выбора почти нет, честнее это сказать, чем делать вид,
    # что голосов много
    if len(voices_for(pair.learning)) <= 2:
        text += f"\n\n<i>{get_text('voice_only_one', lang)}</i>"

    await callback.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=rows + [_back_row(lang, "settings_audio")]
        ),
    )


@router.callback_query(F.data.startswith("audio_voice_"))
async def audio_voice_chosen(callback: CallbackQuery, session: AsyncSession):
    """
    Выбор голоса. Он же и прослушивание: нажатие сразу присылает образец,
    чтобы услышать голос, а не угадывать его по имени.
    """
    voice_name = callback.data.removeprefix("audio_voice_")

    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or "ru"
    pair = pair_from_user(user)

    if not is_valid_voice(voice_name, pair.learning):
        await callback.answer(get_text("voice_preview_failed", lang), show_alert=True)
        return

    await set_voice_for_user(session, user.id, pair.learning, voice_name)
    await session.commit()

    label = _voice_label(pair.learning, voice_name)
    await callback.answer(get_text("voice_set", lang, voice=label))

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

    await audio_voices(callback, session)


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
