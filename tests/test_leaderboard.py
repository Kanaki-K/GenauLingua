"""Месячный рейтинг: бонус за обратный режим, точность, сезоны по языкам."""

from datetime import date, timedelta

import pytest
from sqlalchemy import select

from app.core.clock import utcnow
from app.database.enums import CEFRLevel, TranslationMode
from app.database.models import MonthlySeason, MonthlyStats, QuizSession, User, UserWord
from app.services.monthly_leaderboard_service import (
    create_new_season,
    finalize_season,
    get_current_season,
    get_monthly_leaderboard,
    get_or_create_current_season,
    get_user_monthly_rank,
    update_monthly_stats,
)
from app.services.word_stats import (
    MIN_SHOWS_FOR_DIFFICULTY,
    wilson_lower_bound,
    wilson_upper_bound,
)


async def _season(session):
    return await get_or_create_current_season(session)


def _completed_quiz(user_id, *, learning="de", native="ru", reverse=False,
                    planned=25, answered=25, correct=20):
    now = utcnow()
    return QuizSession(
        user_id=user_id,
        level=CEFRLevel.A1,
        learning_lang=learning,
        native_lang=native,
        is_reverse=reverse,
        total_questions=planned,
        answered_questions=answered,
        correct_answers=correct,
        is_completed=True,
        started_at=now,
        completed_at=now,
        quiz_mode="level",
    )


class TestSeasonCreation:
    async def test_existing_season_is_returned_not_crashed(self, session):
        """
        create_new_season дважды вызывал scalar_one_or_none() на одном Result:
        первый вызов исчерпывал его, второй падал с ResourceClosedError.
        """
        first = await create_new_season(2026, 5, session)
        second = await create_new_season(2026, 5, session)

        assert second is not None
        assert second.id == first.id

    async def test_creating_new_season_deactivates_previous(self, session):
        old = await create_new_season(2026, 4, session)
        new = await create_new_season(2026, 5, session)

        await session.refresh(old)
        assert old.is_active is False
        assert new.is_active is True
        assert (await get_current_season(session)).id == new.id


class TestReverseBonus:
    """
    Бонус за обратный режим не начислялся никогда: код сравнивал
    translation_mode.value со строками в нижнем регистре, а значения enum
    в верхнем. Английский и турецкий в списке вообще не фигурировали.
    """

    async def test_reverse_quiz_counted(self, session, user):
        await _season(session)

        quiz = _completed_quiz(user.id, reverse=True)
        session.add(quiz)
        await session.commit()

        stat = await update_monthly_stats(user.id, session, quiz_session_id=quiz.id)
        assert stat.monthly_reverse == 1

    async def test_forward_quiz_not_counted_as_reverse(self, session, user):
        await _season(session)

        quiz = _completed_quiz(user.id, reverse=False)
        session.add(quiz)
        await session.commit()

        stat = await update_monthly_stats(user.id, session, quiz_session_id=quiz.id)
        assert stat.monthly_reverse == 0

    @pytest.mark.parametrize("learning,native", [
        ("de", "ru"), ("de", "uk"), ("de", "en"), ("de", "tr"),
        ("en", "ru"), ("tr", "uk"),
    ])
    async def test_reverse_counted_for_every_language_pair(self, session, user, learning, native):
        await _season(session)

        user.learning_lang, user.native_lang = learning, native
        await session.commit()

        quiz = _completed_quiz(user.id, learning=learning, native=native, reverse=True)
        session.add(quiz)
        await session.commit()

        stat = await update_monthly_stats(user.id, session, quiz_session_id=quiz.id)
        assert stat.monthly_reverse == 1, f"{learning}->{native} не учтён"

    async def test_reverse_adds_five_points(self, session, user):
        await _season(session)

        quiz = _completed_quiz(user.id, reverse=True)
        session.add(quiz)
        await session.commit()

        stat = await update_monthly_stats(user.id, session, quiz_session_id=quiz.id)
        # 10 за викторину + 5 за обратный режим + 3 за день стрика
        assert stat.monthly_score >= 15


