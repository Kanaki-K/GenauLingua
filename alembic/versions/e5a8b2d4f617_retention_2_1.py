"""Патч 2.1 «Вовлечение»: заморозка серии, лесенка возврата, журнал сообщений

users.streak_freeze_on — день, когда заморозка простила пропуск: следующая
не раньше чем через неделю (`streak_service.advance`).
users.nudge_anchor / nudge_step — лесенка возврата: перерыв и пройденная ступень.
nudge_log — журнал сообщений по инициативе бота и контрольной группы.
quiz_sessions.local_day — день человека на момент завершения занятия:
история серии читается им, а не нынешним поясом (аудит 2.1).

Revision ID: e5a8b2d4f617
Revises: d4f7a1c9e215
Create Date: 2026-10-15
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "e5a8b2d4f617"
down_revision: Union[str, None] = "d4f7a1c9e215"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("streak_freeze_on", sa.Date(), nullable=True))
    op.add_column("users", sa.Column("nudge_anchor", sa.Date(), nullable=True))
    op.add_column("users", sa.Column("nudge_step", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("users", sa.Column("reminders_declined_at", sa.DateTime(), nullable=True))
    op.add_column("quiz_sessions", sa.Column("local_day", sa.Date(), nullable=True))
    op.create_table(
        "nudge_log",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.BigInteger(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("kind", sa.String(16), nullable=False),
        sa.Column("situation", sa.String(16), nullable=True),
        sa.Column("outcome", sa.String(12), nullable=False),
        sa.Column("sent_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_nudge_log_sent", "nudge_log", ["sent_at"])
    op.create_index("ix_nudge_log_user", "nudge_log", ["user_id", "sent_at"])


def downgrade() -> None:
    op.drop_index("ix_nudge_log_user", table_name="nudge_log")
    op.drop_index("ix_nudge_log_sent", table_name="nudge_log")
    op.drop_table("nudge_log")
    op.drop_column("quiz_sessions", "local_day")
    op.drop_column("users", "reminders_declined_at")
    op.drop_column("users", "nudge_step")
    op.drop_column("users", "nudge_anchor")
    op.drop_column("users", "streak_freeze_on")
