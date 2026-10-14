"""ВТОРОЙ ПРОХОД, блок 23 (ряды 4401–4600): 20 правок.

Отдельно от этого блока закрыт СКВОЗНОЙ КЛАСС «запись времени на
часах» — 52 ячейки, `fix_clock_time.py`. Он всплывал по одному ряду в
блоках 16, 18, 22 и здесь (`Auktion`, `Abfahrt`), и четвёртого раза
хватило, чтобы замерить по базе.

ПОДМЕНЫ: польских пять, и это третий блок подряд с таким перекосом.

    ausdenken      (7242)  pl «Wymyśliłem świetny plan na weekend»
    Senf           (11745) pl «Daj mi musztardę do kiełbasy»
    Schleier       (13680) pl «Panna młoda miała długi welon»
    spannungsvoll  (10576) en «That was a thrilling movie»
                           uk «Це був напружений фільм»

Последний ряд интересен тем, что английский и украинский ушли ВМЕСТЕ,
а эталон «Die Stimmung im Raum war spannungsvoll» про атмосферу в
комнате. Турецкий и польский верны — то есть это та же пара-источник,
что en+uk+tr, но без турецкого.

ЕЩЁ ОДИН РЯД С ФОРМОЙ СЛОВА ВМЕСТО ЗАГОЛОВКА. `angerührt` (10577):
эталон писал «Ich war von der Geschichte gerührt» — то есть `gerührt`,
а слово ряда `angerührt`. Это третий такой случай после `schrecken`
(10372, блок 15) и `blasiert` (10481, блок 19), и правится так же: в
эталон ставится форма заголовка.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ КЛАСС: подменённое предложение ═══════════════════════════
    (10576, "example_en",
     "That was a thrilling movie",
     "The atmosphere in the room was full of tension",
     "подмена: эталон «Die Stimmung im Raum war spannungsvoll»"),
    (10576, "example_uk",
     "Це був напружений фільм",
     "Атмосфера в кімнаті була напружена",
     "то же; tr и pl верны"),
    (7242, "example_pl",
     "Wymyśliłem świetny plan na weekend",
     "Wymyślam plan",
     "подмена: ни «świetny», ни «na weekend» в эталоне нет, и время не то"),
    (11745, "example_pl",
     "Daj mi musztardę do kiełbasy",
     "Lubię musztardę na mojej kiełbasie",
     "подмена: эталон «Ich mag Senf auf meiner Wurst»"),
    (13680, "example_pl",
     "Panna młoda miała długi welon",
     "Miała na sobie biały welon na weselu",
     "подмена: невеста и длинная фата вместо белой"),

    # ══ эталон: форма слова вместо заголовка ═════════════════════
    (10577, "example_de",
     "Ich war von der Geschichte gerührt",
     "Ich war von der Geschichte angerührt",
     "слово ряда — `angerührt`; третий случай после `schrecken` и `blasiert`"),

    # ══ слово не из своего списка и не то слово ══════════════════
    (7242, "example_tr",
     "Bir plan aklıma getireceğim",
     "Bir plan düşünüp buluyorum",
     "«aklıma getirmek» это припомнить, а ausdenken — придумать"),
    (13680, "example_tr",
     "Düğünde beyaz peçe takıyordu",
     "Düğünde beyaz duvak takıyordu",
     "«peçe» закрывает лицо; свадебная фата — «duvak», и она первая в списке"),
    (7271, "example_uk",
     "Насамкінець все вийшло",
     "Врешті-решт усе вийшло",
     "«насамкінець» это «в последнюю очередь», а letztlich — в итоге"),
    (17553, "example_ru",
     "Веб-портал удобен в использовании",
     "Портал к веб-сайту был удобным",
     "потеряно прошедшее время и «zur Website»"),

    # ══ не тот притяжательный ═══════════════════════════════════
    (15066, "example_pl",
     "Ich lesbijski związek jest bardzo szczęśliwy",
     "Jej lesbijski związek jest bardzo szczęśliwy",
     "«ich» это «их»; в ru, uk и en стоит «её»"),

    # ══ потерянное слово ════════════════════════════════════════
    (8910, "example_uk",
     "Офіціант приносить рахунок",
     "Офіціант приносить нам рахунок",
     "потеряно «uns»: в ru и pl оно есть"),
    (8910, "example_tr",
     "Garson hesabı getiriyor",
     "Garson bize hesabı getiriyor",
     "то же"),
    (8910, "example_en",
     "The waiter brings the bill",
     "The waiter brings us the bill",
     "то же"),
    (10580, "example_pl",
     "Ja tylko żartuję",
     "Ja tylko z tobą żartuję",
     "потеряно «mit dir»: в остальных четырёх оно есть"),

    # ══ добавленное слово ═══════════════════════════════════════
    (16243, "example_tr",
     "Hükümete karşı isyan cesurca bir eylemdi",
     "Hükümete karşı isyan cesurdu",
     "«bir eylem» в эталоне «war mutig» нет"),
    (7246, "example_pl",
     "Stół jest już nakryty do obiadu",
     "Stół jest już nakryty",
     "«do obiadu» в эталоне нет"),
    (10577, "example_pl",
     "Byłem bardzo wzruszony tą historią",
     "Byłem wzruszony tą historią",
     "«bardzo» в эталоне нет"),
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
