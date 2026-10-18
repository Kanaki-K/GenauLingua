# -*- coding: utf-8 -*-
"""
РЕПЕТИЦИЯ ЗАКРЫТИЯ МЕСЯЦА — только на КОПИИ базы. Ничего не отправляет.

    python -m app.scripts.season_close_rehearsal            # копия обязана называться *rehearsal*

Закрывает текущий сезон тем же `finalize_season`, что и планировщик 1-го
числа, и печатает: сколько медалей, корон и мест 4–10, кому сколько славы и
какое звание, и тексты итогов — как их получил бы человек (извещение
собирается в подставного бота). Люди — первыми шестью знаками хеша.

Зачем: первое закрытие по правилам 2.2 (медали за общий месяц с 3+
занятиями, корона языка, звания) — 1.11.2026, и раньше эти правила в бою не
срабатывали ни разу. Запуск на живой базе запрещён проверкой имени базы.
"""
from __future__ import annotations

import asyncio
import collections
import hashlib
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from sqlalchemy import select  # noqa: E402

from app.config import settings  # noqa: E402
from app.database.models import MonthlyAward  # noqa: E402
from app.database.session import AsyncSessionLocal  # noqa: E402


def _who(user_id: int) -> str:
    return hashlib.md5(str(user_id).encode()).hexdigest()[:6]


class _Collect:
    def __init__(self):
        self.sent: list[tuple[int, str]] = []

    async def send_message(self, chat_id, text, **_):
        self.sent.append((chat_id, text))


async def main() -> int:
    url = os.environ.get("DATABASE_URL") or settings.DATABASE_URL
    if "rehearsal" not in url.rsplit("/", 1)[-1]:
        print("СТОП: это не копия (имя базы без «rehearsal»)")
        return 2

    from app.services import monthly_leaderboard_service as mls
    from app.services.standing import standings, title_for

    async with AsyncSessionLocal() as session:
        season = await mls.get_current_season(session)
        if season is None:
            print("активного сезона нет")
            return 1
        print(f"сезон {season.month}.{season.year} id={season.id}, закрыт заранее: {season.winners_finalized}")
        await mls.finalize_season(season.id, session)
        awards = (await session.execute(
            select(MonthlyAward).where(MonthlyAward.season_id == season.id)
            .order_by(MonthlyAward.award_type, MonthlyAward.rank)
        )).scalars().all()
        print("наград:", dict(collections.Counter(a.award_type for a in awards)))
        for a in awards:
            print(f"  {a.award_type:6} место {a.rank:2} язык {a.learning_lang} "
                  f"+{a.lifetime_bonus or 0} кто {_who(a.user_id)}")

        from app.database.models import User
        users = (await session.execute(
            select(User).where(User.id.in_({a.user_id for a in awards}))
        )).scalars().all()
        for uid, st in (await standings(session, users)).items():
            title = title_for(st.glory)
            print(f"  слава {_who(uid)}: {st.glory}, звание {title[2] if title else '—'}, "
                  f"медали {st.medals}, корон {st.crowns_total}")

        bot = _Collect()
        mls._daytime_for = lambda user, now: True     # время суток проверено тестами
        sent = await mls.notify_season_awards(bot, session)
        print(f"извещений собрано: {sent}")
        for chat_id, text in bot.sent:
            print(f"--- {_who(chat_id)}\n{text}")
        await session.rollback()
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
