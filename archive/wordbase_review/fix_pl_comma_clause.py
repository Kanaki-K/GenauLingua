"""СКВОЗНАЯ ПРАВКА КЛАССА: 8 польских примеров, потерявших вторую часть.

Замер в `scan_pl_comma_clause.py`. Коротко: признак структурный — в
немецком примере есть запятая, то есть он из двух частей, а в примере
одного языка запятой нет вовсе. Примета смотрит только на ru, uk и pl,
потому что у английского и турецкого отсутствие запятой — норма языка
(818 и 843 ряда соответственно, то есть две трети всех).

Из 16 попаданий половина законна: польский соединяет союзом «i»/«ani»
или сложным словом то, что немецкий разделяет запятой. Остальные восемь
правятся здесь: у них вторая часть эталона либо потеряна, либо фраза
подменена целиком.

ЧТО ЭТО ГОВОРИТ О ПРОИСХОЖДЕНИИ ПОЛЬСКИХ ПРИМЕРОВ. Три из восьми —
`entmutigen`, `kitschig`, `wegstecken` — не обрезанный перевод, а ДРУГОЕ
предложение с тем же словом: «не дай себя обескуражить первой неудачей»
вместо «его критика не должна тебя обескураживать», «фигурка на полке»
вместо «комната». Это уточняет гипотезу о польском: дело не только в
отдельном прогоне перевода, а в том, что часть польских примеров
СОЧИНЯЛИ по заголовку, не глядя на немецкую фразу.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    (7499, "example_pl",
     "Dziś jestem w pracy bardzo obciążony",
     "Dziś jestem w pracy bardzo obciążony, jest dużo do zrobienia",
     "потеряно «es gibt viel zu tun»"),
    (7978, "example_pl",
     "Ten film jest strasznie przereklamowany",
     "Uważam ten film za przereklamowany, szczerze mówiąc nie jest taki dobry",
     "потеряно «ehrlich gesagt nicht so gut», и «strasznie» в эталоне нет"),
    (8532, "example_pl",
     "Ten wazon to tylko ozdoba",
     "To tylko ozdoba, nie potrzebujemy tego",
     "потеряно «das brauchen wir nicht», и ваза в эталоне не упомянута"),
    (11122, "example_pl",
     "Ta bezsensowna kłótnia do niczego nie prowadzi",
     "Ta bezsensowna kłótnia do niczego nie prowadzi, po prostu odpuść",
     "потеряно «lass es einfach sein»"),
    (11529, "example_pl",
     "Schowaj telefon i mnie posłuchaj",
     "Schowaj telefon, teraz rozmawiamy",
     "«послушай меня» вместо «wir sprechen jetzt»"),
    (11550, "example_pl",
     "Nie daj się zniechęcić pierwszą porażką",
     "Jego krytyka nie powinna cię zniechęcać, robisz dobre postępy",
     "подмена целиком: первая неудача вместо его критики"),
    (14614, "example_pl",
     "Ta figurka na półce jest strasznie kiczowata",
     "Ten pokój jest dla mnie zbyt kiczowaty, wszędzie te tanie dekoracje",
     "подмена целиком: фигурка на полке вместо комнаты"),
    (18388, "example_pl",
     "W twoim pokoju jest istny chlew",
     "Ten pokój to istny chlew, tak bardzo jest brudny",
     "потеряно «so dreckig ist es», и «twoim» в эталоне нет"),
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
