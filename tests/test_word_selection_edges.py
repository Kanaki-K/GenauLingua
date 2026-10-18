"""
Подбор слов на краях (аудит подбора 15.10): долг из 230 просроченных,
исчерпанный уровень, узкая тема, доска. Помощники симуляции —
`tests/word_selection_sim.py` (полная симуляция дней — там же, вручную).
"""
import collections
import random
from datetime import timedelta

from sqlalchemy import select

from app.core.clock import utcnow
from app.database.enums import CEFRLevel, QuizMode
from app.database.models import UserWord, Word
from tests.word_selection_sim import (
    Learner, report, run_lesson, seed, setup_user, shift, simulate,
)


async def test_backlog_230_overdue(session, user):
    words = await seed(session)
    await setup_user(session, user)
    a1 = [w for w in words if w.level == CEFRLevel.A1]
    rng = random.Random(5)
    for w in a1[:230]:
        session.add(UserWord(user_id=user.id, word_id=w.id, learning_lang="de",
                             times_shown=3, times_correct=2, correct_streak=rng.choice([1, 2, 3]),
                             last_seen_at=utcnow() - timedelta(days=40),
                             created_at=utcnow() - timedelta(days=60), learned=False))
    await session.commit()
    learner = Learner(random.Random(9))
    log = []
    for n in range(1, 4):
        await run_lesson(session, user, learner, log, 0, n)
        await shift(session, timedelta(minutes=1))
    report(log, "Долг: 230 просроченных, 3 занятия подряд")


async def test_level_exhausted(session, user):
    """Все слова A1 начаты и не просрочены: что даёт подбор."""
    words = await seed(session, n_a1=200, n_a2=100)
    await setup_user(session, user)
    a1 = [w for w in words if w.level == CEFRLevel.A1]
    rng = random.Random(5)
    for w in a1:
        streak = rng.choice([2, 3, 4, 5])
        session.add(UserWord(user_id=user.id, word_id=w.id, learning_lang="de",
                             times_shown=4, times_correct=4, correct_streak=streak,
                             learned=streak >= 3,
                             last_seen_at=utcnow() - timedelta(hours=2),
                             created_at=utcnow() - timedelta(days=30)))
    await session.commit()
    learner = Learner(random.Random(9))
    log = []
    for n in range(1, 4):
        await run_lesson(session, user, learner, log, 0, n)
        await shift(session, timedelta(minutes=1))
    r = report(log, "Уровень исчерпан (200 слов A1 начаты, ничего не просрочено), 3 занятия подряд")
    # слова предыдущего занятия, вернувшиеся в следующем
    lessons = collections.defaultdict(set)
    for x in r["shown"]:
        lessons[x["lesson"]].add(x["word"])
    print("повторы из прошлого занятия:",
          [len(lessons[k] & lessons[k - 1]) for k in (2, 3)])


async def test_small_category(session, user):
    """Режим «по теме» с 40 словами темы."""
    await seed(session, category="Kommunikation", n_cat=40)
    await setup_user(session, user, mode=QuizMode.CATEGORY, category="Kommunikation")
    log = await simulate(session, user, days=7, lessons_per_day=3)
    r = report(log, "По теме, 40 слов, 3 занятия в день, 7 дней")
    per_day = collections.Counter((x["day"]) for x in r["shown"])
    print("показов в день:", dict(per_day))


