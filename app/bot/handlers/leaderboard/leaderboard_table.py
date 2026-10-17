"""
Таблица лидеров — топ-10 игроков — ЛОКАЛИЗОВАНО

ОДНА СТРОКА НА ЧЕЛОВЕКА (владелец, 17.10): «место · звание · имя · корона ·
серия». Баллов в строке нет («508 477 — не нужно»), медалей тоже: в
таблице текущего месяца 🥇 путала бы — медаль выдают в конце месяца. Знаков у
имени не больше трёх, имя — первое слово до 12 знаков, без эмодзи из ника
(`standing.clean_name`). Та же строка стоит в якоре человека.
"""

import html

from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import MonthlyAward, MonthlySeason, User
from app.services.monthly_leaderboard_service import (
    ALL_LANGS,
    get_monthly_leaderboard,
    get_user_monthly_rank,
    get_current_season,
    get_lifetime_leaderboard,
    get_user_lifetime_rank,
)
from app.services.standing import clean_name, player_line, standings
from app.bot.handlers.leaderboard.utils import (
    RATING_TABS,
    TABLE_TABS,
    edit_screen,
    format_month_name,
    lang_suffix,
    tabs_row,
)
from app.locales import DEFAULT_LOCALE, get_text
from app.services.language_service import pair_from_user

router = Router()

# Сколько прошлых месяцев показывает зал славы
HALL_MONTHS = 3


def get_table_keyboard(lang: str, current_tab: str = "monthly",
                       learning: str = "de") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            tabs_row(lang, current_tab, learning, TABLE_TABS),
            [
                InlineKeyboardButton(
                    text=get_text("btn_back_to_rating", lang),
                    # На ТУ ЖЕ вкладку: из таблицы «за всё время» прежде
                    # возвращало на карточку месяца (аудит 14 октября)
                    callback_data=RATING_TABS.get(current_tab, RATING_TABS["monthly"]),
                )
            ]
        ]
    )


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


def _you_line(user_rank: Optional[dict], lang: str) -> str:
    """«Вы: #N из M» — без баллов, как и строки таблицы."""
    if user_rank and user_rank.get("rank"):
        return get_text("table_you_in_top", lang, rank=user_rank["rank"],
                        total=user_rank.get("total_users", 1))
    return get_text("table_you_not_ranked", lang)


def build_monthly_table(leaderboard: list, user_rank: dict, season, user_id: int, lang: str,
                        streaks: Optional[dict] = None, learning: Optional[str] = None,
                        ranks: Optional[dict] = None) -> str:
    """`learning` — вкладка языка: заголовок с языком; без него — все люди."""
    month_name = format_month_name(season.month, lang)

    text = get_text("table_title_monthly", lang, month=month_name, year=season.year)
    if learning:
        text += lang_suffix(lang, learning)
    text += "\n\n"

    if not leaderboard:
        return text + get_text("table_empty", lang) + "\n"

    lines, _, crown = _rows(leaderboard, user_id, streaks, ranks)
    text += "\n".join(lines) + "\n"
    text += "\n" + "·" * 17 + "\n"
    text += _you_line(user_rank, lang) + "\n"
    if crown:
        # 👑 в таблице месяца — не лидер ЭТОГО месяца, а лучший в языке за
        # прошлый: без строки её приняли бы за первое место
        text += f"<i>{get_text('table_crown_hint', lang)}</i>\n"
    return text


def build_alltime_table(leaderboard: list, user_rank: dict, user_id: int, lang: str,
                        streaks: Optional[dict] = None, ranks: Optional[dict] = None,
                        hall: Optional[list] = None) -> str:
    text = get_text("table_title_alltime", lang) + "\n\n"

    if not leaderboard:
        return text + get_text("table_empty", lang) + "\n"

    lines, _, crown = _rows(leaderboard, user_id, streaks, ranks)
    text += "\n".join(lines) + "\n"
    text += "\n" + "·" * 17 + "\n"
    # Место и «из N» — из `get_user_lifetime_rank`, тем же расчётом, что
    # строки таблицы (прежде место искалось в первой десятке)
    text += _you_line(user_rank, lang) + "\n"
    if crown:
        text += f"<i>{get_text('table_crown_hint', lang)}</i>\n"
    if hall:
        text += "\n" + get_text("hall_title", lang) + "\n"
        text += "\n".join(
            get_text("hall_line", lang, month=format_month_name(month, lang), name=names)
            for month, names in hall
        ) + "\n"
    return text


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


async def _show_monthly_table(callback: CallbackQuery, session: AsyncSession,
                              *, by_language: bool = False) -> None:
    """Месяц: все люди по всем языкам или — вкладкой языка — учащие тот же."""
    await callback.answer()
    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language if user else DEFAULT_LOCALE
    season = await get_current_season(session)

    if not season:
        await callback.message.edit_text(get_text("rating_not_active", lang))
        return

    learning = pair_from_user(user).learning
    scope = learning if by_language else ALL_LANGS
    leaderboard = await get_monthly_leaderboard(session, season_id=season.id, limit=10,
                                                learning_lang=scope)
    user_rank = await get_user_monthly_rank(user.id, session, season_id=season.id,
                                            learning_lang=scope)
    streaks, ranks = await people_of(session, leaderboard)
    text = build_monthly_table(leaderboard, user_rank, season, user.id, lang,
                               streaks=streaks, learning=learning if by_language else None,
                               ranks=ranks)
    await edit_screen(callback, text, get_table_keyboard(
        lang, "lang" if by_language else "monthly", learning))


async def _show_alltime_table(callback: CallbackQuery, session: AsyncSession) -> None:
    """
    Таблица за всё время — СО ВСЕМИ (владелец, 17.10): баллы по всем языкам.

    Сравнение по языку — своя вкладка (месяц среди учащих тот же язык).
    """
    await callback.answer()
    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language if user else DEFAULT_LOCALE

    leaderboard = await get_lifetime_leaderboard(session, limit=10, learning_lang=ALL_LANGS)
    user_rank = await get_user_lifetime_rank(user.id, session, learning_lang=ALL_LANGS)
    streaks, ranks = await people_of(session, leaderboard)
    text = build_alltime_table(leaderboard, user_rank, user.id, lang, streaks=streaks,
                               ranks=ranks, hall=await hall_of_fame(session))
    await edit_screen(callback, text, get_table_keyboard(
        lang, "alltime", pair_from_user(user).learning))


# Две пары обработчиков на один экран: «Таблица лидеров» с карточки и
# переключатель вкладок внутри таблицы. Прежде у каждой пары было по копии
# тела — четыре копии двух экранов, и правка одной расходилась с другой
@router.callback_query(F.data == "leaderboard_table_monthly")
async def show_table_monthly(callback: CallbackQuery, session: AsyncSession):
    await _show_monthly_table(callback, session)


@router.callback_query(F.data == "leaderboard_table_alltime")
async def show_table_alltime(callback: CallbackQuery, session: AsyncSession):
    await _show_alltime_table(callback, session)


@router.callback_query(F.data == "table_monthly")
async def switch_table_to_monthly(callback: CallbackQuery, session: AsyncSession):
    await _show_monthly_table(callback, session)


@router.callback_query(F.data == "table_alltime")
async def switch_table_to_alltime(callback: CallbackQuery, session: AsyncSession):
    await _show_alltime_table(callback, session)


@router.callback_query(F.data.in_({"leaderboard_table_lang", "table_lang"}))
async def show_table_language(callback: CallbackQuery, session: AsyncSession):
    await _show_monthly_table(callback, session, by_language=True)
