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

    total = sessions_fixed + users_fixed + monthly_fixed
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
