"""
Обработчик команды /start и выбор языка
"""

from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

import html
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
    is_learnable,
    legacy_mode_name,
    pair_from_user,
)

router = Router()


# «НАЗАД» СТРЕЛКОЙ на экранах выбора языка (владелец, 17.10): кто ткнул не
# тот язык, слова «Geri» или «Zpět» не прочтёт, а стрелку поймёт любой
BACK_ARROW = "←"


def _grid(buttons: list[InlineKeyboardButton], per_row: int = 2) -> list[list[InlineKeyboardButton]]:
    return [buttons[i:i + per_row] for i in range(0, len(buttons), per_row)]


def _grid_with_back(buttons: list[InlineKeyboardButton],
                    back: InlineKeyboardButton) -> list[list[InlineKeyboardButton]]:
    """
    Сетка по две и «Назад» СЛЕВА в последнем ряду.

    Исключение из устава (там «Назад» — отдельным рядом внизу), решение
    владельца 16.10: при нечётном числе языков последний ряд и так
    неполный, и «Назад» встаёт в пустую клетку рядом с последним языком.
    При пяти языках выходит три полных ряда, при девяти — пять. При чётном
    числе свободной клетки нет, и «Назад» уходит отдельным рядом.
    """
    rows = _grid(buttons)
    if rows and len(rows[-1]) == 1:
        rows[-1] = [back, rows[-1][0]]
    else:
        rows.append([back])
    return rows


# ============================================================================
# ЭКРАН 1: ВЫБОР СВОЕГО ЯЗЫКА
# ============================================================================

# Пометки «откуда пришёл» в нажатиях смены языка: команда /language или
# настройки. От неё зависят «Назад» и «Готово»
ORIGIN_COMMAND = "c"
ORIGIN_SETTINGS = "s"


def get_language_selection_keyboard(
    prefix: str = "select_lang_", suffix: str = "", current: str | None = None,
    back: str | None = None,
) -> InlineKeyboardMarkup:
    """
    Выбор своего языка — и при первом запуске, и по /language, и из настроек.

    ОДИН ЭКРАН НА ТРИ ВХОДА. Прежде смена языка в настройках была своим
    экраном с подписями на нынешнем языке человека — а менять язык как раз
    приходит тот, кто его НЕ понимает (живой случай 16.10: выбрал не тот и
    не смог найти, где сменить). Поэтому везде экран первого запуска:
    подписи на самих языках.

    Порядок — из INTERFACE_LANGS, надпись — из САМОЙ локали языка: человек,
    не знающий ни одного из остальных, должен узнать свой.
    """
    buttons = [
        InlineKeyboardButton(
            text=("✓ " if code == current else "") + LOCALES[code].get(f"lang_{code}", code),
            callback_data=f"{prefix}{code}{suffix}",
        )
        for code in INTERFACE_LANGS
    ]
    rows = _grid(buttons)
    if back:
        rows.append([InlineKeyboardButton(
            text=BACK_ARROW, callback_data=back,
        )])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def _language_selection_text() -> str:
    """
    Самый первый экран: человек ещё не выбрал язык, значит понять его нельзя.

    Поэтому призыв написан на ВСЕХ языках сразу — единственный экран, где
    многоязычие по делу. ПО СТРОКЕ НА ЯЗЫК (решение владельца 16.10).
    Прежде шесть призывов были сжаты в две строки через «·», и человек
    искал своё в сплошном ряду чужих слов; теперь каждый читает свою строку.
    Приветствия нет: оно было бы на чужом языке у девяти из десяти.

    Порядок строк — тот же, что у кнопок (INTERFACE_LANGS).
    """
    lines = "\n".join(LOCALES[code]["start_pick_language"] for code in INTERFACE_LANGS)
    return f"<b>{BOT_NAME}</b>\n\n{lines}"


# ============================================================================
# ЭКРАН 2: ЧТО УЧИТЬ
# ============================================================================

