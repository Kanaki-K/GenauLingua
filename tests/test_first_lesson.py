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


async def test_first_lesson_mixes_three_games_on_easy_words(session, user):
    """
    Решение владельца 16.10: не семь карточек, а Читаю · Слышу · Вспоминаю
    по кругу. Слова словаря здесь похожи на свои значения («Haus0» —
    «Haus0_ru»), значит у «Слышу» и «Вспоминаю» есть что взять.
    """
    from app.services import first_lesson

    hard, easy = await _dictionary(session, user)
    user.audio_enabled = True
    user.quiz_channels = "tasrb"
    await session.commit()
    assert quiz_service.in_first_lesson(user) and quiz_service.lesson_length(user) == 7
    hard_ids = {w.id for w in hard}
    used, games = [], []
    for n in range(1, 7):
        q = await quiz_service.generate_question(
            session, user, exclude_ids=used, pair=pair_from_user(user),
            round_length=7, question_number=n)
        assert q["correct_word"].id not in hard_ids, q["correct_word"].word_de
        assert q["correct_word"].id not in used, "слово повторилось"
        used.append(q["correct_word"].id)
        games.append(q["channel"])
    assert games == list(first_lesson.PLAN), games
    assert QuizChannel.SPEECH not in games and QuizChannel.BUILD not in games


async def test_first_lesson_without_similar_word_gives_a_card(session, user):
    """Похожего на родное нет — «Слышу» не становится загадкой, идёт карточка."""
    words = [make_word(f"Wort{i}", ru=f"значение{i}") for i in range(8)]
    session.add_all(words)
    await build_groups(session, ["de"])
    user.level = CEFRLevel.A1
    user.quiz_mode = QuizMode.LEVEL
    user.audio_enabled = True
    user.quiz_channels = "tasrb"
    await session.commit()
    q = await quiz_service.generate_question(
        session, user, exclude_ids=[], pair=pair_from_user(user),
        round_length=7, question_number=2)
    assert q["channel"] is QuizChannel.TEXT


def test_similarity_threshold():
    from app.services.first_lesson import SIMILAR_ENOUGH, similarity

    for learning, native in (("Taxi", "такси"), ("Hotel", "отель"), ("Kaffee", "кофе")):
        assert similarity(learning, native) >= SIMILAR_ENOUGH, (learning, native)
    for learning, native in (("Hand", "рука"), ("Bett", "кровать")):
        assert similarity(learning, native) < SIMILAR_ENOUGH, (learning, native)


async def test_first_lesson_board_is_last_with_three_new_pairs(session, user):
    from app.bot.handlers.quiz.match import _board_due
    from app.services.match_service import pick_first_lesson_words

    await _dictionary(session, user)
    bot, _ = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    state = dp.fsm.get_context(bot, chat_id=user.id, user_id=user.id)
    pair = pair_from_user(user)
    assert not await _board_due(state, session, user, pair, 4, 7), "доска в середине первого урока"
    assert await _board_due(state, session, user, pair, 7, 7), "доски в конце первого урока нет"
    words = await pick_first_lesson_words(user, session, pair, 3)
    assert len(words) == 3 and len({w.id for w in words}) == 3


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
    # Доска последним вопросом здесь не нужна: проверяется отметка урока
    user.match_in_round = False
    await session.commit()
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


async def test_whole_first_lesson_three_games_then_a_three_pair_board(session, user):
    """
    Живой путь целиком: шесть вопросов трёх игр, доска на 3 пары последним
    вопросом, затем итог. Учёт: 6 ответов + 3 пары = 9, урок закрыт.
    """
    from sqlalchemy import select

    from app.database.models import QuizSession

    await _dictionary(session, user)
    user.audio_enabled = False        # звука в тестах нет; «Слышу» уступит карточке
    await session.commit()
    bot, recorder = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    context = dp.fsm.get_context(bot, chat_id=user.id, user_id=user.id)

    await dp.feed_update(bot, text_update(user.id, LEARN))
    for _ in range(6):
        data = await context.get_data()
        await dp.feed_update(bot, press(user.id, f"answer_{data['correct_word_id']}"))
        await dp.feed_update(bot, press(user.id, "next_question"))

    assert [b for b in recorder.buttons() if b.startswith("mt:")], (
        f"после шестого вопроса нет доски: {recorder.buttons()}"
    )
    data = await context.get_data()
    assert len(data["match_words"]) == 3
    for _ in range(3):
        data = await context.get_data()
        order, matched = data["match_right"], data["match_matched"]
        left = next(i for i in range(3) if i not in matched)
        await dp.feed_update(bot, press(user.id, f"mt:l:{left}:{data['match_version']}"))
        data = await context.get_data()
        await dp.feed_update(bot, press(user.id, f"mt:r:{order.index(left)}:{data['match_version']}"))
    await dp.feed_update(bot, press(user.id, "next_question"))

    await session.refresh(user)
    assert user.quizzes_passed == 1 and user.onboarded_at is not None
    quiz = (await session.execute(select(QuizSession))).scalar_one()
    assert quiz.is_completed and quiz.answered_questions == 9, (
        quiz.is_completed, quiz.answered_questions)