class TestAccuracyAccounting:
    """
    total_questions хранит плановое число вопросов. Если считать по нему,
    брошенная викторина выглядит как сплошные ошибки: на проде это давало
    60.7% вместо реальных 88.1%.
    """

    async def test_abandoned_quiz_does_not_destroy_accuracy(self, session, user):
        await _season(session)

        # Планировалось 25, отвечено 4, все верно
        quiz = _completed_quiz(user.id, planned=25, answered=4, correct=4)
        session.add(quiz)
        await session.commit()

        stat = await update_monthly_stats(user.id, session, quiz_session_id=quiz.id)

        assert stat.total_questions == 4, "учитываться должны отвеченные, не плановые"
        assert stat.monthly_avg_percent == 100

    async def test_accuracy_adds_to_the_score_without_a_cliff(self, session, user):
        """
        Прибавка за точность начисляется ПЛАВНО, от порога 60%.

        Прежде здесь проверялся обрыв: «100% ≥ 90 → бонус 50», и тест
        требовал `monthly_score >= 50`. Обрыв убран — человек с 89% видел,
        что двадцать баллов пропали из-за одного вопроса, и это читалось
        как несправедливость, даже будучи описанным в правилах.

        Теперь проверяется то, ради чего прибавка и существует: она есть,
        она растёт вместе с точностью и не прыгает скачком.
        """
        await _season(session)

        quiz = _completed_quiz(user.id, planned=25, answered=10, correct=10)
        session.add(quiz)
        await session.commit()

        stat = await update_monthly_stats(user.id, session, quiz_session_id=quiz.id)
        assert stat.monthly_avg_percent == 100

        perfect = stat.calculate_monthly_score()

        # тот же объём, но точность на пороге — прибавки быть не должно
        stat.monthly_avg_percent = MonthlyStats.ACCURACY_FLOOR
        at_floor = stat.calculate_monthly_score()
        assert perfect > at_floor, "за точность не начислено ничего"

        # и соседние проценты отличаются чуть-чуть, а не скачком
        stat.monthly_avg_percent = 89
        just_below = stat.calculate_monthly_score()
        stat.monthly_avg_percent = 90
        just_above = stat.calculate_monthly_score()
        assert 0 <= just_above - just_below <= 2, "обрыв на 90% вернулся"

    async def test_session_accuracy_property(self, session, user):
        quiz = _completed_quiz(user.id, planned=25, answered=8, correct=6)
        assert quiz.accuracy_percent == pytest.approx(75.0)

        empty = _completed_quiz(user.id, planned=25, answered=0, correct=0)
        assert empty.accuracy_percent == 0.0


class TestIdempotency:
    async def test_same_quiz_counted_once(self, session, user):
        await _season(session)

        quiz = _completed_quiz(user.id)
        session.add(quiz)
        await session.commit()

        first = await update_monthly_stats(user.id, session, quiz_session_id=quiz.id)
        assert first.monthly_quizzes == 1

        second = await update_monthly_stats(user.id, session, quiz_session_id=quiz.id)
        assert second.monthly_quizzes == 1, "повторный учёт той же викторины"


class TestPerLanguageSeasons:
    async def test_stats_are_separate_per_language(self, session, user):
        await _season(session)

        de_quiz = _completed_quiz(user.id, learning="de")
        en_quiz = _completed_quiz(user.id, learning="en", native="ru")
        session.add_all([de_quiz, en_quiz])
        await session.commit()

        await update_monthly_stats(user.id, session, quiz_session_id=de_quiz.id)
        await update_monthly_stats(user.id, session, quiz_session_id=en_quiz.id)

        stats = (await session.execute(
            select(MonthlyStats).where(MonthlyStats.user_id == user.id)
        )).scalars().all()

        by_lang = {s.learning_lang: s for s in stats}
        assert set(by_lang) == {"de", "en"}
        assert by_lang["de"].monthly_quizzes == 1
        assert by_lang["en"].monthly_quizzes == 1

    async def test_leaderboard_filters_by_language(self, session):
        season = await _season(session)

        for uid, lang, score in [(1, "de", 100), (2, "de", 50), (3, "en", 200)]:
            session.add(User(id=uid, first_name=f"U{uid}", learning_lang=lang,
                             native_lang="ru", interface_language="ru"))
        await session.commit()

        for uid, lang, score in [(1, "de", 100), (2, "de", 50), (3, "en", 200)]:
            session.add(MonthlyStats(user_id=uid, season_id=season.id,
                                     learning_lang=lang, monthly_score=score))
        await session.commit()

        de_board = await get_monthly_leaderboard(session, season.id, learning_lang="de")
        en_board = await get_monthly_leaderboard(session, season.id, learning_lang="en")

        assert [r["user_id"] for r in de_board] == [1, 2]
        assert [r["user_id"] for r in en_board] == [3]

    async def test_rank_computed_within_language(self, session):
        season = await _season(session)

        session.add_all([
            User(id=1, first_name="A", learning_lang="de", native_lang="ru", interface_language="ru"),
            User(id=2, first_name="B", learning_lang="en", native_lang="ru", interface_language="ru"),
        ])
        await session.commit()

        session.add_all([
            MonthlyStats(user_id=1, season_id=season.id, learning_lang="de", monthly_score=10),
            MonthlyStats(user_id=2, season_id=season.id, learning_lang="en", monthly_score=999),
        ])
        await session.commit()

        # Учащий немецкий первый среди немецких, несмотря на более высокий
        # балл учащего английский
        rank = await get_user_monthly_rank(1, session, season.id)
        assert rank["rank"] == 1
        assert rank["total_users"] == 1
        assert rank["learning_lang"] == "de"


