#!/usr/bin/env python3
"""
Обратный перевод it/es/fr/cs «вслепую» — проверка смысла без носителя.

Агент получает только слово и пример на одном языке (без немецкого, без
других языков) и переводит их на русский. Потом его перевод сравнивают с
немецким оригиналом: расхождение смысла видно сразу, а вычитчик, который
видит немецкий, его пропускает — он «понимает, что имелось в виду».

    python -m app.scripts.new_langs_backtrans blind --levels A1 A2 --size 200
    python -m app.scripts.new_langs_backtrans pairs     # после агентов: файл для сверки
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from app.scripts.new_langs_check import LANGS, load_jsonl  # noqa: E402

BASE = Path(__file__).resolve().parent.parent.parent / "archive" / "new_langs"
OUT, SRC, BT = BASE / "out", BASE / "src", BASE / "backtrans"


def _rows(levels: set[str]) -> tuple[dict, list]:
    src = {}
    for f in SRC.glob("block_*.jsonl"):
        for r in load_jsonl(f):
            src[r["id"]] = r
    out = []
    for f in sorted(OUT.glob("block_*.jsonl")):
        out.extend(r for r in load_jsonl(f) if src[r["id"]]["lvl"] in levels)
    return src, out


def cmd_blind(levels: list[str], size: int) -> None:
    _, rows = _rows(set(levels))
    BT.mkdir(exist_ok=True)
    n_files = 0
    for lang in LANGS:
        for k in range(0, len(rows), size):
            chunk = rows[k:k + size]
            name = BT / f"blind_{lang}_{k // size:03d}.txt"
            with name.open("w", encoding="utf-8", newline="\n") as fh:
                for r in chunk:
                    fh.write(f"#{r['id']}\t{r[lang]}\t{r['ex_' + lang]}\n")
            n_files += 1
    print(f"рядов {len(rows)} × {len(LANGS)} языка → файлов {n_files} по {size} в {BT}")


def cmd_pairs() -> None:
    """Свести обратный перевод с оригиналом: файл для агента-судьи."""
    src = {}
    for f in SRC.glob("block_*.jsonl"):
        for r in load_jsonl(f):
            src[r["id"]] = r
    cur = {}
    for f in OUT.glob("block_*.jsonl"):
        for r in load_jsonl(f):
            cur[r["id"]] = r
    n = 0
    for f in sorted(BT.glob("back_*.jsonl")):
        lang, part = f.stem.split("_")[1:3]
        with (BT / f"pairs_{lang}_{part}.txt").open("w", encoding="utf-8", newline="\n") as fh:
            for b in load_jsonl(f):
                s, r = src[b["id"]], cur[b["id"]]
                fh.write(f"#{b['id']} {s['de']} «{s['ex_de']}»  ru(эталон): {s['ru']} «{s['ex_ru']}»\n"
                         f"   {lang}: {r[lang]} ~ {r['ex_' + lang]}\n"
                         f"   вслепую → {b.get('ru_word')} «{b.get('ru_example')}»\n")
                n += 1
    print(f"пар сведено: {n}")


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("blind")
    b.add_argument("--levels", nargs="+", default=["A1", "A2"])
    b.add_argument("--size", type=int, default=200)
    sub.add_parser("pairs")
    args = ap.parse_args()
    if args.cmd == "blind":
        cmd_blind(args.levels, args.size)
    else:
        cmd_pairs()


if __name__ == "__main__":
    main()