def phone_language(from_user) -> str | None:
    """
    Язык телефона по Telegram — часть кода до дефиса («pt-br» → «pt»).

    Поля может не быть вовсе: Telegram передаёт его не всегда.
    """
    code = getattr(from_user, "language_code", None)
    if not code:
        return None
    return code.split("-", 1)[0].lower() or None


def phone_hint(phone: str | None, chosen: str) -> str:
    """
    Строка на языке ТЕЛЕФОНА, если он не совпал с выбранным.

    Защита от промаха (решение владельца 16.10): человек ткнул не в ту
    кнопку и видит экран на незнакомом языке. Сказать ему это можно только
    на его языке — а его знает телефон. Нет поля, язык не наш, совпал —
    строки нет. «Назад» в ней назван так, как подписана кнопка: стрелкой.
    """
    if not phone or phone == chosen or phone not in INTERFACE_LANGS:
        return ""
    return get_text("onboard_phone_hint", phone, back=BACK_ARROW)


def learning_screen_text(chosen: str, phone: str | None = None) -> str:
    """
    Экран 2: подтверждение своего языка и вопрос, что учить.

    «✓ Ваш язык» наверху — подтверждение первого нажатия (устав:
    подтверждение начинается с ✓). Под ним — где сменить: команда
    /language. Прежде строка звала «в настройки», где смена лежала на
    третьем уровне вложенности под чужим именем.
    """
    text = (
        f"{get_text('onboard_your_lang', chosen, language=get_text(f'lang_{chosen}', chosen))}\n"
        f"{get_text('onboard_change_hint', chosen)}\n\n"
        f"{get_text('onboarding_learning_title', chosen)}"
    )
    hint = phone_hint(phone, chosen)
    if hint:
        text += f"\n\n<i>{hint}</i>"
    return text


def get_learning_keyboard(native: str, lang: str, *, prefix: str = "onboard_learn_",
                          suffix: str = "", back: str = "onboard_back") -> InlineKeyboardMarkup:
    """
    Выбор ИЗУЧАЕМОГО языка — второй шаг знакомства.

    Прежде этого шага не было вовсе: новому человеку молча ставился немецкий,
    и 233 пользователя из 233 учили немецкий.

    Свой язык из списка убран: учить язык, на котором показывают значения, —
    вырожденная задача «слово = слово».

    ВЫБРАННЫЙ ЯЗЫК БОТА ЕДЕТ В НАЖАТИИ (`:{язык}`), а не в базе. В базу
    знакомство пишется только целиком, вторым нажатием: иначе ушедший с
    этого экрана остаётся с языком бота, которого, возможно, не хотел, и
    /start ему его уже не предложит.
    """
    buttons = [
        InlineKeyboardButton(
            text=get_text(f"langname_{code}", lang),
            callback_data=f"{prefix}{code}{suffix}",
        )
        for code in LEARNABLE_LANGS
        if code != native
    ]
    return InlineKeyboardMarkup(inline_keyboard=_grid_with_back(
        buttons, InlineKeyboardButton(text=BACK_ARROW, callback_data=back),
    ))




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
        # Напоминания — сразу включены, на час захода (16.10): см.
        # `enable_by_default`. Тем, кто в боте уже был, ничего не меняется
        from app.services.reminder_service import enable_by_default

        enable_by_default(user)
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
            learning_screen_text(lang, phone_language(message.from_user)),
            reply_markup=get_learning_keyboard(lang, lang, suffix=f":{lang}"),
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
# ЗНАКОМСТВО: ЯЗЫК БОТА → ЧТО УЧИТЬ
# ============================================================================

def _split_choice(data: str, prefix: str) -> tuple[str, str | None]:
    """`onboard_learn_de:ru` → («de», «ru»); старое `onboard_learn_de` → («de», None)."""
    code, _, rest = data.removeprefix(prefix).partition(":")
    return code, (rest or None)


