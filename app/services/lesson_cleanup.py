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


# «ВЫУЧЕНО» У ЧЕЛОВЕКА СВЕРЯЕТСЯ С ЕГО СЛОВАМИ (репетиция 2.2.1 на копии прода).
# Счётчик `users.words_learned` пересчитывается только в конце ЗАКОНЧЕННОГО
# занятия, а слово становится выученным прямо при ответе. Двое людей 18.10
# начали по пять занятий, не закончили ни одного и выучили 6 и 2 слова —
# в статистике у них стоял ноль, и приёмка учёта поймала расхождение.
# Правило — то же, что у приёмки (`audit_accounting`): выученные слова в
# изучаемом языке человека.
SYNC_WORDS_LEARNED = """
    update users u set words_learned = coalesce(r.n, 0)
    from users x left join (
        select uw.user_id, count(*) n from user_words uw join users v on v.id = uw.user_id
        where uw.learned and uw.learning_lang = v.learning_lang group by uw.user_id
    ) r on r.user_id = x.id
    where u.id = x.id and coalesce(u.words_learned, 0) <> coalesce(r.n, 0)
"""


async def sync_words_learned(session: AsyncSession) -> int:
    """Поправить «выучено» у тех, у кого счётчик разошёлся со словами. Сколько поправлено."""
    from sqlalchemy import text

    result = await session.execute(text(SYNC_WORDS_LEARNED))
    await session.commit()
    fixed = result.rowcount or 0
    if fixed:
        logger.info("«выучено» сверено с словами: поправлено у %s", fixed)
    return fixed


async def close_stale_lessons_job() -> int:
    from app.database.session import AsyncSessionLocal

    async with AsyncSessionLocal() as session:
        closed = await close_stale_lessons(session)
        await sync_words_learned(session)
        return closed
