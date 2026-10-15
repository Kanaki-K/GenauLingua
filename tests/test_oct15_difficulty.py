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


async def test_old_empty_lesson_is_a_real_dropout(session, user):
    """Открыл первую карточку и ушёл на три дня — это отвал, а не перезапуск."""
    from datetime import timedelta

    from app.bot.handlers.quiz.lesson import _close_abandoned_sessions
    from app.core.clock import utcnow

    old = QuizSession(user_id=user.id, level=CEFRLevel.A1, total_questions=7,
                      answered_questions=0, started_at=utcnow() - timedelta(days=3))
    session.add(old)
    await session.commit()

    await _close_abandoned_sessions(session, user.id)

    assert old.exit_reason == "abandoned"


async def test_reminders_lead_from_the_second_lesson(session, user):
    """
    Выбор уровня впереди напоминаний — только после первого занятия.
    Проигнорировал и ушёл — со второго напоминания снова первыми.
    """
    from app.bot.handlers.quiz.summary import _offer_what_fits
    from app.services.level_service import NEWCOMER_MIN_ANSWERS
    from app.testing import make_bot, press
    from tests.test_level_offer import _answers

    user.level = CEFRLevel.A1
    user.quizzes_passed = 2
    user.notifications_enabled = False
    await _answers(session, user, correct=NEWCOMER_MIN_ANSWERS + 1, wrong=0)
    bot, recorder = make_bot()
    callback = press(user.id, "next_question").callback_query.as_(bot)

    await _offer_what_fits(callback, session, user, "ru")

    buttons = [b["callback_data"] for _, p in recorder.calls if p.get("reply_markup")
               for row in p["reply_markup"]["inline_keyboard"] for b in row]
    assert not any(b.startswith("level_jump_") for b in buttons), (
        f"со второго занятия уровень снова впереди напоминаний: {buttons}"
    )
    assert buttons, "под итогом ничего не предложено"


async def test_english_learner_gets_english_levels(session, user):
    """
    Уровень — в ИЗУЧАЕМОМ языке. Сверка 15.10: немецкие уровни расходились с
    Oxford на 2+ ступени у 22% слов; «cold» по Goethe B1, по Oxford A1.
    """
    from app.database.models import WordLevel
    from app.services import quiz_service

    cold = make_word("kalt", level=CEFRLevel.B1, en="cold")          # Goethe B1, Oxford A1
    rare = make_word("Kaltfront", level=CEFRLevel.A1, en="cold front")  # обратный случай
    session.add_all([cold, rare])
    await build_groups(session, ["de", "en"])
    session.add_all([WordLevel(word_id=cold.id, lang="en", level=CEFRLevel.A1),
                     WordLevel(word_id=rare.id, lang="en", level=CEFRLevel.B2)])
    user.learning_lang, user.native_lang = "en", "ru"
    user.level = CEFRLevel.A1
    user.quiz_mode = QuizMode.LEVEL
    await session.commit()

    picked = await quiz_service.get_new_words(user.id, session, pair_from_user(user), [], user=user)
    assert picked is not None and picked.id == cold.id, "учащий английский получил немецкий уровень"


async def test_german_learner_keeps_goethe_levels(session, user):
    """Строк уровня для немецкого нет — берётся words.level (Goethe)."""
    from app.services import quiz_service

    haus = make_word("Haus", level=CEFRLevel.A1)
    seele = make_word("Seele", level=CEFRLevel.B1)
    session.add_all([haus, seele])
    await build_groups(session, ["de"])
    user.level = CEFRLevel.A1
    user.quiz_mode = QuizMode.LEVEL
    await session.commit()

    for _ in range(5):
        picked = await quiz_service.get_new_words(user.id, session, pair_from_user(user), [], user=user)
        assert picked.id == haus.id
