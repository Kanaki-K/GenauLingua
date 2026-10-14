#!/usr/bin/env python3
"""
Свести два источника дефектных примеров в один вход для правки.

Источники ловят разное, и это измерено, а не предположено.

Отсев (app/scripts/example_quality.py) сравнивает пример со словом по началу
основы и находит случаи, где слова в примере нет вовсе: «Подсобить» → «Иногда
нужно помочь удаче». Грамматику и естественность он не видит, а на сильном
спряжении даёт ложные тревоги: «verschwinden» и «verschwunden» для него
непохожие слова.

Пометки модели (examples_ok из прогона переводов) — наоборот: видят
грамматическую ошибку и подмену слова, но выставляются только тем словам,
которые через прогон прошли.

Насколько это важно: на сведении 719 пар пересечение составило 13. То есть
прогон одного источника пропустил бы примерно половину дефектов. Отсюда
правило — после каждого прогона переводов сводить оба и править сведённое.

Формат на выходе — как у отсева: по строке на пару «слово + язык», с текстом
слова и текущего примера, потому что именно это ждёт fix_examples.

    python -m app.scripts.example_quality --out defects.jsonl
    python -m app.scripts.merge_defects --detector defects.jsonl \\
        --model wordbase_a1a2_bad_examples.jsonl --out defects_merged.jsonl
    python -m app.scripts.fix_examples propose --in defects_merged.jsonl
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
from app.services.language_service import LANGUAGES, SUPPORTED_LANGS

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("merge-defects")


def read(path: str) -> list[dict]:
    file = pathlib.Path(path)
    if not file.exists():
        logger.warning("нет файла %s — пропущен", path)
        return []
    return [json.loads(line) for line in file.read_text(encoding="utf-8").splitlines()
            if line.strip()]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--detector", nargs="*", default=[],
                    help="файлы от example_quality: по строке на пару «слово + язык»")
    ap.add_argument("--model", nargs="*", default=[],
                    help="файлы *_bad_examples.jsonl от прогона переводов")
    ap.add_argument("--out", default="defects_merged.jsonl")
    args = ap.parse_args()

    if not args.detector and not args.model:
        ap.error("нужен хотя бы один источник: --detector или --model")

    pairs: dict[tuple[int, str], str] = {}

    for path in args.detector:
        rows = read(path)
        for row in rows:
            pairs[(row["id"], row["lang"])] = "отсев"
        logger.info("%s: %d пар от отсева", path, len(rows))

    for path in args.model:
        rows = read(path)
        added = 0
        for row in rows:
            for lang in row.get("langs", []):
                if lang not in SUPPORTED_LANGS:
                    continue
                key = (row["id"], lang)
                if key in pairs:
                    pairs[key] = "оба"
                else:
                    pairs[key] = "модель"
                    added += 1
        logger.info("%s: %d слов, новых пар %d", path, len(rows), added)

    if not pairs:
        logger.error("ни одной пары не собралось")
        return 1

    # Текст слова и примера берётся из базы, а не из файлов: файлы могли
    # устареть, а править нужно то, что в базе стоит сейчас
    engine = create_engine(settings.DATABASE_URL_SYNC)
    columns = ["id", "word_de"]
    for lang in SUPPORTED_LANGS:
        cfg = LANGUAGES[lang]
        columns.extend([cfg.word_attr, cfg.example_attr])
    with engine.connect() as conn:
        rows_db = {
            r["id"]: dict(r)
            for r in conn.execute(text(
                f"SELECT {', '.join(dict.fromkeys(columns))}, level::text AS level "
                f"FROM words WHERE id = ANY(:ids)"
            ), {"ids": sorted({i for i, _ in pairs})}).mappings()
        }

    out_path = pathlib.Path(args.out)
    written = skipped = 0
    by_source: dict[str, int] = {}
    by_lang: dict[str, int] = {}

    with out_path.open("w", encoding="utf-8") as out:
        for (word_id, lang), source in sorted(pairs.items()):
            row = rows_db.get(word_id)
            if row is None:
                skipped += 1
                continue
            cfg = LANGUAGES[lang]
            word = (row[cfg.word_attr] or "").strip()
            if not word:
                # Перевода на этот язык нет — править нечего. Польский так
                # стоит на всех уровнях выше A2
                skipped += 1
                continue
            out.write(json.dumps({
                "id": word_id,
                "level": row["level"],
                "word": word,
                "example": (row[cfg.example_attr] or "").strip(),
                "lang": lang,
                "source": source,
            }, ensure_ascii=False) + "\n")
            written += 1
            by_source[source] = by_source.get(source, 0) + 1
            by_lang[lang] = by_lang.get(lang, 0) + 1

    logger.info("пар всего %d, записано %d, отброшено (нет слова или перевода) %d",
                len(pairs), written, skipped)
    logger.info("по источнику: %s",
                ", ".join(f"{k} {v}" for k, v in sorted(by_source.items())))
    logger.info("по языкам: %s",
                ", ".join(f"{k} {v}" for k, v in sorted(by_lang.items())))
    logger.info("→ %s", out_path)

    both = by_source.get("оба", 0)
    if written and both / written < 0.1:
        logger.info(
            "Пересечение источников %d из %d — каждый нашёл то, что второй не "
            "видит по устройству. Это и есть довод сводить оба.", both, written,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
