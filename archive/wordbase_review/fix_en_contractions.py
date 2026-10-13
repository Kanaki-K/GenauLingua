"""
Класс: в английских сокращениях пропал апостроф.

«Were staying overnight» вместо «We're staying», «Its getting dark»
вместо «It's getting», «Lets dig in» вместо «Let's dig in». Тринадцать
ячеек.

Это зеркало класса `fix_apostrophe_s`: там апостроф влез туда, где его
нет («wa's» вместо «was»), здесь пропал там, где он нужен. Похоже на
один и тот же сбой кавычек где-то в прогоне — он и добавлял, и терял.

**Почему «Were» нельзя править шаблоном.** «Were» — законное слово:
«Were all the students present at the lecture?» (id 6934) верно, это
прошедшее время от «to be». Отличить можно только по смыслу, поэтому
список именной, а не вычисляемый, и каждая строка прочитана.

То же про «Its»: «Its» без апострофа — притяжательное местоимение («its
colour»), и в базе оно встречается законно. В список попали только те
строки, где по смыслу нужно «It is».

    python -m app.scripts.fix_en_contractions            # показать
    python -m app.scripts.fix_en_contractions --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

_WE = "«Were» вместо «We're»: пропал апостроф"
_IT = "«Its» вместо «It's»: пропал апостроф"
_LET = "«Lets» вместо «Let's»: пропал апостроф"

# (id, колонка, что стоит сейчас, на что менять, зачем)
FIXES: list[tuple[int, str, str, str, str]] = [
    (2895, "example_en", "Were staying overnight at the lakeside hotel",
     "We're staying overnight at the lakeside hotel", _WE),
    (7820, "example_en", "Were inaugurating the new building tomorrow",
     "We're inaugurating the new building tomorrow", _WE),
    (8141, "example_en",
     "Were searching systematically for a solution to the problem",
     "We're searching systematically for a solution to the problem", _WE),
    (13563, "example_en", "Were going to dance at the festival",
     "We're going to dance at the festival", _WE),
    (15016, "example_en", "Were spending our honeymoon in Hawaii",
     "We're spending our honeymoon in Hawaii", _WE),
    (15468, "example_en", "Were taking the narrow path through the forest",
     "We're taking the narrow path through the forest", _WE),
    (17218, "example_en", "Were going overseas for two weeks of vacation",
     "We're going overseas for two weeks of vacation", _WE),
    (7918, "example_en",
     "Its hardly conceivable that he did such a thing",
     "It's hardly conceivable that he did such a thing", _IT),
    (8695, "example_en",
     "Its all the same to me whether we go now or later",
     "It's all the same to me whether we go now or later", _IT),
    (12681, "example_en", "Its like a madhouse in here",
     "It's like a madhouse in here", _IT),
    (18925, "example_en",
     "Its getting dark outside, soon it will be completely dark",
     "It's getting dark outside, soon it will be completely dark", _IT),
    (8216, "example_en", "Lets dig in and finish this task",
     "Let's dig in and finish this task", _LET),
    (8498, "example_en", "Lets set a date for our meeting",
     "Let's set a date for our meeting", _LET),
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

    print(f"=== правок {len(FIXES)}, совпало {len(ok)}, пропущено {len(skipped)} ===\n")
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
