"""
Второй проход по английскому апострофу: 2 ячейки.

В блоке 30 глазами нашлось `On Valentines Day people give flowers` —
притяжательное в названии праздника. Примета `scan_en_apostrophe` его
не видела: она искала только общие слова вроде `its` и `theres`.
После добавления правила про праздники нашлись ещё две ячейки, обе про
`New Years Eve`.

Это третий класс, где расширение приметы дало добавку, и картина та же:
ноль у приметы означает «того, что она умеет видеть, больше нет».

    python -m app.scripts.fix_en_apostrophe_2            # показать
    python -m app.scripts.fix_en_apostrophe_2 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# (id, колонка, что стоит сейчас, на что менять, слово ряда)
FIXES: list[tuple[int, str, str, str, str]] = [
    (12177, "example_en",
     "The fireworks on New Years Eve were very beautiful",
     "The fireworks on New Year's Eve were very beautiful", "Feuerwerk"),
    (12393, "example_en",
     "The fireworks on New Years Eve were particularly loud",
     "The fireworks on New Year's Eve were particularly loud",
     "Feuerwerkskörper"),
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
