# -*- coding: utf-8 -*-
"""
Аудит 2.1: настоящие приёмка и починка на случайных
историях; полночь между завершением и отметкой дня; админка на границе
суток; 🔥 в рейтинге.
"""
from __future__ import annotations

import random
from datetime import datetime, timedelta
from types import SimpleNamespace

import pytest

from app.core.clock import utctoday
from app.database.enums import CEFRLevel
from app.database.models import QuizSession, User
from app.services.streak_service import register_activity, user_day

from test_streak_history_property import ZONES, random_history

pytestmark = pytest.mark.asyncio


def _session_row(user_id, moment, kind):
    return QuizSession(
        user_id=user_id, level=CEFRLevel.A1, total_questions=7,
        answered_questions=7 if kind != "abandoned" else 2,
        correct_answers=5, is_completed=kind != "abandoned",
        started_at=moment - timedelta(minutes=3),
        completed_at=moment if kind != "abandoned" else None,
        quiz_mode="error_repeat" if kind == "repeat" else None,
    )


async def test_real_audit_and_repair_agree_with_live_path(session):
    from app.scripts.audit_accounting import Report, _check_streaks
    from app.scripts.repair_accounting import repair_user_totals

    rng = random.Random(7)
    rows = []
    for uid in range(5000, 5400):
        tz, offset = rng.choice(ZONES)
        # timezone=None база заменяет умолчанием колонки (Europe/Berlin) — так и считаем
        tz = tz or "Europe/Berlin"
        person = User(id=uid, first_name="P", interface_language="ru", learning_lang="de",
                      native_lang="ru", reverse_mode=False, timezone=tz, utc_offset=offset,
                      streak_days=0, best_streak_days=0, quizzes_passed=0, words_learned=0)
        history = random_history(rng, tz, offset)
        for moment, kind in history:
            rows.append(_session_row(uid, moment, kind))
            if kind == "scored":
                person.quizzes_passed += 1
                register_activity(person, today=user_day(person, moment))
        session.add(person)
    await session.commit()
    session.add_all(rows)
    await session.commit()

    rep = Report(show=5)
    await _check_streaks(session, rep)
    assert not rep.bad, rep.bad
    fixed = await repair_user_totals(session, apply=False)
    assert fixed == 0, fixed


async def test_midnight_between_completion_and_day_mark(session, user, monkeypatch):
    """
    `_finish_quiz` ставит `completed_at=utcnow()`, а день отмечает позже —
    `update_user_activity` → `register_activity` → `user_today(utcnow())`.
    Между ними — коммит, `update_monthly_stats` и запросы. Занятие,
    законченное в 23:59:59.8 по Берлину, отмечается днём, который
    наступил через полсекунды; приёмка читает день из `completed_at`.
    """
    import app.services.streak_service as SS
    from app.bot.handlers.quiz.summary import update_user_activity
    from app.scripts.audit_accounting import Report, _check_streaks

    user.timezone = "Europe/Berlin"
    # Вчера (по Берлину 19.11) занятие, серия 1
    y = datetime(2026, 11, 19, 12, 0)
    session.add(_session_row(user.id, y, "scored"))
    register_activity(user, today=user_day(user, y))
    await session.commit()

    completed = datetime(2026, 11, 20, 22, 59, 59, 800000)   # Берлин 20.11 23:59:59.8
    session.add(_session_row(user.id, completed, "scored"))
    await session.commit()
    monkeypatch.setattr(SS, "utcnow", lambda: completed + timedelta(milliseconds=500))
    await update_user_activity(session, user.id, day=user_day(user, completed))
    await session.refresh(user)
    print("живой путь:", user.streak_days, user.last_active_date)

    rep = Report(show=5)
    await _check_streaks(session, rep)
    assert not rep.bad, rep.bad


async def test_admin_finished_never_exceeds_started_across_midnight(session, user):
    """Начал вчера в 23:58 UTC, закончил сегодня в 00:03 UTC."""
    from app.bot.handlers.admin import retention_today

    since = datetime.combine(utctoday(), datetime.min.time())
    session.add(QuizSession(
        user_id=user.id, level=CEFRLevel.A1, total_questions=7, answered_questions=7,
        is_completed=True, started_at=since - timedelta(minutes=2),
        completed_at=since + timedelta(minutes=3),
    ))
    await session.commit()
    started, finished, back, base = await retention_today(session)
    print("начали", started, "закончили", finished)
    assert finished <= started, (started, finished)


async def test_fire_only_for_live_streak_and_name_escaped(session):
    from app.bot.handlers.leaderboard.leaderboard_table import build_monthly_table, streaks_of
    from app.services.streak_service import user_today

    probe = User(id=1, timezone="Europe/Berlin")
    today = user_today(probe)
    gone = User(id=3001, first_name="Gone", interface_language="ru", learning_lang="de",
                native_lang="ru", streak_days=12, last_active_date=today - timedelta(days=5),
                timezone="Europe/Berlin")
    alive = User(id=3002, first_name="Alive", interface_language="ru", learning_lang="de",
                 native_lang="ru", streak_days=12, last_active_date=today - timedelta(days=1),
                 timezone="Europe/Berlin")
    tag = User(id=3003, first_name="Tom <3", interface_language="ru", learning_lang="de",
               native_lang="ru", streak_days=4, last_active_date=today, timezone="Europe/Berlin")
    session.add_all([gone, alive, tag])
    await session.commit()
    board = [
        {"rank": i + 1, "user_id": p.id, "display_name": p.display_name, "monthly_score": 100 - i}
        for i, p in enumerate([gone, alive, tag])
    ]
    streaks = await streaks_of(session, board)
    text = build_monthly_table(board, None, SimpleNamespace(month=10, year=2026), 3002, "ru",
                               streaks=streaks)
    print(text)
    assert "Gone 🔥" not in text
    assert "<b>Alive 🔥12</b>" in text
    assert "Tom &lt;3 🔥4" in text, "имя не экранировано — Telegram отвергнет HTML"

