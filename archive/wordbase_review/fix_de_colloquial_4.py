"""
Четвёртый проход по разговорному усечению в НЕМЕЦКОМ ЭТАЛОНЕ: 7 ячеек.

Блок 33 показал ещё одну дырку: `Lass mich, ich zieh mir gerade einen
Film rein`. Примета искала `Ich` только с заглавной буквы, а тут «ich»
стоит посреди фразы со строчной. После `\b[Ii]ch` нашлось ещё семь
ячеек — все с `ich hab`, `ich sag`, `ich brauch`, `ich glaub`,
`ich lauf`.

Счёт по классу: 88, 15, 7, теперь 7. Четыре прохода, и каждый раз дырку
находил глаз. Это уже не случайность, а свойство работы: примета видит
ровно то, что в неё заложили, и каждый новый блок может показать, что
заложили не всё.

    python -m app.scripts.fix_de_colloquial_4            # показать
    python -m app.scripts.fix_de_colloquial_4 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# (id, колонка, что стоит сейчас, на что менять, слово ряда)
FIXES: list[tuple[int, str, str, str, str]] = [
    (7699, "example_de",
     "Das Essen war vorzüglich, ich hab es wirklich genossen",
     "Das Essen war vorzüglich, ich habe es wirklich genossen",
     "vorzüglich"),
    (10162, "example_de", "Hör mal, ich brauch deine Aufmerksamkeit",
     "Hör mal, ich brauche deine Aufmerksamkeit", "Aufmerksamkeit"),
    (10316, "example_de", "Ich schwöre dir, ich sag die Wahrheit",
     "Ich schwöre dir, ich sage die Wahrheit", "schwören"),
    (10827, "example_de",
     "Das Essen war absolut himmlisch, ich hab noch nie so gut gegessen",
     "Das Essen war absolut himmlisch, ich habe noch nie so gut gegessen",
     "himmlisch"),
    (12606, "example_de", "Mir ist schwindelig, ich hab Schwindel",
     "Mir ist schwindelig, ich habe Schwindel", "Schwindel"),
    (14149, "example_de",
     "Du redest mir immer ein, dass ich es nicht schaffe, aber ich glaub "
     "an mich",
     "Du redest mir immer ein, dass ich es nicht schaffe, aber ich glaube "
     "an mich", "einreden"),
    (18639, "example_de", "Komm, ich lauf dir hinterher!",
     "Komm, ich laufe dir hinterher!", "hinterher"),
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
