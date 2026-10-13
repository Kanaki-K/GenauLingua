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
from app.bot.utils import BOT_NAME, delete_messages_fast, ensure_anchor
from app.database.enums import CEFRLevel, QuizMode
from app.database.models import User
from app.locales import DEFAULT_LOCALE, LOCALES, get_text
from app.services.goal_service import GOAL_ORDER, is_goal
from app.services.language_service import (
    INTERFACE_LANGS,
    LEARNABLE_LANGS,
    fallback_native_for,
    is_learnable,
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

    Поэтому призыв написан на ВСЕХ шести сразу — это единственный экран,
    где многоязычие по делу. Прежде здесь стоял флаг 🇩🇪 и четыре строки:
    флаг обещал немецкий, которого бот больше не обещает, а четырёх строк
    не хватало на шесть кнопок.

    ШЕСТЬ ПРИЗЫВОВ СЖАТЫ В ДВЕ СТРОКИ. Шестью отдельными строками они
    занимали полэкрана, и читать их все незачем: человек ищет своё слово в
    списке кнопок, а не в абзаце. Название языка перед призывом тоже ушло —
    оно дублировало кнопку, а после снятия флагов строки стали читаться как
    «Українська Обери мову інтерфейсу бота:», будто это одно предложение.

    Призыв берётся коротким: у `settings_language_description` в каждой
    локали длинная форма («Выбери язык интерфейса бота:»), а в две строки
    влезает только существо.
    """
    prompts = [LOCALES[code]["start_pick_language"] for code in INTERFACE_LANGS]
    half = (len(prompts) + 1) // 2
    lines = "\n".join([
        " · ".join(prompts[:half]),
        " · ".join(prompts[half:]),
    ])
    return f"<b>{BOT_NAME}</b>\n\n{lines}"


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

    if user.level:
        # `/START` — ЭТО ВСТУПИТЕЛЬНЫЙ БЛОК, И БОЛЬШЕ НИЧЕГО.
        #
        # Замечание владельца: сюда возвращаются только набрав команду
        # руками, то есть осознанно, — и обычно затем, чтобы понять, что это
        # за бот и что он теперь умеет. Значит здесь не место ни шкалам (они
        # на кнопке «Прогресс», куда приходят постоянно), ни пересказу меню.
        #
        # Пересказ как раз и стоял здесь прежде: восемь строк «📚 Учить
        # слова — запуск викторины», «📊 Статистика — твой прогресс» и так
        # далее. Две беды сразу. Первая: он описывал кнопки, которые человек
        # видит перед собой на клавиатуре. Вторая хуже — он ВРАЛ, обещая
        # «❓ Помощь» среди кнопок меню, откуда она давно уехала в настройки.
        #
        # Что здесь нужно вместо этого: чем бот стал (три навыка, а не один),
        # сколько в нём всего, где человек сейчас — и кнопка.
        await _show_intro(message, session, user, lang)
    else:
        # Уровень называет язык, к которому относится: A1 немецкого и A1
        # английского — разные словари, и без названия вопрос неполон
        learning_name = get_text(f"langname_{pair_from_user(user).learning}", lang)

        # Текст тот же, что и на втором шаге онбординга: человек попал сюда,
        # не досидев до выбора уровня, и рассказать ему надо ровно то же
        await message.answer(
            f"{get_text('welcome_title', lang, name=first_name)}\n\n"
            f"{get_text('intro_three_games', lang)}\n\n"
            f"{get_text('intro_numbers', lang)}\n\n"
            f"{get_text('welcome_choose_level', lang, language=learning_name)}",
            reply_markup=get_level_keyboard(lang),
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
    # Считаем ДО вызова: test_format_parameters_match разбирает get_text
    # регулярным выражением, и вложенный вызов внутри аргумента рвёт разбор
    learning_name = get_text(f"langname_{code}", lang)

    # ТОТ ЖЕ ТЕКСТ, ЧТО И ВО ВСТУПИТЕЛЬНОМ БЛОКЕ, а не пересказ меню.
    #
    # Здесь стояли те же восемь строк про кнопки — и с той же ложью:
    # «❓ Помощь» обещалась среди пунктов меню, откуда она уехала в
    # настройки. Новому человеку тем более нельзя обещать кнопку, которой
    # он не найдёт: это первое, что он о боте узнает.
    #
    # А рассказать ему надо ровно то же, что и вернувшемуся: что слово —
    # это три навыка, и сколько тут всего. Один текст на два места,
    # разойтись им теперь нечем.
    welcome_text = (
        f"{get_text('welcome_title', lang, name=first_name)}\n\n"
        f"{get_text('intro_three_games', lang)}\n\n"
        f"{get_text('intro_numbers', lang)}\n\n"
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

    # КНОПКИ, А НЕ ТЕКСТ «НАЖМИ КНОПКУ».
    #
    # Здесь кончается онбординг, и прежде он кончался тупиком: бот писал
    # «✅ Уровень B1 выбран. 📚 Нажми «Учить слова» — и начнём!» и не давал
    # ничего нажать. Текст ОБЪЯСНЯЛ, что сделать, вместо того чтобы дать
    # сделать — а это самый дорогой экран во всём боте: дальше либо первый
    # круг, либо уход навсегда.
    #
    # Замер говорит, чего это стоило: 24 человека из 233 прошли онбординг и
    # не начали НИ ОДНОГО круга, а ещё 220 кругов закрыты без единого
    # ответа. Разбор — MENU_CONCEPT.md §3.4.
    #
    # ВОПРОС «ЗАЧЕМ УЧИШЬ» ВСТРОЕН В ЭТО ЖЕ НАЖАТИЕ, А НЕ ДОБАВЛЕН ШАГОМ.
    # Каждая из пяти кнопок И отвечает на вопрос, И начинает первый круг —
    # то есть онбординг не стал длиннее ни на одно действие. Отдельным
    # экраном спрашивать было нельзя: лишний шаг здесь стоит людей, а
    # замеренная цена выбора в этом проекте известна — 223 человека из 233
    # не меняли ни одной настройки.
    await callback.bot.send_message(
        chat_id=callback.message.chat.id,
        text=(
            f"{get_text('level_selected', lang, level=level_str)}\n\n"
            f"{get_text('goal_question', lang)}"
        ),
        reply_markup=get_goal_keyboard(lang),
    )

    await state.clear()
    await callback.answer()


async def _show_intro(
    message: Message, session: AsyncSession, user: User, lang: str
) -> None:
    """
    Вступительный блок: что это за бот, где человек сейчас, и кнопка.

    Три игры названы ПЕРВЫМИ и не случайно: это главное, что в боте
    изменилось, и единственное, чего о нём нельзя догадаться по кнопкам.
    «Шесть языков в любой паре» — второе такое же: человек, пришедший за
    немецким, не знает, что может учить польский на английском.
    """
    pair = pair_from_user(user)
    learning_name = get_text(f"langname_{pair.learning}", lang)
    # Считаем ДО вызова: test_format_parameters_match разбирает get_text
    # регулярным выражением, и вложенный вызов внутри аргумента рвёт разбор
    mode = _mode_title(user, lang)

    text = (
        f"{get_text('intro_title', lang)}\n\n"
        f"{get_text('intro_three_games', lang)}\n\n"
        f"{get_text('intro_numbers', lang)}\n\n"
        f"{get_text('intro_where_you_are', lang, language=learning_name, mode=mode)}"
    )

    old_anchor_id, _ = await ensure_anchor(message, session, user, emoji="🤖")
    if old_anchor_id:
        await delete_messages_fast(
            message.bot, message.chat.id, old_anchor_id, message.message_id
        )

    await message.answer(text, reply_markup=_intro_keyboard(user, lang))


def _mode_title(user: User, lang: str) -> str:
    """Название режима — то же, что на домашнем экране и в настройках."""
    from app.bot.handlers.quiz.stats import _get_mode_title

    return _get_mode_title(user, lang)


def _intro_keyboard(user: User, lang: str) -> InlineKeyboardMarkup:
    """
    Занятие, прогресс, настройки — и всё.

    Три кнопки вместо пересказа четырёх: заниматься человек пойдёт отсюда,
    а остальное у него на клавиатуре. Рейтинг не дублируется нарочно — он
    кнопкой меню, и вторая дверь в том же боте только путает (решение
    владельца дословно: «зачем-то рейтинг отдельная кнопка и в статистике
    тоже — бред»).
    """
    from app.bot.handlers.quiz.game import DEFAULT_QUIZ_LENGTH

    count = user.quiz_word_count or DEFAULT_QUIZ_LENGTH
    rows = [
        [InlineKeyboardButton(
            text=get_text("home_btn_learn", lang, count=count),
            # Из вступительного блока /start
            callback_data="learn_now:start",
        )],
        [
            InlineKeyboardButton(
                text=get_text("intro_btn_progress", lang), callback_data="home_back"
            ),
            InlineKeyboardButton(
                text=get_text("settings_title_short", lang),
                callback_data="settings_open",
            ),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_goal_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Пять целей, и каждая сразу начинает круг."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=get_text(f"goal_{code}", lang), callback_data=f"goal_{code}"
        )]
        for code in GOAL_ORDER
    ])


@router.callback_query(F.data.startswith("goal_"))
async def choose_goal(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    """
    Запомнить цель и сразу начать занятие.

    Цель не переключает режим викторины — она подмешивает свои категории в
    НОВЫЕ слова, оставляя трудность за уровнем. Почему именно так, разобрано
    в `goal_service`: режим «по категории» не смотрит на уровень вовсе, и
    новичок получал бы C1 вперемешку с A1.
    """
    from app.bot.handlers.quiz.game import start_lesson

    code = callback.data.removeprefix("goal_")
    if not is_goal(code):
        await callback.answer("❌ Error", show_alert=True)
        return

    user = await session.get(User, callback.from_user.id)
    if not user:
        await callback.answer("❌ Error", show_alert=True)
        return

    user.learning_goal = code
    await session.commit()

    await callback.answer()
    await start_lesson(callback.message, state, session)