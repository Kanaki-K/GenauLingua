"""
Обработчик команды /start и выбор языка
"""

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

import logging

logger = logging.getLogger(__name__)

from app.bot.states import QuizStates
from app.bot.utils import delete_messages_fast, ensure_anchor
from app.database.enums import CEFRLevel, QuizMode
from app.database.models import User
from app.locales import DEFAULT_LOCALE, LOCALES, get_text
from app.services.language_service import (
    INTERFACE_LANGS,
    LEARNABLE_LANGS,
    fallback_native_for,
    is_learnable,
    learnable_names,
    legacy_mode_name,
    pair_from_user,
)

router = Router()


def _grid(buttons: list[InlineKeyboardButton], per_row: int = 2) -> list[list[InlineKeyboardButton]]:
    return [buttons[i:i + per_row] for i in range(0, len(buttons), per_row)]


def get_language_selection_keyboard() -> InlineKeyboardMarkup:
    """
    Выбор языка интерфейса при первом запуске.

    Список берётся из INTERFACE_LANGS, а не вписывается руками. Прежде здесь
    стояли ЧЕТЫРЕ кнопки, тогда как локалей уже шесть: немецкая и польская
    написаны полностью (по 522 строки, тест следит за совпадением ключей) — и
    были недостижимы. Немец и поляк при первом запуске свой язык выбрать не
    могли, хотя в настройках он есть.

    Надпись берётся из САМОЙ локали этого языка: человек, не знающий ни одного
    из остальных, должен узнать свой.
    """
    buttons = [
        InlineKeyboardButton(
            text=LOCALES[code].get(f"lang_{code}", code),
            callback_data=f"select_lang_{code}",
        )
        for code in INTERFACE_LANGS
    ]
    return InlineKeyboardMarkup(inline_keyboard=_grid(buttons))


def get_learning_keyboard(native: str, lang: str) -> InlineKeyboardMarkup:
    """
    Выбор ИЗУЧАЕМОГО языка — второй шаг онбординга.

    Прежде этого шага не было вовсе: новому человеку молча ставился немецкий
    (`user.learning_lang = "de"`), а сменить его можно было только в
    настройках, на третьем уровне вложенности. Отсюда и цифра, с которой
    начался этот разбор: 233 пользователя из 233 учили немецкий.

    Свой же язык из списка убран: учить язык, на котором тебе показывают
    значения, — вырожденная задача «слово = слово».
    """
    buttons = [
        InlineKeyboardButton(
            text=get_text(f"langname_{code}", lang),
            callback_data=f"onboard_learn_{code}",
        )
        for code in LEARNABLE_LANGS
        if code != native
    ]
    return InlineKeyboardMarkup(inline_keyboard=_grid(buttons))


def _language_selection_text() -> str:
    """
    Самый первый экран: человек ещё не выбрал язык, значит понять его нельзя.

    Поэтому приглашение написано на ВСЕХ шести сразу, строка берётся из каждой
    локали. Прежде здесь стоял флаг 🇩🇪 и четыре строки — флаг обещал немецкий,
    которого бот больше не обещает, а четырёх строк не хватало на шесть кнопок.
    """
    lines = "\n".join(
        f"{LOCALES[code]['lang_' + code].split()[0]} "
        f"{LOCALES[code]['settings_language_description']}"
        for code in INTERFACE_LANGS
    )
    return f"🌍 <b>GenauLingua</b>\n\n{lines}"


