# -*- coding: utf-8 -*-
"""
Сообщения по инициативе бота — патч 2.1 «Вовлечение».

Владелец 15.10: вовлечение для ВСЕХ, «нельзя заебать напоминаниями: уместно,
ненавязчиво, с интересом, показывать пользу»; «нужно внимательно трекать —
работает или вредит»; «чем человечнее обращение, тем лучше».

Три слоя:
  правило     `nudge_plan.decide` — перебором дней и тиков: не больше одного
              в день, ≥12 ч, днём, лесенка обрывается, отказ — навсегда
  тексты      `nudge_texts.compose` — шесть языков, «Вы», без ИИ-шлейфа
  отправка    `nudges.send_nudges` с базой — захват, журнал, контрольная
              группа, блокировка, сбой сети, кнопки
"""
import asyncio
import random
import re
from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.database.enums import CEFRLevel
from app.database.models import NudgeLog, QuizSession, User
from app.locales import LOCALES
from app.services import nudge_plan
from app.services.nudge_plan import DAILY, NudgeState, decide
from app.services.nudge_texts import NudgeFacts, compose, variants

BERLIN = ZoneInfo("Europe/Berlin")
UTC = ZoneInfo("UTC")


def utc(y, m, d, hh, mm=0) -> datetime:
    """Местное берлинское → наивное UTC."""
    return datetime(y, m, d, hh, mm, tzinfo=BERLIN).astimezone(UTC).replace(tzinfo=None)


# ============================================================================
# ПРАВИЛО
# ============================================================================

def _state(now, *, played=True, anchor, opted=False, own="20:00", days=(0, 1, 2, 3, 4, 5, 6),
           usual=time(18, 0), step=0, last=None, declined=False):
    return NudgeState(now_local=now, played=played, anchor_day=anchor, opted_in=opted,
                      declined=declined, own_time=time.fromisoformat(own) if opted else None,
                      own_days=days, usual_time=usual, sent_step_for_anchor=step,
                      last_sent_local=last)


def test_ladder_days_only_for_not_opted():
    anchor = date(2026, 11, 2)
    sent = []
    for away in range(0, 30):
        now = datetime.combine(anchor + timedelta(days=away), time(18, 0))
        got = decide(_state(now, anchor=anchor, step=max([0] + [s for _, s in sent])))
        if got:
            sent.append(got)
    assert sent == [("back1", 1), ("back3", 3), ("back7", 7), ("back14", 14)], sent


def test_never_played_gets_three_invitations():
    anchor = date(2026, 11, 2)
    sent = []
    for away in range(0, 30):
        now = datetime.combine(anchor + timedelta(days=away), time(18, 0))
        got = decide(_state(now, played=False, anchor=anchor, step=max([0] + [s for _, s in sent])))
        if got:
            sent.append(got)
    assert sent == [("start1", 1), ("start3", 3), ("start7", 7)], sent
    assert nudge_plan.is_last("start7") and nudge_plan.is_last("back14")


def test_opted_in_daily_while_short_break_then_ladder_then_silence():
    anchor = date(2026, 11, 2)
    sent = []
    last = None
    for away in range(0, 30):
        now = datetime.combine(anchor + timedelta(days=away), time(20, 1))
        got = decide(_state(now, anchor=anchor, opted=True, step=max([0] + [s for _, s in sent]),
                            last=last))
        if got:
            sent.append(got)
            last = now
    assert [k for k, _ in sent] == [DAILY, DAILY, "back3", "back7", "back14"], sent


def test_active_today_gets_nothing():
    today = date(2026, 11, 2)
    now = datetime.combine(today, time(20, 1))
    assert decide(_state(now, anchor=today, opted=True)) is None
    assert decide(_state(now, anchor=today)) is None


def test_opted_in_respects_own_days():
    anchor = date(2026, 11, 1)                     # воскресенье
    monday = datetime.combine(date(2026, 11, 2), time(20, 1))
    assert decide(_state(monday, anchor=anchor, opted=True, days=(1, 2, 3, 4))) is None
    assert decide(_state(monday, anchor=anchor, opted=True, days=(0,))) == (DAILY, 0)


