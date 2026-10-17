"""
Учёт рейтинга после аудита 14 октября: шесть находок, каждая — замером.

    участие   таблица и карточка считали место среди всех рядов месяца, а
              закрытие — среди занимавшихся: человек с одними баллами за
              жалобы стоял первым с 🥇 и не получал ничего, двое со 100
              видели «#2» и получали золото
    гонка     «перевод» и «звук» одного слова, принятые одновременно,
              платили оба: report_bonus 30 за одно слово
    слова     месячные «выученные слова» пересчитывались раз в десять
              занятий: выучено 6, записано 2, балл 55 вместо 67
    переход   «+3 за слово» платилось в каждом месяце, где выученное слово
              показали снова, — в «за всё время» дважды
    уровень   устаревшая кнопка «перейти на A2» опускала человека с B1;
              предложение приходило в режимах, где уровень не подбирает слов
"""

import asyncio
from datetime import datetime, time, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.bot.handlers.admin import _claim_reports, _reward_reporters
from app.core.clock import utcnow
from app.database.enums import CEFRLevel, QuizMode
from app.database.models import (
    MonthlyAward, MonthlyStats, QuizQuestion, QuizSession,
    TranslationReport, User, UserWord, Word,
)
from app.services.level_service import (
    MIN_ANSWERS, decline_level, raise_level, should_offer_next_level,
)
from app.services.monthly_leaderboard_service import (
    create_new_season, finalize_season, get_monthly_leaderboard,
    get_or_create_current_season, get_user_monthly_rank, month_words,
    update_monthly_stats,
)
from app.services.quiz_service import update_word_progress
from tests.conftest import make_word


async def _people(session, ids, lang="de"):
    for uid in ids:
        session.add(User(id=uid, first_name=f"U{uid}", learning_lang=lang,
                         native_lang="ru", interface_language="ru"))
    await session.commit()


async def _words(session, n):
    for i in range(n):
        session.add(make_word(f"Wort{i}", level=CEFRLevel.A1, ru=f"слово{i}"))
    await session.commit()
    return (await session.execute(select(Word).order_by(Word.id))).scalars().all()


# ============================================================================
# 1. ОДНО ПРАВИЛО УЧАСТИЯ: ТАБЛИЦА, КАРТОЧКА И ЗАКРЫТИЕ
# ============================================================================

# (id, баллы, занятий): 1 — одни жалобы, 5 — пустой ряд
_MONTH = [(1, 200, 0), (2, 100, 5), (3, 100, 5), (4, 80, 4), (5, 0, 0), (6, 50, 2)]


async def _month(session):
    season = await create_new_season(2026, 3, session)
    await _people(session, [uid for uid, _, _ in _MONTH])
    for uid, score, quizzes in _MONTH:
        session.add(MonthlyStats(
            user_id=uid, season_id=season.id, learning_lang="de",
            monthly_score=score, monthly_quizzes=quizzes,
            report_bonus=score if quizzes == 0 else 0,
        ))
    await session.commit()
    return season


async def test_table_card_and_close_agree_on_places(session):
    season = await _month(session)

    board = await get_monthly_leaderboard(session, season.id, learning_lang="de")
    shown = {row["user_id"]: row["rank"] for row in board}
    # ПОБЕДИТЕЛЬ ОДИН (17.10): равные 100 у 2 и 3 разведены — 2 набрал раньше
    assert shown == {2: 1, 3: 2, 4: 3, 6: 4}, (
        f"в таблице {shown}: человек без занятий не должен стоять в месяце"
    )

    for uid, rank in shown.items():
        card = await get_user_monthly_rank(uid, session, season.id, learning_lang="de")
        assert (card["rank"], card["total_users"]) == (rank, 4), (
            f"карточка {uid}: {card['rank']} из {card['total_users']}, "
            f"в таблице {rank} из 4"
        )

    await finalize_season(season.id, session)

    stats = {s.user_id: s.final_rank for s in
             (await session.execute(select(MonthlyStats))).scalars()}
    awards = {a.user_id: (a.rank, a.award_type) for a in
              (await session.execute(select(MonthlyAward))).scalars()}
    awards = {(a.user_id, a.rank, a.award_type, a.learning_lang) for a in
              (await session.execute(select(MonthlyAward))).scalars()}
    # Медали — с 3 занятий (17.10): 6 с двумя занятиями в таблице стоит, в итогах нет.
    # У остальных место в итогах то же, что в таблице
    assert {uid: stats[uid] for uid in (2, 3, 4)} == {2: 1, 3: 2, 4: 3}, "итог разошёлся с таблицей"
    assert stats[1] is None and stats[5] is None and stats[6] is None
    assert awards == {(2, 1, "gold", "*"), (3, 2, "silver", "*"), (4, 3, "bronze", "*"),
                      (2, 1, "crown", "de")}, awards


