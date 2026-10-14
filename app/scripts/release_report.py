"""
Отчёт владельцу: что дала рассылка патчноута.

    python -m app.scripts.release_report                      # показать здесь
    python -m app.scripts.release_report --to-admin           # прислать в Telegram

Зачем. «Дошло 180» ничего не говорит о том, работает ли обновление.
Работает — если люди, получившие рассылку, вернулись и занимаются. Отчёт
сравнивает это с неделей ДО рассылки и показывает, кто «проснулся» — не
занимался месяц и пришёл. Владелец, 14.10: «хочу, чтобы бот мне сделал
отчёты по этой теме после рассылки». Запускается разово через 1, 3 и 7
дней (таймеры systemd на сервере, `DEPLOY.md`).

Источники — только то, что пишется и так:
    logs/<ключ>.sent              кому дошло, кто заблокировал бота
    quiz_sessions                 занятия: начало, конец, `start_source`
                                  («release» — кнопка под рассылкой)
    quiz_questions.channel        ответы по играм: голос «s», сборка «b»
"""

from __future__ import annotations

import argparse
import asyncio
import collections
import os
import pathlib
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
os.environ.setdefault("ENV_FILE", ".env.local")

from sqlalchemy import func, select  # noqa: E402

from app.config import settings  # noqa: E402
from app.core.clock import utcnow  # noqa: E402
from app.database.models import QuizQuestion, QuizSession, User  # noqa: E402
from app.database.session import AsyncSessionLocal  # noqa: E402
from app.locales import DEFAULT_LOCALE  # noqa: E402
from app.scripts.send_release_notes import read_journal  # noqa: E402

KEY = "release_notes_2026_10"
# Рассылка 2.0 ушла 15.10.2026 в 08:00 по Берлину
SENT_AT = datetime(2026, 10, 15, 6, 0)
# «Спящий» — не занимался столько дней до рассылки
ASLEEP_DAYS = 30


@dataclass
class Report:
    since: datetime
    now: datetime
    delivered: int = 0
    blocked: int = 0
    returned: int = 0             # из получивших — начали хоть одно занятие
    finished: int = 0             # из получивших — довели хоть одно до итога
    via_button: int = 0           # начали с кнопки под рассылкой
    woke: int = 0                 # вернулись после 30+ дней тишины
    lessons: int = 0              # занятий за период у всех людей
    active_after: int = 0         # занимались после рассылки — все люди
    active_week_before: int = 0   # занимались за 7 дней ДО рассылки
    speech: tuple[int, int] = (0, 0)   # ответов голосом: всего, верно
    build: tuple[int, int] = (0, 0)    # сборок: всего, верно
    by_lang: dict[str, tuple[int, int]] = field(default_factory=dict)  # язык → (дошло, вернулись)


async def build_report(session, journal: dict[int, str], since: datetime,
                       now: datetime) -> Report:
    """Числа отчёта. Без сети и без Telegram — проверяется тестом."""
    report = Report(since=since, now=now)
    delivered = {uid for uid, outcome in journal.items() if outcome == "ok"}
    report.delivered = len(delivered)
    report.blocked = sum(1 for outcome in journal.values() if outcome == "blocked")

    rows = (await session.execute(
        select(QuizSession.user_id, QuizSession.started_at,
               QuizSession.completed_at, QuizSession.start_source)
        .where(QuizSession.started_at >= since - timedelta(days=ASLEEP_DAYS))
    )).all()

    after = [r for r in rows if r.started_at >= since]
    report.lessons = len(after)
    report.active_after = len({r.user_id for r in after})
    report.active_week_before = len({
        r.user_id for r in rows if since - timedelta(days=7) <= r.started_at < since
    })

    started = {r.user_id for r in after} & delivered
    report.returned = len(started)
    report.finished = len({r.user_id for r in after if r.completed_at} & delivered)
    report.via_button = len({r.user_id for r in after if r.start_source == "release"})
    recent_before = {r.user_id for r in rows if r.started_at < since}
    report.woke = len(started - recent_before)

    for channel, attr in (("s", "speech"), ("b", "build")):
        total, correct = (await session.execute(
            select(func.count(), func.count().filter(QuizQuestion.is_correct.is_(True)))
            .select_from(QuizQuestion)
            .join(QuizSession, QuizSession.id == QuizQuestion.session_id)
            .where(QuizQuestion.channel == channel, QuizSession.started_at >= since)
        )).one()
        setattr(report, attr, (int(total or 0), int(correct or 0)))

    langs = dict((await session.execute(
        select(User.id, User.interface_language)
        .where(User.id.in_(delivered or {-1}))
    )).all())
    by_lang: dict[str, list[int]] = collections.defaultdict(lambda: [0, 0])
    for uid in delivered:
        lang = langs.get(uid) or DEFAULT_LOCALE
        by_lang[lang][0] += 1
        if uid in started:
            by_lang[lang][1] += 1
    report.by_lang = {k: (v[0], v[1]) for k, v in sorted(by_lang.items())}
    return report


