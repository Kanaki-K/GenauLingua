# -*- coding: utf-8 -*-
"""
Первое занятие — знакомство с уровнем (решение владельца 29.10.2026).

Журнал 16–29.10: 9 из 18 новичков бросили первое занятие, 7 из них — на
втором вопросе «Слышу» или сразу после него; взрослые сами переставляли A1
на B1–C1. Теперь первое занятие — восемь карточек по два новых слова уровней
A1, A2, B1, B2; ответы определяют уровень, и человек может его поправить.
"""
import pytest
from sqlalchemy import select

from app.bot.handlers.quiz.lesson_state import S_SHOWN
from app.database.enums import CEFRLevel, PartOfSpeech, QuizChannel, QuizMode
from app.database.models import QuizSession
from app.services import first_lesson, quiz_service
from app.services.language_service import pair_from_user
from app.testing import make_bot, make_dispatcher, press, reset_state, text_update
from tests.conftest import build_groups, make_word
from tests.test_games_audit_oct14 import LEARN

pytestmark = pytest.mark.asyncio

A1, A2, B1, B2 = CEFRLevel.A1, CEFRLevel.A2, CEFRLevel.B1, CEFRLevel.B2

# Немецкое слово и значение, НЕ похожие друг на друга (знакомство обходит
# похожие на родные: Taxi/такси угадывается без знания языка)
_WORDS = {
    A1: [("Tisch", "стол"), ("Hund", "собака"), ("Brot", "хлеб"), ("Stuhl", "стул"), ("Wasser", "вода")],
    A2: [("Schrank", "шкаф"), ("Gabel", "вилка"), ("Wolke", "облако"), ("Kissen", "подушка"), ("Ziege", "коза")],
    B1: [("Pflicht", "долг"), ("Zweifel", "сомнение"), ("Mut", "смелость"), ("Gier", "жадность"), ("Neid", "зависть")],
    B2: [("Hürde", "препятствие"), ("Ehrgeiz", "честолюбие"), ("Demut", "смирение"), ("Wucht", "сила"), ("Ödnis", "пустошь")],
}


async def _dictionary(session, user):
    words = [make_word(de, level=level, ru=ru) for level, pairs in _WORDS.items() for de, ru in pairs]
    session.add_all(words)
    await build_groups(session, ["de"])
    user.level = A1
    user.quiz_mode = QuizMode.LEVEL
    user.quiz_word_count = 15
    user.audio_enabled = True
    user.quiz_channels = "tasrb"
    await session.commit()
    return {w.id: w.level for w in words}


async def test_placement_is_eight_cards_two_per_level_easy_to_hard(session, user):
    levels = await _dictionary(session, user)
    assert quiz_service.in_first_lesson(user) and quiz_service.lesson_length(user) == 8
    used, asked, games = [], [], []
    for n in range(1, 9):
        q = await quiz_service.generate_question(
            session, user, exclude_ids=used, pair=pair_from_user(user),
            round_length=8, question_number=n)
        assert q["correct_word"].id not in used, "слово повторилось"
        used.append(q["correct_word"].id)
        asked.append(levels[q["correct_word"].id])
        games.append(q["channel"])
    assert asked == list(first_lesson.PLACEMENT), asked
    # Без звука и без трудных игр: «Слышу» на втором вопросе было местом ухода
    assert games == [QuizChannel.TEXT] * 8, games


async def test_placement_skips_words_that_look_like_the_native_one(session, user):
    taxi = make_word("Taxi", level=A1, ru="такси")
    table = make_word("Tisch", level=A1, ru="стол")
    session.add_all([taxi, table])
    await build_groups(session, ["de"])
    user.level, user.quiz_mode = A1, QuizMode.LEVEL
    await session.commit()
    for _ in range(5):
        word = await first_lesson.placement_word(
            session, user, pair_from_user(user), A1, [], set())
        assert word.id == table.id, "Taxi угадывается без знания языка"


