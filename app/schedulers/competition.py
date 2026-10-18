"""
Сообщения соревнования: «Вас обогнали» и финишная прямая (17.10, REWARDS.md §Ж, З).

ЧАСТЬ РАСПОРЯДИТЕЛЯ, А НЕ ВТОРОЙ ОТПРАВИТЕЛЬ. Решает и шлёт `nudges.send_nudges`
на том же тике и в том же бюджете (`nudge_plan.may_send`: ≤1 в день, ≥12 ч
между): сообщение соревнования ЗАМЕНЯЕТ напоминание этого дня, а не
добавляется к нему.

Кому:
  * только включившим напоминания и без отказа — остальным бот не пишет
    по своей инициативе ничего, кроме лесенки возврата;
  * только днём (9–22 по часам человека);
  * контрольная группа (`in_holdout`) получает запись `holdout`, не сообщение;
  * «обогнали» — в первой десятке месяца, не позже суток после обгона, про
    одного соперника не чаще раза в 3 дня;
  * финишная прямая — за 3 дня до конца месяца, местам 4–10, раз в месяц.

ВЫКЛЮЧЕНО (`COMPETITION_NUDGES`), пока владелец не скажет «отправляй».
"""
from __future__ import annotations

import calendar
import html
import logging
from datetime import datetime, timedelta
from typing import Optional

from aiogram.exceptions import TelegramForbiddenError
from sqlalchemy import func, select, update

from app.database.models import NudgeLog, User
from app.services import nudge_plan
from app.services.nudge_plan import NudgeState

logger = logging.getLogger(__name__)

OVERTAKEN = "overtaken"
FINISH = "finish"
OVERTAKEN_FRESH = timedelta(hours=24)
SAME_RIVAL_PAUSE = timedelta(days=3)
FINISH_DAYS = 3
TOP = 10
MEDAL_PLACES = 3


def enabled() -> bool:
    from app.config import settings

    return bool(getattr(settings, "COMPETITION_NUDGES", False))


def _daytime(state: NudgeState) -> bool:
    return nudge_plan.DAY_STARTS <= state.now_local.time() < nudge_plan.DAY_ENDS


async def plan(session, users: list[User], states: dict[int, NudgeState],
               now: datetime) -> dict[int, tuple[str, dict]]:
    """{user_id: (вид, данные)} — кому сейчас сообщение соревнования."""
    from app.services.monthly_leaderboard_service import (
        ALL_LANGS, get_current_season, get_monthly_leaderboard,
    )

    if not enabled():
        return {}
    season = await get_current_season(session)
    if season is None:
        return {}
    board = await get_monthly_leaderboard(session, season_id=season.id, limit=TOP,
                                          learning_lang=ALL_LANGS)
    by_id = {e["user_id"]: e for e in board}
    last_day = calendar.monthrange(season.year, season.month)[1]
    out: dict[int, tuple[str, dict]] = {}

    for user in users:
        state = states.get(user.id)
        if state is None or not user.notifications_enabled or state.declined:
            continue
        if not nudge_plan.may_send(state) or not _daytime(state):
            continue
        mine = by_id.get(user.id)
        if mine is None:
            continue

        if user.overtaken_by_id and user.overtaken_at and now - user.overtaken_at < OVERTAKEN_FRESH:
            rival = by_id.get(user.overtaken_by_id)
            recent = (await session.execute(
                select(func.count()).select_from(NudgeLog).where(
                    NudgeLog.user_id == user.id, NudgeLog.kind == OVERTAKEN,
                    NudgeLog.situation == f"r:{user.overtaken_by_id}",
                    NudgeLog.sent_at > now - SAME_RIVAL_PAUSE,
                ))).scalar() or 0
            if rival and not recent:
                out[user.id] = (OVERTAKEN, {"mine": mine, "rival": rival})
                continue

        days_left = last_day - now.day + 1 if (now.year, now.month) == (season.year, season.month) else 0
        if 0 < days_left <= FINISH_DAYS and MEDAL_PLACES < mine["rank"] <= TOP:
            month_start = datetime(season.year, season.month, 1)
            already = (await session.execute(
                select(func.count()).select_from(NudgeLog).where(
                    NudgeLog.user_id == user.id, NudgeLog.kind == FINISH,
                    NudgeLog.sent_at >= month_start,
                ))).scalar() or 0
            third = next((e for e in board if e["rank"] == MEDAL_PLACES), None)
            if not already and third:
                out[user.id] = (FINISH, {"mine": mine, "third": third, "days": days_left})
    return out


def _text(kind: str, data: dict, lang: str) -> str:
    from app.locales import get_text, plural
    from app.services.standing import clean_name

    mine = data["mine"]
    rank = mine["rank"]
    if kind == OVERTAKEN:
        rival = data["rival"]
        name = html.escape(clean_name(rival["display_name"]))
        gap = plural(max(0, rival["monthly_score"] - mine["monthly_score"]), "plural_points", lang)
        return get_text("nd_overtaken", lang, rank=rank, name=name, gap=gap)
    gap = plural(max(0, data["third"]["monthly_score"] - mine["monthly_score"]), "plural_points", lang)
    days = plural(data["days"], "plural_days", lang)
    return get_text("nd_finish", lang, days=days, rank=rank, gap=gap)


async def deliver(bot, session, user: User, state: NudgeState, kind: str, data: dict,
                  now: datetime) -> Optional[str]:
    """Захват бюджета, отправка, журнал. Возвращает исход."""
    from app.schedulers.nudges import keyboard

    situation = f"r:{user.overtaken_by_id}" if kind == OVERTAKEN else "medal"
    clear = {"overtaken_by_id": None, "overtaken_at": None} if kind == OVERTAKEN else {}

    if nudge_plan.in_holdout(user.id):
        # Контрольная группа: решение в журнал, сообщения нет, бюджет не тратится
        if clear:
            await session.execute(update(User).where(User.id == user.id).values(**clear))
        session.add(NudgeLog(user_id=user.id, kind=kind, situation=situation,
                             outcome="holdout", sent_at=now))
        await session.commit()
        return "holdout"

    previous = user.last_notification_sent
    claimed = (await session.execute(
        update(User).where(
            User.id == user.id,
            User.last_notification_sent.is_not_distinct_from(previous),
        ).values(last_notification_sent=now, **clear).returning(User.id)
    )).scalar()
    await session.commit()
    if claimed is None:
        return None

    lang = user.interface_language or "ru"
    try:
        await bot.send_message(user.id, _text(kind, data, lang), parse_mode="HTML",
                               reply_markup=keyboard(lang, kind, True, state.now_local))
        outcome = "sent"
    except TelegramForbiddenError:
        await session.execute(update(User).where(User.id == user.id).values(
            notifications_enabled=False, reminders_declined_at=now))
        outcome = "forbidden"
    except Exception:
        logger.exception("сообщение %s не ушло (%s)", kind, user.id)
        outcome = "failed"
    session.add(NudgeLog(user_id=user.id, kind=kind, situation=situation,
                         outcome=outcome, sent_at=now))
    await session.commit()
    return outcome
