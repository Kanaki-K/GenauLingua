# -*- coding: utf-8 -*-
"""
Озвучить всю базу в файлы: все слова и все примеры, по всем языкам.

Telegram здесь не участвует. Этот шаг делает дорогую и невосполнимую часть —
синтез, — и складывает клипы на диск. Дальше они переносятся копированием
каталога, живут независимо от движка и годятся любому боту.

Загрузка в Telegram и получение file_id — отдельный дешёвый шаг, он в
app/scripts/tts_pregenerate.py.

Объём по замеру: 53 190 канонических слов по пяти языкам, на каждое два клипа
(слово и слово с примером) — 106 380 клипов, около 2,3 ГБ, порядка двух часов
при 16 потоках. Польский добавится после заполнения его колонок.

Порядок обхода: языки по приоритету (немецкий первым), внутри языка от
частотных слов к редким. Прогон можно прерывать в любой момент — уже
синтезированное не переделывается.

    python -m app.scripts.tts_synthesize                    # всё, все языки
    python -m app.scripts.tts_synthesize --lang de           # один язык
    python -m app.scripts.tts_synthesize --lang de --limit 500
    python -m app.scripts.tts_synthesize --stats             # что уже есть
"""
from __future__ import annotations

import argparse
import asyncio
import logging
import os
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
os.environ.setdefault("ENV_FILE", ".env.local")

from sqlalchemy import text

from app.database.session import AsyncSessionLocal
from app.services import audio_store
from app.services.audio_service import KIND_FULL, KIND_WORD, _synthesize, _trimmed
from app.services.language_service import LANGUAGES, SUPPORTED_LANGS
from app.services.tts_text import full_clip_text, word_clip_text
from app.services.tts_voices import default_voice

logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(message)s")
logging.getLogger("sqlalchemy.engine").setLevel(logging.ERROR)
logger = logging.getLogger("synth")

# Немецкий доводится до качества первым, на нём отрабатывается схема
ORDER = ("de", "en", "uk", "ru", "tr", "pl")

# Замерено: при 16 потоках 13,9 клипа в секунду, при 8 — 10,4, при 4 — 4,7.
# Выше 16 движок начинает отказывать, а отказы дороже выигрыша.
WORKERS = 16

# Отдых после отказа: чаще всего это троттлинг у движка, и он проходит сам
BACKOFF = 2.0


async def expected_clips(lang: str) -> list[tuple[str, str]]:
    """
    Все клипы, которые языку положены: пары (вид клипа, произносимый текст).

    Наличие на диске здесь не проверяется — это полный ожидаемый состав.

    Вынесено отдельно, потому что этим списком пользуется не только синтез:
    tts_prune_orphans по нему решает, на какие клипы больше никто не
    ссылается. Считать состав дважды нельзя — разойдётся. Так и вышло в
    первой версии поиска сирот: она не знала ни про отбор канонических слов,
    ни про артикль перед немецким существительным, и объявила сиротами 14 924
    живых немецких клипа.
    """
    cfg = LANGUAGES[lang]
    async with AsyncSessionLocal() as s:
        rows = (await s.execute(text(f"""
            SELECT w.{cfg.word_attr}    AS word,
                   w.{cfg.example_attr} AS example,
                   w.article
            FROM words w
            JOIN word_lang_groups g
              ON g.word_id = w.id AND g.lang = :lang AND g.is_canonical
            WHERE w.{cfg.word_attr} IS NOT NULL
              AND btrim(w.{cfg.word_attr}) <> ''
            ORDER BY w.frequency_rank NULLS LAST, w.id
        """), {"lang": lang})).mappings().all()

    todo: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()

    for row in rows:
        word = (row["word"] or "").strip()
        if cfg.uses_article:
            article = (row["article"] or "").strip()
            if article and article != "-":
                word = f"{article} {word}"

        for kind, spoken in (
            (KIND_WORD, word_clip_text(word, lang)),
            (KIND_FULL, full_clip_text(word, row["example"], lang)),
        ):
            if not spoken:
                continue
            key = (kind, spoken)
            # Одинаковые фразы не дублируются: ключ хранилища от текста
            if key in seen:
                continue
            seen.add(key)
            todo.append(key)

    return todo


async def clips_to_make(lang: str, voice: str, limit: int | None) -> list[tuple[str, str]]:
    """
    Что осталось синтезировать.

    Ключ хранилища — произносимый текст, поэтому проверять наличие можно
    прямо по диску, без обращения к базе file_id.
    """
    todo = [
        (kind, spoken)
        for kind, spoken in await expected_clips(lang)
        if not audio_store.exists(lang, voice, kind, spoken)
    ]
    return todo[:limit] if limit else todo


