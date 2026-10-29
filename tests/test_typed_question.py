# -*- coding: utf-8 -*-
"""
Ответ вводом во «Вспоминаю» выученного слова (владелец, 29.10.2026): вариантов
нет, слово пишут сами; засчитывается как «Вспоминаю».
"""
from datetime import timedelta

import pytest
from sqlalchemy import select

from app.core.clock import utcnow
from app.database.enums import CEFRLevel, PartOfSpeech, QuizChannel, QuizMode
from app.database.models import QuizQuestion, UserWord
from app.services import quiz_service
from app.testing import make_bot, make_dispatcher, press, reset_state, text_update
from tests.conftest import build_groups, make_word
from tests.test_games_audit_oct14 import LEARN

pytestmark = pytest.mark.asyncio

_NOUNS = (("Bank", "die", "банк"), ("Tisch", "der", "стол"), ("Brot", "das", "хлеб"),
          ("Stuhl", "der", "стул"), ("Wolke", "die", "облако"), ("Messer", "das", "нож"))


async def _setup(session, user, *, learned=True):
    words = [make_word(de, article=art, ru=ru, pos=PartOfSpeech.NOUN) for de, art, ru in _NOUNS]
    session.add_all(words)
    await build_groups(session, ["de"])
    user.level, user.quiz_mode, user.quiz_word_count = CEFRLevel.A1, QuizMode.LEVEL, 5
    user.quiz_channels = "r"
    user.onboarded_at, user.quizzes_passed = utcnow(), 3
    for w in words:
        session.add(UserWord(user_id=user.id, word_id=w.id, learning_lang="de",
                             correct_streak=4 if learned else 1, times_shown=4, times_correct=4,
                             learned=learned, learned_at=utcnow() if learned else None,
                             last_seen_at=utcnow() - timedelta(days=60)))
    await session.commit()
    return {w.id: w for w in words}


async def _start(session, user):
    bot, recorder = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    context = dp.fsm.get_context(bot, chat_id=user.id, user_id=user.id)
    await dp.feed_update(bot, text_update(user.id, LEARN))
    return bot, dp, recorder, context


async def _rows(session):
    return (await session.execute(select(QuizQuestion).order_by(QuizQuestion.id))).scalars().all()


async def test_learned_word_is_typed_and_a_typo_counts(session, user, monkeypatch):
    monkeypatch.setattr(quiz_service, "TYPED_SHARE", 1.0)
    words = await _setup(session, user)
    bot, dp, recorder, context = await _start(session, user)
    assert "typed_skip" in recorder.buttons(), recorder.buttons()
    assert not [b for b in recorder.buttons() if b.startswith("answer_")], "варианты при вводе"
    assert "Напишите самостоятельно текстом" in recorder.sent_texts()[-1]

    word = words[(await context.get_data())["correct_word_id"]]
    typo = word.word_de[:-1] if len(word.word_de) >= 6 else word.word_de.lower()
    await dp.feed_update(bot, text_update(user.id, typo))
    row = (await _rows(session))[-1]
    assert row.word_id == word.id and row.is_correct is True, (typo, word.word_de)
    assert row.channel == QuizChannel.REVERSE.value and row.user_answer == typo
    screen = recorder.sent_texts()[-1] if recorder.sent_texts() else ""
    if typo != word.word_de.lower():
        assert "с опечаткой" in screen and "<u>" in screen, screen

    await dp.feed_update(bot, press(user.id, "next_question"))
    word = words[(await context.get_data())["correct_word_id"]]
    wrong_article = next(a for a in ("der", "die", "das") if a != word.article)
    await dp.feed_update(bot, text_update(user.id, f"{wrong_article} {word.word_de}"))
    assert (await _rows(session))[-1].is_correct is False, "неверный артикль засчитан"
    assert f"<u>{wrong_article}</u>" in recorder.sent_texts()[-1], "ошибка в артикле не подчёркнута"

    await dp.feed_update(bot, press(user.id, "next_question"))
    await dp.feed_update(bot, press(user.id, "typed_skip"))
    last = (await _rows(session))[-1]
    assert last.is_correct is False and last.user_answer is None


async def test_word_still_being_learned_keeps_the_options(session, user, monkeypatch):
    monkeypatch.setattr(quiz_service, "TYPED_SHARE", 1.0)
    await _setup(session, user, learned=False)
    _, _, recorder, _ = await _start(session, user)
    assert "typed_skip" not in recorder.buttons()
    assert [b for b in recorder.buttons() if b.startswith("answer_")]


async def test_menu_buttons_still_work_during_a_typed_question(session, user, monkeypatch):
    from app.locales import get_text

    monkeypatch.setattr(quiz_service, "TYPED_SHARE", 1.0)
    await _setup(session, user)
    bot, dp, recorder, _ = await _start(session, user)
    await dp.feed_update(bot, text_update(user.id, get_text("btn_settings", "ru")))
    assert not await _rows(session), "нажатие меню засчитано как ответ"
