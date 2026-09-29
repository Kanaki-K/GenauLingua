"""fix accuracy accounting: store answered question count separately from planned

Проблема (видна на прод-данных): quiz_sessions.total_questions хранит
плановое число вопросов (обычно 25), а не фактически отвеченное. Брошенная
сессия выглядит как сплошные ошибки. Точность, посчитанная посессионно,
даёт 60.7% против реальных 88.1% по фактическим ответам — разрыв 27 п.п.
Пороги бонусов месячного рейтинга (90/80/70) из-за этого систематически
недоначислялись.

answered_questions пишется инкрементально на каждый ответ, поэтому брошенная
сессия сама показывает точку выхода — отдельный exit_at_question не нужен.

Историчные строки бэкфиллятся точным подсчётом из quiz_questions.

Revision ID: e8f9a0b1c2d3
Revises: d7e8f9a0b1c2
Create Date: 2026-09-29

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "e8f9a0b1c2d3"
down_revision: Union[str, None] = "d7e8f9a0b1c2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "quiz_sessions",
        sa.Column("answered_questions", sa.Integer(), nullable=False, server_default="0"),
    )

    # Точный бэкфилл: сколько вопросов реально было задано в каждой сессии
    op.execute(
        """
        UPDATE quiz_sessions s
        SET answered_questions = COALESCE(q.cnt, 0)
        FROM (
            SELECT session_id, COUNT(*) AS cnt
            FROM quiz_questions
            GROUP BY session_id
        ) q
        WHERE q.session_id = s.id
        """
    )

    op.create_index(
        "ix_quiz_sessions_user_completed",
        "quiz_sessions",
        ["user_id", "completed_at"],
    )


def downgrade() -> None:
    op.drop_index("ix_quiz_sessions_user_completed", table_name="quiz_sessions")
    op.drop_column("quiz_sessions", "answered_questions")
