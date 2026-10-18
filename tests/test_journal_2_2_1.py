"""
Журнал пути, 2.2.1: блокировка бота, ошибки, начало и конец занятия.

Разбор прода 18.10 упирался в то, чего бот не писал: когда человек ушёл
(блокировку было видно только по недошедшему сообщению), кто наткнулся на
сбой, какой дверью и сколько шло занятие.
"""
from datetime import datetime, timezone

from aiogram.types import Chat, ChatMemberBanned, ChatMemberMember, ChatMemberUpdated, Update
from aiogram.types import User as TgUser
from sqlalchemy import select

from app.core.clock import utcnow
from app.database.models import UserEvent
from app.services.journal import journal_error
from app.testing import make_bot, make_dispatcher, press, reset_state, text_update
from tests.test_games_audit_oct14 import LEARN, _words


async def _events(session, user, kind):
    return (await session.execute(
        select(UserEvent).where(UserEvent.user_id == user.id, UserEvent.kind == kind)
        .order_by(UserEvent.id)
    )).scalars().all()


def _status(user_id, before, after):
    tg = TgUser(id=user_id, is_bot=False, first_name="Т")
    bot_user = TgUser(id=1, is_bot=True, first_name="bot")
    when = datetime.now(timezone.utc)
    old = ChatMemberMember(user=bot_user) if before == "member" else ChatMemberBanned(user=bot_user, until_date=0)
    new = ChatMemberMember(user=bot_user) if after == "member" else ChatMemberBanned(user=bot_user, until_date=0)
    return Update(update_id=91, my_chat_member=ChatMemberUpdated(
        chat=Chat(id=user_id, type="private"), from_user=tg, date=when,
        old_chat_member=old, new_chat_member=new))


async def test_blocking_and_coming_back_are_written(session, user):
    bot, _ = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    await dp.feed_update(bot, _status(user.id, "member", "kicked"))
    await dp.feed_update(bot, _status(user.id, "kicked", "member"))
    assert [e.action for e in await _events(session, user, "chat")] == ["blocked", "unblocked"]


class _Event:
    def __init__(self, update, exc):
        self.update, self.exception = update, exc


async def test_an_unhandled_error_is_written_with_kind_and_place(session, user):
    from contextlib import asynccontextmanager

    @asynccontextmanager
    async def same_session():
        yield session

    await journal_error(_Event(press(user.id, "answer_77"), KeyError("x")), session_factory=same_session)
    (event,) = await _events(session, user, "error")
    assert event.action == "KeyError"
    assert event.data == {"where": "кнопка answer"}


async def test_lesson_start_and_finish_are_written(session, user):
    await _words(session, user)
    user.onboarded_at = utcnow()
    await session.commit()
    bot, _ = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    ctx = dp.fsm.get_context(bot, chat_id=user.id, user_id=user.id)

    await dp.feed_update(bot, text_update(user.id, LEARN))
    for _ in range(20):
        data = await ctx.get_data()
        if data.get("current_question", 99) > 15 or not data.get("session_id"):
            break
        await dp.feed_update(bot, press(user.id, f"answer_{data['correct_word_id']}"))
        await dp.feed_update(bot, press(user.id, "next_question"))

    started, finished = await _events(session, user, "lesson")
    assert started.action == "started" and started.data["source"] == "menu"
    assert started.data["total"] == 15
    assert finished.action == "finished" and finished.data["answered"] == 15
    assert finished.data["correct"] == 15 and finished.data["seconds"] >= 0
    assert finished.session_id == started.session_id
    taps = [e.action for e in await _events(session, user, "msg")]
    assert "меню learn_words" in taps
