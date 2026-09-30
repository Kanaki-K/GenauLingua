# -*- coding: utf-8 -*-
"""
Записать указания «эта строка — форма, а лемма вот эта».

Источник — файл столкновений от fix_lemmas: пары, где лемма уже есть в базе на
том же уровне, и переименовать форму нельзя из-за уникальности.

Что даёт указание: форма перестаёт появляться в викторине, потому что при
сборке групп попадает в группу леммы и та назначается канонической. Прогресс
с формы сливается на лемму тем же кодом, что переносил его при переходе на
многоязычность. Ничего не удаляется — 326 исторических ответов в викторинах
остаются на месте.

    python -m app.scripts.apply_lemma_overrides --file lemma_fixes_collisions.jsonl --dry-run
    python -m app.scripts.apply_lemma_overrides --file lemma_fixes_collisions.jsonl
    python -m app.scripts.apply_lemma_overrides --clear      # откат
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
logger = logging.getLogger("lemma-overrides")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", default="lemma_fixes_collisions.jsonl")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--clear", action="store_true",
                    help="удалить все указания — откат")
    args = ap.parse_args()

    engine = create_engine(settings.DATABASE_URL_SYNC)

    if args.clear:
        with engine.begin() as conn:
            removed = conn.execute(text("DELETE FROM word_lemma_overrides")).rowcount
        logger.info("указаний удалено: %d", removed)
        logger.warning("пересоберите группы: python -m app.scripts.rebuild_word_groups")
        return 0

    path = pathlib.Path(args.file)
    if not path.exists():
        logger.error("нет файла %s", path)
        return 1

    rows = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    with engine.connect() as conn:
        words = {
            r["id"]: dict(r)
            for r in conn.execute(text(
                "SELECT id, word_de, level::text AS level, frequency_rank, times_shown "
                "FROM words"
            )).mappings()
        }

    payload: list[dict] = []
    rejected: list[dict] = []

    for r in rows:
        form_id, lemma_id = r.get("id"), r.get("occupied_by")
        if form_id is None or lemma_id is None or form_id == lemma_id:
            rejected.append({**r, "reason": "нет пары или ссылка на себя"})
            continue
        if form_id not in words or lemma_id not in words:
            rejected.append({**r, "reason": "слова нет в базе"})
            continue

        form, lemma = words[form_id], words[lemma_id]
        # Уровни должны совпадать: указание объединяет одно слово, а не
        # переносит его между уровнями
        if form["level"] != lemma["level"]:
            rejected.append({**r, "reason": f"разные уровни: {form['level']} и {lemma['level']}"})
            continue

        payload.append({
            "word_id": form_id,
            "lemma_word_id": lemma_id,
            "reason": f"{form['word_de']} — форма от {lemma['word_de']}",
        })

    logger.info("к записи %d, отклонено %d", len(payload), len(rejected))
    for item in rejected[:5]:
        logger.warning("  %s: %s", item.get("current"), item["reason"])

    if args.dry_run:
        print(f"\n--dry-run: записалось бы {len(payload)} указаний\n")
        for item in payload[:20]:
            form = words[item["word_id"]]
            lemma = words[item["lemma_word_id"]]
            print(f"  {form['word_de']!r:<16} → {lemma['word_de']!r:<16} "
                  f"{form['level']}  показов формы {form['times_shown']}, "
                  f"леммы {lemma['times_shown']}")
        if len(payload) > 20:
            print(f"  ... ещё {len(payload) - 20}")
        print()
        return 0

    if not payload:
        logger.info("записывать нечего")
        return 0

    with engine.begin() as conn:
        # Повторный прогон не должен падать: указание переписывается
        conn.execute(text("""
            INSERT INTO word_lemma_overrides (word_id, lemma_word_id, reason, created_at)
            VALUES (:word_id, :lemma_word_id, :reason, NOW())
            ON CONFLICT (word_id) DO UPDATE
                SET lemma_word_id = EXCLUDED.lemma_word_id,
                    reason = EXCLUDED.reason
        """), payload)

    logger.info("указаний записано: %d", len(payload))
    logger.warning(
        "ОБЯЗАТЕЛЬНО пересобрать группы — без этого указания не действуют:\n"
        "    python -m app.scripts.rebuild_word_groups\n"
        "Прогресс с форм сольётся на леммы, ничего не удаляется."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
