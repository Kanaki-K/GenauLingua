"""
Работают ли сообщения вовлечения — или вредят (патч 2.1).

Владелец 15.10: «нужно внимательно трекать, чтобы точно понимать, что это
либо работает, либо вредит». Одного «вернулись после сообщения» для этого
мало: часть вернулась бы и без него. Поэтому рядом — контрольная группа
(`holdout`: решение было, сообщения не было), и разница между ними — то,
что сделало само сообщение. А вред виден в двух последних столбцах: кто
после сообщения отписался («Не присылать», выключил) и кто заблокировал
бота.

Всё считается из занятий и отметок, а не хранится в журнале: поправят
правило отчёта — пересчитается и прошлое.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta

from sqlalchemy import select

from app.database.models import NudgeLog, QuizSession, User

WINDOW = timedelta(hours=24)


@dataclass
class KindStats:
    sent: int = 0
    returned: int = 0            # закончил занятие в течение суток
    via_button: int = 0          # начал занятие кнопкой из этого сообщения
    stopped: int = 0             # отписался в течение суток
    blocked: int = 0
    holdout: int = 0
    holdout_returned: int = 0


@dataclass
class NudgeReport:
    since: datetime
    kinds: dict[str, KindStats] = field(default_factory=dict)

    def total(self) -> KindStats:
        out = KindStats()
        for stats in self.kinds.values():
            for name in vars(out):
                setattr(out, name, getattr(out, name) + getattr(stats, name))
        return out


async def nudge_report(session, now: datetime, days: int = 14) -> NudgeReport:
    since = now - timedelta(days=days)
    logs = (await session.execute(
        select(NudgeLog).where(NudgeLog.sent_at >= since).order_by(NudgeLog.sent_at)
    )).scalars().all()
    report = NudgeReport(since=since)
    if not logs:
        return report

    ids = {log.user_id for log in logs}
    lessons = (await session.execute(
        select(QuizSession.user_id, QuizSession.started_at, QuizSession.completed_at,
               QuizSession.start_source)
        .where(QuizSession.user_id.in_(ids), QuizSession.started_at >= since)
    )).all()
    by_user: dict[int, list] = {}
    for row in lessons:
        by_user.setdefault(row.user_id, []).append(row)
    declined = dict((await session.execute(
        select(User.id, User.reminders_declined_at).where(User.id.in_(ids))
    )).all())

    for log in logs:
        stats = report.kinds.setdefault(log.kind, KindStats())
        end = log.sent_at + WINDOW
        rows = by_user.get(log.user_id, [])
        came_back = any(r.completed_at and log.sent_at < r.completed_at <= end for r in rows)
        if log.outcome == "holdout":
            stats.holdout += 1
            stats.holdout_returned += came_back
            continue
        if log.outcome == "forbidden":
            stats.blocked += 1
            continue
        if log.outcome != "sent":
            continue
        stats.sent += 1
        stats.returned += came_back
        stats.via_button += any(r.start_source == f"nd_{log.kind}"
                                and log.sent_at < r.started_at <= end for r in rows)
        moment = declined.get(log.user_id)
        stats.stopped += bool(moment and log.sent_at < moment <= end)
    return report


def share(part: int, whole: int) -> str:
    return f"{round(100 * part / whole)}%" if whole else "—"
