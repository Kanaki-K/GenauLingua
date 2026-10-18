# -*- coding: utf-8 -*-
"""
«Повторить ошибки» на итоге, когда состояния занятия уже нет — аудит 2.1.

Redis хранит состояние 2 дня; вернувшийся через 3 дня к кнопке на старом
итоге слышал «✓ У Вас не было ошибок!», хотя ошибки были. Теперь ошибки
берутся из базы — из последнего законченного занятия.
"""
import pytest
from sqlalchemy import select

from app.database.models import QuizSession
from app.locales import get_text
from app.testing import make_bot, make_dispatcher, press, reset_state, text_update
from tests.test_scenarios import ROUND_LENGTH, _ready, _wrong_answer

pytestmark = pytest.mark.asyncio


async def test_repeat_errors_after_state_expired_repeats_them(session, user):
    bot, recorder = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    await _ready(session, user)

    await dp.feed_update(bot, text_update(user.id, get_text("btn_learn_words", "ru")))
    for _ in range(ROUND_LENGTH):
        await dp.feed_update(bot, press(user.id, await _wrong_answer(dp, bot, user.id, recorder)))
        await dp.feed_update(bot, press(user.id, "next_question"))
    assert "repeat_errors" in recorder.all_buttons()

    # Прошло 3 дня: состояние истекло (как сделал бы TTL Redis)
    await dp.fsm.get_context(bot, chat_id=user.id, user_id=user.id).clear()
    await reset_state(dp)

    recorder.clear()
    await dp.feed_update(bot, press(user.id, "repeat_errors", message_id=900))
    assert get_text("quiz_no_errors", "ru") not in recorder.sent_texts(), \
        "после истечения состояния бот говорит «не было ошибок», хотя они были"
    repeat = (await session.execute(select(QuizSession).where(
        QuizSession.user_id == user.id, QuizSession.quiz_mode == "error_repeat"))).scalars().all()
    assert repeat, "повтор ошибок не начался"
