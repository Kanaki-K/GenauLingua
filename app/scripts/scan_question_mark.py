"""
Немецкий пример — вопрос, перевод выглядит утверждением.

Нашлось вычиткой: в первых трёх сотнях самых частых слов таких ячеек
оказалось около двадцати пяти. «Hast du eine Frage?» — «У тебя есть
вопрос», «Wann kommst du?» — «Ne zaman geliyorsun». На карточке немецкий и
перевод стоят стопкой друг под другом, и пара читается как небрежность.

Три проверки, разной надёжности:

1. **В немецком знак есть, в переводе нет** — надёжно. Вопрос остаётся
   вопросом в любом из пяти языков.
2. **В немецком знака нет, в переводе есть** — слабее, но почти всегда это
   значит, что знак потерян в самом немецком: «Wie geht's dir», «Was machen
   wir nun». Немецкий здесь эталон для пяти языков, и если он выглядит
   утверждением, за ним пойдут переводы.
3. **Немецкий начинается вопросительным словом, а знака нет** — отдельно,
   потому что это правка эталона, а не перевода.

Чего проверка НЕ делает. Она не трогает восклицательные знаки: «Komm rein!»
и «Заходи» — обе формы живые, и требовать совпадения значило бы ломать
нормальный текст. И не судит о том, вопрос ли фраза по смыслу: только по
знаку и по вопросительному слову в начале.

    python -m app.scripts.scan_question_mark
    python -m app.scripts.scan_question_mark --show 40
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

LANGS = ["en", "ru", "uk", "tr", "pl"]

# Немецкие вопросительные слова, однозначные в начале фразы. «Was für ein
# Tag» бывает и восклицанием, поэтому восклицательный знак в конце снимает
# подозрение — он проверяется отдельно.
GERMAN_QUESTION_START = re.compile(
    r"^(wer|wen|wem|wessen|was|wo|wohin|woher|wann|wie|warum|wieso|weshalb|"
    r"welche[rsnm]?|darf|dürfen|kann|kannst|könnt|könnte|hast|habt|hat|habe|"
    r"bist|ist|sind|seid|willst|wollt|möchtest|möchtet|soll|sollst|sollen)\b",
    re.IGNORECASE,
)


def is_question(s: str) -> bool:
    return s.rstrip().endswith("?")


# «Was die Bezahlung anbelangt, …» — это оборот «что касается», а не вопрос.
# На первом прогоне шаблон объявил его дефектом, и это ровно тот случай, из-за
# которого здесь есть самопроверка.
NOT_A_QUESTION = re.compile(
    r"^Was\b.*\b(anbelangt|anbetrifft|betrifft|angeht)\b"
    r"|^Was für ein",
    re.IGNORECASE,
)


def looks_like_question(s: str) -> bool:
    s = s.strip()
    if s.endswith("!"):
        return False
    # Знак уже стоит внутри: «Wo ist der Feuerlöscher? Ich kann ihn nicht
    # finden» — фраза из двух предложений, и она в порядке
    if "?" in s:
        return False
    if NOT_A_QUESTION.match(s):
        return False
    return bool(GERMAN_QUESTION_START.match(s))


# Самопроверка до работы: шаблон, который врёт, опаснее отсутствия проверки
MUST_BE_QUESTION = [
    "Wann kommst du",
    "Was machen wir nun",
    "Wie geht's dir",
    "Darf ich hier rauchen",
    "Hast du genug Geld",
    "Welches ist dein Sternzeichen",
]
MUST_NOT_BE_QUESTION = [
    "Ich bin Student",
    "Was für ein Tag!",          # восклицание, не вопрос
    "Was für ein Zufall",        # оно же без знака
    "Das ist nicht schwer",
    "Wir gehen nach Hause",
    "Istanbul ist schön",        # «Ist» внутри слова не считается
    "Sie kommen morgen vorbei",
    # Оборот «что касается» — не вопрос, хотя начинается с «Was»
    "Was die Bezahlung anbelangt, haben wir noch keine Einigung erzielt",
    # Два предложения, знак стоит внутри — здесь всё в порядке
    "Wo ist der Feuerlöscher? Ich kann ihn nicht finden",
    "Hast du ein Taschentuch? Ich muss mir die Nase putzen",
]


def selfcheck() -> None:
    print("=== самопроверка шаблонов ===")
    bad = False
    for s in MUST_BE_QUESTION:
        if not looks_like_question(s):
            print(f"  ПРОВАЛ: не распознан вопрос {s!r}")
            bad = True
    for s in MUST_NOT_BE_QUESTION:
        if looks_like_question(s):
            print(f"  ПРОВАЛ: зря признан вопросом {s!r}")
            bad = True
    if bad:
        sys.exit("шаблон ненадёжен — работать с ним нельзя")
    print("  шаблон отличает вопрос от утверждения\n")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--show", type=int, default=12, help="сколько примеров печатать")
    ap.add_argument("--pairs", action="store_true",
                    help="печатать немецкий и перевод рядом: так видно, "
                         "потерян ли только знак или вся вопросительная форма")
    ap.add_argument("--from", type=int, default=1, dest="start",
                    help="с какой пары начать (для разбора партиями)")
    ap.add_argument("--count", type=int, default=60,
                    help="сколько пар напечатать")
    args = ap.parse_args()

    selfcheck()

    cols = ["id", "word_de", "example_de"] + [f"example_{c}" for c in LANGS]
    engine = create_engine(settings.DATABASE_URL_SYNC)
    with engine.connect() as conn:
        rows = conn.execute(
            text(f"SELECT {', '.join(cols)} FROM words")
        ).mappings().all()

    found: dict[str, list] = defaultdict(list)

    for r in rows:
        de = (r["example_de"] or "").strip()
        if not de:
            continue
        de_q = is_question(de)

        if not de_q and looks_like_question(de):
            found["немецкий — вопрос, а знака нет"].append(
                (r["id"], r["word_de"], "de", de))

        for lang in LANGS:
            ex = (r[f"example_{lang}"] or "").strip()
            if not ex:
                continue
            if de_q and not is_question(ex):
                found["в немецком знак есть, в переводе нет"].append(
                    (r["id"], r["word_de"], lang, ex))
            elif not de_q and is_question(ex):
                found["в переводе знак есть, в немецком нет"].append(
                    (r["id"], r["word_de"], lang, ex))

    if args.pairs:
        items = found["в немецком знак есть, в переводе нет"]
        # Порядок устойчивый: партии не перемешиваются между запусками
        items.sort(key=lambda t: (t[0], t[2]))
        block = items[args.start - 1: args.start - 1 + args.count]
        print(f"=== пары {args.start}–{args.start + len(block) - 1} "
              f"из {len(items)} ===\n")
        de_by_id = {r["id"]: (r["example_de"] or "").strip() for r in rows}
        for number, (wid, word, lang, val) in enumerate(block, args.start):
            print(f"{number}. {wid} {word}")
            print(f"     de  {de_by_id[wid]}")
            print(f"     {lang}  {val}")
        print(f"\nследующая партия: --from {args.start + len(block)}")
        return

    print(f"=== проверено слов: {len(rows)} ===\n")
    for name in sorted(found, key=lambda k: -len(found[k])):
        items = found[name]
        print(f"{name}: {len(items)}")
        for wid, de, lang, val in items[: args.show]:
            print(f"    {wid:>6} {de:<18} {lang}: {val!r}")
        if len(items) > args.show:
            print(f"    ... ещё {len(items) - args.show}")
        print()
    if not found:
        print("ничего не найдено")


if __name__ == "__main__":
    main()
