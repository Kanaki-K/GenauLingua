"""
ПРИЁМКА УЧЁТА: сходятся ли числа, которые бот пишет про человека.

ЗАЧЕМ. Про каждого человека ведётся пять слоёв записей, и каждый следующий
— свёртка предыдущего:

    UserWord        прогресс по слову: показы, верные, серия, каналы
    QuizQuestion    один принятый ответ
    QuizSession     один круг: счётчики
    User            итоги: выучено, точность, серия дней, кругов
    MonthlyStats    месяц по языкам: баллы, точность, каналы

Свёртка может разойтись с источником, и расходится она ТИХО: человек видит
на экране число, которого в данных нет. Так уже было — 934 занятия с
счётчиком верных, не сходящимся со строками ответов, и у 73 человек
показанная точность была чужой.

Этот скрипт сверяет каждый слой с тем, из чего он выведен, и печатает
расхождения числом. Он ТОЛЬКО ЧИТАЕТ — правит `repair_accounting`.

    ENV_FILE=.env.local .venv/Scripts/python.exe -m app.scripts.audit_accounting
    ... --show 20      сколько примеров показывать на каждое расхождение
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import sys

from sqlalchemy import select, text

from app.database.session import AsyncSessionLocal

logging.disable(logging.ERROR)

OK = "ок  "
BAD = "СБОЙ"


class Report:
    def __init__(self, show: int) -> None:
        self.show = show
        self.bad: list[str] = []
        self.checked = 0

    def line(self, ok: bool, title: str, detail: str = "") -> None:
        self.checked += 1
        print(f"  [{OK if ok else BAD}] {title}" + (f" — {detail}" if detail else ""))
        if not ok:
            self.bad.append(f"{title}: {detail}")

    def note(self, text_: str) -> None:
        print(f"         {text_}")


# ============================================================================
# ЗАПРОСЫ. Каждый отвечает на один вопрос и возвращает (расхождений, всего)
# ============================================================================

CHECKS: list[tuple[str, str, str]] = [
    (
        "выучено у человека = выученным словам",
        """
        WITH real AS (
          SELECT uw.user_id, COUNT(*) AS n
          FROM user_words uw JOIN users u ON u.id = uw.user_id
          WHERE uw.learned AND uw.learning_lang = u.learning_lang
          GROUP BY uw.user_id
        )
        SELECT COUNT(*) FROM users u
        LEFT JOIN real r ON r.user_id = u.id
        WHERE COALESCE(u.words_learned,0) <> COALESCE(r.n,0)
        """,
        "SELECT COUNT(*) FROM users",
    ),
    (
        "кругов пройдено = завершённым занятиям",
        """
        WITH real AS (
          SELECT user_id, COUNT(*) AS n FROM quiz_sessions
          WHERE completed_at IS NOT NULL AND COALESCE(quiz_mode,'') <> 'error_repeat'
          GROUP BY user_id
        )
        SELECT COUNT(*) FROM users u
        LEFT JOIN real r ON r.user_id = u.id
        WHERE COALESCE(u.quizzes_passed,0) <> COALESCE(r.n,0)
        """,
        "SELECT COUNT(*) FROM users",
    ),
    # Устаревшая колонка серии — РЕШЕНИЕ, а не дефект: стирать её нельзя,
    # по ней восстанавливается лучшая серия, а экраны читают серию через
    # `current_streak`, который сам возвращает ноль по дате последнего дня.
    # Проверяется поэтому не свежесть колонки, а что число не ПОТЕРЯНО.
    (
        "у устаревшей серии сохранена лучшая",
        """
        SELECT COUNT(*) FROM users
        WHERE COALESCE(streak_days,0) > COALESCE(best_streak_days,0)
        """,
        "SELECT COUNT(*) FROM users WHERE COALESCE(streak_days,0) > 0",
    ),
    (
        "лучшая серия записана у всех, кто занимался",
        """
        SELECT COUNT(*) FROM users
        WHERE COALESCE(quizzes_passed,0) > 0
          AND COALESCE(best_streak_days,0) = 0
        """,
        "SELECT COUNT(*) FROM users WHERE COALESCE(quizzes_passed,0) > 0",
    ),
    # Серия и последний день сверяются НЕ ЗДЕСЬ, а в `_check_streaks` ниже:
    # с 15 октября 2026 день занятий — день ЧЕЛОВЕКА (его часовой пояс), до
    # того — UTC, и на переходе действует допуск. Повторять это правило на
    # SQL значило бы завести вторую копию, которая разойдётся с первой.
    (
        "каналы слова не больше его показов",
        """
        SELECT COUNT(*) FROM user_words
        WHERE COALESCE(shown_audio,0) + COALESCE(shown_speech,0)
              + COALESCE(shown_reverse,0) > times_shown
           OR COALESCE(correct_audio,0) + COALESCE(correct_speech,0)
              + COALESCE(correct_reverse,0) > times_correct
        """,
        "SELECT COUNT(*) FROM user_words",
    ),
    (
        "верных не больше показов",
        "SELECT COUNT(*) FROM user_words WHERE times_correct > times_shown",
        "SELECT COUNT(*) FROM user_words",
    ),
    (
        "отметка «выучено» соответствует серии",
        """
        SELECT COUNT(*) FROM user_words
        WHERE learned AND correct_streak < 3
        """,
        "SELECT COUNT(*) FROM user_words WHERE learned",
    ),
    (
        "у показанного слова есть дата показа",
        """
        SELECT COUNT(*) FROM user_words
        WHERE times_shown > 0 AND last_seen_at IS NULL
        """,
        "SELECT COUNT(*) FROM user_words WHERE times_shown > 0",
    ),
    (
        "счётчики занятия = строкам ответов",
        """
        WITH r AS (
          SELECT session_id, COUNT(*) n,
                 SUM(CASE WHEN is_correct THEN 1 ELSE 0 END) k
          FROM quiz_questions GROUP BY session_id
        )
        SELECT COUNT(*) FROM quiz_sessions s JOIN r ON r.session_id = s.id
        WHERE s.answered_questions <> r.n OR s.correct_answers <> r.k
        """,
        "SELECT COUNT(*) FROM quiz_sessions",
    ),
    (
        "точность человека = его ответам",
        """
        WITH real AS (
          SELECT s.user_id,
                 SUM(CASE WHEN q.is_correct THEN 1 ELSE 0 END) AS correct,
                 COUNT(q.id) AS answered
          FROM quiz_sessions s JOIN quiz_questions q ON q.session_id = s.id
          WHERE s.completed_at IS NOT NULL
          GROUP BY s.user_id
        )
        SELECT COUNT(*) FROM users u JOIN real r ON r.user_id = u.id
        WHERE r.answered > 0
          AND ABS(COALESCE(u.success_rate,0)
                  - ROUND(100.0 * r.correct / r.answered)) > 1
        """,
        "SELECT COUNT(*) FROM users WHERE COALESCE(success_rate,0) > 0",
    ),
    # Месячный балл сверяется в `_check_scores` ниже — ФОРМУЛОЙ БОТА, а не
    # её копией на SQL. Копия здесь уже разошлась: она платила 5 за обратный
    # круг (в боте с пятой игрой 0) и не знала про `correct_reverse`, и
    # ложно падала на каждом из 10 человек с прежней настройкой реверса,
    # стоило тому закончить круг.
    (
        "месячная точность не выше ста",
        """
        SELECT COUNT(*) FROM monthly_stats ms
        JOIN monthly_seasons se ON se.id = ms.season_id
        WHERE se.is_active AND COALESCE(ms.monthly_avg_percent,0) > 100
        """,
        "SELECT COUNT(*) FROM monthly_stats",
    ),
]

# Примеры для расхождений, у которых они полезны
SAMPLES: dict[str, str] = {
    "серия дней НЕ устарела": """
        SELECT id, streak_days, last_active_date,
               CURRENT_DATE - last_active_date AS days_ago
        FROM users
        WHERE COALESCE(streak_days,0) > 0
          AND (last_active_date IS NULL
               OR last_active_date < CURRENT_DATE - INTERVAL '1 day')
        ORDER BY days_ago DESC NULLS FIRST LIMIT :show
    """,
    "выучено у человека = выученным словам": """
        WITH real AS (
          SELECT uw.user_id, COUNT(*) AS n
          FROM user_words uw JOIN users u ON u.id = uw.user_id
          WHERE uw.learned AND uw.learning_lang = u.learning_lang
          GROUP BY uw.user_id
        )
        SELECT u.id, u.words_learned AS written, COALESCE(r.n,0) AS real
        FROM users u LEFT JOIN real r ON r.user_id = u.id
        WHERE COALESCE(u.words_learned,0) <> COALESCE(r.n,0)
        ORDER BY ABS(COALESCE(u.words_learned,0) - COALESCE(r.n,0)) DESC
        LIMIT :show
    """,
    "кругов пройдено = завершённым занятиям": """
        WITH real AS (
          SELECT user_id, COUNT(*) AS n FROM quiz_sessions
          WHERE completed_at IS NOT NULL AND COALESCE(quiz_mode,'') <> 'error_repeat'
          GROUP BY user_id
        )
        SELECT u.id, u.quizzes_passed AS written, COALESCE(r.n,0) AS real
        FROM users u LEFT JOIN real r ON r.user_id = u.id
        WHERE COALESCE(u.quizzes_passed,0) <> COALESCE(r.n,0)
        ORDER BY ABS(COALESCE(u.quizzes_passed,0) - COALESCE(r.n,0)) DESC
        LIMIT :show
    """,
}


async def _check_streaks(session, rep: Report) -> None:
    """
    Серия и последний день = истории завершённых зачётных кругов.

    День каждого круга — `user_day` (до перехода UTC, после — пояс
    человека), череда — `next_streak`: ровно то, чем отмечает день бот.
    Нашла в своё время человека с серией 2 при последних днях 1 и 29 числа.
    """
    from app.database.models import QuizSession, User
    from app.services.monthly_leaderboard_service import scored_sessions_filter
    from app.services.streak_service import next_streak, user_day

    rows = (await session.execute(
        select(User, QuizSession.completed_at)
        .join(QuizSession, QuizSession.user_id == User.id)
        .where(QuizSession.completed_at.isnot(None), scored_sessions_filter())
    )).all()

    days: dict[int, set] = {}
    people: dict[int, object] = {}
    for user, completed_at in rows:
        people[user.id] = user
        days.setdefault(user.id, set()).add(user_day(user, completed_at))

    bad = []
    for user_id, active in days.items():
        streak, last = 0, None
        for day in sorted(active):
            streak = next_streak(streak, last, day)
            last = day
        user = people[user_id]
        if int(user.streak_days or 0) != streak or user.last_active_date != last:
            bad.append(f"{user_id}: записано {user.streak_days} · {user.last_active_date}, "
                       f"по истории {streak} · {last}")

    title = "серия и последний день = истории занятий"
    rep.line(not bad, title,
             f"расходится {len(bad)} из {len(days)}" if bad else f"проверено {len(days)}")
    for line in bad[:rep.show]:
        rep.note(line)


async def _check_scores(session, rep: Report) -> None:
    """Месячный балл действующего сезона = `calculate_monthly_score()` по своим числам."""
    from app.database.models import MonthlySeason, MonthlyStats

    stats = (await session.execute(
        select(MonthlyStats)
        .join(MonthlySeason, MonthlySeason.id == MonthlyStats.season_id)
        .where(MonthlySeason.is_active.is_(True))
    )).scalars().all()

    bad = [
        f"{s.user_id} [{s.learning_lang}]: записано {s.monthly_score}, "
        f"по формуле {s.calculate_monthly_score()}"
        for s in stats if (s.monthly_score or 0) != s.calculate_monthly_score()
    ]
    title = "месячный балл = расчёту по своим же числам"
    rep.line(not bad, title,
             f"расходится {len(bad)} из {len(stats)}" if bad else f"проверено {len(stats)}")
    for line in bad[:rep.show]:
        rep.note(line)


async def run(show: int) -> int:
    rep = Report(show)
    print("Приёмка учёта: сходятся ли числа про человека\n" + "=" * 68)

    async with AsyncSessionLocal() as session:
        await _check_streaks(session, rep)
        await _check_scores(session, rep)
        for title, bad_sql, total_sql in CHECKS:
            bad = int((await session.execute(text(bad_sql))).scalar() or 0)
            total = int((await session.execute(text(total_sql))).scalar() or 0)
            detail = f"расходится {bad} из {total}" if total else f"{bad}"
            rep.line(bad == 0, title, detail if bad else f"проверено {total}")

            if bad and title in SAMPLES:
                rows = (await session.execute(
                    text(SAMPLES[title]), {"show": show}
                )).all()
                for row in rows:
                    rep.note(" · ".join(str(x) for x in row))

    print("\n" + "=" * 68)
    print(f"проверок: {rep.checked}")
    if rep.bad:
        print(f"РАСХОЖДЕНИЙ: {len(rep.bad)}")
        return 1
    print("учёт сходится на всех пяти слоях")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--show", type=int, default=6)
    args = ap.parse_args()
    return asyncio.run(run(args.show))


if __name__ == "__main__":
    sys.exit(main())
