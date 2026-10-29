# -*- coding: utf-8 -*-
"""
ПРИНЯТЬ ЖАЛОБЫ ПАЧКОЙ — та же логика, что кнопка «✓» в админке.

    # просмотр: что будет принято, кому балл
    python -m app.scripts.approve_reports --ids 10 11 12
    # принять, начислить и известить авторов
    python -m app.scripts.approve_reports --ids 10 11 12 --apply

Зачем. При выкатке 2.3 (30.10.2026) 17 жалоб от 19–20.10 исправлены в новом
словаре и звуке; нажимать «✓» семнадцать раз ночью некому. Здесь вызываются
те же `_claim_reports` и `_reward_reporters`: одна оплата человеку за слово,
двойной запуск не платит дважды (статус меняется под замком).

Одно отличие от кнопки — клипы НЕ сбрасываются: звук этих слов уже синтезирован
заново под исправленный текст и лежит на сервере; сброс заставил бы бот
синтезировать его ещё раз при первом показе.
"""
from __future__ import annotations

import argparse
import asyncio
import os
import pathlib
import sys
from types import SimpleNamespace

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
os.environ.setdefault("ENV_FILE", ".env.local")

from aiogram import Bot  # noqa: E402
from aiogram.client.default import DefaultBotProperties  # noqa: E402
from aiogram.enums import ParseMode  # noqa: E402
from sqlalchemy import select  # noqa: E402

from app.bot.handlers.admin import _claim_reports, _reward_reporters, _tell_reporter  # noqa: E402
from app.config import settings  # noqa: E402
from app.database.models import TranslationReport, Word  # noqa: E402
from app.database.session import AsyncSessionLocal  # noqa: E402


async def run(ids: list[int], apply: bool) -> int:
    async with AsyncSessionLocal() as session:
        rows = (await session.execute(
            select(TranslationReport).where(TranslationReport.id.in_(ids))
        )).scalars().all()
        found = {r.id for r in rows}
        missing = sorted(set(ids) - found)
        if missing:
            print(f"СТОП: нет жалоб {missing}")
            return 1
        not_pending = [r.id for r in rows if r.status != "pending"]
        if not_pending:
            print(f"уже решены, пропускаются: {not_pending}")
        groups: dict[int, set[str]] = {}
        for r in rows:
            if r.status == "pending":
                groups.setdefault(r.word_id, set()).add(r.kind or "text")
        for word_id, kinds in sorted(groups.items()):
            word = await session.get(Word, word_id)
            print(f"  {word_id} {word.word_de if word else '?'}: {', '.join(sorted(kinds))}")
        if not apply:
            print("просмотр: ничего не изменено. Принять — с --apply")
            return 0

        bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        holder = SimpleNamespace(bot=bot)
        paid = told = 0
        try:
            for word_id, kinds in sorted(groups.items()):
                claimed = await _claim_reports(session, word_id, tuple(sorted(kinds)), "fixed")
                if not claimed:
                    await session.commit()
                    continue
                rewarded, _ = await _reward_reporters(session, word_id, claimed)
                await session.commit()
                word = await session.get(Word, word_id)
                for user_id, (learning_lang, user_kinds, points) in rewarded.items():
                    paid += 1
                    told += await _tell_reporter(holder, session, user_id, user_kinds,
                                                 word, learning_lang, points)
        finally:
            await bot.session.close()
        print(f"принято слов {len(groups)}, оплат {paid}, извещено {told}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ids", type=int, nargs="+", required=True)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    return asyncio.run(run(args.ids, args.apply))


if __name__ == "__main__":
    sys.exit(main())
