# -*- coding: utf-8 -*-
"""
Показывает ли пример само слово: отделить словоизменение от дефекта.

Проверка по подстроке не годится. «Рыба» → «Я люблю рыбу» — слово там есть,
просто в другом падеже, и такая проверка даёт 26% ложных срабатываний на всей
базе, в которых тонет настоящая проблема: «Подсобить» → «Иногда нужно помочь
удаче», где исходного слова нет вообще.

Отделяем по основе. Словоизменение меняет окончание, а начало слова остаётся:
рыба/рыбу, książka/książkę, Haus/Häuser. Поэтому ищем в примере слово,
у которого с заголовочным достаточно долгое общее начало, сравнивая без
диакритики — иначе Haus и Häuser разойдутся на второй букве.

Это не морфологический разбор, а отсев: он снимает словоизменение, чтобы
остаток можно было отдать на суждение модели или глазам, не утонув в шуме.

ЧЕГО ОТСЕВ НЕ ВИДИТ, и это надо знать, читая его числа. Чередование в корне
ему недоступно: «wollen» и «willst», «geben» и «gibst», «verschwinden» и
«verschwunden», «erliegen» и «erlegen» — всё это правильные формы одного
слова, а начало у них расходится. В немецком сильном спряжении таких форм
много, поэтому число дефектов по немецкому завышено.

Отсюда важное следствие: вердикт отсева не является основанием отвергать
чужую работу. Модель, которой велено вставить слово в пример, разбирается
в морфологии лучше поиска по началу слова. Несогласие отсева — повод
посмотреть, а не повод выбросить.

    python -m app.scripts.example_quality                  # сводка
    python -m app.scripts.example_quality --lang ru --show 30
    python -m app.scripts.example_quality --lang ru --out bad_ru.jsonl
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import pathlib
import re
import sys
import unicodedata

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
os.environ.setdefault("ENV_FILE", ".env.local")

from sqlalchemy import text

from app.database.session import AsyncSessionLocal
from app.services.language_service import LANGUAGES, SUPPORTED_LANGS

# Порядок разбора — тот же, что у озвучки: сначала немецкий
ORDER = ("de", "en", "uk", "ru", "tr", "pl")

_WORD_RE = re.compile(r"[^\W\d_]+", re.UNICODE)

# Сколько букв основы должно совпасть. Меньше — начнут склеиваться разные
# слова с общим началом (рука/ручей), больше — отсечётся словоизменение
# коротких слов. Для языков с богатым словоизменением порог ниже: там
# окончание съедает большую часть короткого слова.
MIN_STEM = {
    "de": 4, "en": 4,          # словоизменение скудное, начало почти не меняется
    "ru": 3, "uk": 3, "pl": 3, # падежи и роды меняют окончание сильно
    "tr": 3,                   # агглютинация: окончания наращиваются
}

# Короче этого слово проверяется целиком: у «ja», «to», «и» основы нет.
# В славянских и турецком порог ниже: там окончание меняется и у слова
# из четырёх букв — «рыба» в примере стоит как «рыбу».
SHORT_WORD = {"de": 4, "en": 4, "ru": 3, "uk": 3, "pl": 3, "tr": 3}

# Сколько букв заголовочного слова может остаться непокрытыми.
#
# Это оказалось правильной мерой вместо доли слова. Доля путала разные вещи:
# на половине «Fräulein» совпадало с «Frau» (четыре общих буквы из восьми, а
# это разные слова), а при восьмидесяти процентах ломалось спряжение —
# «kommen» не совпадало с «kommst».
#
# Непокрытый хвост различает их сразу: у спряжения это два символа («kommen»
# против «kommst»), у разных слов четыре («Fräulein» против «Frau»).
#
# Случай с Fräulein пойман проверкой озвучки распознаванием: клип
# «das Fräulein … Entschuldigung, Frau» был опознан как не содержащий слова,
# и оказался прав — пример действительно про другое.
MAX_UNMATCHED_TAIL = {
    "de": 3, "en": 3,          # меняется только окончание
    "ru": 5, "uk": 5, "pl": 5, # падежи и роды срезают больше
    "tr": 5,                   # агглютинация наращивает, но и основа плывёт
}
DEFAULT_MAX_TAIL = 4

# Служебные приставки и частицы, которые в примере могут отделяться от слова
LEADING = {
    "de": ("der", "die", "das", "den", "dem", "des",
           "ein", "eine", "einen", "einem", "einer", "eines",
           "sich", "zu"),
    "en": ("to", "the", "a", "an"),
    "pl": ("się",),
    "ru": (), "uk": (), "tr": (),
}

# Немецкие отделяемые приставки: в предложении они отрываются и уходят в
# конец — «aufstehen» превращается в «ich stehe früh auf». Без этого целый
# класс глаголов попадал бы в дефекты, а в немецком их много.
SEPARABLE_PREFIXES = (
    "zusammen", "zurück", "gegenüber", "entgegen", "voraus", "vorbei",
    "herunter", "hinunter", "herüber", "hinüber", "heraus", "hinaus",
    "herein", "hinein", "hervor", "davon", "dabei", "daran",
    "wieder", "weiter", "zurecht", "empor",
    "nach", "über", "unter", "durch", "gegen",
    "auf", "aus", "ein", "mit", "vor", "weg", "hin", "her", "los", "zu",
    "ab", "an", "bei", "um",
    # Отделяемые части, которые приставками не выглядят, но ведут себя как они.
    # Их отсутствие в списке зря браковало годные примеры: «fernsehen» →
    # «Abends sehe ich gern fern», «wohlfühlen» → «Hier fühle ich mich wohl».
    "fern", "rein", "raus", "runter", "rauf", "rüber", "wohl", "heim",
    "fest", "frei", "statt", "teil", "wahr", "acht", "preis", "stand",
    "gleich", "voll", "leer", "fehl", "kund", "wett", "bereit",
)


# Буквы с перечёркиванием — не диакритика, а отдельные знаки: NFD их не
# разбирает, и польское «żółty» оставалось бы «zołty». Для польского это
# существенно, ł там частая буква.
STROKE_LETTERS = {
    "ł": "l", "Ł": "l", "đ": "d", "Đ": "d",
    "ø": "o", "Ø": "o", "ħ": "h", "ŧ": "t",
    "ı": "i", "İ": "i",   # турецкие i без точки и с точкой
}


def fold(s: str) -> str:
    """
    Снять регистр и диакритику для сравнения основ.

    Без этого Haus и Häuser расходятся на второй букве, а książka и książkę
    сравнивались бы точнее, чем нужно. Немецкий ß раскрывается в ss:
    Fuß/Füsse иначе не сойдутся.
    """
    s = s.lower().replace("ß", "ss")
    for source, target in STROKE_LETTERS.items():
        if source in s:
            s = s.replace(source, target)
    decomposed = unicodedata.normalize("NFD", s)
    return "".join(c for c in decomposed if not unicodedata.combining(c))


# Приставки в свёрнутом виде: сравнение идёт со свёрнутым словом
_FOLDED_PREFIXES = tuple(sorted(
    {fold(p) for p in SEPARABLE_PREFIXES}, key=len, reverse=True
))


def common_prefix(a: str, b: str) -> int:
    n = 0
    for x, y in zip(a, b):
        if x != y:
            break
        n += 1
    return n


def strip_leading(tokens: list[str], lang: str) -> list[str]:
    """Убрать артикль или частицу инфинитива из заголовочного слова."""
    particles = LEADING.get(lang, ())
    while len(tokens) > 1 and tokens[0] in particles:
        tokens = tokens[1:]
    return tokens


def word_in_example(word: str, example: str, lang: str) -> tuple[bool, str]:
    """
    Есть ли слово в примере хотя бы в другой форме.

    Возвращает (найдено, чем именно совпало) — второе нужно, чтобы решения
    можно было проверить глазами, а не верить им на слово.
    """
    head_tokens = strip_leading(_WORD_RE.findall(fold(word)), lang)
    if not head_tokens:
        return False, ""

    example_tokens = _WORD_RE.findall(fold(example))
    example_joined = " ".join(example_tokens)
    if not example_tokens:
        return False, ""

    # Составное заголовочное слово («Консервная банка», «ins Bett gehen»):
    # годится, если нашлась любая его содержательная часть. Раньше бралась
    # только самая длинная, и «Консервная банка» → «Банка пустая» считалось
    # дефектом, хотя пример слово показывает.
    candidates = list(head_tokens)
    # Отделяемая приставка ушла в конец предложения: ищем и корень без неё.
    # Приставки сворачиваются так же, как слово: иначе «zurück» никогда не
    # совпало бы с «zuruckgeben», и целый класс глаголов оставался неучтённым.
    if lang == "de":
        for token in head_tokens:
            for prefix in _FOLDED_PREFIXES:
                if token.startswith(prefix) and len(token) - len(prefix) >= 3:
                    candidates.append(token[len(prefix):])
                    break

    for head in sorted(candidates, key=len, reverse=True):
        found, matched = _single_token_in(head, example_tokens, example_joined, lang)
        if found:
            return True, matched
    return False, ""


def _single_token_in(head: str, example_tokens: list[str],
                     example_joined: str, lang: str) -> tuple[bool, str]:
    short = SHORT_WORD.get(lang, 4)

    if len(head) <= short:
        # У короткого слова основы нет, ищем целиком
        if head in example_tokens:
            return True, head
        # Удвоение согласной перед окончанием: run → running, stop → stopping
        doubled = head + head[-1] if head else ""
        for token in example_tokens:
            if token.startswith(head) and len(token) - len(head) <= 3:
                return True, token
            if doubled and token.startswith(doubled):
                return True, token
        return False, ""

    need = min(MIN_STEM.get(lang, 4), len(head))
    max_tail = MAX_UNMATCHED_TAIL.get(lang, DEFAULT_MAX_TAIL)

    # Для поиска подстрокой нужна почти вся основа, а не минимум: назначение
    # у этой проверки узкое — найти корень внутри составного слова («gehe» в
    # «weggehen»). С коротким куском она ловила «вел» в «Величие» и объявляла
    # годным пример про другое слово.
    substring_stem = head[:max(need, len(head) - max_tail)]

    best, best_token = 0, ""
    for token in example_tokens:
        score = common_prefix(head, token)
        if score > best:
            best, best_token = score, token
        # Годится, если совпало достаточно и от слова осталось немного:
        # два непокрытых символа — это окончание, четыре — другое слово
        if score >= need and len(head) - score <= max_tail:
            return True, token

    # Основа может быть спрятана за приставкой или внутри составного слова:
    # «gehen» в «weggehen», «Fahrkarte» в «Fahrkartenautomat»
    if substring_stem in example_joined:
        return True, next(
            (t for t in example_tokens if substring_stem in t), substring_stem
        )

    return False, best_token


async def audit(lang: str) -> dict:
    cfg = LANGUAGES[lang]
    async with AsyncSessionLocal() as s:
        rows = (await s.execute(text(f"""
            SELECT w.id,
                   w.{cfg.word_attr}    AS word,
                   w.{cfg.example_attr} AS example,
                   w.article,
                   w.level::text        AS level
            FROM words w
            JOIN word_lang_groups g
              ON g.word_id = w.id AND g.lang = :lang AND g.is_canonical
        """), {"lang": lang})).mappings().all()

    missing: list[dict] = []
    no_example = 0
    naive_misses = 0

    for r in rows:
        word = (r["word"] or "").strip()
        example = (r["example"] or "").strip()
        if not word:
            continue
        if not example:
            no_example += 1
            continue

        # Для сравнения: сколько дала бы проверка по подстроке
        if fold(word) not in fold(example):
            naive_misses += 1

        found, matched = word_in_example(word, example, lang)
        if not found:
            missing.append({
                "id": r["id"], "level": r["level"],
                "word": word, "example": example, "lang": lang,
            })

    return {
        "total": len(rows),
        "no_example": no_example,
        "naive_misses": naive_misses,
        "missing": missing,
    }


async def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lang", choices=list(SUPPORTED_LANGS))
    ap.add_argument("--show", type=int, default=0, help="сколько случаев напечатать")
    ap.add_argument("--out", help="сохранить найденное в JSONL для прогона правок")
    args = ap.parse_args()

    langs = [args.lang] if args.lang else [c for c in ORDER if c in SUPPORTED_LANGS]
    everything: list[dict] = []
    grand_total = grand_naive = grand_real = 0

    for lang in langs:
        res = await audit(lang)
        total = res["total"]
        if not total:
            print(f"\n=== {lang}: слов нет (колонка не заполнена) ===")
            continue

        real = len(res["missing"])
        grand_total += total
        grand_naive += res["naive_misses"]
        grand_real += real
        everything.extend(res["missing"])

        print(f"\n=== {lang} — {total} канонических слов ===")
        print(f"   по подстроке «не найдено»:  {res['naive_misses']:>6}  "
              f"({res['naive_misses'] / total * 100:.2f}%)")
        print(f"   из них словоизменение:      "
              f"{res['naive_misses'] - real:>6}  — пример годен")
        print(f"   слова в примере правда нет: {real:>6}  "
              f"({real / total * 100:.2f}%)")
        if res["no_example"]:
            print(f"   примера нет вовсе:          {res['no_example']:>6}")

        for item in res["missing"][:args.show]:
            print(f"        {item['level']}  {item['word']!r}  →  {item['example']!r}")

    if len(langs) > 1:
        print("\n=== ИТОГО ===")
        print(f"   слов проверено:             {grand_total}")
        print(f"   по подстроке «не найдено»:  {grand_naive} "
              f"({grand_naive / grand_total * 100:.2f}%)")
        print(f"   ложная тревога от форм:     {grand_naive - grand_real} "
              f"({(grand_naive - grand_real) / grand_total * 100:.2f}%)")
        print(f"   настоящих дефектов:         {grand_real} "
              f"({grand_real / grand_total * 100:.2f}%)")

    if args.out and everything:
        path = pathlib.Path(args.out)
        with path.open("w", encoding="utf-8") as fh:
            for item in everything:
                fh.write(json.dumps(item, ensure_ascii=False) + "\n")
        print(f"\n   список для правки: {path} ({len(everything)} записей)")

    return 0


if __name__ == "__main__":
    # Под защитой, чтобы word_in_example можно было импортировать в тесты,
    # не запуская разбор всей базы
    sys.exit(asyncio.run(main()))
