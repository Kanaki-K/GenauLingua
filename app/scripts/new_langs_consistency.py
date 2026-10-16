#!/usr/bin/env python3
"""
Сверка переводов it, es, fr, cs между блоками archive/new_langs/out.

Блоки переводятся параллельно и друг друга не видят, поэтому одно немецкое
слово (дубли по уровню: «ich» A1 и A2, «du» A1 и A2) может получить разный
перевод, а одинаковый немецкий пример — разные переводы примера. Каждый
такой случай выписывается: какой вариант верен, решает вычитка.

    python -m app.scripts.new_langs_consistency
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from app.scripts.new_langs_check import LANGS, load_jsonl  # noqa: E402

BASE = Path(__file__).resolve().parent.parent.parent / "archive" / "new_langs"


def main() -> None:
    src = {}
    for f in (BASE / "src").glob("block_*.jsonl"):
        for r in load_jsonl(f):
            src[r["id"]] = r
    rows = []
    for f in sorted((BASE / "out").glob("block_*.jsonl")):
        for r in load_jsonl(f):
            r["_block"] = f.stem[-4:]
            rows.append(r)

    by_word: dict[tuple, list] = defaultdict(list)
    by_example: dict[str, list] = defaultdict(list)
    for r in rows:
        s = src.get(r["id"], {})
        by_word[(r["de"], s.get("pos"))].append(r)
        if s.get("ex_de"):
            by_example[s["ex_de"]].append(r)

    n = 0
    for (de, pos), group in sorted(by_word.items()):
        if len(group) < 2:
            continue
        for lang in LANGS:
            firsts = {g[lang].split(",")[0].strip() for g in group}
            if len(firsts) > 1:
                n += 1
                print(f"СЛОВО {de} ({pos}) {lang}: " + " | ".join(
                    f"{g['_block']}/{g['id']}: {g[lang]}" for g in group))
    for ex, group in sorted(by_example.items()):
        if len(group) < 2 or len({g["de"] for g in group}) > 1:
            continue
        for lang in LANGS:
            if len({g["ex_" + lang] for g in group}) > 1:
                n += 1
                print(f"ПРИМЕР «{ex}» {lang}: " + " | ".join(
                    f"{g['_block']}/{g['id']}: {g['ex_' + lang]}" for g in group))
    print(f"рядов {len(rows)}, расхождений {n}")


if __name__ == "__main__":
    main()
