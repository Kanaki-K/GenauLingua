"""
Нажатие по кнопке занятия, которого бот уже не помнит.

ЗАЧЕМ. Состояние занятия живёт в памяти процесса (`MemoryStorage`), и
перезапуск бота его стирает: выкатка, падение, перезапуск контейнера.
Карточки на экране у людей остаются, а нажатия по ним прежде пропадали
молча — у ответа кнопкой просто не находилось обработчика, доска и сборка
гасили нажатие без слова. Владелец, живой тест 14.10: «заглючило, не даёт
пары дособирать, не выбирается вариант» — бот перезапустили посреди доски.

Теперь такое нажатие получает короткое объяснение, а под сообщением вместо
мёртвых кнопок встаёт одна — «Ещё занятие». То же для карточки занятия,
которое давно закончилось: нажатие по ней тоже ни к чему не ведёт.

Роутер стоит ПОСЛЕ игровых: живое занятие свои нажатия ловит раньше, сюда
доходят только те, что не нашли обработчика. Доска и сборка ловят свои
нажатия всегда и сами зовут `lesson_expired`, когда занятия нет.
"""

from __future__ import annotations

import logging

from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User
from app.locales import DEFAULT_LOCALE, get_text

logger = logging.getLogger(__name__)

router = Router()

# Кнопки занятия, которые без живого состояния ни к чему не ведут.
# `answer_…`, «Дальше», «Послушать медленно», «Пропустить»
_LESSON_BUTTONS = ("answer_", "next_question", "speech_reference", "speech_skip",
                   "listen_skip")


async def lesson_expired(callback: CallbackQuery, session: AsyncSession) -> None:
    """Объяснить и заменить мёртвые кнопки одной «Ещё занятие»."""
    user = await session.get(User, callback.from_user.id)
    lang = (user.interface_language if user else None) or DEFAULT_LOCALE
    await callback.answer(get_text("lesson_expired", lang), show_alert=True)
    try:
        await callback.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(
                text=get_text("quiz_btn_one_more", lang),
                callback_data="learn_now:again",
            )]]
        ))
    except Exception:
        # Сообщение могли удалить или кнопки уже те же — не беда
        logger.debug("кнопки устаревшего занятия не заменились", exc_info=True)


@router.callback_query(F.data.startswith(_LESSON_BUTTONS))
async def stale_lesson_button(callback: CallbackQuery, session: AsyncSession):
    await lesson_expired(callback, session)
