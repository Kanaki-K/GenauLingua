# -*- coding: utf-8 -*-
"""
Сообщение второго дня — независимый аудит 2.1 (15.10.2026).

Аудит нашёл четыре дефекта (до починки эти тесты падали):
  * напоминание и сообщение второго дня в одну минуту — два сообщения
    (гонка в обе стороны: отметка дня ставилась после ответа Telegram);
  * через полночь — второе сообщение через 4 ч после напоминания;
  * «Вчера Вы…» в тот же день (первое занятие в 00:30, окно 22–26 ч);
  * выключение в настройках не считалось явным отказом.
И одну потерю: сбой сети навсегда лишал сообщения — теперь повтор.

ВРЕМЯ — НЕПОДВИЖНОЕ (`NOW`): окно привязано к часам дня человека, и тест
от настоящих часов падал бы ночью.
"""
import asyncio
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pytest
from aiogram.exceptions import TelegramNetworkError, TelegramRetryAfter
from aiogram.methods import SendMessage
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.database.enums import CEFRLevel
from app.database.models import QuizSession, User
from app.schedulers import day2_hook
from app.schedulers.day2_hook import due_users, send_day2_hooks

pytestmark = pytest.mark.asyncio

NOW = (datetime(2026, 10, 21, 18, 0, tzinfo=ZoneInfo("Europe/Berlin"))
       .astimezone(ZoneInfo("UTC")).replace(tzinfo=None))


class FakeBot:
    """Бот без сети: записывает отправки, умеет «тормозить» и падать."""

    def __init__(self, delay: float = 0.0, fail=None):
        self.sent: list[tuple[int, str]] = []
        self.delay = delay
        self.fail = fail

    async def send_message(self, chat_id=None, text=None, *args, **kwargs):
        if chat_id is None and args:
            chat_id = args[0]
        if self.delay:
            await asyncio.sleep(self.delay)        # время запроса в Telegram
        if self.fail is not None:
            exc, self.fail = self.fail, None        # падает один раз
            raise exc
        self.sent.append((chat_id, text))


@pytest.fixture
def own_sessions(engine, monkeypatch):
    """Планировщики открывают свои сессии — подменяем фабрику на тестовую базу."""
    import app.database.session as dbs

    maker = async_sessionmaker(engine, expire_on_commit=False)
    monkeypatch.setattr(dbs, "AsyncSessionLocal", maker)
    return maker


async def _finished(session, user, done: datetime):
    user.quizzes_passed = (user.quizzes_passed or 0) + 1
    session.add(QuizSession(user_id=user.id, level=CEFRLevel.A1, total_questions=7,
                            answered_questions=7, is_completed=True,
                            started_at=done - timedelta(minutes=3), completed_at=done))
    await session.commit()


async def _reload(maker, user_id) -> User:
    async with maker() as s:
        return await s.get(User, user_id)


# ============================================================================
# 1. ДЕФЕКТ: два сообщения в один день — обычное напоминание «в полёте» и day2
# ============================================================================

async def test_reminder_in_flight_and_day2_give_two_messages(
        session, user, own_sessions, monkeypatch):
    """
    Новичок принял предложение напоминаний; его час совпал с тиком day2.
    Обычное напоминание ставит `last_notification_sent` только ПОСЛЕ ответа
    Telegram, а захват day2 проверяет лишь `day2_hook_sent_at`. Пока первое
    сообщение в пути, day2 видит «сегодня ничего не было» и шлёт второе.
    """
    from app.schedulers import reminder_scheduler as rs

    now = NOW
    await _finished(session, user, now - timedelta(hours=23))
    local = now.replace(tzinfo=ZoneInfo("UTC")).astimezone(ZoneInfo("Europe/Berlin"))
    user.timezone = "Europe/Berlin"
    user.notifications_enabled = True
    user.notification_time = f"{local.hour:02d}:{local.minute:02d}"
    user.notification_days = [0, 1, 2, 3, 4, 5, 6]
    await session.commit()
    assert rs.reminder_is_due(user, now)

    async def fake_reminder(bot, u, s):
        await bot.send_message(u.id, "обычное напоминание")
        return rs.SENT

    monkeypatch.setattr(rs, "send_notification_to_user", fake_reminder)

    bot = FakeBot(delay=0.5)

    async def day2_slightly_later():
        await asyncio.sleep(0.15)                  # тот же тик, чуть позже
        return await send_day2_hooks(bot, now)

    await asyncio.gather(rs.check_and_send_notifications(bot, now), day2_slightly_later())

    to_user = [t for chat, t in bot.sent if chat == user.id]
    assert len(to_user) == 1, f"в один день ушло {len(to_user)} сообщения: {to_user}"


