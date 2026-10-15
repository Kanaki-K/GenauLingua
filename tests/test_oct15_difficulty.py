# -*- coding: utf-8 -*-
"""
Сложность и отвалы, 15.10.2026.

Прод: новичкам A1 приходили Strumpf и Waffe (новое слово бралось
случайно из уровня), а занятия, начатые повторно через 1–4 секунды,
считались брошенными на нулевом вопросе и завышали отвалы.
"""
import pytest

from app.database.enums import CEFRLevel, QuizMode
from app.database.models import QuizSession, WordFrequency
from app.services.language_service import pair_from_user
from tests.conftest import build_groups, make_word

pytestmark = pytest.mark.asyncio


async def test_new_word_comes_from_the_common_ones(session, user, monkeypatch):
    """Из 200 слов уровня новое берётся среди самых ходовых, а не из любых."""
    from app.services import quiz_service

    monkeypatch.setattr(quiz_service, "COMMON_POOL", 5)
    words = [make_word(f"Wort{i:03d}", level=CEFRLevel.A1) for i in range(200)]
    session.add_all(words)
    await build_groups(session, ["de"])
    for i, w in enumerate(words):
        session.add(WordFrequency(word_id=w.id, lang="de", zipf=7.0 - i * 0.01))
    user.level = CEFRLevel.A1
    user.quiz_mode = QuizMode.LEVEL
    await session.commit()

    common = {w.id for w in words[:5]}
    for _ in range(20):
        picked = await quiz_service.get_new_words(user.id, session, pair_from_user(user), [], user=user)
        assert picked.id in common, f"новое слово {picked.word_de} не из пяти самых ходовых"


async def test_empty_restarted_lesson_is_not_counted_as_abandoned(session, user):
    from app.bot.handlers.quiz.lesson import _close_abandoned_sessions

    empty = QuizSession(user_id=user.id, level=CEFRLevel.A1, total_questions=7, answered_questions=0)
    begun = QuizSession(user_id=user.id, level=CEFRLevel.A1, total_questions=7, answered_questions=3)
    session.add_all([empty, begun])
    await session.commit()

    await _close_abandoned_sessions(session, user.id)

    assert empty.exit_reason == "restarted", "пустое занятие засчитано отвалом"
    assert begun.exit_reason == "abandoned"


async def test_started_words_keep_coming_back_whatever_their_level(session, user):
    """
    Уровень решает, какие НОВЫЕ слова давать, — не какие повторять.
    Переуровнение 15.10 увело бы с уровня 4 317 слов в работе у 165 человек,
    и они перестали бы повторяться.
    """
    from datetime import timedelta

    from app.core.clock import utcnow
    from app.database.models import UserWord
    from app.services import quiz_service

    started = make_word("Waffe", level=CEFRLevel.B1)       # было A1, стало B1
    fresh_low = make_word("Haus", level=CEFRLevel.A1)
    fresh_high = make_word("Strumpf", level=CEFRLevel.B1)
    session.add_all([started, fresh_low, fresh_high])
    await build_groups(session, ["de"])
    user.level = CEFRLevel.A1
    user.quiz_mode = QuizMode.LEVEL
    session.add(UserWord(
        user_id=user.id, word_id=started.id, learning_lang="de",
        times_shown=2, times_correct=1, correct_streak=0, learned=False,
        last_seen_at=utcnow() - timedelta(days=10),
    ))
    await session.commit()
    pair = pair_from_user(user)

    due = await quiz_service.get_due_words(user.id, session, pair, [], user=user)
    assert due is not None and due.id == started.id, "начатое слово B1 не вернулось к человеку A1"

    new = await quiz_service.get_new_words(user.id, session, pair, [started.id], user=user)
    assert new is not None and new.id == fresh_low.id, "новое слово пришло не своего уровня"
