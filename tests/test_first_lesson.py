# -*- coding: utf-8 -*-
"""
Лёгкий первый урок (патч 2.1).

Прод 15.10: 21 из 32 брошенных занятий брошены на 0–2-м вопросе; польский
новичок первым словом получил многозначное «mieć na myśli» и ушёл после
первого ответа. Владелец: «первые 7 с лёгкими вопросами, чтобы юзер как
можно прошёл первый круг и получил дофамин»; «даже если он его сбросит —
чтобы открывалась полноценная игра после первого круга».
"""
import pytest

from app.database.enums import CEFRLevel, PartOfSpeech, QuizChannel, QuizMode
from app.database.models import WordFrequency
from app.services import quiz_service
from app.services.language_service import pair_from_user
from app.testing import make_bot, make_dispatcher, press, reset_state, text_update
from tests.conftest import build_groups, make_word
from tests.test_games_audit_oct14 import LEARN

pytestmark = pytest.mark.asyncio


async def _dictionary(session, user):
    # Самые частые — многословные и служебные: первый урок их обходит
    hard = [make_word("zu Hause", pl="w domu"), make_word("nach Hause", pl="do domu"),
            make_word("aber", pos=PartOfSpeech.CONJUNCTION),
            make_word("Donaudampfschifffahrt")]
    easy = [make_word(f"Haus{i}", level=CEFRLevel.A1) for i in range(12)]
    words = hard + easy
    session.add_all(words)
    await build_groups(session, ["de"])
    for i, w in enumerate(words):
        session.add(WordFrequency(word_id=w.id, lang="de", zipf=7.5 - i * 0.05))
    user.level = CEFRLevel.A1
    user.quiz_mode = QuizMode.LEVEL
    user.quiz_word_count = 15
    await session.commit()
    return hard, easy


async def test_first_lesson_is_seven_cards_of_easy_words(session, user):
    hard, easy = await _dictionary(session, user)
    assert quiz_service.in_first_lesson(user) and quiz_service.lesson_length(user) == 7
    hard_ids = {w.id for w in hard}
    used = []
    for n in range(1, 8):
        q = await quiz_service.generate_question(
            session, user, exclude_ids=used, pair=pair_from_user(user),
            round_length=7, question_number=n)
        assert q["channel"] is QuizChannel.TEXT, q["channel"]
        assert q["correct_word"].id not in hard_ids, q["correct_word"].word_de
        used.append(q["correct_word"].id)


async def test_full_game_after_seven_answers_even_in_abandoned_lessons(session, user):
    """Бросил, вернулся, снова бросил — после 7 ответов всего открывается полная игра."""
    await _dictionary(session, user)
    bot, _ = make_bot()
    dp = make_dispatcher(session)
    for _ in range(3):                       # три брошенных занятия
        await reset_state(dp)
        await dp.feed_update(bot, text_update(user.id, LEARN))
        for _ in range(3):
            data = await dp.fsm.get_context(bot, chat_id=user.id, user_id=user.id).get_data()
            await dp.feed_update(bot, press(user.id, f"answer_{data['correct_word_id']}"))
            await dp.feed_update(bot, press(user.id, "next_question"))
    await session.refresh(user)
    assert user.quizzes_passed == 0
    assert user.onboarded_at is not None, "лёгкий режим держит вечно того, кто бросает"
    assert not quiz_service.in_first_lesson(user) and quiz_service.lesson_length(user) == 15


async def test_finished_first_lesson_opens_the_full_game(session, user):
    await _dictionary(session, user)
    bot, _ = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    await dp.feed_update(bot, text_update(user.id, LEARN))
    data = await dp.fsm.get_context(bot, chat_id=user.id, user_id=user.id).get_data()
    assert data["total_questions"] == 7
    for _ in range(7):
        data = await dp.fsm.get_context(bot, chat_id=user.id, user_id=user.id).get_data()
        await dp.feed_update(bot, press(user.id, f"answer_{data['correct_word_id']}"))
        await dp.feed_update(bot, press(user.id, "next_question"))
    await session.refresh(user)
    assert user.quizzes_passed == 1 and user.onboarded_at is not None
    assert quiz_service.lesson_length(user) == 15


def test_old_players_are_not_newcomers():
    from types import SimpleNamespace

    assert not quiz_service.in_first_lesson(SimpleNamespace(onboarded_at=None, quizzes_passed=4))
    assert not quiz_service.in_first_lesson(SimpleNamespace(onboarded_at=object(), quizzes_passed=0))
    assert quiz_service.in_first_lesson(SimpleNamespace(onboarded_at=None, quizzes_passed=0))
