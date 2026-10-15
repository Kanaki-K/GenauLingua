# -*- coding: utf-8 -*-
"""
Админка, патч 2.1: «начали / закончили» раздельно и «вернулись сегодня из
активных за 7 дней» (CURR). 15.10 админка показала «сегодня 9», а занимались
22: «сегодня» считало только закончивших.
"""
from datetime import datetime, timedelta

import pytest

from app.core.clock import utctoday
from app.database.enums import CEFRLevel
from app.database.models import QuizSession, User

pytestmark = pytest.mark.asyncio


def _at(days_ago: int, hour: int = 12) -> datetime:
    return datetime.combine(utctoday() - timedelta(days=days_ago), datetime.min.time()) + timedelta(hours=hour)


def _lesson(user_id, days_ago, *, done=True, answered=7, exit_reason=None):
    moment = _at(days_ago, hour=0) + timedelta(minutes=30) if days_ago == 0 else _at(days_ago)
    return QuizSession(user_id=user_id, level=CEFRLevel.A1, total_questions=7,
                       answered_questions=answered, is_completed=done,
                       started_at=moment, completed_at=moment if done else None,
                       exit_reason=exit_reason)


async def test_returned_today_among_active_last_week(session, user):
    from app.bot.handlers.admin import retention_today

    b = User(id=2001, first_name="B", interface_language="ru", learning_lang="de", native_lang="ru")
    c = User(id=2002, first_name="C", interface_language="ru", learning_lang="de", native_lang="ru")
    d = User(id=2003, first_name="D", interface_language="ru", learning_lang="de", native_lang="ru")
    session.add_all([b, c, d])
    session.add_all([
        _lesson(user.id, 3), _lesson(user.id, 0),        # был на неделе и вернулся
        _lesson(b.id, 2),                                 # был на неделе, сегодня нет
        _lesson(c.id, 0),                                 # новичок — только сегодня
        _lesson(d.id, 0, done=False, answered=0, exit_reason="restarted"),
    ])
    await session.commit()

    started, finished, back, base = await retention_today(session)
    assert (back, base) == (1, 2), (back, base)
    assert started == 2, "пустой перезапуск засчитан как приход"
    assert finished == 2 and finished <= started
