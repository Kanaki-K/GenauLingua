# -*- coding: utf-8 -*-
"""
Предполётная проверка базы перед озвучкой: где синтез ошибётся.

Часть ошибок озвучки нельзя исправить количеством вычислений — они заложены
в тексте. Слово без контекста читается однозначно не всегда, сокращение с
точкой движок разворачивает по своему усмотрению, а текст не на том языке
озвучится как набор звуков. Этот скрипт находит такие места заранее, чтобы
их обработать отдельно, а не обнаружить в боте.

    python -m app.scripts.tts_preflight            # сводка по всем языкам
    python -m app.scripts.tts_preflight --lang de --show 20
"""
from __future__ import annotations

import argparse
import asyncio
import os
import pathlib
import re
import sys
import unicodedata

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
os.environ.setdefault("ENV_FILE", ".env.local")

from sqlalchemy import text

from app.database.session import AsyncSessionLocal
from app.services.language_service import LANGUAGES, LEARNABLE_LANGS

# Английские гетеронимы: одно написание, разное чтение по смыслу. Без
# контекста движок выбирает одно из чтений, и в половине случаев не то.
# Это главный источник ошибок, которого не лечит ни один объём вычислений.
EN_HETERONYMS = {
    "read", "lead", "live", "bow", "tear", "close", "record", "present",
    "object", "desert", "minute", "wind", "wound", "row", "sow", "bass",
    "content", "contract", "refuse", "produce", "progress", "project",
    "rebel", "subject", "conduct", "console", "contest", "convert",
    "escort", "excuse", "export", "import", "insult", "permit", "perfect",
    "polish", "separate", "use", "abuse", "house", "estimate", "moderate",
    "number", "does", "dove", "entrance", "invalid", "lima", "mobile",
    "resume", "second", "sewer", "slough", "supply", "tier",
}

# Немецкие слова, чтение которых зависит от смысла: смена ударения меняет
# слово (úmfahren объехать / umfáhren сбить), либо это вообще другое слово.
DE_HETERONYMS = {
    "umfahren", "umschreiben", "umstellen", "übersetzen", "durchschauen",
    "modern", "Montage", "Tenor", "August", "Weckglas", "Hochzeit",
    "umgehen", "durchsetzen", "übergehen", "ausführen",
}

HETERONYMS = {"en": EN_HETERONYMS, "de": DE_HETERONYMS}

# Сокращение с точкой: движок либо развернёт, либо прочтёт по буквам
ABBREV = re.compile(r"\b(?:[A-Za-zÄÖÜäöüß]{1,4}\.){1,}")
HTML_LEFTOVER = re.compile(r"<[^>]+>|&[a-z]+;|&#\d+;")
DIGITS = re.compile(r"\d")

# Ожидаемые письменности: текст не на своей письменности озвучится мусором
SCRIPTS = {
    "de": "LATIN", "en": "LATIN", "tr": "LATIN",
    "ru": "CYRILLIC", "uk": "CYRILLIC",
}

MAX_EXAMPLE_CHARS = 120   # длиннее — клип затягивается, на разборе утомляет

# Порядок работы по языкам. Сначала доводится до качества немецкий: он
# основной по спросу, и на нём отрабатывается схема, которая потом
# переносится на остальные без переизобретения.
ORDER = ("de", "en", "uk", "ru", "tr")


def wrong_script(value: str, expected: str) -> bool:
    """Есть ли в тексте буквы чужой письменности."""
    for ch in value:
        if not ch.isalpha():
            continue
        try:
            name = unicodedata.name(ch)
        except ValueError:
            return True
        if "LATIN" in name or "CYRILLIC" in name:
            if expected not in name:
                return True
    return False


