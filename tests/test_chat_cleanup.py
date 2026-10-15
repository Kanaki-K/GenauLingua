# -*- coding: utf-8 -*-
"""
ЗАЧИСТКА ЧАТА: от прежнего якоря до нажатия — всё, даже после длинного занятия.

Прод, 15.10: у владельца рассылка и рейтинг остались в чате, хотя он нажимал
меню. Проба показала: живое сообщение на 352 номера ниже якоря, а удаление
брало только последние 100 номеров. Одно занятие расходует их больше сотни —
каждая карточка отправляется и удаляется, — и всё, что было до занятия,
оказывалось за пределом навсегда.
"""
import pytest

from app.bot.utils import delete_messages_fast
from tests.scenario import make_bot

pytestmark = pytest.mark.asyncio


def _deleted(recorder):
    return {p["message_id"] for n, p in recorder.calls if n == "DeleteMessage"}


async def test_old_messages_after_a_long_lesson_are_removed():
    """Якорь 10, нажатие 362 — как у владельца. Уходит всё, начиная с якоря."""
    bot, rec = make_bot()

    await delete_messages_fast(bot, 1, 10, 362)

    assert _deleted(rec) == set(range(10, 362)), (
        f"не удалены: {sorted(set(range(10, 362)) - _deleted(rec))[:10]}"
    )


async def test_pressed_message_and_newer_are_untouched():
    """Конец диапазона не включается: нажатие и новый экран удаляются не здесь."""
    bot, rec = make_bot()

    await delete_messages_fast(bot, 1, 100, 105)

    assert _deleted(rec) == {100, 101, 102, 103, 104}
