# -*- coding: utf-8 -*-
"""
Серия, заморозка, учёт — перебор (аудит 2.1, после смены пояса расходились 503 истории из 1971).

Живой путь — `register_activity` на каждом зачётном занятии, в порядке
занятий. Восстановление — то, что делают `audit_accounting._check_streaks`
и `repair_accounting.repair_user_totals`: множество дней `user_day` по
`completed_at`, затем `advance` по отсортированным дням.

Тысячи случайных историй: пропуски 1/2/3+ дней, повторные пропуски,
несколько занятий в день, занятия у полуночи, пояса от −11 до +14,
переход на зимнее время, дни до LOCAL_DAYS_FROM/FREEZE_FROM и после,
повторы ошибок и брошенные занятия (ни живой путь, ни история их не берут).
"""
from __future__ import annotations

import random
from datetime import date, datetime, timedelta, timezone
from typing import Optional
from zoneinfo import ZoneInfo

import pytest

from app.database.models import User
from app.services.streak_service import (
    FREEZE_FROM, LOCAL_DAYS_FROM, advance, current_streak, lesson_day, register_activity, user_day,
)

ZONES = [
    ("Europe/Berlin", None), ("Asia/Tokyo", None), ("America/Los_Angeles", None),
    ("Asia/Kolkata", None), ("Pacific/Kiritimati", None), ("Pacific/Pago_Pago", None),
    (None, "+03:00"), (None, "-05:30"), (None, None),
]


def _person(tz, offset) -> User:
    p = User(id=1, first_name="X", interface_language="ru", learning_lang="de",
             native_lang="ru", reverse_mode=False)
    p.timezone = tz
    p.utc_offset = offset
    p.streak_days = 0
    p.best_streak_days = 0
    p.last_active_date = None
    p.streak_freeze_on = None
    return p


def _zone(tz, offset):
    if tz:
        return ZoneInfo(tz)
    if offset:
        sign = -1 if offset[0] == "-" else 1
        h, m = offset[1:].split(":")
        return timezone(sign * timedelta(hours=int(h), minutes=int(m)))
    return ZoneInfo("Europe/Berlin")


def random_history(rng: random.Random, tz, offset) -> list[tuple[datetime, str]]:
    """[(момент UTC наивный, вид)] — вид: scored / repeat / abandoned."""
    zone = _zone(tz, offset)
    start = date(2026, 10, 1) + timedelta(days=rng.randint(0, 60))
    out = []
    day = start
    for _ in range(rng.randint(1, 45)):
        # шаг до следующего дня занятий: 1 (подряд) чаще, 2 (один пропуск), 3+
        day += timedelta(days=rng.choice([1, 1, 1, 1, 2, 2, 3, 8]))
        for _ in range(rng.choice([1, 1, 1, 2, 3])):
            kind = rng.choice(["near_midnight", "late", "early", "any"])
            if kind == "near_midnight":
                local = datetime.combine(day, datetime.min.time()) + timedelta(
                    seconds=rng.choice([-1, -30, 0, 1, 30, 600, -600]))
            elif kind == "late":
                local = datetime.combine(day, datetime.min.time()) + timedelta(hours=23, minutes=rng.randint(0, 59))
            elif kind == "early":
                local = datetime.combine(day, datetime.min.time()) + timedelta(minutes=rng.randint(0, 90))
            else:
                local = datetime.combine(day, datetime.min.time()) + timedelta(minutes=rng.randint(0, 1439))
            moment = local.replace(tzinfo=zone).astimezone(timezone.utc).replace(tzinfo=None)
            out.append((moment, rng.choice(["scored"] * 8 + ["repeat", "abandoned"])))
    out.sort()
    return out


def live(person: User, history) -> User:
    for moment, kind in history:
        if kind != "scored":
            continue  # повтор ошибок не зовёт update_user_activity; брошенное не завершается
        register_activity(person, today=user_day(person, moment))
    return person


