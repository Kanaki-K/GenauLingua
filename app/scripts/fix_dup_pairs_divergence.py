"""СКВОЗНАЯ ПРАВКА: расхождение переводов внутри восьми полных дублей.

ОТКУДА ЗАМЕР. В блоке 33 попался ряд `grob` (7629) — один из восьми
полных дублей, найденных замером блока 24 («то же слово И тот же
немецкий пример»). Его английский пример говорил «That was a GROSS
insult», а у двойника (7005) стоит «a RUDE insult» — слово из списка.

То есть «полный дубль» значит совпадение заголовка и НЕМЕЦКОГО примера,
а переводы у таких рядов могут расходиться. И если расходятся — в одном
из двух может сидеть дефект, которого в другом нет.

ЗАМЕР ПО ВСЕМ ВОСЬМИ ПАРАМ. Сравнены десять ячеек (список и пример на
пяти языках) у каждой пары. **Расходятся ВСЕ ВОСЕМЬ**, от двух ячеек до
семи:

    bestimmt   (103/1269)    5 ячеек
    du         (195/1328)    2
    intern     (2582/7388)   5
    mal        (6705/13262)  7
    Dunkelheit (6716/15414)  2
    grob       (7005/7629)   4
    platzen    (7115/7195)   6
    aufrichtig (10384/11525) 3

Большинство расхождений — порядок синонимов или равноправные варианты
(«Він напевно прийде» против «Він точно прийде»), и править там нечего.
Но два расхождения оказались ДЕФЕКТАМИ, и оба нашлись только потому, что
рядом стоял верный двойник.

ПЕРВЫЙ: `platzen` (7195) противоречит сам себе по виду глагола.

Немецкий эталон «Der Ballon ist geplatzt» — совершённое действие, и все
пять примеров ряда совершенного вида: «лопнул», «лопнула», «patladı»,
«pękł». А списки в ru, uk и pl стоят в НЕСОВЕРШЕННОМ: «лопаться,
трескаться», «лопатися, тріскатися», «pękać, przebijać się». У двойника
(7115) там совершенный вид, и он верен.

Из-за этого карточка показывала «лопаться» при примере «лопнул» — то
самое расхождение §8, которое `main_meaning` исправить не может: «лопаться»
и «лопнул» совпадают на трёх буквах, а нужно четыре.

ВТОРОЙ: `aufrichtig` (11525) турецкий — подмена.

    10384 tr «Bu samimi bir özürdü»  — «это было искреннее извинение» ✓
    11525 tr «O gerçekten samimi bir özür söyledi» — «он сказал...»

Эталон говорит «Das WAR eine aufrichtige Entschuldigung», а не «кто-то
её произнёс».

ЧТО ЭТО МЕНЯЕТ ДЛЯ РЕШЕНИЯ ВЛАДЕЛЬЦА. Ничего не ломает и помогает: после
правок пары различаются только уровнем и порядком синонимов, то есть
выбор «слить или развести» становится чище. Ряды НЕ УДАЛЕНЫ и не
тронуты ни в чём, кроме названных дефектов.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ platzen (7195): список несовершенного вида при примере ══
    #    совершённого; у двойника 7115 там совершенный вид
    (7195, "translation_ru",
     "лопаться, трескаться, срываться",
     "лопнуть, треснуть, сорваться",
     "пример «лопнул» совершённого вида; у двойника 7115 так же"),
    (7195, "translation_uk",
     "лопатися, тріскатися, зриватися",
     "лопнути, тріснути, зірватися",
     "то же"),
    (7195, "translation_pl",
     "pękać, przebijać się",
     "pęknąć, przebić się",
     "то же"),

    # ══ aufrichtig (11525): турецкая подмена ════════════════════
    (11525, "example_tr",
     "O gerçekten samimi bir özür söyledi",
     "Bu samimi bir özürdü",
     "подмена: эталон «Das war eine aufrichtige Entschuldigung»"),
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