async def _get_or_create_user(session: AsyncSession, from_user) -> User:
    user = await session.get(User, from_user.id)
    if user is None:
        # Старый экран у человека, которого в базе уже нет: завести заново,
        # как это сделал бы /start, а не упасть на None
        user = User(id=from_user.id, username=from_user.username,
                    first_name=from_user.first_name)
        session.add(user)
    return user


@router.callback_query(F.data.startswith("select_lang_"))
async def select_language(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    """
    Шаг 1: свой язык. Он же язык бота и язык значений.

    Договорённость владельца дословно: «в первом меню выбор языка
    интерфейса — значит на этот язык учим». Отдельного вопроса про язык
    значений нет.

    В БАЗУ НИЧЕГО НЕ ПИШЕТСЯ. Выбор едет дальше в нажатиях экрана 2, а
    записывается вместе с изучаемым языком. Прежде язык ставился первым же
    нажатием, а на экране 2 не было «Назад»: промахнувшийся оставался на
    чужом языке, и /start уже не спрашивал его заново (живой случай 16.10).
    """
    lang = callback.data.removeprefix("select_lang_")
    if lang not in INTERFACE_LANGS:
        await callback.answer("Error", show_alert=True)
        return

    phone = phone_language(callback.from_user)
    from app.services.journal import note

    if await session.get(User, callback.from_user.id) is not None:
        note(session, callback.from_user.id, "onboard", "own_lang",
             chosen=lang, phone=phone, mismatch=bool(phone_hint(phone, lang)) or None)

    await callback.message.edit_text(
        learning_screen_text(lang, phone),
        reply_markup=get_learning_keyboard(lang, lang, suffix=f":{lang}"),
    )
    await callback.answer()


@router.callback_query(F.data == "onboard_back")
async def onboard_back(callback: CallbackQuery, session: AsyncSession):
    """«Назад» с экрана 2 — снова выбор своего языка. В базе менять нечего."""
    from app.services.journal import note

    if await session.get(User, callback.from_user.id) is not None:
        note(session, callback.from_user.id, "onboard", "back",
             phone=phone_language(callback.from_user))
    await callback.message.edit_text(
        _language_selection_text(), reply_markup=get_language_selection_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("onboard_learn_"))
async def onboard_learning_language(callback: CallbackQuery, state: FSMContext,
                                    session: AsyncSession):
    """
    Шаг 2: какой язык учить. Здесь знакомство записывается целиком: язык
    бота (из нажатия) и изучаемый.
    """
    code, chosen = _split_choice(callback.data, "onboard_learn_")

    user = await _get_or_create_user(session, callback.from_user)
    # Старая кнопка без языка в нажатии — язык бота уже лежит в базе
    lang = chosen or user.interface_language or DEFAULT_LOCALE

    if lang not in INTERFACE_LANGS or not is_learnable(code) or code == lang:
        await callback.answer("Error", show_alert=True)
        return

    user.interface_language = lang
    user.native_lang = lang
    user.reverse_mode = False
    user.learning_lang = code
    user.translation_mode = legacy_mode_name(pair_from_user(user))

    # УРОВЕНЬ НЕ СПРАШИВАЕТСЯ. Начинаем с A1, а поднимает его бот — сам, по
    # точности последних ответов (`level_service`). Это и есть его работа:
    # своего уровня по CEFR человек обычно не знает, а ошибка в нём портит
    # всё занятие. Кому нужно жёстче — уровень есть в настройках.
    user.level = CEFRLevel.A1
    user.quiz_mode = QuizMode.LEVEL
    await session.commit()

    from app.services.journal import note

    note(session, user.id, "onboard", "learning", chosen=lang, learning=code,
         phone=phone_language(callback.from_user))

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
# СМЕНА ЯЗЫКА: /language и «Язык бота» в настройках
# ============================================================================
#
# Один путь на оба входа (решение владельца 16.10): экран 1 знакомства →
# подтверждение. Экран 2 — только если новый язык бота совпал с изучаемым:
# учить язык, на котором показывают значения, нельзя, и изучаемый надо
# выбрать заново.
#
# Нажатия: `chlang_{язык}:{откуда}`, `chlearn_{изучаемый}:{язык}:{откуда}`,
# `chdone:{откуда}`. «Откуда» — `c` (команда) или `s` (настройки): от него
# зависят «Назад» и «Готово».

def change_language_screen(user: User | None, origin: str) -> tuple[str, InlineKeyboardMarkup]:
    current = user.interface_language if user else None
    back = "settings_group_bot" if origin == ORIGIN_SETTINGS else None
    return _language_selection_text(), get_language_selection_keyboard(
        prefix="chlang_", suffix=f":{origin}", current=current, back=back,
    )


def _confirm_screen(user: User, origin: str) -> tuple[str, InlineKeyboardMarkup]:
    """
    Подтверждение смены: «✓ Ваш язык», что учите, и что прогресс цел.

    Строка про прогресс — ответ на страх, с которым язык не меняют: учёт
    ведётся по изучаемому языку (слова, занятия, рейтинг месяца), и смена
    языка бота его не трогает.
    """
    from app.services.language_service import language_word

    lang = user.interface_language or DEFAULT_LOCALE
    pair = pair_from_user(user)
    text = (
        f"{get_text('onboard_your_lang', lang, language=get_text(f'lang_{lang}', lang))}\n"
        f"{get_text('lang_confirm_learning', lang, language=language_word(pair.learning, lang))}\n\n"
        f"<i>{get_text('lang_progress_kept', lang)}</i>"
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_text("btn_done", lang), callback_data=f"chdone:{origin}"),
            InlineKeyboardButton(text=get_text("btn_change_learning", lang),
                                 callback_data="settings_learning"),
        ],
    ])
    return text, keyboard