async def synthesize_language(lang: str, voice: str, limit: int | None,
                              workers: int) -> dict:
    todo = await clips_to_make(lang, voice, limit)
    if not todo:
        print(f"  {lang}: всё уже озвучено")
        return {"done": 0, "failed": 0, "bytes": 0}

    print(f"  {lang}: к синтезу {len(todo)} клипов, голос {voice}")

    queue: asyncio.Queue = asyncio.Queue()
    for item in todo:
        queue.put_nowait(item)

    stats = {"done": 0, "failed": 0, "bytes": 0}
    lock = asyncio.Lock()
    started = time.monotonic()

    async def worker() -> None:
        while True:
            try:
                kind, spoken = queue.get_nowait()
            except asyncio.QueueEmpty:
                return

            data = await _synthesize(spoken, voice)
            if data is None:
                async with lock:
                    stats["failed"] += 1
                # Отказ почти всегда троттлинг: отдыхаем и возвращаем в очередь,
                # чтобы слово не осталось беззвучным из-за минутной заминки
                await asyncio.sleep(BACKOFF)
                queue.put_nowait((kind, spoken))
                continue

            # Тишину вокруг речи снимаем здесь же, а не отдельным прогоном.
            #
            # Прежде обрезка стояла только в живом пути obtain_audio, а этот
            # скрипт писал клип как есть. Первая волна была обрезана отдельным
            # запуском tts_trim_store, и всё выглядело правильно — но каждый
            # следующий пересинтез возвращал тишину, а запустить обрезку я
            # забывал. Замер показал: у немецкого, который с тех пор почти не
            # менялся, хвост 0,17 с, а у пересинтезированных языков 0,38–0,71 с
            # и необрезанное начало у половины клипов.
            #
            # Два пути не должны расходиться, поэтому обрезка теперь часть
            # записи.
            data = _trimmed(data)

            audio_store.write(lang, voice, kind, spoken, data)

            async with lock:
                stats["done"] += 1
                stats["bytes"] += len(data)
                if stats["done"] % 250 == 0:
                    elapsed = time.monotonic() - started
                    rate = stats["done"] / elapsed if elapsed else 0
                    left = (len(todo) - stats["done"]) / rate if rate else 0
                    print(f"    {stats['done']}/{len(todo)}  {rate:.1f} клип/с, "
                          f"осталось ~{left / 60:.0f} мин, "
                          f"{stats['bytes'] / 1024 / 1024:.0f} МБ"
                          + (f", отказов {stats['failed']}" if stats["failed"] else ""))

    await asyncio.gather(*(worker() for _ in range(workers)))

    elapsed = time.monotonic() - started
    print(f"  {lang}: готово {stats['done']} за {elapsed / 60:.1f} мин, "
          f"{stats['bytes'] / 1024 / 1024:.0f} МБ"
          + (f", повторов после отказа {stats['failed']}" if stats["failed"] else ""))
    return stats


def print_stats() -> None:
    data = audio_store.stats()
    print(f"хранилище: {data['clips']} клипов, "
          f"{data['bytes'] / 1024 / 1024 / 1024:.2f} ГБ")
    for lang, entry in sorted(data["by_lang"].items()):
        print(f"  {lang}: {entry['clips']} клипов, "
              f"{entry['bytes'] / 1024 / 1024:.0f} МБ")


async def run(args) -> int:
    if args.stats:
        print_stats()
        return 0

    langs = [args.lang] if args.lang else [c for c in ORDER if c in SUPPORTED_LANGS]

    print(f"каталог хранилища: {audio_store.DEFAULT_ROOT.resolve()}")
    print(f"языки: {' '.join(langs)}, потоков {args.workers}")
    print()

    total = {"done": 0, "failed": 0, "bytes": 0}
    started = time.monotonic()

    for lang in langs:
        voice = args.voice or default_voice(lang)
        result = await synthesize_language(lang, voice, args.limit, args.workers)
        for key in total:
            total[key] += result[key]

    elapsed = time.monotonic() - started
    print()
    print("=== ИТОГ ===")
    print(f"  синтезировано: {total['done']} клипов")
    print(f"  объём:         {total['bytes'] / 1024 / 1024 / 1024:.2f} ГБ")
    print(f"  время:         {elapsed / 60:.1f} мин")
    print()
    print_stats()
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lang", choices=list(SUPPORTED_LANGS),
                    help="только один язык (по умолчанию все по приоритету)")
    ap.add_argument("--limit", type=int, help="ограничить число клипов на язык")
    ap.add_argument("--voice", help="голос (по умолчанию основной для языка)")
    ap.add_argument("--workers", type=int, default=WORKERS)
    ap.add_argument("--stats", action="store_true",
                    help="показать, что уже в хранилище, и выйти")
    return asyncio.run(run(ap.parse_args()))


if __name__ == "__main__":
    sys.exit(main())
