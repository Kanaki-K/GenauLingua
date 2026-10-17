"""
Звания, корона, строка игрока, три карточки, «Инфо», итоги месяца, «Вас
обогнали» — замысел владельца 17.10 (REWARDS.md §0, презентация «Сетка
развития»).

Что держится:
  * слава копится от медалей и достижений, корона славы не даёт;
  * звание — шесть ступеней 🌱 🌳 🌙 🪐 ☀️ 🌌, верхняя тайная;
  * строка игрока одна на таблицу и якорь, имя без эмодзи из ника;
  * у каждой вкладки «Мой рейтинг» своё содержание;
  * итоги месяца — одно сообщение, и оно занимает дневной бюджет;
  * «Вас обогнали» выключено переключателем и включается только им;
  * все новые строки есть на 10 языках.
"""
import re
from datetime import datetime, time, timedelta

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.core.clock import utcnow, utctoday
from app.database.enums import CEFRLevel
from app.database.models import MonthlyAward, MonthlyStats, NudgeLog, QuizSession, User
from app.locales import LOCALES, get_text
from app.services import nudge_plan
from app.services.monthly_leaderboard_service import (
    create_new_season, finalize_season, get_or_create_current_season,
)
from app.services.standing import (
    ACHIEVEMENTS, TITLES, Standing, clean_name, compact_number, next_title,
    player_line, standing_of, title_for,
)
from tests.scenario import make_bot, make_dispatcher, press, reset_state

pytestmark = pytest.mark.asyncio


def _free_ids(n, start=7100):
    """Номера вне контрольной группы: им сообщения приходят."""
    out, uid = [], start
    while len(out) < n:
        if not nudge_plan.in_holdout(uid):
            out.append(uid)
        uid += 1
    return out


async def _person(session, uid, name="Anna", lang="de", **extra):
    user = User(id=uid, first_name=name, interface_language="ru", learning_lang=lang,
                native_lang="ru", level=CEFRLevel.A1, **extra)
    session.add(user)
    await session.commit()
    return user


async def _month(session, season, rows):
    """rows: [(id, язык, баллы, занятий)]"""
    for uid, lang, score, lessons in rows:
        session.add(MonthlyStats(user_id=uid, season_id=season.id, learning_lang=lang,
                                 monthly_score=score, monthly_quizzes=lessons))
    await session.commit()


# ---------------------------------------------------------------------------
# Правила
# ---------------------------------------------------------------------------

def test_title_ladder_from_earth_to_galaxy():
    assert [t[1] for t in TITLES] == ["🌱", "🌳", "🌙", "🪐", "☀️", "🌌"]
    assert title_for(0) is None
    assert title_for(1)[1] == "🌱" and title_for(4)[1] == "🌱"
    assert title_for(12)[1] == "🌙" and title_for(55)[1] == "🌌"
    # Верхняя ступень тайная: «до следующего» её не называет
    assert next_title(40) is None and next_title(30)[1] == "☀️"


def test_name_has_no_fake_crown_or_fire_and_is_short():
    assert clean_name("👑 Оля Петрова") == "Оля"
    assert clean_name("Max🔥99") == "Max99"
    assert clean_name("Maximilian-Alexander") == "Maximilian-…"
    assert clean_name("🔥🔥") == "…"


def test_long_streak_does_not_stretch_the_line():
    assert compact_number(27) == "27" and compact_number(1234) == "1.2k"
    assert compact_number(1000) == "1k" and compact_number(15000) == "15k"
    st = Standing(user_id=1, glory=12, crown_lang="de")
    assert player_line("Kostia", st, 27) == "🌙 Kostia 👑 🔥27"
    assert player_line("Kostia", None, 2) == "Kostia"


async def test_glory_from_medals_and_achievements_but_not_crowns(session):
    season = await create_new_season(2026, 3, session)
    user = await _person(session, 1, best_streak_days=120)
    session.add_all([
        MonthlyAward(user_id=1, season_id=season.id, learning_lang="*", rank=1,
                     award_type="gold", lifetime_bonus=100),
        MonthlyAward(user_id=1, season_id=season.id, learning_lang="de", rank=1,
                     award_type="crown", lifetime_bonus=0),
    ])
    await session.commit()
    st = await standing_of(session, user)
    # золото 5 + серия 30 (1) + серия 100 (3); корона — 0
    assert st.glory == 9 and st.title[1] == "🌳"
    assert st.crowns_total == 1 and st.medals["gold"] == 1
    assert {"streak_7", "streak_30", "streak_100"} <= set(st.achievements)


# ---------------------------------------------------------------------------
# Экраны
# ---------------------------------------------------------------------------