def test_declined_never():
    anchor = date(2026, 11, 2)
    for away in range(30):
        for hour in range(24):
            now = datetime.combine(anchor + timedelta(days=away), time(hour, 0))
            assert decide(_state(now, anchor=anchor, declined=True)) is None
            assert decide(_state(now, anchor=anchor, declined=True, opted=True)) is None


def test_one_per_day_and_twelve_hours():
    anchor = date(2026, 11, 2)
    now = datetime(2026, 11, 3, 18, 0)
    assert decide(_state(now, anchor=anchor, last=datetime(2026, 11, 3, 9, 0))) is None
    assert decide(_state(now, anchor=anchor, last=datetime(2026, 11, 3, 8, 0) - timedelta(hours=1))) is None
    # Вчера в 23:00 — другой день, но 19 ч прошло: можно
    assert decide(_state(now, anchor=anchor, last=datetime(2026, 11, 2, 23, 0)))



def test_one_per_day_alone():
    """Сегодня в 05:00 уже было — 13 ч назад, но тот же день: нельзя."""
    anchor = date(2026, 11, 2)
    now = datetime(2026, 11, 3, 18, 0)
    assert decide(_state(now, anchor=anchor, last=datetime(2026, 11, 3, 5, 0))) is None
    assert decide(_state(now, anchor=anchor, last=datetime(2026, 11, 2, 5, 0)))


def test_twelve_hours_alone():
    """Вчера в 23:30, сейчас 10:30 — другой день и окно открыто, но 11 ч: нельзя."""
    anchor = date(2026, 11, 2)
    now = datetime(2026, 11, 3, 10, 30)
    assert decide(_state(now, anchor=anchor, usual=time(11, 0), last=datetime(2026, 11, 2, 23, 30))) is None
    assert decide(_state(now, anchor=anchor, usual=time(11, 0), last=datetime(2026, 11, 2, 21, 0)))


