# -*- coding: utf-8 -*-
"""
Перезапуск ПОСРЕДИ обработки ответа — аудит 2.1 (до починки падали все три).

Ответ занимает вопрос (`answered_question`) ДО долгой работы: распознавания
голосового, записи в базу, показа разбора. Если процесс убит в этот момент
(выкатка: aiogram не ждёт задач обработчиков, asyncio.run их отменяет;
CancelledError не ловится `except Exception`), отметка остаётся в Redis
навсегда (до TTL 2 дня). Новый процесс видит «уже отвечено» и молча гасит
и новое голосовое, и «Пропустить», и повторное нажатие варианта.

До 2.1 состояние умирало с процессом, и человек видел «занятие прервалось».
"""
import asyncio
import os

import pytest
from sqlalchemy import select

from app.bot.fsm_storage import make_storage
from app.bot.handlers.quiz import lesson as LN
from app.bot.handlers.quiz import speech as SP
from app.database.enums import QuizChannel
from app.database.models import QuizQuestion
from app.services import speech_check as sc
from app.testing import make_bot, make_dispatcher, press, reset_state, text_update
from app.testing.telegram import voice_update
from tests.test_games_audit_oct14 import LEARN, _words

pytestmark = pytest.mark.asyncio
REDIS = os.environ.get("FSM_TEST_REDIS_URL")
need_redis = pytest.mark.skipif(not REDIS, reason="нужен Redis: FSM_TEST_REDIS_URL")


@pytest.fixture
async def stage(session):
    bot, recorder = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    return dp, bot, recorder


def _ctx(dp, bot, user):
    return dp.fsm.get_context(bot, chat_id=user.id, user_id=user.id)


async def _restart(dp, monkeypatch):
    # Новый процесс — новый BOOT: отметки прежнего становятся «чужими»
    from app.bot.handlers.quiz import lesson_state

    monkeypatch.setattr(lesson_state, "BOOT", "restarted-" + lesson_state.BOOT)
    await dp.fsm.storage.close()
    dp.fsm.storage = make_storage(REDIS)


class _Downloaded:
    def read(self):
        return b"x"


async def _download(*_a, **_k):
    return _Downloaded()


def _visible(recorder):
    return [n for n, _ in recorder.calls
            if n in ("EditMessageText", "EditMessageMedia", "EditMessageCaption",
                     "SendMessage", "SendAudio", "SendPhoto", "DeleteMessage")]


@need_redis
async def test_restart_during_voice_recognition_does_not_lock_the_question(
        session, user, stage, monkeypatch):
    dp, bot, recorder = stage
    previous = dp.fsm.storage
    await _words(session, user, channels="ts")
    original = LN.generate_question

    async def forced(*args, **kwargs):
        kwargs["channel"] = QuizChannel.SPEECH
        return await original(*args, **kwargs)

    monkeypatch.setattr(LN, "generate_question", forced)
    monkeypatch.setattr(bot, "download", _download, raising=False)

    await dp.feed_update(bot, text_update(user.id, LEARN))
    data = await _ctx(dp, bot, user).get_data()
    assert data["channel"] == QuizChannel.SPEECH.value
    session_id = data["session_id"]

    # Выкатка во время распознавания: задача обработчика отменена
    async def killed(*_a, **_k):
        raise asyncio.CancelledError()

    monkeypatch.setattr(SP, "check_pronunciation", killed)
    with pytest.raises(asyncio.CancelledError):
        await dp.feed_update(bot, voice_update(user.id))

    await _restart(dp, monkeypatch)
    try:
        after = await _ctx(dp, bot, user).get_data()
        print("\nсостояние после перезапуска:",
              {k: after.get(k) for k in ("current_question", "answered_question")})

        # Новый процесс: человек записывает голосовое ещё раз — верное
        async def judge(_audio, target, _lang):
            return sc.SpeechVerdict(heard=target, matched=True, similarity=1.0)

        monkeypatch.setattr(SP, "check_pronunciation", judge)
        recorder.clear()
        await dp.feed_update(bot, voice_update(user.id))
        voice_reaction = _visible(recorder)
        recorded = (await session.execute(select(QuizQuestion).where(
            QuizQuestion.session_id == session_id))).scalars().all()

        # …и жмёт «Пропустить» на уже отвеченном вопросе
        recorder.clear()
        await dp.feed_update(bot, press(user.id, "speech_skip"))
        skip_reaction = _visible(recorder)
        print("реакция на голосовое:", voice_reaction, "записей ответа:", len(recorded))
        print("реакция на «Пропустить»:", skip_reaction)

        assert recorded, "верное голосовое после перезапуска не засчитано — вопрос застрял"
        # Ответ уже засчитан — «Пропустить» на этот вопрос второго ответа не даёт
        assert len(recorded) == 1
    finally:
        await dp.fsm.storage.redis.flushdb()
        await dp.fsm.storage.close()
        dp.fsm.storage = previous


