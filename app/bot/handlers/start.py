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


def _learning_question_text(user: User, lang: str) -> str:
    """
    Второй вопрос знакомства: какой язык учить.

    Один текст на два входа — сразу после выбора языка бота и при /start
    того, кто на этом вопросе прервался. Две копии разошлись бы.
    """
    native = user.native_lang or lang
    return (
        f"{get_text('onboarding_learning_title', lang)}\n\n"
        f"{get_text('onboarding_learning_desc', lang, native=get_text(f'langname_{native}', lang))}"
    )


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

    if not await _learning_language_unanswered(session, user):
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
        # `/START` ПОКАЗЫВАЕТ ВСТУПЛЕНИЕ ВСЕМ — и новичку, и играющему.
        #
        # Здесь было две неудачные попытки сделать иначе, и обе владелец
        # отверг. Сперва играющего вело на домашний экран со шкалами —
        # «что-то ты не то сделал, теперь при /start вызывает статистику».
        # Потом — короткая строка «С возвращением» с одной кнопкой; на это
        # ответ был прямой: «СТОП, прошлый старт был ПРАВИЛЬНЫМ, не
        # правильной была статистика. Верни старт!»
        #
        # Значит разделения по числу кругов нет. Экран, который он назвал
        # правильным, — это вступление: приветствие, чем бот занимается,
        # сколько в нём всего, что где лежит, и кнопка начать. Набирают
        # `/start` руками и редко; увидеть на него осмысленный экран лучше,
        # чем экран, который где-то уже есть.
        await _show_intro(message, session, user, lang)
    else:
        # ЗНАКОМСТВО ПРЕРВАНО НА ВТОРОМ ВОПРОСЕ: язык бота выбран, а какой
        # язык учить — нет. Задаём его снова.
        #
        # Прежде эта ветка ловила «нет уровня», а уровень у колонки по
        # умолчанию A1 — то есть ветка была мёртвой, вопрос пропускался, и
        # человек учил немецкий по умолчанию колонки —
        # ровно та беда «233 из 233 учат немецкий», против которой второй
        # вопрос и заводился. Немцу выходило хуже всех: учить немецкий со
        # значениями на запасном языке. Воспроизведено аудитом 14 октября.
        #
        # Состояние `choosing_level` больше не ставится: обработчиков у него
        # нет ни одного, и висело оно впустую.
        await message.answer(
            _learning_question_text(user, lang),
            reply_markup=get_learning_keyboard(user.native_lang or lang, lang),
        )