@router.message(Command("language"))
async def cmd_language(message: Message, state: FSMContext, session: AsyncSession):
    """
    /language — смена своего языка с любого места.

    Прежде команды не было, а смена лежала в Настройки → «Бот» → «Язык
    интерфейса»: три нажатия на языке, которого человек, ошибшийся при
    знакомстве, не понимает.
    """
    user = await session.get(User, message.from_user.id)
    try:
        await message.delete()
    except Exception:
        pass
    if user is None or not user.interface_language or user.interface_language == "reset":
        # Знакомства не было — это просто его первый экран
        await cmd_start(message, state, session)
        return
    text, keyboard = change_language_screen(user, ORIGIN_COMMAND)
    await message.answer(text, reply_markup=keyboard)


async def _apply_language(callback: CallbackQuery, session: AsyncSession, user: User,
                          lang: str, origin: str, learning: str | None = None) -> None:
    """Записать язык бота (и изучаемый, если выбран) и показать подтверждение."""
    from app.bot.handlers.quiz.settings import _renew_anchor
    from app.services.journal import note

    before = user.interface_language
    user.interface_language = lang
    if learning:
        user.learning_lang = learning
    # Язык значения следует за языком бота, кроме случая, когда он совпал
    # бы с изучаемым (тогда сюда приходят уже с новым изучаемым)
    if lang != user.learning_lang:
        user.native_lang = lang
    user.translation_mode = legacy_mode_name(pair_from_user(user))
    await session.commit()
    note(session, user.id, "language", "changed", before=before, chosen=lang,
         learning=learning, origin=origin)

    await callback.answer()
    text, keyboard = _confirm_screen(user, origin)
    # Новый язык нужен нижнему меню и строке якоря — якорь пересоздаётся,
    # и подтверждение встаёт под ним
    if await _renew_anchor(callback, session, user):
        try:
            await callback.message.delete()
        except Exception:
            logger.debug("не удалось убрать экран выбора языка", exc_info=True)
        await callback.message.answer(text, reply_markup=keyboard)
        return
    await callback.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(F.data.startswith("chlang_"))
