"""
Что круг ЗАПИСЫВАЕТ человеку: итоги, серия, сезон, прогресс по словам.

ЗАЧЕМ ОТДЕЛЬНЫЙ ФАЙЛ. Приёмка `audit_accounting` сверяет пять слоёв на
живых данных — и нашла шесть расхождений. Но живые данные написаны
ПРЕЖНИМИ версиями кода, и приёмка не отвечает на другой вопрос: пишет ли
верно СЕГОДНЯШНИЙ код. Нынешние тесты на этот вопрос тоже не отвечали:

    grep по шести файлам тестов — `quizzes_passed` встречается 9 раз,
    и ВСЕ ДЕВЯТЬ раз это присваивание в условии сценария.
    Ни одной проверки ПОСЛЕ круга.

То есть завершённый круг мог не записать человеку ничего, и ни тесты, ни
приёмка данных этого не заметили бы: приёмка сверяет колонку с источником,
а если круг не тронул ни колонку, ни источник — они сходятся.

Поэтому здесь круг играется целиком через настоящий диспетчер, а потом
сверяется то же, что сверяет приёмка, — но на свежей записи.
"""

import pytest
from sqlalchemy import func, select

from app.core.clock import utcnow, utctoday
from app.database.enums import CEFRLevel, QuizMode
from app.database.models import (
    MonthlyStats, QuizQuestion, QuizSession, User, UserWord, Word,
)
from app.services.streak_service import current_streak
from tests.conftest import build_groups, make_word
from tests.scenario import (
    make_bot, make_dispatcher, press, reset_state, text_update,
)

pytestmark = pytest.mark.asyncio

WORDS = 40
ROUND_LENGTH = 6


@pytest.fixture
async def stage(session):
    bot, recorder = make_bot()
    dp = make_dispatcher(session)
    await reset_state(dp)
    return dp, bot, recorder


async def _ready(session, user) -> None:
    for i in range(WORDS):
        session.add(make_word(f"Wort{i:03d}", level=CEFRLevel.A1))
    await build_groups(session, ["de"])

    user.level = CEFRLevel.A1
    user.quiz_mode = QuizMode.LEVEL
    user.quiz_word_count = ROUND_LENGTH
    user.audio_enabled = False
    user.quiz_channels = "t"
    user.match_in_round = False      # доска проверена отдельно
    user.quizzes_passed = 0
    user.words_learned = 0
    user.streak_days = 0
    user.best_streak_days = 0
    user.last_active_date = None
    await session.commit()


async def _play_round(dp, bot, recorder, user, *, correct: bool = False) -> None:
    """
    Сыграть круг целиком.

    `correct=True` отвечает ВЕРНО — вариант берётся по `correct_word_id` из
    состояния. Это нужно не для красоты: проверка «выучено = выученным
    словам» на круге с неверными ответами сверяет ноль с нулём и прошла бы
    даже со снятой строкой записи. Чтобы она что-то держала, круг должен
    действительно выучивать слово.
    """
    from app.locales import get_text

    context = dp.fsm.get_context(bot, chat_id=user.id, user_id=user.id)
    await dp.feed_update(bot, text_update(user.id, get_text("btn_learn_words", "ru")))
    for step in range(ROUND_LENGTH):
        options = [b for b in recorder.buttons() if b.startswith("answer_")]
        assert options, f"шаг {step + 1}: вариантов ответа нет"

        if correct:
            wanted = f"answer_{(await context.get_data()).get('correct_word_id')}"
            assert wanted in options, (
                f"шаг {step + 1}: верного варианта нет среди {options}"
            )
            choice = wanted
        else:
            choice = options[0]

        await dp.feed_update(bot, press(user.id, choice))
        await dp.feed_update(bot, press(user.id, "next_question"))