async def _learning_language_unanswered(session: AsyncSession, user: User) -> bool:
    """
    Не ответил ли человек на второй вопрос знакомства — какой язык учить.

    Отдельной колонки «знакомство пройдено» нет, а изучаемый язык и уровень
    имеют значения по умолчанию (`de`, A1) — по ним не отличить ответившего
    от прервавшегося. Отличает ЯКОРЬ: первый раз он создаётся вступлением,
    которое показывается только после ответа, а нижнего меню, через которое
    якорь мог бы появиться раньше, у прервавшегося ещё нет.

    Кругов при этом тоже не должно быть ни одного: человек из давних
    времён, у которого якоря почему-то нет, но занятия есть, знакомство
    прошёл, и переспрашивать его — значит сбросить ему уровень на A1.
    """
    if user.anchor_message_id is not None:
        return False
    from sqlalchemy import func, select

    from app.database.models import QuizSession

    played = await session.scalar(
        select(func.count()).select_from(QuizSession).where(QuizSession.user_id == user.id)
    )
    return not played


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
        await callback.answer("Error", show_alert=True)
        return

    user = await session.get(User, callback.from_user.id)
    if user is None:
        # Старый экран выбора языка у человека, которого в базе уже нет:
        # завести заново, как это сделал бы /start, а не упасть на None
        user = User(
            id=callback.from_user.id,
            username=callback.from_user.username,
            first_name=callback.from_user.first_name,
        )
        session.add(user)
    user.interface_language = lang
    user.native_lang = lang
    user.reverse_mode = False

    await session.commit()

    await callback.message.edit_text(
        _learning_question_text(user, lang),
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
        await callback.answer("Error", show_alert=True)
        return

    user.learning_lang = code
    # Страховка на случай, если язык значения всё же совпал: вопрос выродился
    # бы в «слово = слово»
    if user.native_lang == code:
        user.native_lang = fallback_native_for(code, preferred=lang)
    user.translation_mode = legacy_mode_name(pair_from_user(user))

    await session.commit()

    # УРОВЕНЬ НЕ СПРАШИВАЕТСЯ. Начинаем с A1, а поднимает его бот — сам, по
    # точности последних ответов (`level_service`). Это и есть его работа:
    # своего уровня по CEFR человек обычно не знает, а ошибка в нём портит
    # всё занятие. Кому нужно жёстче — уровень есть в настройках.
    user.level = CEFRLevel.A1
    user.quiz_mode = QuizMode.LEVEL
    await session.commit()

    await state.clear()
    await callback.answer()

    # Знакомство кончается ОДНОЙ КНОПКОЙ, которая начинает круг. Прежде
    # здесь были ещё два экрана — уровень и цель, — и замер говорит, чего
    # это стоило: 24 человека из 233 прошли знакомство и не начали ни
    # одного круга.
    try:
        await callback.message.delete()
    except Exception:
        logger.debug("не удалось убрать экран выбора языка", exc_info=True)

    await _show_intro(callback.message, session, user, lang)


# ============================================================================
# ВЫБОР УРОВНЯ (при /start для новых юзеров)
# ============================================================================


def _menu_map(lang: str) -> str:
    """
    «Что где» — из САМИХ подписей меню, а не пересказом.

    Владелец просил на этом экране «что где находится в боте коротко». Беда
    такого раздела известна: прежний был выписан руками и обещал «Помощь»
    среди кнопок меню, откуда она уехала в настройки. Текст про интерфейс,
    живущий отдельно от интерфейса, расходится с ним молча.

    Поэтому подпись каждой строки берётся тем же ключом, каким кнопка
    рисуется на клавиатуре, а в локали лежит только короткое пояснение.
    Пропадёт кнопка из меню — пропадёт и строка.
    """
    from app.bot.buttons import (
        BTN_LEARN_WORDS, BTN_RATING, BTN_SETTINGS, BTN_STATS,
    )

    rows = (
        (BTN_LEARN_WORDS, "intro_menu_learn"),
        (BTN_RATING, "intro_menu_rating"),
        (BTN_STATS, "intro_menu_stats"),
        (BTN_SETTINGS, "intro_menu_settings"),
    )
    lines = [
        f"<b>{get_text(button, lang)}</b> — {get_text(about, lang)}"
        for button, about in rows
    ]
    return get_text("intro_menu_title", lang) + "\n" + "\n".join(lines)


async def _show_intro(
    message: Message, session: AsyncSession, user: User, lang: str
) -> None:
    """
    Первый внятный экран новичка: привет, что умеет бот, что где и кнопка.

    ЧЕЙ ЭТО ЭКРАН. Владельца дословно: «Старт — это первое внятное меню
    после выбора языка для новика», и отдельно: «тот кто давно играет ему
    это меню попросту не нужно». Это решение потом пересмотрено им же
    («СТОП, прошлый старт был ПРАВИЛЬНЫМ… Верни старт!»), и теперь
    вступление видят ВСЕ, кто набрал /start, — подробно в `cmd_start`.
    Прежняя строка здесь говорила обратное коду.

    Строк ровно четыре: приветствие, три способа, сколько тут всего и что
    где. Кнопка одна — начать.
    """
    first_name = message.chat.first_name or get_text("friend_fallback", lang)

    text = (
        f"{get_text('welcome_title', lang, name=first_name)}\n\n"
        f"{get_text('intro_games', lang)}\n\n"
        f"{get_text('intro_numbers', lang)}\n\n"
        f"{_menu_map(lang)}"
    )

    old_anchor_id, _ = await ensure_anchor(message, session, user, emoji="")
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
    ОДНА КНОПКА. Замечание владельца об этом экране дословно: «Там 4
    кнопки. Нахуя они? Любую тыкаешь — начинаешь игру. И не ясно
    выбралось что-то отдельное или нет».

    Прежде их было три, и две из них вели туда, куда ведёт нижняя
    клавиатура: «Прогресс» и «Настройки» стоят на ней всегда. Экран, где
    половина кнопок дублирует меню, читается как список непонятных
    вариантов — а у этого экрана работа ровно одна: начать.
    """
    from app.bot.handlers.quiz.lesson_state import lesson_length

    count = lesson_length(user)
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text=get_text("home_btn_learn", lang, count=count),
            # Из вступительного блока /start
            callback_data="learn_now:start",
        )
    ]])



