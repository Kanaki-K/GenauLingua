"""СКВОЗНОЙ КЛАСС: несжатый предлог с артиклем в немецком эталоне.

Найдено вычиткой блока 48:

    Wertsachen (9906) «Er verschloss alle Wertsachen IN DEM Safe»

По-немецки говорят «im Safe». Стяжение предлога с артиклем (im, am, zum,
zur, beim, vom, ins, ans) — норма, а несжатая форма МАРКИРОВАНА: она
значит «в ТОМ самом», указывает на уже упомянутое.

ЗАМЕР ПО ВСЕЙ БАЗЕ: 50 попаданий, ни одного после запятой (то есть ни
одного, где несжатая форма была бы относительным местоимением — «das
Haus, in dem ich wohne»). Разметка вручную дала 23 дефекта и 27 законных.

ГРАНИЦА. Правлю там, где указательного смысла быть НЕ МОЖЕТ:

 1. ЛЕКСИКАЛИЗОВАННОЕ стяжение — часть устойчивого оборота:
    «ins Heft schreiben» (389), «Einweisung ins Krankenhaus» (13117),
    «beim Schreiner lernen» (9547), «im ganzen Land» (15273),
    «ans Problem rangehen» (13988, разговорный регистр с «mal»).
 2. ССЫЛКА НА ПРОИЗВЕДЕНИЕ без предшествующего упоминания — «im Film»,
    «im Spiel», «im Roman». Таких семь (1497, 10653, 11935, 14107,
    14394, 14505, 18046), и сам этот повтор показывает, что форму дала
    одна привычка генератора, а не замысел.
 3. ГОЛОЕ родовое существительное-место или предмет, без определения:
    im Safe, im Keller, im Restaurant, im Garten, im Pub, im Lagerhaus,
    im Dorf, im Beruf, vom Baum, ins Fleisch.
 4. Отдельно 16963 — там не стиль, а ПАДЕЖ: «befestigt an» в значении
    места требует датива, «Das Bajonett war AM Gewehr befestigt».

НЕ ПРАВЛЮ (27 рядов):

 • где между предлогом и существительным стоит прилагательное — несжатая
   форма там немаркирована: «von dem neuen Spielzeug», «in dem alten
   Wasser», «an dem berühmten Sänger»;
 • где существительное — СОБЫТИЕ, которое фраза и так предполагает
   известным: «bei dem Unfall», «bei dem Konzert», «bei dem Projekt»,
   «von dem Abend», «von dem Streit», «bei dem Verhör». Это стандартный
   немецкий газетный и разговорный оборот, и учащийся встречает его
   именно так.

ПОЭТОМУ КЛАСС НЕ СТАНОВИТСЯ ГЕЙТОМ. Законный остаток у него есть, и
отличить его от дефекта без знания языка нельзя: `scan_de_uncontracted`
держит 27 рядов списком и падает, если список изменился.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ 1. лексикализованное стяжение ══════════════════════════
    (389, "example_de",
     "Ich schreibe in das Heft",
     "Ich schreibe ins Heft",
     "«ins Heft schreiben» — устойчивый оборот"),
    (9547, "example_de",
     "Der Lehrling lernt bei dem Schreiner das Handwerk",
     "Der Lehrling lernt beim Schreiner das Handwerk",
     "«beim Schreiner» как «beim Bäcker, beim Arzt» — у кого учатся"),
    (13117, "example_de",
     "Die Einweisung in das Krankenhaus erfolgte sofort nach der Diagnose",
     "Die Einweisung ins Krankenhaus erfolgte sofort nach der Diagnose",
     "«Einweisung ins Krankenhaus» — устойчивый оборот"),
    (13988, "example_de",
     "Lass mich mal an das Problem rangehen",
     "Lass mich mal ans Problem rangehen",
     "разговорный регистр с «mal» требует стяжения"),
    (15273, "example_de",
     "Die Vermählung des Prinzen war ein großes Ereignis in dem ganzen Land",
     "Die Vermählung des Prinzen war ein großes Ereignis im ganzen Land",
     "«im ganzen Land» — при «ganz» стяжение обязательно"),

    # ══ 2. ссылка на произведение ══════════════════════════════
    (1497, "example_de",
     "Die Grafik in dem Spiel ist beeindruckend",
     "Die Grafik im Spiel ist beeindruckend",
     "«im Spiel»: предшествующего упоминания нет, указательность не к чему"),
    (10653, "example_de",
     "Der Bösewicht in dem Film ist wirklich fies und gemein",
     "Der Bösewicht im Film ist wirklich fies und gemein",
     "«im Film»"),
    (11935, "example_de",
     "In dem Roman wurde die Idee von Menschenfleisch angesprochen",
     "Im Roman wurde die Idee von Menschenfleisch angesprochen",
     "«Im Roman»"),
    (14107, "example_de",
     "Die Gehirnwäsche in dem Film war übertrieben dargestellt",
     "Die Gehirnwäsche im Film war übertrieben dargestellt",
     "«im Film»"),
    (14394, "example_de",
     "In dem Film spielt er einen Vampir",
     "Im Film spielt er einen Vampir",
     "«Im Film»"),
    (14505, "example_de",
     "Er spielt die Hauptrolle in dem Film",
     "Er spielt die Hauptrolle im Film",
     "«im Film»"),
    (18046, "example_de",
     "Der Mutant in dem Film hatte übernatürliche Kräfte",
     "Der Mutant im Film hatte übernatürliche Kräfte",
     "«im Film»"),

    # ══ 3. голое родовое существительное ═══════════════════════
    (7898, "example_de",
     "Ich muss die Äste von dem Baum kappen, sie sind zu lang",
     "Ich muss die Äste vom Baum kappen, sie sind zu lang",
     "«vom Baum»"),
    (8312, "example_de",
     "Die Blumen duften wunderbar in dem Garten",
     "Die Blumen duften wunderbar im Garten",
     "«im Garten»"),
    (9906, "example_de",
     "Er verschloss alle Wertsachen in dem Safe",
     "Er verschloss alle Wertsachen im Safe",
     "«im Safe»"),
    (11195, "example_de",
     "Er ist noch unerfahren in dem Beruf, aber lernwillig",
     "Er ist noch unerfahren im Beruf, aber lernwillig",
     "«im Beruf»"),
    (11740, "example_de",
     "Wir treffen uns heute Abend in dem Pub",
     "Wir treffen uns heute Abend im Pub",
     "«im Pub»"),
    (11813, "example_de",
     "Ich mache drei Schnitte in das Fleisch, damit es schneller gart",
     "Ich mache drei Schnitte ins Fleisch, damit es schneller gart",
     "«ins Fleisch»"),
    (11986, "example_de",
     "Das Essen in dem Restaurant war mir viel zu fettig",
     "Das Essen im Restaurant war mir viel zu fettig",
     "«im Restaurant»"),
    (15736, "example_de",
     "Die Feuchtigkeit in dem Keller war unerträglich geworden",
     "Die Feuchtigkeit im Keller war unerträglich geworden",
     "«im Keller»"),
    (16335, "example_de",
     "Die Polizei führte eine Razzia in dem Lagerhaus durch",
     "Die Polizei führte eine Razzia im Lagerhaus durch",
     "«im Lagerhaus»"),
    (17319, "example_de",
     "Der kleine Gasthof in dem Dorf ist gemütlich",
     "Der kleine Gasthof im Dorf ist gemütlich",
     "«im Dorf»"),

    # ══ 4. падеж, а не стиль ═══════════════════════════════════
    (16963, "example_de",
     "Das Bajonett war an das Gewehr befestigt",
     "Das Bajonett war am Gewehr befestigt",
     "«befestigt an» в значении места требует датива"),
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
