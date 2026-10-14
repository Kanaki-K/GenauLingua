#!/usr/bin/env python3
"""
Поднять уровень словам, которые сложнее, чем размечены.

Почему это важно. Замер на живых ответах: слова, помеченные как сложнее
своего уровня, дают на A1 и A2 точность 78,6% против 88,9% у остальных слов
того же уровня — разница 10,4 пункта. И стоят они в начале сессии: каждый
пятый первый вопрос такое слово. Прод-аналитика показывала, что 31,5% викторин
умирают к второму вопросу, и вот механизм: человек открывает A1, получает
«Angehörige», ошибается и уходит.

ДВИГАЮТСЯ ТОЛЬКО СЛОВА С ДВУМЯ СИГНАЛАМИ. Пометка модели — суждение, а не
эталон: частотное слово вроде «Untersuchung» может быть уместно на A1 несмотря
на сложность, потому что учебная лексика для начинающих включает конкретные
бытовые слова. Поэтому нужна ещё и низкая точность на настоящих ответах.
Пересечение двух независимых сигналов надёжнее каждого по отдельности.

Слова без ответов не двигаются вообще: подтвердить пометку нечем.

    python -m app.scripts.fix_levels --dry-run
    python -m app.scripts.fix_levels
    python -m app.scripts.fix_levels --accuracy 0.75 --min-answers 5
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
os.environ.setdefault("ENV_FILE", ".env.local")

from sqlalchemy import create_engine, text

from app.config import settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("fix-levels")

ORDER = ["A1", "A2", "B1", "B2", "C1", "C2"]

# Ниже этой точности на живых ответах пометка модели считается подтверждённой.
# Средняя точность по базе 88%, у правильно размеченных слов A1 и A2 — 88,9%,
# так что 80% это заметно хуже нормы, но не шум.
ACCURACY_THRESHOLD = 0.80

# Меньше этого числа ответов — статистики нет. Три ответа мало для уверенности,
# но при большем пороге под правку попадает слишком мало слов: у половины
# помеченных ответов вообще нет.
MIN_ANSWERS = 3


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--marked", nargs="+", default=["wordbase_a1a2_marked.jsonl"],
                    help="файлы с пометками от прогона переводов")
    ap.add_argument("--accuracy", type=float, default=ACCURACY_THRESHOLD)
    ap.add_argument("--min-answers", type=int, default=MIN_ANSWERS)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    suggested: dict[int, str] = {}
    for name in args.marked:
        path = pathlib.Path(name)
        if not path.exists():
            logger.warning("нет файла %s", path)
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get("level_ok", True) or not row.get("suggested_level"):
                continue
            suggested[row["id"]] = row["suggested_level"]

    if not suggested:
        logger.error("помеченных слов не найдено")
        return 1

    engine = create_engine(settings.DATABASE_URL_SYNC)
    with engine.connect() as conn:
        words = {
            r["id"]: dict(r)
            for r in conn.execute(text("""
                SELECT id, word_de, level::text AS level, frequency_rank
                FROM words WHERE id = ANY(:ids)
            """), {"ids": list(suggested)}).mappings()
        }
        # Точность по настоящим ответам, а не по счётчикам слова: счётчики
        # общие на все языки, а ответы привязаны к сессиям
        stats = {
            r["word_id"]: dict(r)
            for r in conn.execute(text("""
                SELECT word_id, COUNT(*) AS answers,
                       SUM(CASE WHEN is_correct THEN 1 ELSE 0 END) AS correct
                FROM quiz_questions WHERE word_id = ANY(:ids)
                GROUP BY word_id
            """), {"ids": list(suggested)}).mappings()
        }
        # Занятые пары «слово + уровень»: перенос не должен упереться в
        # уникальность
        occupied = {
            (r["word_de"].lower(), r["level"])
            for r in conn.execute(text(
                "SELECT word_de, level::text AS level FROM words")).mappings()
        }

    updates: list[dict] = []
    no_data: list[dict] = []
    good_accuracy: list[dict] = []
    collisions: list[dict] = []
    wrong_direction = 0

    for word_id, target in suggested.items():
        word = words.get(word_id)
        if word is None:
            continue

        # Двигаем только вверх: понижение уровня делает викторину легче, а не
        # исправляет причину отвала, и таких случаев всего шесть
        if ORDER.index(target) <= ORDER.index(word["level"]):
            wrong_direction += 1
            continue

        stat = stats.get(word_id)
        answers = stat["answers"] if stat else 0
        accuracy = (stat["correct"] / stat["answers"]) if stat and stat["answers"] else None

        if answers < args.min_answers:
            no_data.append({**word, "target": target, "answers": answers})
            continue
        if accuracy is not None and accuracy >= args.accuracy:
            # Пометка не подтверждается: люди отвечают верно, слово уместно
            good_accuracy.append({**word, "target": target,
                                  "accuracy": round(accuracy, 3), "answers": answers})
            continue

        if (word["word_de"].lower(), target) in occupied:
            collisions.append({**word, "target": target})
            continue

        updates.append({
            "id": word_id, "level": target,
            "word_de": word["word_de"], "was": word["level"],
            "accuracy": round(accuracy, 3) if accuracy is not None else None,
            "answers": answers,
        })

    logger.info(
        "к переносу %d | без ответов %d | точность в норме %d | "
        "столкновений %d | не вверх %d",
        len(updates), len(no_data), len(good_accuracy), len(collisions), wrong_direction,
    )

    for name, items in (("no_answers", no_data), ("accuracy_ok", good_accuracy),
                        ("collisions", collisions)):
        if items:
            path = pathlib.Path(f"level_{name}.jsonl")
            with path.open("w", encoding="utf-8") as fh:
                for item in items:
                    fh.write(json.dumps(item, ensure_ascii=False, default=str) + "\n")
            logger.info("  %s: %d → %s", name, len(items), path)

    if args.dry_run:
        print(f"\n--dry-run: перенеслось бы {len(updates)} слов\n")
        for u in sorted(updates, key=lambda x: -x["answers"])[:25]:
            acc = f"{u['accuracy'] * 100:.0f}%" if u["accuracy"] is not None else "—"
            print(f"  {u['word_de']!r:<24} {u['was']} → {u['level']}   "
                  f"ответов {u['answers']:>3}, верно {acc}")
        if len(updates) > 25:
            print(f"  ... ещё {len(updates) - 25}")
        print()
        return 0

    if not updates:
        logger.info("переносить нечего")
        return 0

    with engine.begin() as conn:
        conn.execute(
            text("UPDATE words SET level = CAST(:level AS cefrlevel) WHERE id = :id"),
            [{"id": u["id"], "level": u["level"]} for u in updates],
        )

    logger.info("уровень поднят: %d слов", len(updates))
    logger.warning(
        "Прогресс не затронут — он привязан к id. Но слова ушли с прежнего "
        "уровня, и ученики этого уровня их больше не увидят: в этом и смысл.\n"
        "Пересобирать группы не нужно: уровень в ключ схлопывания не входит."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
