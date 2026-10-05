"""
Восьмой проход по разговорному усечению в немецком эталоне — на этот раз
по правилу обязательного «-e».

Блок 53 дал `Bitte betätig den Knopf`. Семь прошлых проходов искали
усечение по шаблонам («Ich <основа>», инверсия, проглоченное `es`,
`is`/`-n»), а этот ищет по правилу орфографии: у слабых глаголов с
основой на `-t`, `-d`, `-ig`, `-n` формы без `-e` просто не существует.
Правило решаемое, догадываться не нужно.

По базе примета нашла ещё один ряд, которого не видела ни одна прежняя:
`Ich send die Ware zurück`. Основы `send` в списке scan_de_colloquial
не было, и `send` не похоже ни на `es`, ни на `is`.

Счёт проходов: 88, 15, 7, 7, 2, 1, 4, 1.

    python -m app.scripts.fix_de_imperative            # показать
    python -m app.scripts.fix_de_imperative --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

FIXES: list[tuple[int, str, str, str, str]] = [
    (3063, "example_de", "Ich send die Ware zurück",
     "Ich sende die Ware zurück",
     "у основы на «-d» нужно «-e»"),
]


def main() -> None:
    apply_mode = "--apply" in sys.argv
    engine = create_engine(settings.DATABASE_URL_SYNC)

    ok, skipped = [], []
    with engine.connect() as conn:
        for wid, col, was, now, why in FIXES:
            cur = conn.execute(
                text(f"SELECT {col} FROM words WHERE id = :i"), {"i": wid}
            ).scalar()
            if (cur or "").strip() != was:
                skipped.append((wid, col, cur))
            else:
                ok.append((wid, col, was, now, why))

    print(f"=== правок {len(FIXES)}, совпало {len(ok)}, "
          f"пропущено {len(skipped)} ===\n")
    for wid, col, was, now, why in ok:
        print(f"  {wid} {col} — {why}")
        print(f"      было:  {was!r}")
        print(f"      стало: {now!r}")
    for wid, col, cur in skipped:
        print(f"  ПРОПУЩЕНО {wid} {col}: {cur!r}")

    if not apply_mode:
        print("\nэто показ. Для применения — флаг --apply")
        return

    with engine.begin() as conn:
        for wid, col, _, now, _ in ok:
            conn.execute(text(f"UPDATE words SET {col} = :v WHERE id = :i"),
                         {"v": now, "i": wid})
    print(f"\nприменено: {len(ok)}")

    with engine.connect() as conn:
        bad = 0
        for wid, col, _, now, _ in ok:
            cur = conn.execute(text(f"SELECT {col} FROM words WHERE id = :i"),
                               {"i": wid}).scalar()
            if (cur or "").strip() != now:
                print(f"  ТРЕВОГА: {wid} {col} не записалось")
                bad += 1
        print(f"самопроверка: не записалось {bad}")


if __name__ == "__main__":
    main()
