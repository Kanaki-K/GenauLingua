"""
Часть речи перевода против заголовка — сплошной поиск.

Повод. У `pflücken` заголовок инфинитив, а все пять переводов стояли
причастием: «сорванный, picked, zerwany, toplanmış». Человек учил не ту
форму. Нашлось вычиткой; проверяю, единичный ли это случай.

Для глаголов признак формальный и надёжный:
  en — инфинитив с «to»
  tr — на -mak/-mek
  pl — на -ć (есть исключения вроде «być», но они тоже на -ć)
  ru/uk — на -ть/-ти/-чь/-ся/-ся

Проверяется только ПЕРВОЕ значение: именно оно показывается на карточке и
звучит в клипе. Если первое значение не того рода, человек видит не то.

ЧЕГО ПРОВЕРКА НЕ ДЕЛАЕТ. Существительные и прилагательные формально не
отличить: «красный» и «краснота» по окончанию не разделить без словаря.
Поэтому здесь только глаголы — там, где признак однозначен.

Самопроверка на заведомо верных и заведомо битых строках обязательна.
"""

import re
import sys
from collections import defaultdict
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from app.config import settings  # noqa: E402

SPLIT = re.compile(r"[/;,]")


def first_meaning(s: str) -> str:
    parts = [p.strip() for p in SPLIT.split(s or "") if p.strip()]
    return parts[0] if parts else ""


# Глагол ищется в ЛЮБОМ слове оборота, а не в последнем.
#
# Первая версия проверки смотрела только конец строки и объявила дефектом
# 1175 строк — почти половину всех глаголов. Все до единой были исправны:
# «снимать деньги», «cieszyć się», «считать способным» — это глаголы, просто
# многословные, и кончаются они существительным или частицей. Проверка,
# которая врёт в половине случаев, хуже её отсутствия.

def _any_word(s: str, test) -> bool:
    return any(test(w) for w in re.split(r"[\s'’-]+", s.strip()) if w)


# Модальные глаголы «to» не берут: can, must, may, should. Это не дефект.
EN_MODALS = {"can", "must", "may", "might", "should", "would like", "shall"}


def is_verb_en(s: str) -> bool:
    low = s.lower().strip()
    return low.startswith("to ") or low in EN_MODALS


def is_verb_tr(s: str) -> bool:
    return _any_word(s, lambda w: bool(re.search(r"(mak|mek)$", w, re.IGNORECASE)))


def is_verb_pl(s: str) -> bool:
    # się — возвратная частица, сам глагол рядом. Инфинитив кончается на ć,
    # но часть глаголов — на голое c: móc, piec, biec, uciec, strzec.
    return _any_word(s, lambda w: w.lower().endswith(("ć", "c")))


def is_verb_ru(s: str) -> bool:
    return _any_word(
        s, lambda w: bool(re.search(r"(ть|ться|ти|тися|чь|чься)$", w, re.IGNORECASE)))


VERB_CHECK = {
    "en": is_verb_en,
    "tr": is_verb_tr,
    "pl": is_verb_pl,
    "ru": is_verb_ru,
    "uk": is_verb_ru,
}

# (язык, строка, должно ли считаться глаголом)
CASES = [
    ("en", "to pick", True), ("en", "picked", False), ("en", "picture", False),
    ("en", "can", True), ("en", "must", True),
    ("tr", "toplamak", True), ("tr", "toplanmış", False), ("tr", "kitap", False),
    ("pl", "zrywać", True), ("pl", "zerwany", False), ("pl", "książka", False),
    ("ru", "срывать", True), ("ru", "сорванный", False), ("ru", "книга", False),
    ("ru", "снимать деньги", True), ("ru", "считать способным", True),
    ("pl", "cieszyć się", True), ("pl", "walić młotkiem", True),
    ("pl", "móc", True), ("pl", "uciec", True), ("pl", "piec", True),
    ("tr", "para çekmek", True), ("tr", "kitap okumak", True),
    ("uk", "зривати", True), ("uk", "зірваний", False), ("uk", "книга", False),
]

print("=== самопроверка ===")
bad = False
for lang, s, expect in CASES:
    got = VERB_CHECK[lang](s)
    if got != expect:
        print(f"  ПРОВАЛ {lang}: {s!r} ожидалось {expect}, вышло {got}")
        bad = True
if bad:
    sys.exit("проверка ненадёжна")
print("  признак глагола отличает инфинитив от причастия\n")

engine = create_engine(settings.DATABASE_URL_SYNC)
langs = list(VERB_CHECK)
cols = ["id", "word_de", "pos", "level"] + [f"translation_{l}" for l in langs]
with engine.connect() as conn:
    rows = conn.execute(
        text(f"SELECT {', '.join(cols)} FROM words WHERE pos::text = 'VERB'")
    ).mappings().all()

print(f"=== немецких глаголов в базе: {len(rows)} ===\n")

found = defaultdict(list)
for r in rows:
    for lang in langs:
        val = first_meaning(r[f"translation_{lang}"] or "")
        if not val:
            continue
        if not VERB_CHECK[lang](val):
            found[lang].append((r["id"], r["word_de"], r["level"], val,
                                r[f"translation_{lang}"]))

total = sum(len(v) for v in found.values())
print(f"первое значение не глагол: {total}\n")
for lang in sorted(found, key=lambda k: -len(found[k])):
    items = found[lang]
    print(f"--- {lang}: {len(items)} ---")
    for wid, de, lvl, first, full in items[:14]:
        print(f"  {wid:>6} [{lvl}] {de:<18} → {first!r}   (вся ячейка: {full!r})")
    if len(items) > 14:
        print(f"  ... ещё {len(items) - 14}")
    print()
