# -*- coding: utf-8 -*-
"""
Сплошной поиск битой кодировки: текст, который однажды прочитали как
latin-1 вместо utf-8, и в базу легли «кракозябры».

Нашлось глазами в блоке 18: польское `z bronią` стоит в базе как
`z broniÄ…`. Два байта utf-8 (C4 85 = ą) прочитаны как два символа
latin-1 (Ä = C4, … = 85). Проверка на диакритику такое не видит: буквы
формально законные, слово просто не то.

Признак, по которому ищем: латинская заглавная Ã/Ä/Å/Â непосредственно
перед символом, которого в нормальном слове за ней быть не может —
многоточием, кавычкой-ёлочкой, знаком градуса, типографской кавычкой.
Ровно так выглядит utf-8, прочитанный как latin-1.

    python -m app.scripts.scan_mojibake
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

COLUMNS = [
    "word_de", "example_de",
    "translation_en", "example_en",
    "translation_ru", "example_ru",
    "translation_uk", "example_uk",
    "translation_tr", "example_tr",
    "translation_pl", "example_pl",
    "translation_it", "example_it",
    "translation_es", "example_es",
    "translation_fr", "example_fr",
    "translation_cs", "example_cs",
]

# Вторым символом идёт то, что получается из «хвостового» байта utf-8,
# прочитанного как latin-1: он всегда из диапазона 0x80–0xBF.
MOJIBAKE = re.compile(r"[ÃÄÅÂÐÑ][-¿–—‘’‚“”„†‡…‰€ŒœŠšŸŽžƒˆ˜]")

# Заведомо верные строки и заведомо битые — проверка шаблона до работы.
GOOD = [
    "Uzbrojeni mężczyźni są niebezpieczni",   # польская диакритика на месте
    "Mädel",                                  # немецкий умлаут
    "Hâlâ umudum var",                        # турецкий циркумфлекс
    "Älter als ich",                          # Ä в начале слова, дальше буква
    "Я бачу тебе",                            # кириллица
    "Çocukluğum güzeldi",
    "L'été à Paris",
]
BAD = [
    "uzbrojony, z broniÄ…",      # ą
    "mÄ™Å¼czyzna",               # ę, ż
    "ÐŸÑ€Ð¸Ð²ÐµÑ‚",               # кириллица через latin-1
    "GrÃ¼ÃŸe",                   # ü, ß
    "Ã§ocuk",                    # ç
]


def selfcheck() -> None:
    print("=== самопроверка шаблона ===")
    bad_good = [s for s in GOOD if MOJIBAKE.search(s)]
    good_bad = [s for s in BAD if not MOJIBAKE.search(s)]
    if bad_good:
        print("  ПРОВАЛ: верные строки объявлены битыми:")
        for s in bad_good:
            print(f"    {s!r}")
    if good_bad:
        print("  ПРОВАЛ: битые строки не найдены:")
        for s in good_bad:
            print(f"    {s!r}")
    if bad_good or good_bad:
        sys.exit("шаблон негоден, работать нельзя")
    print("  шаблон отличает верное от битого")


async def main() -> int:
    selfcheck()
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    async with engine.connect() as conn:
        total = await conn.scalar(text("SELECT count(*) FROM words"))
        print(f"\n=== проверено слов: {total} ===\n")
        hits = 0
        for col in COLUMNS:
            rows = (await conn.execute(text(
                f"SELECT id, word_de, {col} FROM words "
                f"WHERE {col} IS NOT NULL ORDER BY id"
            ))).all()
            found = [(i, w, v) for i, w, v in rows if MOJIBAKE.search(v)]
            if not found:
                continue
            hits += len(found)
            print(f"{col}: {len(found)}")
            for i, w, v in found:
                print(f"  {i:>7} {w:<18} {v!r}")
            print()
        if not hits:
            print("битой кодировки нет")
        else:
            print(f"всего ячеек с битой кодировкой: {hits}")
    await engine.dispose()
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