async def test_day2_in_flight_and_reminder_give_two_messages(
        session, user, own_sessions, monkeypatch):
    """
    Обратная сторона. Тик напоминаний загрузил людей раньше, чем day2
    захватил человека; `session.get` отдаёт объект из карты тождеств, не
    перечитывая, — `last_notification_sent` у него старый, и напоминание
    уходит вторым сообщением.
    """
    from app.schedulers import reminder_scheduler as rs

    now = NOW
    await _finished(session, user, now - timedelta(hours=23))
    local = now.replace(tzinfo=ZoneInfo("UTC")).astimezone(ZoneInfo("Europe/Berlin"))
    user.timezone = "Europe/Berlin"
    user.notifications_enabled = True
    user.notification_time = f"{local.hour:02d}:{local.minute:02d}"
    await session.commit()

    sent: list[str] = []
    claimed = asyncio.Event()

    async def fake_reminder(bot, u, s):
        sent.append("обычное")
        return rs.SENT

    monkeypatch.setattr(rs, "send_notification_to_user", fake_reminder)

    class Bot2(FakeBot):
        async def send_message(self, chat_id=None, text=None, *a, **k):
            sent.append("day2")
            claimed.set()

    # Выборка напоминаний сделана ДО захвата day2: перехватываем момент
    # после выборки и до отправки
    from sqlalchemy.ext.asyncio import AsyncSession
    orig_get = AsyncSession.get

    async def slow_get(self, cls, ident, *a, **k):
        if cls is User and ident == user.id and not claimed.is_set():
            await asyncio.wait_for(claimed.wait(), 5)
        return await orig_get(self, cls, ident, *a, **k)

    monkeypatch.setattr(AsyncSession, "get", slow_get)

    async def day2_after_reminder_selected():
        await asyncio.sleep(0.2)
        return await send_day2_hooks(Bot2(), now)

    await asyncio.gather(rs.check_and_send_notifications(Bot2(), now),
                         day2_after_reminder_selected())
    assert sent.count("day2") == 1
    assert len(sent) == 1, f"в один день ушло два сообщения: {sent}"


# ============================================================================
# 2. ДЕФЕКТ: выключил напоминания в НАСТРОЙКАХ — отказ не записан
# ============================================================================

async def test_settings_toggle_off_is_not_an_explicit_refusal(session, user):
    """
    Новичок включил напоминания (предложение после занятия) и тут же выключил
    их общим переключателем в настройках. Это такой же явный отказ, как
    «Не напоминать» под напоминанием, но `notif_toggle` не ставит
    `reminders_declined_at` — и через сутки приходит сообщение второго дня.
    """
    from app.testing import make_bot, make_dispatcher, press, reset_state

    now = NOW
    await _finished(session, user, now - timedelta(hours=23))
    user.notifications_enabled = True
    user.timezone = "Europe/Kyiv"
    user.level = CEFRLevel.A1
    await session.commit()

    bot, _ = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    await dp.feed_update(bot, press(user.id, "notif_toggle"))
    await session.refresh(user)
    assert user.notifications_enabled is False

    due = await due_users(session, now)
    assert [u.id for u, _ in due] == [], "выключивший в настройках получит day2"


