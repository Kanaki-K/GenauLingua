# -*- coding: utf-8 -*-
"""
Предгенерация озвучки: синтезировать, загрузить в Telegram, сохранить file_id.

Зачем, если работает ленивое заполнение. Ленивое работает и без этого:
первый ученик, открывший слово, ждёт лишнюю секунду, все следующие получают
звук мгновенно. Предгенерация убирает эту секунду и, что важнее, страхует от
отказа движка: file_id, уже лежащий в Telegram, живёт вечно и не зависит от
того, работает ли edge-tts сегодня. Endpoint недокументированный, и это
единственная защита от его исчезновения.

ГДЕ БЕРЁТСЯ file_id. Только из ответа на отправку файла — другого способа
Telegram не даёт. Значит предгенерация это отправка 25 тысяч сообщений на один
язык. Поэтому нужен отдельный чат-хранилище:

  --chat-id <id канала>   отправлять в отдельный канал (лучший вариант):
                          создать приватный канал, добавить туда бота
                          администратором, передать его id
  --delete-after          отправлять в чат админа и сразу удалять. file_id
                          после удаления сообщения остаётся рабочим, но чат
                          несколько часов будет дёргаться

Порядок обхода — по приоритету языков и от частотных слов к редким: то, что
люди увидят раньше, озвучивается первым. Прогон можно прерывать: уже
сохранённое не переделывается.

    python -m app.scripts.tts_pregenerate --lang de --limit 200 --delete-after
    python -m app.scripts.tts_pregenerate --lang de --all --chat-id -1001234567890
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

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BufferedInputFile
from sqlalchemy import select, text

from app.config import settings
from app.database.models import Word, WordAudio
from app.database.session import AsyncSessionLocal
from app.services.audio_service import (
    KIND_FULL,
    KIND_WORD,
    audio_filename,
    audio_title,
    get_clip,
    remember,
)
from app.services.language_service import LANGUAGES, SUPPORTED_LANGS
from app.services.tts_voices import default_voice

logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(message)s")
logging.getLogger("sqlalchemy.engine").setLevel(logging.ERROR)
logging.getLogger("aiogram").setLevel(logging.WARNING)
logger = logging.getLogger("pregen")

# Порядок языков: сначала немецкий доводится до качества, схема переносится
ORDER = ("de", "en", "uk", "ru", "tr", "pl")

# Лимит отправки примерно 30 сообщений в секунду на бота, но устойчиво держать
# стоит меньше: при 429 приходится ждать retry_after и терять больше, чем
# экономишь.
SEND_PER_SECOND = 3.0
# Пауза после 429. Telegram сообщает, сколько ждать, но подстраховываемся
FLOOD_PAUSE = 5.0

# Синтез, отправка и запись идут по очереди и по секунде на клип — то есть
# семь часов на немецкий. Они не мешают друг другу, поэтому перекрываются:
# пока один клип уходит в Telegram, следующий уже синтезируется.
# Ограничителем остаётся темп отправки, он общий на всех.
WORKERS = 4


class RateLimiter:
    """Общий на всех темп отправки: лимит Telegram один на бота."""

    def __init__(self, per_second: float):
        self._interval = 1.0 / per_second
        self._lock = asyncio.Lock()
        self._next = 0.0

    async def wait(self) -> None:
        async with self._lock:
            now = time.monotonic()
            delay = max(0.0, self._next - now)
            self._next = max(now, self._next) + self._interval
        if delay:
            await asyncio.sleep(delay)


async def pending_words(lang: str, voice: str, kinds: list[str],
                        limit: int | None) -> list[tuple[int, str]]:
    """
    Что осталось озвучить: пары (id слова, вид клипа) без записи в кэше.

    Порядок по частотности: то, что люди увидят раньше, делается первым.
    """
    cfg = LANGUAGES[lang]
    async with AsyncSessionLocal() as s:
        rows = (await s.execute(text(f"""
            SELECT w.id
            FROM words w
            JOIN word_lang_groups g
              ON g.word_id = w.id AND g.lang = :lang AND g.is_canonical
            WHERE w.{cfg.word_attr} IS NOT NULL
              AND btrim(w.{cfg.word_attr}) <> ''
            ORDER BY w.frequency_rank NULLS LAST, w.id
        """), {"lang": lang})).scalars().all()

        already = set(
            (row.word_id, row.kind)
            for row in (await s.execute(
                select(WordAudio.word_id, WordAudio.kind).where(
                    WordAudio.lang == lang, WordAudio.voice == voice
                )
            )).all()
        )

    todo = [
        (word_id, kind)
        for word_id in rows
        for kind in kinds
        if (word_id, kind) not in already
    ]
    return todo[:limit] if limit else todo


async def upload_one(bot: Bot, chat_id: int, session, word: Word, lang: str,
                     kind: str, voice: str, delete_after: bool,
                     limiter: RateLimiter) -> str:
    """
    Один клип: синтез, отправка, сохранение file_id.

    Возвращает исход строкой — для сводки, а не для ветвления: прогон
    не должен останавливаться из-за одного слова.
    """
    clip = await get_clip(session, word, lang, kind, voice)
    if clip is None:
        return "синтез не удался"
    if clip.file_id:
        return "уже было"

    # Темп держим перед отправкой, а не после: синтез к лимиту не относится
    await limiter.wait()

    try:
        message = await bot.send_audio(
            chat_id,
            BufferedInputFile(clip.data, filename=clip.filename),
            title=clip.title,
            disable_notification=True,
        )
    except Exception as exc:
        detail = str(exc)
        if "retry after" in detail.lower() or "flood" in detail.lower():
            await asyncio.sleep(FLOOD_PAUSE)
            return "лимит отправки"
        logger.warning("отправка не удалась (%s): %s", word.id, detail[:120])
        return "отправка не удалась"

    audio = getattr(message, "audio", None)
    if audio is None or not audio.file_id:
        return "в ответе нет file_id"

    await remember(session, word.id, lang, clip, audio.file_id, audio.duration)
    await session.commit()

    if delete_after:
        # file_id после удаления сообщения остаётся рабочим — проверено
        try:
            await bot.delete_message(chat_id, message.message_id)
        except Exception:
            logger.debug("сообщение-хранилище не удалилось", exc_info=True)

    return "готово"


async def run(args) -> int:
    lang = args.lang
    voice = args.voice or default_voice(lang)
    kinds = [KIND_WORD, KIND_FULL] if not args.only else [args.only]

    chat_id = args.chat_id or settings.ADMIN_USER
    delete_after = args.delete_after or bool(args.chat_id is None)

    if args.chat_id is None and not args.delete_after:
        print("Отправлять некуда без спама в личный чат.")
        print("Нужен либо --chat-id канала-хранилища, либо --delete-after.")
        return 1

    todo = await pending_words(lang, voice, kinds, None if args.all else args.limit)
    if not todo:
        print(f"для {lang} голосом {voice} всё уже озвучено")
        return 0

    print(f"язык {lang}, голос {voice}, виды клипов {kinds}")
    print(f"осталось озвучить: {len(todo)}")
    print(f"отправка в {chat_id}" + (", с удалением" if delete_after else ""))
    print()

    bot = Bot(settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    stats: dict[str, int] = {}
    started = time.monotonic()
    limiter = RateLimiter(SEND_PER_SECOND)
    queue: asyncio.Queue = asyncio.Queue()
    for item in todo:
        queue.put_nowait(item)

    done = 0
    report_lock = asyncio.Lock()

    async def worker() -> None:
        nonlocal done
        # Своя сессия на поток: сессия SQLAlchemy не рассчитана на
        # одновременное использование
        async with AsyncSessionLocal() as session:
            while True:
                try:
                    word_id, kind = queue.get_nowait()
                except asyncio.QueueEmpty:
                    return

                try:
                    word = await session.get(Word, word_id)
                    outcome = (
                        "слова нет" if word is None else
                        await upload_one(bot, chat_id, session, word, lang, kind,
                                         voice, delete_after, limiter)
                    )
                except Exception as exc:
                    # Один сорвавшийся клип не должен останавливать прогон
                    logger.warning("сбой на %s/%s: %s", word_id, kind, exc)
                    await session.rollback()
                    outcome = "сбой"

                async with report_lock:
                    done += 1
                    stats[outcome] = stats.get(outcome, 0) + 1
                    if done % 100 == 0 or done == len(todo):
                        elapsed = time.monotonic() - started
                        rate = done / elapsed if elapsed else 0
                        left = (len(todo) - done) / rate if rate else 0
                        print(f"  {done}/{len(todo)}  {rate:.1f} клип/с, "
                              f"осталось ~{left / 60:.0f} мин   {stats}")

    await asyncio.gather(*(worker() for _ in range(args.workers)))
    await bot.session.close()

    print()
    print("=== ИТОГ ===")
    for name, count in sorted(stats.items(), key=lambda kv: -kv[1]):
        print(f"  {name:<24} {count}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lang", default="de", choices=list(SUPPORTED_LANGS))
    ap.add_argument("--limit", type=int, default=100)
    ap.add_argument("--all", action="store_true", help="весь язык целиком")
    ap.add_argument("--only", choices=[KIND_WORD, KIND_FULL],
                    help="только один вид клипа")
    ap.add_argument("--voice", help="голос (по умолчанию основной для языка)")
    ap.add_argument("--chat-id", type=int,
                    help="id канала-хранилища: создать приватный канал и "
                         "добавить бота администратором")
    ap.add_argument("--delete-after", action="store_true",
                    help="отправлять в чат админа и сразу удалять "
                         "(file_id остаётся рабочим)")
    ap.add_argument("--workers", type=int, default=WORKERS,
                    help=f"сколько клипов готовить одновременно (по умолчанию {WORKERS}); "
                         "темп отправки всё равно ограничен общим лимитом")
    return asyncio.run(run(ap.parse_args()))


if __name__ == "__main__":
    sys.exit(main())
