#!/usr/bin/env python3
"""
Путь человека за день — по порядку, из журнала и занятий (патч 2.1).

Владелец 16.10: «мы должны иметь возможность разбирать весь путь, чтобы
быть лучше после анализа». Разбор 15.10 восстанавливал путь польского
новичка по косвенным признакам; теперь это одна команда:

    python -m app.scripts.journey --user 25d251 --day 2026-10-15
    python -m app.scripts.journey --day 2026-10-15            # все за день, кратко

`--user` — номер Telegram или первые 6 знаков md5 номера (как в отчётах:
номера людей в отчёты не попадают). День — по Берлину. Только чтение.
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import os
import pathlib
import sys
from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
os.environ.setdefault("ENV_FILE", ".env.local")

from sqlalchemy import select  # noqa: E402

from app.database.models import QuizQuestion, QuizSession, User, UserEvent, Word  # noqa: E402
from app.database.session import AsyncSessionLocal, engine  # noqa: E402

BERLIN = ZoneInfo("Europe/Berlin")


def short(user_id: int) -> str:
    return hashlib.md5(str(user_id).encode()).hexdigest()[:6]


def local(moment: datetime) -> str:
    return moment.replace(tzinfo=timezone.utc).astimezone(BERLIN).strftime("%H:%M:%S")


def day_bounds(day: date) -> tuple[datetime, datetime]:
    start = datetime.combine(day, time(0), tzinfo=BERLIN).astimezone(timezone.utc).replace(tzinfo=None)
    return start, start + timedelta(days=1)


async def resolve(session, token: str) -> list[int]:
    if token.isdigit():
        return [int(token)]
    ids = (await session.execute(select(User.id))).scalars().all()
    return [i for i in ids if short(i).startswith(token)]


async def journey(session, user_id: int, start: datetime, end: datetime) -> list[str]:
    rows: list[tuple[datetime, str]] = []
    words = {}

    async def word_text(word_id):
        if word_id and word_id not in words:
            w = await session.get(Word, word_id)
            words[word_id] = w.word_de if w else f"#{word_id}"
        return words.get(word_id, "")

    for e in (await session.execute(select(UserEvent).where(
            UserEvent.user_id == user_id, UserEvent.at >= start, UserEvent.at < end)
            .order_by(UserEvent.at, UserEvent.id))).scalars():
        extra = ""
        if e.kind == "question":
            extra = f"вопрос {e.data.get('n')}/{e.data.get('total')} · {e.channel} · {await word_text(e.word_id)}"
        elif e.kind == "speech":
            d = e.data or {}
            extra = (f"голос, попытка {d.get('attempt')} → {e.action} · услышано «{d.get('heard', '')}» "
                     f"(похожесть {d.get('similarity')}, распознавание {d.get('recognize_s')} с) · "
                     f"{await word_text(e.word_id)}")
        elif e.kind == "skip":
            extra = f"пропуск ({e.action}) · {await word_text(e.word_id)}"
        else:
            extra = f"{e.action or ''} · {e.ms} мс"
        rows.append((e.at, f"{e.kind:8} {extra}"))

    for s in (await session.execute(select(QuizSession).where(
            QuizSession.user_id == user_id, QuizSession.started_at >= start,
            QuizSession.started_at < end))).scalars():
        rows.append((s.started_at, f"ЗАНЯТИЕ  начато · {s.total_questions} вопросов · дверь {s.start_source}"))
        if s.completed_at:
            rows.append((s.completed_at, f"ЗАНЯТИЕ  закончено · верно {s.correct_answers}/{s.answered_questions}"))
        elif s.exit_reason:
            rows.append((s.started_at, f"ЗАНЯТИЕ  ({s.exit_reason} после {s.answered_questions} ответов)"))

    for q in (await session.execute(select(QuizQuestion).join(
            QuizSession, QuizSession.id == QuizQuestion.session_id).where(
            QuizSession.user_id == user_id, QuizQuestion.answered_at >= start,
            QuizQuestion.answered_at < end))).scalars():
        mark = "✓" if q.is_correct else "✗"
        rows.append((q.answered_at, f"ОТВЕТ    {mark} {q.channel} · {await word_text(q.word_id)} · "
                                    f"«{q.user_answer or ''}» · {q.response_time_seconds} с"))
    rows.sort(key=lambda r: r[0])
    return [f"{local(at)}  {text}" for at, text in rows]


async def main(args) -> int:
    day = date.fromisoformat(args.day)
    start, end = day_bounds(day)
    async with AsyncSessionLocal() as session:
        if args.user:
            ids = await resolve(session, args.user)
            if not ids:
                print("человек не найден")
                return 1
        else:
            ids = sorted(set((await session.execute(select(UserEvent.user_id).where(
                UserEvent.at >= start, UserEvent.at < end))).scalars()) | set(
                (await session.execute(select(QuizSession.user_id).where(
                    QuizSession.started_at >= start, QuizSession.started_at < end))).scalars()))
        for user_id in ids:
            print(f"\n===== {short(user_id)} · {day}")
            for line in await journey(session, user_id, start, end):
                print(line)
    await engine.dispose()
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--user")
    ap.add_argument("--day", default=str(date.today()))
    sys.exit(asyncio.run(main(ap.parse_args())))
