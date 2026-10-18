"""
Админка → «Рейтинг» и блок рейтинга в карточке человека (17.10).

Владелец: «под это всё нужно улучшить запись инфы по каждому юзеру, а от
этого и админ панель, чтобы я тоже это мог видеть». Всё здесь — тем же
расчётом, что видят люди (`get_monthly_leaderboard`, `standings`), а не
своей копией: иначе админка и экран человека разошлись бы при первой правке.
"""

from aiogram import F, Router
from aiogram.types import CallbackQuery
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.handlers import admin_ui
from app.database.models import NudgeLog, TranslationReport, User
from app.services.monthly_leaderboard_service import (
    ALL_LANGS, get_current_season, get_monthly_leaderboard, get_user_lifetime_rank,
    get_user_monthly_rank,
)
from app.services.standing import (
    ACHIEVEMENTS, CROWN_MIN_PEOPLE, MEDAL_MIN_QUIZZES, TITLES, clean_name, current_crowns,
    next_title, standing_of, standings,
)

router = Router()

TITLE_NAMES = {"title_sprout": "Росток", "title_tree": "Дерево", "title_moon": "Луна",
               "title_planet": "Планета", "title_sun": "Солнце", "title_galaxy": "Галактика"}


def _title(st) -> str:
    t = st.title
    return f"{t[1]} {TITLE_NAMES[t[2]]}" if t else "—"


async def person_rating_block(session: AsyncSession, user: User) -> str:
    """Блок «Рейтинг» карточки /admin_user."""
    from app.config import settings  # noqa: F401  (порядок импорта как у admin)

    st = await standing_of(session, user)
    month = await get_user_monthly_rank(user.id, session, learning_lang=ALL_LANGS)
    lifetime = await get_user_lifetime_rank(user.id, session, learning_lang=ALL_LANGS)
    nxt = next_title(st.glory)
    reports_sent = (await session.execute(
        select(func.count()).select_from(TranslationReport)
        .where(TranslationReport.user_id == user.id))).scalar() or 0
    reports_fixed = (await session.execute(
        select(func.count()).select_from(TranslationReport)
        .where(TranslationReport.user_id == user.id, TranslationReport.status == "fixed"))
    ).scalar() or 0
    m = st.medals
    rows = [
        ("Месяц, место", f"#{month['rank']} из {month['total_users']}" if month else "не в месяце"),
        ("Месяц, баллы", month["monthly_score"] if month else 0),
        ("Месяц, занятий", f"{month['monthly_quizzes'] if month else 0}"
                           f" (медаль с {MEDAL_MIN_QUIZZES})"),
        ("Всё время", f"#{lifetime['rank']} · {lifetime['lifetime_score']}"
                      if lifetime.get("rank") else "—"),
        ("Звание", _title(st)),
        ("Слава", f"{st.glory}" + (f", до {nxt[1]} {nxt[0] - st.glory}" if nxt else "")),
        ("Медали", f"🥇{m['gold']} 🥈{m['silver']} 🥉{m['bronze']}"),
        ("Короны", f"{st.crowns_total}" + (f", носит {st.crown_lang}" if st.crown_lang else "")),
        ("Достижения", f"{len(st.achievements)} из {len(ACHIEVEMENTS)}"),
        ("Жалобы", f"{reports_sent}, принято {reports_fixed}"),
    ]
    if user.overtaken_by_id:
        rows.append(("Обогнал его", str(user.overtaken_by_id)))
    return admin_ui.section("Рейтинг", admin_ui.table(rows))


async def build_rating_screen(session: AsyncSession) -> str:
    """Раздел «Рейтинг»: месяц, тройка, короны, звания, сообщения соревнования."""
    from app.config import settings
    from app.bot.handlers.leaderboard.utils import format_month_name

    season = await get_current_season(session)
    if season is None:
        return admin_ui.screen("Рейтинг", lead="сезона нет")
    board = await get_monthly_leaderboard(session, season_id=season.id, limit=100000,
                                          learning_lang=ALL_LANGS)
    eligible = [e for e in board if e["monthly_quizzes"] >= MEDAL_MIN_QUIZZES]
    top = eligible[:3]

    langs = (await session.execute(
        select(User.learning_lang).distinct())).scalars().all()
    lang_rows = []
    for lang in sorted(l for l in langs if l):
        people = await get_monthly_leaderboard(session, season_id=season.id, limit=100000,
                                               learning_lang=lang)
        contenders = sum(1 for e in people if e["monthly_quizzes"] >= MEDAL_MIN_QUIZZES)
        if people:
            leader = clean_name(people[0]["display_name"])
            lang_rows.append((lang, len(people), contenders,
                              leader if contenders >= CROWN_MIN_PEOPLE else "не разыгр."))

    crowns = await current_crowns(session)
    wearers = []
    for uid, lang in sorted(crowns.items(), key=lambda kv: kv[1]):
        person = await session.get(User, uid)
        if person:
            wearers.append(f"{lang} {admin_ui.DOT} {clean_name(person.display_name)}")

    everyone = (await session.execute(select(User))).scalars().all()
    ranks = await standings(session, everyone)
    by_title = {t[1]: 0 for t in TITLES}
    for st in ranks.values():
        if st.title:
            by_title[st.title[1]] += 1

    sent = dict((await session.execute(
        select(NudgeLog.kind, func.count()).where(
            NudgeLog.kind.in_(("overtaken", "finish")), NudgeLog.outcome == "sent")
        .group_by(NudgeLog.kind))).all())

    medals = ("🥇", "🥈", "🥉")
    blocks = [
        admin_ui.table([
            ("В месяце", len(board)),
            (f"С {MEDAL_MIN_QUIZZES}+ занятиями", len(eligible)),
        ]),
        admin_ui.section("Сейчас на медалях", admin_ui.listing(
            f"{medals[i]} {clean_name(e['display_name'])} {admin_ui.DOT} {e['monthly_score']}"
            for i, e in enumerate(top)), empty="никто ещё не набрал 3 занятия"),
        admin_ui.section("По языкам", admin_ui.columns(
            [("язык", "людей", f"{MEDAL_MIN_QUIZZES}+", "лидер")] + lang_rows)
            if lang_rows else None, empty="никого"),
        admin_ui.section("Короны этого месяца", admin_ui.listing(wearers),
                         empty="никто не носит"),
        admin_ui.section("Звания", admin_ui.table(
            [(mark, n) for mark, n in by_title.items()])),
        admin_ui.section("Сообщения соревнования", admin_ui.table([
            ("Включены", "да" if getattr(settings, "COMPETITION_NUDGES", False) else "нет"),
            ("«Вас обогнали» ушло", sent.get("overtaken", 0)),
            ("Финишная прямая ушла", sent.get("finish", 0)),
        ])),
    ]
    month_name = format_month_name(season.month, "ru")
    return admin_ui.screen(f"Рейтинг · {month_name} {season.year}",
                           lead=f"в месяце {admin_ui.num(len(board))}, "
                                f"за медаль борются {admin_ui.num(len(eligible))}",
                           blocks=blocks)


@router.callback_query(F.data == "admin:rating")
async def admin_rating(callback: CallbackQuery, session: AsyncSession):
    from app.bot.handlers.admin import _guard

    if not await _guard(callback):
        return
    await callback.message.edit_text(await build_rating_screen(session),
                                      reply_markup=admin_ui.kb(back="admin:back"))