def get_level_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Клавиатура выбора уровня — все уровни разблокированы"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="A1", callback_data="start_level_A1"),
                InlineKeyboardButton(text="A2", callback_data="start_level_A2"),
                InlineKeyboardButton(text="B1", callback_data="start_level_B1")
            ],
            [
                InlineKeyboardButton(text="B2", callback_data="start_level_B2"),
                InlineKeyboardButton(text="C1", callback_data="start_level_C1"),
                InlineKeyboardButton(text="C2", callback_data="start_level_C2")
            ]
        ]
    )


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, session: AsyncSession):
    """Обработчик команды /start"""
    user_id = message.from_user.id

    await state.clear()

    try:
        await message.delete()
    except Exception:
        pass

    user = await session.get(User, user_id)

    if not user:
        user = User(
            id=user_id,
            username=message.from_user.username,
            first_name=message.from_user.first_name
        )
        session.add(user)
        await session.commit()

    # ========================================================================
    # ПРОВЕРКА: Если язык не выбран — показываем выбор языка
    # ========================================================================
    if not user.interface_language or user.interface_language == "reset":
        await message.answer(
            _language_selection_text(),
            reply_markup=get_language_selection_keyboard()
        )
        return

    # Язык уже выбран — продолжаем обычный flow
    lang = user.interface_language
    # Запасное обращение берётся из локали. Прежде здесь стояло русское «друг»
    # для всех: турок без имени в профиле получал русское слово.
    first_name = message.from_user.first_name or get_text("friend_fallback", lang)
    # Считаем ДО вызова: test_format_parameters_match разбирает get_text
    # регулярным выражением, и скобки внутри аргумента обрывают разбор
    languages = learnable_names(lang)

    welcome_text = (
        f"{get_text('welcome_title', lang, name=first_name)}\n\n"
        f"{get_text('welcome_description', lang, languages=languages)}\n\n"
        f"{get_text('welcome_separator', lang)}\n"
        f"{get_text('welcome_learn_words_title', lang)}\n"
        f"{get_text('welcome_learn_words_desc', lang)}\n\n"
        f"{get_text('welcome_stats_title', lang)}\n"
        f"{get_text('welcome_stats_desc', lang)}\n\n"
        f"{get_text('welcome_settings_title', lang)}\n"
        f"{get_text('welcome_settings_desc', lang)}\n\n"
        f"{get_text('welcome_help_title', lang)}\n"
        f"{get_text('welcome_help_desc', lang)}\n"
        f"{get_text('welcome_separator', lang)}\n\n"
    )

    if user.level:
        # ВЕРНУВШЕМУСЯ ЧЕЛОВЕКУ — ДОМАШНИЙ ЭКРАН, А НЕ ПЕРЕСКАЗ МЕНЮ.
        #
        # Здесь стояла простыня из восьми строк: «Учить слова — проверь себя»,
        # «Статистика — следи за прогрессом» и так далее. Польза от неё
        # кончается на первом прочтении, а показывалась она при каждом
        # `/start`, то есть пересказывала кнопки, которые человек и так видит
        # перед собой на клавиатуре.
        #
        # Новый человек этой ветки не видит вовсе: до неё нужен уровень, а
        # уровень ставится в конце онбординга, который сам всё и рассказывает.
        # Значит ветка целиком про тех, кто вернулся, — и им нужнее всего
        # ответ на вопрос «где я сейчас». Его и дают три шкалы.
        from app.bot.handlers.quiz.home import show_home

        old_anchor_id, new_anchor_id = await ensure_anchor(message, session, user, emoji="🤖")

        if old_anchor_id:
            current_msg_id = message.message_id
            await delete_messages_fast(message.bot, message.chat.id, old_anchor_id, current_msg_id)

        await show_home(message, session, user)
    else:
        # Уровень называет язык, к которому относится: A1 немецкого и A1
        # английского — разные словари, и без названия вопрос неполон
        learning_name = get_text(f"langname_{pair_from_user(user).learning}", lang)
        welcome_text += get_text('welcome_choose_level', lang, language=learning_name)

        await message.answer(
            welcome_text,
            reply_markup=get_level_keyboard(lang)
        )

        await state.set_state(QuizStates.choosing_level)


# ============================================================================
# ВЫБОР ЯЗЫКА
# ============================================================================