# ============================================================================
# 3. Сбой сети / флуд-контроль — захват отпускается, следующий тик повторяет
# ============================================================================

@pytest.mark.parametrize("error", [
    TelegramNetworkError(method=SendMessage(chat_id=1, text="x"), message="timeout"),
    TelegramRetryAfter(method=SendMessage(chat_id=1, text="x"), message="flood", retry_after=5),
])
async def test_transient_failure_is_retried_next_tick(session, user, own_sessions, error):
    now = NOW
    await _finished(session, user, now - timedelta(hours=23))

    bot = FakeBot(fail=error)
    assert await send_day2_hooks(bot, now) == 0
    stored = await _reload(own_sessions, user.id)
    assert stored.day2_hook_sent_at is None, "сбой сети съел сообщение навсегда"
    assert stored.last_notification_sent is None, "и обычное напоминание сегодня тоже"

    assert await send_day2_hooks(bot, now + timedelta(minutes=10)) == 1
    assert len(bot.sent) == 1


# ============================================================================
# Проверки верного поведения
# ============================================================================

async def test_two_processes_send_once(session, user, own_sessions):
    now = NOW
    await _finished(session, user, now - timedelta(hours=23))
    bot = FakeBot(delay=0.05)
    results = await asyncio.gather(send_day2_hooks(bot, now), send_day2_hooks(bot, now))
    assert sum(results) == 1 and len(bot.sent) == 1


async def test_after_day2_regular_reminder_waits_till_tomorrow(session, user, own_sessions):
    from app.schedulers.reminder_scheduler import reminder_is_due

    now = NOW
    await _finished(session, user, now - timedelta(hours=23))
    assert await send_day2_hooks(FakeBot(), now) == 1
    stored = await _reload(own_sessions, user.id)
    local = now.replace(tzinfo=ZoneInfo("UTC")).astimezone(ZoneInfo("Europe/Berlin"))
    stored.notifications_enabled = True
    stored.timezone = "Europe/Berlin"
    stored.notification_days = [0, 1, 2, 3, 4, 5, 6]
    stored.notification_time = f"{local.hour:02d}:{local.minute:02d}"
    assert not reminder_is_due(stored, now + timedelta(minutes=1))


async def test_blocked_bot_turns_reminders_off(session, user, own_sessions):
    from aiogram.exceptions import TelegramForbiddenError

    now = NOW
    await _finished(session, user, now - timedelta(hours=23))
    user.notifications_enabled = True
    await session.commit()
    err = TelegramForbiddenError(method=SendMessage(chat_id=1, text="x"), message="blocked")
    assert await send_day2_hooks(FakeBot(fail=err), now) == 0
    stored = await _reload(own_sessions, user.id)
    assert stored.notifications_enabled is False


async def test_old_users_are_not_targeted_after_migration(session, user, own_sessions):
    """Старый человек (первое занятие месяц назад, 3 занятия, сегодня вернулся) — не цель."""
    now = NOW
    await _finished(session, user, now - timedelta(days=30))
    await _finished(session, user, now - timedelta(days=29))
    await _finished(session, user, now - timedelta(hours=23))
    assert user.day2_hook_sent_at is None
    assert await due_users(session, now) == []


async def test_repeat_only_session_does_not_count_as_return_nor_first(session, user):
    """Брошенное/незавершённое занятие во второй день не мешает day2; повтор ошибок не «первое»."""
    now = NOW
    await _finished(session, user, now - timedelta(hours=23))
    session.add(QuizSession(user_id=user.id, level=CEFRLevel.A1, total_questions=7,
                            answered_questions=2, is_completed=False,
                            started_at=now - timedelta(hours=1), exit_reason="abandoned"))
    await session.commit()
    assert [u.id for u, _ in await due_users(session, now)] == [user.id]


