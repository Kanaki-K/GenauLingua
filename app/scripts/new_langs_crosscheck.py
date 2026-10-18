#!/usr/bin/env python3
"""
Сверка пар языков: в каждой строке словаря все 10 языков должны показать
ОДИН смысл.

Бот учит любой язык с любого: француз учит чешский, турок — итальянский.
Карточка пары X→Y берёт из одной строки слово на X и на Y, причём не первое
значение, а то, что стоит в примере этого языка (main_meaning). Если в
итальянском примере одно значение, а в чешском другое, пара it↔cs врёт, хотя
каждый язык по отдельности верен немецкому.

Скрипт показывает, что бот реально выведет на карточке на каждом языке, и
отбирает строки, где это может разойтись: хоть один язык многозначен.

    python -m app.scripts.new_langs_crosscheck            # счёт и файлы cross/cross_NNN.txt
"""

from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from app.scripts.new_langs_check import load_jsonl  # noqa: E402
from app.services.language_service import main_meaning  # noqa: E402

BASE = Path(__file__).resolve().parent.parent.parent / "archive" / "new_langs"
ORDER = ("de", "ru", "uk", "en", "pl", "tr", "it", "es", "fr", "cs")


def as_word(s: dict, o: dict) -> SimpleNamespace:
    w = SimpleNamespace(word_de=s["de"], article=s.get("art"), example_de=s.get("ex_de"))
    for c in ("ru", "uk", "en", "pl", "tr"):
        setattr(w, f"translation_{c}", s.get(c))
        setattr(w, f"example_{c}", s.get(f"ex_{c}"))
    for c in ("it", "es", "fr", "cs"):
        setattr(w, f"translation_{c}", o.get(c))
        setattr(w, f"example_{c}", o.get(f"ex_{c}"))
    return w


def main() -> None:
    src = {}
    for f in (BASE / "src").glob("block_*.jsonl"):
        for r in load_jsonl(f):
            src[r["id"]] = r
    out = []
    for f in sorted((BASE / "out").glob("block_*.jsonl")):
        out.extend(load_jsonl(f))

    candidates = []
    for o in out:
        s = src[o["id"]]
        w = as_word(s, o)
        multi = any("," in (s.get(c) or "") for c in ("ru", "uk", "en", "pl", "tr")) or \
            any("," in (o.get(c) or "") for c in ("it", "es", "fr", "cs"))
        if not multi:
            continue
        shown = {c: main_meaning(w, c) for c in ORDER if c != "de"}
        candidates.append((o, s, shown))

    d = BASE / "cross"
    d.mkdir(exist_ok=True)
    size = 150
    for k in range(0, len(candidates), size):
        with (d / f"cross_{k // size:03d}.txt").open("w", encoding="utf-8", newline="\n") as fh:
            for o, s, shown in candidates[k:k + size]:
                art = f"{s['art']} " if s.get("art") else ""
                fh.write(f"#{o['id']} {art}{s['de']} [{s['pos']}] «{s['ex_de']}»\n")
                fh.write("   ПОКАЖЕТ: " + " | ".join(f"{c}: {shown[c]}" for c in ORDER if c != "de") + "\n")
                for c in ("it", "es", "fr", "cs"):
                    fh.write(f"   {c}: {o[c]} ~ {o['ex_' + c]}\n")
    print(f"строк всего {len(out)}, многозначных (кандидатов) {len(candidates)}, "
          f"файлов {-(-len(candidates) // size)} по {size} в {d}")


if __name__ == "__main__":
    main()
