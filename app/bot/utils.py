"""
Общие утилиты для хендлеров бота
"""

import asyncio
import logging

from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.keyboards import get_main_menu_keyboard
from app.database.models import User

logger = logging.getLogger(__name__)


# Telegram ограничивает бота примерно 30 сообщениями в секунду. Удаляем
# порциями с паузой, иначе большой разрыв в id упирается в лимит и получаем 429.
DELETE_CHUNK_SIZE = 20
DELETE_CHUNK_PAUSE = 0.35
# Разрыв больше этого означает, что пользователь давно не заходил: вычищать
# сотни чужих сообщений бессмысленно и дорого
MAX_DELETE_RANGE = 100


async def delete_messages_fast(bot, chat_id: int, start_id: int, end_id: int):
    """Массовое удаление сообщений между start_id и end_id"""
    if end_id <= start_id:
        return

    first_id = max(start_id, end_id - MAX_DELETE_RANGE)
    message_ids = list(range(first_id, end_id))

    deleted = 0
    for offset in range(0, len(message_ids), DELETE_CHUNK_SIZE):
        chunk = message_ids[offset:offset + DELETE_CHUNK_SIZE]
        results = await asyncio.gather(
            *(bot.delete_message(chat_id=chat_id, message_id=mid) for mid in chunk),
            return_exceptions=True,
        )
        deleted += sum(1 for r in results if not isinstance(r, Exception))

        if offset + DELETE_CHUNK_SIZE < len(message_ids):
            await asyncio.sleep(DELETE_CHUNK_PAUSE)

    logger.debug("Удалено %d/%d сообщений", deleted, len(message_ids))


async def ensure_anchor(message: Message, session: AsyncSession, user: User, emoji: str = "🏠"):
    """Создать новое якорное сообщение с главным меню"""
    old_anchor_id = user.anchor_message_id
    lang = user.interface_language or "ru"
    try:
        sent = await message.answer(emoji, reply_markup=get_main_menu_keyboard(lang))
        new_anchor_id = sent.message_id
        user.anchor_message_id = new_anchor_id
        await session.commit()
        logger.debug(f"Создан новый якорь {new_anchor_id}")
        return old_anchor_id, new_anchor_id
    except Exception as e:
        logger.error(f"Ошибка создания якоря: {e}")
        return old_anchor_id, None