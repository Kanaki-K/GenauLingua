"""ВТОРОЙ ПРОХОД, блок 65 (ряды 12801–12902) — ПОСЛЕДНИЙ: 3 правки.

В блоке 102 ряда, а не 200: это остаток базы. Формальных замечаний
извлекателя — НОЛЬ из 102, как и в блоке 64.

Состав: конец безрангового хвоста B1 (`Versandkosten`, `Widerrufsrecht`,
`Vollkaskoversicherung`, `Umweltschutz`, `Wiedervereinigung`), а с ряда
12872 идёт короткий «сборный» хвост — ряды с большими id, добавленные
позже и потому стоящие в самом конце: `festkleben` (8723), `Assistenz`
(9363), `IBAN` (10021), `Verspannung` (13203), `Seehund` (15888),
`Zulassungsstelle` (17012), `Monatsmiete` (18498), `Unglückstag`
(18963). Этот хвост чистый — в нём не нашлось ни одной правки.

ТРИ ПРАВКИ:

 • `zustellen` (3076) uk «Пошта доставляє посилку ЗА ДВА ДНІ» — срок
   выдуман: его нет ни в немецком «Die Post stellt das Paket zu», ни в
   остальных четырёх языках. Лишний факт в учебной фразе хуже, чем
   неточность: человек запоминает его как часть примера.
 • `Torwart/in` (2879) pl «Bramkarz broni PIŁKĘ» — винительный падеж при
   `bronić`, который требует родительного. Норма базы единогласна (см.
   ниже), и 2879 — единственный выброс из десяти.
 • `Anzeigetafel` (17438) ru список «табло, информационное табло, СЧЁТНОЕ
   ТАБЛО». «Счётное» по-русски значит «считающее» (счётное устройство),
   а нужно «показывающее счёт». Ближайший сосед говорит ровно это: uk
   «табло результатів». Согласны и en «scoreboard», tr «skorbord», pl
   «tablica wyników».

════════════════════════════════════════════════════════════════════════
НОРМА БАЗЫ: `bronić` + РОДИТЕЛЬНЫЙ, ДЕВЯТЬ РЯДОВ ПРОТИВ ОДНОГО
════════════════════════════════════════════════════════════════════════

    Löwin (15830)            broniła swoich MŁODYCH
    verteidigen (15974)      bronić swojego ZDANIA
    Republikaner (16342)     bronił swoich PRZEKONAŃ
    Kommunist (16357)        bronił swojej IDEOLOGII
    Unzucht (16526)          bronił swojego KLIENTA
    Strafverteidiger (16967) bronił swojego KLIENTA
    vertreten (6812)         список: «bronić POGLĄDU»
    Torwart/in (2879)        broni PIŁKĘ          ← единственный выброс

Правка написана не «broni piłki», а «ŁAPIE piłkę», и вот почему.
Падеж — настоящий дефект, но «bronić piłki» лишь грамматично: польский
комментатор скажет «bramkarz obronił strzał» или просто «broni», а
«broni piłki» в живой речи не звучит. Немецкое «hält den Ball» это
«держит/ловит мяч», и ровно так говорят оба соседних языка: ru «ловит
мяч», uk «ловить м'яч». «Łapie piłkę» — винительный с `łapać` верен, и
фраза та же, что у соседей. Правило 1q: норма базы указала на дефект, а
живой язык выбрал формулировку.

════════════════════════════════════════════════════════════════════════
СЛЕПОЕ МЕСТО ГЕЙТА №2, И ПОЧЕМУ ОНО НЕ ЗАКРЫВАЕТСЯ ПРИМЕТОЙ
════════════════════════════════════════════════════════════════════════

`zustellen` навёл на вопрос: `scan_number_mismatch` (гейт №2) сверяет
числа, НО начинается с «если в немецком цифр нет — ряд пропускается».
Значит число, ВЫДУМАННОЕ переводом на пустом месте, гейт не видит.
Проверено на самом ряде: «за два дні» он пропускает.

Замерить это приметой не удалось, и это стоит записать как результат.

  Попытка 1 — цифры и числа словами, шесть языков: **1162 попадания**.
  Причина: «bir» по-турецки и «один» по-русски — неопределённый артикль,
  а не число («Bir mektup yazıyorum» = «Ich schreibe einen Brief»).
  Заодно мой же регексп не узнал немецкое «einEN» из-за границы слова.

  Попытка 2 — только числа от двух и выше: **589 попаданий**, и опять
  мусор: русская приставка «пол-» съедает «полон», «полиции»,
  «половине», «положительно», «полке», «политике».

  Попытка 3 — ТОЛЬКО ЦИФРЫ: **4 попадания, все законные.** Три раза
  турецкое «24 saat» на немецкое «rund um die Uhr» (`Redaktion` 14607,
  `Bewachung` 16609, `Überwachung` 17527) и `Quadratmeter` (18383), где
  немецкое «fünfzig» написано словом, а русское «50» цифрой — это первый
  же разобранный случай в докстринге самого гейта №2.

Вывод: в ЦИФРОВОЙ форме слепое место гейта пусто — база в этом месте
чиста. В СЛОВЕСНОЙ форме примета неизмерима: числительные в шести языках
совпадают с артиклями и с частыми приставками, и правило 1s («дало
тысячу попаданий — значит признак назван неверно») тут упирается в то,
что сузить его дальше нечем. **Единственный найденный случай найден
глазом, и примету для него писать нельзя.** Поэтому новый гейт не
добавляется, а класс закрывается замером и этой записью.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    (3076, "example_uk",
     "Пошта доставляє посилку за два дні",
     "Пошта доставляє посилку",
     "срок «за два дні» выдуман: его нет ни в немецком, ни в "
     "остальных четырёх языках"),
    (2879, "example_pl",
     "Bramkarz broni piłkę",
     "Bramkarz łapie piłkę",
     "`bronić` требует родительного, а стоял винительный; норма базы — "
     "девять рядов с родительным. Формулировка по соседям: ru «ловит "
     "мяч», uk «ловить м'яч»"),
    (17438, "translation_ru",
     "табло, информационное табло, счётное табло",
     "табло, информационное табло, табло результатов",
     "«счётное» значит «считающее», а нужно «показывающее счёт»; "
     "uk «табло результатів», en «scoreboard», pl «tablica wyników»"),
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
