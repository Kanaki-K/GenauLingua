"""
Жалоба прямо на разборе ответа — у каждого слова, а не в конце занятия.

ЗАЧЕМ (владелец, 17.10): «в конце игры уже просто можно не помнить что там
было не так, а так будет по сути всегда напоминание». Список слов в итоге
просил вспомнить, где споткнулся, через десять вопросов; здесь ошибка ещё
на экране.

Ход — три нажатия, и ни одно не лишнее:
  1. «Сообщить об ошибке» под «Далее» — раскрывает выбор;
  2. что не так: перевод, пример, озвучка — можно несколько, отмеченное с ✓;
  3. «Отправить» — оно же подтверждение: видно, что именно уходит.

Предлагается только то, что человек видел: пример — если он был на экране,
озвучка — если звук играл (клип разбора, вопрос на слух, эталон речи).

ВСЁ НУЖНОЕ — В САМОЙ КНОПКЕ: слово, что предлагалось, что отмечено. От
состояния занятия жалоба не зависит: нажатие под карточкой прошлого вопроса
или после конца занятия жалуется на ТО слово, под которым стоит.

«Далее» — последней строкой на каждом шаге, под жалобой (владелец, 17.10:
«дальше должно быть ниже»): жалоба — побочный путь, и занятие не должно
ждать, пока её дособирают.
"""

import logging
from typing import Optional

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import TranslationReport, User, Word
from app.locales import DEFAULT_LOCALE, get_text, plural
from app.services.language_service import LanguagePair, example_text

logger = logging.getLogger(__name__)

router = Router()

PREFIX = "rp"

# Вид жалобы — бит в кнопке. Порядок — порядок кнопок на экране
TEXT, EXAMPLE, AUDIO = 1, 2, 4
_KINDS = ((TEXT, "text", "report_kind_text"),
          (EXAMPLE, "example", "report_kind_example"),
          (AUDIO, "audio", "report_kind_audio"))


def offered(word: Word, pair: LanguagePair, *, heard: bool) -> int:
    """Какие виды предложить: только то, что человек на этом слове видел."""
    mask = TEXT
    if example_text(word, pair.learning) or example_text(word, pair.native):
        mask |= EXAMPLE
    if heard:
        mask |= AUDIO
    return mask


def _next_row(lang: str) -> list[InlineKeyboardButton]:
    return [InlineKeyboardButton(text=get_text("quiz_btn_next", lang),
                                 callback_data="next_question")]


def answer_keyboard(lang: str, word_id: int, avail: int) -> InlineKeyboardMarkup:
    """Разбор ответа: «Сообщить об ошибке» и под ним — «Далее»."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text("quiz_btn_report_error", lang),
                              callback_data=f"{PREFIX}:o:{word_id}:{avail}:0")],
        _next_row(lang),
    ])


def _pick_keyboard(lang: str, word_id: int, avail: int, sel: int) -> InlineKeyboardMarkup:
    kinds = []
    for bit, _, key in _KINDS:
        if not avail & bit:
            continue
        mark = "✓ " if sel & bit else ""
        kinds.append(InlineKeyboardButton(
            text=f"{mark}{get_text(key, lang)}",
            callback_data=f"{PREFIX}:t:{word_id}:{avail}:{sel ^ bit}",
        ))
    last = [InlineKeyboardButton(text=get_text("btn_back", lang),
                                 callback_data=f"{PREFIX}:b:{word_id}:{avail}:0")]
    if sel:
        last.append(InlineKeyboardButton(text=get_text("report_btn_send", lang),
                                         callback_data=f"{PREFIX}:s:{word_id}:{avail}:{sel}"))
    return InlineKeyboardMarkup(inline_keyboard=[kinds, last, _next_row(lang)])


def _sent_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text("report_btn_sent", lang),
                              callback_data=f"{PREFIX}:d:0:0:0")],
        _next_row(lang),
    ])


def _parse(data: str) -> Optional[tuple[str, int, int, int]]:
    try:
        _, op, word_id, avail, sel = data.split(":")
        return op, int(word_id), int(avail), int(sel)
    except ValueError:
        return None


async def _edit(callback: CallbackQuery, keyboard: InlineKeyboardMarkup) -> None:
    try:
        await callback.message.edit_reply_markup(reply_markup=keyboard)
    except Exception:
        logger.debug("клавиатура жалобы не обновилась", exc_info=True)


@router.callback_query(F.data.startswith(f"{PREFIX}:"))
async def report_inline(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    parsed = _parse(callback.data or "")
    user = await session.get(User, callback.from_user.id)
    lang = (user.interface_language if user else None) or DEFAULT_LOCALE
    if parsed is None or user is None:
        await callback.answer()
        return
    op, word_id, avail, sel = parsed
    sel &= avail

    if op == "d":
        await callback.answer(get_text("report_already_sent", lang))
        return
    if op == "b":
        await _edit(callback, answer_keyboard(lang, word_id, avail))
        await callback.answer()
        return
    if op in ("o", "t"):
        await _edit(callback, _pick_keyboard(lang, word_id, avail, sel))
        await callback.answer(get_text("report_pick_hint", lang) if op == "o" else None)
        return
    if op == "s" and sel:
        await _send(callback, state, session, user, lang, word_id, sel)
        return
    await callback.answer()


async def _send(callback: CallbackQuery, state: FSMContext, session: AsyncSession,
                user: User, lang: str, word_id: int, sel: int) -> None:
    from app.bot.handlers.quiz.report import (
        DAILY_REPORT_LIMIT, REPORT_REWARD_POINTS, _get_today_report_count, report_pair,
    )
    from app.services.audio_service import voice_for_user

    if await session.get(Word, word_id) is None:
        await callback.answer()
        return
    remaining = DAILY_REPORT_LIMIT - await _get_today_report_count(user.id, session)
    if remaining <= 0:
        await callback.answer(get_text("report_daily_limit", lang), show_alert=True)
        return

    # Пара — того занятия, что идёт или только что шло: в нём слово и видели
    data = await state.get_data()
    quiz_id = data.get("session_id") or data.get("report_session_id")
    pair = await report_pair(session, user, quiz_id)

    saved = 0
    for bit, kind, _ in _KINDS:
        if not sel & bit or saved >= remaining:
            continue
        exists = (await session.execute(select(TranslationReport.id).where(
            TranslationReport.user_id == user.id,
            TranslationReport.word_id == word_id,
            TranslationReport.kind == kind,
            TranslationReport.learning_lang == pair.learning,
            TranslationReport.native_lang == pair.native,
        ))).first()
        if exists:
            continue
        voice = await voice_for_user(session, user.id, pair.learning) if kind == "audio" else None
        session.add(TranslationReport(
            user_id=user.id, word_id=word_id, quiz_session_id=quiz_id, kind=kind,
            voice=voice, learning_lang=pair.learning, native_lang=pair.native,
            status="pending",
        ))
        saved += 1
    await session.commit()
    logger.info("User %s reported word %s from the answer card: mask=%s saved=%s pair=%s-%s",
                user.id, word_id, sel, saved, pair.learning, pair.native)

    if saved:
        points = plural(REPORT_REWARD_POINTS, "plural_points", lang)
        await callback.answer(get_text("report_sent_one", lang, points=points), show_alert=True)
    else:
        await callback.answer(get_text("report_already_sent", lang), show_alert=True)
    await _edit(callback, _sent_keyboard(lang))
