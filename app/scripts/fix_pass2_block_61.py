"""ВТОРОЙ ПРОХОД, блок 61 (ряды 12001–12200): 6 правок.

ЗДЕСЬ НАЧАЛСЯ БЕЗРАНГОВЫЙ ХВОСТ — ряды, у которых `frequency_rank` нет
вовсе, и извлекатель ставит их в конец. Это не продолжение частотного
списка: вся лексика блока A1 и A2, примеры короткие («Die Himbeeren sind
süß», «Er wartet im Hausflur»), и слова учебные — `Gesundheitskarte`,
`Krankenkasse`, `Jobcenter`, `Kursraum`, `Postleitzahl`.

И ОНА ЗАМЕТНО ЧИЩЕ: плотность 3% против 5.5–21.5% в предыдущих блоках.
Подмен целиком нет ни одной. Похоже, этот слой собирали отдельно и
аккуратнее — что понятно, это ядро, с которого начинает учащийся.

ДЕСЯТЫЙ ВИНОВАТЫЙ ЭТАЛОН, И САМЫЙ ГРУБЫЙ ЗА ВЕСЬ ПРОХОД:

    ihr/ihre (428, A1) de «Das ist die Tasche MEINER SCHWESTER»
                       en «That is HER bag»
                       ru «Это ЕЁ сумка»
                       uk «Це ЇЇ сумка»
                       pl «To jest JEJ torba»
                       tr «Bu ONLARIN çantası»   ← «их», а не «её»

Заголовка `ihr/ihre` в немецком примере НЕТ ВОВСЕ: вместо притяжательного
«ihre» там «meiner Schwester». То есть ряд A1, который учит самому
нужному притяжательному местоимению, показывает фразу с ДРУГИМ
местоимением — «моей сестры».

Четыре перевода при этом говорят «её сумка», то есть переводчики
переводили ЗАМЫСЕЛ ряда, а не эту фразу. Правка «Das ist ihre Tasche»
делает их все верными сразу. Турецкий отдельно: «onların» значит «их», а
нужно «onun» — в списке оба значения есть («onun, onların»), но пример
должен показывать то же, что остальные пять.

Почему это грубее предыдущих девяти: `zurückdrehen` (блок 47) и
`Muttermilch` (блок 59) были C2 и B1, а здесь A1 — ряд, который видят
все и в первую неделю.

ОСТАЛЬНЫЕ ЧЕТЫРЕ:

 • `Kiwi` (484) ru «Киви ЗЕЛЁНЫЙ» — мужской род значит ПТИЦУ киви; фрукт
   по-русски среднего рода («зелёное»), и немецкое «Die Kiwi» — именно
   фрукт. Список держит оба значения («киви, птица киви»), и род здесь
   их и различает.
 • `Krankmeldung` (514) uk «повідомлення про хворобу» не из списка
   («лікарняний, довідка про хворобу») — карточка показывала
   «лікарняний».
 • `Kurzstrecke` (525) uk «коротка дистанція» не из списка («коротка
   поїздка, коротка відстань»).
 • `Mango` (570) ru добавлено «очень», которого в «schmeckt lecker» нет.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ десятый виноватый эталон, уровень A1 ════════════════════
    (428, "example_de",
     "Das ist die Tasche meiner Schwester",
     "Das ist ihre Tasche",
     "заголовка `ihr/ihre` в примере нет вовсе: вместо него «meiner Schwester»"),
    (428, "example_tr",
     "Bu onların çantası",
     "Bu onun çantası",
     "«onların» значит «их»; остальные пять языков говорят «её»"),

    # ══ род различает значения списка ══════════════════════════
    (484, "example_ru",
     "Киви зелёный",
     "Киви зелёное",
     "мужской род значит ПТИЦУ киви; «Die Kiwi» — фрукт, он среднего рода"),

    # ══ слово не из своего списка ══════════════════════════════
    (514, "example_uk",
     "Він подає повідомлення про хворобу",
     "Він подає лікарняний",
     "«повідомлення про хворобу» не из списка; «лікарняний» в нём первый"),
    (525, "example_uk",
     "Від Берліна до Потсдама — коротка дистанція",
     "Від Берліна до Потсдама — коротка відстань",
     "«дистанція» не из списка; «коротка відстань» в нём второе"),

    # ══ добавлено лишнее ═══════════════════════════════════════
    (570, "example_ru",
     "Манго очень вкусное",
     "Манго вкусное",
     "«очень» в «Die Mango schmeckt lecker» нет"),
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
