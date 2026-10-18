"""
Напоминания по умолчанию (решение владельца 16.10).

«Убрал бы просто уведомления нахуй не нужные, а поставил бы базово на то
время, как человек зашёл — хочет? меняет сам». Прежде бот спрашивал
«Напоминать раз в день?» после первого урока, а потом ещё раз — после
ответа на предложение уровня.
"""
from datetime import datetime

import pytest

from app.database.models import User
from app.services.reminder_service import default_reminder_time, enable_by_default
from tests.scenario import make_bot, make_dispatcher, press, reset_state, text_update
from tests.test_nudges import own_sessions  # noqa: F401 — фикстура

pytestmark = pytest.mark.asyncio


@pytest.fixture
async def stage(session):
    bot, recorder = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    return dp, bot, recorder


async def test_new_person_gets_reminders_on_without_a_question(session, stage):
    dp, bot, recorder = stage
    await dp.feed_update(bot, text_update(4242, "/start"))
    person = await session.get(User, 4242)
    assert person.notifications_enabled and person.reminders_auto
    hour = int(person.notification_time[:2])
    assert 10 <= hour <= 20 and person.notification_time.endswith(":00")


async def test_existing_person_is_not_switched_on(session, user, stage):
    dp, bot, recorder = stage
    user.notifications_enabled = False
    await session.commit()
    await dp.feed_update(bot, text_update(user.id, "/start"))
    await session.refresh(user)
    assert not user.notifications_enabled and not user.reminders_auto


def test_time_is_the_hour_of_arrival_clamped_to_day():
    person = User(id=1, timezone="Europe/Berlin")
    # 06:30 UTC = 08:30 в Берлине летом → не раньше 10:00
    assert default_reminder_time(person, datetime(2026, 7, 1, 6, 30)) == "10:00"
    # 12:10 UTC = 14:10 → 14:00
    assert default_reminder_time(person, datetime(2026, 7, 1, 12, 10)) == "14:00"
    # 19:30 UTC = 21:30 → не позже 20:00
    assert default_reminder_time(person, datetime(2026, 7, 1, 19, 30)) == "20:00"
    # 23:00 UTC = 01:00 ночью → утром, в 10:00, а не в час ночи
    assert default_reminder_time(person, datetime(2026, 7, 1, 23, 0)) == "10:00"


async def test_setting_time_by_hand_clears_the_auto_mark(session, user, stage):
    dp, bot, recorder = stage
    enable_by_default(user)
    await session.commit()
    await dp.feed_update(bot, press(user.id, "notif_time:18:00"))
    await session.refresh(user)
    assert user.notification_time == "18:00" and not user.reminders_auto


async def test_auto_reminders_keep_a_control_group(session, own_sessions):  # noqa: F811 — фикстура
    """Включённым БОТОМ — контрольные 10% и без ежедневного; включившим сами — всегда."""
    from app.schedulers.nudges import send_nudges
    from tests.test_nudges import FakeBot, _log, _person, utc

    person = await _person(session, 5000, opted=True)        # 5000 — в контрольной
    person.reminders_auto = True
    await session.commit()
    bot = FakeBot()
    assert await send_nudges(bot, utc(2026, 11, 3, 20, 1)) == {"holdout": 1}
    assert bot.sent == []
    assert await _log(own_sessions, 5000) == [("daily", "holdout")]
    # Ежедневное удержано один раз за день, а не каждые 5 минут окна
    assert await send_nudges(bot, utc(2026, 11, 3, 20, 6)) == {}


async def test_first_auto_message_names_the_time_and_offers_to_change(session, own_sessions):  # noqa: F811
    from app.schedulers.nudges import send_nudges
    from tests.test_nudges import FakeBot, _person, utc

    person = await _person(session, 5001, opted=True)        # 5001 — не в контрольной
    person.reminders_auto = True
    await session.commit()
    bot = FakeBot()
    assert await send_nudges(bot, utc(2026, 11, 3, 20, 1)) == {"sent": 1}
    _, text, markup = bot.sent[0]
    assert "20:00" in text
    data = [b.callback_data for row in markup.inline_keyboard for b in row]
    assert "notif_change_time" in data and "notif_off" in data
