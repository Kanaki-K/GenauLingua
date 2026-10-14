"""
Мой рейтинг — вкладка «За всё время»
Персональная карточка lifetime — ЛОКАЛИЗОВАНО
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User
from app.services.monthly_leaderboard_service import get_lifetime_leaderboard
from app.bot.handlers.leaderboard.monthly import get_rating_keyboard
from app.locales import DEFAULT_LOCALE, get_text

router = Router()

def build_alltime_card(user: User, leaderboard: list, lang: str) -> str:
    user_id = user.id

    text = get_text("rating_title_alltime", lang) + "\n\n"

    # Позиция
    user_rank_num = None
    if leaderboard:
        for entry in leaderboard:
            if entry["user_id"] == user_id:
                user_rank_num = entry["rank"]
                break

    lifetime_score = user.lifetime_score or 0
    total_wins = user.total_monthly_wins or 0
    words_learned = user.words_learned or 0

    if user_rank_num:
        text += get_text("rating_position_alltime", lang, rank=user_rank_num) + "\n"
    else:
        text += get_text("rating_position_none", lang) + "\n"

    text += get_text("rating_points", lang, score=lifetime_score) + "\n\n"

    # Достижения
    text += get_text("rating_achievements", lang) + "\n"
    text += get_text("rating_wins", lang, count=total_wins) + "\n"
    text += get_text("rating_total_words", lang, count=words_learned) + "\n"

    # Мотивация
    if total_wins == 0 and lifetime_score == 0:
        text += "\n" + get_text("rating_motivation_start", lang) + "\n"
    elif total_wins == 0:
        text += "\n" + get_text("rating_motivation_continue", lang) + "\n"
    elif total_wins >= 3:
        text += "\n" + get_text("rating_motivation_champion", lang) + "\n"

    # ПОЯСНЕНИЯ ПРО БАЛЛЫ ЗДЕСЬ БОЛЬШЕ НЕТ.
    #
    # Стояло такое: «Lifetime баллы — это: • Все баллы за все месяцы •
    # +100 за · +50 за · +25 за». Владелец прочёл и сказал прямо: «тут
    # вообще бред, не понятно за что. Лучше убрать наверное. Потому что
    # много писать за что баллы».
    #
    # Он прав дважды. Во-первых, строка была СЛОМАНА: в ней стояли медали
    # «+100 за 🥇», и знаки снял наш же чистильщик интерфейса — осталось
    # «за» без того, за что. Во-вторых, объяснять правила начисления на
    # экране рейтинга и не нужно: их место там, где балл начисляется.
    #
    # Дословно про это: «лучше как-то показывать в конце игр / уведомление
    # после одобрения репортов, за что получен балл». Так и работает: итог
    # круга печатает «Баллы: +12», а подтверждение жалобы шлёт автору
    # извещение с ценой.
    return text


@router.callback_query(F.data == "rating_alltime")
async def switch_to_alltime(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()
    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language if user else DEFAULT_LOCALE

    leaderboard = await get_lifetime_leaderboard(session, limit=10)
    text = build_alltime_card(user, leaderboard, lang)

    await callback.message.edit_text(text, reply_markup=get_rating_keyboard(lang, "alltime"))