class TestFinalizeSeason:
    async def test_awards_given_per_language(self, session):
        season = await create_new_season(2026, 3, session)

        users = [(1, "de", 300), (2, "de", 200), (3, "en", 150), (4, "en", 100)]
        for uid, lang, _ in users:
            session.add(User(id=uid, first_name=f"U{uid}", learning_lang=lang,
                             native_lang="ru", interface_language="ru"))
        await session.commit()

        for uid, lang, score in users:
            session.add(MonthlyStats(user_id=uid, season_id=season.id,
                                     learning_lang=lang, monthly_score=score))
        await session.commit()

        await finalize_season(season.id, session)

        # В каждом языке должен быть свой золотой призёр
        from app.database.models import MonthlyAward

        awards = (await session.execute(select(MonthlyAward))).scalars().all()
        golds = {a.user_id for a in awards if a.award_type == "gold"}
        assert golds == {1, 3}, "золото должно быть в каждом языке своё"

    async def test_final_ranks_restart_per_language(self, session):
        season = await create_new_season(2026, 3, session)

        users = [(1, "de", 300), (2, "de", 200), (3, "en", 150)]
        for uid, lang, _ in users:
            session.add(User(id=uid, first_name=f"U{uid}", learning_lang=lang,
                             native_lang="ru", interface_language="ru"))
        await session.commit()
        for uid, lang, score in users:
            session.add(MonthlyStats(user_id=uid, season_id=season.id,
                                     learning_lang=lang, monthly_score=score))
        await session.commit()

        await finalize_season(season.id, session)

        stats = {
            s.user_id: s
            for s in (await session.execute(select(MonthlyStats))).scalars().all()
        }
        assert stats[1].final_rank == 1
        assert stats[2].final_rank == 2
        assert stats[3].final_rank == 1, "нумерация должна начинаться заново в каждом языке"

    async def test_finalize_is_not_repeated(self, session):
        season = await create_new_season(2026, 3, session)
        session.add(User(id=1, first_name="A", learning_lang="de",
                         native_lang="ru", interface_language="ru"))
        await session.commit()
        session.add(MonthlyStats(user_id=1, season_id=season.id,
                                 learning_lang="de", monthly_score=100))
        await session.commit()

        await finalize_season(season.id, session)
        await finalize_season(season.id, session)

        from app.database.models import MonthlyAward

        awards = (await session.execute(select(MonthlyAward))).scalars().all()
        assert len(awards) == 1


