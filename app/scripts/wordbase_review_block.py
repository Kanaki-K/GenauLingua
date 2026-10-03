# -*- coding: utf-8 -*-
"""
Сплошная вычитка базы блоками: ряды подряд, в неизменном порядке.

Чем отличается от wordbase_sample_review. Тот берёт случайную выборку и
отвечает на вопрос «каково качество базы в целом». Этот отвечает на другой:
«какие ряды ещё не читал никто». Для полной вычитки нужен именно он —
случайные выборки неизбежно читают одно дважды и не доходят до остального.

Порядок рядов задан жёстко и не меняется между запусками:

    сначала по рангу частотности (чем чаще слово, тем раньше),
    слова без ранга — в конец, между собой по id.

Поэтому «блок 7» это всегда одни и те же ряды, а запись «дочитано до 1200»
имеет однозначный смысл. Самые частые слова идут первыми намеренно: их
видят все ученики, и дефект в них стоит дороже дефекта в слове с рангом
24 000.

    python -m app.scripts.wordbase_review_block --from 1 --count 100
    python -m app.scripts.wordbase_review_block --from 101 --count 100 --out b2.txt
    python -m app.scripts.wordbase_review_block --where          # сколько всего
"""
from __future__ import annotations

import argparse
import asyncio
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
os.environ.setdefault("ENV_FILE", ".env.local")

from app.scripts.wordbase_sample_review import (  # noqa: E402
    filled_languages,
    formal_notes,
    load_pool,
    render,
)
from app.services.language_service import SUPPORTED_LANGS  # noqa: E402


def ordered(pool: list[dict]) -> list[dict]:
    """
    Неизменный порядок: частые слова первыми, безранговые в конец.

    Ключ сортировки не зависит ни от зерна, ни от времени запуска, ни от
    содержимого строк — только от ранга и id. Если добавить в базу новое
    слово, оно встанет на своё место по рангу, и нумерация после него
    сдвинется; поэтому в журнале вычитки отмечается не только номер ряда,
    но и id последнего прочитанного.
    """
    return sorted(
        pool,
        key=lambda r: (r.get("frequency_rank") is None,
                       r.get("frequency_rank") or 0,
                       r["id"]),
    )


async def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--from", type=int, default=1, dest="start",
                    help="с какого ряда по общему порядку (считая с 1)")
    ap.add_argument("--count", type=int, default=100, help="сколько рядов")
    ap.add_argument("--lang", choices=list(SUPPORTED_LANGS),
                    help="читать один язык, а не все")
    ap.add_argument("--where", action="store_true",
                    help="только сказать, сколько всего рядов, и выйти")
    args = ap.parse_args()

    requested = [args.lang] if args.lang else list(SUPPORTED_LANGS)
    langs = await filled_languages(requested)
    pool = ordered(await load_pool(args.lang))
    if not pool or not langs:
        print("в базе нет подходящих слов")
        return 1

    if args.where:
        ranked = sum(1 for r in pool if r.get("frequency_rank") is not None)
        print(f"всего рядов: {len(pool)}")
        print(f"  с рангом частотности: {ranked}")
        print(f"  без ранга (идут в конце): {len(pool) - ranked}")
        print(f"языки: {' '.join(langs)}")
        return 0

    if args.start < 1 or args.start > len(pool):
        print(f"ряд {args.start} вне базы: всего рядов {len(pool)}")
        return 1

    block = pool[args.start - 1: args.start - 1 + args.count]
    last = args.start + len(block) - 1
    flagged = sum(1 for r in block if formal_notes(r, langs))

    print("=" * 72)
    print(f"БЛОК: ряды {args.start}–{last} из {len(pool)}")
    print(f"  id первого: {block[0]['id']}, id последнего: {block[-1]['id']}")
    print(f"  порядок: по рангу частотности, безранговые в конец")
    print(f"  с формальными замечаниями: {flagged} из {len(block)}")
    print("  формальные замечания — подсказки, а не оценка качества")
    print("=" * 72)
    print()

    for offset, row in enumerate(block):
        print(render(row, langs, args.start + offset))
        print()

    print("=" * 72)
    print(f"конец блока. Следующий: --from {last + 1}")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
