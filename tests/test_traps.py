# -*- coding: utf-8 -*-
"""
Ловушки среди вариантов для знакомых слов (владелец, 29.10.2026): с чем путают
люди, похожие на вид, из той же темы. Новое слово — без ловушек.
"""
import pytest

from app.core.clock import utcnow
from app.database.enums import CEFRLevel, PartOfSpeech, QuizMode
from app.database.models import QuizQuestion, QuizSession, UserWord
from app.services import quiz_service, traps
from app.services.language_service import pair_from_user
from tests.conftest import build_groups, make_word

pytestmark = pytest.mark.asyncio


async def _base(session, user):
    bank = make_word("Bank", ru="банк")
    lookalikes = [make_word("Band", ru="лента"), make_word("Bart", ru="борода")]
    noise = [make_word(de, ru=ru) for de, ru in (
        ("Wolke", "облако"), ("Ziege", "коза"), ("Messer", "нож"), ("Kissen", "подушка"),
        ("Schrank", "шкаф"), ("Gabel", "вилка"), ("Zucker", "сахар"), ("Regen", "дождь"),
        ("Fenster", "окно"), ("Garten", "сад"), ("Spiegel", "зеркало"), ("Teller", "тарелка"))]
    session.add_all([bank, *lookalikes, *noise])
    await build_groups(session, ["de"])
    user.level, user.quiz_mode = CEFRLevel.A1, QuizMode.LEVEL
    await session.commit()
    return bank, lookalikes, noise


async def _know(session, user, word, streak=4, learned=True):
    session.add(UserWord(user_id=user.id, word_id=word.id, learning_lang="de",
                         correct_streak=streak, times_shown=streak, times_correct=streak,
                         learned=learned, learned_at=utcnow() if learned else None,
                         last_seen_at=utcnow()))
    await session.commit()


async def test_familiar_word_gets_lookalikes_new_word_does_not(session, user):
    bank, lookalikes, _ = await _base(session, user)
    pair = pair_from_user(user)
    lookalike_ids = {w.id for w in lookalikes}

    new_hits = 0
    for _ in range(10):
        picked = await quiz_service.get_distractors(bank, session, pair, user=user)
        new_hits += len({w.id for w in picked} & lookalike_ids)
    await _know(session, user, bank)
    for _ in range(5):
        picked = await quiz_service.get_distractors(bank, session, pair, user=user)
        ids = {w.id for w in picked}
        assert lookalike_ids <= ids, "у знакомого слова нет похожих на вид Band, Bart"
        assert len(ids - lookalike_ids) >= 1, "ловушек больше двух — вопрос нечестный"
    # Новое слово: ловушки не подставляются нарочно (случайно — бывает, но не всегда)
    assert new_hits < 20, "новое слово получает ловушки так же, как знакомое"


async def test_what_people_confuse_comes_first(session, user):
    bank, _, noise = await _base(session, user)
    pillow = noise[3]                                   # «подушка» — не похожа на Bank
    quiz = QuizSession(user_id=user.id, level=CEFRLevel.A1, learning_lang="de",
                       native_lang="ru", total_questions=15)
    session.add(quiz)
    await session.commit()
    for _ in range(3):
        session.add(QuizQuestion(session_id=quiz.id, word_id=bank.id, chosen_word_id=pillow.id,
                                 is_correct=False, answered_at=utcnow()))
    await session.commit()
    await _know(session, user, bank)
    found = await traps.trap_candidates(session, quiz_service._usable_words(pair_from_user(user)),
                                        bank, pair_from_user(user))
    assert found and found[0].id == pillow.id, [w.word_de for w in found]


async def test_same_topic_is_a_trap(session, user):
    fork = make_word("Gabel", ru="вилка")
    spoon = make_word("Löffel", ru="ложка")
    plate = make_word("Teller", ru="тарелка")
    cloud = make_word("Wolke", ru="облако")
    for w in (fork, spoon, plate):
        w.category = "Küche"
    cloud.category = "Wetter"
    session.add_all([fork, spoon, plate, cloud])
    await build_groups(session, ["de"])
    user.level, user.quiz_mode = CEFRLevel.A1, QuizMode.LEVEL
    await session.commit()
    found = await traps.trap_candidates(session, quiz_service._usable_words(pair_from_user(user)),
                                        fork, pair_from_user(user))
    assert {w.id for w in found} == {spoon.id, plate.id}


async def test_a_trap_never_shares_the_meaning(session, user):
    """Ловушка с тем же значением сделала бы два верных ответа — она отсеивается."""
    bank = make_word("Bank", ru="банк")
    twin = make_word("Banken", ru="банк", pos=PartOfSpeech.NOUN)
    others = [make_word(de, ru=ru) for de, ru in (("Wolke", "облако"), ("Ziege", "коза"),
                                                    ("Messer", "нож"), ("Kissen", "подушка"))]
    session.add_all([bank, twin, *others])
    await build_groups(session, ["de"])
    user.level, user.quiz_mode = CEFRLevel.A1, QuizMode.LEVEL
    await session.commit()
    await _know(session, user, bank)
    for _ in range(5):
        picked = await quiz_service.get_distractors(bank, session, pair_from_user(user), user=user)
        assert twin.id not in {w.id for w in picked}
