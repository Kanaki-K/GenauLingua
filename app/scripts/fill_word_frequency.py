#!/usr/bin/env python3
"""
Заполнить word_frequency: насколько ходовое слово на каждом языке.

Частота — zipf по wordfreq (сводная по Википедии, новостям, книгам,
субтитрам и соцсетям) для ГЛАВНОГО значения слова на этом языке — того, что
на карточке. Нужна подбору нового слова: внутри уровня сначала ходовые
(`quiz_service.get_new_words`).

Запускать после изменения словаря (новые слова, правка переводов).
Повторный запуск переписывает значения — ничего не копится.

    python -m app.scripts.fill_word_frequency
"""
from __future__ import annotations

import asyncio
import os
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
os.environ.setdefault("ENV_FILE", ".env.local")

from sqlalchemy import delete, select  # noqa: E402
from wordfreq import zipf_frequency  # noqa: E402

from app.database.models import Word, WordFrequency  # noqa: E402
from app.database.session import AsyncSessionLocal, engine  # noqa: E402
from app.services.language_service import SUPPORTED_LANGS, main_meaning  # noqa: E402

# Служебное в начале значения не делает слово редким: «to go», «der Hund»
_LEADING = re.compile(r"^(to|the|a|an|der|die|das|sich)\s+", re.IGNORECASE)
_BRACKETS = re.compile(r"\([^)]*\)")
# Артикль it/es/fr стоит в самом переводе («la casa», «l'uomo») — снимается
# только у этих языков, у прежних ключ слова не меняется
_ROMANCE = re.compile(r"^(il|lo|la|i|gli|le|el|los|las|les)\s+|^l'", re.IGNORECASE)


def _headword(text: str) -> str:
    text = _BRACKETS.sub("", text or "").strip()
    return _LEADING.sub("", text).strip()


def frequency(word: Word, lang: str) -> float:
    head = _headword(main_meaning(word, lang))
    if lang in ("it", "es", "fr"):
        head = _ROMANCE.sub("", head).strip()
    return zipf_frequency(head, lang) if head else 0.0


async def main() -> int:
    async with AsyncSessionLocal() as session:
        words = (await session.execute(select(Word))).scalars().all()
        await session.execute(delete(WordFrequency))
        rows = [
            WordFrequency(word_id=w.id, lang=lang, zipf=round(frequency(w, lang), 2))
            for w in words for lang in SUPPORTED_LANGS
        ]
        session.add_all(rows)
        await session.commit()
    await engine.dispose()
    print(f"частот записано: {len(rows)} ({len(words)} слов × {len(SUPPORTED_LANGS)} языков)")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