async def audit(lang: str) -> dict:
    cfg = LANGUAGES[lang]
    async with AsyncSessionLocal() as s:
        rows = (await s.execute(text(f"""
            SELECT w.id,
                   w.{cfg.word_attr}    AS word,
                   w.{cfg.example_attr} AS example,
                   w.article,
                   w.pos::text          AS pos,
                   w.level::text        AS level
            FROM words w
            JOIN word_lang_groups g
              ON g.word_id = w.id AND g.lang = :lang AND g.is_canonical
        """), {"lang": lang})).mappings().all()

    # Ломает звук: движок прочтёт не то, что написано, или не то слово
    audio_risk: dict[str, list] = {
        "пусто": [],
        "чужая письменность": [],
        "сокращение с точкой": [],
        "цифры": [],
        "остатки разметки": [],
        "гетероним": [],
        "омограф по артиклю": [],
        "пример длинный": [],
    }

    # Не про звук: озвучится верно, но говорит о качестве словарной базы.
    # Считается отдельно, чтобы не завышать риск озвучки.
    content_signal: dict[str, list] = {
        "слова нет в примере": [],
    }

    seen_spelling: dict[str, list] = {}
    hetero = {h.lower() for h in HETERONYMS.get(lang, set())}
    script = SCRIPTS[lang]

    for r in rows:
        word = (r["word"] or "").strip()
        example = (r["example"] or "").strip()
        tag = f"{r['id']}  {word!r}"

        if not word or not example:
            audio_risk["пусто"].append(f"{tag}  пример={example!r}")
            continue

        for field, value in (("слово", word), ("пример", example)):
            if wrong_script(value, script):
                audio_risk["чужая письменность"].append(f"{tag}  {field}={value!r}")
            if HTML_LEFTOVER.search(value):
                audio_risk["остатки разметки"].append(f"{tag}  {field}={value!r}")
            if DIGITS.search(value):
                audio_risk["цифры"].append(f"{tag}  {field}={value!r}")
            if ABBREV.search(value):
                audio_risk["сокращение с точкой"].append(f"{tag}  {field}={value!r}")

        bare = word.split()[-1] if " " in word else word
        if bare.lower() in hetero:
            audio_risk["гетероним"].append(f"{tag}  пример={example!r}")

        # Одно написание с разными артиклями — разные слова (der See / die See)
        if cfg.uses_article:
            key = bare.lower()
            seen_spelling.setdefault(key, []).append(
                (r["id"], (r["article"] or "").strip(), r["pos"])
            )

        # Проверка по подстроке: в русском, украинском и турецком слово в
        # примере стоит в другой форме («рыба» → «люблю рыбу»), и проверка
        # срабатывает зря. Поэтому это сигнал о базе, а не риск озвучки:
        # звук в таких случаях верный.
        if bare.lower() not in example.lower():
            content_signal["слова нет в примере"].append(f"{tag}  пример={example!r}")

        if len(example) > MAX_EXAMPLE_CHARS:
            audio_risk["пример длинный"].append(f"{tag}  {len(example)} симв.")

    for spelling, entries in seen_spelling.items():
        articles = {a for _, a, _ in entries if a and a != "-"}
        if len(articles) > 1:
            audio_risk["омограф по артиклю"].append(
                f"{spelling!r}: " + ", ".join(f"{a} (id={i})" for i, a, _ in entries)
            )

    return {"total": len(rows), "audio": audio_risk, "content": content_signal}


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", choices=list(LEARNABLE_LANGS))
    ap.add_argument("--show", type=int, default=0,
                    help="сколько примеров печатать по каждой категории")
    args = ap.parse_args()

    langs = [args.lang] if args.lang else list(ORDER)
    grand_total = grand_audio = grand_content = 0

    def ids_in(groups: dict[str, list]) -> set[str]:
        """Слово может попасть в несколько категорий — считаем без двойного счёта."""
        found = set()
        for items in groups.values():
            for entry in items:
                head = entry.split()[0]
                if head.isdigit():
                    found.add(head)
        return found

    def report(title: str, groups: dict[str, list], total: int) -> None:
        print(f"   {title}")
        for name, items in groups.items():
            if not items:
                print(f"      {name:<24} —")
                continue
            print(f"      {name:<24} {len(items):>5}  ({len(items) / total * 100:.2f}%)")
            for entry in items[:args.show]:
                print(f"           {entry}")

    for position, lang in enumerate(langs, 1):
        res = await audit(lang)
        total = res["total"]
        audio_ids = ids_in(res["audio"])
        content_ids = ids_in(res["content"])
        grand_total += total
        grand_audio += len(audio_ids)
        grand_content += len(content_ids)

        order = f"приоритет {ORDER.index(lang) + 1}" if lang in ORDER else "вне очереди"
        print(f"\n=== {lang} — {total} канонических слов, {order} ===")
        report("ЛОМАЕТ ЗВУК:", res["audio"], total)
        report("НЕ ПРО ЗВУК (качество базы, озвучится верно):", res["content"], total)
        print(f"   → под риском озвучки {len(audio_ids)} "
              f"({len(audio_ids) / total * 100:.2f}%), "
              f"чисто {total - len(audio_ids)} "
              f"({(total - len(audio_ids)) / total * 100:.2f}%)")

    if len(langs) > 1:
        print("\n=== ИТОГО ===")
        print(f"   слов всего:            {grand_total}")
        print(f"   под риском озвучки:    {grand_audio} "
              f"({grand_audio / grand_total * 100:.2f}%)")
        print(f"   озвучится чисто:       {grand_total - grand_audio} "
              f"({(grand_total - grand_audio) / grand_total * 100:.2f}%)")
        print(f"   отдельно, к переводам: {grand_content} "
              f"({grand_content / grand_total * 100:.2f}%) — пример не содержит "
              f"слова в исходной форме")


asyncio.run(main())
