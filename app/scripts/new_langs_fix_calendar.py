#!/usr/bin/env python3
"""
Месяцы и дни недели в it/es/fr — без артикля (GUIDE: «Месяцы и дни недели»).

Блоки делались до этого правила, и в части из них стоит «l'aprile»,
«el junio», «le mardi». Список конечный, поэтому правится скриптом, а не
вычиткой: у ряда, чьё немецкое слово — месяц или день недели (NOUN),
снимается определённый артикль в it/fr у всех значений и в es — у месяцев
(испанские дни недели остаются с «el»), и ставится note «без артикля».
Наречия (dienstags) и составные (Sonntagabend) не трогаются.

    python -m app.scripts.new_langs_fix_calendar           # вхолостую
    python -m app.scripts.new_langs_fix_calendar --apply
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from app.scripts.new_langs_check import load_jsonl  # noqa: E402

OUT = Path(__file__).resolve().parent.parent.parent / "archive" / "new_langs" / "out"
SRC = OUT.parent / "src"

MONTHS = {"Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August",
          "September", "Oktober", "November", "Dezember"}
DAYS = {"Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag",
        "Sonnabend", "Sonntag"}

ART = re.compile(r"^(il |lo |la |l'|el |le )", re.IGNORECASE)


def strip(value: str) -> str:
    return ", ".join(ART.sub("", m.strip()) for m in value.split(","))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    pos = {}
    for f in SRC.glob("block_*.jsonl"):
        for r in load_jsonl(f):
            pos[r["id"]] = r["pos"]

    changed = 0
    for path in sorted(OUT.glob("block_*.jsonl")):
        rows = load_jsonl(path)
        dirty = False
        for r in rows:
            if pos.get(r["id"]) != "NOUN" or r["de"] not in MONTHS | DAYS:
                continue
            langs = ("it", "fr", "es") if r["de"] in MONTHS else ("it", "fr")
            row_changed = False
            for lang in langs:
                new = strip(r[lang])
                if new != r[lang]:
                    print(f"{path.name} {r['de']} {lang}: {r[lang]} → {new}")
                    r[lang] = new
                    row_changed = dirty = True
                    changed += 1
            if row_changed and "без артикля" not in (r.get("note") or ""):
                r["note"] = ((r.get("note") or "") + " без артикля (месяц/день недели)").strip()
        if dirty and args.apply:
            path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows),
                            encoding="utf-8")
    print(f"исправлено значений: {changed}" + ("" if args.apply else " (вхолостую)"))


if __name__ == "__main__":
    main()
