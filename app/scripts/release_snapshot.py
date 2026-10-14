# -*- coding: utf-8 -*-
"""
СЛЕПОК ТОГО, ЧТО ВЫКАТКА НЕ ИМЕЕТ ПРАВА ПОТЕРЯТЬ. Только чтение.

    python -m app.scripts.release_snapshot --out before.json
    ... выкатка ...
    python -m app.scripts.release_snapshot --out after.json --compare before.json

Люди (число и контрольная сумма их id), прогресс по словам (строки, показы,
верные, выученные), круги, ответы, баллы сезонов, награды, жалобы, словарь.
При сравнении печатает каждое число «до → после» и выходит с кодом 1, если
изменилось хоть что-то, кроме ожидаемого.

ОЖИДАЕМО МЕНЯЕТСЯ ОДНО: число включённых напоминаний (миграция
`d9a3f0c7e214` включает их всем — решение владельца). Число строк прогресса
на ПРОДЕ может уменьшиться: миграция `d7e8f9a0b1c2` схлопывает дубли слов,
но СУММЫ показов и верных обязаны сойтись до единицы — они и сверяются.

Проверено генеральной репетицией 14.10.2026 на копии прод-схемы со старым
словарём прода: всё совпало, кроме напоминаний (121 → 233).
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
os.environ.setdefault("ENV_FILE", ".env.local")

from sqlalchemy import create_engine, text  # noqa: E402

from app.config import settings  # noqa: E402

CHECKS = {
    "users": "select count(*) from users",
    "users_ids_md5": "select md5(string_agg(id::text, ',' order by id)) from users",
    "user_words_rows": "select count(*) from user_words",
    "uw_shown": "select coalesce(sum(times_shown),0) from user_words",
    "uw_correct": "select coalesce(sum(times_correct),0) from user_words",
    "uw_learned": "select count(*) from user_words where learned",
    "quiz_sessions": "select count(*) from quiz_sessions",
    "quiz_questions": "select count(*) from quiz_questions",
    "qq_correct": "select count(*) from quiz_questions where is_correct",
    "quizzes_passed": "select coalesce(sum(quizzes_passed),0) from users",
    "streak_days": "select coalesce(sum(streak_days),0) from users",
    "monthly_stats": "select count(*) from monthly_stats",
    "ms_score": "select coalesce(sum(monthly_score),0) from monthly_stats",
    "ms_quizzes": "select coalesce(sum(monthly_quizzes),0) from monthly_stats",
    "monthly_awards": "select count(*) from monthly_awards",
    "seasons": "select count(*) from monthly_seasons",
    "reports": "select count(*) from translation_reports",
    "words": "select count(*) from words",
    "reminders_on": "select count(*) from users where notifications_enabled",
}
# Что выкатка меняет НАРОЧНО (см. шапку)
EXPECTED_TO_CHANGE = {"reminders_on", "user_words_rows"}


def snapshot() -> dict:
    out = {}
    with create_engine(settings.DATABASE_URL_SYNC).connect() as c:
        for key, query in CHECKS.items():
            value = c.execute(text(query)).scalar()
            out[key] = value if isinstance(value, (int, str)) or value is None else float(value)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True)
    ap.add_argument("--compare")
    args = ap.parse_args()

    now = snapshot()
    pathlib.Path(args.out).write_text(json.dumps(now, indent=1), encoding="utf-8")
    if not args.compare:
        for key, value in now.items():
            print(f"  {key:16} {value}")
        print(f"слепок записан: {args.out}")
        return 0

    before = json.loads(pathlib.Path(args.compare).read_text(encoding="utf-8"))
    bad = []
    for key in CHECKS:
        a, b = before.get(key), now.get(key)
        mark = "  " if a == b else ("~ " if key in EXPECTED_TO_CHANGE else "≠ ")
        print(f"{mark}{key:16} {a!s:>34} -> {b}")
        if a != b and key not in EXPECTED_TO_CHANGE:
            bad.append(key)
    if bad:
        print(f"\nСТОП: изменилось то, что меняться не должно: {', '.join(bad)}")
        return 1
    print("\nвсё сохранено; изменилось только ожидаемое (~)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
