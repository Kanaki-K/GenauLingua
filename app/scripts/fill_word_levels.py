#!/usr/bin/env python3
"""
Заполнить word_levels: уровень слова в каждом изучаемом языке, кроме немецкого.

ПРАВИЛО (сверка и выбор — 15.10.2026, см. модель `WordLevel`):
  * английский — официальный Oxford 3000/5000 by CEFR
    (`app/data/oxford_cefr.json`, слово → уровень) по главному значению;
  * слова английского вне списка, польский, турецкий, русский, украинский —
    среднее (с округлением вниз) двух уровней:
      - уровень ПОНЯТИЯ — `Word.level` (Goethe): «мама», «хлеб» просты везде;
      - уровень ФОРМЫ — место слова по частоте (wordfreq) среди слов этого
        языка, разрезанное в тех же долях, что уровни понятий.
    Место, а не абсолютная частота: у славянских языков частота дробится
    по падежам, и с общими порогами русский A1 вышел бы в 150 слов, а
    «телевизор» и «торт» — на B1 (первый прототип 15.10).
    Итог — не дальше одной ступени от уровня понятия.

Только канонические строки языка — остальные в викторину не идут.
Запускать после rebuild_word_groups, relevel_words_2026_10 и правок
переводов. Повторный запуск переписывает таблицу.

    python -m app.scripts.fill_word_levels
"""
from __future__ import annotations

import asyncio
import collections
import json
import os
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
os.environ.setdefault("ENV_FILE", ".env.local")

from sqlalchemy import delete, select  # noqa: E402
from wordfreq import zipf_frequency  # noqa: E402

from app.database.enums import CEFRLevel  # noqa: E402
from app.database.models import Word, WordLangGroup, WordLevel  # noqa: E402
from app.database.session import AsyncSessionLocal, engine  # noqa: E402
from app.services.language_service import main_meaning  # noqa: E402

LANGS = ("en", "pl", "tr", "ru", "uk")
ORDER = ["A1", "A2", "B1", "B2", "C1", "C2"]
OXFORD = json.loads(
    (pathlib.Path(__file__).resolve().parents[1] / "data" / "oxford_cefr.json").read_text(encoding="utf-8")
)

_LEADING = re.compile(r"^(to|the|a|an|der|die|das|sich)\s+", re.IGNORECASE)
_BRACKETS = re.compile(r"\([^)]*\)")


def headword(text: str) -> str:
    """Главное значение без скобок, хвоста перечня и служебного «to/the»."""
    text = _BRACKETS.sub("", text or "").strip().split(",")[0].strip()
    return _LEADING.sub("", text).strip()


def levels_for(words: list[Word], lang: str) -> tuple[dict[int, str], collections.Counter]:
    heads = {w.id: headword(main_meaning(w, lang)) for w in words}
    zipf = {w.id: zipf_frequency(heads[w.id], lang) if heads[w.id] else 0.0 for w in words}
    ranked = sorted(words, key=lambda w: (-zipf[w.id], w.id))
    share = collections.Counter(w.level.value for w in words)
    cuts, acc = [], 0
    for level in ORDER:
        acc += share[level]
        cuts.append(acc)
    form = {w.id: next(i for i, cut in enumerate(cuts) if pos < cut) for pos, w in enumerate(ranked)}

    out: dict[int, str] = {}
    source: collections.Counter = collections.Counter()
    for w in words:
        oxford = OXFORD.get(heads[w.id].lower()) if lang == "en" else None
        if oxford:
            out[w.id] = oxford
            source["oxford"] += 1
        else:
            concept = ORDER.index(w.level.value)
            blended = (concept + form[w.id]) // 2
            # Не дальше одной ступени от понятия: частота по новостям тянула
            # на A1 «правительство», «развитие», «война» (второй замер 15.10)
            out[w.id] = ORDER[max(concept - 1, min(concept + 1, blended))]
            source["понятие+частота"] += 1
    return out, source


async def main() -> int:
    async with AsyncSessionLocal() as session:
        words = {w.id: w for w in (await session.execute(select(Word))).scalars()}
        await session.execute(delete(WordLevel))
        for lang in LANGS:
            canonical = (await session.execute(
                select(WordLangGroup.word_id).where(
                    WordLangGroup.lang == lang, WordLangGroup.is_canonical.is_(True))
            )).scalars().all()
            mine = [words[i] for i in canonical if i in words]
            levels, source = levels_for(mine, lang)
            session.add_all(WordLevel(word_id=i, lang=lang, level=CEFRLevel(lv))
                            for i, lv in levels.items())
            dist = collections.Counter(levels.values())
            print(f"{lang}: {len(levels)} слов, {dict(source)}, "
                  + " ".join(f"{lv} {dist[lv]}" for lv in ORDER))
        await session.commit()
    await engine.dispose()
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
