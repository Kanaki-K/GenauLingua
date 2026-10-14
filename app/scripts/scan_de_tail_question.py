"""
ВОСЬМОЙ ГЕЙТ. Немецкий пример кончается вопросом, а знака вопроса нет.

Найдено вычиткой блока 48:

    Verstärker (17679) «Der Gitarrenverstärker ist zu laut, kannst du ihn
                        leiser stellen»

Вторая часть — вопрос с инверсией («kannst du»), и фраза им кончается, а
знака нет. Все пять переводов повторили немецкий без знака. Близнец того
же ряда, `Lautstärke` (17683), знак имеет: «Die Lautstärke ist zu hoch,
kannst du sie runterdrehen?» — то есть внутри базы норма уже задана, и
ряд из неё выпадает.

ПОЧЕМУ ЭТО ОТДЕЛЬНАЯ ПРИМЕТА, А НЕ ЧАСТЬ `scan_question_mark`. Та ловит
вопрос, который НАЧИНАЕТСЯ вопросительным словом («Wie geht's dir»).
Здесь вопросительного слова нет вовсе: вопрос узнаётся по ИНВЕРСИИ —
личная форма глагола стоит перед подлежащим. Начало фразы при этом
утвердительное, и первая примета проходит мимо.

ГРАНИЦА ЗАДАНА ДО ПРОГОНА, ИЗ ГРАММАТИКИ. Инверсия в немецком бывает не
только в вопросе, поэтому берутся только однозначные зачины: модальный
или вспомогательный глагол во втором лице («kannst du», «hast du»,
«können Sie»). И вопрос должен стоять в ПОСЛЕДНЕЙ клаузе — иначе знак
законно стоит внутри фразы, а фраза кончается утверждением:

    Taschentuch (7177) «Hast du ein Taschentuch? Ich muss mir die Nase
                        putzen»          ← знак внутри, это норма

Замер по всей базе: 9 фраз с вопросительным зачином и без знака на конце,
из них 8 — ровно такие, со знаком внутри. Дефект один. Поэтому примета
ограничена последней клаузой и сделана ГЕЙТОМ: законного остатка у неё
нет, любое попадание — дефект.

    python -m app.scripts.scan_de_tail_question
    python -m app.scripts.scan_de_tail_question --selfcheck
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# Однозначные вопросительные зачины: личная форма глагола + местоимение.
STARTS = (
    "kannst du", "könntest du", "könnt ihr", "können Sie", "könnten Sie",
    "willst du", "wollt ihr", "wollen Sie",
    "möchtest du", "möchten Sie",
    "hast du", "habt ihr", "haben Sie", "hättest du",
    "bist du", "seid ihr", "sind Sie",
    "darf ich", "darfst du", "dürfen Sie",
    "würdest du", "würden Sie",
    "machst du", "magst du", "weißt du", "wissen Sie",
    "gehst du", "kommst du", "brauchst du", "siehst du", "hilfst du",
)

_START_RE = re.compile("|".join(re.escape(s) for s in STARTS), re.I)
# Клауза кончается на . ? ! или … ; внутри фразы части делит запятая, тире,
# точка с запятой и двоеточие.
_SPLIT_RE = re.compile(r"[,;:–—]|\s-\s")


def tail_clause(example: str) -> str:
    """Последняя часть фразы после последнего разделителя."""
    parts = _SPLIT_RE.split(example)
    return parts[-1].strip() if parts else ""


def is_defect(example: str) -> bool:
    text_ = (example or "").strip()
    if not text_ or text_.endswith("?"):
        return False
    # знак вопроса где-то внутри — значит вопрос уже закрыт, а фраза
    # продолжается утверждением; это норма
    if "?" in text_:
        return False
    tail = tail_clause(text_)
    if not tail:
        return False
    match = _START_RE.match(tail)
    return match is not None


def selfcheck() -> int:
    good = [
        "Hast du ein Taschentuch? Ich muss mir die Nase putzen",
        "Die Lautstärke ist zu hoch, kannst du sie runterdrehen?",
        "Kannst du mir helfen?",
        "Er ist zu laut, ich kann nichts hören",
        "Kommst du mit? – Nee, keine Lust",
        "Du hast das Buch gelesen",
    ]
    bad = [
        "Der Gitarrenverstärker ist zu laut, kannst du ihn leiser stellen",
        "Das Fenster ist offen, kannst du es zumachen",
        "Ich habe Hunger, hast du etwas zu essen",
    ]
    failures = 0
    for phrase in good:
        if is_defect(phrase):
            print(f"GOOD помечен дефектом: {phrase!r}")
            failures += 1
    for phrase in bad:
        if not is_defect(phrase):
            print(f"BAD не помечен: {phrase!r}")
            failures += 1
    if failures:
        print(f"САМОПРОВЕРКА ПРОВАЛЕНА: {failures}")
        return 1
    print(f"самопроверка: {len(good)} верных и {len(bad)} битых различены")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--selfcheck", action="store_true")
    args = parser.parse_args()

    if args.selfcheck:
        return selfcheck()

    engine = create_engine(settings.DATABASE_URL_SYNC)
    with engine.connect() as conn:
        rows = conn.execute(
            text("SELECT id, word_de, example_de FROM words ORDER BY id")
        ).mappings().all()

    hits = [r for r in rows if is_defect(r["example_de"] or "")]
    for r in hits:
        print(f"{r['id']:>6}  {r['word_de']:<24} {r['example_de']}")
    print(f"\nвсего: {len(hits)}")
    if hits:
        print("ГЕЙТ: вопрос на конце фразы без знака вопроса — дефект всегда")
        return 1
    print("ЧИСТО")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
