"""ПРИМЕТА: в немецком число цифрой, в переводе — словом.

ОТКУДА ВЗЯЛАСЬ. `scan_number_mismatch` сравнивает ЦИФРЫ немецкого и
перевода и потому слепа там, где цифра заменена словом: сравнивать
нечего. Класс всплывал четыре раза по одному случаю — `Kaufmann` (блок
32), `Radius` и `Quote` (блок 36), `Franken` (блок 38). В блоке 36 я
записал, что при четвёртом случае надо замерить класс узко, без списка
числительных. Здесь это сделано.

**САМОКРИТИКА, ТУ ЖЕ, ЧТО ПО ЗАГОЛОВКАМ-ПОВТОРАМ.** Правило «всякое
наблюдение, повторившееся дважды, становится замером по всей базе»
действовало с начала прохода. Я правил этот класс по одной ячейке ЧЕТЫРЕ
раза, прежде чем замерить. Замер нашёл 44 ячейки — на порядок больше, и
он стоил десяти минут.

КАК УСТРОЕНО ПРАВИЛО, И ПОЧЕМУ БЕЗ СПИСКА ЧИСЛИТЕЛЬНЫХ. Перечислять
«pięć/пять/beş/five» на шесть языков во всех падежах — то самое
перечисление, которое шесть раз за проход покрывало только само себя.
Поэтому правило ЧИСТО СТРУКТУРНОЕ: в немецком примере есть цифра, а в
примере какого-то языка цифры НЕТ ВООБЩЕ. Что именно стоит на её месте,
примета не знает и знать не обязана.

ЗАМЕР: 168 рядов с цифрой в немецком, из них 106 с языком без цифры.

    в каком языке нет цифры:  pl 105,  uk 21,  ru 18,  en 4,  tr 2
    и только в этом языке:    pl 80

То есть класс — ПОЛЬСКИЙ. Это пятый случай за проход, когда дефект
оказывается сосредоточен в одном языке (см. польские полосы в блоках
21, 22, 27, 35, 36, 37): польский переводили отдельным прогоном, и в нём
числа систематически писали словами.

ТРИ ПОДКЛАССА, И ДВА ИЗ НИХ — НОРМА. Разделение берётся из САМОГО
немецкого, а не из догадки:

    порядковое или десятилетие  — цифра с точкой («5. Klasse»,
        «18. Jahrhundert») либо «70ern». 23 ряда. НОРМА: по-русски,
        по-украински и по-польски порядковые и века называют словом
        («в девятнадцатом веке», «w piątej klasie»), и ru с uk делают
        это вместе с польским.
    время                        — цифра перед «Uhr». 37 рядов. НОРМА
        по той же причине: «в десять часов», «o ósmej» — так говорят.
    ИЗМЕРЕНИЕ ИЛИ КОЛИЧЕСТВО     — всё остальное: «50 Euro», «38 Grad»,
        «300 Kilometer», «100 PS», «800 Lumen», «50000 Einwohner».
        46 рядов. ВОТ ЭТО дефект: цифра и есть предмет фразы, пять
        языков из шести её сохраняют, и только польский — нет.

Из 46 измерений польский промахивался в 45, и в 44 из них он был
ЕДИНСТВЕННЫМ промахнувшимся. Эти 44 ячейки исправлены
`fix_pl_numbers_as_words.py`.

ДВА ЗАКОННЫХ ОСТАТКА, И ОБА ОДНОГО ПОДКЛАССА — НОМЕР ПЛАТФОРМЫ ИЛИ ПУТИ:

    Bahnsteig    (1211)  de «von Bahnsteig 3»
        ru «с третьей платформы», uk «з третього перону»,
        pl «z peronu trzeciego»
    Anschlusszug (1145)  de «fährt von Gleis 5»
        ru «с пятой платформы», uk «з п'ятої платформи»,
        tr «beşinci perondan»

Правило относит их к измерениям только потому, что у «3» и «5» нет
точки, — но по смыслу это ПОРЯДКОВЫЕ номера, и словом их называет не
один язык, а сразу три, причём в двух рядах разные тройки. Так и
говорят: «с пятой платформы», а не «с платформы 5».

**Второй ряд примета нашла сама.** `Bahnsteig` я разобрал глазами в
блоке 37 и решил не трогать; `Anschlusszug` в тот блок не попадал, и я
его не искал. Замер нашёл его и вынес тот же вердикт независимо от меня
— это и есть цена замера против чтения по одному ряду. Примета ждёт
РОВНО ДВА остатка и падает, если число изменилось.

ПРЕДЕЛ ПРИМЕТЫ. Она видит только полное отсутствие цифры. Если в переводе
цифра есть, но ДРУГАЯ, это дело `scan_number_mismatch`; если цифр две и
одна из них словом — не увидит ни та, ни эта.
"""