async def test_points_without_a_lesson_are_not_a_place(session):
    """Баллы за жалобы без занятия — не место: карточка зовёт на занятие."""
    season = await _month(session)
    assert await get_user_monthly_rank(1, session, season.id, learning_lang="de") is None
    assert await get_user_monthly_rank(5, session, season.id, learning_lang="de") is None


async def test_card_names_the_points_already_credited(session):
    """Карточка не делает вид, что баллов нет: «200 начислены, пройдите занятие»."""
    from app.bot.handlers.leaderboard.monthly import month_screen
    from app.locales import get_text

    season = await _month(session)
    lonely = await session.get(User, 1)
    empty = await session.get(User, 5)

    card = await month_screen(lonely, session, season, "ru")
    assert get_text("rating_join_by_lesson", "ru", score=200) in card, card
    assert get_text("rating_start_quiz", "ru") not in card

    # Пустой ряд (0 баллов) — прежний зов на первое занятие
    card = await month_screen(empty, session, season, "ru")
    assert get_text("rating_start_quiz", "ru") in card, card


# ============================================================================
# 2. ОПЛАТА ЖАЛОБЫ: ДВА ВИДА ОДНОГО СЛОВА ОДНОВРЕМЕННО — ОДНА ОПЛАТА
# ============================================================================

async def _race(session, engine, *, with_row: bool):
    season = await get_or_create_current_season(session)
    await _people(session, [7], lang="en")
    word = (await _words(session, 1))[0]
    for kind in ("text", "audio"):
        session.add(TranslationReport(user_id=7, word_id=word.id, kind=kind,
                                      status="pending"))
    if with_row:
        session.add(MonthlyStats(user_id=7, season_id=season.id, learning_lang="en",
                                 monthly_quizzes=1, monthly_score=10))
    await session.commit()

    maker = async_sessionmaker(engine, expire_on_commit=False)

    async def approve(kind, hold):
        async with maker() as s:
            claimed = await _claim_reports(s, word.id, (kind,), "fixed")
            rewarded, _ = await _reward_reporters(s, word.id, claimed)
            # Держим транзакцию открытой: второе решение успевает дойти до
            # проверки «уже платили», пока первое не записано
            await asyncio.sleep(hold)
            await s.commit()
            return rewarded

    results = await asyncio.gather(approve("text", 0.3), approve("audio", 0.0))
    paid = [r for r in results if r]
    row = (await session.execute(
        select(MonthlyStats).where(MonthlyStats.user_id == 7)
        .execution_options(populate_existing=True)
    )).scalar_one()
    return paid, row


async def test_two_kinds_at_once_pay_once(session, engine):
    paid, row = await _race(session, engine, with_row=True)
    assert len(paid) == 1, f"оплат {len(paid)}: одно слово оплачено дважды"
    assert row.report_bonus == 15


async def test_two_kinds_at_once_without_a_row_do_not_crash(session, engine):
    """Ряда месяца нет: прежде второе решение падало на уникальности."""
    paid, row = await _race(session, engine, with_row=False)
    assert len(paid) == 1
    assert row.report_bonus == 15 and row.monthly_score == 15


# ============================================================================
# 3–4. СЛОВА МЕСЯЦА: НА КАЖДОМ ЗАНЯТИИ И ПО ДАТЕ ПЕРЕХОДА
# ============================================================================

def _quiz(uid):
    now = utcnow()
    return QuizSession(user_id=uid, level=CEFRLevel.A1, learning_lang="de",
                       native_lang="ru", total_questions=10, answered_questions=10,
                       correct_answers=10, is_completed=True, started_at=now,
                       completed_at=now, quiz_mode="level")


def _learned(uid, word, at):
    return UserWord(user_id=uid, word_id=word.id, learning_lang="de",
                    correct_streak=3, times_shown=3, times_correct=3,
                    last_seen_at=utcnow(), learned=True, learned_at=at,
                    created_at=utcnow() - timedelta(days=10))


async def test_words_counted_on_every_lesson(session):
    await _people(session, [8])
    words = await _words(session, 6)
    now = utcnow()

    for word in words[:2]:
        session.add(_learned(8, word, now))
    first = _quiz(8)
    session.add(first)
    await session.commit()
    stat = await update_monthly_stats(8, session, quiz_session_id=first.id)
    assert stat.monthly_words == 2

    for word in words[2:]:
        session.add(_learned(8, word, now))
    second = _quiz(8)
    session.add(second)
    await session.commit()
    stat = await update_monthly_stats(8, session, quiz_session_id=second.id)
    assert stat.monthly_words == 6, (
        f"после второго занятия слов {stat.monthly_words} из 6: пересчёт отстаёт"
    )


async def test_word_learned_last_month_is_not_paid_again(session):
    """Выучено в прошлом месяце, показано сейчас — в этом месяце не платится."""
    season = await get_or_create_current_season(session)
    await _people(session, [9])
    old, new = await _words(session, 2)
    last_month = datetime.combine(season.start_date, time()) - timedelta(days=3)
    session.add(_learned(9, old, last_month))
    session.add(_learned(9, new, utcnow()))
    await session.commit()
    assert await month_words(session, 9, "de", season) == 1


