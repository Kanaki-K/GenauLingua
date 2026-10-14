"""ВТОРОЙ ПРОХОД, блок 47 (ряды 9201–9400): 5 правок.

ГЛАВНОЕ ЗДЕСЬ — ПЯТЫЙ СЛУЧАЙ, КОГДА ВИНОВАТ НЕМЕЦКИЙ ЭТАЛОН:

    zurückdrehen (8167) de «Ich drehe die Musik LEISER, sie ist mir zu laut»

Заголовок `zurückdrehen`, а в примере его нет: есть «leiser drehen» —
другой, хоть и близкий по смыслу оборот. Ряд учит не тому слову, которое
показывает. Все пять переводов при этом верны («убавляю музыку»), потому
что они переведены с немецкого правильно. Дефект один и ровно в эталоне,
и правка одна: «Ich drehe die Musik zurück, sie ist mir zu laut».

ПОЧЕМУ ЭТОГО НЕ ВИДИТ `scan_word_in_example`: для отделяемых глаголов
примета ищет основу, а «drehe» в примере есть. Приставки она не
проверяет, и проверять не может — у «umschauen» в примере «schaut sich
um» приставка стоит в конце, у «ausfahren» — «fahren … aus». Отличить
«приставка унесена в конец» от «приставки нет вовсе» структурно нельзя
без разбора предложения. Класс остаётся глазным.

ОСТАЛЬНЫЕ ЧЕТЫРЕ — подмены, три из них польские (участок тот же, что в
блоке 46): `dampfen` с супом вместо еды, `umschauen` с повелительным «по
комнате» вместо «он оглядывается и видит город», `verbitten` с
«замечаниями» вместо «оскорбления». Плюс украинская подмена в
`statistisch`: «люди набирають менше ваги» (люди набирают меньше веса)
вместо «mniej ludzi ma nadwagę» (меньше людей страдают избыточным весом)
— смысл перевёрнут с «сколько людей» на «сколько веса».
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ немецкий эталон не содержит своего заголовка ════════════
    (8167, "example_de",
     "Ich drehe die Musik leiser, sie ist mir zu laut",
     "Ich drehe die Musik zurück, sie ist mir zu laut",
     "заголовок zurückdrehen, а в примере «leiser drehen» — другой оборот"),

    # ══ подмена смысла ═════════════════════════════════════════
    (18042, "example_uk",
     "Статистично кажучи, люди набирають менше ваги, ніж раніше",
     "Статистично кажучи, менше людей має надмірну вагу, ніж раніше",
     "«набирають менше ваги» вместо «weniger Menschen übergewichtig»"),

    # ══ польские подмены ═══════════════════════════════════════
    (11290, "example_pl",
     "Nie życzę sobie takich uwag",
     "Nie życzę sobie takiej obrazy",
     "«uwag» это замечания; в эталоне «Beleidigung» — оскорбление"),
    (8176, "example_pl",
     "Zupa jeszcze paruje, jest gorąca",
     "Jedzenie jeszcze paruje, jest za gorące",
     "«Zupa» вместо «Das Essen», и потеряно «zu» в «zu heiß»"),
    (8181, "example_pl",
     "Rozejrzyj się dobrze po pokoju",
     "Rozgląda się i widzi miasto",
     "подмена целиком: повеление про комнату вместо «Er schaut sich um "
     "und sieht die Stadt»"),
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
