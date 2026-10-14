# -*- coding: utf-8 -*-
"""
Сравнить «было» и «стало» на случайных рядах до применения в базу.

Отличается от wordbase_sample_review тем, что смотрит не базу, а предложения:
рядом стоят нынешний перевод и предложенный, и видно, что именно меняется.
Это и есть проверка перед тем, как что-то применять.

Выборка расслоена по уровням и воспроизводима: зерно печатается.

Автоматически отмечается то, что видно без языкового суждения: потерянные
значения, смена алфавита, пропавшая диакритика, пустые поля. Но решение за
глазами — «естественный ли перевод» правилами не проверяется.

    python -m app.scripts.review_proposals --file wordbase_a1a2.jsonl --size 20
    python -m app.scripts.review_proposals --file wordbase_a1a2.jsonl --rounds 10 --size 100 --summary
    python -m app.scripts.review_proposals --file wordbase_a1a2.jsonl --only-changed
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import pathlib
import random
import sys
import unicodedata

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
os.environ.setdefault("ENV_FILE", ".env.local")

from sqlalchemy import text

from app.database.session import AsyncSessionLocal
from app.services.language_service import LANGUAGES

LEVELS = ("A1", "A2", "B1", "B2", "C1", "C2")
LANGS = ("ru", "uk", "en", "tr", "pl")

BASE_SEED = 20260930

SCRIPT_OF = {"ru": "CYRILLIC", "uk": "CYRILLIC",
             "en": "LATIN", "tr": "LATIN", "pl": "LATIN"}

# Диакритика, потеря которой в предложенном переводе — ошибка, потому что
# раньше она была
DIACRITICS = {
    "tr": set("çğıöşüÇĞİÖŞÜ"),
    "pl": set("ąćęłńóśźżĄĆĘŁŃÓŚŹŻ"),
    "uk": set("іїєґІЇЄҐ"),
}


def joined(translation: dict) -> str:
    """Значения в одну строку — так же, как их применит apply."""
    meanings = translation.get("meanings") or []
    primary = translation.get("primary") or ""
    ordered = [primary] + [m for m in meanings if m != primary]
    seen, result = set(), []
    for item in ordered:
        key = (item or "").strip().lower()
        if key and key not in seen:
            seen.add(key)
            result.append(item.strip())
    return ", ".join(result)


def wrong_script(value: str, expected: str) -> bool:
    for ch in value:
        if not ch.isalpha():
            continue
        try:
            name = unicodedata.name(ch)
        except ValueError:
            return True
        if ("LATIN" in name or "CYRILLIC" in name) and expected not in name:
            return True
    return False


def machine_notes(old: dict, new: dict) -> list[str]:
    """
    Что видно без языкового суждения.

    Главное здесь — потеря: если раньше значений было больше, чем теперь,
    предложение хуже прежнего, и это надо заметить до применения.
    """
    notes: list[str] = []

    for lang in LANGS:
        cfg = LANGUAGES[lang]
        before = (old.get(cfg.word_attr) or "").strip()
        after = joined(new[lang])

        if not after:
            notes.append(f"{lang}: предложен пустой перевод")
            continue

        if wrong_script(after, SCRIPT_OF[lang]):
            notes.append(f"{lang}: чужой алфавит — {after!r}")

        # Потеря значений: было перечисление, стало одно
        before_count = len([p for p in before.replace("/", ",").split(",") if p.strip()])
        after_count = len(new[lang].get("meanings") or [])
        if before_count > 1 and after_count < before_count:
            notes.append(
                f"{lang}: значений было {before_count}, стало {after_count} — "
                f"{before!r} → {after!r}"
            )

        expected = DIACRITICS.get(lang)
        if expected and (set(before) & expected) and not (set(after) & expected):
            notes.append(f"{lang}: диакритика пропала — {before!r} → {after!r}")

    example_pl = (new.get("example_pl") or "").strip()
    if not example_pl:
        notes.append("pl: нет примера")
    elif len(example_pl.split()) < 2:
        notes.append(f"pl: пример не фраза — {example_pl!r}")

    return notes


async def load_current(ids: list[int]) -> dict[int, dict]:
    columns = ["id", "word_de", "article", "pos::text AS pos", "level::text AS level"]
    for lang in LANGS:
        cfg = LANGUAGES[lang]
        columns.append(cfg.word_attr)
        columns.append(cfg.example_attr)
    columns.append("example_de")

    async with AsyncSessionLocal() as s:
        rows = (await s.execute(
            text(f"SELECT {', '.join(columns)} FROM words WHERE id = ANY(:ids)"),
            {"ids": ids},
        )).mappings().all()
    return {r["id"]: dict(r) for r in rows}


def stratified(items: list[dict], size: int, seed: int) -> list[dict]:
    rng = random.Random(seed)
    by_level: dict[str, list[dict]] = {}
    for item in items:
        by_level.setdefault(item.get("_level") or "?", []).append(item)

    chosen: list[dict] = []
    for level in LEVELS:
        bucket = by_level.get(level, [])
        if not bucket:
            continue
        want = max(1, round(size * len(bucket) / len(items)))
        chosen.extend(rng.sample(bucket, min(want, len(bucket))))
    rng.shuffle(chosen)
    return chosen[:size]


def render(old: dict, new: dict, index: int) -> str:
    article = (old.get("article") or "").strip()
    head = old.get("word_de") or ""
    if article and article != "-":
        head = f"{article} {head}"

    lines = [f"─── {index}. {head}   [{old['pos']}, {old['level']}, id={old['id']}]"]
    if old.get("example_de"):
        lines.append(f"      de · {old['example_de']}")

    for lang in LANGS:
        cfg = LANGUAGES[lang]
        before = (old.get(cfg.word_attr) or "—").strip() or "—"
        after = joined(new[lang]) or "—"
        mark = "  " if before == after else "→ "
        lines.append(f"   {mark}{lang}  было:  {before}")
        lines.append(f"      {'  '}   стало: {after}")

    example_pl = (new.get("example_pl") or "").strip()
    if example_pl:
        lines.append(f"      pl · {example_pl}   (новый пример)")

    if not new.get("lemma_ok"):
        lines.append("      ! слово не в словарной форме")
    if not new.get("level_ok") and new.get("suggested_level"):
        lines.append(f"      ! уровень: {old['level']} → предлагается {new['suggested_level']}")
    if new.get("note"):
        lines.append(f"      ! {new['note']}")

    bad = [c for c, ok in (new.get("examples_ok") or {}).items() if ok is False]
    if bad:
        lines.append(f"      ! негодные примеры: {', '.join(bad)}")

    for note in machine_notes(old, new):
        lines.append(f"      ⚠ {note}")

    return "\n".join(lines)


async def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", required=True)
    ap.add_argument("--rounds", type=int, default=1)
    ap.add_argument("--size", type=int, default=20)
    ap.add_argument("--seed", type=int, default=BASE_SEED)
    ap.add_argument("--summary", action="store_true",
                    help="только сводка машинных замечаний, без рядов")
    ap.add_argument("--only-flagged", action="store_true",
                    help="печатать только ряды с машинными замечаниями")
    args = ap.parse_args()

    proposals = [
        json.loads(line)
        for line in pathlib.Path(args.file).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    current = await load_current([p["id"] for p in proposals])

    for item in proposals:
        row = current.get(item["id"])
        item["_level"] = row["level"] if row else "?"

    proposals = [p for p in proposals if p["id"] in current]
    print(f"предложений: {len(proposals)}, зерно {args.seed}")
    print()

    all_notes: dict[str, int] = {}
    total_flagged = total_seen = 0

    for number in range(1, args.rounds + 1):
        seed = args.seed + number
        sample = stratified(proposals, args.size, seed)

        flagged = []
        for item in sample:
            notes = machine_notes(current[item["id"]], item)
            if notes:
                flagged.append(item)
                for note in notes:
                    key = note.split(":")[0] + ": " + note.split(":")[1].strip().split("—")[0].strip()
                    all_notes[key] = all_notes.get(key, 0) + 1

        total_flagged += len(flagged)
        total_seen += len(sample)

        print("=" * 74)
        print(f"ВЫБОРКА {number}: {len(sample)} рядов, зерно {seed}, "
              f"машинных замечаний у {len(flagged)} ({len(flagged)/len(sample)*100:.0f}%)")
        print("=" * 74)

        if not args.summary:
            shown = flagged if args.only_flagged else sample
            for index, item in enumerate(shown, 1):
                print()
                print(render(current[item["id"]], item, index))
        print()

    if args.rounds > 1 or args.summary:
        print("=" * 74)
        print(f"ИТОГО: рядов {total_seen}, с машинными замечаниями {total_flagged} "
              f"({total_flagged/total_seen*100:.1f}%)")
        if all_notes:
            print("\nчто именно:")
            for key, count in sorted(all_notes.items(), key=lambda kv: -kv[1]):
                print(f"   {count:>5}  {key}")
        print("\nМашинные замечания — это не оценка качества перевода.")
        print("Естественность проверяется только глазами.")

    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
