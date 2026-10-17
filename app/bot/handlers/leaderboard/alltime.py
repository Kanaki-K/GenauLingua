"""
Мой рейтинг — вкладка «За всё время»
Персональная карточка lifetime — ЛОКАЛИЗОВАНО

ЧТО ОСТАНЕТСЯ НАВСЕГДА (владелец, 17.10: «за месяц он собрал, а за всё время
видит все свои награды»): строка игрока, как в таблице и якоре; место и баллы
за всё время; звание с названием и путь к следующему; медали и сколько раз
была корона («3 раза корону имел, но если хочешь ещё — борись»).
"""

import html

from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User
from app.services.monthly_leaderboard_service import ALL_LANGS, get_user_lifetime_rank
from app.services.language_service import pair_from_user
from app.services.standing import (
    TITLES, Standing, clean_name, next_title, player_line, standing_of,
)
from app.bot.handlers.leaderboard.monthly import get_rating_keyboard
from app.bot.handlers.leaderboard.utils import edit_screen
from app.locales import DEFAULT_LOCALE, get_text, plural

router = Router()


def build_alltime_card(user, rank_info: dict, lang: str,
                       standing: Standing | None = None, streak: int = 0) -> str:
    """
    Карточка «за всё время» по `get_user_lifetime_rank` и `standing`.

    Все числа — из того же расчёта, что таблица за всё время, и совпадают с
    ней. Звание объясняется ЗДЕСЬ, с названием: в таблице знак стоит без
    подписи (владелец: «можем даже не пояснять»).
    """
    text = get_text("rating_title_alltime", lang) + "\n\n"

    if user is not None:
        text += player_line(html.escape(clean_name(user.display_name)), standing, streak) + "\n"

    rank = rank_info.get("rank")
    score = rank_info.get("lifetime_score", 0)
    if rank:
        total = rank_info.get("total_users", 1)
        points = plural(score, "plural_points", lang)
        text += get_text("card_place", lang, rank=rank, total=total, points=points) + "\n"
    else:
        text += get_text("rating_position_none", lang) + "\n"
        text += get_text("rating_motivation_start", lang) + "\n"

    st = standing or Standing(user_id=getattr(user, "id", 0))
    text += "\n"
    title = st.title
    if title:
        mark, name = title[1], get_text(title[2], lang)
        text += get_text("card_title", lang, mark=mark, name=name) + "\n"
    else:
        mark = TITLES[0][1]
        text += get_text("card_title_none", lang, mark=mark) + "\n"
    following = next_title(st.glory)
    if following:
        mark, name, glory = following[1], get_text(following[2], lang), following[0] - st.glory
        text += get_text("card_title_next", lang, mark=mark, name=name, glory=glory) + "\n"
    elif title:
        text += get_text("card_title_secret", lang) + "\n"

    medals = st.medals
    if any(medals.values()):
        shown = f"🥇 {medals['gold']} · 🥈 {medals['silver']} · 🥉 {medals['bronze']}"
        text += get_text("card_medals", lang, medals=shown) + "\n"
    if st.crowns_total:
        text += get_text("card_crowns", lang, count=st.crowns_total) + "\n"

    # ПОЯСНЕНИЯ ПРО БАЛЛЫ ЗДЕСЬ НЕТ — они на экране «Инфо». Владелец о прежнем
    # тексте: «тут вообще бред, не понятно за что. Лучше убрать наверное»
    return text


@router.callback_query(F.data == "rating_alltime")
async def switch_to_alltime(callback: CallbackQuery, session: AsyncSession):
    from app.services.streak_service import current_streak

    await callback.answer()
    user = await session.get(User, callback.from_user.id)
    lang = user.interface_language if user else DEFAULT_LOCALE

    # ЗА ВСЁ ВРЕМЯ — СО ВСЕМИ (владелец, 17.10): баллы по всем языкам
    rank_info = await get_user_lifetime_rank(user.id, session, learning_lang=ALL_LANGS)
    text = build_alltime_card(user, rank_info, lang, await standing_of(session, user),
                              current_streak(user))

    await edit_screen(callback, text, get_rating_keyboard(
        lang, "alltime", pair_from_user(user).learning))
