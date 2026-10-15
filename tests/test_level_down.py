# -*- coding: utf-8 -*-
"""
ПОНИЖЕНИЕ УРОВНЯ — обратная сторона выбора одним нажатием (15.10).

Раз уровень можно выбрать сразу (A2 / B1 / B2 / C1), человек может и
переоценить себя. Владелец: «подумай ещё раз и сделай лучшее решение по
адекватности и логике; убедись, что всё работает и правильно записывается».
"""
import pytest

from app.database.enums import CEFRLevel, QuizMode
from app.services.level_service import (
    LOWER_ACCURACY,
    LOWER_MIN_ANSWERS,
    REOFFER_AFTER_ROUNDS,
    decline_lower_level,
    lower_level,
    should_offer_lower_level,
    should_offer_next_level,
)
from tests.test_level_offer import _answers

pytestmark = pytest.mark.asyncio


async def _struggling(session, user):
    user.level = CEFRLevel.B2
    user.quiz_mode = QuizMode.LEVEL
    user.quizzes_passed = 10
    wrong = LOWER_MIN_ANSWERS // 2 + 1          # больше половины — ниже 60%
    await _answers(session, user, correct=LOWER_MIN_ANSWERS - wrong, wrong=wrong)


async def test_too_hard_offers_the_level_below(session, user):
    await _struggling(session, user)
    assert await should_offer_lower_level(user, session) == CEFRLevel.B1


async def test_normal_learning_is_not_too_hard(session, user):
    """85% — обычная учёба: понижать незачем."""
    user.level = CEFRLevel.B2
    user.quizzes_passed = 10
    await _answers(session, user, correct=17, wrong=3)
    assert 17 / 20 >= LOWER_ACCURACY
    assert await should_offer_lower_level(user, session) is None


async def test_one_lesson_is_not_enough_to_judge(session, user):
    user.level = CEFRLevel.B2
    user.quizzes_passed = 10
    await _answers(session, user, correct=2, wrong=8)
    assert await should_offer_lower_level(user, session) is None, (
        "по десяти ответам уже предлагаем вниз — рано"
    )


async def test_a1_has_nowhere_to_go_down(session, user):
    user.level = CEFRLevel.A1
    user.quizzes_passed = 10
    await _answers(session, user, correct=5, wrong=15)
    assert await should_offer_lower_level(user, session) is None


async def test_staying_is_remembered_and_asked_again_after_five(session, user):
    await _struggling(session, user)
    assert await decline_lower_level(user, session, offered=CEFRLevel.B1)
    assert user.level_offer_declined == "B2:down"
    assert await should_offer_lower_level(user, session) is None

    user.quizzes_passed += REOFFER_AFTER_ROUNDS
    assert await should_offer_lower_level(user, session) == CEFRLevel.B1, (
        "через пять занятий на той же трудности не спросили снова"
    )


async def test_staying_down_does_not_block_going_up_later(session, user):
    """Отказ от понижения записан как «B2:down» — подъём с B2 он не глушит."""
    user.level = CEFRLevel.B2
    user.quizzes_passed = 10
    user.level_offer_declined = "B2:down"
    user.level_offer_declined_round = 10
    await _answers(session, user, correct=LOWER_MIN_ANSWERS, wrong=0)
    assert await should_offer_next_level(user, session) == CEFRLevel.C1


async def test_lowering_goes_one_step_and_stale_buttons_do_nothing(session, user):
    user.level = CEFRLevel.B2
    await session.commit()
    assert not await lower_level(user, session, CEFRLevel.A2), "прыжок вниз через ступень"
    assert await lower_level(user, session, CEFRLevel.B1)
    assert user.level == CEFRLevel.B1
    assert not await lower_level(user, session, CEFRLevel.B1), "устаревшая кнопка сработала"
    assert user.level == CEFRLevel.B1


async def test_the_result_offers_the_level_below(session, user):
    from app.bot.handlers.quiz.summary import _offer_what_fits
    from app.testing import make_bot, press

    await _struggling(session, user)
    user.notifications_enabled = True
    bot, recorder = make_bot()
    callback = press(user.id, "next_question").callback_query.as_(bot)

    await _offer_what_fits(callback, session, user, "ru")

    buttons = [b["callback_data"] for _, p in recorder.calls if p.get("reply_markup")
               for row in p["reply_markup"]["inline_keyboard"] for b in row]
    assert buttons == ["level_down_B1", "level_down_no_B1"], buttons


async def test_pressing_lower_changes_the_level_through_the_bot(session, user):
    from app.testing import make_bot, make_dispatcher, press, reset_state

    user.level = CEFRLevel.B2
    user.anchor_message_id = 990
    await session.commit()
    bot, recorder = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)

    await dp.feed_update(bot, press(user.id, "level_down_B1", message_id=995))

    await session.refresh(user)
    assert user.level == CEFRLevel.B1


async def test_accuracy_counts_only_words_of_the_current_level(session, user):
    """
    Повторы прежнего уровня не раздувают точность: прыгнувший A1→B1 не
    получит «выше» снова на лёгких повторах A1 (независимая проверка 15.10).
    """
    from app.database.models import QuizQuestion, QuizSession, Word
    from app.services.level_service import recent_accuracy
    from tests.conftest import build_groups, make_word

    easy = make_word("Haus", level=CEFRLevel.A1)
    hard = make_word("Gewerkschaft", level=CEFRLevel.B1)
    session.add_all([easy, hard])
    await build_groups(session, ["de"])
    user.level = CEFRLevel.B1
    quiz = QuizSession(user_id=user.id, learning_lang="de", level=CEFRLevel.B1, total_questions=30)
    session.add(quiz)
    await session.commit()
    for i in range(20):                                    # повторы A1 — все верно
        session.add(QuizQuestion(session_id=quiz.id, word_id=easy.id, is_correct=True, channel="t"))
    for i in range(10):                                    # слова B1 — половина
        session.add(QuizQuestion(session_id=quiz.id, word_id=hard.id, is_correct=i < 5, channel="t"))
    await session.commit()

    answered, accuracy = await recent_accuracy(user, session)
    assert answered == 10 and accuracy == 0.5, (answered, accuracy)


async def test_no_swing_back_up_right_after_lowering(session, user):
    """C1→B2 вниз — и сразу снова «на C1» через два лёгких занятия: качели."""
    user.level = CEFRLevel.C1
    user.quizzes_passed = 10
    await session.commit()
    assert await lower_level(user, session, CEFRLevel.B2)
    await _answers(session, user, correct=LOWER_MIN_ANSWERS, wrong=0)
    assert await should_offer_next_level(user, session) is None
    user.quizzes_passed += REOFFER_AFTER_ROUNDS
    assert await should_offer_next_level(user, session) == CEFRLevel.C1