def audit_replay(person: User, history):
    """Копия цикла `audit_accounting._check_streaks`."""
    active = {user_day(person, m) for m, k in history if k == "scored"}
    streak, last, freeze = 0, None, None
    for day in sorted(active):
        streak, freeze, _ = advance(streak, last, day, freeze)
        last = day
    return streak, last, freeze


def repair_replay(person: User, history):
    """Копия цикла `repair_accounting.repair_user_totals` (с лучшей серией)."""
    dates = sorted({user_day(person, m) for m, k in history if k == "scored"})
    if not dates:
        return None
    best = run = 1
    freeze = None
    for before, after in zip(dates, dates[1:]):
        run, freeze, _ = advance(run, before, after, freeze)
        best = max(best, run)
    return run, dates[-1], freeze, max(run, best)


@pytest.mark.parametrize("seed", range(5))
def test_live_equals_history_fixed_zone(seed):
    rng = random.Random(seed)
    bad = []
    freezes = 0
    for i in range(2000):
        tz, offset = rng.choice(ZONES)
        history = random_history(rng, tz, offset)
        person = live(_person(tz, offset), history)
        got = (int(person.streak_days or 0), person.last_active_date, person.streak_freeze_on)
        want = audit_replay(person, history)
        rep = repair_replay(person, history)
        freezes += person.streak_freeze_on is not None
        if rep is None:
            assert got == (0, None, None)
            continue
        if got != want or got != rep[:3] or int(person.best_streak_days) != rep[3]:
            bad.append((i, tz, offset, got, want, rep, person.best_streak_days))
    assert freezes > 100, "перебор не дошёл до заморозки"
    assert not bad, bad[:5]


def test_current_streak_alive_iff_next_lesson_would_continue():
    """«Живая» серия (🔥 в рейтинге, домашний экран) ⇔ занятие сегодня её продолжит."""
    rng = random.Random(42)
    bad = []
    for _ in range(3000):
        tz, offset = rng.choice(ZONES)
        person = live(_person(tz, offset), random_history(rng, tz, offset))
        if not person.last_active_date:
            continue
        for ahead in range(1, 10):
            today = person.last_active_date + timedelta(days=ahead)
            shown = current_streak(person, today)
            nxt = advance(person.streak_days, person.last_active_date, today, person.streak_freeze_on)[0]
            continues = nxt == person.streak_days + 1
            if (shown > 0) != continues or (shown and shown != person.streak_days):
                bad.append((person.streak_days, person.last_active_date, person.streak_freeze_on, today, shown, nxt))
    assert not bad, bad[:5]


# ---------------------------------------------------------------------------
# Заданные последовательности (дни после FREEZE_FROM)
# ---------------------------------------------------------------------------

def _days_run(offsets: list[int], base: date = date(2026, 11, 2)):
    streak, last, freeze = 0, None, None
    trace = []
    for off in offsets:
        today = base + timedelta(days=off)
        streak, freeze, used = advance(streak, last, today, freeze)
        last = today
        trace.append((streak, used))
    return trace


def test_freeze_sequences():
    # один пропуск → прощён, серия +1 (пропущенный день не засчитан)
    assert _days_run([0, 1, 3]) == [(1, False), (2, False), (3, True)]
    # пропуск 2 дней → заново
    assert _days_run([0, 1, 4])[-1] == (1, False)
    # два пропуска через день: второй в пределах недели → заново
    assert _days_run([0, 2, 4]) == [(1, False), (2, True), (1, False)]
    # следующий пропуск ровно через 7 дней после заморозки → прощён
    assert _days_run([0, 2, 3, 4, 5, 6, 7, 9])[-1] == (8, True)
    # через 6 → не прощён
    assert _days_run([0, 2, 3, 4, 5, 6, 8])[-1] == (1, False)
    # до FREEZE_FROM пропуск рвёт
    before = FREEZE_FROM - timedelta(days=3)
    assert _days_run([0, 2], base=before)[-1] == (1, False)
    # первый день, когда заморозка действует, — сам FREEZE_FROM
    assert _days_run([0, 2], base=FREEZE_FROM - timedelta(days=2))[-1] == (2, True)


