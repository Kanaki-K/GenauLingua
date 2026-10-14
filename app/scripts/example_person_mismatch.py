#!/usr/bin/env python3
"""
Пример-перевод не соответствует немецкому примеру: разное лицо подлежащего.

«Ich schneide gerade das Brot» и «Он режет хлеб острым ножом» — это не перевод,
а другое предложение. В разборе после ответа оба примера показываются рядом, и
такая пара читается как плохой перевод, подрывая доверие ко всей базе.

Чем эта проверка отличается от example_quality. Тот ищет, есть ли слово в
примере вообще; здесь слово есть, и он проходит мимо. Нашлось разбором глазами:
в выборке из 55 рядов C1 и C2 таких оказалось пять.

Сравнивается только подлежащее и только в однозначных случаях — «ich», «du»,
«wir» в немецком. Поэтому найденное это нижняя оценка, а не весь объём:

  - третье лицо не проверяется: немецкое «sie» это и «она», и «они», и
    вежливое «Вы», формально не различить;
  - турецкий не проверяется: местоимение там обычно опускается, лицо выражено
    окончанием глагола.

    python -m app.scripts.example_person_mismatch
    python -m app.scripts.example_person_mismatch --lang uk --show 30
    python -m app.scripts.example_person_mismatch --out person_defects.jsonl
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
logger = logging.getLogger("person-mismatch")

# Лицо в немецком примере. Третьего здесь нет намеренно — см. заголовок.
GERMAN_PERSON = {
    "1s": r"\bich\b",
    "2s": r"\bdu\b",
    "1p": r"\bwir\b",
}

# Лицо в переводе — ТОЛЬКО ИМЕНИТЕЛЬНЫЙ ПАДЕЖ.
#
# Первая версия искала любые формы местоимений и врала. «Kannst du mir die
# Schuhe binden?» → «Можешь мне завязать шнурки?» — перевод верный: русский
# опускает подлежащее, лицо выражено глаголом, а «мне» отвечает немецкому
# «mir». Проверка видела «мне», не находила «ты» и объявляла расхождение. Из
# шести разобранных находок пять оказались такими.
#
# Косвенные падежи подлежащим не бывают, поэтому их здесь нет. Гендерное
# расхождение («Er will spielen» → «Вона хоче грати», потому что собака
# по-украински женского рода) уходит само: третье лицо не сравнивается с
# первым и вторым.
PERSON = {
    "ru": {
        "1s": r"\bя\b",
        "2s": r"\bты\b",
        "3s": r"\b(он|она|оно)\b",
        "1p": r"\bмы\b",
    },
    "uk": {
        "1s": r"\bя\b",
        "2s": r"\bти\b",
        "3s": r"\b(він|вона|воно)\b",
        "1p": r"\bми\b",
    },
    "en": {
        "1s": r"\bI\b",
        "2s": r"\byou\b",
        "3s": r"\b(he|she|it)\b",
        "1p": r"\bwe\b",
    },
    "pl": {
        "1s": r"\bja\b",
        "2s": r"\bty\b",
        "3s": r"\b(on|ona|ono)\b",
        "1p": r"\bmy\b",
    },
}


def found(pattern: str, value: str) -> bool:
    return bool(re.search(pattern, value, re.IGNORECASE))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lang", choices=sorted(PERSON), default=None,
                    help="один язык вместо всех проверяемых")
    ap.add_argument("--show", type=int, default=14)
    ap.add_argument("--out", help="сохранить находки в JSONL для правки примеров")
    args = ap.parse_args()

    # Проверка собственных шаблонов перед работой. Однажды они приехали с
    # символом backspace вместо границы слова — экранирование в оболочке
    # испортило «\b», — и проверка показала ноль расхождений на всей базе.
    # Молчаливый ноль хуже ошибки: он читается как «всё хорошо».
    for lang, table in PERSON.items():
        for key, pattern in table.items():
            if "\b" in pattern:
                logger.error("шаблон %s/%s содержит backspace вместо границы слова: %r",
                             lang, key, pattern)
                return 2
    if not found(PERSON["ru"]["3s"], "Он весь день ходит"):
        logger.error("шаблоны не работают: «Он» не опознан как третье лицо")
        return 2

    langs = [args.lang] if args.lang else sorted(PERSON)
    columns = ["id", "word_de", "level::text AS level", "example_de"]
    for lang in langs:
        columns.append(LANGUAGES[lang].example_attr)

    engine = create_engine(settings.DATABASE_URL_SYNC)
    with engine.connect() as conn:
        rows = conn.execute(text(
            f"SELECT {', '.join(dict.fromkeys(columns))} FROM words "
            f"WHERE example_de IS NOT NULL AND btrim(example_de) <> ''"
        )).mappings().all()

    hits: list[dict] = []
    checked = {lang: 0 for lang in langs}

    for row in rows:
        german = (row["example_de"] or "").strip()
        if not german:
            continue
        person = next((key for key, pattern in GERMAN_PERSON.items()
                       if found(pattern, german)), None)
        if person is None:
            continue

        for lang in langs:
            native = (row[LANGUAGES[lang].example_attr] or "").strip()
            if not native:
                continue
            checked[lang] += 1
            table = PERSON[lang]
            if found(table[person], native):
                continue
            # Своего подлежащего нет. Есть ли чужое — иначе это безличный
            # перевод или опущенное местоимение, и придираться не к чему
            other = next((key for key in table if key != person
                          and found(table[key], native)), None)
            if other is None:
                continue
            hits.append({
                "id": row["id"], "word_de": row["word_de"], "level": row["level"],
                "lang": lang, "word": "", "example": native,
                "german": german, "german_person": person, "native_person": other,
            })

    total = sum(checked.values())
    print(f"=== примеров с явным подлежащим в немецком: {total} ===")
    for lang in langs:
        lang_hits = [h for h in hits if h["lang"] == lang]
        share = len(lang_hits) / checked[lang] * 100 if checked[lang] else 0
        print(f"  {lang}: проверено {checked[lang]}, расхождений {len(lang_hits)} "
              f"({share:.1f}%)")
    print()

    for hit in hits[:args.show]:
        print(f"  {hit['word_de']!r} {hit['level']} {hit['lang']}: "
              f"немецкий {hit['german_person']}, перевод {hit['native_person']}")
        print(f"      de: {hit['german'][:64]}")
        print(f"      {hit['lang']}: {hit['example'][:64]}")

    if args.out and hits:
        path = pathlib.Path(args.out)
        with path.open("w", encoding="utf-8") as out:
            for hit in hits:
                out.write(json.dumps(hit, ensure_ascii=False) + "\n")
        print()
        logger.info("находок записано: %d → %s", len(hits), path)
        logger.warning(
            "Правятся тем же прогоном, что и прочие дефекты примеров:\n"
            "    python -m app.scripts.fix_examples propose --in %s", path,
        )

    print()
    print("Это нижняя оценка: третье лицо и турецкий не проверяются — "
          "немецкое «sie» неоднозначно, а турецкий опускает местоимение.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
