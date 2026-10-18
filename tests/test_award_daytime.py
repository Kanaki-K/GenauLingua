"""
Итоги месяца — днём у самого человека (2.2.1).

Сезон закрывается 1-го в 00:05 UTC, и извещение уходило сразу: 01:05 Берлин,
02:05 Киев. Теперь оно ждёт дня [10:00, 20:00) по поясу человека; почасовая
досылка отправляет его в первый же дневной час, и ровно один раз.
"""
from datetime import timedelta

from app.core.clock import utcnow
from app.services.monthly_leaderboard_service import _daytime_for, notify_season_awards
from tests.test_awards import FakeBot, _award, _season


def _at_utc(hour: int):
    return utcnow().replace(hour=hour, minute=30, second=0, microsecond=0)


def test_berlin_night_and_day(user):
    user.timezone = "Europe/Berlin"
    assert not _daytime_for(user, _at_utc(0))        # 01:30 / 02:30 Берлин
    assert _daytime_for(user, _at_utc(12))           # 13:30 / 14:30 Берлин


def test_kyiv_is_an_hour_ahead_of_berlin(user):
    user.timezone = "Europe/Kyiv"
    assert _daytime_for(user, _at_utc(8))            # 10:30 / 11:30 Киев


async def test_at_night_the_award_waits_and_goes_out_by_day_once(session, user):
    user.timezone = "Europe/Berlin"
    season = await _season(session)
    await _award(session, season, user)
    bot = FakeBot()
    night = _at_utc(0)
    assert await notify_season_awards(bot, session, now=night) == 0, "итоги ушли ночью"
    assert not bot.sent
    day = night + timedelta(hours=12)
    assert await notify_season_awards(bot, session, now=day) == 1
    assert await notify_season_awards(bot, session, now=day + timedelta(hours=1)) == 0
    assert len(bot.sent) == 1
