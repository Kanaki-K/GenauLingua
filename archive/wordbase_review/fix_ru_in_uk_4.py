"""Сквозная правка по примете scan_ru_in_uk, четвёртый проход.

Примета сработала после правок блоков 69–71: два ряда, где в
украинской ячейке осталось русское слово.

И одно ложное срабатывание — «на продаж» (ряд 1594). Это нормальный
украинский оборот; в белом списке приметы стоял родительный
«продажу», а именительный забыли. Добавлен туда же. Попалось оно на
МОЕЙ собственной правке из блока 69, что лишний раз показывает,
зачем сторожей прогонять после каждого блока, а не только до.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    (1212, "translation_uk",
     "гурт, музичний гурт, лента, тасьма, бинт",
     "гурт, музичний гурт, стрічка, тасьма, бинт",
     "«лента» это русское слово, по-украински «стрічка»"),
    (1313, "translation_uk",
     "удома, у себе дома",
     "удома, у себе вдома",
     "«у себе дома» — русская форма; по-украински «у себе вдома»"),
]


def main() -> None:
    apply_mode = "--apply" in sys.argv
    engine = create_engine(settings.DATABASE_URL_SYNC)
    ok: list[tuple[int, str, str, str, str]] = []
    skipped: list[tuple[int, str, str | None]] = []
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
    for wid, col, cur in skipped:
        print(f"ПРОПУСК id={wid} {col}: в базе {cur!r}")

    if not apply_mode:
        for wid, col, was, now, why in ok:
            print(f"id={wid} {col}")
            print(f"  было:  {was}")
            print(f"  стало: {now}")
            print(f"  зачем: {why}")
        print("\nсухой прогон. применить: --apply")
        return

    with engine.begin() as conn:
        for wid, col, _, now, _ in ok:
            conn.execute(
                text(f"UPDATE words SET {col} = :v WHERE id = :i"),
                {"v": now, "i": wid},
            )
    print(f"\nприменено: {len(ok)}")

    bad = 0
    with engine.connect() as conn:
        for wid, col, _, now, _ in ok:
            cur = conn.execute(
                text(f"SELECT {col} FROM words WHERE id = :i"), {"i": wid}
            ).scalar()
            if (cur or "").strip() != now:
                bad += 1
                print(f"НЕ ЗАПИСАЛОСЬ id={wid} {col}: {cur!r}")
    print(f"самопроверка: не записалось {bad}")


if __name__ == "__main__":
    main()
