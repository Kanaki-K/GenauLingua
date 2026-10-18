"""
«Говорю» — не в начале занятия и не тем, кто его раз за разом пропускает (2.2.1).

Прод 14–18.10: показан 78 раз, пропущен 42; одному человеку 23 показа и 21
пропуск. На 1–3 вопросе показан 4 раза — 3 раза человек ушёл на нём.
"""

import pytest
from sqlalchemy import select

from app.bot.handlers.quiz import lesson as LN
from app.bot.handlers.quiz.speech import CB_SPEECH_KEEP, CB_SPEECH_OFF, _skips_in_a_row
from app.core.clock import utcnow
from app.database.enums import QuizChannel
from app.database.models import UserEvent
from app.services.quiz_service import SPEECH_FROM_QUESTION, place_in_round
from app.testing import make_bot, make_dispatcher, press, reset_state, text_update
from tests.test_games_audit_oct14 import LEARN, _words

T, S = QuizChannel.TEXT, QuizChannel.SPEECH


def test_speech_never_lands_on_the_first_three_questions():
    for position in range(1, SPEECH_FROM_QUESTION):
        for _ in range(30):
            got = place_in_round([T, S], enabled=[T, S], recent=["t"] * (position - 1),
                                 round_length=15, position=position)
            assert got is not S, f"голос на вопросе {position}"


def test_speech_is_possible_from_the_fourth_question():
    seen = {place_in_round([T, S], enabled=[T, S], recent=["t", "t", "t"],
                           round_length=15, position=SPEECH_FROM_QUESTION) for _ in range(30)}
    assert S in seen


async def _event(session, user, kind, channel=None):
    session.add(UserEvent(user_id=user.id, at=utcnow(), kind=kind, channel=channel))
    await session.flush()


async def test_offer_after_three_skips_in_a_row_not_after_two(session, user):
    await _event(session, user, "skip", "s")
    await _event(session, user, "skip", "s")
    assert not await _skips_in_a_row(session, user.id)
    await _event(session, user, "skip", "s")
    assert await _skips_in_a_row(session, user.id)


async def test_a_voice_answer_between_skips_resets_the_count(session, user):
    await _event(session, user, "skip", "s")
    await _event(session, user, "skip", "s")
    await _event(session, user, "speech")
    await _event(session, user, "skip", "s")
    assert not await _skips_in_a_row(session, user.id)


async def test_listening_skips_do_not_count(session, user):
    for _ in range(3):
        await _event(session, user, "skip", "a")
    assert not await _skips_in_a_row(session, user.id)


async def test_after_an_offer_the_next_one_waits_for_three_new_skips(session, user):
    for _ in range(3):
        await _event(session, user, "skip", "s")
    await _event(session, user, "speech_offer")
    await _event(session, user, "skip", "s")
    assert not await _skips_in_a_row(session, user.id)


@pytest.fixture
async def stage(session, user):
    await _words(session, user, channels="ts")
    user.onboarded_at = utcnow()
    user.audio_enabled = True
    await session.commit()
    bot, recorder = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    return dp, bot, recorder


def _offer_shown(recorder):
    for name, payload in recorder.calls:
        rows = (payload.get("reply_markup") or {}).get("inline_keyboard") or []
        if name == "SendMessage" and any(b.get("callback_data") == CB_SPEECH_OFF
                                         for row in rows for b in row):
            return True
    return False


async def test_three_skipped_speech_questions_bring_the_offer(session, user, stage, monkeypatch):
    dp, bot, recorder = stage
    original = LN.generate_question

    async def forced(*args, **kwargs):
        kwargs["channel"] = S
        return await original(*args, **kwargs)

    monkeypatch.setattr(LN, "generate_question", forced)
    await dp.feed_update(bot, text_update(user.id, LEARN))
    for n in range(3):
        assert not _offer_shown(recorder), f"предложение раньше третьего пропуска ({n})"
        await dp.feed_update(bot, press(user.id, "speech_skip"))
        await dp.feed_update(bot, press(user.id, "next_question")) if n < 2 else None
    assert _offer_shown(recorder)


async def test_remove_takes_speech_out_of_the_games(session, user, stage):
    dp, bot, recorder = stage
    await dp.feed_update(bot, press(user.id, CB_SPEECH_OFF, message_id=880))
    await session.refresh(user)
    assert "s" not in user.quiz_channels and "t" in user.quiz_channels
    kinds = (await session.execute(select(UserEvent.action).where(
        UserEvent.user_id == user.id, UserEvent.kind == "speech_offer"))).scalars().all()
    assert "off" in kinds


async def test_keep_leaves_the_games_as_they_are(session, user, stage):
    dp, bot, recorder = stage
    before = user.quiz_channels
    await dp.feed_update(bot, press(user.id, CB_SPEECH_KEEP, message_id=881))
    await session.refresh(user)
    assert user.quiz_channels == before
    deleted = {p["message_id"] for n, p in recorder.calls if n == "DeleteMessage"}
    assert 881 in deleted


def test_remove_question_not_more_often_than_every_two_weeks():
    from datetime import timedelta
    from types import SimpleNamespace

    from app.bot.handlers.quiz.speech import ASK_OFF_AGAIN_DAYS, _may_ask_again

    assert _may_ask_again(SimpleNamespace(speech_asked_at=None))
    assert not _may_ask_again(SimpleNamespace(speech_asked_at=utcnow() - timedelta(days=3)))
    assert _may_ask_again(SimpleNamespace(
        speech_asked_at=utcnow() - timedelta(days=ASK_OFF_AGAIN_DAYS + 1)))