async def test_anchor_second_line_is_the_table_line(session):
    from app.bot.utils import anchor_text

    user = await _person(session, 1, name="Kostia")
    st = Standing(user_id=1, glory=12)
    text = anchor_text(user, st)
    first, second = text.split("\n")
    assert "A1" in first and "🔥" not in first
    assert second == "🌙 Kostia"


async def test_three_cards_and_info(session):
    season = await get_or_create_current_season(session)
    ids = (11, 12, 13)
    for uid, name in zip(ids, ("Anna", "Boris", "Clara")):
        await _person(session, uid, name=name)
    await _month(session, season, [(11, "de", 300, 5), (12, "de", 200, 2), (13, "de", 100, 4)])
    bot, recorder = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)

    await dp.feed_update(bot, press(12, "rating_monthly"))
    month = recorder.last_text()
    assert get_text("card_above", "ru", name="Anna", gap="100 баллов") in month, month
    assert get_text("card_below", "ru", name="Clara", gap="100 баллов") in month
    # У Бориса два занятия — медали не будет, и это сказано
    assert get_text("card_medal_need", "ru", need=3, have=2) in month
    assert recorder.button_texts()[0] == "✓ Месяц"

    await dp.feed_update(bot, press(12, "rating_lang"))
    lang_card = recorder.last_text()
    assert get_text("card_crown_nobody", "ru") in lang_card
    assert get_text("card_to_leader", "ru", gap="100 баллов") in lang_card
    # В языке трое, но с 3+ занятиями только двое: корона не разыгрывается
    assert get_text("card_crown_small", "ru") in lang_card

    await dp.feed_update(bot, press(12, "rating_alltime"))
    alltime = recorder.last_text()
    assert get_text("card_title_none", "ru", mark="🌱") in alltime
    assert "rating_info:alltime" in recorder.buttons()

    await dp.feed_update(bot, press(12, "rating_info:alltime"))
    assert get_text("info_title", "ru") in recorder.last_text()
    assert recorder.buttons() == ["rating_alltime"]


async def test_crown_is_worn_in_the_table_with_a_hint(session):
    from app.bot.handlers.leaderboard.leaderboard_table import build_monthly_table

    season = await get_or_create_current_season(session)
    rows = [{"user_id": 1, "rank": 1, "display_name": "Olga"},
            {"user_id": 2, "rank": 2, "display_name": "Ivan"}]
    ranks = {1: Standing(user_id=1, crown_lang="de"), 2: Standing(user_id=2)}
    text = build_monthly_table(rows, {"rank": 2, "total_users": 2}, season, 2, "ru",
                               ranks=ranks)
    assert "1. Olga 👑\n" in text and "2. <b>Ivan</b>\n" in text
    assert get_text("table_crown_hint", "ru") in text
    plain = build_monthly_table(rows, None, season, 2, "ru", ranks={})
    assert get_text("table_crown_hint", "ru") not in plain


# ---------------------------------------------------------------------------
# Итоги месяца — одно сообщение
# ---------------------------------------------------------------------------

class FakeBot:
    def __init__(self):
        self.sent = []

    async def send_message(self, chat_id, text, **kwargs):
        self.sent.append((chat_id, text, kwargs.get("reply_markup")))


async def test_month_results_are_one_message_with_crown_and_title(session):
    from app.services.monthly_leaderboard_service import notify_season_awards

    season = await create_new_season(2026, 3, session)
    for uid in (1, 2, 3):
        await _person(session, uid, name=f"U{uid}")
    await _month(session, season, [(1, "de", 300, 3), (2, "de", 200, 3), (3, "de", 100, 3)])
    await finalize_season(season.id, session)

    bot = FakeBot()
    assert await notify_season_awards(bot, session) == 3
    first = [text for uid, text, _ in bot.sent if uid == 1]
    assert len(first) == 1, "медаль и корона — одним сообщением"
    text = first[0]
    assert get_text("award_month_header", "ru") in text
    assert "👑" in text and "🥇" in text
    assert get_text("award_new_title", "ru", mark="🌳", name="Дерево") in text
    winner = await session.get(User, 1)
    await session.refresh(winner)
    assert winner.last_notification_sent is not None, "сообщение заняло дневной бюджет"
    assert await notify_season_awards(bot, session) == 0


# ---------------------------------------------------------------------------
# «Вас обогнали»
# ---------------------------------------------------------------------------

@pytest.fixture
def own_sessions(engine, monkeypatch):
    import app.database.session as dbs

    maker = async_sessionmaker(engine, expire_on_commit=False)
    monkeypatch.setattr(dbs, "AsyncSessionLocal", maker)
    return maker


