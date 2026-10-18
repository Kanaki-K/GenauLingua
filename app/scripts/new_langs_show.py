#!/usr/bin/env python3
"""
Показать блок переводов it/es/fr/cs рядом с немецким оригиналом — для вычитки.

По ряду на слово: немецкое слово, часть речи, немецкий пример, английская
подсказка, затем четыре перевода с примерами и note.

    python -m app.scripts.new_langs_show archive/new_langs/out/block_0042.jsonl
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from app.scripts.new_langs_check import LANGS, load_jsonl  # noqa: E402


def main() -> None:
    for arg in sys.argv[1:]:
        path = Path(arg)
        src = {r["id"]: r for r in load_jsonl(path.parent.parent / "src" / path.name)}
        for r in load_jsonl(path):
            s = src.get(r["id"], {})
            art = f"{s['art']} " if s.get("art") else ""
            print(f"#{r['id']} {art}{r['de']} [{s.get('pos')}] «{s.get('ex_de')}»  en: {s.get('en')}")
            for lang in LANGS:
                print(f"   {lang}: {r[lang]}  ~  {r['ex_' + lang]}")
            if r.get("note"):
                print(f"   note: {r['note']}")


if __name__ == "__main__":
    main()
