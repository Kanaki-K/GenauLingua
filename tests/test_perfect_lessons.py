"""
«10 занятий без ошибок» — без единой ошибки (2.2.1).

Прежде «без ошибок» = верных ≥ запланированных 15. Доска пар добавляет 5
ответов (итог «X/19»), поэтому проходили занятия с четырьмя ошибками, а
повтор ошибок тоже шёл в счёт.
"""

from app.core.clock import utcnow
from app.database.enums import CEFRLevel
from app.database.models import QuizQuestion, QuizSession, Word
from app.services.standing import PERFECT_LESSONS, standings
from tests.conftest import make_word


async def _lesson(session, user, word, *, wrong: int, answered: int = 19,
                  mode: str = "level"):
    quiz = QuizSession(user_id=user.id, level=CEFRLevel.A1, total_questions=15, answered_questions=answered,
                       correct_answers=answered - wrong, is_completed=True,
                       completed_at=utcnow(), quiz_mode=mode,
                       learning_lang="de", native_lang="ru")
    session.add(quiz)
    await session.flush()
    for i in range(answered):
        session.add(QuizQuestion(session_id=quiz.id, word_id=word.id, channel="t",
                                 is_correct=i >= wrong, answered_at=utcnow()))
    await session.flush()


async def _perfect(session, user):
    st = (await standings(session, [user]))[user.id]
    return "perfect_10" in st.achievements


async def _word(session):
    word = make_word("Haus", ru="дом")
    session.add(word)
    await session.flush()
    return word


async def test_lessons_with_four_mistakes_on_19_answers_are_not_perfect(session, user):
    word = await _word(session)
    for _ in range(PERFECT_LESSONS):
        await _lesson(session, user, word, wrong=4)      # 15 верных из 19 — прежде «без ошибок»
    assert not await _perfect(session, user)


async def test_ten_lessons_without_a_single_mistake_are_perfect(session, user):
    word = await _word(session)
    for _ in range(PERFECT_LESSONS):
        await _lesson(session, user, word, wrong=0)
    assert await _perfect(session, user)


async def test_error_repeats_do_not_count(session, user):
    word = await _word(session)
    for _ in range(PERFECT_LESSONS - 1):
        await _lesson(session, user, word, wrong=0)
    await _lesson(session, user, word, wrong=0, answered=3, mode="error_repeat")
    assert not await _perfect(session, user)