async def test_declined_offer_button_blocks_day2(session, user):
    from app.testing import make_bot, make_dispatcher, press, reset_state

    now = NOW
    await _finished(session, user, now - timedelta(hours=23))
    bot, _ = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    await dp.feed_update(bot, press(user.id, "reminder_offer_no"))
    await session.refresh(user)
    assert user.reminders_declined_at is not None
    assert await due_users(session, now) == []


async def test_day2_button_records_source_day2(session, user, own_sessions):
    """Кнопка из настоящего сообщения второго дня → занятие с пометкой day2."""
    from app.testing import make_bot, make_dispatcher, press, reset_state
    from tests.conftest import build_groups, make_word
    from app.database.enums import QuizMode

    for i in range(40):
        session.add(make_word(f"Wort{i:03d}", level=CEFRLevel.A1))
    await build_groups(session, ["de"])
    user.level = CEFRLevel.A1
    user.quiz_mode = QuizMode.LEVEL
    user.quiz_word_count = 4
    user.quiz_channels = "t"
    now = NOW
    await _finished(session, user, now - timedelta(hours=23))

    bot, recorder = make_bot()
    assert await send_day2_hooks(bot, now) == 1
    data = recorder.buttons()[0]
    assert data == "learn_now:day2"

    dp = make_dispatcher(session)
    await reset_state(dp)
    await dp.feed_update(bot, press(user.id, data))
    src = (await session.execute(
        select(QuizSession.start_source).where(QuizSession.user_id == user.id)
        .order_by(QuizSession.id.desc()).limit(1))).scalar()
    assert src == "day2"


# ============================================================================
# 4. Граница суток: «одно в день» — по календарю, а не по промежутку
# ============================================================================

def _berlin(y, m, d, hh, mm) -> datetime:
    """Местное берлинское время → наивное UTC, как в схеме."""
    return (datetime(y, m, d, hh, mm, tzinfo=ZoneInfo("Europe/Berlin"))
            .astimezone(ZoneInfo("UTC")).replace(tzinfo=None))


async def test_reminder_at_20_then_day2_at_midnight(session, user):
    """
    Первое занятие в 23:50 (Берлин). На следующий день в 20:00 пришло обычное
    напоминание — day2 до полуночи молчит («сегодня уже было»). В 00:00
    наступает новый календарный день, окно (до 26 ч, т.е. до 01:50) ещё
    открыто — и day2 уходит в полночь, через четыре часа после напоминания,
    со словом «Вчера» про позавчерашнее занятие.
    """
    first = _berlin(2026, 10, 20, 23, 50)
    await _finished(session, user, first)
    user.timezone = "Europe/Berlin"
    user.last_notification_sent = _berlin(2026, 10, 21, 20, 0)
    await session.commit()

    midnight = _berlin(2026, 10, 22, 0, 0)
    due = await due_users(session, midnight)
    assert due == [], "второе сообщение через 4 часа после напоминания, в полночь"


async def test_yesterday_said_on_the_same_day(session, user):
    """
    Первое занятие в 00:30 (Берлин). Через 22 ч — 22:30 ТОГО ЖЕ дня, и
    человек получает «Вчера Вы узнали…» о сегодняшнем занятии.
    """
    from app.services.streak_service import user_day

    first = _berlin(2026, 10, 20, 0, 30)
    await _finished(session, user, first)
    user.timezone = "Europe/Berlin"
    await session.commit()

    now = _berlin(2026, 10, 20, 22, 40)
    due = await due_users(session, now)
    if due:
        assert user_day(user, now) > user_day(user, first), \
            "«Вчера» в тот же календарный день"


# ============================================================================
# 5. Перебор: первое занятие в любую минуту суток, в разных поясах
# ============================================================================

