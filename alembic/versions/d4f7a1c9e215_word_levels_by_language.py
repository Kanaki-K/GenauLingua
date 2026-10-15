"""Уровень слова в изучаемом языке: английский по Oxford, остальные — понятие + частота

`words.level` — уровень немецкого слова (Goethe); учащий английский получал
немецкие уровни (сверка 15.10: 22% слов расходятся с Oxford на 2+ уровня).
Таблица `word_levels` (слово, язык → уровень) для en, pl, tr, ru, uk;
нет строки — берётся `words.level`. Заполняет
`python -m app.scripts.fill_word_levels`.

Revision ID: d4f7a1c9e215
Revises: c8e2f4a6b913
Create Date: 2026-10-15
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision: str = "d4f7a1c9e215"
down_revision: Union[str, None] = "c8e2f4a6b913"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "word_levels",
        sa.Column("word_id", sa.Integer(), sa.ForeignKey("words.id", ondelete="CASCADE"),
                  primary_key=True),
        sa.Column("lang", sa.String(2), primary_key=True),
        # Тип уровня уже есть в базе — тот же, что у words.level
        sa.Column("level", postgresql.ENUM(name="cefrlevel", create_type=False), nullable=False),
    )
    op.create_index("ix_word_levels_lang_level", "word_levels", ["lang", "level"])


def downgrade() -> None:
    op.drop_index("ix_word_levels_lang_level", table_name="word_levels")
    op.drop_table("word_levels")
