"""
«Говорю» — по желанию (2.2.1, владелец 18.10).

Игра не приходит сама: под итогом занятия, когда есть слово, готовое для
«Говорю», бот один раз предлагает попробовать. «Не сейчас» — через неделю.
Включил или убрал сам (настройки, кнопка 🎤 главного экрана) — это выбор.
Согласившемуся после трёх пропусков подряд — «убрать?», не чаще раза в две недели.
"""
from datetime import timedelta
from types import SimpleNamespace

import pytest

from app.bot.handlers.quiz import summary as SM
from app.bot.handlers.quiz.speech_invite import CB_LATER, CB_TRY, should_invite
from app.core.clock import utcnow
from app.database.enums import QuizChannel
from app.database.models import UserWord
from app.services.quiz_service import enabled_channels
from app.testing import make_bot, make_dispatcher, press, reset_state
from tests.test_games_audit_oct14 import _words

S = QuizChannel.SPEECH


def _user(choice, channels="tasrb", audio=True):
    return SimpleNamespace(quiz_channels=channels, audio_enabled=audio, speech_choice=choice)


def test_speech_only_for_those_who_agreed():
    assert S not in enabled_channels(_user(None))
    assert S not in enabled_channels(_user("later"))
    assert S not in enabled_channels(_user("off"))
    assert S in enabled_channels(_user("on"))


def test_tools_without_the_field_keep_speech():
    assert S in enabled_channels(SimpleNamespace(quiz_channels="tasrb", audio_enabled=True))


@pytest.fixture
async def ready(session, user):
    """Человек ещё не выбирал, два занятия позади, одно слово готово говорить."""
    words = await _words(session, user, n=6, channels="tasrb")
    user.speech_choice = None
    user.quizzes_passed = 2
    user.audio_enabled = True
    session.add(UserWord(user_id=user.id, word_id=words[0].id, learning_lang="de",
                         times_shown=3, times_correct=2, correct_streak=2))
    await session.commit()
    return user


async def test_invite_when_ready(session, ready):
    assert await should_invite(session, ready)


async def test_no_invite_too_early_or_without_a_ready_word(session, ready):
    ready.quizzes_passed = 1
    assert not await should_invite(session, ready)
    ready.quizzes_passed = 2
    ready.audio_enabled = False
    assert not await should_invite(session, ready)


async def test_not_now_waits_a_week(session, ready):
    ready.speech_choice = "later"
    ready.speech_asked_at = utcnow() - timedelta(days=3)
    assert not await should_invite(session, ready)
    ready.speech_asked_at = utcnow() - timedelta(days=8)
    assert await should_invite(session, ready)


async def test_decided_people_are_not_asked(session, ready):
    for choice in ("on", "off"):
        ready.speech_choice = choice
        assert not await should_invite(session, ready)


class _Bot:
    def __init__(self):
        self.sent = []

    async def send_message(self, chat_id, text, **kw):
        self.sent.append((text, kw.get("reply_markup")))


async def test_the_invite_comes_after_the_lesson_when_no_level_offer(session, ready, monkeypatch):
    async def none(*_a, **_k):
        return None

    monkeypatch.setattr(SM, "should_offer_next_level", none)
    monkeypatch.setattr(SM, "should_offer_lower_level", none)
    bot = _Bot()
    callback = SimpleNamespace(bot=bot, message=SimpleNamespace(chat=SimpleNamespace(id=ready.id)))
    await SM._offer_what_fits(callback, session, ready, "ru")
    (text, markup), = bot.sent
    assert "🎤" in text
    assert [b.callback_data for row in markup.inline_keyboard for b in row] == [CB_TRY, CB_LATER]
    assert ready.speech_asked_at is not None


async def test_try_turns_speech_on_and_later_waits(session, ready):
    bot, _ = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    ready.quiz_channels = "tarb"
    await session.commit()
    await dp.feed_update(bot, press(ready.id, CB_TRY, message_id=900))
    await session.refresh(ready)
    assert ready.speech_choice == "on" and "s" in ready.quiz_channels
    assert S in enabled_channels(ready)

    ready.speech_choice = None
    await session.commit()
    await dp.feed_update(bot, press(ready.id, CB_LATER, message_id=901))
    await session.refresh(ready)
    assert ready.speech_choice == "later" and ready.speech_asked_at is not None
    assert S not in enabled_channels(ready)


async def test_settings_toggle_is_a_choice(session, ready):
    bot, _ = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    await dp.feed_update(bot, press(ready.id, "channel_toggle_s", message_id=902))
    await session.refresh(ready)
    assert ready.speech_choice == "on"
    await dp.feed_update(bot, press(ready.id, "channel_toggle_s", message_id=903))
    await session.refresh(ready)
    assert ready.speech_choice == "off"


async def test_an_unanswered_invite_waits_a_week_too(session, ready):
    # Прод 18.10: 3 приглашения двоим — без ответа выбор пуст, и бот звал снова
    ready.speech_choice = None
    ready.speech_asked_at = utcnow() - timedelta(hours=1)
    assert not await should_invite(session, ready)
    ready.speech_asked_at = utcnow() - timedelta(days=8)
    assert await should_invite(session, ready)