async def _seen_before(session, user, *, dated: bool) -> list[Word]:
    """
    Завести ряды прогресса ЗАРАНЕЕ — чтобы круг пошёл по пути ОБНОВЛЕНИЯ, а
    не создания.

    Разница решает. На чистом человеке все ряды создаются в ходе круга, а
    создание ставит и дату, и счётчики само. Обе проверки на эти поля
    прошли со сломанным обновлением: `last_seen_at = now` снят — зелено,
    `times_shown += 1` снят и `times_correct` растёт всегда — тоже зелено.
    Проверялся путь, которым ряд с историей не ходит.

    `dated=False` воспроизводит ровно те 60 рядов, что нашла приёмка:
    показы есть, даты показа нет.
    """
    words = (await session.execute(select(Word).order_by(Word.id))).scalars().all()
    for word in words:
        session.add(UserWord(
            user_id=user.id, word_id=word.id, learning_lang="de",
            correct_streak=0, times_shown=2, times_correct=1, learned=False,
            last_seen_at=utcnow() if dated else None,
        ))
    await session.commit()
    return words


async def _almost_learned(session, user) -> int:
    """
    Подготовить слова, которым до «выучено» остался один верный ответ:
    серия 2 из 3 и знакомство вчера (сегодняшнее знакомство выучиться не
    даёт нарочно). Возвращает, сколько таких рядов.
    """
    from datetime import timedelta

    from app.core.clock import utcnow

    words = (await session.execute(select(Word).order_by(Word.id))).scalars().all()
    yesterday = utcnow() - timedelta(days=2)
    for word in words:
        session.add(UserWord(
            user_id=user.id, word_id=word.id, learning_lang="de",
            correct_streak=2, times_shown=2, times_correct=2, learned=False,
            created_at=yesterday, last_seen_at=yesterday,
        ))
    await session.commit()
    return len(words)


# ============================================================================
# СЛОЙ «ЧЕЛОВЕК»
# ============================================================================

async def test_a_finished_round_is_counted(session, user, stage):
    """
    Самое простое, чего не проверял никто: круг пройден — счётчик вырос.

    И вырос РОВНО на один: приёмка нашла человека с 109 завершёнными
    занятиями при записанных 54, то есть прежняя версия увеличивала
    счётчик не на каждом завершении.
    """
    dp, bot, recorder = stage
    await _ready(session, user)
    await _play_round(dp, bot, recorder, user)

    await session.refresh(user)
    assert user.quizzes_passed == 1, (
        f"круг пройден, а счётчик кругов {user.quizzes_passed}"
    )

    completed = (await session.execute(
        select(func.count()).select_from(QuizSession).where(
            QuizSession.user_id == user.id,
            QuizSession.completed_at.isnot(None),
        )
    )).scalar()
    assert user.quizzes_passed == completed, (
        f"колонка {user.quizzes_passed}, завершённых занятий {completed}"
    )


async def test_the_learned_count_matches_the_words(session, user, stage):
    """
    `words_learned` должно равняться выученным словам, а не жить само.

    Приёмка нашла у одного человека 225 при НУЛЕ выученных слов по всем
    языкам сразу — число кратно двадцати пяти, его написало какое-то
    прежнее правило.

    Круг играется ВЕРНЫМИ ответами по словам, которым до «выучено» остался
    один ответ: иначе выученных ноль, проверка сверяет ноль с нулём и
    прошла бы даже со снятой строкой записи.
    """
    dp, bot, recorder = stage
    await _ready(session, user)
    await _almost_learned(session, user)
    await _play_round(dp, bot, recorder, user, correct=True)

    await session.refresh(user)
    real = (await session.execute(
        select(func.count()).select_from(UserWord).where(
            UserWord.user_id == user.id,
            UserWord.learning_lang == user.learning_lang,
            UserWord.learned.is_(True),
        )
    )).scalar()
    assert real > 0, (
        "круг верными ответами не выучил ни слова — проверка вхолостую"
    )
    assert user.words_learned == real, (
        f"записано выученных {user.words_learned}, на деле {real}"
    )


async def test_the_shown_accuracy_matches_the_answers(session, user, stage):
    dp, bot, recorder = stage
    await _ready(session, user)
    await _play_round(dp, bot, recorder, user)

    await session.refresh(user)
    answered, correct = (await session.execute(
        select(func.coalesce(func.sum(QuizSession.answered_questions), 0),
               func.coalesce(func.sum(QuizSession.correct_answers), 0))
        .where(QuizSession.user_id == user.id,
               QuizSession.completed_at.isnot(None))
    )).one()
    expected = int(correct / answered * 100) if answered else 0
    assert user.success_rate == expected, (
        f"показывается {user.success_rate}%, по ответам {expected}%"
    )


