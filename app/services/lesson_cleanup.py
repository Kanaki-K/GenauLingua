"""
Висящие занятия закрываются сами (2.2.1).

Незаконченное занятие закрывалось только следующим нажатием «Учить»
(`lesson._close_abandoned_sessions`). Кто не вернулся, оставлял занятие
открытым навсегда: на проде 18.10 таких 25 старше суток без причины выхода,
и статистика уходов и путь новичка считались по ним неверно.

Раз в сутки занятие без ответов дольше `STALE_AFTER` помечается брошенным —
ровно так же, как это сделало бы новое нажатие. Срок равен жизни занятия в
Redis (двое суток): то, что ещё можно продолжить, не трогается. Людям ничего
не пишется.
"""
from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.clock import utcnow
from app.database.models import QuizQuestion, QuizSession

logger = logging.getLogger(__name__)

STALE_AFTER = timedelta(days=2)


async def close_stale_lessons(session: AsyncSession, now: Optional[datetime] = None) -> int:
    """Пометить брошенными занятия без движения дольше `STALE_AFTER`. Сколько закрыто."""
    cutoff = (now or utcnow()) - STALE_AFTER
    last_answer = (select(func.max(QuizQuestion.answered_at))
                   .where(QuizQuestion.session_id == QuizSession.id)
                   .scalar_subquery())
    result = await session.execute(
        update(QuizSession)
        .where(QuizSession.is_completed.is_(False),
               QuizSession.exit_reason.is_(None),
               func.coalesce(last_answer, QuizSession.started_at) < cutoff)
        .values(exit_reason="abandoned", exit_at_question=QuizSession.answered_questions)
        .execution_options(synchronize_session=False)
    )
    await session.commit()
    closed = result.rowcount or 0
    if closed:
        logger.info("висящих занятий закрыто: %s", closed)
    return closed


async def close_stale_lessons_job() -> int:
    from app.database.session import AsyncSessionLocal

    async with AsyncSessionLocal() as session:
        return await close_stale_lessons(session)
