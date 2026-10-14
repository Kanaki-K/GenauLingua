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

ДЫРА, ЗАКРЫТАЯ В ТРЕТЬЕМ ПРОХОДЕ (блок 1). Вопросительное слово искалось
строго в НАЧАЛЕ фразы, и МЕЖДОМЕТИЕ С ЗАПЯТОЙ его прятало:

    Na  (13810, A1) «Na, wie geht's dir denn»     ← вопрос, знака нет
    Tja (13835, A1) «Tja, was soll ich sagen»     ← вопрос, знака нет

Оба ряда прожили два полных прохода. Близнецы в базе знак имеют —
`Moin` (14207) «Moin, wie geht's dir denn?», `hallo` (370), `wie` (1035),
то есть норма была задана, а эти два из неё выпадали в ШЕСТИ языках
каждый.

Замер перед правкой: «W-слово в начале фразы, можно после междометия, и
знака вопроса нет нигде» даёт по базе 5 попаданий. Три законные, и обе
отсечки для них в примете УЖЕ БЫЛИ — восклицание («Was für ein Zufall!»,
`Zufall` 6464, `Schweinerei` 10744) и оборот «что касается» («Was die
Bezahlung anbelangt», `anbelangen` 8250). Значит дыра была ровно одна:
якорь `^`. Теперь перед проверкой снимается ведущее междометие.

ВТОРАЯ ДЫРА, ЗАКРЫТАЯ В БЛОКЕ 7 ТРЕТЬЕГО ПРОХОДА, И ЗАКРЫТА ОНА
ГРАММАТИКОЙ, А НЕ СПИСКОМ. Список междометий из блока 1 поймал `Na` и
`Tja`, но пропустил ЗВАТЕЛЬНЫЕ ОБОРОТЫ, которых в списке нет и быть не
может — их бесконечно много:

    Herrgott      (13894, B2) «Herrgott, was ist denn hier passiert»
    Menschenskind (15311, B2) «Menschenskind, was hast du denn getan»
    Sau           (15459, B1) «Du dumme Sau, was machst du denn da»

Обобщать «что угодно + запятая + W-слово» НЕЛЬЗЯ: замер дал 45
попаданий, и 42 из них — подчинённые клаузы («Es ist unklar, WARUM er
nicht kam», «Das ist das Maximum, WAS ich dir leihen kann»). Ровно
поэтому `scan_de_tail_question` W-слова и не берёт.

Отделяет вопрос от подчинённой клаузы НЕМЕЦКАЯ ВОПРОСИТЕЛЬНАЯ ЧАСТИЦА.
«denn», «bloß», «eigentlich» при W-слове стоят только в настоящем
вопросе — в подчинённой клаузе их там не бывает. Замер: 20 рядов с
таким сочетанием, 17 со знаком «?» и ровно 3 без, и все три были
вопросами без знака. **Ни одного ложного попадания.**

ПОЧЕМУ ТЕПЕРЬ ГЕЙТ. После правки этих двух рядов примета чиста по ВСЕМ
ТРЁМ ведрам по всей базе — ноль, ноль и ноль. Правило формальное и от
языка не зависит (знак препинания), законного остатка нет. Поэтому она
возвращает код 1 при любом попадании, как остальные девять гейтов: ноль,
доставшийся дорого, надо запирать, иначе он утечёт.

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


# Ведущее междометие прячет вопросительное слово от якоря `^`: «Na, wie
# geht's dir denn» — вопрос, а шаблон его не видел. Список ЗАКРЫТЫЙ и
# только из междометий: расширять его словами вроде «sag mal» нельзя, иначе
# снимется и начало настоящего утверждения.
LEAD_INTERJECTION = re.compile(
    r"^(?:na|ach|tja|nun|also|hey|hallo|moin|oh|ah|hm+|puh|mensch|mann)\b"
    r"\s*[,!]\s*",
    re.IGNORECASE,
)


def strip_interjection(s: str) -> str:
    """Снимает ведущее междометие с запятой, если оно есть."""
    return LEAD_INTERJECTION.sub("", s, count=1).strip()