# ============================================================================
# СЕРИЯ ДНЕЙ
# ============================================================================

async def test_the_first_round_starts_the_streak(session, user, stage):
    dp, bot, recorder = stage
    await _ready(session, user)
    await _play_round(dp, bot, recorder, user)

    await session.refresh(user)
    assert user.streak_days == 1
    assert user.last_active_date == utctoday()
    assert current_streak(user) == 1, "серия не читается как живая"


async def test_the_best_streak_is_written_by_the_round(session, user, stage):
    """
    Колонка `best_streak_days` существовала с начала и была НУЛЁМ у всех
    233 человек: её не писал никто. Теперь пишет отметка дня, и проверяет
    это круг, а не только тест на функцию.
    """
    dp, bot, recorder = stage
    await _ready(session, user)
    await _play_round(dp, bot, recorder, user)

    await session.refresh(user)
    assert user.best_streak_days == 1, (
        f"лучшая серия не записана: {user.best_streak_days}"
    )


async def test_a_second_round_today_counts_but_does_not_grow_the_streak(
    session, user, stage,
):
    """
    71% дней — это два круга и больше. Второй круг должен дать второй
    пройденный круг, но НЕ второй день серии.
    """
    dp, bot, recorder = stage
    await _ready(session, user)
    await _play_round(dp, bot, recorder, user)
    await _play_round(dp, bot, recorder, user)

    await session.refresh(user)
    assert user.quizzes_passed == 2, f"кругов {user.quizzes_passed}, а сыграно 2"
    assert user.streak_days == 1, (
        f"два круга за день дали серию {user.streak_days}"
    )


# ============================================================================
# СЛОЙ «ЗАНЯТИЕ» И «ВОПРОС»
# ============================================================================

async def test_the_session_counters_match_the_answer_rows(session, user, stage):
    dp, bot, recorder = stage
    await _ready(session, user)
    await _play_round(dp, bot, recorder, user)

    quiz = (await session.execute(
        select(QuizSession).where(QuizSession.user_id == user.id)
        .order_by(QuizSession.id.desc()).limit(1)
    )).scalar_one()

    rows, correct = (await session.execute(
        select(func.count(),
               func.count().filter(QuizQuestion.is_correct.is_(True)))
        .where(QuizQuestion.session_id == quiz.id)
    )).one()

    assert quiz.answered_questions == rows, (
        f"в занятии {quiz.answered_questions} ответов, строк {rows}"
    )
    assert quiz.correct_answers == correct
    assert quiz.is_completed and quiz.completed_at is not None


async def test_every_shown_word_gets_a_date(session, user, stage):
    """
    Приёмка нашла 60 рядов с показами и ПУСТОЙ датой показа. С подбором по
    времени такое слово просрочено ВСЕГДА и лезет вперёд остальных —
    человек получал бы одни и те же слова.

    Ряды заводятся заранее ИМЕННО В ТАКОМ ВИДЕ. Первая редакция теста
    играла круг на чистом человеке и прошла даже со снятой строкой
    `last_seen_at = now` в записи ответа: на чистом человеке ряды СОЗДАЮТСЯ
    в ходе круга, а создание ставит дату само. Проверялось создание, а не
    ответ.
    """
    dp, bot, recorder = stage
    await _ready(session, user)

    words = await _seen_before(session, user, dated=False)

    before = (await session.execute(
        select(func.count()).select_from(UserWord).where(
            UserWord.user_id == user.id, UserWord.last_seen_at.is_(None),
        )
    )).scalar()
    assert before == len(words), "подготовка не удалась: даты всё-таки есть"

    await _play_round(dp, bot, recorder, user)

    # Слово, по которому в круге был ответ, обязано получить дату
    answered = (await session.execute(
        select(QuizQuestion.word_id)
        .join(QuizSession, QuizSession.id == QuizQuestion.session_id)
        .where(QuizSession.user_id == user.id,
               QuizQuestion.answered_at.isnot(None))
    )).scalars().all()
    assert answered, "в круге не записано ни одного ответа"

    undated = (await session.execute(
        select(func.count()).select_from(UserWord).where(
            UserWord.user_id == user.id,
            UserWord.word_id.in_(answered),
            UserWord.last_seen_at.is_(None),
        )
    )).scalar()
    assert undated == 0, (
        f"отвеченных слов без даты показа: {undated} из {len(answered)}"
    )


