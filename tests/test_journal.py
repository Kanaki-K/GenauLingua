# -*- coding: utf-8 -*-
"""
Журнал пути человека (`UserEvent`, патч 2.1).

Владелец 16.10: «мы должны иметь возможность разбирать весь путь, чтобы
быть лучше после анализа»; «записывать попытки про голосовое — это важно».
Разбор 15.10 не смог узнать ни что нажимал польский новичок перед уходом,
ни с какой попытки распознан голос: этого бот не писал.
"""
import pytest
from sqlalchemy import select

from app.bot.handlers.quiz import lesson as LN
from app.bot.handlers.quiz import speech as SP
from app.database.enums import QuizChannel
from app.database.models import UserEvent
from app.services import speech_check as sc
from app.testing import make_bot, make_dispatcher, press, reset_state, text_update
from app.testing.telegram import voice_update
from tests.test_games_audit_oct14 import LEARN, _words

pytestmark = pytest.mark.asyncio


class _Downloaded:
    def read(self):
        return b"x"


async def _download(*_a, **_k):
    return _Downloaded()


async def _events(session, user_id, kind=None):
    query = select(UserEvent).where(UserEvent.user_id == user_id).order_by(UserEvent.id)
    if kind:
        query = query.where(UserEvent.kind == kind)
    return (await session.execute(query)).scalars().all()


async def test_lesson_leaves_taps_and_questions(session, user):
    bot, _ = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    await _words(session, user, channels="t")

    await dp.feed_update(bot, text_update(user.id, LEARN))
    data = await dp.fsm.get_context(bot, chat_id=user.id, user_id=user.id).get_data()
    await dp.feed_update(bot, press(user.id, f"answer_{data['correct_word_id']}"))
    await dp.feed_update(bot, press(user.id, "next_question"))

    events = await _events(session, user.id)
    kinds = [e.kind for e in events]
    assert kinds.count("question") == 2, kinds
    assert "msg" in kinds and kinds.count("tap") == 2, kinds
    first_q = next(e for e in events if e.kind == "question")
    assert first_q.word_id == data["correct_word_id"] and first_q.data["n"] == 1
    assert first_q.session_id == data["session_id"]
    taps = [e for e in events if e.kind == "tap"]
    assert all(e.ms is not None and e.action.startswith("кнопка") for e in taps), taps
    # Текста людей в журнале нет: у нажатия — только вид действия
    assert all("_" not in e.action or not any(c.isdigit() for c in e.action) for e in taps)


async def test_every_voice_attempt_is_recorded(session, user, monkeypatch):
    """Не разобрал → неверно (повторите) → верно: три записи с номерами попыток."""
    bot, _ = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    await _words(session, user, channels="ts")
    original = LN.generate_question

    async def forced(*args, **kwargs):
        kwargs["channel"] = QuizChannel.SPEECH
        return await original(*args, **kwargs)

    monkeypatch.setattr(LN, "generate_question", forced)
    monkeypatch.setattr(bot, "download", _download, raising=False)
    await dp.feed_update(bot, text_update(user.id, LEARN))

    verdicts = iter([
        sc.SpeechVerdict(heard="", matched=False, similarity=0.0, failed=True),
        sc.SpeechVerdict(heard="Dietze und Tonk", matched=False, similarity=0.31),
    ])

    async def judge(_audio, target, _lang):
        return next(verdicts, sc.SpeechVerdict(heard=target, matched=True, similarity=1.0))

    monkeypatch.setattr(SP, "check_pronunciation", judge)
    for _ in range(3):
        await dp.feed_update(bot, voice_update(user.id))

    speech = await _events(session, user.id, "speech")
    assert [(e.action, e.data["attempt"]) for e in speech] == [
        ("not_understood", 1), ("retry", 1), ("matched", 2)], [(e.action, e.data) for e in speech]
    assert speech[1].data["heard"] == "Dietze und Tonk" and speech[1].data["similarity"] == 0.31
    assert all(e.word_id and e.session_id and "recognize_s" in e.data for e in speech)


async def test_give_up_and_skip_are_recorded(session, user, monkeypatch):
    bot, _ = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    await _words(session, user, channels="ts")
    original = LN.generate_question

    async def forced(*args, **kwargs):
        kwargs["channel"] = QuizChannel.SPEECH
        return await original(*args, **kwargs)

    monkeypatch.setattr(LN, "generate_question", forced)
    monkeypatch.setattr(bot, "download", _download, raising=False)

    async def wrong(_audio, target, _lang):
        return sc.SpeechVerdict(heard="nein", matched=False, similarity=0.2)

    monkeypatch.setattr(SP, "check_pronunciation", wrong)
    await dp.feed_update(bot, text_update(user.id, LEARN))
    await dp.feed_update(bot, voice_update(user.id))
    await dp.feed_update(bot, voice_update(user.id))
    assert [e.action for e in await _events(session, user.id, "speech")] == ["retry", "give_up"]

    await dp.feed_update(bot, press(user.id, "next_question"))
    await dp.feed_update(bot, press(user.id, "speech_skip"))
    skips = await _events(session, user.id, "skip")
    assert len(skips) == 1 and skips[0].action == "speech_skip" and skips[0].channel == "s"


async def test_journey_script_prints_the_path(session, user):
    """`app.scripts.journey` собирает путь по порядку."""
    from datetime import timedelta

    from app.core.clock import utcnow
    from app.scripts.journey import day_bounds, journey

    bot, _ = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    await _words(session, user, channels="t")
    await dp.feed_update(bot, text_update(user.id, LEARN))
    data = await dp.fsm.get_context(bot, chat_id=user.id, user_id=user.id).get_data()
    await dp.feed_update(bot, press(user.id, f"answer_{data['correct_word_id']}"))

    today = utcnow().date()
    start, _ = day_bounds(today - timedelta(days=1))
    _, end = day_bounds(today + timedelta(days=1))
    lines = await journey(session, user.id, start, end)
    text = "\n".join(lines)
    assert "ЗАНЯТИЕ  начато" in text and "вопрос 1/" in text and "ОТВЕТ    ✓" in text, text
