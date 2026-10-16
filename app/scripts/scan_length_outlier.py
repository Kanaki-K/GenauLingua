"""
Примета: перевод вдвое короче, чем положено его языку.

ЗАЧЕМ. Класс «подменённое предложение» (перевод говорит не то, что
эталон) и класс «потерянный оборот» (перевод отбросил половину фразы)
до сих пор ловились только глазами. В блоке 14 я попробовал формальный
признак «в переводе нет ни одного слова из его же списка переводов» —
он дал 7 попаданий, и все семь оказались артефактами `_STEM_MIN`.
Признака не было.

Этот есть, и он простой: СЧИТАТЬ СЛОВА. Подменённое предложение почти
всегда короче эталона, потому что подмена — это чужая короткая фраза
(«No entry» вместо «Der Zutritt zum Fitnessstudio kostet extra»), а
потерянный оборот короче по определению.

ПОЧЕМУ НЕЛЬЗЯ СРАВНИВАТЬ С НЕМЕЦКИМ НАПРЯМУЮ. Первая версия сравнивала
число слов перевода с числом слов эталона и дала 222 попадания, из
которых ~200 турецкие. Это не дефект, а устройство языка: турецкий
агглютинативный, «Postaneye gidiyorum» — два слова против пяти в «Ich
gehe zur Post». Славянские языки тоже короче немецкого: падеж съедает
предлог и артикль («Мотыгой рыхлят почву» против «Mit der Hacke lockert
man den Boden auf»).

Поэтому норма берётся ИЗ САМОЙ БАЗЫ, по каждому языку отдельно:
медиана отношения «слов в переводе / слов в эталоне» по всем рядам.
Получается

    en 1.00   ru 0.80   uk 0.80   pl 0.80   tr 0.71

и дальше выброс считается относительно нормы своего языка. После
нормировки улов упал с 222 до 142, и турецкий перестал быть особым
случаем: в улове все пять языков.

ПОРОГ ВЫБРАН ЗАМЕРОМ, А НЕ НА ГЛАЗ. Самопроверка первой версии
(порог 0.55) НЕ ПРОШЛА, и правильно: «Пастух доглядав овець» против
«Der Hirte passte auf die Schafe auf» это 0.54, а потерянный оборот в
`Knüppel` — 0.42. Законное сжатие и дефект стояли по одну сторону
границы. Пришлось замерить улов по 25 рядам, прочитанным глазами, и по
13 законным сжатиям:

    порог 0.55 → улов 142, настоящих 21, все 13 законных в улове
    порог 0.50 → улов  52, настоящих 20, законных в улове 6
    порог 0.45 → улов  22, настоящих  8, законных в улове 2

Взято 0.50: доля настоящих выросла с одной седьмой до двух пятых, а
потерялось при этом ровно одно попадание — `hinhalten` (7535), где
турецкий говорит совсем другое той же длины.

ГЕЙТОМ НЕ ЯВЛЯЕТСЯ: больше половины улова — законное сжатие.
«Przeskoczyliśmy mały strumień» против «Wir sind über den kleinen Bach
gesprungen» это правильный польский, он просто короче. Примета выводит
мягкий список для глаз, как `scan_imperative_formality`.

ПРЕДЕЛ. Подмену РАВНОЙ длины примета не видит вовсе. Из 25 настоящих
рядов, найденных глазами, четыре не видит ни один порог: `Zutritt` (tr)
и `ausstehen` (tr) — подмена ровно той же длины, `umstimmen` (pl) и
`Begleiterin` (pl) — тоже. И `wundern` (10379) говорил «я дивуюся
твоєму терпінню» вместо «реакції»: одно слово заменено на другое, длина
не изменилась. Примета закрывает подмножество класса, а не класс.

    python -m app.scripts.scan_length_outlier
"""

from __future__ import annotations

import statistics
import sys
from collections import Counter
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

LANGS = ("en", "ru", "uk", "tr", "pl", "it", "es", "fr", "cs")

# вдвое короче нормы своего языка И не меньше чем на 2.5 слова.
# Второе условие нужно, чтобы короткие ряды не шумели: «Das Hemd ist
# orange» это четыре слова, и половина от нормы там — два, то есть
# любой нормальный перевод «Gömlek turuncu» был бы выбросом.
SHARE = 0.50
MIN_GAP = 2.5
MIN_DE_WORDS = 4


