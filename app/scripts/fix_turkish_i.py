#!/usr/bin/env python3
"""
Заглавная I вместо İ в турецких переводах.

По-турецки «I» и «İ» — разные буквы, а не разное оформление одной. «I» —
заглавная от «ı» (задний неогублённый гласный), «İ» — от «i» (передний).
Написание «Iyimser» вместо «İyimser» меняет чтение, и озвучка произносит такое
слово неправильно.

Дефект системный и повторяющийся: прогон переводов ставит латинскую I всюду,
где нужна İ. На первом прогоне так оказалось 429 строк из 12 902. Поэтому это
не разовая правка, а шаг, который нужно повторять после каждого прогона
турецких переводов.

Слепая замена невозможна: в турецком есть настоящие слова с ı в начале —
«ışık» (свет), «ıslak» (мокрый), «ızgara» (решётка), «ırk» (раса). В базе они
есть, и их порча была бы такой же ошибкой. На первом прогоне таких нашлось 23.

Почему список дотless-основ надёжен. Турецкая гармония гласных: за начальным
«ı» идут задние гласные (ı, a, o, u), за начальным «i» — передние (i, e, ö, ü).
Поэтому «ısı-» и «isi-», «ılık» и «ilik», «ıtır» и «itir-» расходятся уже на
второй букве, и различить их можно формально. Список ниже закрытый: всё, что
в него не попало, по-турецки пишется через İ.

Направление списка выбрано так намеренно. Перечислять «основы через İ»
пришлось бы почти для всего турецкого словаря, а дотless-начал в языке
десятка два, и их можно выписать и проверить целиком.

    python -m app.scripts.fix_turkish_i --review     # решение по каждому слову
    python -m app.scripts.fix_turkish_i              # пробный прогон
    python -m app.scripts.fix_turkish_i --apply
"""
from __future__ import annotations

import argparse
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
logger = logging.getLogger("turkish-i")

# Продолжения слова после начальной ı — то есть без первой буквы. Совпадение
# ищется по самому длинному подходящему, чтобы «ışık» не спутался с «iş».
DOTLESS_RESTS = (
    "şı",                    # ışık, ışıl, ışın — свет, луч. Против «işi-», «işe-»
    "sı",                    # ısı, ısıtma, ısırmak. Против «isim», «isyan»
    "sla", "slı", "slah",    # ıslak, ıslık, ıslanmak, ıslah. Против «islam»
    "rk",                    # ırk, ırkçı. Дотted слов на «irk-» в турецком нет
    "rmak", "rgat", "rz",    # ırmak (река), ırgat, ırz
    "lık", "lıman", "lım",   # ılık (тёплый), ılıman. Против «ilik» (костный мозг)
    "zgara", "zdırap",       # ızgara (решётка), ızdırap
    "hlamur",                # ıhlamur — липа
    "spanak", "stakoz", "stırap", "skarta", "skala",
    "ssız",                  # ıssız — безлюдный
    "smarla",                # ısmarlamak — заказывать
    "tır",                   # ıtır — герань. Против «itiraf», «itiraz»
    "vır",                   # ıvır zıvır
)

# Сначала длинные: «şı» не должно перехватить то, что разрешает «slah»
DOTLESS_SORTED = tuple(sorted(DOTLESS_RESTS, key=len, reverse=True))

# Иностранные слова, сохраняющие исходное написание. У них вторая буква
# строчная, поэтому правило про аббревиатуры их не отсеивает, а турецкая
# орфография на них не распространяется: «Intercity» — название поезда и в
# немецкой колонке стоит так же, «Inline» — часть «Inline paten».
KEEP_LATIN = ("intercity", "inline")

WORD = re.compile(r"(?<!\w)I(\w+)", re.UNICODE)


def classify(rest: str) -> str:
    """dotless — оставить I, dotted — заменить на İ, foreign — не трогать."""
    # Аббревиатуры: IBAN, IT, DVD. Заглавная вторая буква значит, что это не
    # турецкое слово в обычном написании
    if rest[:1].isupper():
        return "foreign"
    lowered = rest.lower()
    if any(("i" + lowered).startswith(word) for word in KEEP_LATIN):
        return "foreign"
    for stem in DOTLESS_SORTED:
        if lowered.startswith(stem):
            return "dotless"
    return "dotted"


def fix(value: str) -> str:
    def replace(match: re.Match) -> str:
        rest = match.group(1)
        return "İ" + rest if classify(rest) == "dotted" else match.group(0)

    return WORD.sub(replace, value)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--review", action="store_true",
                    help="напечатать решение по каждому слову для разбора глазами")
    args = ap.parse_args()

    attr = LANGUAGES["tr"].word_attr
    example_attr = LANGUAGES["tr"].example_attr

    engine = create_engine(settings.DATABASE_URL_SYNC)
    with engine.connect() as conn:
        rows = conn.execute(text(
            f"SELECT id, word_de, {attr} AS w, {example_attr} AS e FROM words"
        )).mappings().all()

    decisions: dict[str, str] = {}
    counts = {"dotted": 0, "dotless": 0, "foreign": 0}
    updates: list[dict] = []
    samples: list[str] = []

    for row in rows:
        word = (row["w"] or "").strip()
        example = (row["e"] or "").strip()

        for match in WORD.finditer(f"{word} {example}"):
            token = match.group(0)
            if token not in decisions:
                decisions[token] = classify(match.group(1))
                counts[decisions[token]] += 1

        new_word, new_example = fix(word), fix(example)
        if (new_word, new_example) == (word, example):
            continue
        updates.append({"id": row["id"], "w": new_word, "e": new_example})
        if len(samples) < 10:
            changed = (f"{word} → {new_word}" if new_word != word
                       else f"{example} → {new_example}")
            samples.append(f"    {row['word_de']!r:<18} {changed}")

    print(f"=== заглавная I в турецкой колонке: {len(decisions)} разных слов ===")
    print(f"  → İ (дотted):         {counts['dotted']}")
    print(f"  оставить I (дотless): {counts['dotless']}")
    print(f"  иностранные:          {counts['foreign']}")
    print(f"  строк к правке:       {len(updates)}")
    print()

    if args.review:
        for verdict in ("dotless", "foreign", "dotted"):
            chosen = sorted(t for t, v in decisions.items() if v == verdict)
            if not chosen:
                continue
            mark = {"dotless": "оставлено как ı",
                    "foreign": "иностранное, не тронуто",
                    "dotted": "заменено на İ"}[verdict]
            print(f"--- {mark} ({len(chosen)}) ---")
            for start in range(0, len(chosen), 6):
                print("   " + "  ".join(f"{t:<15}" for t in chosen[start:start + 6]))
            print()
    else:
        print("\n".join(samples))
        print()

    if not updates:
        print("править нечего")
        return 0

    if not args.apply:
        print("  (пробный прогон, для применения --apply)")
        return 0

    with engine.begin() as conn:
        conn.execute(text(
            f"UPDATE words SET {attr} = :w, {example_attr} = :e WHERE id = :id"
        ), updates)

    logger.info("применено: %d строк", len(updates))
    logger.warning(
        "Турецкий текст изменился — нужен пересинтез:\n"
        "    python -m app.scripts.tts_synthesize --lang tr\n"
        "И пересборка групп: переводы входят в ключ схлопывания.\n"
        "    python -m app.scripts.rebuild_word_groups"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
