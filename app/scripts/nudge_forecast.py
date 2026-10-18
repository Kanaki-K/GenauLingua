#!/usr/bin/env python3
"""
Кому и когда распорядитель напишет в ближайшие часы — без отправки (патч 2.1).

Урок выкатки 14.10: напоминания «догнали» 109 человек сразу после запуска,
24 заблокировали бота. Перед запуском 2.1 — посмотреть на живой базе, что
будет: тики каждые 5 минут, то же правило (`build_state` + `decide`), что и
у `send_nudges`; после «отправки» отметки человека сдвигаются в памяти, как
их сдвинул бы захват. Ничего не пишет и не отправляет.

    python -m app.scripts.nudge_forecast                 # 48 ч от сейчас
    python -m app.scripts.nudge_forecast --hours 24 --from 2026-10-16T06:00
"""
from __future__ import annotations

import argparse
import asyncio
import os
import pathlib
import sys
from collections import Counter

from datetime import datetime, timedelta

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
os.environ.setdefault("ENV_FILE", ".env.local")

from sqlalchemy import select  # noqa: E402

from app.core.clock import utcnow  # noqa: E402
from app.database.models import User  # noqa: E402
from app.database.session import AsyncSessionLocal, engine  # noqa: E402
from app.schedulers.nudges import _last_done, build_state  # noqa: E402
from app.services import nudge_plan  # noqa: E402
from app.services.nudge_plan import DAILY  # noqa: E402

TICK = timedelta(minutes=5)


async def main(args) -> int:
    start = datetime.fromisoformat(args.start) if args.start else utcnow()
    end = start + timedelta(hours=args.hours)
    async with AsyncSessionLocal() as session:
        users = (await session.execute(select(User))).scalars().all()
        done = await _last_done(session, [u.id for u in users])
    await engine.dispose()

    # Отметки, которые сдвинул бы захват: (последняя отправка, якорь, ступень)
    marks = {u.id: (u.last_notification_sent, u.nudge_anchor, u.nudge_step or 0) for u in users}
    kinds, hours, people = Counter(), Counter(), set()
    holdout = Counter()
    first_hour = Counter()
    now = start
    while now < end:
        for user in users:
            sent, anchor, step = marks[user.id]
            probe = replace_user(user, sent, anchor, step)
            state = build_state(probe, now, done.get(user.id))
            if state is None:
                continue
            decision = nudge_plan.decide(state)
            if not decision:
                continue
            kind, new_step = decision
            held = kind != DAILY and not user.notifications_enabled and nudge_plan.in_holdout(user.id)
            marks[user.id] = (sent if held else now,
                              anchor if kind == DAILY else state.anchor_day,
                              step if kind == DAILY else new_step)
            if held:
                holdout[kind] += 1
                continue
            kinds[kind] += 1
            people.add(user.id)
            hours[now.replace(minute=0, second=0, microsecond=0)] += 1
            if now - start < timedelta(hours=1):
                first_hour[kind] += 1
        now += TICK

    print(f"окно: {start:%d.%m %H:%M} — {end:%d.%m %H:%M} UTC, людей в базе: {len(users)}")
    print(f"включены напоминания: {sum(1 for u in users if u.notifications_enabled)}, "
          f"отказались: {sum(1 for u in users if u.reminders_declined_at)}")
    print(f"сообщений: {sum(kinds.values())} у {len(people)} человек; "
          f"в первый час после запуска: {sum(first_hour.values())} {dict(first_hour)}")
    print("по видам:", dict(sorted(kinds.items())))
    print("контрольная группа (не отправлено, только запись):", dict(sorted(holdout.items())))
    print("по часам:")
    for hour, n in sorted(hours.items()):
        print(f"  {hour:%d.%m %H:00} UTC  {n}")
    return 0


def replace_user(user: User, sent, anchor, step):
    """Человек с подменёнными отметками — без записи в базу."""
    class Probe:
        def __getattr__(self, name):
            return getattr(user, name)
    probe = Probe()
    probe.last_notification_sent = sent
    probe.nudge_anchor = anchor
    probe.nudge_step = step
    return probe


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--hours", type=int, default=48)
    ap.add_argument("--from", dest="start")
    sys.exit(asyncio.run(main(ap.parse_args())))
