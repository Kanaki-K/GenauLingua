# -*- coding: utf-8 -*-
"""
ЗАНЯТИЕ ПЕРЕЖИВАЕТ ПЕРЕЗАПУСК БОТА (патч 2.1, пункт 1).

15.10.2026 перезапуски при выкатке дважды оборвали людям занятия: в памяти
состояние умирало вместе с процессом. С Redis новый процесс продолжает с
того же вопроса.

Нужен живой Redis: FSM_TEST_REDIS_URL=redis://localhost:6380/2. Без него
тест пропускается — на машине без Redis проверять нечего.
"""
import os

import pytest
from aiogram import Dispatcher

from app.bot.fsm_storage import make_storage
from app.locales import get_text
from app.testing import make_bot, make_dispatcher, press, text_update
from tests.test_scenarios import _ready

pytestmark = pytest.mark.asyncio

REDIS = os.environ.get("FSM_TEST_REDIS_URL")


def _restart(dp: Dispatcher) -> None:
    """
    «Перезапуск»: новое подключение к тому же Redis вместо прежнего.

    Роутеры подключаются к диспетчеру один раз на процесс, поэтому второй
    диспетчер здесь не собрать; но всё, что переживает перезапуск, живёт в
    хранилище — его и меняем на свежее, без единого байта в памяти.
    """
    dp.fsm.storage = make_storage(REDIS)


@pytest.mark.skipif(not REDIS, reason="нужен Redis: FSM_TEST_REDIS_URL")
async def test_lesson_continues_after_restart(session, user):
    await _ready(session, user)
    dp = make_dispatcher(session)
    previous = dp.fsm.storage
    dp.fsm.storage = make_storage(REDIS)
    await dp.fsm.storage.redis.flushdb()
    bot, rec = make_bot()

    await dp.feed_update(bot, text_update(user.id, get_text("btn_learn_words", "ru")))
    ctx = dp.fsm.get_context(bot, chat_id=user.id, user_id=user.id)
    before = await ctx.get_data()
    assert before.get("session_id"), "занятие не началось"
    await dp.fsm.storage.close()

    _restart(dp)
    second = dp
    ctx2 = second.fsm.get_context(bot, chat_id=user.id, user_id=user.id)
    after = await ctx2.get_data()
    assert after == before, "состояние занятия не пережило перезапуск"
    assert await ctx2.get_state() is not None

    rec.clear()
    await second.feed_update(bot, press(user.id, f"answer_{after['correct_word_id']}"))
    sent = [n for n, _ in rec.calls]
    assert any(n in ("EditMessageText", "EditMessageMedia", "SendMessage", "SendAudio") for n in sent), (
        f"после перезапуска ответ не принят: {sent}"
    )
    data = await ctx2.get_data()
    assert data.get("correct_answers") == 1, "ответ после перезапуска не засчитан"
    await second.fsm.storage.redis.flushdb()
    await second.fsm.storage.close()
    dp.fsm.storage = previous
