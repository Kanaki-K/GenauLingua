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

from app.database.models import MonthlyAward, MonthlySeason, User
from app.services.standing import clean_name, player_line, standings

router = Router()

# Сколько прошлых месяцев показывает зал славы
HALL_MONTHS = 3


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
          ranks: Optional[dict]) -> tuple[list[str], bool, bool]:
    """Строки таблицы; есть ли в ней человек и есть ли на экране корона."""
    lines, me_in, crown = [], False, False
    for entry in leaderboard:
        # Имя — в HTML-сообщении: «Tom <3» Telegram отверг бы целиком.
        # Экранируем ПОСЛЕ обрезки — иначе она резала бы «&lt;» (аудит 2.1)
        name = html.escape(clean_name(entry["display_name"]))
        is_me = entry["user_id"] == user_id
        if is_me:
            me_in = True
            name = f"<b>{name}</b>"
        st = (ranks or {}).get(entry["user_id"])
        crown = crown or bool(st and st.crown_lang)
        line = player_line(name, st, (streaks or {}).get(entry["user_id"], 0))
        lines.append(f"{entry['rank']}. {line}")
    return lines, me_in, crown


async def hall_of_fame(session: AsyncSession) -> list[tuple[int, str]]:
    """
    Зал славы: победители последних закрытых месяцев — [(месяц, имена)].

    До 17.10 золото раздавалось по языкам, и у старого месяца победителей
    бывает несколько — они идут через запятую.
    """
    seasons = (await session.execute(
        select(MonthlySeason).where(MonthlySeason.winners_finalized.is_(True))
        .order_by(MonthlySeason.year.desc(), MonthlySeason.month.desc())
        .limit(HALL_MONTHS)
    )).scalars().all()
    hall = []
    for season in seasons:
        winners = (await session.execute(
            select(User).join(MonthlyAward, MonthlyAward.user_id == User.id)
            .where(MonthlyAward.season_id == season.id, MonthlyAward.award_type == "gold")
            .order_by(User.id)
        )).scalars().all()
        if winners:
            hall.append((season.month,
                         ", ".join(html.escape(clean_name(w.display_name)) for w in winners)))
    return hall


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
