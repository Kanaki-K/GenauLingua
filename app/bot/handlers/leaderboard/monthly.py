"""
Рейтинг — ОДИН ЭКРАН НА ВКЛАДКУ — ЛОКАЛИЗОВАНО

Владелец, 17.10: «есть месяц, есть всё время, есть язык — три категории, где
я хочу себя видеть»; «таблица лидеров значит лишнее». Прежде на каждой вкладке
было два экрана — «Мой рейтинг» и «Таблица лидеров», — и зачем их два, понятно
не было. Теперь каждая вкладка отвечает на три вопроса одним экраном:

  1. кто впереди — первая десятка;
  2. где я — моя строка под чертой, даже вне десятки;
  3. за что борюсь — приз этой вкладки и расстояние до него.

  Месяц      все люди                     🥇🥈🥉 в конце месяца
  Язык       учащие тот же язык           👑 на следующий месяц
  Всё время  все люди, все баллы          звание 🌱 → ☀️, медали, короны

Правила — на экране «Инфо», а не в /help: справка — про бота (владелец).
Старые кнопки «Таблица лидеров» ведут сюда же (`leaderboard_table.py`).
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
    get_current_season,
    get_lifetime_leaderboard,
    get_monthly_leaderboard,
    get_user_lifetime_rank,
    get_waiting_month_score,
)
from app.services.standing import (
    CROWN_MIN_PEOPLE, MEDAL_MIN_QUIZZES, Standing, clean_name, next_title, standing_of,
)
from app.bot.handlers.leaderboard.utils import (
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
TOP = 10
MEDALS = {1: "🥇", 2: "🥈", 3: "🥉"}


def get_rating_keyboard(lang: str, current_tab: str = "monthly",
                        learning: str = "de") -> InlineKeyboardMarkup:
    """Три вкладки и «Инфо». «Таблицы лидеров» больше нет: таблица и есть экран."""
    return InlineKeyboardMarkup(inline_keyboard=[
        tabs_row(lang, current_tab, learning, RATING_TABS),
        [InlineKeyboardButton(text=get_text("btn_rating_info", lang),
                              callback_data=f"{INFO}:{current_tab}")],
    ])


def _days_left(season) -> int:
    """Дней до конца месяца сезона, считая сегодняшний."""
    today = utctoday()
    if (today.year, today.month) != (season.year, season.month):
        return 0
    return calendar.monthrange(season.year, season.month)[1] - today.day + 1


def _name(entry: dict) -> str:
    return html.escape(clean_name(entry["display_name"]))


def _points(n: int, lang: str) -> str:
    return plural(max(0, int(n)), "plural_points", lang)


async def _table(session: AsyncSession, board: list, user_id: int) -> tuple[list[str], bool]:
    """Строки десятки (строка игрока) и есть ли на экране корона."""
    from app.bot.handlers.leaderboard.leaderboard_table import _rows, people_of

    streaks, ranks = await people_of(session, board)
    lines, _, crown = _rows(board, user_id, streaks, ranks)
    return lines, crown


def _you(rank: int, total: int, score: int, lang: str) -> str:
    points = _points(score, lang)
    return get_text("rating_you", lang, rank=rank, total=total, points=points)


def _line(text: str) -> str:
    """Строка с заглавной: «до 🥉 12 баллов» → «До 🥉 12 баллов»."""
    return text[:1].upper() + text[1:] if text else text


def _quiet(text: str) -> str:
    return f"<i>{text}</i>"


# АККУРАТНО (владелец, 17.10: «немного наляписто и неаккуратно в плане эмодзи,
# описания всего»). Под таблицей на каждой вкладке одно и то же:
#   строка «Вы» — место и баллы;
#   строка приза — за что я борюсь и сколько до него;
#   при надобности одна тихая строка курсивом.
# Подписи знаков (👑, звания, 🔥) — только в «Инфо», а не на каждом экране.

async def month_screen(user: User, session: AsyncSession, season, lang: str) -> str:
    """Месяц — все люди; приз — медаль."""
    month_name = format_month_name(season.month, lang)
    text = get_text("rating_screen_title", lang, month=month_name, year=season.year) + "\n\n"

    board = await get_monthly_leaderboard(session, season_id=season.id, limit=100000,
                                          learning_lang=ALL_LANGS)
    if not board:
        return text + get_text("table_empty", lang)
    lines, _ = await _table(session, board[:TOP], user.id)
    text += "\n".join(lines) + "\n\n"

    mine = next((e for e in board if e["user_id"] == user.id), None)
    if mine is None:
        learning = pair_from_user(user).learning
        waiting = await get_waiting_month_score(user.id, session, season.id, learning)
        text += get_text("rating_not_in_ranking", lang) + "\n"
        return text + (get_text("rating_join_by_lesson", lang, score=waiting) if waiting
                       else get_text("rating_start_quiz", lang))

    rank, score = mine["rank"], mine["monthly_score"]
    text += _you(rank, len(board), score, lang) + "\n"
    if mine["monthly_quizzes"] < MEDAL_MIN_QUIZZES:
        # Таблица показывает и тех, у кого одно занятие, а медаль — с трёх
        have = mine["monthly_quizzes"]
        text += get_text("card_medal_need", lang, need=MEDAL_MIN_QUIZZES, have=have) + "\n"
    elif rank == 1:
        if len(board) > 1:
            name, gap = _name(board[1]), _points(score - board[1]["monthly_score"], lang)
            text += f"🥇 · {get_text('rating_lead', lang, name=name, gap=gap)}\n"
        else:
            text += "🥇\n"
    else:
        # Следующая медаль: на место выше в тройке, вне тройки — бронза
        target = rank - 1 if rank in MEDALS else 3
        medal, gap = MEDALS[target], _points(board[target - 1]["monthly_score"] - score, lang)
        prize = get_text("rating_to_medal", lang, medal=medal, gap=gap)
        text += (f"{MEDALS[rank]} · {prize}" if rank in MEDALS else _line(prize)) + "\n"
    days = _days_left(season)
    if days:
        days = plural(days, "plural_days", lang)
        text += _quiet(get_text("rating_results_in", lang, days=days))
    return text.rstrip("\n")


async def language_screen(user: User, session: AsyncSession, season, lang: str) -> str:
    """Язык — учащие тот же язык; приз — корона на следующий месяц."""
    learning = pair_from_user(user).learning
    month_name = format_month_name(season.month, lang)
    text = get_text("rating_screen_title", lang, month=month_name, year=season.year)
    text += lang_suffix(lang, learning) + "\n\n"

    board = await get_monthly_leaderboard(session, season_id=season.id, limit=100000,
                                          learning_lang=learning)
    if not board:
        return text + get_text("table_empty", lang)
    lines, _ = await _table(session, board[:TOP], user.id)
    text += "\n".join(lines) + "\n\n"

    mine = next((e for e in board if e["user_id"] == user.id), None)
    contenders = sum(1 for e in board if e["monthly_quizzes"] >= MEDAL_MIN_QUIZZES)
    if mine is None:
        text += get_text("rating_not_in_ranking", lang) + "\n"
        text += get_text("rating_start_quiz", lang)
        return text
    text += _you(mine["rank"], len(board), mine["monthly_score"], lang) + "\n"
    if contenders < CROWN_MIN_PEOPLE:
        # Корона только в языке, где учатся хотя бы трое с 3+ занятиями
        return text + _quiet(get_text("card_crown_small", lang))
    if mine["rank"] == 1:
        text += get_text("rating_crown_lead", lang)
    else:
        gap = _points(board[0]["monthly_score"] - mine["monthly_score"], lang)
        text += _line(get_text("rating_crown_race", lang, gap=gap))
    return text


def awards_block(standing: Standing, lang: str) -> str:
    """Звание и путь к следующему одной строкой; медали и короны — второй."""
    st = standing
    title = st.title
    following = next_title(st.glory)
    if title and following:
        mark, name = title[1], get_text(title[2], lang)
        # Следующее — одним знаком: «до 🪐 Планета» не склоняется ни в одном языке
        nxt = following[1]
        glory = following[0] - st.glory
        lines = [get_text("rating_title_line", lang, mark=mark, name=name, next=nxt, glory=glory)]
    elif title:
        mark, name = title[1], get_text(title[2], lang)
        lines = [get_text("rating_title_top", lang, mark=mark, name=name)]
    else:
        lines = [get_text("rating_title_first", lang)]
    # Только то, что есть: «🥉 0» читалось как упрёк
    m = st.medals
    shelf = [f"{mark} {m[kind]}" for mark, kind in (("🥇", "gold"), ("🥈", "silver"), ("🥉", "bronze"))
             if m[kind]]
    if st.crowns_total:
        shelf.append(f"👑 {st.crowns_total}")
    if shelf:
        lines.append(" · ".join(shelf))
    return "\n".join(lines)


async def alltime_screen(user: User, session: AsyncSession, lang: str) -> str:
    """Всё время — все люди; приз — звание. Здесь же мои медали и короны."""
    from app.bot.handlers.leaderboard.leaderboard_table import hall_of_fame

    text = get_text("rating_screen_title_alltime", lang) + "\n\n"
    board = await get_lifetime_leaderboard(session, limit=TOP, learning_lang=ALL_LANGS)
    if board:
        lines, _ = await _table(session, board, user.id)
        text += "\n".join(lines) + "\n\n"
    else:
        text += get_text("table_empty", lang) + "\n\n"

    mine = await get_user_lifetime_rank(user.id, session, learning_lang=ALL_LANGS)
    if mine.get("rank"):
        text += _you(mine["rank"], mine.get("total_users", 1), mine.get("lifetime_score", 0),
                     lang) + "\n"
    else:
        text += get_text("table_you_not_ranked", lang) + "\n"
    text += awards_block(await standing_of(session, user), lang)

    hall = await hall_of_fame(session)
    if hall:
        listing = " · ".join(f"{format_month_name(month, lang)} — {names}" for month, names in hall)
        text += "\n\n" + _quiet(get_text("rating_hall", lang, list=listing))
    return text


# ---------------------------------------------------------------------------
# Инфо и показ
# ---------------------------------------------------------------------------

def info_text(lang: str) -> str:
    """Правила одним экраном: три вкладки, знаки у имени, за что баллы."""
    lines = [
        get_text("info_title", lang), "",
        get_text("info_month", lang),
        get_text("info_lang", lang),
        get_text("info_alltime", lang), "",
        get_text("info_signs", lang), "",
        get_text("rating_scoring_title", lang),
        get_text("rating_scoring_answer", lang),
        get_text("rating_scoring_quiz", lang),
        get_text("rating_scoring_word", lang),
        get_text("rating_scoring_streak", lang),
        get_text("rating_scoring_bonus", lang),
        get_text("rating_scoring_report", lang, points=MonthlyStats.POINTS_PER_REPORT),
    ]
    return "\n".join(lines)


async def screen_for(user: User, session: AsyncSession, tab: str) -> tuple[str, InlineKeyboardMarkup]:
    """Текст и клавиатура вкладки. Нет сезона — месяц и язык не показать."""
    lang = user.interface_language or DEFAULT_LOCALE
    learning = pair_from_user(user).learning
    if tab == "alltime":
        text = await alltime_screen(user, session, lang)
    else:
        season = await get_current_season(session)
        if not season:
            return get_text("rating_not_active", lang), get_rating_keyboard(lang, tab, learning)
        text = (await language_screen(user, session, season, lang) if tab == "lang"
                else await month_screen(user, session, season, lang))
    return text, get_rating_keyboard(lang, tab, learning)


async def show_tab(callback: CallbackQuery, session: AsyncSession, tab: str) -> None:
    await callback.answer()
    user = await session.get(User, callback.from_user.id)
    if user is None:
        return
    text, keyboard = await screen_for(user, session, tab)
    # Через edit_screen: повторное нажатие на открытую вкладку шло в журнал
    # ошибкой «message is not modified»
    await edit_screen(callback, text, keyboard)


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
    await show_tab(callback, session, "monthly")


@router.message(Command("leaderboard"))
# Кнопка «🏆 Рейтинг» в главном меню; фильтр — через pressed(): надписи
# берутся из самих локалей, поэтому кнопка работает на всех языках сразу
@router.message(pressed(BTN_RATING))
async def show_leaderboard(message: Message, session: AsyncSession):
    user = await session.get(User, message.from_user.id)
    try:
        await message.delete()
    except Exception:
        pass
    if user is None:
        await message.answer(get_text("rating_not_active", DEFAULT_LOCALE))
        return

    text, keyboard = await screen_for(user, session, "monthly")
    old_anchor_id, _ = await ensure_anchor(message, session, user, emoji="")
    await message.answer(text, reply_markup=keyboard)
    # Прежние сообщения убираются ПОСЛЕДНИМИ, когда новый экран уже на месте
    # (владелец, 15.10: «рейтинг и настройки более плавно работают»)
    if old_anchor_id:
        await delete_messages_fast(message.bot, message.chat.id, old_anchor_id, message.message_id)


@router.callback_query(F.data == "rating_monthly")
async def switch_to_monthly(callback: CallbackQuery, session: AsyncSession):
    await show_tab(callback, session, "monthly")


@router.callback_query(F.data == "rating_lang")
async def switch_to_language(callback: CallbackQuery, session: AsyncSession):
    await show_tab(callback, session, "lang")


@router.callback_query(F.data == "rating_alltime")
async def switch_to_alltime(callback: CallbackQuery, session: AsyncSession):
    await show_tab(callback, session, "alltime")
