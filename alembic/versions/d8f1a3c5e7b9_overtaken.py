"""«Вас обогнали»: кто и когда обогнал человека в месяце (17.10)

Событие записывается в конце занятия того, кто обогнал, а сообщение уходит
позже — через распорядитель сообщений, в общем бюджете «одно в день» и днём.
Две колонки у человека, а не таблица: важен только последний обгон — если
обогнали трижды за утро, сообщение одно, про последнего.

Revision ID: d8f1a3c5e7b9
Revises: c3e5a7b9d1f2
"""

import sqlalchemy as sa
from alembic import op

revision = "d8f1a3c5e7b9"
down_revision = "c3e5a7b9d1f2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("overtaken_by_id", sa.BigInteger(), nullable=True))
    op.add_column("users", sa.Column("overtaken_at", sa.DateTime(), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "overtaken_at")
    op.drop_column("users", "overtaken_by_id")
