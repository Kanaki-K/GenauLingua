"""Патч 2.1 «Удержание»: заморозка серии и сообщение второго дня

users.streak_freeze_on — день, когда заморозка простила пропуск: следующая
не раньше чем через неделю (`streak_service.advance`).
users.day2_hook_sent_at — когда новичку ушло сообщение второго дня (одно).

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
    op.add_column("users", sa.Column("day2_hook_sent_at", sa.DateTime(), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "day2_hook_sent_at")
    op.drop_column("users", "streak_freeze_on")
