"""
Таблица лидеров — топ-10 игроков — ЛОКАЛИЗОВАНО
"""

import html

from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User
from app.services.monthly_leaderboard_service import (
    ALL_LANGS,
    get_monthly_leaderboard,
    get_user_monthly_rank,
    get_current_season,
    get_lifetime_leaderboard,
    get_user_lifetime_rank,
)
from app.bot.handlers.leaderboard.utils import (
    RATING_TABS,
    TABLE_TABS,
    edit_screen,
    format_month_name,
    lang_suffix,
    tabs_row,
)
from app.locales import DEFAULT_LOCALE, get_text, plural
from app.services.language_service import pair_from_user

router = Router()


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


def _rank_emoji(rank: int) -> str:
    """
    Первые три места — медалью, остальные числом.

    ЗДЕСЬ Я ОШИБАЛСЯ, и стоит сказать, в чём именно. Общей чисткой знаков
    медали были сняты: «числа читаются сразу и сравниваются между собой;
    медаль говорит „ты молодец“, чего таблица и не обещает». Довод верен
    для украшений — и неверен для НАГРАД. Медаль не хвалит, она НАЗЫВАЕТ:
    первое место за месяц, за которое начислено сто баллов к lifetime.
    Сняв её, мы сделали золото неотличимым от седьмого места.

    Владелец: «награды, баджи за викторины (которые были в проде) — важно
    сохранить. Это повышает их ценность».

    Медаль стоит ВМЕСТО номера, а не рядом: «🥇 1.» — это одно и то же
    дважды. Дальше идут числа, и сравнивать их ничто не мешает.
    """
    from app.services.monthly_leaderboard_service import AWARD_MARKS

    by_rank = {1: "gold", 2: "silver", 3: "bronze"}
    mark = AWARD_MARKS.get(by_rank.get(rank, ""), "")
    return mark or f"{rank}."


def _shorten_name(name: str, max_len: int = 15) -> str:
    if len(name) <= max_len:
        return name
    first = name.split()[0]
    if len(first) <= max_len:
        return first
    return first[:max_len - 1] + "…"


# 🔥 у имени — с трёх дней подряд (патч 2.1). Один-два дня — ещё не серия:
# огонёк у каждого второго перестал бы что-то значить
FIRE_FROM_DAYS = 3


def _with_fire(name: str, user_id: int, streaks: Optional[dict]) -> str:
    """Имя и серия: «Оксана 🔥12». Серия живая (`current_streak`), не из колонки."""
    days = (streaks or {}).get(user_id, 0)
    return f"{name} 🔥{days}" if days >= FIRE_FROM_DAYS else name


async def streaks_of(session: AsyncSession, leaderboard: list) -> dict[int, int]:
    """Текущая серия каждого в таблице — одним запросом."""
    from app.services.streak_service import current_streak

    ids = [entry["user_id"] for entry in leaderboard]
    if not ids:
        return {}
    people = (await session.execute(select(User).where(User.id.in_(ids)))).scalars().all()
    return {person.id: current_streak(person) for person in people}


def build_monthly_table(leaderboard: list, user_rank: dict, season, user_id: int, lang: str,
                        streaks: Optional[dict] = None, learning: Optional[str] = None) -> str:
    """`learning` — вкладка языка: заголовок с языком; без него — все люди."""
    month_name = format_month_name(season.month, lang)

    text = get_text("table_title_monthly", lang, month=month_name, year=season.year)
    if learning:
        text += lang_suffix(lang, learning)
    text += "\n\n"

    if not leaderboard:
        text += get_text("table_empty", lang) + "\n"
        return text

    user_in_top = False
    for entry in leaderboard:
        rank = entry["rank"]
        # Имя — в HTML-сообщении: «Tom <3» Telegram отверг бы целиком.
        # Экранируем ПОСЛЕ обрезки — иначе она резала бы «&lt;» (аудит 2.1)
        name = _with_fire(html.escape(_shorten_name(entry["display_name"])), entry["user_id"], streaks)
        score = entry["monthly_score"]
        emoji = _rank_emoji(rank)


        is_me = entry["user_id"] == user_id
        if is_me:
            user_in_top = True
            text += f"{emoji} <b>{name}</b> — {plural(score, 'plural_points', lang)}\n"
        else:
            text += f"{emoji} {name} — {plural(score, 'plural_points', lang)}\n"

    text += "\n" + "·" * 17 + "\n"

    if user_rank:
        rank = user_rank['rank']
        score = user_rank['monthly_score']
        total = user_rank.get('total_users', 1)

        if user_in_top:
            text += get_text("table_you_in_top", lang, rank=rank, total=total) + "\n"
        else:
            # Число со словом считается ДО вызова: test_format_parameters_match
            # разбирает get_text регулярным выражением, и вложенный вызов
            # внутри аргумента рвёт разбор
            shown = plural(score, "plural_points", lang)
            text += get_text("table_you_not_in_top", lang, rank=rank, total=total, score=shown) + "\n"
    else:
        text += get_text("table_you_not_ranked", lang) + "\n"

    return text


def build_alltime_table(leaderboard: list, user_rank: dict, user_id: int, lang: str,
                        streaks: Optional[dict] = None) -> str:
    text = get_text("table_title_alltime", lang) + "\n\n"

    if not leaderboard:
        text += get_text("table_empty", lang) + "\n"
        return text

    user_in_top = False
    for entry in leaderboard:
        rank = entry["rank"]
        name = _with_fire(html.escape(_shorten_name(entry["display_name"])), entry["user_id"], streaks)
        score = entry["lifetime_score"]
        emoji = _rank_emoji(rank)


        is_me = entry["user_id"] == user_id
        if is_me:
            user_in_top = True
            text += f"{emoji} <b>{name}</b> — {plural(score, 'plural_points', lang)}\n"
        else:
            text += f"{emoji} {name} — {plural(score, 'plural_points', lang)}\n"

    text += "\n" + "·" * 17 + "\n"

    # Место, баллы и «из N» — из `get_user_lifetime_rank`, тем же расчётом,
    # что и строки таблицы. Прежде место искалось в первой десятке, баллы
    # брались из `users.lifetime_score` (одни бонусы за места), а «из N»
    # было `len(leaderboard)` — размером таблицы, то есть «из 10» при
    # семидесяти участниках
    user_rank_num = user_rank.get("rank") if user_rank else None
    lifetime = user_rank.get("lifetime_score", 0) if user_rank else 0
    total = user_rank.get("total_users", 0) if user_rank else 0
    shown = plural(lifetime, "plural_points", lang)

    if user_rank_num:
        if user_in_top:
            text += get_text("table_you_in_top", lang, rank=user_rank_num, total=total) + "\n"
        else:
            text += get_text("table_you_not_in_top", lang, rank=user_rank_num, total=total, score=shown) + "\n"
    else:
        if lifetime > 0:
            text += get_text("table_you_outside", lang, score=shown) + "\n"
        else:
            text += get_text("table_you_not_ranked", lang) + "\n"

    return text


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
    text = build_monthly_table(leaderboard, user_rank, season, user.id, lang,
                               streaks=await streaks_of(session, leaderboard),
                               learning=learning if by_language else None)
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
    text = build_alltime_table(leaderboard, user_rank, user.id, lang,
                               streaks=await streaks_of(session, leaderboard))
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
