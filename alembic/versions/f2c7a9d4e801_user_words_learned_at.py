"""Когда слово стало выученным: user_words.learned_at

Revision ID: f2c7a9d4e801
Revises: e6b1c8d2f357
Create Date: 2026-10-14

Месячный балл «+3 за выученное слово» считал выученные слова с последним
показом в месяце: слово, повторённое по расписанию в следующем месяце,
оплачивалось снова, а «за всё время» (сумма месяцев) брало его дважды.
Теперь платится переход в «выучено» — по дате перехода.

Бэкафилл: у уже выученных слов дата перехода неизвестна, ставится
`last_seen_at` — ровно то, чем их считал прежний код. Поэтому действующий
месяц от выкатки не меняется ни на балл (у слов, выученных раньше и
повторённых в этом месяце, last_seen_at и так в этом месяце), а со
следующего повторения дата больше не сдвигается.
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "f2c7a9d4e801"
down_revision: Union[str, None] = "e6b1c8d2f357"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("user_words", sa.Column("learned_at", sa.DateTime(), nullable=True))
    op.execute(
        "UPDATE user_words SET learned_at = COALESCE(last_seen_at, created_at) "
        "WHERE learned"
    )


def downgrade() -> None:
    op.drop_column("user_words", "learned_at")
