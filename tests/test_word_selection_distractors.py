"""
Неверные варианты: не угадывается ли ответ по исключению (аудит подбора 15.10).

«Вспоминаю»: варианты — немецкие слова С АРТИКЛЕМ. Подбор требовал у
существительных артикль, ОТЛИЧНЫЙ от верного, — и артикль верного ответа
всегда был единственным: «бери непохожий» угадывал 63–65% вместо 25%.
Теперь у вариантов тот же артикль. И уровень вариантов — в изучаемом
языке: у учащего английский A1 все 60 вариантов приходили из en-C1.
"""
import collections
import random

from sqlalchemy import select

from app.database.enums import CEFRLevel, PartOfSpeech, QuizChannel
from app.database.models import Word
from app.services.language_service import option_label, pair_for_channel, pair_from_user
from app.services.quiz_service import build_options, get_distractors
from tests.conftest import build_groups, make_word

# Доли артиклей у канонических существительных A1 в dev-базе (der/die/das)
A1_ARTICLES = {"der": 154, "die": 119, "das": 85}


async def _seed(session):
    i = 0
    for art, n in A1_ARTICLES.items():
        for _ in range(n):
            session.add(make_word(f"N{i:04d}", level=CEFRLevel.A1, pos=PartOfSpeech.NOUN,
                                  article=art, ru=f"сущ{i:04d}"))
            i += 1
    await build_groups(session, ["de"])


def _article(label: str) -> str:
    return label.split(" ", 1)[0]


async def test_reverse_noun_article_gives_nothing_away(session, user):
    await _seed(session)
    user.level = CEFRLevel.A1
    await session.commit()
    pair = pair_for_channel(pair_from_user(user), QuizChannel.REVERSE)
    assert pair.answer_lang == "de"

    nouns = (await session.execute(select(Word).order_by(Word.id))).scalars().all()
    rng = random.Random(3)
    sample = rng.sample(nouns, 300)

    unique_correct = 0          # артикль верного — единственный среди вариантов
    fully_guessable = 0         # все три неверных — одного артикля
    guess_success = 0.0         # «выбери вариант с единственным артиклем» наугад
    for w in sample:
        distractors = await get_distractors(w, session, pair, user=user)
        assert len(distractors) == 3
        options, cidx = build_options(w, distractors, pair)
        arts = [_article(lbl) for _, lbl in options]
        counts = collections.Counter(arts)
        if counts[arts[cidx]] == 1:
            unique_correct += 1
        wrong = {a for k, a in enumerate(arts) if k != cidx}
        if len(wrong) == 1:
            fully_guessable += 1
        singles = [k for k, a in enumerate(arts) if counts[a] == 1]
        if cidx in singles:
            guess_success += 1 / len(singles)

    n = len(sample)
    print(f"\nREVERSE, существительные A1 (n={n}): артикль верного единственный "
          f"в {unique_correct / n:.0%}; все неверные одного артикля (ответ виден сразу) "
          f"в {fully_guessable / n:.0%}; стратегия «бери единственный артикль» "
          f"угадывает {guess_success / n:.0%} при честных 25%")
    # До починки (аудит подбора 15.10): единственный в 100%, угадывание 63–65%
    assert unique_correct == 0, "артикль верного ответа выделяется среди вариантов"
    assert guess_success / n <= 0.30


async def test_text_card_distractors_vary(session, user):
    """Карточка: у одного слова варианты не застывают одним набором."""
    await _seed(session)
    user.level = CEFRLevel.A1
    await session.commit()
    pair = pair_from_user(user)
    w = (await session.execute(select(Word).order_by(Word.id).limit(1))).scalar_one()
    seen = collections.Counter()
    sets = set()
    for _ in range(30):
        d = await get_distractors(w, session, pair, user=user)
        sets.add(frozenset(x.id for x in d))
        seen.update(x.id for x in d)
    print(f"\nКарточка: 30 вопросов по одному слову — {len(sets)} разных наборов, "
          f"самый частый неверный вариант встретился {seen.most_common(1)[0][1]} раз из 30")
    assert len(sets) >= 25


async def test_english_learner_distractors_use_english_level(session, user):
    """
    Неверные варианты «того же уровня» берутся по `Word.level` (Goethe), а не
    по уровню в изучаемом языке (`level_expr`) — тот же род ошибки, что был в
    подборе слов. Учащий английский A1: верное слово en-A1 (Goethe B1),
    вокруг — 20 глаголов en-A1/Goethe-A1 и 20 глаголов en-C1/Goethe-B1.
    """
    from app.database.models import WordLevel
    from app.database.enums import QuizMode

    target = make_word("kalt", level=CEFRLevel.B1, pos=PartOfSpeech.ADJECTIVE, en="cold")
    easy = [make_word(f"leicht{i}", level=CEFRLevel.A1, pos=PartOfSpeech.ADJECTIVE, en=f"easy{i}")
            for i in range(20)]
    hard = [make_word(f"schwer{i}", level=CEFRLevel.B1, pos=PartOfSpeech.ADJECTIVE, en=f"hard{i}")
            for i in range(20)]
    session.add_all([target, *easy, *hard])
    await build_groups(session, ["de", "en"])
    session.add(WordLevel(word_id=target.id, lang="en", level=CEFRLevel.A1))
    session.add_all([WordLevel(word_id=w.id, lang="en", level=CEFRLevel.A1) for w in easy])
    session.add_all([WordLevel(word_id=w.id, lang="en", level=CEFRLevel.C1) for w in hard])
    user.learning_lang, user.native_lang = "en", "ru"
    user.level = CEFRLevel.A1
    user.quiz_mode = QuizMode.LEVEL
    await session.commit()

    pair = pair_for_channel(pair_from_user(user), QuizChannel.REVERSE)
    hard_ids = {w.id for w in hard}
    from_hard = total = 0
    for _ in range(20):
        for d in await get_distractors(target, session, pair, user=user):
            total += 1
            from_hard += d.id in hard_ids
    print(f"\nУчащий английский A1: неверные варианты из en-C1 — {from_hard} из {total}")
    # До починки: 60 из 60 — уровень брался немецкий, а не изучаемого языка
    assert from_hard == 0
