"""
Мой рейтинг — вкладки «Месяц» и «Язык», экран «Инфо» — ЛОКАЛИЗОВАНО

ТРИ ВКЛАДКИ (владелец, 17.10): «за месяц со всеми, за всё время со всеми и
язык — с теми, кто учит тоже английский». У каждой своё (REWARDS.md §Г2):
  * Месяц — что собрано сейчас: место, баллы, соперник, сколько осталось;
  * Язык — гонка за короной среди своих;
  * За всё время (`alltime.py`) — что останется навсегда: звание, медали.
Правила — на экране «Инфо», а не в /help: справка — про бота (владелец).
"""

import calendar
import html
import logging

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.clock import utctoday
from app.database.models import MonthlyStats, User
from app.bot.utils import delete_messages_fast, ensure_anchor
from app.services.monthly_leaderboard_service import (
    ALL_LANGS,
    get_monthly_leaderboard,
    get_user_monthly_rank,
    get_current_season,
    get_waiting_month_score,
    month_neighbours,
)
from app.services.standing import (
    CROWN_MIN_PEOPLE, MEDAL_MIN_QUIZZES, clean_name, crown_holders,
)
from app.bot.handlers.leaderboard.utils import (
    OPEN_TABLE,
    RATING_TABS,
    edit_screen,
    format_month_name,
    lang_suffix,
    tabs_row,
)
from app.bot.buttons import BTN_RATING, pressed
from app.locales import DEFAULT_LOCALE, get_text, plural
from app.services.language_service import pair_from_user

logger = logging.getLogger(__name__)

router = Router()

INFO = "rating_info"


def get_rating_keyboard(lang: str, current_tab: str = "monthly",
                        learning: str = "de") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            tabs_row(lang, current_tab, learning, RATING_TABS),
            [
                InlineKeyboardButton(
                    text=get_text("btn_leaderboard_table", lang),
                    # Таблица ТОЙ ЖЕ вкладки, что открыта на карточке. Прежде
                    # кнопка вела в таблицу месяца всегда: владелец с вкладки
                    # «За всё время» жал «Таблица лидеров» и получал «Октябрь
                    # 2026» (жалоба 14 октября)
                    callback_data=OPEN_TABLE.get(current_tab, OPEN_TABLE["monthly"]),
                ),
                InlineKeyboardButton(text=get_text("btn_rating_info", lang),
                                     callback_data=f"{INFO}:{current_tab}"),
            ]
        ]
    )


def _days_left(season) -> int:
    """Дней до конца месяца сезона, считая сегодняшний."""
    last = calendar.monthrange(season.year, season.month)[1]
    today = utctoday()
    if (today.year, today.month) != (season.year, season.month):
        return 0
    return last - today.day + 1


def _name(entry: dict) -> str:
    return html.escape(clean_name(entry["display_name"]))


def build_monthly_card(user: User, user_rank: dict, season, lang: str,
                       waiting_score: int = 0, learning: str | None = None,
                       above: dict | None = None, below: dict | None = None) -> str:
    """
    Месяц — что собрано сейчас: место, баллы, соперник выше и ниже, сколько
    дней осталось, хватает ли занятий для медали.

    `waiting_score` — баллы за жалобы у ряда без занятий (не в рейтинге).
    `learning` — заголовок с языком (зовётся и из вкладки языка, см. ниже).
    """
    month_name = format_month_name(season.month, lang)

    text = get_text("rating_title_monthly", lang, month=month_name, year=season.year)
    if learning:
        text += lang_suffix(lang, learning)
    text += "\n\n"

    if not user_rank:
        text += get_text("rating_not_in_ranking", lang) + "\n"
        if waiting_score > 0:
            text += get_text("rating_join_by_lesson", lang, score=waiting_score) + "\n"
        else:
            text += get_text("rating_start_quiz", lang) + "\n"
        return text

    # Значения — до вызова: вложенный вызов внутри аргументов рвёт разбор
    # в `test_format_parameters_match`
    score = user_rank['monthly_score']
    rank, total = user_rank['rank'], user_rank.get('total_users', 1)
    points = plural(score, "plural_points", lang)
    text += get_text("card_place", lang, rank=rank, total=total, points=points) + "\n"

    # СОПЕРНИК: «обогнать Ольгу» понятнее, чем «#5 из 17»
    if above:
        name = _name(above)
        gap = plural(max(0, above['monthly_score'] - score), "plural_points", lang)
        text += get_text("card_above", lang, name=name, gap=gap) + "\n"
    else:
        text += get_text("card_top", lang) + "\n"
    if below:
        name = _name(below)
        gap = plural(max(0, score - below['monthly_score']), "plural_points", lang)
        text += get_text("card_below", lang, name=name, gap=gap) + "\n"

    quizzes = user_rank.get('monthly_quizzes', 0)
    words = user_rank.get('monthly_words', 0)
    percent = user_rank.get('monthly_avg_percent', 0)
    text += "\n" + get_text("card_month_line", lang, quizzes=quizzes, words=words,
                            percent=percent) + "\n"
    days = _days_left(season)
    if days:
        days = plural(days, "plural_days", lang)
        text += get_text("card_days_left", lang, days=days) + "\n"
    if quizzes < MEDAL_MIN_QUIZZES:
        # Таблица показывает и тех, у кого одно занятие, а медаль — с трёх:
        # без строки первый в таблице мог остаться без медали и не понять почему
        text += "<i>" + get_text("card_medal_need", lang, need=MEDAL_MIN_QUIZZES,
                                 have=quizzes) + "</i>\n"
    return text


