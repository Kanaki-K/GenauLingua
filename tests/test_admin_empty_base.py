# -*- coding: utf-8 -*-
"""Аудит 2.1 (a3): админка на пустой базе не падает."""
import pytest

pytestmark = pytest.mark.asyncio


async def test_admin_on_empty_db(session):
    from app.bot.handlers.admin import _get_main_stats, retention_today

    assert await retention_today(session) == (0, 0, 0, 0)
    text = await _get_main_stats(session)
    assert "Сегодня начали" in text and "0 из 0" in text, text


async def test_unfinished_today_counts_as_started_not_finished(session, user):
    """Начал сегодня, не закончил (exit_reason None) — «начали» 1, «закончили» 0."""
    from app.bot.handlers.admin import retention_today
    from tests.test_admin_retention import _lesson

    session.add(_lesson(user.id, 0, done=False, answered=2))
    await session.commit()
    started, finished, back, base = await retention_today(session)
    assert (started, finished, back, base) == (1, 0, 0, 0)