def _pct(part: int, whole: int) -> str:
    return f"{part * 100 // whole}%" if whole else "—"


def format_report(r: Report) -> str:
    """Сообщение владельцу. По-русски: это служебный отчёт, как админка."""
    days = max(0, (r.now - r.since).days)
    hours = max(0, int((r.now - r.since).total_seconds() // 3600))
    period = f"{days} дн." if days else f"{hours} ч"
    lines = [
        f"<b>Отчёт о рассылке 2.0</b> · прошло {period}",
        "",
        "<b>Охват</b>",
        f"Дошло: {r.delivered} · заблокировали бота: {r.blocked}",
        "",
        "<b>Вернулись</b>",
        f"Начали занятие: {r.returned} из {r.delivered} ({_pct(r.returned, r.delivered)})",
        f"Довели до итога: {r.finished}",
        f"С кнопки под рассылкой: {r.via_button}",
        f"Проснулись (не занимались {ASLEEP_DAYS}+ дней): {r.woke}",
        "",
        "<b>Сравнение</b>",
        f"Занимались за неделю до рассылки: {r.active_week_before}",
        f"Занимались после рассылки: {r.active_after} · занятий: {r.lessons}",
        "",
        "<b>Новые игры</b>",
        f"Голосом: {r.speech[0]} ответов, верно {r.speech[1]}",
        f"«Собираю»: {r.build[0]} сборок, верно {r.build[1]}",
    ]
    if r.by_lang:
        lines += ["", "<b>По языку интерфейса</b> (дошло → вернулись)"]
        lines += [f"{lang}: {sent} → {back}" for lang, (sent, back) in r.by_lang.items()]
    return "\n".join(lines)


async def run(args) -> int:
    journal_path = pathlib.Path(settings.LOG_DIR or "logs") / f"{args.key}.sent"
    journal = read_journal(journal_path)
    if not journal:
        print(f"журнала рассылки нет ({journal_path}) — рассылка ещё не уходила")
    async with AsyncSessionLocal() as session:
        report = await build_report(session, journal, args.since, utcnow())
    text = format_report(report)
    print(text)
    if args.to_admin:
        from aiogram import Bot
        from aiogram.client.default import DefaultBotProperties
        from aiogram.enums import ParseMode

        bot = Bot(token=settings.BOT_TOKEN,
                  default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        try:
            await bot.send_message(settings.ADMIN_USER, text)
            print("\nотправлено владельцу")
        finally:
            await bot.session.close()
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--key", default=KEY)
    ap.add_argument("--since", type=datetime.fromisoformat, default=SENT_AT,
                    help="когда ушла рассылка, UTC (по умолчанию 2026-10-15 06:00)")
    ap.add_argument("--to-admin", action="store_true", help="прислать отчёт в Telegram")
    return asyncio.run(run(ap.parse_args()))


if __name__ == "__main__":
    sys.exit(main())
