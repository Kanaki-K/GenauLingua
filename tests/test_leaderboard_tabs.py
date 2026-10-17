"""
Рейтинг в три вкладки (владелец, 17.10): «за месяц со всеми, за всё время
со всеми и язык — с теми, кто учит тоже английский».

Двое: Анна учит немецкий (100) и английский (30), Борис — английский (50).
  * «Месяц» — все люди, баллы по языкам складываются: Анна 130, Борис 50;
  * вкладка языка — месяц среди учащих тот же язык: у Бориса (en) Борис
    первый, Анна вторая со своими 30 английскими;
  * «За всё время» — тоже со всеми.
"""
import pytest

from app.database.models import MonthlyStats, User
from app.services.monthly_leaderboard_service import (
    ALL_LANGS,
    get_lifetime_leaderboard,
    get_monthly_leaderboard,
    get_or_create_current_season,
    get_user_monthly_rank,
)
from tests.scenario import make_bot, make_dispatcher, press, reset_state

pytestmark = pytest.mark.asyncio

ANNA, BORIS = 5001, 5002


async def _people(session):
    season = await get_or_create_current_season(session)
    session.add_all([
        User(id=ANNA, first_name="Anna", interface_language="ru", learning_lang="de",
             native_lang="ru"),
        User(id=BORIS, first_name="Boris", interface_language="ru", learning_lang="en",
             native_lang="ru"),
    ])
    await session.flush()
    for uid, lang, score in ((ANNA, "de", 100), (ANNA, "en", 30), (BORIS, "en", 50)):
        session.add(MonthlyStats(user_id=uid, season_id=season.id, learning_lang=lang,
                                 monthly_score=score, monthly_quizzes=2, monthly_words=3,
                                 monthly_avg_percent=80))
    await session.commit()
    return season


async def test_month_with_everyone_adds_languages_up(session):
    season = await _people(session)
    board = await get_monthly_leaderboard(session, season_id=season.id, learning_lang=ALL_LANGS)
    assert [(e["user_id"], e["monthly_score"], e["rank"]) for e in board] == [
        (ANNA, 130, 1), (BORIS, 50, 2)]
    boris = await get_user_monthly_rank(BORIS, session, season_id=season.id,
                                        learning_lang=ALL_LANGS)
    assert (boris["rank"], boris["total_users"], boris["monthly_quizzes"]) == (2, 2, 2)


async def test_language_tab_is_only_that_language(session):
    season = await _people(session)
    board = await get_monthly_leaderboard(session, season_id=season.id, learning_lang="en")
    assert [(e["user_id"], e["monthly_score"]) for e in board] == [(BORIS, 50), (ANNA, 30)]


async def test_all_time_with_everyone(session):
    await _people(session)
    board = await get_lifetime_leaderboard(session, learning_lang=ALL_LANGS)
    assert [(e["user_id"], e["lifetime_score"]) for e in board] == [(ANNA, 130), (BORIS, 50)]


async def test_screens_have_three_tabs_and_the_right_tables(session):
    await _people(session)
    bot, recorder = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)

    await dp.feed_update(bot, press(BORIS, "show_my_rating"))
    assert recorder.buttons()[:3] == ["rating_monthly", "rating_alltime", "rating_lang"]
    assert "Английский" in recorder.button_texts()[2]
    # Карточка месяца: место и баллы со всеми (130 у Анны, 50 у Бориса)
    card = recorder.last_text()
    assert "#2" in card and "Anna" in card, card

    await dp.feed_update(bot, press(BORIS, "rating_monthly"))
    month = recorder.last_text()
    assert month.index("Anna") < month.index("Boris"), month
    # Строка таблицы (17.10): «место · звание · имя — баллы»; баллы по языкам сложены
    assert "1. Anna — 130" in month, month

    await dp.feed_update(bot, press(BORIS, "rating_lang"))
    by_lang = recorder.last_text()
    assert "Английский" in by_lang
    assert by_lang.index("Boris") < by_lang.index("Anna"), by_lang
    assert "Anna — 30" in by_lang and "130" not in by_lang, by_lang
    # Старая кнопка «Таблица лидеров» ведёт на тот же экран вкладки
    await dp.feed_update(bot, press(BORIS, "table_lang"))
    assert recorder.last_text() == by_lang

    await dp.feed_update(bot, press(BORIS, "rating_lang"))
    assert "Английский" in recorder.last_text()
    assert "rating_info:lang" in recorder.buttons()

    await dp.feed_update(bot, press(BORIS, "rating_alltime"))
    alltime = recorder.last_text()
    assert alltime.index("Anna") < alltime.index("Boris"), alltime
