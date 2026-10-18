# -*- coding: utf-8 -*-
"""
Остановка бота дожидается начатых ответов (аудит 2.1).

С 2.1 состояние занятия в Redis переживает процесс, и ответ, оборванный
выкаткой посреди распознавания, запирал вопрос. `app.main._wait_in_flight`
висит на `dp.shutdown` — до того, как aiogram закроет соединение с Telegram.
"""
import asyncio

import pytest
from aiogram import Dispatcher

pytestmark = pytest.mark.asyncio


async def test_shutdown_waits_for_a_handler_in_flight():
    from app.main import waiter_for

    dp = Dispatcher()
    dp.shutdown.register(waiter_for(dp))
    finished = []

    async def slow_answer():
        await asyncio.sleep(0.3)
        finished.append(True)

    task = asyncio.create_task(slow_answer())
    dp._handle_update_tasks.add(task)
    await dp.emit_shutdown()
    assert finished == [True], "остановка не дождалась ответа в пути"