def test_recommend_the_first_level_not_fully_right():
    ok, bad = True, False
    assert first_lesson.recommend([(A1, ok), (A1, bad)]) is A1
    assert first_lesson.recommend([(A1, ok), (A1, ok), (A2, ok), (A2, bad)]) is A2
    assert first_lesson.recommend(
        [(A1, ok), (A1, ok), (A2, ok), (A2, ok), (B1, bad), (B1, ok), (B2, ok), (B2, ok)]) is B1
    assert first_lesson.recommend([(lv, ok) for lv in first_lesson.PLACEMENT]) is B2
    # Ступени не было (оборвано) — она и граница: выше ответы ничего не говорят
    assert first_lesson.recommend([(A1, ok), (A1, ok)]) is A2


def test_similarity_threshold():
    from app.services.first_lesson import SIMILAR_ENOUGH, similarity

    for learning, native in (("Taxi", "такси"), ("Hotel", "отель"), ("Kaffee", "кофе")):
        assert similarity(learning, native) >= SIMILAR_ENOUGH, (learning, native)
    for learning, native in (("Hand", "рука"), ("Bett", "кровать")):
        assert similarity(learning, native) < SIMILAR_ENOUGH, (learning, native)


async def test_no_board_in_the_first_lesson(session, user):
    from app.bot.handlers.quiz.match import _board_due

    await _dictionary(session, user)
    bot, _ = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    state = dp.fsm.get_context(bot, chat_id=user.id, user_id=user.id)
    pair = pair_from_user(user)
    for n in range(1, 9):
        assert not await _board_due(state, session, user, pair, n, 8)


async def _play(session, user, wrong_levels=()):
    """Пройти знакомство в боте; ошибиться на словах названных уровней."""
    levels = {w: lv for w, lv in (await _dictionary(session, user)).items()}
    bot, recorder = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    context = dp.fsm.get_context(bot, chat_id=user.id, user_id=user.id)
    await dp.feed_update(bot, text_update(user.id, LEARN))
    data = await context.get_data()
    assert data["total_questions"] == 8
    for _ in range(8):
        data = await context.get_data()
        correct = data["correct_word_id"]
        pick = correct
        if levels[correct] in wrong_levels:
            pick = next(o["id"] for o in data[S_SHOWN]["o"] if o["id"] != correct)
        await dp.feed_update(bot, press(user.id, f"answer_{pick}"))
        await dp.feed_update(bot, press(user.id, "next_question"))
    return bot, dp, recorder


async def test_answers_set_the_level_and_offer_to_change_it(session, user):
    _, dp, recorder = await _play(session, user, wrong_levels=(B1,))
    await session.refresh(user)
    assert user.quizzes_passed == 1 and user.onboarded_at is not None
    assert user.level is B1, user.level
    assert quiz_service.lesson_length(user) == 15
    buttons = recorder.buttons()
    assert "level_set_A1" in buttons and "level_set_B2" in buttons
    assert "level_set_B1" not in buttons, "текущий уровень предлагать незачем"
    # Предложение «легко — выше» после знакомства не дублируется
    assert not [b for b in buttons if b.startswith(("level_jump_", "level_up_"))]
    quiz = (await session.execute(select(QuizSession))).scalar_one()
    assert quiz.is_completed and quiz.answered_questions == 8


async def test_all_right_lands_on_b2_and_the_person_can_go_down(session, user):
    bot, dp, recorder = await _play(session, user)
    await session.refresh(user)
    assert user.level is B2
    await dp.feed_update(bot, press(user.id, "level_set_A2"))
    await session.refresh(user)
    assert user.level is A2, "поправить уровень можно и вниз"


async def test_full_game_after_eight_answers_even_in_abandoned_lessons(session, user):
    """Бросил, вернулся, снова бросил — после 8 ответов всего открывается полная игра."""
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


def test_old_players_are_not_newcomers():
    from types import SimpleNamespace

    assert not quiz_service.in_first_lesson(SimpleNamespace(onboarded_at=None, quizzes_passed=4))
    assert not quiz_service.in_first_lesson(SimpleNamespace(onboarded_at=object(), quizzes_passed=0))
    assert quiz_service.in_first_lesson(SimpleNamespace(onboarded_at=None, quizzes_passed=0))
