"""
Админка → «Аналитика» (2.2.1): путь, уходы, «Говорю», журнал — по журналу
пути, без владельца. И исправления по аудиту 18.10.
"""
from datetime import timedelta

from app.core.clock import utcnow
from app.database.enums import CEFRLevel
from app.database.models import QuizSession, User, UserEvent
from app.testing import make_bot, make_dispatcher, press, reset_state, text_update

ADMIN = 1          # tests/conftest.py: ADMIN_USER=1


async def _seed(session, user):
    now = utcnow()
    owner = User(id=ADMIN, first_name="Владелец", interface_language="ru",
                 learning_lang="de", native_lang="ru")
    session.add(owner)
    await session.flush()

    def lesson(uid, *, done, answered, source="menu", reason=None):
        return QuizSession(user_id=uid, level=CEFRLevel.A1, total_questions=15,
                           answered_questions=answered, correct_answers=answered,
                           is_completed=done, completed_at=now if done else None,
                           exit_reason="completed" if done else reason, start_source=source,
                           started_at=now - timedelta(hours=1),
                           learning_lang="de", native_lang="ru")

    s1 = lesson(user.id, done=False, answered=0, reason="restarted")
    s2 = lesson(user.id, done=False, answered=3, reason="abandoned")
    s3 = lesson(user.id, done=True, answered=15, source="again")
    s4 = lesson(user.id, done=True, answered=15, source="nd_back3")
    mine = lesson(ADMIN, done=False, answered=1, reason="abandoned")    # владелец — не в счёт
    session.add_all([s1, s2, s3, s4, mine])
    await session.flush()
    for kind, action, channel, sid, data in [
        ("question", "s", "s", s2.id, {"n": 3}),
        ("skip", "speech_skip", "s", s2.id, None),
        ("speech", "matched", "s", s3.id, {"attempt": 1}),
        ("lesson", "resume", None, s3.id, None),
        ("speech_invite", "try", None, None, None),
        ("chat", "blocked", None, None, None),
        ("error", "KeyError", None, None, {"where": "кнопка answer"}),
        ("msg", "меню learn_words", None, None, None),
    ]:
        session.add(UserEvent(user_id=user.id, at=now, kind=kind, action=action,
                              channel=channel, session_id=sid, data=data))
    session.add(UserEvent(user_id=ADMIN, at=now, kind="chat", action="blocked"))
    user.speech_choice = "on"
    await session.commit()


async def _screen(session, data):
    bot, recorder = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    await dp.feed_update(bot, press(ADMIN, data, message_id=700))
    edits = [p.get("text") or "" for n, p in recorder.calls if n == "EditMessageText"]
    assert edits, f"{data}: экран не показан"
    return edits[-1]


async def test_hub_and_screens_render_with_data(session, user):
    await _seed(session, user)
    assert "Путь" in await _screen(session, "admin:insights")

    path = await _screen(session, "admin:ins_path:7")
    assert "Пришли" in path and "Занимались 2+ дня" in path

    leave = await _screen(session, "admin:ins_leave:7")
    assert "перезапуск" in leave and "брошено" in leave
    assert "Говорю" in leave, "последняя игра перед уходом — по журналу"
    assert "«Ещё занятие»" in leave and "сообщение back3" in leave
    assert "Продолжили" in leave

    speech = await _screen(session, "admin:ins_speech:7")
    assert "согласились" in speech and "«Попробовать»" in speech

    log = await _screen(session, "admin:ins_log:7")
    assert "ушли 1" in log, "блокировка владельца попала в счёт или не видна"
    assert "KeyError" in log and "меню learn_words" in log


async def test_owner_is_not_counted(session, user):
    await _seed(session, user)
    leave = await _screen(session, "admin:ins_leave:30")
    # Брошено: только у человека (1 без единого ответа 0), не у владельца (было бы 2)
    import re
    row = re.search(r"брошено\s+(\d+)\s+(\d+)", leave)
    assert row and row.groups() == ("1", "0"), leave


async def test_strangers_get_nothing(session, user):
    bot, recorder = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    await dp.feed_update(bot, press(user.id, "admin:ins_path:7"))
    assert not [n for n, _ in recorder.calls if n == "EditMessageText"]


async def test_person_card_shows_the_path(session, user):
    await _seed(session, user)
    bot, recorder = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    await dp.feed_update(bot, text_update(ADMIN, f"/admin_user {user.id}"))
    card = " ".join(recorder.sent_texts())      # длинная карточка — несколькими сообщениями
    assert "Путь" in card and "заблокировал" in card and "Брошено   " in card
    assert "Говорю" in card