@need_redis
async def test_restart_after_card_answer_commit_does_not_lock_the_question(
        session, user, stage, monkeypatch):
    """Карточка: процесс убит между записью ответа в базу и показом разбора."""
    dp, bot, recorder = stage
    previous = dp.fsm.storage
    await _words(session, user, channels="t")
    await dp.feed_update(bot, text_update(user.id, LEARN))
    data = await _ctx(dp, bot, user).get_data()
    word_id = data["correct_word_id"]

    async def killed(*_a, **_k):
        raise asyncio.CancelledError()

    monkeypatch.setattr(LN, "update_word_progress", killed)
    with pytest.raises(asyncio.CancelledError):
        await dp.feed_update(bot, press(user.id, f"answer_{word_id}"))
    monkeypatch.undo()

    await _restart(dp, monkeypatch)
    try:
        recorder.clear()
        # Карточка с вариантами всё ещё на экране: человек жмёт снова
        await dp.feed_update(bot, press(user.id, f"answer_{word_id}"))
        again = _visible(recorder)
        recorder.clear()
        await dp.feed_update(bot, press(user.id, "next_question"))
        nxt = _visible(recorder)
        print("\nповторное нажатие:", again, "| «Далее» (кнопки на экране нет):", nxt)
        assert again, "после перезапуска нажатие варианта молча погашено — разбора и «Далее» нет"
        assert nxt, "«Далее» после восстановления не сработало"
        answers = (await session.execute(select(QuizQuestion).where(
            QuizQuestion.word_id == word_id))).scalars().all()
        assert len(answers) == 1, f"ответ записан дважды: {len(answers)}"
    finally:
        await dp.fsm.storage.redis.flushdb()
        await dp.fsm.storage.close()
        dp.fsm.storage = previous


@need_redis
async def test_restart_during_next_question_keeps_next_working(
        session, user, stage, monkeypatch):
    """«Далее»: процесс убит после отметки «продвинуто», до нового вопроса."""
    dp, bot, recorder = stage
    previous = dp.fsm.storage
    await _words(session, user, channels="t")
    await dp.feed_update(bot, text_update(user.id, LEARN))
    data = await _ctx(dp, bot, user).get_data()
    await dp.feed_update(bot, press(user.id, f"answer_{data['correct_word_id']}"))

    async def killed(*_a, **_k):
        raise asyncio.CancelledError()

    monkeypatch.setattr(LN, "generate_question", killed)
    with pytest.raises(asyncio.CancelledError):
        await dp.feed_update(bot, press(user.id, "next_question"))
    monkeypatch.undo()

    await _restart(dp, monkeypatch)
    try:
        recorder.clear()
        await dp.feed_update(bot, press(user.id, "next_question"))
        reaction = _visible(recorder)
        state = await _ctx(dp, bot, user).get_data()
        print("\n«Далее» после перезапуска:", reaction,
              {k: state.get(k) for k in ("current_question", "advanced_from")})
        assert reaction, "«Далее» на экране разбора после перезапуска молча погашено"
    finally:
        await dp.fsm.storage.redis.flushdb()
        await dp.fsm.storage.close()
        dp.fsm.storage = previous


@need_redis
async def test_restart_before_card_answer_is_written_accepts_the_answer(
        session, user, stage, monkeypatch):
    """Карточка: процесс убит после отметки «принят», ДО записи в базу — ответ не потерян."""
    from app.bot.handlers.quiz import choice as CH

    dp, bot, recorder = stage
    previous = dp.fsm.storage
    await _words(session, user, channels="t")
    await dp.feed_update(bot, text_update(user.id, LEARN))
    data = await _ctx(dp, bot, user).get_data()
    word_id = data["correct_word_id"]

    async def killed(*_a, **_k):
        raise asyncio.CancelledError()

    monkeypatch.setattr(CH, "_record_answer", killed)
    with pytest.raises(asyncio.CancelledError):
        await dp.feed_update(bot, press(user.id, f"answer_{word_id}"))
    monkeypatch.undo()

    await _restart(dp, monkeypatch)
    try:
        await dp.feed_update(bot, press(user.id, f"answer_{word_id}"))
        answers = (await session.execute(select(QuizQuestion).where(
            QuizQuestion.word_id == word_id))).scalars().all()
        assert len(answers) == 1, "ответ после перезапуска погашен как повтор — вопрос застрял"
    finally:
        await dp.fsm.storage.redis.flushdb()
        await dp.fsm.storage.close()
        dp.fsm.storage = previous
