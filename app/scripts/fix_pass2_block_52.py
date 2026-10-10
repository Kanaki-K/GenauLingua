"""ВТОРОЙ ПРОХОД, блок 52 (ряды 10201–10400): 8 правок и ДЕВЯТЫЙ ГЕЙТ.

БЛОК ДАЛ ДВА ГРАММАТИЧЕСКИХ КЛАССА, И ОБА СТАЛИ ГЕЙТОМ
(`scan_de_declension`). Оба нашлись на одной ячейке каждый, и оба
проверяются формально — правило 1j в чистом виде.

РОД. `Sellerie` (11963) article='der', а пример «Ich schneide DIE
Sellerie». Замер по 7250 существительным дал 5 расхождений, и все пять
законны: у `Daumen`, `Goldbarren`, `Zügel` множественное совпадает с
единственным («die Daumen» — оба больших пальца), `Sommerferien` —
plurale tantum, а `Sellerie` Дуден даёт в ОБОИХ родах. Отсечка по
окончаниям -en/-el/-er делает остаток нулевым, и это гейт.

СКЛОНЕНИЕ. `Kongressabgeordneter` (16796) «DER KongressabgeordnetER
sprach». Субстантивированное прилагательное в мужском именительном берёт
слабое «-e» после определённого определителя и сильное «-er» после
неопределённого. **База делает это верно 26 раз из 27** — «Der
Abgeordnete», «Der Beamte», «Der Gelehrte», «Mein Verwandter», «Ein
Angehöriger» — и выпадает ровно этот ряд. Четвёртый случай подряд, где
довод дала сама база (правило 1r).

САМОПРОВЕРКА НАШЛА ДЫРУ В МОЕЙ ЖЕ ПРИМЕТЕ. Первый прогон `--selfcheck`
провалился на паре «Das Tisch ist neu»: регулярка была регистрозависимой
и артикль в НАЧАЛЕ фразы пропускала. После `re.IGNORECASE` примета нашла
ещё один ряд — `Risse` (7791), заголовок во множественном числе при
артикле «der». Он в куче решений владельца (несловарная форма
заголовка), исключён по id с этой причиной. Без самопроверки гейт
родился бы наполовину слепым.

ТРИ ЗАМЕРА ОТМЕНИЛИСЬ, и это тоже стоит назвать:

 • «beim + существительное + строчный инфинитив» — 69 попаданий, и 68
   законны («zum Arzt gehen», «im Garten toben»). Дефект один:
   `Gummibärchen` (11960) «beim Film schauen», где «beim» управляет
   субстантивированным инфинитивом и нужно «beim Filmschauen». Отличить
   это от законного можно только зная, какой глагол в клаузе главный.
 • «стяжение + строчное слово на -en» — 38 попаданий, все «am besten»,
   «im zweiten»: регулярка поймала прилагательные, а не инфинитивы.
 • «Der + заголовок на -er» — 400 попаданий, все обычные имена деятеля
   («Der Fahrer», «Der Maler»). Класс нашёлся только через ЗАКРЫТЫЙ
   список субстантивированных прилагательных, а не через окончание.

ОСТАЛЬНЫЕ ПРАВКИ:

 • `verfassen` (14285) de «Ich muss einen Bericht verfassen BIS MORGEN»
   — порядок слов: обстоятельство времени уехало за инфинитив, хотя
   нормальный немецкий ставит его перед дополнением. Седьмой случай
   виноватого эталона.
 • `Anwohner` (18431) ru «Жители» и uk «Мешканці» потеряли «местный»,
   который стоит первым в своих списках, — из-за чего карточка
   показывала «местный житель» при примере «Жители».
 • `Stoffwechsel` (13041) pl и `gebraten` (11961) pl — подмены целиком:
   «у меня быстрый метаболизм и я вечно голоден» вместо «его обмен
   веществ особенно быстрый»; «на обед жареная картошка» вместо
   «жареная курица сегодня особенно вкусная».
 • `Magenschmerzen` (13045) pl — настоящее время при немецком прошедшем
   и «po obiedzie» (после обеда) вместо «nach dem Essen» (после еды).
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ грамматика немецкого эталона (девятый гейт) ══════════════
    (16796, "example_de",
     "Der Kongressabgeordneter sprach vor dem Plenum",
     "Der Kongressabgeordnete sprach vor dem Plenum",
     "после определённого определителя нужно слабое «-e»; база так делает 26 раз из 27"),
    (11960, "example_de",
     "Die Kinder lieben Gummibärchen beim Film schauen",
     "Die Kinder lieben Gummibärchen beim Filmschauen",
     "«beim» управляет существительным: субстантивированный инфинитив слитно"),
    (14285, "example_de",
     "Ich muss einen Bericht verfassen bis morgen",
     "Ich muss bis morgen einen Bericht verfassen",
     "обстоятельство времени уехало за инфинитив"),

    # ══ вид карточки: показывалось не то, что в примере ══════════
    (18431, "example_ru",
     "Жители жалуются на шум",
     "Местные жители жалуются на шум",
     "потеряно «местный», стоящее в списке первым; карточка показывала его"),
    (18431, "example_uk",
     "Мешканці скаржаться на шум",
     "Місцеві мешканці скаржаться на шум",
     "то же в украинском"),

    # ══ польские подмены целиком ════════════════════════════════
    (13041, "example_pl",
     "Mam szybki metabolizm i ciągle jestem głodny",
     "Jego metabolizm jest szczególnie szybki",
     "«у меня ... и я голоден» вместо «Sein Stoffwechsel ist besonders schnell»"),
    (11961, "example_pl",
     "Na obiad są smażone ziemniaki",
     "Smażony kurczak smakuje dziś szczególnie dobrze",
     "жареная картошка на обед вместо жареной курицы"),

    # ══ время и подмена слова ═══════════════════════════════════
    (13045, "example_pl",
     "Po obiedzie mam straszny ból brzucha",
     "Po jedzeniu miałem straszny ból brzucha",
     "настоящее при немецком «hatte»; «obiad» (обед) вместо «Essen» (еда)"),
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