async def test_no_word_row_claims_more_correct_than_shown(session, user, stage):
    """
    Верных не может быть больше показов. Ряды заводятся заранее — иначе
    круг идёт путём создания, а не обновления, и проверка проходит даже
    когда обновление растит верные без показов (так и вышло в первой
    редакции).
    """
    dp, bot, recorder = stage
    await _ready(session, user)
    words = await _seen_before(session, user, dated=True)
    await _play_round(dp, bot, recorder, user)

    shown_before = 2 * len(words)
    shown_now = (await session.execute(
        select(func.coalesce(func.sum(UserWord.times_shown), 0))
        .where(UserWord.user_id == user.id)
    )).scalar()
    assert shown_now == shown_before + ROUND_LENGTH, (
        f"показов {shown_now}, ожидалось {shown_before + ROUND_LENGTH}: "
        f"круг не досчитал показы"
    )

    broken = (await session.execute(
        select(func.count()).select_from(UserWord).where(
            UserWord.user_id == user.id,
            UserWord.times_correct > UserWord.times_shown,
        )
    )).scalar()
    assert broken == 0, f"рядов с верными больше показов: {broken}"


# ============================================================================
# СЛОЙ «СЕЗОН»
# ============================================================================

async def test_the_round_lands_in_the_season(session, user, stage):
    """
    Месячный ряд должен появиться сам, с языком круга, и его балл — быть
    не меньше награды за круг.
    """
    dp, bot, recorder = stage
    await _ready(session, user)
    await _play_round(dp, bot, recorder, user)

    stat = (await session.execute(
        select(MonthlyStats).where(MonthlyStats.user_id == user.id)
    )).scalars().all()
    assert len(stat) == 1, f"месячных рядов {len(stat)}, ожидался один"

    row = stat[0]
    assert row.learning_lang == user.learning_lang
    assert row.monthly_quizzes == 1, f"кругов в сезоне {row.monthly_quizzes}"
    assert row.total_questions == ROUND_LENGTH
    assert row.monthly_score >= MonthlyStats.POINTS_PER_ROUND, (
        f"балл {row.monthly_score} меньше награды за круг"
    )
    assert 0 <= row.monthly_avg_percent <= 100


async def test_the_season_accuracy_matches_its_own_counters(session, user, stage):
    dp, bot, recorder = stage
    await _ready(session, user)
    await _play_round(dp, bot, recorder, user)

    row = (await session.execute(
        select(MonthlyStats).where(MonthlyStats.user_id == user.id)
    )).scalar_one()
    expected = (int(row.total_correct / row.total_questions * 100)
                if row.total_questions else 0)
    assert row.monthly_avg_percent == expected, (
        f"в сезоне {row.monthly_avg_percent}%, по своим же числам {expected}%"
    )


# ============================================================================
# БРОШЕННЫЙ КРУГ НЕ ПИШЕТ ИТОГОВ
# ============================================================================

async def test_an_abandoned_round_is_not_counted(session, user, stage):
    """
    Обратная сторона: пока круг не дошёл до конца, итогов человеку быть не
    должно. Иначе счётчик кругов рос бы от начатых, а не пройденных — и
    это ровно то расхождение, что приёмка нашла у 41 человека.
    """
    from app.locales import get_text

    dp, bot, recorder = stage
    await _ready(session, user)

    await dp.feed_update(bot, text_update(user.id, get_text("btn_learn_words", "ru")))
    for _ in range(2):
        options = [b for b in recorder.buttons() if b.startswith("answer_")]
        await dp.feed_update(bot, press(user.id, options[0]))
        await dp.feed_update(bot, press(user.id, "next_question"))

    await session.refresh(user)
    assert user.quizzes_passed == 0, (
        f"круг брошен на середине, а кругов записано {user.quizzes_passed}"
    )
    assert user.streak_days == 0, "брошенный круг отметил день"
