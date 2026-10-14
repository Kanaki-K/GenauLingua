"""
Чужой язык внутри перевода: первый проход по всей базе.

Примета `scan_lang_leak` родилась из одного ряда блока 46
(`handhaben`: «Потрібно обережно обращаться з цими інструментами») — и
по всей базе показала ещё два, которых сорок пять блоков чтения глазами
не заметили: `всё` и `ведёт` в украинских примерах. Русская «ё»
проскакивает мимо глаза, потому что фраза вокруг украинская.

Счёт: 1 глазами, 2 приметой.

    python -m app.scripts.fix_lang_leak            # показать
    python -m app.scripts.fix_lang_leak --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

FIXES: list[tuple[int, str, str, str, str]] = [
    (11485, "example_uk",
     "Той хлопець просто халтурник, всё що він бере в руки не працює",
     "Той хлопець просто халтурник, усе, що він бере в руки, не працює",
     "русское «всё» посреди украинской фразы"),
    (18486, "example_uk",
     "Вона ведёт дуже домашній спосіб життя й рідко виходить",
     "Вона веде дуже домашній спосіб життя й рідко виходить",
     "русское «ведёт» посреди украинской фразы"),
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
