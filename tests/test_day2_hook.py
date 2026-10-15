# -*- coding: utf-8 -*-
"""
СООБЩЕНИЕ ВТОРОГО ДНЯ (патч 2.1, пункт 2).

79% новичков не возвращаются на второй день. Через сутки после первого
занятия — одно личное сообщение с числом вчерашних слов и кнопкой занятия.
"""
from datetime import timedelta

import pytest

from app.core.clock import utcnow
from app.database.enums import CEFRLevel
from app.database.models import QuizSession
from app.schedulers.day2_hook import day2_keyboard, due_users, may_write

pytestmark = pytest.mark.asyncio


async def _finished(session, user, hours_ago: float, now=None):
    # Закончил — значит, и в счётчике занятий (как в боте, `_finish_quiz`)
    user.quizzes_passed = (user.quizzes_passed or 0) + 1
    done = (now or utcnow()) - timedelta(hours=hours_ago)
    session.add(QuizSession(user_id=user.id, level=CEFRLevel.A1, total_questions=7,
                            answered_questions=7, is_completed=True,
                            started_at=done - timedelta(minutes=3), completed_at=done))
    await session.commit()


async def test_newcomer_a_day_later_is_due(session, user):
    await _finished(session, user, hours_ago=23)
    due = await due_users(session, utcnow())
    assert [u.id for u, _ in due] == [user.id]


async def test_too_early_and_too_late_are_not_due(session, user):
    await _finished(session, user, hours_ago=10)
    assert await due_users(session, utcnow()) == []
    assert await due_users(session, utcnow() + timedelta(hours=30)) == []


async def test_who_came_back_is_not_bothered(session, user):
    await _finished(session, user, hours_ago=23)
    await _finished(session, user, hours_ago=1)          # вернулся сам
    assert await due_users(session, utcnow()) == []


async def test_once_in_a_lifetime(session, user):
    await _finished(session, user, hours_ago=23)
    user.day2_hook_sent_at = utcnow() - timedelta(days=30)
    await session.commit()
    assert await due_users(session, utcnow()) == []


async def test_declined_reminders_means_no_message(session, user):
    """
    Писать нельзя только тому, кто ЯВНО отказался. Предложение без ответа —
    не отказ: новичок, который просто ушёл, и есть тот, кого возвращаем
    (независимая проверка 2.1 — прежнее правило отсекало почти всех).
    """
    user.reminder_offered_at = utcnow() - timedelta(hours=20)
    user.notifications_enabled = False
    assert may_write(user), "промолчавший новичок сочтён отказавшимся"
    user.reminders_declined_at = utcnow() - timedelta(hours=19)
    assert not may_write(user), "явный отказ проигнорирован"
    user.notifications_enabled = True
    assert may_write(user), "отказался, а потом включил — можно"


async def test_no_second_message_on_a_reminder_day(session, user):
    """Обычное напоминание сегодня уже было — второго сообщения в тот же день нет."""
    now = utcnow()
    user.last_notification_sent = now - timedelta(minutes=30)
    assert not may_write(user, now)


async def test_two_lessons_on_the_first_day_still_due(session, user):
    """Утром и вечером первого дня — всё равно «не вернулся на второй»."""
    # «Сейчас» — полдень: оба занятия вчера днём по Берлину, в один день,
    # когда бы ни запускали тест
    noon = utcnow().replace(hour=12, minute=0, second=0, microsecond=0)
    await _finished(session, user, hours_ago=25, now=noon)
    await _finished(session, user, hours_ago=23, now=noon)
    due = await due_users(session, noon)
    assert [u.id for u, _ in due] == [user.id]


def test_button_starts_a_lesson_marked_day2():
    kb = day2_keyboard("ru", 7)
    assert kb.inline_keyboard[0][0].callback_data == "learn_now:day2"
    assert kb.inline_keyboard[1][0].callback_data == "notif_off"


def test_day2_source_is_known():
    from app.bot.handlers.quiz.sources import source_from_callback

    assert source_from_callback("learn_now:day2") == "day2"


def test_texts_in_every_language():
    from app.locales import get_text

    for lang in ("ru", "uk", "en", "de", "pl", "tr"):
        for key in ("day2_hook_words", "day2_hook"):
            text = get_text(key, lang, count=7)
            assert text and "{" not in text and "[MISSING" not in text, (lang, key)
