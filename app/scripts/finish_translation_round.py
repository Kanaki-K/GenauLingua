#!/usr/bin/env python3
"""
Довести прогон переводов до конца: от предложений до проверенной базы с озвучкой.

Зачем скриптом. После прогона переводов остаётся одиннадцать шагов, и порядок
между ними важен: озвучка зависит от текста, группы — от переводов, дефекты
примеров приходят из двух источников, а записи, которые правка примеров
отклоняет, надо править переводом. В этой сессии я один шаг уже забывал — 547
помеченных слов существовали только в строке журнала, пока я не пошёл их
считать. Последовательность, записанная в DEPLOY.md, здесь исполняется, чтобы
документ и дело не разошлись.

Шаги с расходом денег помечены и без --paid не выполняются: прогон примеров и
пересборка отклонённых записей обращаются к модели.

Прогресс пользователей сверяется до и после. Если суммы разошлись — прогон
останавливается, потому что дальше пойдёт порча, а не правка.

    python -m app.scripts.finish_translation_round --files wordbase_c1.jsonl
    python -m app.scripts.finish_translation_round --files a.jsonl b.jsonl --paid
    python -m app.scripts.finish_translation_round --files a.jsonl --skip-audio
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import pathlib
import subprocess
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
os.environ.setdefault("ENV_FILE", ".env.local")

from sqlalchemy import create_engine, text

from app.config import settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("finish-round")

PYTHON = sys.executable


def run(args: list[str], label: str) -> subprocess.CompletedProcess:
    logger.info("── %s", label)
    started = time.monotonic()
    result = subprocess.run(
        [PYTHON, "-u", "-m", *args],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    minutes = (time.monotonic() - started) / 60
    tail = (result.stdout or "").strip().splitlines()[-6:]
    for line in tail:
        print(f"      {line}")
    if result.returncode != 0:
        logger.error("%s: код возврата %d", label, result.returncode)
        for line in (result.stderr or "").strip().splitlines()[-12:]:
            print(f"      {line}")
    logger.info("   %s: %.1f мин", label, minutes)
    return result


def progress(engine) -> tuple[int, int]:
    with engine.connect() as conn:
        shown = conn.execute(text("SELECT SUM(times_shown) FROM user_words")).scalar()
        correct = conn.execute(text("SELECT SUM(times_correct) FROM user_words")).scalar()
    return int(shown or 0), int(correct or 0)


def rejected_ids(paths: list[pathlib.Path]) -> list[int]:
    """
    Записи, которые правка примеров отклонила.

    Отклоняет она их правильно: испорчен там перевод, а не пример — слово не в
    словарной форме, не на том языке или выдуманное. Их надо пересобрать
    переводом.
    """
    found: set[int] = set()
    for path in paths:
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                found.add(json.loads(line)["id"])
    return sorted(found)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--files", nargs="+", required=True,
                    help="файлы предложений от retranslate_wordbase propose")
    ap.add_argument("--paid", action="store_true",
                    help="выполнять шаги с обращением к модели")
    ap.add_argument("--skip-audio", action="store_true",
                    help="не пересинтезировать и не убирать сирот")
    ap.add_argument("--chunk", type=int, default=12,
                    help="порция для пересборки отклонённых записей")
    args = ap.parse_args()

    missing = [f for f in args.files if not pathlib.Path(f).exists()]
    if missing:
        logger.error("нет файлов: %s", missing)
        return 1

    engine = create_engine(settings.DATABASE_URL_SYNC)
    before = progress(engine)
    logger.info("прогресс до прогона: показов %d, правильных %d", *before)

    # 1. Переводы
    for path in args.files:
        run(["app.scripts.retranslate_wordbase", "apply", "--file", path],
            f"переводы из {path}")

    # 2. Турецкая İ — прогон ставит латинскую I систематически
    run(["app.scripts.fix_turkish_i", "--apply"], "турецкая İ")

    # 3-4. Дефекты примеров из ДВУХ источников: пересечение мало, и один
    #      источник пропускает примерно половину
    run(["app.scripts.example_quality", "--out", "round_defects.jsonl"],
        "отсев дефектных примеров")

    model_flags = [
        str(pathlib.Path(f).with_name(pathlib.Path(f).stem + "_bad_examples.jsonl"))
        for f in args.files
    ]
    merge = ["app.scripts.merge_defects", "--detector", "round_defects.jsonl",
             "--out", "round_merged.jsonl"]
    existing = [m for m in model_flags if pathlib.Path(m).exists()]
    if existing:
        merge += ["--model", *existing]
    else:
        logger.warning("пометок модели не найдено (%s) — сведение только по отсеву",
                       model_flags)
    run(merge, "сведение двух источников")

    if args.paid:
        # 5-6. Переписать примеры
        run(["app.scripts.fix_examples", "propose", "--in", "round_merged.jsonl",
             "--out", "round_example_fixes.jsonl"], "правка примеров (расход)")
        run(["app.scripts.fix_examples", "apply", "--file",
             "round_example_fixes.jsonl"], "применение примеров")

        # 7. Отклонённые — это испорченные переводы, а не примеры
        ids = rejected_ids([pathlib.Path("round_example_fixes_rejected.jsonl")])
        if ids:
            logger.info("отклонено правкой примеров: %d записей — пересобираю переводом",
                        len(ids))
            run(["app.scripts.retranslate_wordbase", "propose",
                 "--ids", *map(str, ids), "--chunk", str(args.chunk),
                 "--out", "round_nonlemma.jsonl"], "пересборка отклонённых (расход)")
            if pathlib.Path("round_nonlemma.jsonl").exists():
                run(["app.scripts.retranslate_wordbase", "apply",
                     "--file", "round_nonlemma.jsonl"], "применение пересобранных")
    else:
        logger.warning("шаги с расходом пропущены — для них нужен --paid")

    # 8. Группы: переводы входят в ключ схлопывания
    run(["app.scripts.rebuild_word_groups"], "пересборка групп")

    after = progress(engine)
    logger.info("прогресс после: показов %d, правильных %d", *after)
    if after != before:
        logger.error(
            "ПРОГРЕСС РАЗОШЁЛСЯ: было %s, стало %s. Прогон остановлен: дальше "
            "пойдёт порча, а не правка. Разбираться до продолжения.", before, after,
        )
        return 2
    logger.info("прогресс сохранён до единицы")

    # 9-10. Озвучка: текст изменился, старые клипы осиротели
    if not args.skip_audio:
        run(["app.scripts.tts_synthesize"], "синтез недостающих клипов")
        run(["app.scripts.tts_prune_orphans", "--delete"], "уборка сирот")

    # 11. Проверки
    run(["app.scripts.example_quality"], "остаточные дефекты примеров")
    run(["app.scripts.verify_all_flows"], "сквозные сценарии")

    logger.info("прогон завершён")
    logger.warning(
        "Остаётся глазами: выборочная проверка базы\n"
        "    python -m app.scripts.wordbase_sample_review --rounds 10 --size 100"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
