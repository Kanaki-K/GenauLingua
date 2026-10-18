#!/usr/bin/env python3
"""
Уровни слов по официальным спискам Goethe-Institut (15.10.2026).

ЗАЧЕМ. Владелец: «Сложность — большая проблема сейчас». Новичкам A1
приходили Waffe, Seele, Mission, Bord, Strumpf — и они уходили после первых
слов, отвечая на всё верно. Уровни шли из частотного ранга по киносубтитрам
(Waffe — 578-е слово), и с официальными списками совпадали на 42% и в
старой прод-версии, и в 2.0: из 1 388 слов A1 старого прода 883 в списке A1
Goethe не значились.

ПРАВИЛО (карта — `app/data/word_levels_2026_10.json`, номер → [слово, уровень]):
  * слово есть в списке Goethe A1 / A2 / B1 (Start Deutsch 1, Goethe-
    Zertifikat A2 и B1) — уровень из списка, наименьший;
  * слова в списках нет, а стоял A1/A2 — A2, если оно очень ходовое (частота
    zipf ≥ 5.0 по wordfreq), иначе B1;
  * слова в списках нет, а стоял B1 и выше — уровень прежний.
Итог: A1 1 331 → 770 (в официальном A1 около 650), A2 867, B1 5 067.

Потолок по частоте: zipf ≥ 5.8 — не выше A1, ≥ 5.0 — не выше A2 (местоимения
в списке A1 стоят таблицами и не находятся: du ушло бы на B1). Омонимы и
дубли: (слово, уровень) уникально — на целевой уровень встаёт строка, уже
стоящая там, иначе первая; прочие сохраняют прежний уровень.

Карта проверяется по слову: номер с другим словом пропускается — значит,
база не та, на которой карта строилась.

    python -m app.scripts.relevel_words_2026_10            # показать
    python -m app.scripts.relevel_words_2026_10 --apply    # записать

Повторный запуск ничего не меняет.
"""
from __future__ import annotations

import argparse
import asyncio
import collections
import json
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
os.environ.setdefault("ENV_FILE", ".env.local")

from sqlalchemy import select  # noqa: E402

from app.database.enums import CEFRLevel  # noqa: E402
from app.database.models import Word  # noqa: E402
from app.database.session import AsyncSessionLocal, engine  # noqa: E402

MAP_FILE = pathlib.Path(__file__).resolve().parents[1] / "data" / "word_levels_2026_10.json"


async def main(apply: bool) -> int:
    mapping = json.loads(MAP_FILE.read_text(encoding="utf-8"))
    moves: collections.Counter = collections.Counter()
    skipped = 0
    async with AsyncSessionLocal() as session:
        words = {w.id: w for w in (await session.execute(select(Word))).scalars()}
        for key, (word_de, level) in mapping.items():
            word = words.get(int(key))
            if word is None or word.word_de != word_de:
                skipped += 1
                continue
            if word.level.value != level:
                moves[(word.level.value, level)] += 1
                word.level = CEFRLevel(level)
        if apply:
            await session.commit()
    await engine.dispose()

    for (a, b), n in sorted(moves.items(), key=lambda x: -x[1]):
        print(f"  {a} → {b}: {n}")
    print(f"\nслов {'перенесено' if apply else 'к переносу'}: {sum(moves.values())}, "
          f"пропущено (номер не совпал со словом): {skipped}")
    return 1 if skipped else 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    sys.exit(asyncio.run(main(ap.parse_args().apply)))
