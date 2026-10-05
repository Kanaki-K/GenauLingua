# -*- coding: utf-8 -*-
"""
Сплошной поиск: слова ряда нет в его немецком примере.

Карточка устроена так: показывается слово, под ним пример, и озвучка
читает их вместе. Если слова в примере нет, пример не учит ничему —
ученик видит заголовок и фразу, которые между собой не связаны.

Нашлось при вычитке блока 22. Ряд `Umwelt` (id 1996), пример:
«Umweltschutz ist wichtig». Слово «Umwelt» там есть только внутри
составного «Umweltschutz» — то есть отдельно его не видно, а рядом в
базе стоит отдельный ряд `Umweltschutz` (id 2916) с тем же примером.

ПОЧЕМУ ТОЛЬКО СУЩЕСТВИТЕЛЬНЫЕ. У немецкого глагола основа меняется:
`nehmen` → «nahm», «genommen»; `gehen` → «ging». Шаблон по основе
объявил бы их дефектом, а они верны. У отделяемых приставок хуже:
`anfangen` → «fängt … an», и слова целиком в примере нет никогда.
Существительные почти всегда узнаваемы: меняется окончание и умлаут
(«Haus» → «Häuser»), а основа цела. Поэтому глаголы, прилагательные и
наречия шаблон не смотрит — для них нужен другой приём.

Умлауты нормализуются (ä→a, ö→o, ü→u, ß→ss), сравнение по основе без
последних двух букв, и совпадение считается только с начала слова —
иначе «Umweltschutz» сошло бы за «Umwelt».

    python -m app.scripts.scan_word_in_example
"""
from __future__ import annotations

import asyncio
import os
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
os.environ.setdefault("ENV_FILE", ".env.local")

from sqlalchemy import text  # noqa: E402
from sqlalchemy.ext.asyncio import create_async_engine  # noqa: E402

from app.config import settings  # noqa: E402

WORD = re.compile(r"[^\W\d_]+(?:-[^\W\d_]+)*", re.UNICODE)  # буквы и дефис: «E-Mail», «Café»


def norm(s: str) -> str:
    s = s.lower()
    for a, b in (("ä", "a"), ("ö", "o"), ("ü", "u"), ("ß", "ss")):
        s = s.replace(a, b)
    return s


def heads(word: str) -> list[str]:
    """Все части парного заголовка: «Hausmann/Hausfrau» → обе.

    Пример может стоять в любой из них: у `Krankenpfleger/Krankenschwester`
    пример про сестру, и по первой части он не найдётся. Первая версия
    шаблона смотрела только первую часть и объявила такие ряды дефектом.
    """
    parts = [p for p in re.split(r"/", norm(word).strip()) if p]
    return [re.split(r"\s", p)[0] for p in parts] or [norm(word)]


def head(word: str) -> str:
    """Первая часть заголовка: без «/in» и без второго слова.

    В базе заголовки бывают составными: «Bürger/in», «Experte/Expertin»,
    «Deutsche Demokratische Republik», «Übernachtung mit Frühstück».
    Сравнивать надо по первой части, иначе слеш и пробел попадут в основу
    и шаблон объявит дефектом всё подряд — так и вышло в первой версии,
    пятьдесят ложных попаданий.
    """
    return re.split(r"[/\s]", norm(word).strip())[0]


# Неправильное множественное: основа меняется, и шаблон по ней не сработает.
# Список короткий и проверенный — это надёжнее, чем ослаблять шаблон.
IRREGULAR = {
    "mann": ("leute", "manner", "leuten"),
    "virus": ("viren",),
    "serum": ("sera", "seren"),
    "museum": ("museen",),
    "datum": ("daten",),
    "forum": ("foren",),
    "zentrum": ("zentren",),
    "konto": ("konten",),
}


def irregular_match(part: str, tokens: list[str]) -> bool:
    for ending, plurals in IRREGULAR.items():
        if not part.endswith(ending):
            continue
        base = part[: -len(ending)]
        for pl in plurals:
            if any(tok.startswith(base + pl) for tok in tokens):
                return True
    return False