async def _monthly_card(user: User, session: AsyncSession, season, lang: str,
                        *, by_language: bool = False) -> str:
    """Месяц со всеми или — вкладкой языка — среди учащих тот же язык."""
    learning = pair_from_user(user).learning
    if by_language:
        return await _language_card(user, session, season, lang, learning)
    user_rank = await get_user_monthly_rank(user.id, session, season_id=season.id,
                                            learning_lang=ALL_LANGS)
    waiting = 0
    above = below = None
    if user_rank:
        above, below = await month_neighbours(session, user.id, season.id, ALL_LANGS)
    else:
        waiting = await get_waiting_month_score(user.id, session, season.id, learning)
    return build_monthly_card(user, user_rank, season, lang, waiting_score=waiting,
                              above=above, below=below)


async def _language_card(user: User, session: AsyncSession, season, lang: str,
                         learning: str) -> str:
    """
    Язык — гонка за короной: у кого она сейчас, моё место среди своих,
    сколько до лидера. Корона разыгрывается, только если в языке
    CROWN_MIN_PEOPLE человек с MEDAL_MIN_QUIZZES занятиями — так и сказано.
    """
    month_name = format_month_name(season.month, lang)
    text = get_text("rating_title_monthly", lang, month=month_name, year=season.year)
    text += lang_suffix(lang, learning) + "\n\n"

    holders = await crown_holders(session, learning)
    if holders:
        people = [await session.get(User, uid) for uid in holders]
        names = ", ".join(html.escape(clean_name(p.display_name)) for p in people if p)
        text += get_text("card_crown_holder", lang, name=names) + "\n\n"
    else:
        text += get_text("card_crown_nobody", lang) + "\n\n"

    board = await get_monthly_leaderboard(session, season_id=season.id, limit=100000,
                                          learning_lang=learning)
    mine = next((e for e in board if e["user_id"] == user.id), None)
    if not mine:
        text += get_text("rating_not_in_ranking", lang) + "\n"
        text += get_text("rating_start_quiz", lang) + "\n"
    else:
        points = plural(mine["monthly_score"], "plural_points", lang)
        rank, total = mine["rank"], len(board)
        text += get_text("card_place", lang, rank=rank, total=total, points=points) + "\n"
        if mine["rank"] == 1:
            text += get_text("card_you_lead", lang) + "\n"
        else:
            gap = plural(max(0, board[0]["monthly_score"] - mine["monthly_score"]),
                         "plural_points", lang)
            text += get_text("card_to_leader", lang, gap=gap) + "\n"

    contenders = sum(1 for e in board if e["monthly_quizzes"] >= MEDAL_MIN_QUIZZES)
    rule = "card_crown_rule" if contenders >= CROWN_MIN_PEOPLE else "card_crown_small"
    text += "\n<i>" + get_text(rule, lang) + "</i>\n"
    return text