@router.callback_query(F.data.startswith("select_lang_"))
async def select_language(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    """
    Шаг 1: язык интерфейса. Он же язык, на котором показываются значения.

    Такова договорённость владельца дословно: «в первом меню выбор языка
    интерфейса — значит на этот язык учим». Читать бота и читать переводы на
    разных языках человеку незачем, поэтому отдельного вопроса про язык
    значения нет: он равен интерфейсу и меняется вместе с ним.

    Дальше — НЕ уровень, а выбор изучаемого языка: уровень без языка
    бессмыслен, A1 немецкого и A1 английского это разные словари.
    """
    lang = callback.data.removeprefix("select_lang_")
    if lang not in INTERFACE_LANGS:
        await callback.answer("❌ Error", show_alert=True)
        return

    user = await session.get(User, callback.from_user.id)
    user.interface_language = lang
    user.native_lang = lang
    user.reverse_mode = False

    await session.commit()

    await callback.message.edit_text(
        f"{get_text('onboarding_learning_title', lang)}\n\n"
        f"{get_text('onboarding_learning_desc', lang, native=get_text(f'langname_{lang}', lang))}",
        reply_markup=get_learning_keyboard(lang, lang),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("onboard_learn_"))
async def onboard_learning_language(callback: CallbackQuery, state: FSMContext,
                                    session: AsyncSession):
    """
    Шаг 2: какой язык учить. Прежде этого шага не было, и всем молча ставился
    немецкий.
    """
    code = callback.data.removeprefix("onboard_learn_")

    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or DEFAULT_LOCALE

    if not is_learnable(code) or code == user.native_lang:
        await callback.answer("❌ Error", show_alert=True)
        return

    user.learning_lang = code
    # Страховка на случай, если язык значения всё же совпал: вопрос выродился
    # бы в «слово = слово»
    if user.native_lang == code:
        user.native_lang = fallback_native_for(code, preferred=lang)
    user.translation_mode = legacy_mode_name(pair_from_user(user))

    await session.commit()

    first_name = callback.from_user.first_name or get_text("friend_fallback", lang)
    languages = learnable_names(lang)
    # Считаем ДО вызова: test_format_parameters_match разбирает get_text
    # регулярным выражением, и вложенный вызов внутри аргумента рвёт разбор
    learning_name = get_text(f"langname_{code}", lang)

    welcome_text = (
        f"{get_text('welcome_title', lang, name=first_name)}\n\n"
        f"{get_text('welcome_description', lang, languages=languages)}\n\n"
        f"{get_text('welcome_separator', lang)}\n"
        f"{get_text('welcome_learn_words_title', lang)}\n"
        f"{get_text('welcome_learn_words_desc', lang)}\n\n"
        f"{get_text('welcome_stats_title', lang)}\n"
        f"{get_text('welcome_stats_desc', lang)}\n\n"
        f"{get_text('welcome_settings_title', lang)}\n"
        f"{get_text('welcome_settings_desc', lang)}\n\n"
        f"{get_text('welcome_help_title', lang)}\n"
        f"{get_text('welcome_help_desc', lang)}\n"
        f"{get_text('welcome_separator', lang)}\n\n"
        f"{get_text('welcome_choose_level', lang, language=learning_name)}"
    )

    await callback.message.edit_text(welcome_text, reply_markup=get_level_keyboard(lang))

    await state.set_state(QuizStates.choosing_level)
    await callback.answer()


# ============================================================================
# ВЫБОР УРОВНЯ (при /start для новых юзеров)
# ============================================================================

@router.callback_query(F.data.startswith("start_level_"))
async def select_level(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    """Обработчик выбора уровня при первом старте"""
    level_str = callback.data.replace("start_level_", "")

    user_id = callback.from_user.id
    user = await session.get(User, user_id)

    user.level = CEFRLevel(level_str)
    user.quiz_mode = QuizMode.LEVEL
    await session.commit()

    lang = user.interface_language or DEFAULT_LOCALE

    await callback.message.delete()

    old_anchor_id, new_anchor_id = await ensure_anchor(callback.message, session, user, emoji="🤖")

    if old_anchor_id:
        current_msg_id = callback.message.message_id
        await delete_messages_fast(callback.bot, callback.message.chat.id, old_anchor_id, current_msg_id)

    await callback.bot.send_message(
        chat_id=callback.message.chat.id,
        text=get_text("level_selected", lang, level=level_str)
    )

    await state.clear()
    await callback.answer()