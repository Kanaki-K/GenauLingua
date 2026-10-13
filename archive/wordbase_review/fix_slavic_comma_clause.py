"""СКВОЗНОЙ КЛАСС: примета сама прятала от себя 61 ряд.

`scan_pl_comma_clause` (блок 42) искала ряды, где в немецком примере есть
запятая, а в переводе её нет. Чтобы не считать английский и турецкий,
где отсутствие запятой — норма, в ней стояло условие:

    if len(missing) == 1 and missing[0] in SLAVIC

То есть: промахнуться должен РОВНО ОДИН язык из пяти, и он должен быть
славянским. Условие выглядело аккуратным и давало 8 рядов остатка.

ЧТО С НИМ НЕ ТАК. Оно не только глушит шум, оно глушит и сигнал. Как
только английский или турецкий ТОЖЕ оказываются без запятой — а это их
норма и случается в двух третях рядов, — счётчик становится 2 или 3, и
польский дефект под ним пропадает. Нашлось это на `Alge` (15770):

    de «Im See wachsen Algen, die das Wasser grün färben»
    ru «В озере растут водоросли, которые делают воду зелёной»
    pl «W jeziorze rosną glony I WODA JEST ZIELONA»

Польский потерял определительную часть. Русский и украинский её держат.
Примета ряд не видела, потому что без запятой были ещё en и tr — то есть
ровно по норме своих языков.

ПРАВИЛЬНОЕ УСЛОВИЕ: считать промахи ТОЛЬКО по славянским. Английский и
турецкий тогда исключены по построению, а не по счёту.

    старое условие (все пять, промах один):      8
    новое условие (только славянские, промах один): 69

ЗАМЕР ПРИБАВКИ: 61 ряд, разметка глазами дала 15 дефектов и 46 законных.

ПОЧЕМУ 46 ЗАКОННЫ. Славянские языки законно сворачивают немецкое
подчинение в оборот, которому запятая не нужна:

    schärfen (7398)  de «..., bevor ich koche» → uk «перед готуванням»
    Riegel  (18303)  de «..., bevor ich schlafe» → pl «przed snem»
    Miliz   (16418)  de «..., um Ordnung zu halten» → uk «для порядку»

Это не потеря, а другое средство языка. Отдельно: русский и украинский
ставят на месте немецкой запятой ТИРЕ (`Gemeinheit` 11265,
`Familientradition` 15301) — функция та же, знак другой.

ПЯТНАДЦАТЬ ДЕФЕКТОВ, и это самый крупный разбор класса за весь проход
после матчера:

 • ПОДМЕНА ЦЕЛИКОМ, пять рядов — польская фраза не перевод, а
   самостоятельное предложение с тем же словом. Та самая форма, что
   замерена в блоке 42: пример СОЧИНЁН по заголовку.
       festbinden (8401)  «привяжи велосипед к столбику» вместо чемодана
       verzweifeln(11100) «не отчаивайся так сразу» вместо «я отчаиваюсь»
       pingelig  (11424)  «не будь привередлив в еде» вместо шефа и
                          форматирования
       spotten   (11552)  «не насмехайся над младшим братом» вместо
                          «парни насмехаются над ним»
       winken    (14127)  «помахала из окна на прощание» вместо
                          «помахала, когда увидела меня»
 • ПОТЕРЯНА ВТОРАЯ ЧАСТЬ, пять рядов: `Paradox` (8414) без «которого я
   не понимаю», `hysterisch` (12655) без «когда услышала новость»,
   `insofern` (13602, uk) без «но с осторожностью», `Alge` (15770) без
   «которые окрашивают воду», `erstaunt` (10493) с «этой новостью»
   вместо «когда она мне это рассказала».
 • ПОДМЕНА ЛИЦА ИЛИ ПОДЛЕЖАЩЕГО, три ряда: `erahnen` (8597) «уже
   догадываюсь о твоих планах» вместо «могу догадаться, о чём ты
   думаешь»; `Scharlatan` (11425) «этот ВРАЧ» вместо «Der Mann»;
   `Zahnfleisch` (13057) «кровоточат У МЕНЯ» при немецком «Sein».
 • ОБЯЗАТЕЛЬНАЯ ПОЛЬСКАЯ ЗАПЯТАЯ, два ряда — здесь дефект не в смысле,
   а в пунктуации: перед «jakby» (10481) и перед «odkąd» (12728)
   польский требует запятой, и её не было. Заодно в 12728 «od kiedy»
   заменено на нормативное «odkąd».
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ подмена целиком: пример сочинён по заголовку ════════════
    (8401, "example_pl",
     "Przywiąż rower do słupka",
     "Musimy przywiązać walizkę, zanim wyruszymy",
     "велосипед и столбик вместо чемодана и отъезда"),
    (11100, "example_pl",
     "Nie rozpaczaj tak od razu",
     "Powoli zaczynam rozpaczać, jeśli tak dalej pójdzie",
     "повеление вместо «Ich verzweifle langsam, wenn das so weitergeht»"),
    (11424, "example_pl",
     "Nie bądź taki wybredny przy jedzeniu",
     "Mój szef jest strasznie drobiazgowy, jeśli chodzi o formatowanie",
     "еда вместо шефа и форматирования"),
    (11552, "example_pl",
     "Nie wyśmiewaj się z młodszego brata",
     "Chłopcy wyśmiewają się z niego, bo jest kujonem",
     "младший брат вместо «Die Jungs spotten über ihn, weil er nerdig ist»"),
    (14127, "example_pl",
     "Pomachała mi z okna na pożegnanie",
     "Pomachała mi, kiedy mnie zobaczyła",
     "окно и прощание вместо «als sie mich sah»"),

    # ══ потеряна вторая часть ══════════════════════════════════
    (8414, "example_pl",
     "To naprawdę dziwny paradoks",
     "To prawdziwy paradoks, którego nie rozumiem",
     "потеряно «das ich nicht verstehe»"),
    (10493, "example_pl",
     "Byłem bardzo zdziwiony tą wiadomością",
     "Byłem bardzo zdziwiony, kiedy mi to powiedziała",
     "«этой новостью» вместо «als sie mir das erzählt hat»"),
    (12655, "example_pl",
     "Wpadła w histeryczny płacz",
     "Wpadła w histerię, kiedy usłyszała tę wiadomość",
     "потеряно «als sie die Nachricht hörte»"),
    (13602, "example_uk",
     "У цьому плані я з тобою згоден",
     "У цьому плані я з тобою згоден, але з обережністю",
     "потеряно «aber mit Vorsicht»"),
    (15770, "example_pl",
     "W jeziorze rosną glony i woda jest zielona",
     "W jeziorze rosną glony, które zabarwiają wodę na zielono",
     "потеряно «die das Wasser grün färben» — на этом ряде класс и найден"),

    # ══ подмена лица или подлежащего ═══════════════════════════
    (8597, "example_pl",
     "Już domyślam się twoich planów",
     "Mogę się domyślić, o czym myślisz",
     "«твои планы» вместо «was du denkst»"),
    (11425, "example_pl",
     "Ten lekarz to zwykły szarlatan",
     "Ten człowiek to szarlatan, który sprzedaje fałszywą wiedzę",
     "«врач» вместо «Der Mann» и потеряна вторая часть"),
    (13057, "example_pl",
     "Krwawią mi dziąsła przy myciu zębów",
     "Jego dziąsła krwawią, kiedy myje zęby",
     "«у меня» при немецком «Sein Zahnfleisch»"),

    # ══ обязательная польская запятая ══════════════════════════
    (10481, "example_pl",
     "Wygląda na zblazowanego jakby nic go nie obchodziło",
     "Wygląda na zblazowanego, jakby nic go nie obchodziło",
     "перед «jakby» в польском запятая обязательна"),
    (12728, "example_pl",
     "Czuję się lepiej od kiedy to powiedziałem",
     "Czuję się lepiej, odkąd to powiedziałem",
     "перед «odkąd» запятая обязательна; «od kiedy» заменено нормативным"),
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