async def _race(session):
    season = await get_or_create_current_season(session)
    a, b = _free_ids(2)
    yesterday = utctoday() - timedelta(days=1)
    for uid, name in ((a, "Anna"), (b, "Boris")):
        session.add(User(id=uid, first_name=name, interface_language="ru",
                         learning_lang="de", native_lang="ru", level=CEFRLevel.A1,
                         timezone="UTC", notifications_enabled=True, notification_time="12:00",
                         quizzes_passed=3, last_active_date=yesterday,
                         created_at=utcnow() - timedelta(days=10)))
    await session.commit()
    await _month(session, season, [(a, "de", 100, 3), (b, "de", 150, 3)])
    anna = await session.get(User, a)
    anna.overtaken_by_id, anna.overtaken_at = b, utcnow() - timedelta(hours=1)
    await session.commit()
    return a, b


async def test_overtaken_is_off_until_the_owner_says_send(session, own_sessions):
    from app.schedulers import competition

    a, _ = await _race(session)
    users = (await session.execute(select(User))).scalars().all()
    assert await competition.plan(session, users, {}, utcnow()) == {}


async def test_overtaken_replaces_the_daily_message(session, own_sessions, monkeypatch):
    from app.config import settings
    from app.schedulers.nudges import send_nudges

    monkeypatch.setattr(settings, "COMPETITION_NUDGES", True, raising=False)
    a, b = await _race(session)
    now = datetime.combine(utctoday(), time(12, 30))

    class Bot:
        sent = []

        async def send_message(self, chat_id, text, **kwargs):
            self.sent.append((chat_id, text))

    bot = Bot()
    await send_nudges(bot, now)
    to_anna = [text for uid, text in bot.sent if uid == a]
    assert len(to_anna) == 1, bot.sent
    assert "Boris" in to_anna[0]
    async with own_sessions() as s:
        kinds = [r.kind for r in (await s.execute(
            select(NudgeLog).where(NudgeLog.user_id == a))).scalars()]
        anna = await s.get(User, a)
    assert kinds == ["overtaken"], kinds
    assert anna.overtaken_by_id is None


# ---------------------------------------------------------------------------
# Рывок в итоге занятия и отметка обгона
# ---------------------------------------------------------------------------

async def test_place_up_line_and_overtaken_mark(session):
    from app.bot.handlers.quiz.summary import _mark_overtaken, _month_place, _race_lines

    season = await get_or_create_current_season(session)
    for uid, name in ((1, "Anna"), (2, "Boris")):
        await _person(session, uid, name=name)
    await _month(session, season, [(1, "de", 100, 3), (2, "de", 150, 3)])
    before = await _month_place(session, 1)
    assert before["rank"] == 2
    stat = (await session.execute(select(MonthlyStats).where(MonthlyStats.user_id == 1))).scalar_one()
    stat.monthly_score = 200
    await session.commit()

    anna = await session.get(User, 1)
    lines = await _race_lines(session, anna, "ru", before)
    assert lines and lines[0].startswith(get_text("summary_place", "ru", rank=1)), lines
    await _mark_overtaken(session, 1, before)
    boris = await session.get(User, 2)
    await session.refresh(boris)
    assert boris.overtaken_by_id == 1


# ---------------------------------------------------------------------------
# Тексты на 10 языках
# ---------------------------------------------------------------------------

NEW_KEYS = [
    "title_sprout", "title_tree", "title_moon", "title_planet", "title_sun", "title_galaxy",
    "btn_rating_info", "card_place", "card_above", "card_below", "card_top", "card_month_line",
    "card_days_left", "card_medal_need", "card_title", "card_title_next", "card_title_secret",
    "card_title_none", "card_medals", "card_crowns", "card_crown_holder", "card_crown_nobody",
    "card_to_leader", "card_you_lead", "card_crown_rule", "card_crown_small", "table_crown_hint",
    "hall_title", "hall_line", "info_title", "info_month", "info_alltime", "info_lang",
    "info_titles", "info_streak", "summary_place", "summary_gap", "summary_record",
    "collection_title", "collection_locked", "award_month_header", "award_crown",
    "award_glory", "award_new_title", "nd_overtaken", "nd_finish",
] + [f"ach_{a.key}" for a in ACHIEVEMENTS]
CYRILLIC = re.compile(r"[А-Яа-яЁёІіЇїЄєҐґ]")


@pytest.mark.parametrize("lang", sorted(LOCALES))
def test_new_texts_exist_in_every_language(lang):
    for key in NEW_KEYS:
        value = LOCALES[lang].get(key)
        assert value, (lang, key)
        if lang not in ("ru", "uk"):
            assert not CYRILLIC.search(value), (lang, key, value)
    # Вкладки помещаются в ряд: «За всё время» и «Depuis le début» резались
    assert len(LOCALES[lang]["rating_tab_alltime"]) <= 10, lang