class TestWilson:
    """
    Порог «больше 5 показов» превращал список сложных слов в статистический
    шум: при 8 показах 3/8 — обычный разброс для слова, которое знают на 70%.

    Для поиска трудных слов нужна ВЕРХНЯЯ граница интервала: слово трудное,
    если даже оптимистичная оценка его точности низкая. Нижняя граница здесь
    даёт обратный эффект — она штрафует малые выборки вниз, и шумное 3/8
    обгоняет честно трудное 13/28.
    """

    def test_ranking_puts_solid_evidence_above_noise(self):
        # gleich с прода: 46.4% при n=28 против шумного 3/8
        hard = wilson_upper_bound(13, 28)
        noisy = wilson_upper_bound(3, 8)
        assert hard < noisy, "честно трудное слово должно быть выше в списке"

    def test_lower_bound_would_rank_wrongly(self):
        """Фиксируем, почему нижняя граница для этой задачи не подходит."""
        assert wilson_lower_bound(3, 8) < wilson_lower_bound(13, 28)

    def test_wide_interval_for_small_sample(self):
        lo, hi = wilson_lower_bound(3, 8), wilson_upper_bound(3, 8)
        assert hi - lo > 0.4, "малая выборка должна давать широкий интервал"

    def test_narrow_interval_for_large_sample(self):
        lo, hi = wilson_lower_bound(130, 280), wilson_upper_bound(130, 280)
        assert hi - lo < 0.15

    def test_bounds_bracket_the_observed_rate(self):
        for successes, total in [(3, 8), (13, 28), (60, 100), (1, 20)]:
            p = successes / total
            assert wilson_lower_bound(successes, total) <= p <= wilson_upper_bound(successes, total)

    def test_edge_cases(self):
        assert wilson_lower_bound(0, 0) == 0.0
        assert wilson_upper_bound(0, 0) == 1.0
        assert wilson_lower_bound(0, 10) == 0.0
        assert 0 < wilson_lower_bound(10, 10) < 1
        assert wilson_upper_bound(10, 10) == pytest.approx(1.0)

    def test_threshold_is_meaningful(self):
        assert MIN_SHOWS_FOR_DIFFICULTY >= 15


class TestRepeatRoundDoesNotPay:
    """
    КРУГ-ПОВТОР ОШИБОК В МЕСЯЧНЫЙ ЗАЧЁТ НЕ ИДЁТ.

    Платить ему нельзя по сути: тогда выгодно ошибаться нарочно — провалил
    круг, повторил, получил ещё десять баллов за круг плюс ответы.

    Правило было записано в ОДНОМ месте — в обработчике, который повтор
    просто не передавал в учёт. А считается балл ДВУМЯ путями: обычно
    инкрементом по занятию, при сбое — полным пересчётом за месяц. Пересчёт
    брал все завершённые занятия без отбора, и повторы в нём платили.
    Замер по рабочей копии: 314 завершённых повторов у 25 человек на 986
    верных ответов — около четырёх тысяч баллов из ничего, причём
    выстрелило бы само, а не по команде: пересчёт включается, когда круг
    закрылся на границе месяца или занятие не нашлось.
    """

    async def test_incremental_path_ignores_a_repeat_round(self, session, user):
        await _season(session)

        quiz = _completed_quiz(user.id, answered=5, correct=5)
        quiz.quiz_mode = "error_repeat"
        session.add(quiz)
        await session.commit()

        stat = await update_monthly_stats(
            user_id=user.id, session=session, quiz_session_id=quiz.id
        )

        assert stat.monthly_quizzes == 0, "повтор засчитан как круг"
        assert stat.total_correct == 0, "ответы повтора попали в зачёт"

    async def test_full_recalc_ignores_a_repeat_round(self, session, user):
        """
        Тот же круг, другой путь — и прежде он платил.
        """
        await _season(session)

        honest = _completed_quiz(user.id, answered=10, correct=8)
        repeat = _completed_quiz(user.id, answered=5, correct=5)
        repeat.quiz_mode = "error_repeat"
        session.add_all([honest, repeat])
        await session.commit()

        stat = await update_monthly_stats(
            user_id=user.id, session=session, force_full_recalc=True
        )

        assert stat.monthly_quizzes == 1, (
            f"пересчёт засчитал {stat.monthly_quizzes} круга вместо одного"
        )
        assert stat.total_correct == 8, (
            f"в зачёт попало {stat.total_correct} верных вместо восьми"
        )

    async def test_an_old_round_without_a_mode_still_counts(self, session, user):
        """
        ЛОВУШКА ПУСТОГО ЗНАЧЕНИЯ, и она не умозрительная: в рабочей копии
        1 069 занятий со старым пустым `quiz_mode` на 14 930 верных ответов.

        Короткое условие `quiz_mode != "error_repeat"` выглядит верным, но в
        SQL сравнение с NULL даёт NULL, а не истину, — и все эти занятия
        вылетели бы из пересчёта МОЛЧА. Та же беда с другим знаком.
        """
        await _season(session)

        legacy = _completed_quiz(user.id, answered=10, correct=7)
        legacy.quiz_mode = None
        session.add(legacy)
        await session.commit()

        stat = await update_monthly_stats(
            user_id=user.id, session=session, force_full_recalc=True
        )

        assert stat.monthly_quizzes == 1, "занятие с пустым режимом потерялось"
        assert stat.total_correct == 7
