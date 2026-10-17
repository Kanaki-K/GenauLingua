"""
Мой рейтинг — вкладки «Месяц» и «Язык»
Персональная карточка за текущий месяц — ЛОКАЛИЗОВАНО

ТРИ ВКЛАДКИ (владелец, 17.10): «за месяц со всеми, за всё время со всеми и
язык — с теми, кто учит тоже английский». «Месяц» — все люди, баллы по всем
языкам складываются; вкладка языка — тот же месяц среди учащих тот же язык.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

import logging

logger = logging.getLogger(__name__)

from app.database.models import MonthlyStats, User
from app.bot.utils import delete_messages_fast, ensure_anchor
from app.services.monthly_leaderboard_service import (
    ALL_LANGS,
    get_user_monthly_rank,
    get_current_season,
    get_waiting_month_score,
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
from app.locales import DEFAULT_LOCALE, get_text
from app.services.language_service import pair_from_user

router = Router()

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
                )
            ]
        ]
    )


def build_monthly_card(user: User, user_rank: dict, season, lang: str,
                       waiting_score: int = 0, learning: str | None = None) -> str:
    """
    `waiting_score` — баллы за жалобы у ряда без занятий (не в рейтинге).
    `learning` — вкладка языка: заголовок с названием языка; без него — месяц
    со всеми.
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

    rank = user_rank['rank']
    score = user_rank['monthly_score']
    total_users = user_rank.get('total_users', 1)
    quizzes = user_rank.get('monthly_quizzes', 0)
    words = user_rank.get('monthly_words', 0)
    streak = user_rank.get('monthly_streak', 0)
    avg_pct = user_rank.get('monthly_avg_percent', 0)

    text += get_text("rating_position", lang, rank=rank, total=total_users) + "\n"
    text += get_text("rating_points", lang, score=score) + "\n\n"

    text += get_text(
        "rating_your_month", lang,
        month=format_month_name(season.month, lang, inline=True),
    ) + "\n"
    text += get_text("rating_quizzes", lang, count=quizzes) + "\n"
    text += get_text("rating_words_learned", lang, count=words) + "\n"
    text += get_text("rating_streak", lang, days=streak) + "\n"
    text += get_text("rating_avg_result", lang, percent=avg_pct) + "\n"

    text += "\n"
    text += get_text("rating_scoring_title", lang) + "\n"
    # Строка про ответы стоит ПЕРВОЙ: это единственное начисление, которое
    # происходит на каждом вопросе, и единственное, которое зависит от того,
    # насколько человек себя напряг
    text += get_text("rating_scoring_answer", lang) + "\n"
    text += get_text("rating_scoring_quiz", lang) + "\n"
    text += get_text("rating_scoring_word", lang) + "\n"
    text += get_text("rating_scoring_streak", lang) + "\n"
    text += get_text("rating_scoring_bonus", lang) + "\n"
    text += get_text(
        "rating_scoring_report", lang,
        points=MonthlyStats.POINTS_PER_REPORT,
    ) + "\n"

    return text


async def _monthly_card(user: User, session: AsyncSession, season, lang: str,
                        *, by_language: bool = False) -> str:
    """Месяц: со всеми (по умолчанию) или среди учащих тот же язык."""
    learning = pair_from_user(user).learning
    user_rank = await get_user_monthly_rank(
        user.id, session, season_id=season.id,
        learning_lang=learning if by_language else ALL_LANGS)
    waiting = 0
    if not user_rank:
        waiting = await get_waiting_month_score(user.id, session, season.id, learning)
    return build_monthly_card(user, user_rank, season, lang, waiting_score=waiting,
                              learning=learning if by_language else None)


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
