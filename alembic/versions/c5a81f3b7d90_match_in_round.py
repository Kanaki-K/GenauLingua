"""Показывать ли доску сопоставления внутри круга

ЗАЧЕМ ОТДЕЛЬНАЯ КОЛОНКА, А НЕ БУКВА В `quiz_channels`. Там лежат КАНАЛЫ —
способы задать вопрос про ОДНО слово, и `pick_channel` выбирает из них для
каждого слова отдельно. Доска же берёт пять слов сразу, и каналом быть не
может: выбери её «для слова» — и непонятно, что делать с остальными
четырьмя.

ПОЧЕМУ ПО УМОЛЧАНИЮ ВКЛЮЧЕНО. Значение по умолчанию — это и есть решение о
том, увидят ли люди новое. В проекте уже измерено, чем кончается
«сделали, но по умолчанию выключено»: 223 пользователя из 233 не меняли
режим викторины НИ РАЗУ, 117 из 121 не меняли время напоминания. Спрячь
доску за переключателем — и её не увидит никто.

Revision ID: c5a81f3b7d90
Revises: b94d2f017ae3
"""

import sqlalchemy as sa
from alembic import op

revision = "c5a81f3b7d90"
down_revision = "b94d2f017ae3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("match_in_round", sa.Boolean(), nullable=False,
                  server_default=sa.true()),
    )


def downgrade() -> None:
    op.drop_column("users", "match_in_round")
