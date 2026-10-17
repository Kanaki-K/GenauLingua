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
    anchor_line, standing_of, table_line, title_for,
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
    # Таблица — звание и имя; корона — только на вкладке языка; серия — в якоре
    assert table_line("Kostia", st) == "🌙 Kostia"
    assert table_line("Kostia", st, crown=True) == "🌙 Kostia 👑"
    assert anchor_line("Kostia", st, 27) == "🌙 Kostia 🔥27"
    assert anchor_line("Kostia", None, 2) == "Kostia"


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

    # ОДИН ЭКРАН НА ВКЛАДКУ (17.10): таблица, под чертой — я, и мой приз
    await dp.feed_update(bot, press(12, "rating_monthly"))
    month = recorder.last_text()
    assert "1. Anna — 300" in month and "2. <b>Boris</b> — 200" in month, month
    assert get_text("rating_you", "ru", rank=2, total=3, points="200 баллов") in month
    # У Бориса два занятия — медали не будет, и это сказано
    assert get_text("card_medal_need", "ru", need=3, have=2) in month
    assert recorder.button_texts()[0] == "✓ Месяц"

    # Под таблицей: строка «Вы», строка приза, тихая строка — и только
    tail = month.split("\n\n")[-1].split("\n")
    assert len(tail) <= 3, tail

    # Строки приза нет (владелец: «🥈 · до 🥇 — тупо лишнее»): только место и баллы
    await dp.feed_update(bot, press(11, "rating_monthly"))
    leader = recorder.last_text()
    assert "🥇" not in leader and "🥈" not in leader, leader

    await dp.feed_update(bot, press(12, "rating_lang"))
    lang_card = recorder.last_text()
    # В языке трое, но с 3+ занятиями только двое: корона не разыгрывается
    assert get_text("card_crown_small", "ru") in lang_card

    await dp.feed_update(bot, press(12, "rating_alltime"))
    alltime = recorder.last_text()
    # Своего звания и медалей во «Всё время» нет (17.10): звание у имени,
    # медали — в статистике; под таблицей только «Вы»
    assert alltime.rstrip().endswith(get_text("rating_you", "ru", rank=2, total=3,
                                              points="200 баллов")), alltime
    assert "rating_info:alltime" in recorder.buttons()

    await dp.feed_update(bot, press(12, "rating_info:alltime"))
    assert get_text("info_title", "ru") in recorder.last_text()
    assert recorder.buttons() == ["rating_alltime"]


async def test_crown_is_worn_in_the_table_with_a_hint(session):
    from app.bot.handlers.leaderboard.leaderboard_table import _rows
    from app.bot.handlers.leaderboard.monthly import month_screen

    rows = [{"user_id": 1, "rank": 1, "display_name": "Olga"},
            {"user_id": 2, "rank": 2, "display_name": "Ivan"}]
    ranks = {1: Standing(user_id=1, crown_lang="de"), 2: Standing(user_id=2)}
    lines, me_in, crown = _rows(rows, 2, None, ranks, crown=True)
    assert lines == ["1. Olga 👑", "2. <b>Ivan</b>"] and me_in and crown
    # На «Месяце» и «Всё время» короны в строках нет (владелец: только на языке)
    assert _rows(rows, 2, None, ranks)[0] == ["1. Olga", "2. <b>Ivan</b>"]

    # Подпись к 👑 — в «Инфо», а не на каждом экране (владелец: «наляписто»)
    from app.bot.handlers.leaderboard.monthly import info_text

    assert "👑" in info_text("ru")


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
    "btn_rating_info", "card_medal_need", "card_crown_small",
    "rating_screen_title", "rating_screen_title_alltime", "rating_you", "rating_results_in",
    "rating_crown_rule",
    "info_title", "info_month", "info_alltime", "info_lang", "info_points_title", "info_points",
    "summary_place", "summary_gap", "summary_record",
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


@pytest.mark.parametrize("lang", sorted(LOCALES))
async def test_every_rating_screen_reads_right_in_every_language(session, lang):
    """
    Владелец, 17.10: «нужно убедиться, что на всех языках интерфейс будет
    выглядеть правильно». Все экраны рейтинга на языке интерфейса: без
    пропусков, без русских букв в латинских языках, кнопки вкладок короткие.
    """
    from app.bot.handlers.quiz.stats import collection_text
    from app.schedulers.competition import _text

    season = await get_or_create_current_season(session)
    for uid, name in ((21, "Anna"), (22, "Boris"), (23, "Clara")):
        session.add(User(id=uid, first_name=name, interface_language=lang, learning_lang="de",
                         native_lang="en" if lang != "en" else "fr", level=CEFRLevel.A1))
    await session.commit()
    await _month(session, season, [(21, "de", 300, 5), (22, "de", 200, 2), (23, "de", 100, 4)])
    bot, recorder = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    for data in ("rating_monthly", "rating_lang", "rating_alltime", "rating_info:monthly"):
        await dp.feed_update(bot, press(22, data))
        if data.startswith("rating_") and ":" not in data:
            tabs = recorder.button_texts()[:3]
            assert all(len(t) <= 14 for t in tabs), (lang, tabs)
    texts = recorder.sent_texts()
    boris = await session.get(User, 22)
    texts.append(await collection_text(boris, session, lang))
    mine = {"rank": 5, "monthly_score": 80, "display_name": "Boris"}
    texts.append(_text("overtaken", {"mine": mine, "rival": {"display_name": "Anna",
                                                               "monthly_score": 95}}, lang))
    texts.append(_text("finish", {"mine": mine, "days": 2,
                                  "third": {"monthly_score": 120}}, lang))
    assert len(texts) >= 7
    for text in texts:
        assert "[MISSING" not in text and "[ERROR" not in text, (lang, text)
        if lang not in ("ru", "uk"):
            assert not CYRILLIC.search(text), (lang, text)