async def test_board_prefers_due_and_keeps_the_gap(session, user):
    """
    Доска (`match_service.pick_words`) брала случайные знакомые слова: без
    приоритета просроченных и без паузы после ответа (PRACTICE_GAP), которые
    есть у отработки. Теперь — то же правило, что у отработки.
    """
    from app.services.language_service import pair_from_user
    from app.services.match_service import pick_words
    words = await seed(session, n_a1=60, n_a2=0)
    await setup_user(session, user)
    for i, w in enumerate(words):
        due = i < 10
        session.add(UserWord(user_id=user.id, word_id=w.id, learning_lang="de",
                             times_shown=2, times_correct=2, correct_streak=2,
                             last_seen_at=utcnow() - (timedelta(days=5) if due else timedelta(seconds=30)),
                             created_at=utcnow() - timedelta(days=10), learned=False))
    await session.commit()
    # «только что отвечено» — строки ответов минуту назад у 50 не просроченных
    from app.database.models import QuizQuestion, QuizSession
    qsess = QuizSession(user_id=user.id, level=user.level, learning_lang="de", native_lang="ru",
                        total_questions=15, quiz_mode="level")
    session.add(qsess)
    await session.commit()
    for w in words[10:]:
        session.add(QuizQuestion(session_id=qsess.id, word_id=w.id, is_correct=True,
                                 answered_at=utcnow() - timedelta(seconds=30), channel="t"))
    await session.commit()
    pair = pair_from_user(user)
    due_ids = {w.id for w in words[:10]}
    due_hits = total = 0
    for _ in range(40):
        picked = await pick_words(user, session, pair)
        total += len(picked)
        due_hits += sum(1 for w in picked if w.id in due_ids)
    print(f"\nДоска: из {total} слов просроченных {due_hits} ({due_hits / total:.0%}); "
          f"остальные отвечены 30 секунд назад (просроченных в пуле 10 из 60 = 17%)")
    # До починки: доля просроченных 10% — доска брала только что отвеченные
    assert due_hits == total, "доска взяла слово, отвеченное 30 секунд назад"



async def test_board_prefers_words_not_seen_today(session, user):
    """
    Слова, отвеченные 5 ч назад (пауза прошла, но сегодня уже были), доска
    берёт только когда других нет: у владельца 14.10 все 5 слов каждой из 9
    досок уже встречались в тот же день.
    """
    from app.database.models import QuizQuestion, QuizSession
    from app.services.language_service import pair_from_user
    from app.services.match_service import pick_words

    words = await seed(session, n_a1=30, n_a2=0)
    await setup_user(session, user)
    for w in words:
        session.add(UserWord(user_id=user.id, word_id=w.id, learning_lang="de",
                             times_shown=2, times_correct=2, correct_streak=2,
                             last_seen_at=utcnow() - timedelta(days=1),
                             created_at=utcnow() - timedelta(days=10), learned=False))
    qsess = QuizSession(user_id=user.id, level=user.level, learning_lang="de", native_lang="ru",
                        total_questions=15, quiz_mode="level")
    session.add(qsess)
    await session.commit()
    seen_today = {w.id for w in words[:20]}
    for w in words[:20]:
        session.add(QuizQuestion(session_id=qsess.id, word_id=w.id, is_correct=True,
                                 answered_at=utcnow() - timedelta(hours=5), channel="t"))
    await session.commit()
    pair = pair_from_user(user)
    for _ in range(20):
        picked = await pick_words(user, session, pair)
        assert picked and not ({w.id for w in picked} & seen_today), "доска взяла сегодняшнее слово"


async def test_board_keeps_the_gap_even_when_all_were_seen_today(session, user):
    """Всё уже было сегодня: доска берёт отвеченные 5 ч назад, но не 30 с назад."""
    from app.database.models import QuizQuestion, QuizSession
    from app.services.language_service import pair_from_user
    from app.services.match_service import pick_words

    words = await seed(session, n_a1=30, n_a2=0)
    await setup_user(session, user)
    for w in words:
        session.add(UserWord(user_id=user.id, word_id=w.id, learning_lang="de",
                             times_shown=2, times_correct=2, correct_streak=2,
                             last_seen_at=utcnow() - timedelta(days=1),
                             created_at=utcnow() - timedelta(days=10), learned=False))
    qsess = QuizSession(user_id=user.id, level=user.level, learning_lang="de", native_lang="ru",
                        total_questions=15, quiz_mode="level")
    session.add(qsess)
    await session.commit()
    just_now = {w.id for w in words[10:]}
    for i, w in enumerate(words):
        ago = timedelta(seconds=30) if w.id in just_now else timedelta(hours=5)
        session.add(QuizQuestion(session_id=qsess.id, word_id=w.id, is_correct=True,
                                 answered_at=utcnow() - ago, channel="t"))
    await session.commit()
    pair = pair_from_user(user)
    for _ in range(20):
        picked = await pick_words(user, session, pair)
        assert picked and not ({w.id for w in picked} & just_now), "доска взяла слово 30 с спустя"
