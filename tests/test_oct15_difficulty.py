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
