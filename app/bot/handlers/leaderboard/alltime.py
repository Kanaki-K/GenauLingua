"""
Мой рейтинг — вкладка «За всё время»
Персональная карточка lifetime — ЛОКАЛИЗОВАНО
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User
from app.services.monthly_leaderboard_service import ALL_LANGS, get_user_lifetime_rank
from app.services.language_service import pair_from_user
from app.bot.handlers.leaderboard.monthly import get_rating_keyboard
from app.bot.handlers.leaderboard.utils import edit_screen
from app.locales import DEFAULT_LOCALE, get_text

router = Router()

def build_alltime_card(user: User, rank_info: dict, lang: str) -> str:
    """
    Карточка «за всё время» по `get_user_lifetime_rank`.

    Прежде место искалось в первой десятке таблицы, а баллы, победы и слова
    брались из колонок `users`: баллы — из `lifetime_score`, где копились
    одни бонусы за места. Владелец с 189 баллами за октябрь видел здесь
    «Позиция: —, Баллы: 0» и совет новичку. Теперь все числа карточки — из
    того же расчёта, что и таблица за всё время, и совпадают с ней.
    """
    text = get_text("rating_title_alltime", lang) + "\n\n"

    rank = rank_info.get("rank")
    score = rank_info.get("lifetime_score", 0)
    total_wins = rank_info.get("total_wins", 0)
    words_learned = rank_info.get("words_learned", 0)

    if rank:
        text += get_text("rating_position_alltime", lang, rank=rank) + "\n"
    else:
        text += get_text("rating_position_none", lang) + "\n"

    text += get_text("rating_points", lang, score=score) + "\n\n"

    # Достижения
    text += get_text("rating_achievements", lang) + "\n"
    text += get_text("rating_wins", lang, count=total_wins) + "\n"
    text += get_text("rating_total_words", lang, count=words_learned) + "\n"

    # Мотивация. «Начни учить слова» — только тому, кто на этом языке ещё не
    # сыграл ни круга (нет месячной строки, места нет). Прежде условие было
    # «побед ноль и lifetime ноль», а lifetime у всех вне призовой десятки
    # был нулём — совет новичку получал и тот, кто сыграл десятки кругов
    if not rank:
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

    # ЗА ВСЁ ВРЕМЯ — СО ВСЕМИ (владелец, 17.10): баллы по всем языкам
    rank_info = await get_user_lifetime_rank(user.id, session, learning_lang=ALL_LANGS)
    text = build_alltime_card(user, rank_info, lang)

    await edit_screen(callback, text, get_rating_keyboard(
        lang, "alltime", pair_from_user(user).learning))