def stem_of(part: str) -> str:
    """Основа: без двух последних букв, но не короче четырёх."""
    return part[: max(4, len(part) - 2)]


def present(word: str, example: str) -> bool:
    """Есть ли в примере слово, начинающееся с основы заголовка.

    Длина ограничена: окончание разрешено («Haus» → «Häuser», плюс две
    буквы), а приклеенное слово нет («Umwelt» → «Umweltschutz», плюс
    шесть). Иначе составное слово сошло бы за заголовок, а это и есть
    дефект, который ищется.
    """
    # Слово через дефис даёт и целый токен, и части: «Vampir-Kostüm»
    # показывает «Kostüm» ученику, а «E-Mail» сам заголовок дефисный.
    tokens: list[str] = []
    for tok in WORD.findall(example):
        n = norm(tok)
        tokens.append(n)
        if "-" in n:
            tokens.extend(part for part in n.split("-") if part)
    for part in heads(word):
        st = stem_of(part)
        limit = len(part) + 3
        for t in tokens:
            if t.startswith(st) and len(t) <= limit:
                return True
        if irregular_match(part, tokens):
            return True
    return False


# Заведомо верные пары: слово в примере есть, пусть и в другой форме.
GOOD = [
    ("Haus", "Das Haus ist groß"),
    ("Haus", "Die Häuser sind alt"),
    ("Buch", "Ich lese die Bücher"),
    ("Mann", "Die Männer arbeiten"),
    ("Straße", "Die Strassen sind nass"),
    ("Kindheit", "Meine Kindheit war schön"),
    ("Munition", "Die Polizei fand Munition"),
    ("Bürger/in", "Ich bin deutscher Bürger"),
    ("Experte/Expertin", "Sie ist Expertin auf diesem Gebiet"),
    ("Deutsche Demokratische Republik",
     "Meine Oma wuchs in der Deutschen Demokratischen Republik auf"),
    ("Übernachtung mit Frühstück", "Ich buche eine Übernachtung mit Frühstück"),
    ("Café", "Wir sitzen in einem Café"),
    ("E-Mail", "Ich schreibe eine E-Mail"),
    ("Kostüm", "Für Halloween hab ich mir ein Vampir-Kostüm gekauft"),
    ("Hausmann/Hausfrau", "Sie ist Hausfrau"),
    ("Krankenpfleger/Krankenschwester", "Die Krankenschwester hilft den Patienten"),
    ("Geschäftsmann", "Die Geschäftsleute trafen sich im Hotel"),
    ("Virus", "Der Computer wurde von Viren infiziert"),
]
# Заведомо битые: слова ряда в примере нет.
BAD = [
    ("Umwelt", "Umweltschutz ist wichtig"),
    ("Daumen", "Mein Finger tut weh"),
    ("Kasse", "Sie zahlt mit Karte"),
]


def selfcheck() -> None:
    print("=== самопроверка шаблона ===")
    bad_good = [(w, e) for w, e in GOOD if not present(w, e)]
    good_bad = [(w, e) for w, e in BAD if present(w, e)]
    if bad_good:
        print("  ПРОВАЛ: верные пары объявлены битыми:")
        for w, e in bad_good:
            print(f"    {w!r} / {e!r}")
    if good_bad:
        print("  ПРОВАЛ: битые пары не найдены:")
        for w, e in good_bad:
            print(f"    {w!r} / {e!r}")
    if bad_good or good_bad:
        sys.exit("шаблон негоден, работать нельзя")
    print("  шаблон отличает верное от битого")


async def main() -> int:
    selfcheck()
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    async with engine.connect() as conn:
        rows = (await conn.execute(text(
            "SELECT id, word_de, example_de, level::text FROM words "
            "WHERE pos::text = 'NOUN' AND example_de IS NOT NULL "
            "ORDER BY frequency_rank NULLS LAST, id"
        ))).all()
        print(f"\n=== существительных с примером: {len(rows)} ===\n")
        found = [(i, w, e, lv) for i, w, e, lv in rows if not present(w, e)]
        for i, w, e, lv in found:
            print(f"  {i:>7} [{lv}] {w:<22} {e!r}")
        print(f"\nвсего: {len(found)}")
    await engine.dispose()
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
