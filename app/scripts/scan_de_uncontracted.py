"""
Несжатый предлог с артиклем в немецком эталоне: «in dem Safe» вместо «im».

Стяжение (im, am, zum, zur, beim, vom, ins, ans) — немецкая норма.
Несжатая форма МАРКИРОВАНА: она значит «в ТОМ самом» и указывает на уже
упомянутое. В одиночной фразе-примере указывать не на что.

ЗАМЕР (блок 48): 50 попаданий по всей базе, ни одного после запятой — то
есть ни одного, где несжатая форма была бы относительным местоимением
(«das Haus, in dem ich wohne»). Разметка вручную: 23 дефекта,
27 законных. Дефекты правлены `fix_de_uncontracted.py`.

ПОЧЕМУ ЭТО НЕ ГЕЙТ. Законный остаток у класса ЕСТЬ, и он большой:

 • между предлогом и существительным стоит прилагательное — несжатая
   форма там немаркирована: «von dem neuen Spielzeug», «in dem alten
   Wasser», «an dem berühmten Sänger»;
 • существительное — СОБЫТИЕ, которое фраза предполагает известным:
   «bei dem Unfall», «bei dem Konzert», «bei dem Projekt», «von dem
   Abend». Это стандартный немецкий газетный оборот.

Отличить одно от другого без знания языка нельзя, поэтому примета держит
27 законных рядов СПИСКОМ и падает, если список изменился: появился новый
несжатый оборот или исчез законный. Решение по каждому новому — глазами.

    python -m app.scripts.scan_de_uncontracted
    python -m app.scripts.scan_de_uncontracted --selfcheck
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

PAIRS = (
    ("in dem", "im"),
    ("an dem", "am"),
    ("zu dem", "zum"),
    ("zu der", "zur"),
    ("bei dem", "beim"),
    ("von dem", "vom"),
    ("in das", "ins"),
    ("an das", "ans"),
)

# 27 рядов, размеченных вручную в блоке 48 как ЗАКОННЫЕ.
LEGIT: frozenset[int] = frozenset({
    # прилагательное между предлогом и существительным
    7138, 10702, 11161, 13148, 15138, 15634, 16743,
    # существительное-событие, известное из самой фразы
    2280, 6733, 6836, 6889, 8260, 8267, 9088, 10219, 10932, 11565,
    12570, 12809, 14571, 16052, 16142, 16191, 16448, 16732, 17713,
    # «in dem Fall» — газетный оборот про уже названное дело
    8795,
})

_RES = [
    (re.compile(r"(?<![\wäöüßÄÖÜ])" + bad + r"(?![\wäöüßÄÖÜ])", re.I), bad, good)
    for bad, good in PAIRS
]


def findings(example: str) -> list[tuple[str, str, bool]]:
    """(несжатое, стяжение, законно ли по запятой перед ним)."""
    out: list[tuple[str, str, bool]] = []
    for pattern, bad, good in _RES:
        for match in pattern.finditer(example or ""):
            before = (example or "")[: match.start()].rstrip()
            out.append((bad, good, before.endswith(",")))
    return out


def selfcheck() -> int:
    good_phrases = [
        "Er verschloss alle Wertsachen im Safe",
        "Das Haus, in dem ich wohne, ist alt",
        "Wir fahren zum Bahnhof",
        "Sie wohnt am Meer",
    ]
    bad_phrases = [
        "Er verschloss alle Wertsachen in dem Safe",
        "Die Grafik in dem Spiel ist beeindruckend",
        "Das Bajonett war an das Gewehr befestigt",
    ]
    failures = 0
    for phrase in good_phrases:
        hits = [f for f in findings(phrase) if not f[2]]
        if hits:
            print(f"GOOD помечен: {phrase!r} -> {hits}")
            failures += 1
    for phrase in bad_phrases:
        hits = [f for f in findings(phrase) if not f[2]]
        if not hits:
            print(f"BAD не помечен: {phrase!r}")
            failures += 1
    if failures:
        print(f"САМОПРОВЕРКА ПРОВАЛЕНА: {failures}")
        return 1
    print(
        f"самопроверка: {len(good_phrases)} верных и {len(bad_phrases)} "
        "битых различены (запятая перед предлогом снимает попадание)"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--selfcheck", action="store_true")
    args = parser.parse_args()

    if args.selfcheck:
        return selfcheck()

    engine = create_engine(settings.DATABASE_URL_SYNC)
    with engine.connect() as conn:
        rows = conn.execute(
            text("SELECT id, word_de, example_de FROM words ORDER BY id")
        ).mappings().all()

    found: dict[int, tuple[str, str, str]] = {}
    for row in rows:
        hits = [f for f in findings(row["example_de"] or "") if not f[2]]
        if hits:
            found[row["id"]] = (row["word_de"], hits[0][0], row["example_de"])

    unexpected = sorted(set(found) - LEGIT)
    vanished = sorted(LEGIT - set(found))

    for wid in sorted(found):
        word, bad, example = found[wid]
        mark = "   " if wid in LEGIT else "НОВОЕ"
        print(f"{mark} {wid:>6}  {word:<22} {bad!r}")
        print(f"              {example}")

    print(f"\nвсего: {len(found)}, законных по разметке: {len(LEGIT)}")
    if unexpected:
        print(f"НОВЫЕ несжатые обороты: {unexpected}")
    if vanished:
        print(f"ИСЧЕЗЛИ из законных: {vanished}")
    if unexpected or vanished:
        print("Список законных изменился — разметить глазами и обновить LEGIT")
        return 1
    print("остаток совпадает с разметкой блока 48")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
