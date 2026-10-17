"""
Строки таблицы рейтинга, зал славы и старые кнопки «Таблица лидеров».

ОДНА СТРОКА НА ЧЕЛОВЕКА (владелец, 17.10): «место · звание · имя · корона ·
серия». Баллов в строке нет («508 477 — не нужно»), медалей тоже: в таблице
текущего месяца 🥇 путала бы — медаль выдают в конце месяца. Имя — первое
слово до 12 знаков, без эмодзи из ника (`standing.clean_name`). Та же строка
стоит в якоре человека.

ОТДЕЛЬНОГО ЭКРАНА ТАБЛИЦЫ БОЛЬШЕ НЕТ (владелец: «таблица лидеров значит
лишнее»): таблица — часть экрана вкладки (`monthly.py`). Кнопки прежней
версии в старых сообщениях ведут на ту же вкладку.
"""

import html
from typing import Optional

from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User
from app.services.standing import clean_name, standings, table_line

router = Router()


async def streaks_of(session: AsyncSession, leaderboard: list) -> dict[int, int]:
    """Текущая серия каждого в таблице — одним запросом."""
    from app.services.streak_service import current_streak

    ids = [entry["user_id"] for entry in leaderboard]
    if not ids:
        return {}
    people = (await session.execute(select(User).where(User.id.in_(ids)))).scalars().all()
    return {person.id: current_streak(person) for person in people}


async def people_of(session: AsyncSession, leaderboard: list) -> tuple[dict, dict]:
    """Серия и положение (звание, корона) каждого в таблице."""
    ids = [entry["user_id"] for entry in leaderboard]
    if not ids:
        return {}, {}
    from app.services.streak_service import current_streak

    people = (await session.execute(select(User).where(User.id.in_(ids)))).scalars().all()
    return ({p.id: current_streak(p) for p in people}, await standings(session, people))


def _rows(leaderboard: list, user_id: int, streaks: Optional[dict],
          ranks: Optional[dict], *, crown: bool = False) -> tuple[list[str], bool, bool]:
    """
    Строки таблицы «1. 🌳 Olga — 455»; есть ли в ней человек и корона.

    `crown` — показывать ли 👑: только на вкладке языка (владелец). Баллы —
    числом после тире: так они читаются как баллы, а не как уровень.
    Серии в таблице нет — она в якоре каждого (`streaks` оставлен ради
    вызывающих).
    """
    lines, me_in, crowned = [], False, False
    for entry in leaderboard:
        # Имя — в HTML-сообщении: «Tom <3» Telegram отверг бы целиком.
        # Экранируем ПОСЛЕ обрезки — иначе она резала бы «&lt;» (аудит 2.1)
        name = html.escape(clean_name(entry["display_name"]))
        is_me = entry["user_id"] == user_id
        if is_me:
            me_in = True
            name = f"<b>{name}</b>"
        st = (ranks or {}).get(entry["user_id"])
        crowned = crowned or bool(crown and st and st.crown_lang)
        score = entry.get("monthly_score", entry.get("lifetime_score"))
        tail = f" — {score}" if score is not None else ""
        lines.append(f"{entry['rank']}. {table_line(name, st, crown=crown)}{tail}")
    return lines, me_in, crowned


# Кнопки прежней версии в старых сообщениях — на экран той же вкладки
@router.callback_query(F.data.in_({"leaderboard_table_monthly", "table_monthly"}))
async def legacy_table_monthly(callback: CallbackQuery, session: AsyncSession):
    from app.bot.handlers.leaderboard.monthly import show_tab

    await show_tab(callback, session, "monthly")


@router.callback_query(F.data.in_({"leaderboard_table_alltime", "table_alltime"}))
async def legacy_table_alltime(callback: CallbackQuery, session: AsyncSession):
    from app.bot.handlers.leaderboard.monthly import show_tab

    await show_tab(callback, session, "alltime")


@router.callback_query(F.data.in_({"leaderboard_table_lang", "table_lang"}))
async def legacy_table_language(callback: CallbackQuery, session: AsyncSession):
    from app.bot.handlers.leaderboard.monthly import show_tab

    await show_tab(callback, session, "lang")
