#!/usr/bin/env python3
"""
Число в немецком примере и в переводе расходится.

Это порча знаний, а не стиль. «Die Ankunftszeit des Zuges ist um 14 Uhr» с
переводом «Время прибытия — 18:00» учит неверному времени, и человек запомнит
именно перевод.

Два вида расхождения, и они очень разной надёжности.

ЧИСЛА РАЗНЫЕ — признак надёжный, но только после трёх поправок, каждая из
которых иначе объявляла дефектом верный текст:

  1. Английский пишет время двенадцатичасовым циферблатом: «19 Uhr» → «7 pm».
     Девять правильных примеров из четырнадцати разобранных были помечены зря.
  2. Разделитель тысяч у языков разный: «50000», «50,000», «50 000» и немецкое
     «50.000» — одно число. Три записи «Preisgeld» попали в дефекты именно так.
  3. Шаблон разделителя дважды приезжал с символом backspace вместо границы
     слова — экранирование в оболочке ломало «\\b», — и проверка молча ничего
     не склеивала. Поэтому ниже есть самопроверка шаблонов перед работой.

ЧИСЛА В ПЕРЕВОДЕ НЕТ ВОВСЕ — слабее: число могло быть записано словом, в том
числе порядковым («o siódmej», «о п'ятнадцятій годині»). Числительные словами
здесь перечислены, иначе проверка кричит на правильный текст: в первой версии
так вышло у пяти случаев из восемнадцати.

    python -m app.scripts.example_number_mismatch
    python -m app.scripts.example_number_mismatch --only-different
    python -m app.scripts.example_number_mismatch --out number_defects.jsonl
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
os.environ.setdefault("ENV_FILE", ".env.local")

from sqlalchemy import create_engine, text

from app.config import settings
from app.services.language_service import LANGUAGES

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("number-mismatch")

LANGS = ("ru", "uk", "en", "tr", "pl", "it", "es", "fr", "cs")

DIGITS = re.compile(r"\d+")

# Разделитель тысяч: запятая, точка (так пишет немецкий), обычный и неразрывный
# пробел. Ровно три цифры после разделителя не дают съесть десятичную точку:
# «10.000» склеивается, «3.5» нет.
THOUSANDS = re.compile(r"(?<=\d)[,.   ](?=\d{3}(?!\d))")

# Числительные словами, включая порядковые. Корень короткий, дальше любые
# окончания: иначе пришлось бы перечислять «пятой», «пятому», «пятым».
NUMERAL_WORDS = {
    "ru": r"(ноль|один|одна|одно|перв|два|две|втор|три|трет|четыр|четвёрт|четверт|"
          r"пят|шест|семь|седьм|восем|восьм|девят|десят|одиннадцат|двенадцат|"
          r"тринадцат|четырнадцат|пятнадцат|шестнадцат|семнадцат|восемнадцат|"
          r"девятнадцат|двадцат|тридцат|сорок|сорока|пятьдесят|шестьдесят|"
          r"сто|двест|трист|четырест|пятьсот|тысяч|миллион|полов|пол)",
    "uk": r"(нуль|один|одна|одне|перш|два|дві|друг|три|трет|чотир|четверт|"
          r"п.ят|шіст|сім|сьом|вісім|восьм|дев.ят|десят|одинадцят|дванадцят|"
          r"тринадцят|чотирнадцят|п.ятнадцят|шістнадцят|сімнадцят|вісімнадцят|"
          r"дев.ятнадцят|двадцят|тридцят|сорок|п.ятдесят|шістдесят|"
          r"сто|двіст|трист|чотирист|п.ятсот|тисяч|мільйон|полов|пів)",
    "en": r"(zero|one|first|two|second|three|third|four|five|fif|six|seven|"
          r"eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|"
          r"seventeen|eighteen|nineteen|twent|thirt|fort|sixt|sevent|"
          r"ninet|hundred|thousand|million|half|noon|midnight)",
    "tr": r"(sıfır|bir|iki|üç|dört|beş|altı|yedi|sekiz|dokuz|on|yirmi|otuz|"
          r"kırk|elli|altmış|yetmiş|seksen|doksan|yüz|bin|milyon|yarım|buçuk)",
    "pl": r"(zero|jeden|jedna|pierwsz|dwa|dwie|drug|trzy|trzec|czter|czwart|"
          r"pięć|piąt|sześć|szóst|siedem|siódm|osiem|ósm|dziewięć|dziewiąt|"
          r"dziesięć|dziesiąt|jedenast|dwanast|dwunast|trzynast|czternast|"
          r"piętnast|szesnast|siedemnast|osiemnast|dziewiętnast|dwadzieścia|"
          r"dwudziest|trzydziest|czterdziest|pięćdziesiąt|sto|stu|dwieście|"
          r"dwustu|trzysta|tysiąc|milion|pół|połow|południ)",
    # Новые языки — с границей слова в начале: короткие корни «un», «tre»,
    # «dos», «sei» без неё совпали бы внутри любого слова
    "it": r"\b(zero|un|uno|una|prim|due|second|tre|terz|quattr|quart|cinque|"
          r"quint|sei|sest|sette|settim|otto|ottav|nove|non[oa]\b|dieci|decim|"
          r"undic|dodic|tredic|quattordic|quindic|sedic|diciasset|diciott|"
          r"diciannov|vent|trent|quarant|cinquant|sessant|settant|ottant|"
          r"novant|cent|mille|mila|milion|miliard|mezz|metà|dozzin)",
    "es": r"\b(cero|un|uno|una|primer|dos|segund|tres|tercer|cuatro|cuart|"
          r"cinco|quint|seis|sext|siete|séptim|ocho|octav|nueve|noven|diez|"
          r"décim|once|doce|trece|catorce|quince|dieci|veint|treint|cuarent|"
          r"cincuent|sesent|setent|ochent|novent|cien|cient|doscient|trescient|"
          r"quinient|mil|millón|millon|medi|mitad|docena)",
    "fr": r"\b(zéro|un|une|premi|deux|second|trois|quatr|cinq|six|sept|huit|"
          r"neuf|neuv|dix|onze|douze|treize|quatorze|quinze|seize|vingt|"
          r"trente|quarante|cinquante|soixante|cent|mille|million|milliard|"
          r"demi|moitié|midi|minuit|douzaine)",
    "cs": r"\b(nul|jed|prv|dva|dvě|dvou|druh|tři|tří|třet|čtyř|čtvrt|pět|pát|"
          r"šest|šes|sedm|osm|devět|devát|deset|desát|jedenáct|dvanáct|"
          r"třináct|čtrnáct|patnáct|šestnáct|sedmnáct|osmnáct|devatenáct|"
          r"dvacet|dvacát|třicet|třicát|čtyřicet|padesát|šedesát|sedmdesát|"
          r"osmdesát|devadesát|sto|set|tisíc|milion|miliard|půl|polovin|"
          r"poledn|půlnoc|tucet)",
}


# Века в it, es, fr пишутся римскими цифрами: «Im 19. Jahrhundert» →
# «Nel XIX secolo», «En el siglo XIX», «Au XIXe siècle». Это то же число.
ROMAN_LANGS = {"it", "es", "fr"}
ROMAN = re.compile(r"\b[IVXLC]{2,}(e|ème)?\b")


def has_numeral_word(value: str, lang: str) -> bool:
    if lang in ROMAN_LANGS and ROMAN.search(value):
        return True
    return bool(re.search(NUMERAL_WORDS[lang], value, re.IGNORECASE))


def numbers_in(value: str) -> set[int]:
    """Числа строки как значения, с убранным разделителем тысяч."""
    return {int(found) for found in DIGITS.findall(THOUSANDS.sub("", value))}


def same_time_other_clock(german: set[int], native: set[int]) -> bool:
    """
    Одно и то же время в двадцатичетырёхчасовой и двенадцатичасовой записи.

    «Der Einlass ist ab 19 Uhr» → «Admission is from 7 pm» — перевод верный, а
    числа разные. По-английски такая запись — большинство.
    """
    if not german or not native:
        return False
    shifted = set(german)
    shifted |= {n - 12 for n in german if 13 <= n <= 24}
    shifted |= {n + 12 for n in german if 1 <= n <= 11}
    # Все числа перевода объяснимы — значит это та же мысль другим циферблатом
    return native <= shifted


def self_check() -> bool:
    """
    Проверка собственных шаблонов перед работой.

    Дважды они приезжали с символом backspace вместо границы слова, и проверка
    молча перестала склеивать разделитель тысяч. Молчаливый ноль читается как
    «всё хорошо», поэтому лучше упасть.
    """
    cases = [
        ("About 50,000 inhabitants", {50000}),
        ("10.000 Euro", {10000}),
        ("10 000 евро", {10000}),
        ("3.5 kg", {3, 5}),
        ("50000", {50000}),
        ("von 15 bis 19 Uhr", {15, 19}),
    ]
    for value, expected in cases:
        got = numbers_in(value)
        if got != expected:
            logger.error("самопроверка не прошла: %r дало %s, ожидалось %s",
                         value, got, expected)
            return False
    if not same_time_other_clock({19}, {7}):
        logger.error("самопроверка: 19 и 7 должны считаться одним временем")
        return False
    if same_time_other_clock({14}, {18}):
        logger.error("самопроверка: 14 и 18 — разное время, а признано одним")
        return False
    words_cases = [
        ("it", "Il treno parte alle sette", True),
        ("it", "Vado a casa", False),
        ("es", "Llego a las tres y media", True),
        ("es", "Hoy hace calor", False),
        ("fr", "Je pars à huit heures", True),
        ("fr", "Il fait beau", False),
        ("cs", "Vlak jede v osm hodin", True),
        ("cs", "Venku prší", False),
        ("fr", "Au XIXe siècle, le corset était à la mode", True),
        ("es", "En el siglo XIX el corsé estaba de moda", True),
    ]
    for lang, value, expected in words_cases:
        if has_numeral_word(value, lang) != expected:
            logger.error("самопроверка числительных: %s %r дало %s, ожидалось %s",
                         lang, value, not expected, expected)
            return False
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only-different", action="store_true",
                    help="только случаи, где числа есть в обоих и они разные")
    ap.add_argument("--show", type=int, default=16)
    ap.add_argument("--out")
    args = ap.parse_args()

    if not self_check():
        return 2

    columns = ["id", "word_de", "level::text AS level", "example_de"]
    for lang in LANGS:
        columns.append(LANGUAGES[lang].example_attr)

    engine = create_engine(settings.DATABASE_URL_SYNC)
    with engine.connect() as conn:
        rows = conn.execute(text(
            f"SELECT {', '.join(dict.fromkeys(columns))} FROM words "
            f"WHERE example_de ~ '[0-9]'"
        )).mappings().all()

    different: list[dict] = []
    missing: list[dict] = []

    for row in rows:
        german = (row["example_de"] or "").strip()
        german_numbers = numbers_in(german)
        if not german_numbers:
            continue

        for lang in LANGS:
            native = (row[LANGUAGES[lang].example_attr] or "").strip()
            if not native:
                continue
            native_numbers = numbers_in(native)

            record = {
                "id": row["id"], "word_de": row["word_de"], "level": row["level"],
                "lang": lang, "word": "", "example": native, "german": german,
            }
            if native_numbers:
                if german_numbers & native_numbers:
                    continue
                if same_time_other_clock(german_numbers, native_numbers):
                    continue
                # десятилетие двумя цифрами: «aus den 1960ern» → «ze 60. let»
                if native_numbers <= {n % 100 for n in german_numbers
                                      if 1000 <= n <= 2099 and n % 10 == 0}:
                    continue
                record["kind"] = "числа разные"
                record["german_numbers"] = sorted(german_numbers)
                record["native_numbers"] = sorted(native_numbers)
                different.append(record)
            elif not has_numeral_word(native, lang):
                record["kind"] = "числа в переводе нет"
                missing.append(record)

    print(f"=== немецких примеров с числом: {len(rows)} ===")
    print(f"  числа есть в обоих, но РАЗНЫЕ: {len(different)} строк, "
          f"{len({h['id'] for h in different})} слов")
    print(f"  числа в переводе нет вовсе:    {len(missing)} строк, "
          f"{len({h['id'] for h in missing})} слов")
    print()

    print("--- числа разные (признак надёжный) ---")
    for hit in different[:args.show]:
        print(f"  {hit['word_de']!r} {hit['level']} {hit['lang']}: "
              f"{hit['german_numbers']} против {hit['native_numbers']}")
        print(f"      de: {hit['german'][:62]}")
        print(f"      {hit['lang']}: {hit['example'][:62]}")

    if not args.only_different:
        print()
        print("--- числа в переводе нет (слабее: могло быть опущено осознанно) ---")
        for hit in missing[:args.show]:
            print(f"  {hit['word_de']!r} {hit['level']} {hit['lang']}")
            print(f"      de: {hit['german'][:62]}")
            print(f"      {hit['lang']}: {hit['example'][:62]}")

    chosen = different if args.only_different else different + missing
    if args.out and chosen:
        path = pathlib.Path(args.out)
        with path.open("w", encoding="utf-8") as out:
            for hit in chosen:
                out.write(json.dumps(hit, ensure_ascii=False) + "\n")
        print()
        logger.info("записано: %d → %s", len(chosen), path)

    return 0


if __name__ == "__main__":
    sys.exit(main())