def info_text(lang: str) -> str:
    """Правила одним экраном: вкладки, медали, корона, звания, серия, баллы."""
    lines = [
        get_text("info_title", lang), "",
        get_text("info_month", lang), "",
        get_text("info_alltime", lang), "",
        get_text("info_lang", lang), "",
        get_text("info_titles", lang),
        get_text("info_streak", lang), "",
        get_text("rating_scoring_title", lang),
        get_text("rating_scoring_answer", lang),
        get_text("rating_scoring_quiz", lang),
        get_text("rating_scoring_word", lang),
        get_text("rating_scoring_streak", lang),
        get_text("rating_scoring_bonus", lang),
        get_text("rating_scoring_report", lang, points=MonthlyStats.POINTS_PER_REPORT),
    ]
    return "\n".join(lines)


@router.callback_query(F.data.startswith(f"{INFO}:"))
async def show_rating_info(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()
    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language if user else DEFAULT_LOCALE
    tab = callback.data.split(":", 1)[1]
    back = RATING_TABS.get(tab, RATING_TABS["monthly"])
    await edit_screen(callback, info_text(lang), InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=get_text("btn_back", lang), callback_data=back)
    ]]))


@router.callback_query(F.data == "show_my_rating")
async def show_my_rating_callback(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()
    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language if user else DEFAULT_LOCALE
    season = await get_current_season(session)

    if not season:
        await callback.message.edit_text(get_text("rating_not_active", lang))
        return

    text = await _monthly_card(user, session, season, lang)
    keyboard = get_rating_keyboard(lang, "monthly", pair_from_user(user).learning)

    try:
        await edit_screen(callback, text, keyboard)
    except Exception:
        await callback.message.answer(text, reply_markup=keyboard)


@router.message(Command("leaderboard"))
# Кнопка «🏆 Рейтинг» вернулась в главное меню, и фильтр к ней — через
# pressed(): надписи берутся из самих локалей, поэтому кнопка работает на всех
# шести языках сразу. Прежняя попытка это сделать провалилась ровно потому, что
# в фильтр дважды вписали одну и ту же РУССКУЮ строку руками, и на остальных
# языках нажатие не ловилось. Это та же ошибка «список вместо правила».
@router.message(pressed(BTN_RATING))
async def show_leaderboard(message: Message, session: AsyncSession):
    user = await session.get(User, message.from_user.id)
    try:
        await message.delete()
    except Exception:
        pass

    lang = user.interface_language if user else DEFAULT_LOCALE
    season = await get_current_season(session)

    if not season:
        await message.answer(get_text("rating_not_active", lang))
        return

    text = await _monthly_card(user, session, season, lang)

    old_anchor_id, new_anchor_id = await ensure_anchor(message, session, user, emoji="")
    await message.answer(text, reply_markup=get_rating_keyboard(
        lang, "monthly", pair_from_user(user).learning))
    # Прежние сообщения убираются ПОСЛЕДНИМИ, когда новый экран уже на
    # месте: иначе, пока он готовится (статистика — запросы к базе,
    # занятие — загрузка звука), на экране один якорь. Владелец, 15.10:
    # «рейтинг и настройки более плавно работают». Диапазон удаления —
    # от прежнего якоря до нажатия человека, новых сообщений он не задевает
    if old_anchor_id:
        await delete_messages_fast(message.bot, message.chat.id, old_anchor_id, message.message_id)


async def _switch(callback: CallbackQuery, session: AsyncSession, tab: str) -> None:
    await callback.answer()
    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language if user else DEFAULT_LOCALE
    season = await get_current_season(session)

    if not season:
        await callback.message.edit_text(get_text("rating_not_active", lang))
        return

    text = await _monthly_card(user, session, season, lang, by_language=tab == "lang")
    # Через edit_screen, как соседние вкладки: повторное нажатие на уже
    # открытый «Месяц» шло в журнал ошибкой «message is not modified»
    await edit_screen(callback, text, get_rating_keyboard(
        lang, tab, pair_from_user(user).learning))


@router.callback_query(F.data == "rating_monthly")
async def switch_to_monthly(callback: CallbackQuery, session: AsyncSession):
    await _switch(callback, session, "monthly")


@router.callback_query(F.data == "rating_lang")
async def switch_to_language(callback: CallbackQuery, session: AsyncSession):
    await _switch(callback, session, "lang")
