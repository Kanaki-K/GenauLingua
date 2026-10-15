# -*- coding: utf-8 -*-
"""
Очерёдность нажатий одного человека (SimpleEventIsolation) и журнал
медленных нажатий — аудит 2.1. Журнал прежде стоял ВНУТРИ замка очереди и
не видел ожидания в ней (тест «ожидание в журнале» падал до починки).
"""
import asyncio
import logging
import os
import time

import pytest
from aiogram import Dispatcher, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import SimpleEventIsolation

from app.bot.fsm_storage import make_storage
from app.bot.slow_log import SLOW_MS, install_slow_log
from app.testing import make_bot, text_update

pytestmark = pytest.mark.asyncio
REDIS = os.environ.get("FSM_TEST_REDIS_URL")
LOGGER = "app.main"

SLOW_S = SLOW_MS / 1000 + 0.3


def _dispatcher(storage):
    dp = Dispatcher(storage=storage, events_isolation=SimpleEventIsolation())
    router = Router()

    @router.message(F.text == "slow")
    async def slow(message, state: FSMContext):
        await state.update_data(slow_done=True, seen=[1, 2])
        await asyncio.sleep(SLOW_S)

    @router.message(F.text == "fast")
    async def fast(message, state: FSMContext):
        data = await state.get_data()
        await state.update_data(fast_saw_slow=bool(data.get("slow_done")))

    @router.message(F.text == "boom")
    async def boom(message):
        await asyncio.sleep(SLOW_S)
        raise RuntimeError("упал")

    dp.include_router(router)

    install_slow_log(dp)   # как в app/main.py

    return dp


async def test_lock_wait_is_in_slow_log(caplog):
    """Второе нажатие ~1.8 с стоит в очереди за первым — журнал пишет оба."""
    dp = _dispatcher(make_storage(None))
    bot, _ = make_bot()
    caplog.set_level(logging.WARNING, logger=LOGGER)

    first = asyncio.create_task(dp.feed_update(bot, text_update(77001, "slow")))
    await asyncio.sleep(0.05)
    started_second = time.perf_counter()
    await dp.feed_update(bot, text_update(77001, "fast"))
    waited = time.perf_counter() - started_second
    await first
    lines = [r.getMessage() for r in caplog.records if r.name == LOGGER and "медленно" in r.getMessage()]
    print(f"\nвторое нажатие ждало {waited*1000:.0f} мс; журнал: {lines}")
    assert waited * 1000 >= SLOW_MS, "очередь не держала второе нажатие (проверка не о том)"
    assert len(lines) == 2, (
        f"второе нажатие человек ждал {waited*1000:.0f} мс, а журнал его не записал: {lines}")


async def test_other_chats_are_not_blocked():
    dp = _dispatcher(make_storage(None))
    bot, _ = make_bot()
    first = asyncio.create_task(dp.feed_update(bot, text_update(77002, "slow")))
    await asyncio.sleep(0.05)
    t = time.perf_counter()
    await dp.feed_update(bot, text_update(77003, "fast"))
    other = time.perf_counter() - t
    await first
    assert other < 0.5, f"чужой чат ждал {other:.2f} с"


@pytest.mark.skipif(not REDIS, reason="нужен Redis")
async def test_same_user_serialized_on_redis_no_lost_update():
    storage = make_storage(REDIS)
    await storage.redis.flushdb()
    try:
        dp = _dispatcher(storage)
        bot, _ = make_bot()
        first = asyncio.create_task(dp.feed_update(bot, text_update(77004, "slow")))
        await asyncio.sleep(0.05)
        await asyncio.wait_for(dp.feed_update(bot, text_update(77004, "fast")), 10)
        await first
        ctx = dp.fsm.get_context(bot, chat_id=77004, user_id=77004)
        data = await ctx.get_data()
        assert data == {"slow_done": True, "seen": [1, 2], "fast_saw_slow": True}, data
        # TTL поставлен на данные
        ttl = await storage.redis.ttl(storage.key_builder.build(ctx.key, "data"))
        assert 0 < ttl <= 2 * 86400, ttl
    finally:
        await storage.redis.flushdb()
        await storage.close()


async def test_slow_log_on_exception_logs_and_reraises(caplog):
    dp = _dispatcher(make_storage(None))
    bot, _ = make_bot()
    caplog.set_level(logging.WARNING, logger=LOGGER)
    with pytest.raises(RuntimeError):
        await dp.feed_update(bot, text_update(77005, "boom"))
    lines = [r.getMessage() for r in caplog.records if r.name == LOGGER and "медленно" in r.getMessage()]
    assert len(lines) == 1 and lines[0].endswith(": сообщение"), lines
