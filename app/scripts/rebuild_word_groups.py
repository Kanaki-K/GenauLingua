#!/usr/bin/env python3
"""
Пересобрать word_lang_groups — группы слов по языкам.

Запускать после любого изменения словарной базы (импорт Excel, правка
переводов): группы производны от words и иначе разойдутся с данными.

Usage:
  python -m app.scripts.rebuild_word_groups
  python -m app.scripts.rebuild_word_groups --langs en tr
  python -m app.scripts.rebuild_word_groups --no-remap   # не трогать прогресс

Внутри docker:
  docker compose run --rm app python -m app.scripts.rebuild_word_groups
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import os

from dotenv import load_dotenv

# Тот же файл, что читает app.config — иначе локальный запуск
# подхватит боевые строки подключения из .env.
load_dotenv(os.environ.get("ENV_FILE", ".env"))

from sqlalchemy import create_engine

from app.config import settings
from app.services.language_service import LEARNABLE_LANGS
from app.services.word_groups import build_groups, remap_user_progress_to_canonical


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--langs",
        nargs="*",
        default=list(LEARNABLE_LANGS),
        help=f"Языки для пересборки (по умолчанию все: {' '.join(LEARNABLE_LANGS)})",
    )
    parser.add_argument(
        "--no-remap",
        action="store_true",
        help="Не перепривязывать прогресс пользователей на канонические слова",
    )
    args = parser.parse_args()

    engine = create_engine(settings.DATABASE_URL_SYNC)

    with engine.begin() as conn:
        stats = build_groups(conn, args.langs)

        print("\nГруппы слов по языкам:")
        print(f"  {'язык':6} {'строк':>8} {'слов':>8} {'схлопнуто':>10}")
        for lang, s in stats.items():
            print(f"  {lang:6} {s['rows']:8} {s['groups']:8} {s['collapsed']:10}")

        if args.no_remap:
            print("\n--no-remap: прогресс пользователей не тронут.")
        else:
            moved = remap_user_progress_to_canonical(conn)
            print(f"\nПрогресс перепривязан на канонические слова: {moved} записей.")

    print("\nГотово.")


if __name__ == "__main__":
    main()
