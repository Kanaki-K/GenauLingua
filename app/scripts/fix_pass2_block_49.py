"""ВТОРОЙ ПРОХОД, блок 49 (ряды 9601–9800): 7 правок.

ШЕСТОЙ СЛУЧАЙ, КОГДА ВИНОВАТ НЕМЕЦКИЙ ЭТАЛОН:

    würdevoll (11346) de «Er TRUG SICH würdevoll aus dem Saal HINAUS,
                          ohne zu murren»

«sich hinaustragen» значит «вынести себя наружу» — для человека, который
просто вышел, это не по-немецки. Все пять переводов говорят «вышел из
зала достойно», то есть переводчики передали ЗАМЫСЕЛ, а не эту фразу. И
снова придраться не к чему ни в одном переводе: дефект один, в эталоне.
Правка «Er verließ den Saal würdevoll» оставляет все пять верными.

ДО ЭТОГО ЭТАЛОН БЫЛ ВИНОВАТ ПЯТЬ РАЗ: `Arche`, `Güte`, `Zünder`,
`verfehlen`, `zurückdrehen` (блок 47). Держится около одного случая на
десять блоков.

ОДИН РЯД ПРОТИВ СВОИХ ВОСЬМИ БЛИЗНЕЦОВ:

    trödeln (18888) de «HÖRE auf zu trödeln, wir müssen los»

«Höre auf» грамматически верно, короткая форма «Hör auf» — разговорная
норма. Поэтому я замерил, прежде чем править, и класса НЕ НАШЛОСЬ, а
нашлось кое-что точнее. По всей базе:

    Hör    8      Höre   1   ← этот ряд
    Geh   12      Gehe   0
    Komm  22      Komme  0
    Sag    2      Sage   0
    Nimm   3      Nehme  0

То есть база держит короткую форму единогласно, и ровно один ряд из неё
выпадает — причём на том же глаголе и в том же обороте «aufhören», что и
восемь его близнецов (`runterziehen` 8237: «Hör auf, mich
runterzuziehen»). Это не класс и не стилистическая придирка, а один
выброс против собственной нормы базы.

ПРОВЕРИЛ И ВТОРОЕ: среди 44 повелительных с «-e» есть и такие, где «-e»
не обязательно (`störe`, `zeige`, `verschone`, `verteile`). Их я НЕ
трогаю — это законный письменный регистр, и база вправе его держать.
Довод в `trödeln` не «длинная форма хуже», а «тот же оборот в базе
написан иначе восемь раз из девяти».

ОСТАЛЬНЫЕ ПЯТЬ:

 • `knirschen` (8234) en «His teeth grind at night» — подлежащим стали
   зубы. По-английски говорят «He grinds his teeth»; немецкий, русский,
   украинский, турецкий и польский все держат человека подлежащим.
 • `bedrängen` (11347) pl «Dzieciaki» (детишки) вместо «Die
   Schulkinder» (школьники) — и слово другое, и регистр ниже.
 • `Heuschrecke` (15771) pl «zjadła całe pole zboża» (съела целое поле
   зерна) вместо «zerstörten ganze Felder» (уничтожили целые поля):
   добавлено зерно, потеряно множественное число полей.
 • `zuwider` (11353) pl «Takie zachowanie jest mi wstrętne» — добавлено
   «zachowanie» (поведение), которого в «Das ist mir zuwider» нет.
 • `Zwangsjacke` (13007) pl «Założyli mu kaftan» (надели на него)
   вместо «festgehalten werden» (приходилось удерживать).
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ немецкий эталон ════════════════════════════════════════
    (11346, "example_de",
     "Er trug sich würdevoll aus dem Saal hinaus, ohne zu murren",
     "Er verließ den Saal würdevoll, ohne zu murren",
     "«sich hinaustragen» о человеке, который вышел, — не по-немецки"),
    (18888, "example_de",
     "Höre auf zu trödeln, wir müssen los",
     "Hör auf zu trödeln, wir müssen los",
     "база держит «Hör» 8 раз против 1 «Höre» — один выброс из нормы"),

    # ══ подлежащее подменено ═══════════════════════════════════
    (8234, "example_en",
     "His teeth grind at night when he's stressed",
     "He grinds his teeth at night when he's stressed",
     "подлежащим стали зубы; в пяти других языках подлежащее — человек"),

    # ══ польские подмены ═══════════════════════════════════════
    (11347, "example_pl",
     "Dzieciaki ciągle go nękają",
     "Uczniowie ciągle go nękają",
     "«Dzieciaki» вместо «Die Schulkinder»: другое слово и ниже регистр"),
    (15771, "example_pl",
     "Szarańcza zjadła całe pole zboża",
     "Szarańcza zniszczyła całe pola",
     "добавлено зерно, потеряно множественное «ganze Felder»"),
    (11353, "example_pl",
     "Takie zachowanie jest mi wstrętne",
     "To jest mi wstrętne",
     "добавлено «zachowanie», которого в «Das ist mir zuwider» нет"),
    (13007, "example_pl",
     "Założyli mu kaftan bezpieczeństwa",
     "Trzeba go było przytrzymywać w kaftanie bezpieczeństwa",
     "«надели на него» вместо «festgehalten werden» — приходилось удерживать"),
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
