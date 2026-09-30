"""Польский язык: колонки перевода и примера

Колонки добавляются отдельно от включения польского в обучение. Заполняются
они скриптом переводов, а до заполнения польский не входит в LEARNABLE_LANGS:
пустой язык в меню означал бы викторину без слов.

Группы слов (word_lang_groups) для польского собираются тем же
rebuild_word_groups после заполнения колонок — миграция их не строит,
потому что строить группы по пустым колонкам нечего.

Revision ID: f9a0b1c2d3e4
Revises: e8f9a0b1c2d3
"""

import sqlalchemy as sa
from alembic import op

revision = "f9a0b1c2d3e4"
down_revision = "e8f9a0b1c2d3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("words", sa.Column("translation_pl", sa.Text(), nullable=True))
    op.add_column("words", sa.Column("example_pl", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("words", "example_pl")
    op.drop_column("words", "translation_pl")
