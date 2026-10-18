"""
Журнал пути человека — `UserEvent` (патч 2.1).

Владелец 16.10: «мы должны иметь возможность разбирать весь путь, чтобы
быть лучше после анализа». Разбор 15.10 упёрся в то, чего бот не писал:
что нажимал польский новичок перед уходом, с какой попытки распознан голос.

Два вида записей:
  * каждое обновление Telegram — middleware `install_journal`: вид
    действия (кнопка, команда, голосовое) и сколько бот его обрабатывал;
  * события изнутри обработчиков — `note`: показанный вопрос, попытка
    голосом, пропуск.

Запись идёт в ТУ ЖЕ сессию базы, что и обработчик, и фиксируется в конце
нажатия. Сбой журнала занятию не мешает: он проглатывается и пишется в лог.
"""
from __future__ import annotations

import logging
import time
from typing import Optional

from app.bot.slow_log import describe
from app.core.clock import utcnow
from app.database.models import UserEvent

logger = logging.getLogger(__name__)


def note(session, user_id: int, kind: str, action: Optional[str] = None, *,
         session_id: Optional[int] = None, word_id: Optional[int] = None,
         channel: Optional[str] = None, **data) -> None:
    """Событие изнутри обработчика. Фиксируется вместе с нажатием."""
    if session is None or not user_id:
        return
    try:
        session.add(UserEvent(
            user_id=user_id, at=utcnow(), kind=kind, action=(action or None) and action[:64],
            session_id=session_id, word_id=word_id, channel=channel,
            data={k: v for k, v in data.items() if v is not None} or None,
        ))
    except Exception:
        logger.warning("журнал: событие %s не записано", kind, exc_info=True)


def _user_id(update) -> Optional[int]:
    for part in ("callback_query", "message"):
        event = getattr(update, part, None)
        sender = getattr(event, "from_user", None)
        if sender is not None:
            return sender.id
    return None


async def journal_update(handler, event, data):
    """Middleware: каждое нажатие и сообщение — в журнал, с длительностью."""
    started = time.perf_counter()
    try:
        return await handler(event, data)
    finally:
        session = data.get("session")
        user_id = _user_id(event)
        if session is not None and user_id:
            try:
                session.add(UserEvent(
                    user_id=user_id, at=utcnow(),
                    kind="tap" if getattr(event, "callback_query", None) is not None else "msg",
                    action=describe(event)[:64],
                    ms=int((time.perf_counter() - started) * 1000),
                ))
                await session.commit()
            except Exception:
                logger.warning("журнал: нажатие не записано", exc_info=True)
                try:
                    await session.rollback()
                except Exception:
                    pass


def install_journal(dp) -> None:
    """
    Журнал — ВНУТРЕННИЙ middleware ПОСЛЕ того, что подставляет сессию базы:
    ему нужна `data["session"]`. Вызывать сразу после регистрации сессии —
    и в `app.main`, и в `app.testing` (иначе приёмки его не проверят).
    """
    dp.update.middleware()(journal_update)


async def journal_error(event, session_factory=None) -> None:
    """
    Необработанная ошибка — в журнал пути человека (2.2.1): вид исключения и
    действие, на котором оно случилось, без текста ошибки. Иначе по журналу не
    узнать, кто наткнулся на сбой и ушёл ли после. Сессия своя: сессия
    обработчика к этому моменту откатана. Сбой записи не мешает ничему.
    """
    try:
        if session_factory is None:
            from app.database.session import AsyncSessionLocal as session_factory
        update = getattr(event, "update", None)
        user_id = _user_id(update) if update is not None else None
        if not user_id:
            return
        async with session_factory() as session:
            session.add(UserEvent(
                user_id=user_id, at=utcnow(), kind="error",
                action=type(event.exception).__name__[:64],
                data={"where": describe(update)[:64]},
            ))
            await session.commit()
    except Exception:
        logger.warning("журнал: ошибка не записана", exc_info=True)
