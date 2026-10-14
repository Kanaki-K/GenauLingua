"""
Пропущенный апостроф в АНГЛИЙСКИХ примерах: 6 ячеек по всей базе.

Класс нашёлся в блоке 22 (`wa's`, `doe's` — лишний апостроф) и держался
дальше в обратную сторону, с пропущенным: `maybe its there`,
`8 oclock`, `the teams mood`, `My grandpas hug`, `I'll rather stay`.
После того как эти четыре блока закрыли вручную, `scan_en_apostrophe`
прошёл по всем 12 902 английским примерам и нашёл ещё шесть.

Примета не ищет слово — она ищет слово в обстановке, где другое чтение
невозможно: `its` только перед наречием или прилагательным (`its too
bright`), а перед существительным (`its colour`) не трогает, потому что
там это настоящее притяжательное.

Первая версия приметы включила в список «несуществующих» форм `shell`
как `she'll` — и сразу ложно сработала на `The shell lay on the beach`.
Ракушка. Строка теперь постоянная запись в списке заведомо правильных.

    python -m app.scripts.fix_en_apostrophe            # показать
    python -m app.scripts.fix_en_apostrophe --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# (id, колонка, что стоит сейчас, на что менять, слово ряда)
FIXES: list[tuple[int, str, str, str, str]] = [
    (7971, "example_en", "Can you lower the blinds, its too bright",
     "Can you lower the blinds, it's too bright", "runterlassen"),
    (8176, "example_en", "The food is still steaming, its too hot",
     "The food is still steaming, it's too hot", "dampfen"),
    (10704, "example_en", "Theres great unrest in the city",
     "There's great unrest in the city", "Unruhe"),
    (18242, "example_en", "Theres a small, cute little house in the forest",
     "There's a small, cute little house in the forest", "Häuschen"),
    (18318, "example_en",
     "This is a damn backwater, theres nothing to do anywhere",
     "This is a damn backwater, there's nothing to do anywhere", "Kaff"),
    (18443, "example_en",
     "Watch out for the doorstep, otherwise youll trip",
     "Watch out for the doorstep, otherwise you'll trip", "Türschwelle"),
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
