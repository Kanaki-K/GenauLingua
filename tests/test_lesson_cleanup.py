"""
Висящие занятия закрываются сами (2.2.1): прод 18.10 — 25 незаконченных
старше суток без причины выхода; их закрывало только следующее «Учить».
"""
from datetime import timedelta

from app.core.clock import utcnow
from app.database.enums import CEFRLevel
from app.database.models import QuizQuestion, QuizSession
from app.services.lesson_cleanup import STALE_AFTER, close_stale_lessons
from tests.conftest import make_word


async def _lesson(session, user, *, started_ago, answered_ago=None, completed=False):
    now = utcnow()
    quiz = QuizSession(user_id=user.id, level=CEFRLevel.A1, total_questions=15,
                       answered_questions=1 if answered_ago is not None else 0,
                       correct_answers=0, is_completed=completed,
                       started_at=now - started_ago, learning_lang="de", native_lang="ru")
    session.add(quiz)
    await session.flush()
    if answered_ago is not None:
        word = make_word(f"W{quiz.id}", ru="с")
        session.add(word)
        await session.flush()
        session.add(QuizQuestion(session_id=quiz.id, word_id=word.id, channel="t",
                                 is_correct=True, answered_at=now - answered_ago))
    await session.commit()
    return quiz


async def test_old_untouched_lesson_is_closed_as_abandoned(session, user):
    old = await _lesson(session, user, started_ago=STALE_AFTER + timedelta(hours=1),
                        answered_ago=STALE_AFTER + timedelta(minutes=30))
    assert await close_stale_lessons(session) == 1
    await session.refresh(old)
    assert old.exit_reason == "abandoned" and old.exit_at_question == 1


async def test_recent_activity_finished_and_fresh_lessons_are_left_alone(session, user):
    # Начато давно, но ответ был час назад — его ещё можно продолжить
    alive = await _lesson(session, user, started_ago=STALE_AFTER + timedelta(days=1),
                          answered_ago=timedelta(hours=1))
    fresh = await _lesson(session, user, started_ago=timedelta(hours=3))
    done = await _lesson(session, user, started_ago=timedelta(days=5), completed=True)
    assert await close_stale_lessons(session) == 0
    for quiz in (alive, fresh, done):
        await session.refresh(quiz)
        assert quiz.exit_reason is None


async def test_second_run_changes_nothing(session, user):
    await _lesson(session, user, started_ago=timedelta(days=4))
    assert await close_stale_lessons(session) == 1
    assert await close_stale_lessons(session) == 0
