# -*- coding: utf-8 -*-
"""
der / die / das вместо карточки «Читаю» знакомого существительного
(владелец, 29.10.2026). Только немецкий, только знакомое слово, не в первом
занятии; без звука и без примера — они выдали бы артикль.
"""
from datetime import timedelta

import pytest
from sqlalchemy import select

from app.core.clock import utcnow
from app.database.enums import CEFRLevel, PartOfSpeech, QuizChannel, QuizMode
from app.database.models import QuizQuestion, UserWord
from app.services import quiz_service
from app.services.language_service import pair_from_user
from app.testing import make_bot, make_dispatcher, press, reset_state, text_update
from tests.conftest import build_groups, make_word
from tests.test_games_audit_oct14 import LEARN

pytestmark = pytest.mark.asyncio

_NOUNS = (("Bank", "die", "банк"), ("Tisch", "der", "стол"), ("Brot", "das", "хлеб"),
          ("Stuhl", "der", "стул"), ("Wolke", "die", "облако"), ("Messer", "das", "нож"))


async def _setup(session, user, *, familiar=True):
    words = [make_word(de, article=art, ru=ru, pos=PartOfSpeech.NOUN) for de, art, ru in _NOUNS]
    session.add_all(words)
    await build_groups(session, ["de"])
    user.level, user.quiz_mode, user.quiz_word_count = CEFRLevel.A1, QuizMode.LEVEL, 5
    user.quiz_channels = "t"
    user.onboarded_at, user.quizzes_passed = utcnow(), 3
    if familiar:
        for w in words:
            session.add(UserWord(user_id=user.id, word_id=w.id, learning_lang="de",
                                 correct_streak=4, times_shown=4, times_correct=4, learned=True,
                                 learned_at=utcnow(), last_seen_at=utcnow() - timedelta(days=60)))
    await session.commit()
    return words


async def test_only_a_familiar_german_noun_on_a_card(session, user, monkeypatch):
    monkeypatch.setattr(quiz_service, "ARTICLE_SHARE", 1.0)
    words = await _setup(session, user, familiar=False)
    pair = pair_from_user(user)
    assert not await quiz_service.wants_article(session, user, words[0], pair, QuizChannel.TEXT), \
        "новое слово — сперва значение, артикль потом"
    word = words[0]
    session.add(UserWord(user_id=user.id, word_id=word.id, learning_lang="de",
                         correct_streak=3, times_shown=3, times_correct=3, last_seen_at=utcnow()))
    await session.commit()
    assert await quiz_service.wants_article(session, user, word, pair, QuizChannel.TEXT)
    assert not await quiz_service.wants_article(session, user, word, pair, QuizChannel.REVERSE)
    user.onboarded_at, user.quizzes_passed = None, 0
    assert not await quiz_service.wants_article(session, user, word, pair, QuizChannel.TEXT), \
        "в знакомстве с уровнем артикля нет"


async def test_live_article_question_counts_like_a_card(session, user, monkeypatch):
    monkeypatch.setattr(quiz_service, "ARTICLE_SHARE", 1.0)
    words = {w.id: w for w in await _setup(session, user)}
    bot, recorder = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    context = dp.fsm.get_context(bot, chat_id=user.id, user_id=user.id)
    await dp.feed_update(bot, text_update(user.id, LEARN))

    assert {"art_der", "art_die", "art_das"} <= set(recorder.buttons()), recorder.buttons()
    data = await context.get_data()
    word = words[data["correct_word_id"]]
    card = recorder.sent_texts()[-1]
    assert "Какой артикль у этого слова?" in card and f"<b>{word.word_de}</b>" in card
    assert f"{word.article} {word.word_de}" not in card, "артикль виден в вопросе"

    wrong = next(a for a in ("der", "die", "das") if a != word.article)
    await dp.feed_update(bot, press(user.id, f"art_{wrong}"))
    row = (await session.execute(select(QuizQuestion))).scalars().one()
    assert row.word_id == word.id and row.is_correct is False
    assert row.user_answer == wrong and row.chosen_word_id is None
    uw = (await session.execute(select(UserWord).where(UserWord.word_id == word.id))).scalars().one()
    assert uw.correct_streak == 0, "не знаешь артикль — не знаешь существительное"

    await dp.feed_update(bot, press(user.id, "next_question"))
    data = await context.get_data()
    word = words[data["correct_word_id"]]
    await dp.feed_update(bot, press(user.id, f"art_{word.article}"))
    rows = (await session.execute(select(QuizQuestion).order_by(QuizQuestion.id))).scalars().all()
    assert rows[-1].is_correct is True and rows[-1].channel == QuizChannel.TEXT.value
