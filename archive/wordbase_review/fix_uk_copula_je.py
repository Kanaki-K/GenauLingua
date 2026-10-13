"""Сквозная правка по примете scan_uk_copula_je.

Вся база: 8 ячеек. Везде книжная связка «є» заменена на тире или
снята — так, как эту фразу сказали бы по-украински.

Выбор между тире и простым снятием зависит от сказуемого: при
существительном ставится тире («Король — голова держави»), при
прилагательном связка просто уходит, а прилагательное переходит из
орудного в именительный («Компанія провідна в галузі»).
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    (2679, "example_uk",
     "Німеччина є членом НАТО",
     "Німеччина — член НАТО",
     "при существительном связка заменяется тире"),
    (3016, "example_uk",
     "Папір є вторсировиною",
     "Папір — вторсировина",
     "то же"),
    (7861, "example_uk",
     "Компанія є провідною в галузі",
     "Компанія провідна в галузі",
     "при прилагательном связка уходит, орудный переходит в именительный"),
    (8437, "example_uk",
     "Населення, що зростає, є викликом",
     "Населення, що зростає, — це виклик",
     "при существительном связка заменяется тире"),
    (12692, "example_uk",
     "Внутрішності є частиною травної системи",
     "Внутрішності — частина травної системи",
     "то же"),
    (13108, "example_uk",
     "Клітор є важливою частиною жіночої сексуальності",
     "Клітор — важлива частина жіночої сексуальності",
     "то же"),
    (15142, "example_uk",
     "Статевий акт є частиною стосунків",
     "Статевий акт — частина стосунків",
     "то же"),
    (16432, "example_uk",
     "Король є головою держави",
     "Король — голова держави",
     "то же"),
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
