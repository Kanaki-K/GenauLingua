"""
Репорт ошибок перевода

Flow:
1. Нажал «📝 Помилка перекладу» → список слов викторины (только кнопки, текст не трогаем)
2. Выбрал слова (✅ галочки) → кнопка «Підтвердити (N)»
3. Підтвердити → «Відправити» + «Назад»
4. Відправити → сохраняет в БД, alert, возврат кнопок результата

Защита:
- UNIQUE(user_id, word_id) — одно слово репортится один раз
- Лимит 20 репортов в сутки
- Уже зарепорченные слова показываются с ✓ (некликабельные)
"""

import logging
from datetime import datetime
from app.core.clock import utcnow

from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.database.models import MonthlyStats, User, Word, TranslationReport
from app.locales import DEFAULT_LOCALE, get_text, plural
from app.services.audio_service import voice_for_user
from app.services.language_service import LanguagePair, display_text, pair_from_user

logger = logging.getLogger(__name__)

router = Router()

WORDS_PER_PAGE = 10
DAILY_REPORT_LIMIT = 20

# Сколько баллов ОБЕЩАТЬ за подтверждённую жалобу. Читается из того же
# места, откуда их начисляет админ-панель, — иначе обещание и начисление
# разойдутся, а врёт в этой паре всегда обещание.
REPORT_REWARD_POINTS = MonthlyStats.POINTS_PER_REPORT


# ============================================================================
# ХЕЛПЕРЫ
# ============================================================================

def _get_word_label(word: Word, pair: LanguagePair) -> str:
    """Сформировать label для слова: der Tisch — Стіл"""
    return f"{display_text(word, pair.learning)} — {display_text(word, pair.native)}"


async def report_pair(session: AsyncSession, user: User, quiz_session_id):
    """Пара жалобы: из занятия, где ошибку видели; нет занятия — нынешняя."""
    from app.database.models import QuizSession
    from app.services.language_service import LanguagePair

    if quiz_session_id:
        quiz = await session.get(QuizSession, quiz_session_id)
        if quiz is not None and quiz.learning_lang and quiz.native_lang:
            return LanguagePair(learning=quiz.learning_lang, native=quiz.native_lang,
                                reverse=False)
    return pair_from_user(user)


async def _get_already_reported_ids(
    user_id: int, session: AsyncSession, *, audio_enabled: bool = False, pair=None,
) -> set[int]:
    """
    Слова, по которым человеку больше нечего сказать.

    Видов жалобы два — на перевод и на произношение, — и закрытым слово
    становится, когда исчерпаны оба. Иначе, пожаловавшись на текст, человек
    потерял бы возможность пожаловаться на озвучку того же слова: оно
    показывалось бы галочкой и не нажималось.

    Когда озвучка выключена, второго вида для человека не существует, и
    хватает жалобы на текст.
    """
    result = await session.execute(
        select(TranslationReport.word_id, TranslationReport.kind)
        .where(TranslationReport.user_id == user_id,
               # В ЭТОЙ ПАРЕ: жалоба на русский перевод не закрывает чешский
               *(() if pair is None else (
                   TranslationReport.learning_lang == pair.learning,
                   TranslationReport.native_lang == pair.native,
               )))
    )

    kinds_by_word: dict[int, set[str]] = {}
    for word_id, kind in result.all():
        kinds_by_word.setdefault(word_id, set()).add(kind or "text")

    needed = {"text", "audio"} if audio_enabled else {"text"}
    return {
        word_id for word_id, kinds in kinds_by_word.items()
        if needed <= kinds
    }


async def _get_today_report_count(user_id: int, session: AsyncSession) -> int:
    """Количество репортов юзера за сегодня"""
    today_start = utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    result = await session.execute(
        select(func.count())
        .select_from(TranslationReport)
        .where(
            TranslationReport.user_id == user_id,
            TranslationReport.created_at >= today_start
        )
    )
    return result.scalar() or 0