def words(s: str | None) -> int:
    return len((s or "").split())


def language_norms(rows) -> dict[str, float]:
    """Медиана отношения длин по каждому языку — норма берётся из базы."""
    acc: dict[str, list[float]] = {l: [] for l in LANGS}
    for r in rows:
        nde = words(r["example_de"])
        if nde < 3:
            continue
        for l in LANGS:
            if r[f"example_{l}"]:
                acc[l].append(words(r[f"example_{l}"]) / nde)
    # язык без единого примера (ещё не переведён) нормы не имеет
    return {l: statistics.median(v) for l, v in acc.items() if v}


def outlier(n: int, nde: int, norm: float) -> bool:
    expect = nde * norm
    return n <= expect * SHARE and expect - n >= MIN_GAP


def selfcheck() -> None:
    errs = []
    # Турецкий: законное сжатие НЕ должно срабатывать.
    # «Ich gehe zur Post» (4) → «Postaneye gidiyorum» (2), норма 0.71.
    if outlier(2, 4, 0.71):
        errs.append("tr: законное сжатие «Postaneye gidiyorum» объявлено выбросом")
    # Украинский падежом вместо предлога — тоже законно, и ИМЕННО ЭТА
    # строка не прошла при пороге 0.55. Она здесь как граница класса:
    # всё, что сжато слабее, трогать нельзя.
    # «Der Hirte passte auf die Schafe auf» (7) → «Пастух доглядав овець» (3)
    if outlier(3, 7, 0.80):
        errs.append("uk: законное «Пастух доглядав овець» объявлено выбросом")
    # А вот потерянный оборот должен срабатывать.
    # «Er schlug mit dem Knüppel auf den Tisch, um Aufmerksamkeit zu
    # bekommen» (12) → «Uderzył pałką w stół» (4), норма 0.80
    if not outlier(4, 12, 0.80):
        errs.append("pl: потерянный оборот в «Knüppel» не найден")
    # Подмена короткой фразой.
    # «Der Zutritt zum Fitnessstudio kostet extra» (6) → «No entry» (2)
    if not outlier(2, 6, 1.00):
        errs.append("en: подмена «No entry» не найдена")
    # Норма должна считаться по языку, а не одна на всех: то же число
    # слов при турецкой норме — не выброс, при английской — выброс.
    if outlier(3, 6, 0.71) == outlier(3, 6, 1.00):
        errs.append("нормировка по языку ничего не меняет — признак сломан")
    if errs:
        print("САМОПРОВЕРКА НЕ ПРОШЛА:")
        for e in errs:
            print("   ", e)
        sys.exit(1)
    print("самопроверка: сжатие по морфологии отличается от потери оборота")


def main() -> None:
    selfcheck()
    engine = create_engine(settings.DATABASE_URL_SYNC)
    cols = ", ".join(f"example_{l}" for l in LANGS)
    with engine.connect() as conn:
        rows = conn.execute(
            text(
                f"SELECT id, word_de, example_de, {cols} FROM words "
                "WHERE example_de IS NOT NULL ORDER BY id"
            )
        ).mappings().all()

    norm = language_norms(rows)
    print(f"\nпрочитано рядов: {len(rows)}")
    print("норма отношения длин по базе:", {l: round(v, 2) for l, v in norm.items()})

    hits: list[tuple[int, str, str, int, float, str, str]] = []
    for r in rows:
        nde = words(r["example_de"])
        if nde < MIN_DE_WORDS:
            continue
        for l in LANGS:
            s = r[f"example_{l}"]
            if s and outlier(words(s), nde, norm[l]):
                hits.append(
                    (r["id"], r["word_de"], l, words(s), round(nde * norm[l], 1),
                     r["example_de"], s)
                )

    print(f"выбросов: {len(hits)}  (нужны глаза)")
    print("по языкам:", dict(Counter(h[2] for h in hits).most_common()))
    print()
    for wid, word, lang, n, expect, de, other in hits:
        print(f"  {wid:>6}  {word:<18} {lang} {n}/{expect}")
        print(f"          de: {de}")
        print(f"          ->  {other}")


if __name__ == "__main__":
    main()
