"""ВТОРОЙ ПРОХОД, блок 46 (ряды 9001–9200): 7 правок.

ПЛОТНОСТЬ 3.5% — ВЫШЕ, ЧЕМ В БЛОКЕ 45 (0.5%), И ЭТО ВАЖНО ЗАПИСАТЬ.
Пять блоков падение шло подряд, и легко было решить, что база просто
становится чище к концу. Здесь кривая дёрнулась вверх, значит дело не в
общем «улучшении», а в том, что **дефекты сидят участками**: блок 45
попал на чистый участок, блок 46 — на участок с польскими подменами.

Четыре правки из семи польские, и среди них подмена целиком:

    Pfosten (18393) de «Der Zaun hängt schief, weil einer der Pfosten
                        verrottet ist»
                    pl «PIŁKA ODBIŁA SIĘ OD SŁUPKA»

Немецкая фраза про покосившийся забор и сгнивший столб. Польская — про
мяч, отскочивший от штанги. Это ровно та форма, что замерена в блоке 42:
польский пример СОЧИНЁН по заголовку («słupek» это и столбик, и штанга
ворот), а не переведён с немецкого.

ОСТАЛЬНОЕ — МЕЛОЧЬ ТОГО ЖЕ РАЗБОРА, что весь проход: `Synagoge` с лишним
«naszym», `Sprechanlage` с «dzwonię» вместо «drücke», `rütteln` с
«klamką» (ручка) вместо «an der Tür» (дверь), `entfallen` с «зникає»
вместо «відпадає» из своего списка, `Füller` с «dolmakalemim» в одно
слово при «dolma kalem» в списке, `Spritzer` с «biraz» вместо «birkaç
damla».
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ польский сочинил своё предложение ══════════════════════
    (18393, "example_pl",
     "Piłka odbiła się od słupka",
     "Płot jest krzywy, bo jeden ze słupków zgnił",
     "подмена целиком: мяч и штанга вместо забора и сгнившего столба"),

    # ══ добавленное и не то слово ══════════════════════════════
    (14699, "example_pl",
     "Synagoga w naszym mieście jest bardzo stara",
     "Synagoga w tym mieście jest bardzo stara",
     "«naszym» в эталоне «in der Stadt» нет"),
    (17672, "example_pl",
     "Dzwonię przez domofon i wołam dozorcę",
     "Naciskam przycisk domofonu i wołam dozorcę",
     "«dzwonię» вместо «Ich drücke auf die Sprechanlage»"),
    (8142, "example_pl",
     "Proszę nie szarpać klamką, drzwi są zamknięte",
     "Proszę nie szarpać drzwiami, są zamknięte",
     "«klamka» это ручка; в эталоне «an der Tür»"),

    # ══ вид карточки: слово не из своего списка ════════════════
    (8127, "example_uk",
     "При реструктуризації, на жаль, зникає багато робочих місць",
     "При реструктуризації, на жаль, відпадає багато робочих місць",
     "«зникає» не из списка; «відпадати» стоит в нём первым"),
    (11920, "example_tr",
     "Suya biraz limon suyu ekliyorum",
     "Suya birkaç damla limon suyu ekliyorum",
     "«biraz» не из списка; «birkaç damla» в нём первое, и так в ru, uk, pl"),

    # ══ написание внутри одного ряда ═══════════════════════════
    (9592, "example_tr",
     "Dolmakalemim boş, yeni mürekkep gerekli",
     "Dolma kalemim boş, yeni mürekkep gerekli",
     "в списке «dolma kalem» раздельно, а в примере слитно"),
]


def main() -> None:
    apply_mode = "--apply" in sys.argv
    engine = create_engine(settings.DATABASE_URL_SYNC)
    ok: list[tuple[int, str, str, str, str]] = []
    skipped: list[tuple[int, str, str | None]] = []
    seen: set[tuple[int, str]] = set()
    dupes: list[tuple[int, str]] = []
    with engine.connect() as conn:
        for wid, col, was, now, why in FIXES:
            if (wid, col) in seen:
                dupes.append((wid, col))
            seen.add((wid, col))
            cur = conn.execute(
                text(f"SELECT {col} FROM words WHERE id = :i"), {"i": wid}
            ).scalar()
            if (cur or "").strip() != was:
                skipped.append((wid, col, cur))
            else:
                ok.append((wid, col, was, now, why))

    print(f"=== правок {len(FIXES)}, совпало {len(ok)}, пропущено {len(skipped)} ===\n")
    for wid, col in dupes:
        print(f"ВНИМАНИЕ: одна ячейка правится дважды — id={wid} {col}")
    for wid, col, cur in skipped:
        print(f"ПРОПУСК id={wid} {col}: в базе {cur!r}")

    if not apply_mode:
        for wid, col, was, now, why in ok:
            print(f"id={wid} {col}")
            print(f"  было:  {was}")
            print(f"  стало: {now}")
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
