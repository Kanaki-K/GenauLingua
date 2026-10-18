"""Частота слов по языкам: новое слово — среди самых ходовых

Новое слово внутри уровня бралось случайно, и новичок A1 получал Strumpf
раньше Haus; прод 15.10 — новички уходили после первых слов, отвечая на всё
верно. Таблица `word_frequency` (слово, язык → zipf по wordfreq) отдельно
от word_lang_groups: та пересобирается целиком и стёрла бы частоты.
Заполняет `python -m app.scripts.fill_word_frequency`.

Revision ID: c8e2f4a6b913
Revises: b6d1e3f7a920
Create Date: 2026-10-15
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "c8e2f4a6b913"
down_revision: Union[str, None] = "b6d1e3f7a920"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "word_frequency",
        sa.Column("word_id", sa.Integer(), sa.ForeignKey("words.id", ondelete="CASCADE"),
                  primary_key=True),
        sa.Column("lang", sa.String(2), primary_key=True),
        sa.Column("zipf", sa.Float(), nullable=False),
    )
    # Подбор нового слова сортирует по частоте внутри языка
    op.create_index("ix_word_frequency_lang_zipf", "word_frequency", ["lang", "zipf"])


def downgrade() -> None:
    op.drop_index("ix_word_frequency_lang_zipf", table_name="word_frequency")
    op.drop_table("word_frequency")