def test_not_opted_only_in_the_daytime():
    anchor = date(2026, 11, 2)
    for minute in range(0, 24 * 60, 10):
        for usual in (time(0, 30), time(7, 0), time(13, 0), time(23, 50)):
            now = datetime.combine(anchor + timedelta(days=1), time(minute // 60, minute % 60))
            if decide(_state(now, anchor=anchor, usual=usual)):
                assert time(9, 0) <= now.time() < time(22, 0), (usual, now)


@pytest.mark.parametrize("seed", range(4))
def test_simulation_never_annoys(seed):
    """
    Перебор: случайные люди, случайные дни занятий, тик каждые 10 минут два
    месяца. Ни разу не два сообщения в день, ни разу ближе 12 ч, не больше
    четырёх за перерыв у не включавших, после отказа — ничего.
    """
    rng = random.Random(seed)
    for _ in range(40):
        opted = rng.random() < 0.4
        own = f"{rng.randint(7, 22):02d}:{rng.choice(['00', '30'])}"
        usual = time(rng.randint(0, 23), rng.randint(0, 59))
        played = rng.random() < 0.8
        start = date(2026, 11, 1)
        lesson_days = sorted({start + timedelta(days=d) for d in range(60) if rng.random() < 0.25}) if played else []
        declined_from = start + timedelta(days=rng.randint(10, 80)) if rng.random() < 0.2 else None
        anchor = lesson_days[0] if lesson_days else start
        nudge_anchor, nudge_step, last = None, 0, None
        sent = []
        t = datetime.combine(start, time(0, 0))
        while t < datetime.combine(start + timedelta(days=60), time(0, 0)):
            today = t.date()
            done_today = today in lesson_days and t.time() >= usual
            past = [d for d in lesson_days if d < today or (d == today and done_today)]
            if played and past:
                anchor = past[-1]
            elif played:
                t += timedelta(minutes=10)
                continue
            declined = declined_from is not None and today >= declined_from
            state = _state(t, played=played, anchor=anchor, opted=opted, own=own, usual=usual,
                           step=nudge_step if nudge_anchor == anchor else 0, last=last,
                           declined=declined)
            got = decide(state)
            if got:
                kind, step = got
                assert not declined
                sent.append((t, kind, anchor))
                last = t
                if kind != DAILY:
                    nudge_anchor, nudge_step = anchor, step
            t += timedelta(minutes=10)
        days = [s[0].date() for s in sent]
        assert len(days) == len(set(days)), "два сообщения в один день"
        for a, b in zip(sent, sent[1:]):
            assert b[0] - a[0] >= timedelta(hours=12), (a, b)
        if not opted:
            per_break = {}
            for _, _, anc in sent:
                per_break[anc] = per_break.get(anc, 0) + 1
            assert max(per_break.values(), default=0) <= 4
            for moment, _, _ in sent:
                assert time(9, 0) <= moment.time() < time(22, 0)


def test_holdout_is_about_ten_percent_and_stable():
    share = sum(nudge_plan.in_holdout(i) for i in range(10_000, 30_000)) / 20_000
    assert 0.08 <= share <= 0.12, share
    assert nudge_plan.in_holdout(5000) and not nudge_plan.in_holdout(5001)


# ============================================================================
# ТЕКСТЫ
# ============================================================================

PEOPLE = [
    NudgeFacts(name="Анна", flag="🇩🇪", word=("die Rechnung", "счёт"), questions=7),
    NudgeFacts(name="Анна", first_day=True, first_day_words=7, known=5, in_work=7,
               word=("die Fahrkarte", "билет"), lessons=1),
    NudgeFacts(name="Анна", first_day=True, first_day_words=1, known=1, in_work=1, lessons=1),
    NudgeFacts(name="Анна", streak=5, known=31, in_work=38, learned=6, word=("schnell", "быстро"), lessons=9),
    NudgeFacts(name="Анна", streak=2, known=3, in_work=5, lessons=2),
    NudgeFacts(name="Анна", known=24, in_work=30, due=9, word=("gehen", "идти"), lessons=12),
    NudgeFacts(name="Анна", known=1, in_work=1, due=1, lessons=1),
    NudgeFacts(name="Анна", known=24, learned=3, best=5, lessons=12),
    NudgeFacts(name="Анна"),
]
KINDS = ("daily", "back1", "back3", "back7", "back14", "start1", "start3", "start7")


def _all_messages(lang):
    for kind in KINDS:
        for facts in PEOPLE:
            for seed in range(10):
                yield kind, facts, seed, compose(kind, facts, lang, seed)


@pytest.mark.parametrize("lang", sorted(LOCALES))
def test_every_message_is_complete_html(lang):
    for kind, facts, seed, text in _all_messages(lang):
        where = (lang, kind, seed, text[:90])
        assert "{" not in text and "[MISSING" not in text and "[ERROR" not in text, where
        assert text.count("<b>") == text.count("</b>"), where
        assert text.count("<tg-spoiler>") == text.count("</tg-spoiler>"), where
        assert text.startswith("<b>"), where


def test_same_parts_in_every_language():
    ru = {k for k in LOCALES["ru"] if k.startswith("nd_")}
    for lang, texts in LOCALES.items():
        assert {k for k in texts if k.startswith("nd_")} == ru, lang


# Обращение на «ты» — во всех языках только уважительная форма
INFORMAL = {
    "ru": r"\b(ты|тебе|тебя|твой|твоя|твои|твоё|можешь|хочешь|знаешь|помнишь)\b",
    "uk": r"\b(ти|тебе|тобі|твій|твоя|твої|можеш|хочеш|знаєш|пам'ятаєш)\b",
    "de": r"\b(du|dich|dir|dein|deine|deinen|kannst|weißt|hast)\b",
    "pl": r"\b(ty|ciebie|tobie|twój|twoja|twoje|masz|możesz|pamiętasz|wiesz|Pan|Pani|Państwo)\b",
    "tr": r"\b(sen|seni|sana|senin)\b",
}


@pytest.mark.parametrize("lang", sorted(INFORMAL))
def test_formal_address_only(lang):
    pattern = re.compile(INFORMAL[lang], re.IGNORECASE if lang != "pl" else 0)
    for key, text in LOCALES[lang].items():
        if key.startswith("nd_"):
            assert not pattern.search(text), (lang, key, text)


@pytest.mark.parametrize("lang", ["ru", "uk"])
def test_vy_with_capital_letter(lang):
    low = re.compile(r"\b(вы|вас|вам|ваш|ваша|ваши|ваше|ви|вам|ваш|вашу)\b")
    for key, text in LOCALES[lang].items():
        if key.startswith("nd_"):
            assert not low.search(text), (lang, key, text)


@pytest.mark.parametrize("lang", sorted(LOCALES))
def test_no_ai_trail(lang):
    """
    «Меньше ИИ-шлейфа» (владелец): не цепочки тире и не лозунги. В одном
    сообщении — не больше двух тире, в одной строке — не больше одного.
    """
    for kind, facts, seed, text in _all_messages(lang):
        # Владелец 16.10: «без длинных тире, вместо них минус — так человечнее»
        assert "—" not in text, (lang, kind, text)
        assert text.count(" - ") <= 2, (lang, kind, text)
        lines = text.split("\n")
        for line in lines:
            assert line.count(" - ") <= 1, (lang, kind, line)
            # Без точки в конце: «точки визуально сковывают»
            assert not (line.endswith(".") and not line.endswith("...")), (lang, kind, line)
        # Между строками — пустая строка, «чтобы текст дышал»
        assert not any(a and b for a, b in zip(lines, lines[1:])), (lang, kind, text)


def test_heads_do_not_repeat_until_all_were_shown():
    facts = PEOPLE[3]
    heads = [compose("daily", facts, "ru", seed).split("\n")[0] for seed in range(len(variants("nd_streak_head")))]
    assert len(set(heads)) == len(heads), heads


def test_name_is_escaped():
    text = compose("daily", NudgeFacts(name="Tom <3", streak=3, known=5, in_work=5), "ru", 0)
    assert "Tom &lt;3" in text and "Tom <3" not in text


def test_message_speaks_about_the_person():
    """Прежний текст: «Пора позаниматься» + справка о боте. Теперь — его числа и его слово."""
    text = compose("daily", PEOPLE[3], "ru", 0)
    assert "5 дней" in text and ("31" in text or "38" in text) and "schnell" in text
    assert "<tg-spoiler>быстро</tg-spoiler>" in text


# ============================================================================
# ОТПРАВКА — с базой
# ============================================================================

class FakeBot:
    def __init__(self, fail=None, delay=0.0):
        self.sent = []
        self.fail = fail
        self.delay = delay

    async def send_message(self, chat_id, text, **kwargs):
        if self.delay:
            await asyncio.sleep(self.delay)
        if self.fail is not None:
            exc, self.fail = self.fail, None
            raise exc
        self.sent.append((chat_id, text, kwargs.get("reply_markup")))


@pytest.fixture
def own_sessions(engine, monkeypatch):
    import app.database.session as dbs

    maker = async_sessionmaker(engine, expire_on_commit=False)
    monkeypatch.setattr(dbs, "AsyncSessionLocal", maker)
    return maker


async def _person(session, uid, *, played=True, opted=False, last_day=date(2026, 11, 2),
                  name="Анна"):
    user = User(id=uid, first_name=name, interface_language="ru", learning_lang="de",
                native_lang="ru", reverse_mode=False, timezone="Europe/Berlin",
                notifications_enabled=opted, notification_time="20:00",
                created_at=utc(2026, 11, 1, 18, 0), level=CEFRLevel.A1)
    session.add(user)
    if played:
        done = utc(last_day.year, last_day.month, last_day.day, 18, 0)
        user.quizzes_passed = 3
        user.last_active_date = last_day
        user.streak_days = 1
        session.add(QuizSession(user_id=uid, level=CEFRLevel.A1, total_questions=7,
                                answered_questions=7, is_completed=True, local_day=last_day,
                                started_at=done - timedelta(minutes=4), completed_at=done))
    await session.commit()
    return user


async def _log(maker, uid):
    async with maker() as s:
        return [(r.kind, r.outcome) for r in (await s.execute(
            select(NudgeLog).where(NudgeLog.user_id == uid).order_by(NudgeLog.id))).scalars()]


@pytest.mark.asyncio
async def test_back1_goes_once_and_is_logged(session, own_sessions):
    from app.schedulers.nudges import send_nudges

    await _person(session, 5001)
    bot = FakeBot()
    assert await send_nudges(bot, utc(2026, 11, 3, 17, 30)) == {"sent": 1}
    assert await send_nudges(bot, utc(2026, 11, 3, 17, 35)) == {}
    assert len(bot.sent) == 1
    assert await _log(own_sessions, 5001) == [("back1", "sent")]
    data = [b.callback_data for row in bot.sent[0][2].inline_keyboard for b in row]
    assert data[0] == "learn_now:nd_back1" and "notif_off" in data
    assert any(d.startswith("nd_optin:") for d in data)


@pytest.mark.asyncio
async def test_holdout_gets_no_message_but_a_log_row(session, own_sessions):
    from app.schedulers.nudges import send_nudges

    await _person(session, 5000)
    bot = FakeBot()
    assert await send_nudges(bot, utc(2026, 11, 3, 17, 30)) == {"holdout": 1}
    assert bot.sent == []
    assert await _log(own_sessions, 5000) == [("back1", "holdout")]
    # Ступень пройдена — и в контрольной группе лесенка идёт дальше
    assert await send_nudges(bot, utc(2026, 11, 3, 18, 30)) == {}
    assert await send_nudges(bot, utc(2026, 11, 5, 17, 30)) == {"holdout": 1}


@pytest.mark.asyncio
async def test_opted_in_get_daily_even_in_holdout(session, own_sessions):
    from app.schedulers.nudges import send_nudges

    await _person(session, 5000, opted=True)
    bot = FakeBot()
    assert await send_nudges(bot, utc(2026, 11, 3, 20, 1)) == {"sent": 1}
    assert await _log(own_sessions, 5000) == [("daily", "sent")]


@pytest.mark.asyncio
async def test_blocked_bot_is_a_no(session, own_sessions):
    from aiogram.exceptions import TelegramForbiddenError
    from aiogram.methods import SendMessage

    from app.schedulers.nudges import send_nudges

    await _person(session, 5001)
    err = TelegramForbiddenError(method=SendMessage(chat_id=1, text="x"), message="blocked")
    assert await send_nudges(FakeBot(fail=err), utc(2026, 11, 3, 17, 30)) == {"forbidden": 1}
    bot = FakeBot()
    for day in range(4, 20):
        await send_nudges(bot, utc(2026, 11, day, 17, 30))
    assert bot.sent == [], "заблокировавшему писали дальше"


@pytest.mark.asyncio
async def test_network_failure_is_retried_once(session, own_sessions):
    from aiogram.exceptions import TelegramNetworkError
    from aiogram.methods import SendMessage

    from app.schedulers.nudges import send_nudges

    await _person(session, 5001)
    bot = FakeBot(fail=TelegramNetworkError(method=SendMessage(chat_id=1, text="x"), message="timeout"))
    assert await send_nudges(bot, utc(2026, 11, 3, 17, 30)) == {"retry": 1}
    assert await send_nudges(bot, utc(2026, 11, 3, 17, 35)) == {"sent": 1}
    assert await send_nudges(bot, utc(2026, 11, 3, 17, 40)) == {}
    assert len(bot.sent) == 1


@pytest.mark.asyncio
async def test_two_processes_send_once(session, own_sessions):
    from app.schedulers.nudges import send_nudges

    await _person(session, 5001)
    bot = FakeBot(delay=0.05)
    now = utc(2026, 11, 3, 17, 30)
    await asyncio.gather(send_nudges(bot, now), send_nudges(bot, now))
    assert len(bot.sent) == 1


@pytest.mark.asyncio
async def test_never_played_get_invited(session, own_sessions):
    from app.schedulers.nudges import send_nudges

    await _person(session, 5001, played=False)
    bot = FakeBot()
    assert await send_nudges(bot, utc(2026, 11, 2, 17, 30)) == {"sent": 1}
    assert await _log(own_sessions, 5001) == [("start1", "sent")]


@pytest.mark.asyncio
async def test_stop_button_stops_everything(session, own_sessions):
    from app.schedulers.nudges import send_nudges
    from app.testing import make_bot, make_dispatcher, press, reset_state

    user = await _person(session, 5001)
    bot = FakeBot()
    await send_nudges(bot, utc(2026, 11, 3, 17, 30))
    tg_bot, _ = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    await dp.feed_update(tg_bot, press(user.id, "notif_off"))
    for day in range(4, 20):
        await send_nudges(bot, utc(2026, 11, day, 17, 30))
    assert len(bot.sent) == 1, "после «Не присылать» писали дальше"


@pytest.mark.asyncio
async def test_optin_button_turns_reminders_on(session, own_sessions):
    from app.schedulers.nudges import send_nudges
    from app.testing import make_bot, make_dispatcher, press, reset_state

    user = await _person(session, 5001)
    tg_bot, _ = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    await dp.feed_update(tg_bot, press(user.id, "nd_optin:18:00"))
    await session.refresh(user)
    assert user.notifications_enabled and user.notification_time == "18:00"
    bot = FakeBot()
    assert await send_nudges(bot, utc(2026, 11, 3, 18, 1)) == {"sent": 1}
    assert await _log(own_sessions, 5001) == [("daily", "sent")]


@pytest.mark.asyncio
async def test_lesson_from_the_message_is_marked(session, own_sessions):
    from app.bot.handlers.quiz.sources import source_from_callback

    assert source_from_callback("learn_now:nd_back3") == "nd_back3"
    assert source_from_callback("learn_now:nd_bogus") != "nd_bogus"



@pytest.mark.asyncio
async def test_two_processes_send_one_daily(session, own_sessions):
    """Ежедневное напоминание держит только отметка дня — её захват и проверяем."""
    from app.schedulers.nudges import send_nudges

    await _person(session, 5001, opted=True)
    bot = FakeBot(delay=0.05)
    now = utc(2026, 11, 3, 20, 1)
    await asyncio.gather(send_nudges(bot, now), send_nudges(bot, now))
    assert len(bot.sent) == 1


@pytest.mark.asyncio
async def test_report_tells_works_or_harms(session):
    """Отчёт: вернулись, кнопкой, отписались, заблокировали — и контрольная группа рядом."""
    from app.services.nudge_report import nudge_report, share

    sent_at = utc(2026, 11, 3, 18, 0)
    for uid in (6001, 6002, 6003, 6004, 6005, 6006):
        session.add(User(id=uid, first_name="X", interface_language="ru", learning_lang="de",
                         native_lang="ru", reverse_mode=False))
    await session.commit()
    session.add_all([
        NudgeLog(user_id=6001, kind="back1", outcome="sent", sent_at=sent_at),     # вернулся кнопкой
        NudgeLog(user_id=6002, kind="back1", outcome="sent", sent_at=sent_at),     # отписался
        NudgeLog(user_id=6006, kind="back1", outcome="sent", sent_at=sent_at),     # вернулся, но не кнопкой
        QuizSession(user_id=6006, level=CEFRLevel.A1, total_questions=7, answered_questions=7,
                    is_completed=True, start_source="home",
                    started_at=sent_at + timedelta(hours=5), completed_at=sent_at + timedelta(hours=5, minutes=4)),
        NudgeLog(user_id=6003, kind="back1", outcome="forbidden", sent_at=sent_at),
        NudgeLog(user_id=6004, kind="back1", outcome="holdout", sent_at=sent_at),  # вернулся сам
        NudgeLog(user_id=6005, kind="back1", outcome="holdout", sent_at=sent_at),  # не вернулся
        QuizSession(user_id=6001, level=CEFRLevel.A1, total_questions=7, answered_questions=7,
                    is_completed=True, start_source="nd_back1",
                    started_at=sent_at + timedelta(minutes=5), completed_at=sent_at + timedelta(minutes=9)),
        QuizSession(user_id=6004, level=CEFRLevel.A1, total_questions=7, answered_questions=7,
                    is_completed=True, start_source="home",
                    started_at=sent_at + timedelta(hours=3), completed_at=sent_at + timedelta(hours=3, minutes=4)),
        # Через двое суток — уже не «вернулся за сутки»
        QuizSession(user_id=6005, level=CEFRLevel.A1, total_questions=7, answered_questions=7,
                    is_completed=True, started_at=sent_at + timedelta(days=2),
                    completed_at=sent_at + timedelta(days=2, minutes=4)),
    ])
    (await session.get(User, 6002)).reminders_declined_at = sent_at + timedelta(minutes=1)
    await session.commit()

    k = (await nudge_report(session, sent_at + timedelta(days=3))).kinds["back1"]
    assert (k.sent, k.returned, k.via_button, k.stopped, k.blocked) == (3, 2, 1, 1, 1)
    assert (k.holdout, k.holdout_returned) == (2, 1)
    assert share(k.returned, k.sent) == "67%" and share(0, 0) == "—"


def test_huge_backlog_does_not_crush():
    """Живой пример из базы: «Пора освежить 2742 слова» — число не зовёт, а придавливает."""
    facts = NudgeFacts(name="Юрий", known=2743, in_work=2743, due=2742, lessons=198)
    for seed in range(6):
        assert "2742" not in compose("back3", facts, "ru", seed)


def test_yesterday_only_when_it_was_yesterday():
    """Первый день был позавчера — «вчера Вы узнали» было бы неправдой."""
    facts = NudgeFacts(name="Анна", first_day=True, first_day_words=7, known=5, in_work=7, away=2)
    for seed in range(6):
        assert "вчера" not in compose("daily", facts, "ru", seed).lower()
    facts = NudgeFacts(name="Анна", first_day=True, first_day_words=7, known=5, in_work=7, away=1)
    assert any("вчера" in compose("daily", facts, "ru", s).lower() for s in range(6))


@pytest.mark.parametrize("lang", sorted(LOCALES))
def test_no_icons_outside_the_bot_charter(lang):
    """
    Владелец о первой редакции: «сделаны не в стилистике бота. Откуда
    появились все эти смайлики?» Устав (`strip_marks.py`): 🔥 — только в
    похвале в конце занятия, флагов, ▶️ и ⏰ нет нигде. В сообщениях — ни
    одного значка, кроме ✓ в подтверждении.
    """
    import unicodedata

    for key, text in LOCALES[lang].items():
        if not key.startswith("nd_"):
            continue
        icons = {ch for ch in text if unicodedata.category(ch) in ("So", "Sk", "Cs")
                 or 0x1F000 <= ord(ch) <= 0x1FAFF or ch == "️"} - {"✓"}
        assert not icons, (lang, key, icons)
    for kind in KINDS:
        for facts in PEOPLE:
            text = compose(kind, facts, lang, 0)
            assert not any(0x1F000 <= ord(ch) <= 0x1FAFF for ch in text), (lang, kind, text)


@pytest.mark.parametrize("lang", sorted(LOCALES))
def test_no_zero_numbers_in_messages(lang):
    """«Знакомых слов 0, выученных 0» в прощальном письме — насмешка, а не польза."""
    for facts in (NudgeFacts(name="Анна", lessons=1),
                  NudgeFacts(name="Анна", known=25, in_work=25, lessons=2)):
        for kind in ("daily", "back3", "back7", "back14"):
            for seed in range(8):
                text = compose(kind, facts, lang, seed)
                assert not re.search(r"(?<![\d.])0(?![\d:])", text), (lang, kind, text)


def test_minutes_promised_match_the_lesson():
    """
    «Около трёх минут» было неправдой: на проде 15.10 медиана занятия из 15
    вопросов — 3,8 мин, первого (7 вопросов) — 1,7 мин. Обещание считается
    из длины занятия человека.
    """
    first = compose("start7", NudgeFacts(name="Анна", questions=7), "ru", 0)
    assert "около 2 минут" in first, first
    regular = compose("back7", NudgeFacts(name="Анна", questions=15, known=5), "ru", 1)
    assert "около 4 минут" in regular, regular
    for lang in LOCALES:
        for kind in KINDS:
            assert "{minutes_n}" not in compose(kind, NudgeFacts(name="A", questions=15), lang, 0)


# Все сообщения, которые бот присылает сам, — в одном оформлении с
# сообщениями вовлечения (владелец 16.10: «уведомления других типов нужно
# тоже привести к такому внешнему виду»)
OUTGOING_KEYS = ("award_won", "report_approved", "report_approved_audio",
                 "nd_optin_done", "reminder_offer_done", "reminder_offer")


@pytest.mark.parametrize("lang", sorted(LOCALES))
def test_every_outgoing_message_has_the_same_look(lang):
    for key in OUTGOING_KEYS:
        text = LOCALES[lang][key]
        lines = text.split("\n")
        assert "—" not in text, (lang, key, text)
        assert not any(l.endswith(".") and not l.endswith("...") for l in lines), (lang, key, text)
        assert not any(a and b for a, b in zip(lines, lines[1:])), (lang, key, text)