from __future__ import annotations

import re
import sys

from sqlalchemy import create_engine, text

from app.config import settings

LANGS = ("en", "ru", "uk", "tr", "pl")
DIGIT = re.compile(r"\d")
ORDINAL = re.compile(r"\d+\.")
DECADE = re.compile(r"\d+ern")
CLOCK = re.compile(r"\d+\s*Uhr")

EXPECTED = 2  # Bahnsteig (1211) и Anschlusszug (1145), см. docstring


def kind_of(example_de: str) -> str:
    if ORDINAL.search(example_de) or DECADE.search(example_de):
        return "порядковое/десятилетие"
    if CLOCK.search(example_de):
        return "время"
    return "измерение"


def selfcheck() -> None:
    cases = [
        # ХОРОШО: это норма, число словами ожидаемо
        ("Ich bin in der 5. Klasse", "порядковое/десятилетие"),
        ("Das Korsett war im 19. Jahrhundert Mode", "порядковое/десятилетие"),
        ("Dieser retro Stil aus den 70ern gefällt mir", "порядковое/десятилетие"),
        ("Die Besprechung beginnt um 10 Uhr", "время"),
        ("Der Zug fährt um 10 Uhr ab", "время"),
        # ПЛОХО: цифра и есть предмет фразы
        ("Das kostet höchstens 20 Euro", "измерение"),
        ("Das Thermometer zeigt 38 Grad", "измерение"),
        ("Das Auto hat 100 PS", "измерение"),
        ("Diese Stadt hat etwa 50000 Einwohner", "измерение"),
    ]
    bad = 0
    for sentence, want in cases:
        got = kind_of(sentence)
        if got != want:
            bad += 1
            print(f"САМОПРОВЕРКА ПРОВАЛЕНА: {sentence!r} -> {got}, ждали {want}")
    if bad:
        sys.exit(1)
    print("самопроверка правила: 9 из 9")


def main() -> None:
    if "--selfcheck" in sys.argv:
        selfcheck()
        return

    engine = create_engine(settings.DATABASE_URL_SYNC)
    with engine.connect() as conn:
        rows = conn.execute(text(
            "SELECT id, word_de, example_de, example_en, example_ru, "
            "example_uk, example_tr, example_pl FROM words "
            "WHERE example_de ~ '[0-9]'"
        )).mappings().all()

    counts = {"порядковое/десятилетие": 0, "время": 0, "измерение": 0}
    per_lang = {lang: 0 for lang in LANGS}
    defects = []
    for row in rows:
        missing = [
            lang for lang in LANGS
            if not DIGIT.search(row[f"example_{lang}"] or "")
        ]
        if not missing:
            continue
        kind = kind_of(row["example_de"] or "")
        counts[kind] += 1
        for lang in missing:
            per_lang[lang] += 1
        if kind == "измерение":
            defects.append((row, missing))

    for row, missing in defects:
        print(f"{row['word_de']} ({row['id']})  без цифры в: {','.join(missing)}")
        print(f"    de  {row['example_de']}")
        for lang in missing:
            print(f"    {lang}  {row[f'example_{lang}']}")

    print(f"\nрядов с цифрой в немецком: {len(rows)}")
    print(f"по виду числа: {counts}")
    print(f"в каком языке нет цифры: {per_lang}")
    print(f"\nвсего дефектов (измерение/количество): {len(defects)}")
    print(f"ожидаемый остаток: {EXPECTED} — номера платформы, см. docstring")
    if len(defects) != EXPECTED:
        print("ВНИМАНИЕ: остаток изменился — разбери и обнови docstring")
        sys.exit(1)


if __name__ == "__main__":
    main()
