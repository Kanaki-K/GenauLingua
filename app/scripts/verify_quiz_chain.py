# -*- coding: utf-8 -*-
"""
Пройти викторину от начала до конца тем же кодом, что и бот.

Проверяет всю цепочку, которая падала: создание сессии, запись ответа,
обновление прогресса, месячная статистика. Именно на последних двух
спотыкались несдвинутые счётчики последовательностей.
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from sqlalchemy import delete, func, select

from app.core.clock import utcnow
from app.database.models import (
    MonthlyQuizEvent, MonthlyStats, QuizQuestion, QuizSession, User, UserWord,
)
from app.database.session import AsyncSessionLocal
from app.services.language_service import legacy_mode_name, pair_from_user
from app.services.monthly_leaderboard_service import update_monthly_stats
from app.services.quiz_service import generate_question, update_word_progress

PROBE_ID = -4242


async def main() -> int:
    async with AsyncSessionLocal() as s:
        # чистая песочница
        await s.execute(delete(MonthlyQuizEvent).where(MonthlyQuizEvent.user_id == PROBE_ID))
        await s.execute(delete(MonthlyStats).where(MonthlyStats.user_id == PROBE_ID))
        await s.execute(delete(UserWord).where(UserWord.user_id == PROBE_ID))
        old = (await s.execute(select(QuizSession.id).where(QuizSession.user_id == PROBE_ID))).scalars().all()
        if old:
            await s.execute(delete(QuizQuestion).where(QuizQuestion.session_id.in_(old)))
            await s.execute(delete(QuizSession).where(QuizSession.user_id == PROBE_ID))
        await s.execute(delete(User).where(User.id == PROBE_ID))
        await s.commit()

        for learning, native in [("de", "ru"), ("en", "ru"), ("tr", "uk")]:
            user = User(
                id=PROBE_ID, first_name="probe", interface_language="ru",
                learning_lang=learning, native_lang=native, reverse_mode=False,
            )
            await s.merge(user)
            await s.commit()
            user = await s.get(User, PROBE_ID)
            pair = pair_from_user(user)

            quiz = QuizSession(
                user_id=user.id, level=user.level,
                learning_lang=pair.learning, native_lang=pair.native,
                is_reverse=pair.reverse, translation_mode=legacy_mode_name(pair),
                total_questions=3, answered_questions=0, correct_answers=0,
                quiz_mode="level", start_source="probe",
            )
            s.add(quiz)
            await s.commit()

            used: list[int] = []
            asked = 0
            for _ in range(3):
                q = await generate_question(s, user, exclude_ids=used, pair=pair)
                if q is None:
                    print(f"  {learning}->{native}: вопрос не собрался")
                    return 1
                word = q["correct_word"]
                used.append(word.id)
                asked += 1

                s.add(QuizQuestion(
                    session_id=quiz.id, word_id=word.id, user_answer=q["options"][0][1][:255],
                    is_correct=True, answered_at=utcnow(), response_time_seconds=3,
                ))
                quiz.answered_questions += 1
                quiz.correct_answers += 1
                await s.commit()

                await update_word_progress(user.id, word.id, True, s, learning_lang=pair.learning)

            quiz.is_completed = True
            quiz.completed_at = utcnow()
            quiz.exit_reason = "completed"
            await s.commit()

            stat = await update_monthly_stats(user.id, s, quiz_session_id=quiz.id)

            answers = (await s.execute(
                select(func.count()).select_from(QuizQuestion)
                .where(QuizQuestion.session_id == quiz.id)
            )).scalar()
            progress = (await s.execute(
                select(func.count()).select_from(UserWord)
                .where(UserWord.user_id == user.id, UserWord.learning_lang == pair.learning)
            )).scalar()

            print(f"  {learning}->{native}: сессия {quiz.id}, вопросов {asked}, "
                  f"ответов записано {answers}, прогресс {progress} слов, "
                  f"месячный балл {stat.monthly_score}")

        # убрать за собой
        ids = (await s.execute(select(QuizSession.id).where(QuizSession.user_id == PROBE_ID))).scalars().all()
        await s.execute(delete(MonthlyQuizEvent).where(MonthlyQuizEvent.user_id == PROBE_ID))
        await s.execute(delete(MonthlyStats).where(MonthlyStats.user_id == PROBE_ID))
        await s.execute(delete(UserWord).where(UserWord.user_id == PROBE_ID))
        if ids:
            await s.execute(delete(QuizQuestion).where(QuizQuestion.session_id.in_(ids)))
        await s.execute(delete(QuizSession).where(QuizSession.user_id == PROBE_ID))
        await s.execute(delete(User).where(User.id == PROBE_ID))
        await s.commit()

    print("\nВся цепочка работает: сессия → ответы → прогресс → месячный рейтинг.")
    return 0


sys.exit(asyncio.run(main()))