# ---------------------------------------------------------------------------
# ДЕФЕКТ-КАНДИДАТ: смена пояса. Живой путь считает день по поясу НА МОМЕНТ
# занятия, восстановление — по НЫНЕШНЕМУ поясу человека для всей истории.
# ---------------------------------------------------------------------------

def _live_with_days(person, history, switch=None):
    """Живой путь как в боте: день занятия — `lesson_day`, он же пишется в занятие."""
    stored = []
    for j, (moment, kind) in enumerate(history):
        if switch and j == switch[0]:
            person.timezone, person.utc_offset = switch[1]
        if kind != "scored":
            continue
        day = lesson_day(person, moment)
        stored.append(day)
        register_activity(person, today=day)
    return stored


def _replay_days(days):
    streak, last, freeze = 0, None, None
    for day in sorted(set(days)):
        streak, freeze, _ = advance(streak, last, day, freeze)
        last = day
    return streak, last, freeze


def test_tz_change_live_vs_history():
    """Токио → Лос-Анджелес. Занятия 21.11 (Токио), 21.11 и 22.11 по Л-А."""
    person = _person("Asia/Tokyo", None)
    history = [(datetime(2026, 11, 20, 16, 0), "scored"),
               (datetime(2026, 11, 21, 21, 0), "scored"),
               (datetime(2026, 11, 22, 21, 0), "scored")]
    stored = _live_with_days(person, history, switch=(1, ("America/Los_Angeles", None)))
    got = (person.streak_days, person.last_active_date, person.streak_freeze_on)
    assert got == _replay_days(stored)


def test_tz_change_west_does_not_move_last_day_back():
    """Последний день не уезжает назад, и тот же день не засчитывается дважды."""
    person = _person("Asia/Tokyo", None)
    history = [(datetime(2026, 11, 19, 16, 0), "scored"), (datetime(2026, 11, 20, 16, 0), "scored"),
               (datetime(2026, 11, 21, 4, 0), "scored"), (datetime(2026, 11, 21, 21, 0), "scored")]
    stored = _live_with_days(person, history, switch=(2, ("America/Los_Angeles", None)))
    assert stored[2] >= date(2026, 11, 21), stored
    assert person.streak_days == 2, person.streak_days


@pytest.mark.parametrize("seed", range(2))
def test_live_equals_history_with_tz_change(seed):
    """Человек раз поменял пояс: живая серия = восстановление по записанным дням."""
    rng = random.Random(1000 + seed)
    bad, total, example = 0, 0, None
    for _ in range(2000):
        (tz1, off1), (tz2, off2) = rng.sample(ZONES, 2)
        history = random_history(rng, tz1, off1)
        if len(history) < 2:
            continue
        person = _person(tz1, off1)
        stored = _live_with_days(person, history,
                                 switch=(rng.randint(1, len(history) - 1), (tz2, off2)))
        total += 1
        got = (int(person.streak_days or 0), person.last_active_date, person.streak_freeze_on)
        want = _replay_days(stored) if stored else (0, None, None)
        if got != want:
            bad += 1
            example = example or (tz1, tz2, got, want)
    assert bad == 0, f"{bad} из {total}; пример {example}"


def test_praise_freeze_and_milestone_same_day():
    """Заморозка довела серию до 7: что видит человек (наблюдение, не дефект)."""
    from app.services.praise_service import RoundFacts, build_lines, pick_event

    facts = RoundFacts(rounds_total=20, streak_days=7, best_streak=7,
                       first_round_today=True, freeze_used_today=True)
    print(build_lines(facts, "ru"))
    assert pick_event(facts)[0] == "praise_freeze_saved"   # рубеж 7 не прозвучит никогда
    second = RoundFacts(rounds_total=21, streak_days=7, best_streak=7,
                        first_round_today=False, freeze_used_today=True)
    assert pick_event(second) is None or pick_event(second)[0] not in (
        "praise_freeze_saved", "praise_streak_7")
