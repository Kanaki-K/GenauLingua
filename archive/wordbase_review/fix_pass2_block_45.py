"""ВТОРОЙ ПРОХОД, блок 45 (ряды 8801–9000): 1 правка.

САМЫЙ ЧИСТЫЙ БЛОК ЗА ПРОХОД — одна правка на 200 рядов, 0.5%. Шестой
блок подряд вниз: 18–22% → 8% → 6.5% → 4% → 2.5% → 0.5%.

ГЛАВНОЕ В БЛОКЕ — НЕ ПРАВКА, А ЗАМЕР. Ряд 8899 `entkommen` (8103) и ряд
8730 `entfliehen` (16640) из прошлого блока: заголовки разные, немецкие
эталоны разные, а переводы совпадают СЛОВО В СЛОВО в ru, uk и pl —
«Заключённые сбежали из тюрьмы».

Ни `scan_same_headword` (сравнивает заголовки), ни `scan_inflected_twin`
(нужна общая основа) этого не видят. Признак структурный — равенство
строк, — поэтому по правилу из блока 42 примета написана сразу:
`scan_twin_example.py`.

ЗАМЕР: 223 пары с совпавшим примером хотя бы в одном языке; порог «не
меньше трёх языков» оставляет 86. Делятся по тому, совпадает ли ТАКЖЕ
немецкий эталон:

    30 пар — ЗАКОННЫ: одна немецкая фраза нарочно обслуживает несколько
        рядов, и каждый учит своё слово этой фразы. «Das Bild hängt an
        der Wand» → `an`, `hängen`, `Wand`. Для A1 это разумно.
    56 пар — НАСТОЯЩИЙ КЛАСС, и он о синонимах: `herrlich`/`wunderbar`,
        `schrecklich`/`furchtbar`/`miserabel` (тройка),
        `Toilette`/`WC`/`Klo` (тройка), `Beil`/`Axt`,
        `Gegenmittel`/`Gegengift`, `Stockwerk`/`Geschoss`…

ПЕРВОЕ, ЧТО Я ПРОВЕРИЛ — НЕ ЛОМАЕТ ЛИ ЭТО ТЕСТ, и ответ оказался
неожиданным: **код уже защищён.** Если `herrlich` и `wunderbar` дают один
перевод, вопрос про `herrlich` с дистрактором `wunderbar` имел бы два
верных ответа. Но `get_distractors` отбрасывает кандидата, чьи значения
пересекаются с верным ответом хотя бы по одному:

    if not variants or variants & taken:
        continue

Сравнение идёт по `meaning_variants`, то есть по каждому значению
отдельно. Все 56 пар для теста безвредны.

**Это первый случай за проход, когда замер нашёл класс, а продакшн-код
оказался к нему уже готов.** Вывод, который стоит внести в правила:
прежде чем считать класс дефектом, посмотри, не обрабатывает ли его код.
Я подходил к этому с другой стороны четыре раза (матчер, поблажка, хвост
основы) — но там код был ВИНОВАТ, а здесь он спас.

Владельцу остаётся решение о составе базы: два ряда всё равно учат одному
и тому же. Разумный вариант — не удалять ряды, а РАЗВЕСТИ примеры, чтобы
`Beil` остался про топорик, а `Axt` про колун.

ЕДИНСТВЕННАЯ ПРАВКА: `präsent` (8101) ru — «была мысленно включена» не
по-людски, и слова ряда в примере нет, поэтому карточка показывала
«присутствующий» при фразе про «включена».
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    (8101, "example_ru",
     "Во время встреч она всегда была мысленно включена",
     "Во время встреч она мысленно всегда присутствовала",
     "«мысленно включена» не по-людски, и слова ряда в примере не было"),
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