def _build_word_list_keyboard(
    word_labels: dict,
    selected: list[int],
    already_reported: set[int],
    page: int,
    lang: str,
) -> InlineKeyboardMarkup:
    """Клавиатура со списком слов + пагинация + кнопки"""
    word_ids = list(word_labels.keys())
    total_pages = max(1, (len(word_ids) + WORDS_PER_PAGE - 1) // WORDS_PER_PAGE)
    page = min(page, total_pages - 1)

    start = page * WORDS_PER_PAGE
    end = start + WORDS_PER_PAGE
    page_words = word_ids[start:end]

    buttons = []
    for wid in page_words:
        label = word_labels[wid]

        if wid in already_reported:
            # Уже отправлено — показываем ✔️, клик → alert
            display = f"✓ {label}"
            if len(display) > 50:
                display = display[:47] + "…"
            buttons.append([InlineKeyboardButton(
                text=display,
                callback_data=f"report_already_{wid}"
            )])
        else:
            # Можно выбрать
            check = "✓ " if wid in selected else ""
            display = f"{check}{label}"
            if len(display) > 50:
                display = display[:47] + "…"
            buttons.append([InlineKeyboardButton(
                text=display,
                callback_data=f"report_toggle_{wid}"
            )])

    # Пагинация
    if total_pages > 1:
        nav_row = []
        if page > 0:
            nav_row.append(InlineKeyboardButton(text="<", callback_data=f"report_page_{page - 1}"))
        nav_row.append(InlineKeyboardButton(text=f"{page + 1}/{total_pages}", callback_data="noop"))
        if page < total_pages - 1:
            nav_row.append(InlineKeyboardButton(text=">", callback_data=f"report_page_{page + 1}"))
        buttons.append(nav_row)

    # Кнопка подтверждения (если выбрано ≥1)
    if selected:
        buttons.append([InlineKeyboardButton(
            text=get_text("report_btn_confirm", lang, count=len(selected)),
            callback_data="report_confirm"
        )])

    # Назад
    buttons.append([InlineKeyboardButton(
        text=get_text("btn_back", lang),
        callback_data="report_cancel"
    )])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def _build_confirm_keyboard(lang: str, *, audio_available: bool) -> InlineKeyboardMarkup:
    """
    Что именно не так: текст или озвучка.

    С появлением озвучки жалоба перестала быть однозначной — перевод может
    быть верным, а произношение нет. Разделение не формальное: живые люди
    ловят ровно то, чего не ловит машинная проверка озвучки, — ударение и
    слова с двумя чтениями.

    Когда озвучка выключена или её на слове нет, выбор не показывается:
    спрашивать про звук, которого человек не слышал, бессмысленно. Тогда
    экран остаётся прежним — «Отправить» и «Назад».
    """
    if not audio_available:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text=get_text("report_btn_send", lang),
                callback_data="report_send"
            )],
            [InlineKeyboardButton(
                text=get_text("btn_back", lang),
                callback_data="report_back_to_select"
            )]
        ])

    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=get_text("report_btn_kind_text", lang),
            callback_data="report_send_text"
        )],
        [InlineKeyboardButton(
            text=get_text("report_btn_kind_audio", lang),
            callback_data="report_send_audio"
        )],
        [InlineKeyboardButton(
            text=get_text("btn_back", lang),
            callback_data="report_back_to_select"
        )]
    ])


def _get_results_keyboard_lazy(has_errors: bool, lang: str) -> InlineKeyboardMarkup:
    """
    Вернуть кнопки итога круга — ТЕ ЖЕ, что рисует сам итог.

    Здесь жила своя копия клавиатуры, и она отстала дважды: в ней не было
    «Ещё круг» (главной кнопки итога, ради петли возврата) и пометки
    `:result`, по которой «Назад» с экрана уровня ведёт домой, а не в
    настройки. Человек, открывший и закрывший жалобу, терял и то и другое
    — аудит 14 октября. Копии больше нет: источник один, `summary.py`.

    Импорт внутри функции: `summary` сам тянет модули настроек, и на уровне
    модуля это грозит циклом.
    """
    from app.bot.handlers.quiz.summary import get_results_keyboard

    return get_results_keyboard(has_errors, lang)


