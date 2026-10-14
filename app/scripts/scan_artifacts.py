"""
Сплошной поиск следов правки в примерах — по урокам двух кругов вычитки.

Вычитка нашла два класса, которых формальные проверки не искали: стрелки
«→» с двумя вариантами (4 строки) и слеши с приклеенным переводом (9 строк).
Оба нашлись потом сплошным поиском за секунды. Значит дешевле искать
классы, а не ряды: читать глазами — часы, искать по шаблону — мгновение.

Здесь собраны шаблоны того, что в примере стоять не должно: словарная
статья, приклеенная к фразе; пометки в скобках; многоточия-заглушки;
повтор одного и того же текста; пример, равный переводу; чужой алфавит.

Самопроверка обязательна: шаблон проверяется на заведомо верных строках,
иначе он сам станет источником ложной тревоги.
"""

import re
import sys
from collections import defaultdict
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from app.config import settings  # noqa: E402

LANGS = ["de", "ru", "uk", "en", "tr", "pl"]
CYR = re.compile(r"[а-яёіїєґ]", re.IGNORECASE)
LAT = re.compile(r"[a-z]", re.IGNORECASE)

# Немецкие служебные слова: если стоят отдельным словом в НЕнемецкой колонке,
# это почти наверняка затесавшийся немецкий, как «Ich dom stoi w górach»
GERMAN_MARKERS = re.compile(
    r"(?<![\w])(ich|du|er|sie|wir|ihr|das|der|die|ein|eine|und|nicht|ist|sind|"
    r"haben|habe|hat|war|mit|für|auf|von|zu)(?![\w])", re.IGNORECASE)

CHECKS: dict[str, object] = {
    # Словарная статья, приклеенная к примеру: «Peace / quiet - There is peace»
    "перевод приклеен через тире":
        lambda s: bool(re.match(r"^[^.!?]{3,40}\s[-—–]\s[A-ZА-ЯЇІЄҐ]", s)),
    # Пометка в скобках внутри примера
    "скобки в примере":
        lambda s: bool(re.search(r"\([^)]{2,}\)", s)),
    # Многоточие-заглушка
    "многоточие":
        lambda s: "..." in s or "…" in s,
    # Квадратные скобки, фигурные, подстановки
    "служебные скобки":
        lambda s: bool(re.search(r"[\[\]{}<>]", s)),
    # Два пробела подряд или пробел перед запятой
    "лишние пробелы":
        lambda s: "  " in s or bool(re.search(r"\s[,.!?]", s)),
    # Точка в конце — в этой базе её намеренно нет
    "точка в конце":
        lambda s: s.rstrip().endswith(".") and not s.rstrip().endswith("..."),
    # Пример из одного слова — употребления по нему не видно
    "пример из одного слова":
        lambda s: len(s.split()) < 2,
}

# Строки, на которых шаблоны НЕ должны срабатывать
MUST_PASS = [
    "There is peace here",
    "Бардак devrildi",
    "Ich trinke Wasser",
    "Co to był za odgłos?",
    "Я п'ю воду",
]
# Строки, на которых шаблоны ДОЛЖНЫ срабатывать, с именем шаблона
MUST_FLAG = [
    ("Peace / quiet - There is peace here", "перевод приклеен через тире"),
    ("Он пришёл (разг.) вчера", "скобки в примере"),
    ("Это только начало...", "многоточие"),
    ("Текст [вставить]", "служебные скобки"),
    ("Два  пробела", "лишние пробелы"),
    ("Фраза с точкой.", "точка в конце"),
    ("Слово", "пример из одного слова"),
]

print("=== самопроверка шаблонов ===")
bad = False
for s in MUST_PASS:
    for name, fn in CHECKS.items():
        if fn(s):
            print(f"  ПРОВАЛ: {name!r} зря сработал на {s!r}")
            bad = True
for s, expect in MUST_FLAG:
    if not CHECKS[expect](s):
        print(f"  ПРОВАЛ: {expect!r} не сработал на {s!r}")
        bad = True
if bad:
    sys.exit("шаблоны ненадёжны — работать с ними нельзя")
print("  шаблоны отличают верное от битого\n")

engine = create_engine(settings.DATABASE_URL_SYNC)
cols = ["id", "word_de"] + [f"example_{l}" for l in LANGS] + \
       [f"translation_{l}" for l in LANGS if l != "de"]
with engine.connect() as conn:
    rows = conn.execute(text(f"SELECT {', '.join(cols)} FROM words")).mappings().all()

found: dict[str, list] = defaultdict(list)

for r in rows:
    for lang in LANGS:
        ex = (r[f"example_{lang}"] or "").strip()
        if not ex:
            continue
        for name, fn in CHECKS.items():
            if fn(ex):
                found[name].append((r["id"], r["word_de"], lang, ex))

        # чужой алфавит: кириллица в латинской колонке и наоборот
        if lang in ("ru", "uk") and len(LAT.findall(ex)) > 3 and not CYR.search(ex):
            found["кириллическая колонка без кириллицы"].append(
                (r["id"], r["word_de"], lang, ex))
        if lang in ("en", "tr", "pl", "de") and CYR.search(ex):
            found["кириллица в латинской колонке"].append(
                (r["id"], r["word_de"], lang, ex))
        # немецкие служебные слова вне немецкой колонки
        if lang != "de":
            hits = GERMAN_MARKERS.findall(ex)
            # «die» есть и в польском, «ist» нет; требуем два разных маркера
            if len(set(h.lower() for h in hits)) >= 2 and lang in ("ru", "uk", "tr"):
                found["немецкие слова в чужой колонке"].append(
                    (r["id"], r["word_de"], lang, ex))

    # пример совпадает с переводом — употребления по нему не видно
    for lang in LANGS:
        if lang == "de":
            continue
        ex = (r[f"example_{lang}"] or "").strip().lower()
        tr = (r[f"translation_{lang}"] or "").strip().lower()
        if ex and ex == tr:
            found["пример равен переводу"].append(
                (r["id"], r["word_de"], lang, ex))

print(f"=== проверено слов: {len(rows)} ===\n")
for name in sorted(found, key=lambda k: -len(found[k])):
    items = found[name]
    print(f"{name}: {len(items)}")
    for wid, de, lang, val in items[:8]:
        print(f"    {wid:>6} {de:<18} {lang}: {val!r}")
    if len(items) > 8:
        print(f"    ... ещё {len(items) - 8}")
    print()
if not found:
    print("ничего не найдено")
