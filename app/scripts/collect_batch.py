#!/usr/bin/env python3
"""
Забрать результаты пакета, оставшегося без присмотра.

Зачем это нужно. propose создаёт пакет и ждёт его в том же процессе. Если
процесс прерван — а он идёт часами, — результаты остаются на сервере
невостребованными, хотя они уже посчитаны и оплачены.

Случай из практики: пакет на 51 запрос я объявил зависшим и отменил, потому
что он три часа показывал ноль готовых. Отмена в Batches API работает по
возможности: запросы, уже начатые, доводятся до конца и списываются. Пакет
завершился с 50 успешными из 51, и эти 50 лежали на сервере ещё девять часов,
пока я не додумался их запросить. Забираются они бесплатно.

Отсюда правило: прежде чем платить за повторный прогон, посмотрите список
пакетов. Отменённый пакет — не пустой пакет.

    python -m app.scripts.collect_batch --list
    python -m app.scripts.collect_batch msgbatch_... --kind examples
    python -m app.scripts.collect_batch msgbatch_... --kind words

Проверка соответствия ослаблена намеренно: разбивка на порции живёт только в
памяти процесса, который пакет создал, и восстановить, какой запрос какие
слова просил, нечем. Принимается всё, чей id есть в базе. Содержательную
проверку делает apply соответствующего скрипта — он сверяет и текст, и то, что
слово в примере видно.
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
os.environ.setdefault("ENV_FILE", ".env.local")

from sqlalchemy import create_engine, text

from app.config import settings
from app.services.language_service import SUPPORTED_LANGS

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("collect-batch")

# Какой прогон какой ключ кладёт в ответ. Ключ — единственный надёжный признак:
# custom_id у разных прогонов выглядит похоже
KINDS = {
    "examples": "app.scripts.fix_examples",       # переписанные примеры
    "words": "app.scripts.retranslate_wordbase",  # переводы
}


def api_key() -> str:
    """
    Ключ берётся из настроек, а при их отсутствии — из .env.local напрямую.
    Скрипт запускают руками и нередко без поднятого окружения.
    """
    key = getattr(settings, "ANTHROPIC_API_KEY", None) or os.environ.get("ANTHROPIC_API_KEY")
    if key:
        return str(key)
    env = pathlib.Path(os.environ.get("ENV_FILE", ".env.local"))
    if env.exists():
        found = re.search(r"ANTHROPIC_API_KEY\s*=\s*(\S+)", env.read_text(encoding="utf-8"))
        if found:
            return found.group(1).strip().strip("\"'")
    raise SystemExit("не найден ANTHROPIC_API_KEY")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("batch_id", nargs="?")
    ap.add_argument("--kind", choices=sorted(KINDS), default="examples")
    ap.add_argument("--out")
    ap.add_argument("--list", action="store_true", dest="show_list",
                    help="показать последние пакеты и их состояние")
    args = ap.parse_args()

    import anthropic
    client = anthropic.Anthropic(api_key=api_key())

    if args.show_list:
        for batch in client.messages.batches.list(limit=20).data:
            counts = batch.request_counts
            total = (counts.processing + counts.succeeded + counts.errored
                     + counts.canceled + counts.expired)
            print(f"{batch.id}  {batch.processing_status}")
            print(f"   готово {counts.succeeded}/{total}  ошибок {counts.errored}  "
                  f"отменено {counts.canceled}  истекло {counts.expired}")
            print(f"   создан {batch.created_at}  "
                  f"результаты {'есть' if batch.results_url else 'нет'}")
        return 0

    if not args.batch_id:
        ap.error("нужен id пакета или --list")

    batch = client.messages.batches.retrieve(args.batch_id)
    counts = batch.request_counts
    logger.info("пакет %s: успешно %d, отменено %d, ошибок %d",
                batch.processing_status, counts.succeeded, counts.canceled, counts.errored)

    if batch.processing_status != "ended":
        logger.info("пакет ещё не завершён — забирать нечего")
        return 1

    engine = create_engine(settings.DATABASE_URL_SYNC)
    with engine.connect() as conn:
        word_ids = {r[0] for r in conn.execute(text("SELECT id FROM words"))}

    if args.kind == "examples":
        from app.scripts.fix_examples import _parse as parse
        allowed = {(i, lang) for i in word_ids for lang in SUPPORTED_LANGS}
        default_out = "example_fixes_recovered.jsonl"
    else:
        from app.scripts.retranslate_wordbase import _parse_response as parse
        allowed = word_ids
        default_out = "wordbase_recovered.jsonl"

    out_path = pathlib.Path(args.out or default_out)
    kinds: dict[str, int] = {}
    total = 0

    with out_path.open("w", encoding="utf-8") as out:
        for result in client.messages.batches.results(args.batch_id):
            kind = result.result.type
            kinds[kind] = kinds.get(kind, 0) + 1
            if kind != "succeeded":
                continue
            items, problems = parse(result.result.message, allowed)
            for problem in problems:
                # «модель пропустила» здесь ожидаемо: ослабленная проверка
                # считает пропущенным всё, кроме пришедшего
                if "пропустила" not in problem:
                    logger.warning("%s: %s", result.custom_id, problem)
            for item in items:
                out.write(json.dumps(item, ensure_ascii=False) + "\n")
                total += 1

    logger.info("по типам результата: %s", kinds)
    logger.info("забрано записей: %d → %s", total, out_path)
    if total:
        logger.warning(
            "Предложения могли устареть: база с момента создания пакета менялась. "
            "Прежде чем применять, сверьте, есть ли дефект сейчас — иначе правка "
            "затрёт уже исправленное. На первом восстановлении устаревшими "
            "оказались 1142 предложения из 1335."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
