# -*- coding: utf-8 -*-
"""
ПАТЧНОУТ — КАЖДОМУ НА ЕГО ЯЗЫКЕ. Отправляется боевым ботом после выкатки.

    # просмотр: кому и сколько уйдёт, по языкам; ничего не отправляется
    python -m app.scripts.send_release_notes --key release_notes_2026_10

    # себе: проверить вид на всех шести языках
    python -m app.scripts.send_release_notes --key release_notes_2026_10 --to-admin

    # всем
    python -m app.scripts.send_release_notes --key release_notes_2026_10 --send

ЗАЧЕМ ОТДЕЛЬНЫЙ СКРИПТ. `/broadcast` в админке шлёт ОДИН текст всем, а
владелец хочет «на выбранном ими языке». Текст берётся из локали по языку
интерфейса человека — тот же `get_text`, что и в боте, так что язык и
обращение совпадают с тем, что человек видит каждый день.

ПОВТОР НЕ ДУБЛИРУЕТ. Отправленные помечаются в файле журнала
(`logs/<ключ>.sent`) сразу после каждой доставки. Прерванную рассылку
можно запустить снова той же командой — получившие её второй раз не
получат. Это не «на всякий случай»: при 233 людях и паузе между
сообщениями рассылка идёт минуты, и сеть за это время рвётся.

ВЕЖЛИВО К TELEGRAM. Пауза между сообщениями (по умолчанию 0.1 с — около
десяти в секунду, втрое ниже предела), «подожди N секунд» соблюдается.
Заблокировавшим бота — ни повторов, ни ошибок в итог.

Под сообщением — кнопка «Учить слова»: прочитал — сразу попробовал.
"""
from __future__ import annotations

import argparse
import asyncio
import collections
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
os.environ.setdefault("ENV_FILE", ".env.local")

from aiogram import Bot  # noqa: E402
from aiogram.client.default import DefaultBotProperties  # noqa: E402
from aiogram.enums import ParseMode  # noqa: E402
from aiogram.exceptions import TelegramForbiddenError, TelegramRetryAfter  # noqa: E402
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup  # noqa: E402
from sqlalchemy import select  # noqa: E402

from app.config import settings  # noqa: E402
from app.database.models import User  # noqa: E402
from app.database.session import AsyncSessionLocal  # noqa: E402
from app.locales import DEFAULT_LOCALE, LOCALES, get_text  # noqa: E402

PAUSE = 0.1
RETRY_AFTER_CAP = 60


def _keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
        text=get_text("btn_learn_words", lang),
        # Своя дверь: замер покажет, сколько людей пришло именно с патчноута
        callback_data="learn_now:release",
    )]])


async def _deliver(bot: Bot, chat_id: int, text: str, lang: str) -> str:
    for attempt in (1, 2):
        try:
            await bot.send_message(chat_id, text, reply_markup=_keyboard(lang))
            return "ok"
        except TelegramRetryAfter as exc:
            if attempt == 2:
                return "failed"
            await asyncio.sleep(min(exc.retry_after, RETRY_AFTER_CAP))
        except TelegramForbiddenError:
            return "blocked"
        except Exception as exc:
            text_exc = str(exc).lower()
            if "blocked" in text_exc or "deactivated" in text_exc or "chat not found" in text_exc:
                return "blocked"
            print(f"  не доставлено {chat_id}: {exc}", flush=True)
            return "failed"
    return "failed"


def read_journal(journal: pathlib.Path) -> dict[int, str]:
    """
    Журнал рассылки: номер человека → исход («ok» или «blocked»).

    Строка — «<номер> <исход>». Строка из одного номера — журнал прежнего
    вида, без исхода; такой человек считается получившим.
    """
    out: dict[int, str] = {}
    if not journal.exists():
        return out
    for line in journal.read_text(encoding="utf-8").splitlines():
        parts = line.split()
        if parts and parts[0].lstrip("-").isdigit():
            out[int(parts[0])] = parts[1] if len(parts) > 1 else "ok"
    return out


async def run(args) -> int:
    missing = [lang for lang in LOCALES if args.key not in LOCALES[lang]]
    if missing:
        print(f"СТОП: ключа {args.key} нет в языках {missing}")
        return 1

    journal = pathlib.Path(settings.LOG_DIR or "logs") / f"{args.key}.sent"
    journal.parent.mkdir(parents=True, exist_ok=True)
    sent = set(read_journal(journal))

    async with AsyncSessionLocal() as session:
        people = (await session.execute(
            select(User.id, User.interface_language)
        )).all()

    by_lang = collections.Counter((lang or DEFAULT_LOCALE) for _, lang in people)
    pending = [(uid, lang or DEFAULT_LOCALE) for uid, lang in people if uid not in sent]
    print(f"людей {len(people)}, уже получили {len(sent)}, к отправке {len(pending)}")
    print("по языкам: " + ", ".join(f"{k} {v}" for k, v in sorted(by_lang.items())))

    bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    try:
        if args.to_admin:
            admin = settings.ADMIN_USER
            for lang in LOCALES:
                result = await _deliver(bot, admin, f"[{lang}]\n\n" + get_text(args.key, lang), lang)
                print(f"  {lang}: {result}")
            return 0

        if not args.send:
            print("\nпросмотр: ничего не отправлено. Себе — --to-admin, всем — --send")
            return 0

        counts = collections.Counter()
        with journal.open("a", encoding="utf-8") as log:
            for index, (uid, lang) in enumerate(pending, start=1):
                result = await _deliver(bot, uid, get_text(args.key, lang), lang)
                counts[result] += 1
                # Помечается и заблокировавший: стучаться к нему снова незачем.
                # Исход — рядом с номером: по нему отчёт (`release_report`)
                # отличает «дошло» от «заблокировал бота»
                if result in ("ok", "blocked"):
                    log.write(f"{uid} {result}\n")
                    log.flush()
                if index % 25 == 0:
                    print(f"  {index}/{len(pending)}: {dict(counts)}", flush=True)
                await asyncio.sleep(PAUSE)
        print(f"\nготово: доставлено {counts['ok']}, заблокировали {counts['blocked']}, "
              f"не дошло {counts['failed']} (повторный запуск дошлёт)")
        return 0 if not counts["failed"] else 1
    finally:
        await bot.session.close()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--key", default="release_notes_2026_10",
                    help="ключ текста в локалях (по умолчанию — патчноут 2.0, октябрь 2026)")
    ap.add_argument("--send", action="store_true", help="отправить всем")
    ap.add_argument("--to-admin", action="store_true", help="прислать себе на всех языках")
    return asyncio.run(run(ap.parse_args()))


if __name__ == "__main__":
    sys.exit(main())
