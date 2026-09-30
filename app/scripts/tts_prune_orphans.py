#!/usr/bin/env python3
"""
Найти в хранилище озвучки клипы, на которые больше никто не ссылается.

Откуда они берутся. Ключ клипа — хеш произносимого текста, а не id слова: это
сделано нарочно, чтобы исправленный перевод получал новый клип, а не тянул за
собой прежнее звучание. Обратная сторона — старый клип остаётся на диске.
Пример: правка турецкой заглавной I изменила 429 строк, синтез создал 607
новых клипов, и ровно столько же прежних осиротело.

Почему это важно не только из-за места. Хранилище переносится на прод
копированием каталога, и сироты поехали бы туда впустую. На 133 тысячах
клипов лишние проценты — это лишние десятки мегабайт по сети и в бэкапе.

Что считается живым определяет tts_synthesize.expected_clips — тот же
перебор, которым клипы и создавались. Считать состав своим кодом нельзя:
первая версия этого скрипта так и сделала, не знала про отбор канонических
слов и про артикль перед немецким существительным, и объявила сиротами 14 924
живых немецких клипа. Пробные озвучки для выбора голоса (kind=preview) живые
всегда: они привязаны не к словам, а к языку.

Удаление безопасно: любой удалённый клип пересоздастся синтезом или при первом
показе карточки. Но по умолчанию скрипт только считает.

    python -m app.scripts.tts_prune_orphans                 # только посчитать
    python -m app.scripts.tts_prune_orphans --lang tr
    python -m app.scripts.tts_prune_orphans --delete
"""
from __future__ import annotations

import argparse
import asyncio
import logging
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
os.environ.setdefault("ENV_FILE", ".env.local")

from app.services.audio_service import KIND_PREVIEW
from app.services.audio_store import DEFAULT_ROOT, text_hash
from app.services.language_service import SUPPORTED_LANGS
from app.scripts.tts_synthesize import expected_clips

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("prune-orphans")


async def live_hashes(lang: str) -> dict[str, set[str]]:
    """
    Хеши живых клипов по виду, из того же перебора, что и синтез.

    Свой запрос к базе здесь был бы ошибкой: см. пояснение в заголовке.
    """
    live: dict[str, set[str]] = {}
    for kind, spoken in await expected_clips(lang):
        live.setdefault(kind, set()).add(text_hash(spoken))
    return live


async def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lang", choices=list(SUPPORTED_LANGS))
    ap.add_argument("--delete", action="store_true")
    ap.add_argument("--root", type=pathlib.Path, default=DEFAULT_ROOT)
    args = ap.parse_args()

    if not args.root.exists():
        logger.error("хранилища нет: %s", args.root)
        return 1

    langs = [args.lang] if args.lang else list(SUPPORTED_LANGS)

    total_files = total_orphans = 0
    total_bytes = orphan_bytes = 0
    to_delete: list[pathlib.Path] = []

    print(f"{'язык':<6} {'клипов':>9} {'живых':>9} {'сирот':>8} {'сироты, МБ':>12}")
    for lang in langs:
        lang_root = args.root / lang
        if not lang_root.exists():
            continue
        live = await live_hashes(lang)

        files = live_count = orphans = 0
        lang_orphan_bytes = 0
        for path in lang_root.rglob("*.mp3"):
            files += 1
            size = path.stat().st_size
            total_bytes += size
            # Вид клипа — предпоследний каталог: <язык>/<голос>/<вид>/<xx>/файл
            kind = path.parent.parent.name
            if kind == KIND_PREVIEW:
                # Пробные озвучки привязаны к языку, а не к словам
                live_count += 1
                continue
            expected = live.get(kind)
            if expected is None:
                # Неизвестный вид — не наш файл, трогать не будем
                live_count += 1
                continue
            if path.stem in expected:
                live_count += 1
            else:
                orphans += 1
                lang_orphan_bytes += size
                to_delete.append(path)

        total_files += files
        total_orphans += orphans
        orphan_bytes += lang_orphan_bytes
        print(f"{lang:<6} {files:>9} {live_count:>9} {orphans:>8} "
              f"{lang_orphan_bytes / 1024 / 1024:>12.1f}")

    print()
    share = (total_orphans / total_files * 100) if total_files else 0
    print(f"всего клипов {total_files}, сирот {total_orphans} ({share:.1f}%), "
          f"{orphan_bytes / 1024 / 1024:.1f} МБ")

    if not to_delete:
        print("удалять нечего")
        return 0

    if not args.delete:
        print()
        print("  (только подсчёт, для удаления --delete)")
        return 0

    removed = failed = 0
    for path in to_delete:
        try:
            path.unlink()
            removed += 1
        except OSError as exc:
            failed += 1
            logger.warning("не удалось удалить %s: %s", path, exc)

    # Опустевшие каталоги: без этого остаются десятки тысяч пустых папок
    empty = 0
    for lang in langs:
        lang_root = args.root / lang
        if not lang_root.exists():
            continue
        for path in sorted(lang_root.rglob("*"), key=lambda p: -len(p.parts)):
            if path.is_dir() and not any(path.iterdir()):
                path.rmdir()
                empty += 1

    # Итог через print, а не logger: logger пишет в stderr, и в конвейере
    # вроде «| grep» сообщение о завершении теряется — скрипт выглядит так,
    # будто ничего не сделал, хотя удалил тысячи файлов
    print()
    print(f"удалено клипов {removed}, не удалось {failed}, "
          f"убрано пустых каталогов {empty}")
    print("Любой удалённый клип пересоздастся синтезом или при первом показе "
          "карточки — потери нет.")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
