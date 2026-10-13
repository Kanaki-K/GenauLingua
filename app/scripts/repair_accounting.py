"""
Починка учёта: счётчики занятий, показанная точность, месячный балл.

ЧТО ПОЧИНИТЬ И ОТКУДА ОНО ВЗЯЛОСЬ. Три расхождения, найденные аудитом
13 октября 2026. Все три — РАСХОЖДЕНИЯ ДАННЫХ, а не дефекты кода: код уже
верен, но прежние его редакции оставили числа, которые никто не пересчитал.

1. СЧЁТЧИКИ ЗАНЯТИЙ. `correct_answers` расходится со строками ответов у
   934 занятий из 2 100, причём В ОБЕ СТОРОНЫ. Поэтому прежде чем править,
   пришлось разобрать, кто первоисточник, — и обе стороны объяснились:

     счётчик МЕНЬШЕ строк (323)   все до единого — БРОШЕННЫЕ круги, и у
                                  всех `correct_answers = 0` при непустых
                                  строках. Прежде счётчик писался в КОНЦЕ
                                  круга, а у брошенного конца не было.
                                  Свежайший случай — 29 сентября, день
                                  миграции `fix_accuracy_accounting`,
                                  после которой счётчик растёт на каждом
                                  ответе

     счётчик БОЛЬШЕ строк (611)   завершённые круги по 8 апреля
                                  включительно, с систематическим +1..+2.
                                  Строки при этом самосогласованы: 24
                                  строки на 24 отвеченных

   В обоих случаях СТРОКИ — первоисточник, и проект это уже признал:
   сентябрьская миграция тем же способом пересчитала из них
   `answered_questions` (сейчас он сходится со строками у всех 2 100
   занятий, расхождений ноль).

   Видимое следствие порчи: 326 занятий носят верных БОЛЬШЕ, чем
   отвеченных, то есть точность выше ста процентов. Админка так и
   показывает: «Лучший: 200.0%». По всей базе счётчики дают 93.08% против
   88.30% по строкам — завышение на 4.78 пункта.

2. ПОКАЗАННАЯ ТОЧНОСТЬ ЧЕЛОВЕКА. `users.success_rate` считается суммой по
   счётчикам занятий, поэтому порча протекает в него. У 37 человек
   расхождение от 2 до 23 пунктов, причём шестеро видят у себя 100% при
   настоящих 77–88%.

3. МЕСЯЧНЫЙ БАЛЛ. Формулу переписали («платим за усилие»: ответ по каналу
   1/2/3, плавная точность, растущая серия), а ХРАНИМУЮ колонку
   `monthly_stats.monthly_score` у существующих рядов никто не пересчитал.
   Свежайшая правка статистики — 1 октября, формула новее. Расходятся ВСЕ
   166 рядов, от −19 до +212 баллов.

   Рейтинг читает именно хранимую колонку (и сортирует по ней), а экраны
   показывают её же. Значит после выкладки рейтинг окажется смесью старых и
   новых чисел: пересчитается только у тех, кто сыграет ещё круг.

ЧЕГО ЭТОТ СКРИПТ НЕ ДЕЛАЕТ НАРОЧНО

* НЕ УДАЛЯЕТ 50 лишних строк ответов (31 вопрос, записанный дважды). Код
  это больше не создаёт — защита «один вопрос — один ответ» стоит, — но
  удалять чужие прошлые ответы значит молча переписывать историю людей.
  Решение владельца, не моё. Скрипт только пересчитывает счётчики ПО
  строкам, какие есть, — тогда они хотя бы сходятся между собой.

* НЕ ТРОГАЕТ прогресс по словам (`user_words`). Двойные ответы двигали его
  дважды, но отличить «двойной» вклад от настоящего в накопленном итоге
  нечем: строки есть, а какой из них лишний — не знает никто.

* НЕ ТРОГАЕТ ЗАКРЫТЫЕ СЕЗОНЫ без `--all-seasons`. Там розданы награды и
  записаны итоговые места: пересчёт баллов задним числом рассогласовал бы
  их с наградами. По умолчанию правится действующий сезон — тот, который
  люди видят.

* НЕ ТРОГАЕТ `final_rank` и награды никогда.

    ENV_FILE=.env.local .venv/Scripts/python.exe -m app.scripts.repair_accounting
    ... -m app.scripts.repair_accounting --apply
    ... -m app.scripts.repair_accounting --apply --all-seasons
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import sys
from datetime import datetime

from sqlalchemy import Integer, func, select

from app.core.clock import utcnow
from app.database.enums import QuizChannel
from app.database.models import (
    MonthlySeason, MonthlyStats, QuizQuestion, QuizSession, User, UserWord,
)
from app.database.session import AsyncSessionLocal
from app.services.monthly_leaderboard_service import (
    REPEAT_QUIZ_MODE, scored_sessions_filter,
)
from app.services.quiz_service import MIN_ATTEMPTS_FOR_LEARNED

logging.disable(logging.ERROR)


# ============================================================================
# 1. СЧЁТЧИКИ ЗАНЯТИЙ ← СТРОКИ ОТВЕТОВ
# ============================================================================

async def repair_sessions(session, apply: bool) -> int:
    """
    Привести `answered_questions`/`correct_answers` к строкам `quiz_questions`.

    Строки — первоисточник: каждая это один принятый ответ. Счётчики же
    инкрементировались в коде и однажды разошлись. Считать надо от строк, а
    не наоборот: восстановить потерянную строку по счётчику нельзя, а
    счётчик по строкам — ровно одним запросом.
    """
    counted = (
        select(
            QuizQuestion.session_id.label("sid"),
            func.count().label("answered"),
            func.sum(func.cast(QuizQuestion.is_correct, Integer)).label("correct"),
        )
        .group_by(QuizQuestion.session_id)
        .subquery()
    )

    rows = (await session.execute(
        select(QuizSession, counted.c.answered, counted.c.correct)
        .outerjoin(counted, counted.c.sid == QuizSession.id)
    )).all()

    fixed = 0
    for quiz, answered, correct in rows:
        answered = int(answered or 0)
        correct = int(correct or 0)
        if quiz.answered_questions == answered and quiz.correct_answers == correct:
            continue
        fixed += 1
        if fixed <= 8:
            print(f"   занятие {quiz.id}: отвечено "
                  f"{quiz.answered_questions}→{answered}, верных "
                  f"{quiz.correct_answers}→{correct}")
        if apply:
            quiz.answered_questions = answered
            quiz.correct_answers = correct
            if quiz.exit_at_question and quiz.exit_at_question > answered:
                quiz.exit_at_question = answered

    if fixed > 8:
        print(f"   … и ещё {fixed - 8}")
    if apply:
        await session.commit()
    return fixed


# ============================================================================
# 2. ПОКАЗАННАЯ ТОЧНОСТЬ ЧЕЛОВЕКА
# ============================================================================

async def repair_success_rate(session, apply: bool) -> int:
    """
    Пересчитать `users.success_rate` по ЗАВЕРШЁННЫМ занятиям.

    Тем же выражением, которым это делает `_finish_quiz`, — иначе появится
    второе место, решающее «какая у человека точность».

    Верные берутся ИЗ СТРОК, а не из колонки занятия, и это важно для
    режима показа: первая редакция читала колонку, которую сама же ещё не
    поправила, и показывала человеку точность 104% и 109% — то есть
    «починка» отчитывалась невозможными числами. В режиме правки порядок
    спас бы, в режиме показа — нет.
    """
    correct_rows = (
        select(
            QuizQuestion.session_id.label("sid"),
            func.sum(func.cast(QuizQuestion.is_correct, Integer)).label("k"),
        )
        .group_by(QuizQuestion.session_id)
        .subquery()
    )
    totals = (
        select(
            QuizSession.user_id.label("uid"),
            func.coalesce(func.sum(QuizSession.answered_questions), 0).label("answered"),
            func.coalesce(func.sum(correct_rows.c.k), 0).label("correct"),
        )
        .outerjoin(correct_rows, correct_rows.c.sid == QuizSession.id)
        .where(QuizSession.completed_at.isnot(None))
        .group_by(QuizSession.user_id)
        .subquery()
    )

    rows = (await session.execute(
        select(User, totals.c.answered, totals.c.correct)
        .outerjoin(totals, totals.c.uid == User.id)
    )).all()

    fixed = 0
    for user, answered, correct in rows:
        answered = int(answered or 0)
        correct = int(correct or 0)
        rate = int(correct / answered * 100) if answered else 0
        if (user.success_rate or 0) == rate:
            continue
        fixed += 1
        if fixed <= 8:
            print(f"   человек {user.id}: точность "
                  f"{user.success_rate}%→{rate}%")
        if apply:
            user.success_rate = rate

    if fixed > 8:
        print(f"   … и ещё {fixed - 8}")
    if apply:
        await session.commit()
    return fixed


# ============================================================================
# 3. МЕСЯЧНЫЙ БАЛЛ ← ЗАНЯТИЯ СЕЗОНА
# ============================================================================

async def repair_monthly(session, apply: bool, all_seasons: bool) -> int:
    """
    Пересчитать месячную статистику по занятиям сезона.

    Формула берётся из `MonthlyStats.calculate_monthly_score()` — того же
    единственного места, которым считает бот. Своя копия расчёта здесь
    означала бы, что починка и бот разойдутся при первой правке цены.

    Круги-повторы отсеиваются `scored_sessions_filter()` — тем же условием,
    которым их отсеивает учёт. Иначе починка «восстановила» бы ровно те
    баллы, которые аудит из зачёта убрал.
    """
    seasons = (await session.execute(
        select(MonthlySeason).order_by(MonthlySeason.year, MonthlySeason.month)
    )).scalars().all()
    if not all_seasons:
        seasons = [s for s in seasons if s.is_active]
    if not seasons:
        print("   действующего сезона нет — пересчитывать нечего")
        return 0

    fixed = 0
    for season in seasons:
        start = datetime.combine(season.start_date, datetime.min.time())
        end = datetime.combine(season.end_date, datetime.max.time())

        stats = (await session.execute(
            select(MonthlyStats).where(MonthlyStats.season_id == season.id)
        )).scalars().all()

        for stat in stats:
            quizzes = (await session.execute(
                select(QuizSession).where(
                    QuizSession.user_id == stat.user_id,
                    QuizSession.learning_lang == stat.learning_lang,
                    QuizSession.completed_at.isnot(None),
                    QuizSession.started_at >= start,
                    QuizSession.started_at <= end,
                    scored_sessions_filter(),
                )
            )).scalars().all()

            answered = sum(q.answered_questions or 0 for q in quizzes)
            correct = sum(q.correct_answers or 0 for q in quizzes)
            ids = [q.id for q in quizzes]

            by_channel = {}
            if ids:
                by_channel = {
                    channel: count
                    for channel, count in (await session.execute(
                        select(QuizQuestion.channel, func.count())
                        .where(
                            QuizQuestion.session_id.in_(ids),
                            QuizQuestion.is_correct.is_(True),
                            QuizQuestion.channel.isnot(None),
                        )
                        .group_by(QuizQuestion.channel)
                    )).all()
                }

            words = (await session.execute(
                select(func.count()).select_from(UserWord).where(
                    UserWord.user_id == stat.user_id,
                    UserWord.learning_lang == stat.learning_lang,
                    UserWord.learned.is_(True),
                    UserWord.last_seen_at >= start,
                    UserWord.last_seen_at <= end,
                )
            )).scalar() or 0

            fresh = dict(
                monthly_quizzes=len(quizzes),
                monthly_reverse=sum(1 for q in quizzes if q.is_reverse),
                total_correct=correct,
                total_questions=answered,
                monthly_avg_percent=int(correct / answered * 100) if answered else 0,
                correct_audio=by_channel.get(QuizChannel.AUDIO.value, 0),
                correct_speech=by_channel.get(QuizChannel.SPEECH.value, 0),
                monthly_words=int(words),
            )

            before = stat.monthly_score
            for key, value in fresh.items():
                setattr(stat, key, value)
            after = stat.calculate_monthly_score()

            if before == after and not _changed(stat, fresh):
                continue

            fixed += 1
            if fixed <= 10:
                print(f"   {season.month:02}/{season.year} человек {stat.user_id} "
                      f"[{stat.learning_lang}]: балл {before}→{after}")

            if apply:
                stat.monthly_score = after
                stat.updated_at = utcnow()
            else:
                session.expunge(stat)

    if fixed > 10:
        print(f"   … и ещё {fixed - 10}")
    if apply:
        await session.commit()
    else:
        await session.rollback()
    return fixed


def _changed(stat: MonthlyStats, fresh: dict) -> bool:
    """Изменилось ли что-то, кроме балла."""
    return any(getattr(stat, key) != value for key, value in fresh.items())


# ============================================================================
# 4. ИТОГИ ЧЕЛОВЕКА ← ЕГО ЖЕ ЗАПИСИ
# ============================================================================

async def repair_user_totals(session, apply: bool) -> int:
    """
    Привести `words_learned`, `quizzes_passed` и лучшую серию к источнику.

    ЧТО НАШЛОСЬ (замер 13 октября 2026, приёмка `audit_accounting`):

      выучено      расходится у 35 человек из 233, и расхождение не
                   объяснимо сменой языка: у одного записано 225 при НУЛЕ
                   выученных слов по всем языкам сразу. Числа 125 · 175 ·
                   225 кратны двадцати пяти — так считала какая-то прежняя
                   версия, по другому правилу
      кругов       недосчитано у 41 человека: у одного 109 завершённых
                   занятий при записанных 54. Все они февраль–апрель с
                   пустым режимом, то есть прежняя версия увеличивала
                   счётчик не на каждом завершении
      лучшая серия НЕ ЗАПИСЫВАЛАСЬ НИ РАЗУ: ноль у всех 233. Колонка
                   существовала с самого начала

    Сейчас код считает и то и другое верно — расхождение историческое. Но
    видит человек именно эти числа.

    Лучшая серия считается ПО ИСТОРИИ — по самой длинной череде подряд
    идущих дней с завершённым кругом. Первая попытка брала максимум из
    нынешней серии и записанного, и это оказалось слабо: сломав колонку
    серии нарочно, починка не смогла вернуть число — восстанавливать его
    было не из чего. А даты завершённых занятий в базе есть, и серия дней
    отмечается ровно на тех же завершениях, так что история — это и есть
    источник. Берётся максимум из посчитанного и записанного: записанное
    могло попасть из дней, которых в занятиях нет (старые версии).
    """
    days = (await session.execute(
        select(QuizSession.user_id,
               func.date(QuizSession.completed_at).label("day"))
        .where(QuizSession.completed_at.isnot(None), scored_sessions_filter())
        .group_by(QuizSession.user_id, func.date(QuizSession.completed_at))
    )).all()

    history_best: dict[int, int] = {}
    history_last: dict[int, tuple] = {}
    active_days: dict[int, list] = {}
    for user_id, day in days:
        active_days.setdefault(user_id, []).append(day)
    for user_id, dates in active_days.items():
        dates.sort()
        best = run = 1
        for before, after in zip(dates, dates[1:]):
            run = run + 1 if (after - before).days == 1 else 1
            best = max(best, run)
        history_best[user_id] = best
        # Серия на последний активный день — это череда, которая им
        # оканчивается. Вместе с самим днём это и есть то, что хранят
        # `streak_days` и `last_active_date`
        history_last[user_id] = (run, dates[-1])

    learned = (
        select(UserWord.user_id, func.count().label("n"))
        .join(User, User.id == UserWord.user_id)
        .where(UserWord.learned.is_(True),
               UserWord.learning_lang == User.learning_lang)
        .group_by(UserWord.user_id)
        .subquery()
    )
    rounds = (
        select(QuizSession.user_id, func.count().label("n"))
        .where(QuizSession.completed_at.isnot(None), scored_sessions_filter())
        .group_by(QuizSession.user_id)
        .subquery()
    )

    rows = (await session.execute(
        select(User, learned.c.n, rounds.c.n)
        .outerjoin(learned, learned.c.user_id == User.id)
        .outerjoin(rounds, rounds.c.user_id == User.id)
    )).all()

    fixed = 0
    by_column = {"выучено": 0, "кругов": 0, "серия": 0, "лучшая серия": 0}
    worst = []

    for user, learned_n, rounds_n in rows:
        learned_n = int(learned_n or 0)
        rounds_n = int(rounds_n or 0)
        # Источник — история. Колонка берётся ТОЛЬКО когда истории нет
        # совсем: иначе выдуманное число живёт вечно, ведь живой код
        # `best_streak_days` лишь наращивает максимумом и никогда не
        # пересчитывает. У выученных слов выдуманное снимается (там живой
        # код считает заново каждый круг) — правило должно быть то же.
        if user.id in history_last:
            streak_n, last_day = history_last[user.id]
            best = max(streak_n, history_best[user.id])
        else:
            streak_n, last_day = int(user.streak_days or 0), user.last_active_date
            best = max(int(user.best_streak_days or 0), streak_n)

        gaps = {
            "выучено": abs(int(user.words_learned or 0) - learned_n),
            "кругов": abs(int(user.quizzes_passed or 0) - rounds_n),
            "серия": abs(int(user.streak_days or 0) - streak_n)
                     + (user.last_active_date != last_day),
            "лучшая серия": abs(int(user.best_streak_days or 0) - best),
        }
        if not any(gaps.values()):
            continue

        fixed += 1
        for column, gap in gaps.items():
            if gap:
                by_column[column] += 1
        worst.append((max(gaps.values()),
                      f"   человек {user.id}: выучено "
                      f"{user.words_learned}→{learned_n}, кругов "
                      f"{user.quizzes_passed}→{rounds_n}, серия "
                      f"{user.streak_days}→{streak_n}, лучшая "
                      f"{user.best_streak_days}→{best}"))

        if apply:
            user.words_learned = learned_n
            user.quizzes_passed = rounds_n
            user.streak_days = streak_n
            user.last_active_date = last_day
            user.best_streak_days = best

    for column, count in by_column.items():
        if count:
            print(f"   {column}: {count}")
    # Самые крупные расхождения вперёд: именно по ним видно, что правка
    # попала в тот дефект, который нашла приёмка, а не в мелкую рябь
    for _, line in sorted(worst, key=lambda item: -item[0])[:8]:
        print(line)
    if len(worst) > 8:
        print(f"   … и ещё {len(worst) - 8}")

    if apply:
        await session.commit()
    return fixed


# ============================================================================
# 5. ПРОГРЕСС ПО СЛОВАМ: МЕЛКИЙ ДОЛГ
# ============================================================================

async def repair_word_rows(session, apply: bool) -> int:
    """
    Две мелочи в `user_words`, обе историческиe.

      отметка «выучено» при серии меньше трёх — 1 ряд из 1 537. Правило
      `_is_learned` пересчитывается на каждом ответе, так что это остаток
      прежней версии

      пустая дата показа при непустых показах — 60 рядов. С подбором по
      времени такое слово считается просроченным ВСЕГДА и лезет вперёд
      остальных; дата ставится по последнему ответу на это слово, а если
      ответов нет — по времени создания ряда
    """
    stale_learned = (await session.execute(
        select(UserWord).where(
            UserWord.learned.is_(True),
            UserWord.correct_streak < MIN_ATTEMPTS_FOR_LEARNED,
        )
    )).scalars().all()

    # Дата берётся по ответам ЭТОГО человека на ЭТО слово: соединение
    # только по слову притянуло бы чужой ответ и поставило дату, которой у
    # человека не было
    last_answer = (
        select(
            QuizSession.user_id.label("user_id"),
            QuizQuestion.word_id.label("word_id"),
            func.max(QuizQuestion.answered_at).label("at"),
        )
        .join(QuizSession, QuizSession.id == QuizQuestion.session_id)
        .where(QuizQuestion.answered_at.isnot(None))
        .group_by(QuizSession.user_id, QuizQuestion.word_id)
        .subquery()
    )
    no_date = (await session.execute(
        select(UserWord, last_answer.c.at)
        .outerjoin(
            last_answer,
            (last_answer.c.user_id == UserWord.user_id)
            & (last_answer.c.word_id == UserWord.word_id),
        )
        .where(UserWord.times_shown > 0, UserWord.last_seen_at.is_(None))
    )).all()

    fixed = len(stale_learned) + len(no_date)
    if stale_learned:
        print(f"   отметка «выучено» при короткой серии: {len(stale_learned)}")
    if no_date:
        print(f"   без даты показа: {len(no_date)}")

    if apply:
        for row in stale_learned:
            row.learned = False
        for row, answered_at in no_date:
            row.last_seen_at = answered_at or row.created_at or utcnow()
        await session.commit()

    return fixed


# ============================================================================
# ПРОГОН
# ============================================================================

async def run(apply: bool, all_seasons: bool) -> int:
    mode = "ПРАВКА" if apply else "только показ (для правки --apply)"
    print(f"Починка учёта — {mode}\n")

    async with AsyncSessionLocal() as session:
        print("1. Счётчики занятий ← строки ответов")
        sessions_fixed = await repair_sessions(session, apply)
        print(f"   расходится занятий: {sessions_fixed}\n")

        print("2. Показанная точность человека")
        users_fixed = await repair_success_rate(session, apply)
        print(f"   расходится людей: {users_fixed}\n")

        scope = "все сезоны" if all_seasons else "действующий сезон"
        print(f"3. Месячный балл ← занятия сезона ({scope})")
        monthly_fixed = await repair_monthly(session, apply, all_seasons)
        print(f"   расходится рядов: {monthly_fixed}\n")

        # Слова ПЕРЕД итогами: снятая отметка «выучено» меняет счёт
        # выученных, и считать итоги надо уже по исправленным рядам
        print("4. Прогресс по словам")
        words_fixed = await repair_word_rows(session, apply)
        print(f"   расходится рядов: {words_fixed}\n")

        print("5. Итоги человека ← его же записи")
        totals_fixed = await repair_user_totals(session, apply)
        print(f"   расходится людей: {totals_fixed}\n")

    total = (sessions_fixed + users_fixed + monthly_fixed
             + totals_fixed + words_fixed)
    if not total:
        print("учёт сходится: править нечего")
        return 0

    if apply:
        print(f"поправлено записей: {total}")
    else:
        print(f"РАСХОЖДЕНИЙ: {total} — ничего не менялось, "
              f"для правки прогнать с --apply")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true",
                    help="записать правки (по умолчанию только показ)")
    ap.add_argument("--all-seasons", action="store_true",
                    help="пересчитать и закрытые сезоны — там розданы награды")
    args = ap.parse_args()
    return asyncio.run(run(args.apply, args.all_seasons))


if __name__ == "__main__":
    sys.exit(main())