async def change_language(callback: CallbackQuery, session: AsyncSession):
    lang, origin = _split_choice(callback.data, "chlang_")
    origin = origin or ORIGIN_COMMAND
    user = await session.get(User, callback.from_user.id)
    if user is None or lang not in INTERFACE_LANGS:
        await callback.answer("Error", show_alert=True)
        return

    if lang == pair_from_user(user).learning:
        # Язык бота совпал с изучаемым — изучаемый выбирается заново.
        # В базу пока ничего: язык едет в нажатии, как при знакомстве
        await callback.answer()
        await callback.message.edit_text(
            learning_screen_text(lang),
            reply_markup=get_learning_keyboard(
                lang, lang, prefix="chlearn_", suffix=f":{lang}:{origin}",
                back=f"chback:{origin}",
            ),
        )
        return

    await _apply_language(callback, session, user, lang, origin)


@router.callback_query(F.data.startswith("chlearn_"))
async def change_language_learning(callback: CallbackQuery, session: AsyncSession):
    code, _, rest = callback.data.removeprefix("chlearn_").partition(":")
    lang, _, origin = rest.partition(":")
    user = await session.get(User, callback.from_user.id)
    if (user is None or lang not in INTERFACE_LANGS
            or not is_learnable(code) or code == lang):
        await callback.answer("Error", show_alert=True)
        return
    await _apply_language(callback, session, user, lang, origin or ORIGIN_COMMAND, learning=code)


@router.callback_query(F.data.startswith("chback:"))
async def change_language_back(callback: CallbackQuery, session: AsyncSession):
    origin = callback.data.partition(":")[2] or ORIGIN_COMMAND
    user = await session.get(User, callback.from_user.id)
    text, keyboard = change_language_screen(user, origin)
    await callback.answer()
    await callback.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(F.data.startswith("chdone:"))
async def change_language_done(callback: CallbackQuery, session: AsyncSession):
    """«Готово»: из настроек — назад в настройки, после команды — убрать экран."""
    await callback.answer()
    if callback.data.partition(":")[2] == ORIGIN_SETTINGS:
        from app.bot.handlers.quiz.settings import show_settings_callback

        await show_settings_callback(callback, session)
        return
    try:
        await callback.message.delete()
    except Exception:
        logger.debug("не удалось убрать подтверждение", exc_info=True)


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
    # Команда — не кнопка, но и ей место здесь: смена языка нужна как раз
    # тому, кто промахнулся, и искать её в настройках он не станет
    lines.append(f"<b>/language</b> — {get_text('intro_menu_language', lang)}")
    return get_text("intro_menu_title", lang) + "\n" + "\n".join(lines)


def intro_pair_line(user: User, lang: str) -> str:
    """
    «Вы учите немецкий с переводом на русский» — пара словами, под
    приветствием (решение владельца 16.10).

    Человек, промахнувшийся языком, узнаёт об этом здесь, до первого
    вопроса, а не по переводам на чужом языке. Формы названий — из таблицы
    `language_forms`: «вивчаєте німецьку з перекладом українською»
    склонением кода не собрать.
    """
    from app.locales.language_forms import language_form

    pair = pair_from_user(user)
    return get_text(
        "intro_pair", lang,
        learning=language_form(lang, "learn", pair.learning),
        native=language_form(lang, "into", pair.native),
    )


def intro_numbers(lang: str) -> str:
    """Числа бота; число языков — из списка открытых, а не словом в локали."""
    from app.locales import plural
    from app.services.language_service import learnable_count

    return get_text("intro_numbers", lang,
                    languages=plural(learnable_count(), "plural_languages", lang))


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
    # Экранируется: имя идёт в HTML (аудит 2.1, «Tom <3»)
    first_name = html.escape(message.chat.first_name or get_text("friend_fallback", lang))

    text = (
        f"{get_text('welcome_title', lang, name=first_name)}\n"
        f"{intro_pair_line(user, lang)}\n\n"
        f"{get_text('intro_games', lang)}\n\n"
        f"{intro_numbers(lang)}\n\n"
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