@pytest.mark.parametrize("zone", ["Europe/Berlin", "Europe/Kyiv", "America/New_York", "Asia/Tokyo"])
async def test_every_time_of_day_gets_one_daytime_message_next_day(session, user, zone):
    """
    Для первого занятия в любое время суток (шаг 20 мин): сообщение уходит
    ровно назавтра (по поясу человека), днём 09:00–22:00, хотя бы в одну
    10-минутную проверку — никто не пропущен.
    """
    from app.services.streak_service import user_day

    tz = ZoneInfo(zone)
    user.timezone = zone
    await session.commit()
    for minute_of_day in range(0, 24 * 60, 20):
        local_first = datetime(2026, 11, 10, minute_of_day // 60, minute_of_day % 60, tzinfo=tz)
        first = local_first.astimezone(ZoneInfo("UTC")).replace(tzinfo=None)
        user.quizzes_passed = 1
        session.add(QuizSession(user_id=user.id, level=CEFRLevel.A1, total_questions=7,
                                answered_questions=7, is_completed=True,
                                started_at=first - timedelta(minutes=3), completed_at=first))
        await session.commit()

        hits = []
        t = first
        while t < first + timedelta(hours=60):
            if await due_users(session, t):
                hits.append(t)
            t += timedelta(minutes=10)
        assert hits, f"{zone} {local_first:%H:%M}: сообщение не ушло бы ни разу"
        for t in hits:
            local = t.replace(tzinfo=ZoneInfo("UTC")).astimezone(tz)
            assert user_day(user, t) == user_day(user, first) + timedelta(days=1), (zone, local_first, local)
            assert 9 <= local.hour < 22, f"{zone}: первое в {local_first:%H:%M} → сообщение в {local:%H:%M}"

        await session.execute(QuizSession.__table__.delete().where(QuizSession.user_id == user.id))
        await session.commit()


# ============================================================================
# 6. Каждая защита по отдельности (прочие её подстраховывают и прячут поломку)
# ============================================================================

def _berlin_utc(d, hh, mm) -> datetime:
    return (datetime(2026, 11, d, hh, mm, tzinfo=ZoneInfo("Europe/Berlin"))
            .astimezone(ZoneInfo("UTC")).replace(tzinfo=None))


async def test_not_on_the_same_day_even_inside_the_window(session, user):
    """Первое в 08:00, в 10:00 того же дня окно (09:00–13:00) и день — но не назавтра."""
    user.timezone = "Europe/Berlin"
    await _finished(session, user, _berlin_utc(10, 8, 0))
    assert await due_users(session, _berlin_utc(10, 10, 0)) == []
    assert [u.id for u, _ in await due_users(session, _berlin_utc(11, 10, 0))] == [user.id]


async def test_twelve_hours_after_any_message(session, user):
    """Напоминание вчера в 23:00, сегодня 09:30 — другой день, окно, день; но 10,5 ч."""
    user.timezone = "Europe/Berlin"
    await _finished(session, user, _berlin_utc(10, 10, 0))
    user.last_notification_sent = _berlin_utc(10, 23, 0)
    await session.commit()
    assert await due_users(session, _berlin_utc(11, 9, 30)) == []
    assert [u.id for u, _ in await due_users(session, _berlin_utc(11, 11, 30))] == [user.id]


async def test_claim_yields_to_a_reminder_sent_after_the_read(session, user, own_sessions, monkeypatch):
    """Напоминание ушло между выборкой и захватом — захват не состоится."""
    from sqlalchemy import update as sa_update

    now = NOW
    await _finished(session, user, now - timedelta(hours=23))

    async def reminder_sneaks_in(s, u, first_done):
        async with own_sessions() as other:
            await other.execute(sa_update(User).where(User.id == u.id)
                                .values(last_notification_sent=now))
            await other.commit()
        return 3

    monkeypatch.setattr(day2_hook, "words_of_first_day", reminder_sneaks_in)
    bot = FakeBot()
    assert await send_day2_hooks(bot, now) == 0
    assert bot.sent == []
