"""
Третий проход по разговорному усечению в НЕМЕЦКОМ ЭТАЛОНЕ: 7 ячеек.

Блок 29 показал ещё две дырки в примете: `Morgen reis ich ab` и
`Ich pack meine Sachen` — основ `reis` и `pack` в списке не было.
После добавления восемнадцати основ (`pack`, `reis`, `schau`, `zieh`,
`dreh`, `stell`, `steck`, `werf`, `schick`, `erzähl`, `versteh` и
дальше) нашлось ещё семь ячеек.

Это уже третий заход на один класс, и счёт идёт вниз: 88, потом 15,
теперь 7. Каждый раз дырку находил глаз, а не примета. Отсюда правило,
которое стоит в ведомости: ноль у приметы значит «того, что она умеет
видеть, больше нет».

    python -m app.scripts.fix_de_colloquial_3            # показать
    python -m app.scripts.fix_de_colloquial_3 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# (id, колонка, что стоит сейчас, на что менять, слово ряда)
FIXES: list[tuple[int, str, str, str, str]] = [
    (35, "example_de", "Ich zieh mich schnell an",
     "Ich ziehe mich schnell an", "anziehen"),
    (2190, "example_de", "Ich schau mir den Film an",
     "Ich schaue mir den Film an", "anschauen"),
    (2866, "example_de", "Ich schau mir gern die Talkshow an",
     "Ich schaue mir gern die Talkshow an", "Talkshow"),
    (6455, "example_de", "Ich versteh das nicht",
     "Ich verstehe das nicht", "verstehen"),
    (7468, "example_de", "Ich zieh Tee dem Kaffee vor",
     "Ich ziehe Tee dem Kaffee vor", "vorziehen"),
    (10163, "example_de", "Ich erzähl dir keine Geheimnisse mehr",
     "Ich erzähle dir keine Geheimnisse mehr", "Geheimnis"),
    (13815, "example_de", "Ach so, jetzt versteh ich's!",
     "Ach so, jetzt verstehe ich es!",
     "Ach — и усечение, и проглоченное «es»"),
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
