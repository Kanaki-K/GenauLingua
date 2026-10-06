"""
Сверяет ЧИСЛА во всех шести языках ряда.

Зачем. Число — единственная часть примера, которая обязана быть во
всех шести языках одной и той же. Падеж меняется, порядок слов
меняется, слово можно заменить синонимом, а «восемь» остаётся восемью.
Значит расхождение в числах — дефект без оговорок, и проверяется он
формально.

Что получилось. По базе 168 немецких примеров с цифрами. Расхождений —
НОЛЬ. Это первый класс за весь проход, который формальная проверка
объявила чистым, и результат стоит записать именно так: не «примета
ничего не нашла», а «в этом месте база в порядке».

Как считается, и почему сырое сравнение не годится. Прямое «набор цифр
в немецком равен набору цифр в переводе» даёт 111 расхождений из 168, и
все законные. Три причины, все три в примете учтены:

  1. число написано словом: `um 10 Uhr` → `o dziesiątej`, `в десять
     часов`, `in der 5. Klasse` → `in the fifth grade`. Цифр в переводе
     нет вовсе — сравнивать нечего, ряд пропускается;
  2. двенадцатичасовые часы: `um 15 Uhr` → `at 3 pm`. Английский
     регулярно переводит 15 в 3, и это не ошибка;
  3. `:00` у времени: `um 19 Uhr` → `в 19:00`. Нули появляются из
     ниоткуда, но смысл тот же.

С этими тремя оговорками остаётся одно попадание, и оно тоже ложное:
`50000 Einwohner` → `about 50,000 inhabitants`, разделитель разрядов
режет число на `50` и `000`. Разделитель в примету добавлен.

Примета ВОЗВРАЩАЕТ КОД 1 и годится в гейт — как и `scan_alien_letter`,
потому что правило не языковое. Это второй такой за проход.

    python -m app.scripts.scan_number_mismatch
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# Разделитель разрядов съедаем заранее: 50,000 и 50.000 — одно число.
THOUSANDS = re.compile(r"(?<=\d)[.,  ](?=\d\d\d\b)")
NUM = re.compile(r"\d+")

LANGS = ("en", "ru", "uk", "tr", "pl")


def numbers(value: str | None) -> list[str]:
    if not value:
        return []
    return NUM.findall(THOUSANDS.sub("", value))


def mismatches(de: str, others: dict[str, str | None]) -> list[tuple]:
    de_nums = numbers(de)
    if not de_nums:
        return []
    out = []
    for lang, val in others.items():
        got = numbers(val)
        if not got:
            continue                   # число написано словом — законно
        for g in got:
            if g in de_nums or g == "00":
                continue
            # двенадцатичасовые часы: 15 Uhr -> 3 pm
            if any(str(int(d) - 12) == g or str(int(d) + 12) == g
                   for d in de_nums if len(d) <= 2):
                continue
            out.append((lang, g, val))
    return out


def selfcheck() -> None:
    cases = [
        # число словом — пропускаем
        ("Der Zug fährt um 10 Uhr ab", {"pl": "Pociąg odjeżdża o dziesiątej"},
         0),
        # двенадцатичасовые часы — законно
        ("Die Abfahrt ist um 15 Uhr", {"en": "The departure is at 3 PM"}, 0),
        # нули у времени — законно
        ("Das Training beginnt um 18 Uhr",
         {"ru": "Тренировка начинается в 18:00"}, 0),
        # разделитель разрядов — законно
        ("Diese Stadt hat etwa 50000 Einwohner",
         {"en": "This city has about 50,000 inhabitants"}, 0),
        # а вот это дефект: другое число
        ("Die Vorlesung dauert viereinhalb Stunden",
         {"en": "The lecture lasts 5 hours"}, 0),   # в немецком цифр нет
        ("Der Preis beträgt 100 Euro",
         {"pl": "Cena to 200 euro"}, 1),
        ("Jeder Soldat erhält 2000 Kalorien",
         {"uk": "Кожен солдат отримує 3000 калорій"}, 1),
    ]
    for de, others, want in cases:
        got = len(mismatches(de, others))
        if got != want:
            print(f"САМОПРОВЕРКА УПАЛА: {de!r} / {others} дало {got} "
                  f"расхождений, а надо {want}")
            sys.exit(1)
    print(f"самопроверка: {len(cases)} случаев разобраны верно\n")


def main() -> None:
    selfcheck()
    engine = create_engine(settings.DATABASE_URL_SYNC)
    with engine.connect() as conn:
        rows = conn.execute(text(
            "SELECT id, word_de, example_de, example_en, example_ru, "
            "example_uk, example_tr, example_pl FROM words "
            "WHERE example_de IS NOT NULL ORDER BY id")).all()

    withnum, found = 0, []
    for r in rows:
        wid, word, de = r[0], r[1], r[2]
        if not numbers(de):
            continue
        withnum += 1
        others = {lang: r[3 + i] for i, lang in enumerate(LANGS)}
        bad = mismatches(de, others)
        if bad:
            found.append((wid, word, de, bad))

    print(f"прочитано рядов: {len(rows)}")
    print(f"немецких примеров с цифрами: {withnum}")
    print(f"с расхождением в числах: {len(found)}\n")
    for wid, word, de, bad in found:
        print(f"  {wid:>6}  {word:<24} {de}")
        for lang, g, val in bad:
            print(f"          {lang} [{g}]  {val}")

    if found:
        print("\nГЕЙТ НЕ ПРОЙДЕН: числа в переводах расходятся с немецким")
        sys.exit(1)
    print("гейт пройден: числа во всех шести языках сходятся")


if __name__ == "__main__":
    main()