# ВТОРАЯ ПРОВЕРКА, добавленная в блоке 7 третьего прохода, и она сильнее
# первой, потому что опирается на ГРАММАТИКУ, а не на список слов.
#
# Список междометий закрыл `Na` и `Tja`, но пропустил `Herrgott`,
# `Menschenskind` и `Du dumme Sau` — звательные обороты, которых в списке
# нет и быть не может: их бесконечно много.
#
# Признак другой. Немецкая ВОПРОСИТЕЛЬНАЯ ЧАСТИЦА («denn», «bloß»,
# «eigentlich») в клаузе с W-словом стоит только в НАСТОЯЩЕМ вопросе: в
# подчинённой клаузе («Es ist unklar, warum er nicht kam») её там не
# бывает. Поэтому «W-слово + частица» отделяет вопрос от подчинённой
# клаузы без разбора структуры предложения.
#
# Замер по базе: 20 рядов, 17 со знаком «?» и ровно 3 без — и все три
# были настоящими вопросами без знака. Ни одного ложного попадания.
QUESTION_PARTICLE = re.compile(
    r"\b(?:wer|wen|wem|wessen|was|wo|wohin|woher|wann|wie|warum|wieso|"
    r"weshalb|welche[rsnm]?)\b[^,.!?]{0,40}?\b(?:denn|bloß|eigentlich)\b",
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
    core = strip_interjection(s)
    # Отсечки считаются по ядру: «Na, was für ein Zufall» — тоже не вопрос
    if core.endswith("!"):
        return False
    if NOT_A_QUESTION.match(core):
        return False
    if GERMAN_QUESTION_START.match(core):
        return True
    # Вопросительная частица при W-слове — вопрос где угодно во фразе
    return bool(QUESTION_PARTICLE.search(s))


# Самопроверка до работы: шаблон, который врёт, опаснее отсутствия проверки
MUST_BE_QUESTION = [
    "Wann kommst du",
    "Was machen wir nun",
    "Wie geht's dir",
    "Darf ich hier rauchen",
    "Hast du genug Geld",
    "Welches ist dein Sternzeichen",
    # Междометие перед вопросительным словом — дыра, закрытая в третьем
    # проходе. Оба примера настоящие, из базы.
    "Na, wie geht's dir denn",
    "Tja, was soll ich sagen",
    "Ach, warum hast du das nicht gesagt",
    # Вопросительная частица при W-слове — вопрос при любом зачине
    "Herrgott, was ist denn hier passiert",
    "Menschenskind, was hast du denn getan",
    "Du dumme Sau, was machst du denn da",
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
    # Снятие междометия не должно превращать утверждение в вопрос
    "Also, wir gehen um drei Uhr",
    "Na, das ist eine schöne Überraschung",
    "Ach Gott, habe ich das vergessen",
    # Отсечки работают и после снятия междометия
    "Na, was für ein Zufall!",
    "Tja, was die Bezahlung anbelangt, haben wir keine Einigung",
    # Подчинённые клаузы с W-словом — НЕ вопросы, и частицы в них нет
    "Es ist unklar, warum er nicht zur Party gekommen ist",
    "Das ist das Maximum, was ich dir leihen kann",
    "Ich bin gespannt, wie das Konzert wird",
    "Wir rätseln noch immer, wo er hingegangen ist",
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--show", type=int, default=12, help="сколько примеров печатать")
    ap.add_argument("--pairs", action="store_true",
                    help="печатать немецкий и перевод рядом: так видно, "
                         "потерян ли только знак или вся вопросительная форма")
    ap.add_argument("--from", type=int, default=1, dest="start",
                    help="с какой пары начать (для разбора партиями)")
    ap.add_argument("--count", type=int, default=60,
                    help="сколько пар напечатать")
    ap.add_argument("--bucket", default="в немецком знак есть, в переводе нет",
                    choices=["в немецком знак есть, в переводе нет",
                             "в переводе знак есть, в немецком нет"],
                    help="какой из двух списков разбирать парами")
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
        items = found[args.bucket]
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
        # Разбор партиями — это чтение, а не проверка: кода 1 здесь не место
        return 0

    print(f"=== проверено слов: {len(rows)} ===\n")
    total = 0
    for name in sorted(found, key=lambda k: -len(found[k])):
        items = found[name]
        total += len(items)
        print(f"{name}: {len(items)}")
        for wid, de, lang, val in items[: args.show]:
            print(f"    {wid:>6} {de:<18} {lang}: {val!r}")
        if len(items) > args.show:
            print(f"    ... ещё {len(items) - args.show}")
        print()
    if not total:
        print("ЧИСТО")
        return 0
    print("ГЕЙТ: знак вопроса — правило формальное, законного остатка нет")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