async def test_learned_at_follows_the_learned_flag(session):
    await _people(session, [10])
    word = (await _words(session, 1))[0]
    session.add(UserWord(user_id=10, word_id=word.id, learning_lang="de",
                         correct_streak=2, times_shown=2, times_correct=2,
                         last_seen_at=utcnow() - timedelta(days=30),
                         created_at=utcnow() - timedelta(days=30), learned=False))
    await session.commit()

    async def row():
        return (await session.execute(
            select(UserWord).where(UserWord.user_id == 10)
            .execution_options(populate_existing=True))).scalar_one()

    await update_word_progress(10, word.id, True, session, "de")
    first = await row()
    assert first.learned and first.learned_at is not None
    stamp = first.learned_at

    # Ещё верный ответ по выученному — дата перехода стоит на месте
    await update_word_progress(10, word.id, True, session, "de")
    assert (await row()).learned_at == stamp

    # Промах снимает «выучено» — и дату
    await update_word_progress(10, word.id, False, session, "de")
    after = await row()
    assert not after.learned and after.learned_at is None


# ============================================================================
# 6. УРОВЕНЬ: УСТАРЕВШИЕ КНОПКИ И РЕЖИМЫ БЕЗ УРОВНЯ
# ============================================================================

async def test_stale_raise_button_does_not_lower_the_level(session, user):
    user.level = CEFRLevel.B1
    await session.commit()
    assert await raise_level(user, session, CEFRLevel.A2) is False
    assert user.level is CEFRLevel.B1


async def test_raise_to_the_next_level_works(session, user):
    user.level = CEFRLevel.A1
    await session.commit()
    assert await raise_level(user, session, CEFRLevel.A2) is True
    assert user.level is CEFRLevel.A2


async def test_stale_decline_records_nothing(session, user):
    """Отказ от «A1 → A2», нажатый уже на A2, — не отказ от «A2 → B1»."""
    user.level = CEFRLevel.A2
    await session.commit()
    assert await decline_level(user, session, offered=CEFRLevel.A2) is False
    assert user.level_offer_declined is None


async def _easy(session, user):
    word = (await _words(session, 1))[0]
    quiz = QuizSession(user_id=user.id, learning_lang="de", level=user.level,
                       total_questions=MIN_ANSWERS)
    session.add(quiz)
    await session.commit()
    start = utcnow()
    for i in range(MIN_ANSWERS):
        session.add(QuizQuestion(session_id=quiz.id, word_id=word.id, is_correct=True,
                                 answered_at=start + timedelta(seconds=i)))
    await session.commit()


async def test_no_level_offer_where_level_picks_no_words(session, user):
    user.level = CEFRLevel.A1
    await session.commit()
    await _easy(session, user)

    user.quiz_mode = QuizMode.LEVEL
    assert await should_offer_next_level(user, session) is CEFRLevel.A2

    for mode in (QuizMode.ALL_WORDS, QuizMode.DIFFICULT):
        user.quiz_mode = mode
        assert await should_offer_next_level(user, session) is None, mode

    user.quiz_mode = QuizMode.CATEGORY
    user.quiz_category = "food"
    assert await should_offer_next_level(user, session) is None
    # Тема не выбрана — подбор откатывается на уровень, и уровень значим
    user.quiz_category = None
    assert await should_offer_next_level(user, session) is CEFRLevel.A2


# ============================================================================
# ПОРЯДОК ПОЧИНКИ: ДАТА ПЕРЕХОДА РАНЬШЕ МЕСЯЧНОГО БАЛЛА
#
# Репетиция 14.10: после миграции `learned_at` пуст у всех выученных, а
# починка пересчитывала месячный балл ДО того, как заполнить дату, — первый
# `--apply` обнулял людям слова месяца. Один проход обязан дать верное.
# ============================================================================

async def test_one_repair_pass_gives_the_month_its_words(session, engine, monkeypatch):
    from app.scripts import repair_accounting

    season = await get_or_create_current_season(session)
    await _people(session, [11])
    word = (await _words(session, 1))[0]
    session.add(_quiz(11))
    session.add(_learned(11, word, None))   # как после миграции
    session.add(MonthlyStats(user_id=11, season_id=season.id, learning_lang="de",
                             monthly_quizzes=1, monthly_score=10))
    await session.commit()

    monkeypatch.setattr(repair_accounting, "AsyncSessionLocal",
                        async_sessionmaker(engine, expire_on_commit=False))
    await repair_accounting.run(apply=True, all_seasons=False)

    session.expire_all()
    stat = (await session.execute(
        select(MonthlyStats).where(MonthlyStats.user_id == 11)
    )).scalar_one()
    assert stat.monthly_words == 1, (
        f"слов месяца {stat.monthly_words}: балл пересчитан до даты перехода"
    )
