"""ТРЕТИЙ ПРОХОД, блок 8 (ряды 1401–1600): 3 ячейки в 3 рядах.

ЧИТАЛОСЬ 200 РЯДОВ, ЗАМЕЧАНИЕ ГЛАЗАМИ ОДНО — И ОНО РАЗВЕРНУЛОСЬ В КЛАСС.

Глаз остановился на одном ряду из двухсот:

    Krebs (12498, A2)
        en  Cancer, crab
            · My grandpa unfortunately got cancer

Английский различает регистром два разных слова: «cancer» — болезнь,
«Cancer» — знак зодиака. Карточка показывает ученику тот вариант
списка, который совпал с примером, то есть «Cancer» — созвездие там,
где фраза про болезнь. Остальные пять языков регистром ничего не
различают («рак», «rak»), поэтому класс чисто английский, и ни один из
десяти гейтов его не берёт: `scan_lowercase_start` смотрит на начало
примера, `scan_de_lowercase_noun` — на немецкие существительные.

ЗАМЕР ПО ВСЕЙ БАЗЕ: 5 попаданий, 3 дефекта, 2 законных остатка. Правило
и разбор — в новой примете `scan_en_list_case.py` (сорок восьмая).

ТРИ ПРАВКИ ОДНОГО КЛАССА ЛЕГЛИ В РАЗНЫЕ МЕСТА, И ЭТО ГЛАВНОЕ, ЧТО СТОИТ
ЗАПОМНИТЬ. Примета говорит «список и пример не согласны в регистре», а
кто из них неправ — решает чтение, и ответ каждый раз был другой:

    Krebs        (12498)  неправ СПИСОК, регистром. Пример учит
        болезни, и ru/uk/tr/pl тоже дают болезнь первым значением.
        → «cancer, crab»
    Republikaner (16342)  неправ СПИСОК, но не регистром, а ПОЛНОТОЙ.
        В ru три значения, в uk три, в pl два, в en было одно — и сразу
        партийное, с большой буквы. Пример «defended his beliefs» —
        про общее значение, сторонника республики, и по-английски оно
        строчное. Регистр здесь симптом, а дефект — потерянные
        значения. → «republican, supporter of a republic, member of the
        Republican Party», ровно как в ru/uk.
    Pilates      (12412)  неправ ПРИМЕР. «Pilates» — фамилия Йозефа
        Пилатеса, по-английски всегда с большой буквы. Русский,
        польский и турецкий пишут строчным, и для них это правильно, —
        трогаем только английский. → «I do Pilates twice a week»

ФОРМУЛИРОВКУ ТРЕТЬЕГО ВАРИАНТА ВЫБРАЛ ЗАМЕР, А НЕ Я. Сначала я написал
«Republican Party member» — калькой с русского порядка слов. Примета
после правки показала не два остатка, а ТРИ: «Republican Party member»
начинается с большой буквы, в примере стоит строчное «republican», и
попадание получилось моё собственное. Законное — но созданное правкой.
Переписал на «member of the Republican Party»: то же значение, тот же
порядок, что в ru «член Республиканской партии», а первое слово
строчное — и остаток вернулся к двум. **Если правка увеличивает остаток
приметы, сначала проверь, нет ли формулировки без этого побочного
эффекта.** Ячейка перед перезаписью возвращена к исходному значению,
чтобы `was`-страж в этом файле сторожил именно то, что было в базе до
блока.

ЧТО ЕЩЁ ПРОВЕРЕНО В ЭТОМ БЛОКЕ И ОКАЗАЛОСЬ НОРМОЙ

    «Beeilung» (1483) и подобные: в списке стоит повелительная форма
    («поторопись!», «szybciej») рядом с существительным. Это приём
    базы — глосса через ближайший живой оборот, а не дефект.
    «dicht» (2344) и «fein» (6605): английский пример выбирает не первый
    вариант списка («tight», «excellent»), а русский — первый
    («плотный», «вкусная»). Каждый язык по отдельности прав, и
    `scan_shown_sense` такие ряды проверяет своим правилом.

ЧЕТЫРЕ РЯДА В КУЧУ ВЛАДЕЛЬЦА — всё тот же открытый класс «заголовок не
в словарной форме»: `die Vögel` (15416, множественное число),
`herausgefunden` (6584, причастие), `tausend`/`Tausende` (13468, 13471 —
пара числительных) и `Führer` (8774). Они не ошибки, а решение о форме
заголовка, и принимать его владельцу.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    (12498, "translation_en", "Cancer, crab", "cancer, crab",
     "болезнь по-английски строчная; большая буква — знак зодиака"),
    (16342, "translation_en", "Republican",
     "republican, supporter of a republic, member of the Republican Party",
     "было только партийное значение; пример про общее, оно строчное"),
    (12412, "example_en", "I do pilates twice a week",
     "I do Pilates twice a week",
     "Pilates — фамилия, по-английски всегда с большой буквы"),
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
