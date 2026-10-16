#!/usr/bin/env python3
"""
Аудит переводов it/es/fr/cs случайными выборками и внесение найденного.

Выборки не пересекаются: вся база перемешивается одним зерном и режется
по 100 рядов. Аудитор файлы out/ не правит — он пишет найденное в
audit/patch_NNN.jsonl, а вносит этот скрипт: параллельные аудиторы иначе
затирали бы друг другу блоки, а так по каждой выборке остаётся счёт ошибок.

    python -m app.scripts.new_langs_audit sample --count 100 --size 100
    python -m app.scripts.new_langs_audit apply            # вхолостую
    python -m app.scripts.new_langs_audit apply --apply
    python -m app.scripts.new_langs_audit stats

Строка патча: {"id": 123, "field": "it" | "ex_it" | ... | "note",
               "old": "...", "new": "...", "kind": "смысл|пример|грамматика|...",
               "why": "..."}
Поле old сверяется с текущим значением: устаревший патч не вносится.
"""

from __future__ import annotations

import argparse
import collections
import contextlib
import io
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from app.scripts.new_langs_check import LANGS, check_file, load_jsonl  # noqa: E402

BASE = Path(__file__).resolve().parent.parent.parent / "archive" / "new_langs"
OUT, SRC, AUDIT = BASE / "out", BASE / "src", BASE / "audit"
FIELDS = {*LANGS, *("ex_" + c for c in LANGS), "note"}


def cmd_sample(count: int, size: int, seed: int) -> None:
    src = {}
    for f in SRC.glob("block_*.jsonl"):
        for r in load_jsonl(f):
            src[r["id"]] = r
    out = []
    for f in sorted(OUT.glob("block_*.jsonl")):
        out.extend(load_jsonl(f))
    rng = random.Random(seed)
    rng.shuffle(out)
    AUDIT.mkdir(exist_ok=True)
    for n in range(count):
        chunk = out[n * size:(n + 1) * size]
        if not chunk:
            break
        with (AUDIT / f"sample_{n:03d}.txt").open("w", encoding="utf-8", newline="\n") as fh:
            for r in chunk:
                s = src[r["id"]]
                art = f"{s['art']} " if s.get("art") else ""
                fh.write(f"#{r['id']} {art}{r['de']} [{s['pos']}] «{s['ex_de']}»  en: {s['en']}  ru: {s['ru']}\n")
                for c in LANGS:
                    fh.write(f"   {c}: {r[c]}  ~  {r['ex_' + c]}\n")
                if r.get("note"):
                    fh.write(f"   note: {r['note']}\n")
    print(f"выборок: {min(count, -(-len(out) // size))} по {size} (зерно {seed}) → {AUDIT}")


def load_patches() -> list[dict]:
    patches = []
    for f in sorted(AUDIT.glob("patch_*.jsonl")):
        for p in load_jsonl(f):
            p["_file"] = f.stem
            patches.append(p)
    return patches


def cmd_apply(apply: bool) -> None:
    rows_by_block: dict[Path, list[dict]] = {}
    where: dict[int, tuple[Path, int]] = {}
    for f in sorted(OUT.glob("block_*.jsonl")):
        rows = load_jsonl(f)
        rows_by_block[f] = rows
        for i, r in enumerate(rows):
            where[r["id"]] = (f, i)

    ok, done, stale, bad = 0, 0, [], []
    dirty: set[Path] = set()
    for p in load_patches():
        if p.get("field") not in FIELDS or p.get("id") not in where:
            bad.append(p)
            continue
        f, i = where[p["id"]]
        row = rows_by_block[f][i]
        if (row.get(p["field"]) or "") == (p.get("new") or "") and p.get("new") != p.get("old"):
            done += 1  # внесено прежним запуском
            continue
        if (row.get(p["field"]) or "") != (p.get("old") or ""):
            stale.append(p)
            continue
        if p.get("new"):
            row[p["field"]] = p["new"]
        else:
            row.pop(p["field"], None)
        dirty.add(f)
        ok += 1

    print(f"патчей внесено бы: {ok}; уже внесено: {done}; old не совпал: {len(stale)}; негодных: {len(bad)}")
    for p in stale[:20]:
        print(f"  old не совпал: {p['_file']} id={p['id']} {p['field']}: «{p.get('old')}»")
    for p in bad[:20]:
        print(f"  негодный: {p}")
    if not apply:
        return
    for f in dirty:
        f.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows_by_block[f]),
                     encoding="utf-8", newline="\n")
    with contextlib.redirect_stdout(io.StringIO()):
        errors = sum(check_file(f)[0] for f in sorted(dirty))
    print(f"записано блоков: {len(dirty)}; ошибок проверки после: {errors}")


def cmd_stats() -> None:
    patches = load_patches()
    by_sample = collections.Counter(p["_file"] for p in patches)
    rows_by_sample = collections.defaultdict(set)
    for p in patches:
        rows_by_sample[p["_file"]].add(p["id"])
    kinds = collections.Counter(p.get("kind", "?") for p in patches)
    langs = collections.Counter(p["field"].replace("ex_", "") for p in patches)
    done = sorted(AUDIT.glob("done_*.txt"))
    per = [len(rows_by_sample.get(f"patch_{d.stem[5:]}", ())) for d in done]
    print(f"выборок проверено: {len(done)}; правок: {len(patches)}; "
          f"рядов с ошибкой: {sum(len(v) for v in rows_by_sample.values())}")
    if per:
        print(f"рядов с ошибкой на выборку из 100: среднее {sum(per) / len(per):.1f}, "
              f"мин {min(per)}, макс {max(per)}")
    print("по видам:", dict(kinds.most_common()))
    print("по языкам:", dict(langs.most_common()))


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sample")
    s.add_argument("--count", type=int, default=100)
    s.add_argument("--size", type=int, default=100)
    s.add_argument("--seed", type=int, default=20261017)
    a = sub.add_parser("apply")
    a.add_argument("--apply", action="store_true")
    sub.add_parser("stats")
    args = ap.parse_args()
    if args.cmd == "sample":
        cmd_sample(args.count, args.size, args.seed)
    elif args.cmd == "apply":
        cmd_apply(args.apply)
    else:
        cmd_stats()


if __name__ == "__main__":
    main()
