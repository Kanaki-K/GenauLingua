"""
«Говорю» — по желанию (2.2.1, владелец 18.10).

Прод 14–18.10: игра показана 78 раз и пропущена 42, голосом ответили 6
человек; одному она пришла 23 раза и 21 раз была пропущена. Говорить вслух
готов не каждый — в транспорте, на работе, рядом с людьми. Поэтому игра не
приходит сама: под итогом занятия, когда у человека уже есть слово, готовое
для «Говорю», бот один раз ПРЕДЛАГАЕТ попробовать.

Когда спрашивать:
  * звук включён, закончено не меньше `MIN_LESSONS` занятий;
  * есть слово, узнанное верно 2+ раза (раньше «Говорю» и не откроется);
  * ещё не спрашивали, или «Не сейчас» было `ASK_AGAIN` назад и больше;
  * в этом итоге не предлагался уровень — одно предложение за занятие.

«Попробовать» — игра включается и придёт в следующем занятии (не раньше
4-го вопроса, `SPEECH_FROM_QUESTION`). «Не сейчас» — спросим через неделю.
Включить или убрать можно и в настройках — это тоже выбор человека.
"""
import logging
from datetime import datetime, timedelta
from typing import Optional

from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.clock import utcnow
from app.database.models import User, UserWord
from app.locales import DEFAULT_LOCALE, get_text
from app.services import journal
from app.services.quiz_service import SPEECH_LATER, SPEECH_ON

logger = logging.getLogger(__name__)

router = Router()

MIN_LESSONS = 2
ASK_AGAIN = timedelta(days=7)
READY_CORRECT = 2          # тот же порог, что открывает «Говорю» слову
CB_TRY = "speech_try"
CB_LATER = "speech_later"


async def should_invite(session: AsyncSession, user: User,
                        now: Optional[datetime] = None) -> bool:
    if not getattr(user, "audio_enabled", True):
        return False
    choice = user.speech_choice
    if choice == SPEECH_LATER:
        asked = user.speech_asked_at
        if asked is not None and (now or utcnow()) - asked < ASK_AGAIN:
            return False
    elif choice is not None:
        return False
    if (user.quizzes_passed or 0) < MIN_LESSONS:
        return False
    ready = (await session.execute(
        select(UserWord.word_id).where(
            UserWord.user_id == user.id,
            UserWord.learning_lang == (user.learning_lang or "de"),
            UserWord.times_correct >= READY_CORRECT,
        ).limit(1)
    )).first()
    return ready is not None


async def send_invite(bot, chat_id: int, session: AsyncSession, user: User, lang: str) -> None:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=get_text("btn_speech_try", lang), callback_data=CB_TRY),
        InlineKeyboardButton(text=get_text("btn_speech_later", lang), callback_data=CB_LATER),
    ]])
    await bot.send_message(chat_id, get_text("speech_invite_text", lang), reply_markup=keyboard)
    user.speech_asked_at = utcnow()
    journal.note(session, user.id, "speech_invite", "shown")
    await session.commit()


@router.callback_query(F.data == CB_TRY)
async def speech_try(callback: CallbackQuery, session: AsyncSession):
    """«Попробовать» — игра включается; в следующем занятии придёт сама."""
    await callback.answer()
    user = await session.get(User, callback.from_user.id)
    if user is None:
        return
    lang = user.interface_language or DEFAULT_LOCALE
    user.speech_choice = SPEECH_ON
    if "s" not in (user.quiz_channels or ""):
        user.quiz_channels = (user.quiz_channels or "t") + "s"
    user.speech_asked_at = utcnow()
    journal.note(session, user.id, "speech_invite", "try")
    await session.commit()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
        text=get_text("btn_learn_words", lang), callback_data="learn_now:again")]])
    try:
        await callback.message.edit_text(get_text("speech_try_done", lang), reply_markup=keyboard)
    except Exception:
        logger.debug("приглашение не поправилось", exc_info=True)


@router.callback_query(F.data == CB_LATER)
async def speech_later(callback: CallbackQuery, session: AsyncSession):
    """«Не сейчас» — ничего не включается, спросим через неделю."""
    await callback.answer()
    user = await session.get(User, callback.from_user.id)
    if user is None:
        return
    user.speech_choice = SPEECH_LATER
    user.speech_asked_at = utcnow()
    journal.note(session, user.id, "speech_invite", "later")
    await session.commit()
    try:
        await callback.message.delete()
    except Exception:
        logger.debug("приглашение не удалилось", exc_info=True)
