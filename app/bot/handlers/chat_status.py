"""
Человек заблокировал бота или вернулся — в журнал в тот же момент (2.2.1).

Прежде блокировка была видна только косвенно: когда очередное сообщение не
доходило (`nudge_log.outcome='forbidden'`, журнал рассылки). Когда человек
ушёл — после какого занятия, какого сообщения, на какой день, — восстановить
было нельзя. Telegram сообщает об этом сам (`my_chat_member`): здесь это
пишется в журнал пути, ничего не отвечая.
"""
import logging

from aiogram import Router
from aiogram.types import ChatMemberUpdated
from sqlalchemy.ext.asyncio import AsyncSession

from app.services import journal

logger = logging.getLogger(__name__)

router = Router()

GONE = frozenset({"kicked", "left"})


@router.my_chat_member()
async def bot_status_changed(event: ChatMemberUpdated, session: AsyncSession):
    if event.chat.type != "private" or event.from_user is None:
        return
    before = event.old_chat_member.status
    after = event.new_chat_member.status
    action = "blocked" if after in GONE else "unblocked" if before in GONE else "status"
    journal.note(session, event.from_user.id, "chat", action, frm=str(before), to=str(after))
    try:
        await session.commit()
    except Exception:
        logger.warning("журнал: статус бота не записан", exc_info=True)
