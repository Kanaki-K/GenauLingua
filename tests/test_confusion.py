# -*- coding: utf-8 -*-
"""
Перепутал — значит, не знаешь (владелец, 29.10.2026): «1 раз ладно мисклик
по этому слову, но если несколько — не знает». Выбранное вместо верного
слово на второй путанице за 30 дней теряет серию и «выучено».
"""
from datetime import timedelta

import pytest

from app.core.clock import utcnow
from app.database.enums import CEFRLevel
from app.database.models import QuizQuestion, QuizSession, UserWord
from app.services.quiz_service import CONFUSION_WINDOW, note_confusion
from tests.conftest import build_groups, make_word

pytestmark = pytest.mark.asyncio


async def _setup(session, user, *, started=True):
    bank, band = make_word("Bank", ru="банк"), make_word("Band", ru="лента")
    session.add_all([bank, band])
    await build_groups(session, ["de"])
    quiz = QuizSession(user_id=user.id, level=CEFRLevel.A1, learning_lang="de", native_lang="ru",
                       total_questions=15)
    session.add(quiz)
    if started:
        session.add(UserWord(user_id=user.id, word_id=band.id, learning_lang="de",
                             correct_streak=4, times_shown=4, times_correct=4,
                             learned=True, learned_at=utcnow(), last_seen_at=utcnow()))
    await session.commit()
    return quiz, bank, band


async def _confuse(session, quiz, asked, chosen, when=None):
    session.add(QuizQuestion(session_id=quiz.id, word_id=asked.id, chosen_word_id=chosen.id,
                             is_correct=False, answered_at=when or utcnow()))
    await session.commit()
    return await note_confusion(session, quiz.user_id, chosen.id, asked.id, "de")


async def _band(session, user, band):
    return (await session.execute(
        UserWord.__table__.select().where(UserWord.user_id == user.id,
                                          UserWord.word_id == band.id))).first()


async def test_first_confusion_is_a_misclick_second_means_not_known(session, user):
    quiz, bank, band = await _setup(session, user)
    assert not await _confuse(session, quiz, bank, band)
    row = await _band(session, user, band)
    assert row.learned and row.correct_streak == 4, "один промах — ещё не незнание"

    assert await _confuse(session, quiz, bank, band)
    row = await _band(session, user, band)
    assert not row.learned and row.learned_at is None and row.correct_streak == 0


async def test_old_confusion_outside_the_window_does_not_count(session, user):
    quiz, bank, band = await _setup(session, user)
    long_ago = utcnow() - CONFUSION_WINDOW - timedelta(days=1)
    assert not await _confuse(session, quiz, bank, band, when=long_ago)
    assert not await _confuse(session, quiz, bank, band)
    assert (await _band(session, user, band)).learned


async def test_word_never_started_is_not_touched(session, user):
    quiz, bank, band = await _setup(session, user, started=False)
    assert not await _confuse(session, quiz, bank, band)
    assert not await _confuse(session, quiz, bank, band)
    assert await _band(session, user, band) is None


async def test_live_wrong_answer_twice_forgets_the_chosen_word(session, user):
    """Путь бота целиком: два раза выбрать «лента» вместо «банк»."""
    from app.bot.handlers.quiz.lesson_state import S_SHOWN
    from app.database.enums import QuizMode
    from app.testing import make_bot, make_dispatcher, press, reset_state, text_update
    from tests.test_games_audit_oct14 import LEARN

    # Четыре слова — каждый вопрос показывает их все, и подставное всегда среди вариантов
    words = [make_word(de, ru=ru) for de, ru in
             (("Tisch", "стол"), ("Hund", "собака"), ("Brot", "хлеб"), ("Stuhl", "стул"))]
    session.add_all(words)
    await build_groups(session, ["de"])
    user.level, user.quiz_mode, user.quiz_word_count = CEFRLevel.A1, QuizMode.LEVEL, 5
    user.quiz_channels = "t"
    user.onboarded_at, user.quizzes_passed = utcnow(), 3
    for w in words:
        session.add(UserWord(user_id=user.id, word_id=w.id, learning_lang="de",
                             correct_streak=4, times_shown=4, times_correct=4, learned=True,
                             learned_at=utcnow(), last_seen_at=utcnow() - timedelta(days=60)))
    await session.commit()
    decoy = words[3].id  # первым вопросом бот спрашивает words[0] — подставным не годится

    bot, _ = make_bot()
    dp = make_dispatcher(session)
    context = dp.fsm.get_context(bot, chat_id=user.id, user_id=user.id)
    confusions = 0
    for _ in range(8):
        await reset_state(dp)
        await dp.feed_update(bot, text_update(user.id, LEARN))
        data = await context.get_data()
        correct = data["correct_word_id"]
        shown = [o["id"] for o in data[S_SHOWN]["o"]]
        if correct == decoy or decoy not in shown:
            continue
        await dp.feed_update(bot, press(user.id, f"answer_{decoy}"))
        confusions += 1
        if confusions == 2:
            break
    assert confusions == 2, "подставное слово не попалось дважды — проверять нечего"
    row = (await session.execute(UserWord.__table__.select().where(
        UserWord.user_id == user.id, UserWord.word_id == decoy))).first()
    assert not row.learned and row.correct_streak == 0, "дважды выбранное вместо верного осталось выученным"
