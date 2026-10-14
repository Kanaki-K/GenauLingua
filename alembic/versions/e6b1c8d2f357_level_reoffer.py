"""Отказ подняться на уровень — не навсегда: запоминаем, на каком занятии

Revision ID: e6b1c8d2f357
Revises: d9a3f0c7e214
Create Date: 2026-10-14

Прежде отказ «не хочу с A1 на A2» запоминался навсегда: на этом уровне бот
больше не спрашивал никогда, даже когда человек давно его перерос.
Владелец, 14 октября: «если он ещё 5 игр будет на высоком уровне —
предлагаем перейти». Для этого нужно знать, на каком занятии был отказ.

Прежним отказам ставится номер занятия на момент выкатки: следующее
предложение — не раньше, чем через пять занятий после неё. Правило —
`level_service.should_offer_next_level`.
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "e6b1c8d2f357"
down_revision: Union[str, None] = "d9a3f0c7e214"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("level_offer_declined_round", sa.Integer(), nullable=True))
    # Прежним отказам — номер текущего занятия: следующее предложение не
    # раньше, чем через пять занятий после выкатки, а не сразу же
    op.execute(
        "UPDATE users SET level_offer_declined_round = quizzes_passed "
        "WHERE level_offer_declined IS NOT NULL"
    )


def downgrade() -> None:
    op.drop_column("users", "level_offer_declined_round")