# ============================================================================
# НАЧАЛО РЕПОРТА — показать список слов
# ============================================================================

@router.callback_query(F.data == "report_translation_error")
async def report_start(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    """Начать репорт: показать список слов из викторины"""
    data = await state.get_data()
    report_word_ids = data.get("report_word_ids", [])

    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or DEFAULT_LOCALE
    pair = await report_pair(session, user, data.get("report_session_id"))

    if not report_word_ids:
        await callback.answer(get_text("report_no_words", lang), show_alert=True)
        return

    # Проверяем дневной лимит
    today_count = await _get_today_report_count(callback.from_user.id, session)
    if today_count >= DAILY_REPORT_LIMIT:
        await callback.answer(get_text("report_daily_limit", lang), show_alert=True)
        return

    # Получаем уже зарепорченные
    already_reported = await _get_already_reported_ids(
        callback.from_user.id, session,
        audio_enabled=bool(getattr(user, "audio_enabled", False)), pair=pair,
    )

    # Проверяем есть ли хоть одно новое слово для репорта
    new_available = [wid for wid in report_word_ids if wid not in already_reported]
    if not new_available:
        await callback.answer(get_text("report_all_reported", lang), show_alert=True)
        return

    # Загружаем слова
    result = await session.execute(
        select(Word).where(Word.id.in_(report_word_ids))
    )
    words = result.scalars().all()
    words_by_id = {w.id: w for w in words}

    # Формируем labels в порядке викторины
    word_labels = {}
    for wid in report_word_ids:
        if wid in words_by_id:
            word_labels[wid] = _get_word_label(words_by_id[wid], pair)

    if not word_labels:
        await callback.answer(get_text("report_no_words", lang), show_alert=True)
        return

    # Сохраняем в state
    await state.update_data(
        report_word_labels=word_labels,
        report_selected=[],
        report_page=0,
        report_already_reported=list(already_reported),
    )

    keyboard = _build_word_list_keyboard(word_labels, [], already_reported, 0, lang)

    try:
        await callback.message.edit_reply_markup(reply_markup=keyboard)
    except Exception:
        pass

    await callback.answer()


# ============================================================================
# КЛИК ПО УЖЕ ЗАРЕПОРЧЕННОМУ СЛОВУ
# ============================================================================

@router.callback_query(F.data.startswith("report_already_"))
async def report_already_reported(callback: CallbackQuery, session: AsyncSession):
    """Клик по слову которое уже зарепорчено — показать alert"""
    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or DEFAULT_LOCALE
    await callback.answer(get_text("report_already_sent", lang), show_alert=False)


# ============================================================================
# ПЕРЕКЛЮЧЕНИЕ ГАЛОЧКИ
# ============================================================================

@router.callback_query(F.data.startswith("report_toggle_"))
async def report_toggle_word(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    """Переключить галочку у слова"""
    word_id = int(callback.data.replace("report_toggle_", ""))

    data = await state.get_data()
    word_labels = data.get("report_word_labels", {})
    selected = data.get("report_selected", [])
    already_reported = set(data.get("report_already_reported", []))
    page = data.get("report_page", 0)

    word_labels = {int(k): v for k, v in word_labels.items()}

    if word_id in selected:
        selected.remove(word_id)
    else:
        selected.append(word_id)

    await state.update_data(report_selected=selected)

    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or DEFAULT_LOCALE

    keyboard = _build_word_list_keyboard(word_labels, selected, already_reported, page, lang)

    try:
        await callback.message.edit_reply_markup(reply_markup=keyboard)
    except Exception:
        pass

    await callback.answer()


# ============================================================================
# ПАГИНАЦИЯ
# ============================================================================

@router.callback_query(F.data.startswith("report_page_"))
async def report_change_page(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    """Переключить страницу списка слов"""
    page = int(callback.data.replace("report_page_", ""))

    data = await state.get_data()
    word_labels = data.get("report_word_labels", {})
    selected = data.get("report_selected", [])
    already_reported = set(data.get("report_already_reported", []))

    word_labels = {int(k): v for k, v in word_labels.items()}

    await state.update_data(report_page=page)

    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or DEFAULT_LOCALE

    keyboard = _build_word_list_keyboard(word_labels, selected, already_reported, page, lang)

    try:
        await callback.message.edit_reply_markup(reply_markup=keyboard)
    except Exception:
        pass

    await callback.answer()


# ============================================================================
# ПОДТВЕРЖДЕНИЕ
# ============================================================================

@router.callback_query(F.data == "report_confirm")
async def report_confirm(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    """
    Подтверждение. ОДНО, а не два подряд.

    ЧТО БЫЛО НЕ ТАК. Нажав «✓ Подтвердить (2)», человек получал тот же
    текст итога с другими кнопками — «Отправить» и «Назад», — без единого
    слова о том, что произошло и чего от него ждут. Экран менял ТОЛЬКО
    клавиатуру.

    Владелец на этом и попался: «Закончил викторину, отметил 2 слова как
    ошибка перевода» — и дальше: «в админ панели не вижу, чтобы я отметил
    эти 2 неправильных перевода». В базе их и не было: он подтвердил выбор
    и ушёл, уверенный, что отправил. Два подтверждения подряд человек
    читает как одно.

    ТЕПЕРЬ: если выбирать не из чего — отправляем сразу. Второй шаг
    остаётся только там, где он что-то решает: когда озвучка включена и
    жалоба может быть либо на перевод, либо на произношение. И тогда об
    этом СКАЗАНО, а не показано двумя кнопками молча.
    """
    data = await state.get_data()
    selected = data.get("report_selected", [])

    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or DEFAULT_LOCALE

    if not selected:
        await callback.answer(get_text("report_none_selected", lang), show_alert=True)
        return

    audio_available = bool(getattr(user, "audio_enabled", False))
    if not audio_available:
        # Выбора нет — значит и шага нет. Жалоба уходит немедленно.
        await report_send(callback, state, session, kind="text")
        return

    keyboard = _build_confirm_keyboard(lang, audio_available=True)

    try:
        await callback.message.edit_reply_markup(reply_markup=keyboard)
    except Exception:
        pass

    await callback.answer(
        get_text("report_pick_kind", lang, count=len(selected)), show_alert=True
    )


# ============================================================================
# НАЗАД К СПИСКУ СЛОВ (из экрана подтверждения)
# ============================================================================

@router.callback_query(F.data == "report_back_to_select")
async def report_back_to_select(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    """Вернуться к списку слов с сохранёнными галочками"""
    data = await state.get_data()
    word_labels = data.get("report_word_labels", {})
    selected = data.get("report_selected", [])
    already_reported = set(data.get("report_already_reported", []))
    page = data.get("report_page", 0)

    word_labels = {int(k): v for k, v in word_labels.items()}

    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or DEFAULT_LOCALE

    keyboard = _build_word_list_keyboard(word_labels, selected, already_reported, page, lang)

    try:
        await callback.message.edit_reply_markup(reply_markup=keyboard)
    except Exception:
        pass

    await callback.answer()


# ============================================================================
# ОТПРАВКА РЕПОРТА
# ============================================================================

@router.callback_query(F.data == "report_send_text")
async def report_send_text(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    """Жалоба на перевод."""
    await report_send(callback, state, session, kind="text")


@router.callback_query(F.data == "report_send_audio")
async def report_send_audio(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    """
    Жалоба на произношение.

    Записывается вместе с голосом, которым человек слышал слово: без этого
    проверить жалобу нечем — голосов на язык до шести, и звучат они по-разному.
    """
    await report_send(callback, state, session, kind="audio")


@router.callback_query(F.data == "report_send")
async def report_send(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
    kind: str = "text",
):
    """Сохранить репорты в БД и вернуть исходные кнопки"""
    data = await state.get_data()
    selected = data.get("report_selected", [])
    report_session_id = data.get("report_session_id")
    saved_errors = data.get("saved_errors", [])

    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or DEFAULT_LOCALE

    if not selected:
        await callback.answer(get_text("report_none_selected", lang), show_alert=True)
        return

    # Проверяем дневной лимит
    today_count = await _get_today_report_count(callback.from_user.id, session)
    remaining = DAILY_REPORT_LIMIT - today_count
    if remaining <= 0:
        await callback.answer(get_text("report_daily_limit", lang), show_alert=True)
        return

    # Ограничиваем количество если лимит близко
    words_to_report = selected[:remaining]

    # ПАРА — ТА, В КОТОРОЙ ОШИБКУ ВИДЕЛИ: из занятия, а не нынешняя (Н4).
    # Человек мог сменить язык между занятием и жалобой
    pair = await report_pair(session, user, report_session_id)

    # Голос нужен только для жалобы на произношение: по тексту он ни при чём
    voice = None
    if kind == "audio":
        voice = await voice_for_user(session, user.id, pair.learning)

    # Создаём записи (пропускаем дубликаты)
    saved_count = 0
    for word_id in words_to_report:
        existing = await session.execute(
            select(TranslationReport)
            .where(
                TranslationReport.user_id == callback.from_user.id,
                TranslationReport.word_id == word_id,
                TranslationReport.kind == kind,
                TranslationReport.learning_lang == pair.learning,
                TranslationReport.native_lang == pair.native,
            )
        )
        if existing.scalar_one_or_none():
            continue

        report = TranslationReport(
            user_id=callback.from_user.id,
            word_id=word_id,
            quiz_session_id=report_session_id,
            kind=kind,
            voice=voice,
            learning_lang=pair.learning,
            native_lang=pair.native,
            status="pending",
        )
        session.add(report)
        saved_count += 1

    await session.commit()

    logger.info(
        f"User {callback.from_user.id} reported {saved_count} words as {kind} "
        f"(selected={len(selected)}, session={report_session_id}, voice={voice})"
    )

    # Показываем alert
    if saved_count > 0:
        # Обещанное число баллов берётся ОТТУДА ЖЕ, откуда его начисляет
        # подтверждение. Прежде в шести локалях стояло «+1 балл» словами, то
        # есть обещание жило отдельно от начисления и соврало бы при первой
        # же правке цены. Слово при числе — тоже по числу: при цене 1 строка
        # «+{points} баллов» дала бы «+1 баллов»
        key = "report_sent_audio" if kind == "audio" else "report_sent"
        points = plural(REPORT_REWARD_POINTS, "plural_points", lang)
        await callback.answer(
            get_text(key, lang, count=saved_count, points=points),
            show_alert=True
        )
    else:
        await callback.answer(
            get_text("report_all_reported", lang),
            show_alert=True
        )

    # Возвращаем исходные кнопки результата
    has_errors = bool(saved_errors)
    keyboard = _get_results_keyboard_lazy(has_errors, lang)

    try:
        await callback.message.edit_reply_markup(reply_markup=keyboard)
    except Exception:
        pass


# ============================================================================
# ОТМЕНА — возврат к кнопкам результата
# ============================================================================

@router.callback_query(F.data == "report_cancel")
async def report_cancel(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    """Отмена репорта — вернуть исходные кнопки результата"""
    data = await state.get_data()
    saved_errors = data.get("saved_errors", [])

    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language or DEFAULT_LOCALE

    has_errors = bool(saved_errors)
    keyboard = _get_results_keyboard_lazy(has_errors, lang)

    try:
        await callback.message.edit_reply_markup(reply_markup=keyboard)
    except Exception:
        pass

    await callback.answer()