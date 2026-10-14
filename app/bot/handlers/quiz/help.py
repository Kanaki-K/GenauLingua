"""
Помощь и поддержка с локализацией
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.filters import Command

import logging

logger = logging.getLogger(__name__)

from app.database.models import User
from app.bot.utils import delete_messages_fast, ensure_anchor
from app.bot.buttons import BTN_HELP, pressed
from app.services.language_service import (
    interface_names,
    learnable_count,
    learnable_names,
)
from app.locales import DEFAULT_LOCALE, get_text, plural

router = Router()

# Пометка «пришёл из настроек». Помощь живёт в группе «Бот», и прежде её
# экран кончался двумя кнопками без «Назад»: вернуться в настройки было
# нельзя ничем, кроме нижнего меню (аудит 14 октября). Из команды /help
# возвращаться некуда — там «Назад» и не рисуется.
FROM_SETTINGS = "settings"


def _help_text(lang: str) -> str:
    return (
        f"{get_text('help_title', lang)}\n\n"
        f"{get_text('help_description', lang)}\n\n"
        f"{get_text('help_choose', lang)}"
    )


def _back_to_help(lang: str, origin: str) -> InlineKeyboardMarkup:
    tail = f":{origin}" if origin else ""
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(
            text=get_text("btn_back", lang),
            callback_data=f"help_back{tail}"
        )]]
    )


def get_help_keyboard(lang: str, origin: str = "") -> InlineKeyboardMarkup:
    """
    Два экрана вместо четырёх.

    Убран «🚀 Скоро в боте»: он обещал подготовку к Goethe/ÖSD, тексты на
    немецком и грамматику с падежами — то есть врал всем, кто учит не
    немецкий, а таких теперь пять языков из шести. Обещания стареют, и
    держать их в интерфейсе дороже, чем в чате сообщества.

    «ℹ️ О боте» слит с «💬 Сообществом»: оба экрана кончались одной и той же
    ссылкой на чат.
    """
    tail = f":{origin}" if origin else ""
    rows = [
        [InlineKeyboardButton(
            text=get_text("help_btn_how_to_use", lang),
            callback_data=f"help_how_to_use{tail}"
        )],
        [InlineKeyboardButton(
            text=get_text("help_btn_community", lang),
            callback_data=f"help_community{tail}"
        )],
    ]
    if origin == FROM_SETTINGS:
        rows.append([InlineKeyboardButton(
            text=get_text("btn_back", lang),
            callback_data="settings_group_bot"
        )])
    return InlineKeyboardMarkup(inline_keyboard=rows)


# ============================================================================
# ГЛАВНОЕ МЕНЮ ПОМОЩИ
# ============================================================================

@router.callback_query(F.data == "settings_help")
async def show_help_from_settings(callback: CallbackQuery, session: AsyncSession):
    """Помощь из настроек — её единственный вход, кроме команды /help."""
    await callback.answer()
    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language if user else DEFAULT_LOCALE

    await callback.message.edit_text(
        _help_text(lang), reply_markup=get_help_keyboard(lang, FROM_SETTINGS)
    )


@router.message(Command("help"))
# Кнопки «❓ Помощь» в главном меню больше нет — она уехала в настройки.
# Фильтр по её надписи оставлен: у людей, не перезапускавших бота, старая
# клавиатура живёт в клиенте Telegram и шлёт прежний текст. Убери фильтр —
# и у них кнопка молча перестанет работать.
@router.message(pressed(BTN_HELP))
async def show_help(message: Message, session: AsyncSession):
    """Показ меню помощи"""
    user = await session.get(User, message.from_user.id)
    lang = user.interface_language if user else DEFAULT_LOCALE

    help_text = _help_text(lang)

    try:
        await message.delete()
    except Exception:
        pass

    if user:
        old_anchor_id, new_anchor_id = await ensure_anchor(message, session, user, emoji="")
        if old_anchor_id:
            current_msg_id = message.message_id
            await delete_messages_fast(message.bot, message.chat.id, old_anchor_id, current_msg_id)

    await message.answer(help_text, reply_markup=get_help_keyboard(lang))


# ============================================================================
# КАК ПОЛЬЗОВАТЬСЯ
# ============================================================================

@router.callback_query(F.data.startswith("help_how_to_use"))
async def show_how_to_use(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()

    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language if user else DEFAULT_LOCALE

    # Значение считается заранее, а не внутри вызова: tests/test_locales.py
    # сверяет подстановки в тексте с переданными параметрами, разбирая вызов
    # регулярным выражением, и на скобках внутри аргумента разбор обрывается
    languages = learnable_names(lang)
    # ДЛИНА КРУГА — ИЗ ТОГО ЖЕ МЕСТА, ЧТО У ИГРЫ. В тексте стояло «25 слов»
    # во всех шести языках, а круг — 15: число жило отдельно от правила
    from app.bot.handlers.quiz.game import DEFAULT_QUIZ_LENGTH

    length = (user.quiz_word_count if user else None) or DEFAULT_QUIZ_LENGTH
    words = plural(length, "plural_words", lang)

    text = (
        f"{get_text('help_how_to_use_title', lang)}\n\n"
        f"{get_text('help_how_to_use_text', lang, languages=languages, words=words)}"
    )

    origin = callback.data.partition(":")[2]
    await callback.message.edit_text(text, reply_markup=_back_to_help(lang, origin))


# ============================================================================
# О БОТЕ И СООБЩЕСТВО — один экран вместо двух
# ============================================================================

@router.callback_query(F.data.startswith("help_community"))
async def show_community(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()

    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language if user else DEFAULT_LOCALE

    # Значения считаются заранее, а не внутри вызова: tests/test_locales.py
    # сверяет подстановки с переданными параметрами, разбирая вызов
    # регулярным выражением, и на скобках внутри аргумента разбор обрывается
    languages = learnable_names(lang)
    language_count = learnable_count()
    interface_languages = interface_names(lang)

    text = (
        f"{get_text('help_community_title', lang)}\n\n"
        f"{get_text('help_community_text', lang, languages=languages, language_count=language_count, interface_languages=interface_languages)}"
    )

    origin = callback.data.partition(":")[2]
    await callback.message.edit_text(text, reply_markup=_back_to_help(lang, origin))


# ============================================================================
# НАВИГАЦИЯ
# ============================================================================

@router.callback_query(F.data.startswith("help_back"))
async def back_to_help(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()

    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language if user else DEFAULT_LOCALE

    origin = callback.data.partition(":")[2]
    await callback.message.edit_text(
        _help_text(lang), reply_markup=get_help_keyboard(lang, origin)
    )

# Обработчик `back_to_menu` отсюда убран. Он был зарегистрирован ДВАЖДЫ — и
# здесь, и в settings.py — при том, что кнопки, которая шлёт такой callback,
# в боте нет ни одной. Двойная регистрация безвредна только пока callback не
# приходит; стоит кому-то добавить кнопку, и сработает тот роутер, который
# подключён раньше, то есть поведение определялось бы порядком в main.py.
# Живой обработчик остался один, в settings.py.