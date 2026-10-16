"""Итальянский, испанский, французский, чешский: колонки перевода и примера

Как у польского (f9a0b1c2d3e4): колонки добавляются отдельно от открытия
языков. Заполняются они из archive/new_langs/out, а до заполнения языки не
входят в LEARNABLE_LANGS — пустой язык в меню означал бы викторину без слов.

Группы слов строит rebuild_word_groups после заполнения (HANDOVER §12, шаг 7).

Revision ID: a1c3e5f7b9d2
Revises: e5a8b2d4f617
"""

import sqlalchemy as sa
from alembic import op

revision = "a1c3e5f7b9d2"
down_revision = "e5a8b2d4f617"
branch_labels = None
depends_on = None

NEW_LANGS = ("it", "es", "fr", "cs")


def upgrade() -> None:
    for code in NEW_LANGS:
        op.add_column("words", sa.Column(f"translation_{code}", sa.Text(), nullable=True))
        op.add_column("words", sa.Column(f"example_{code}", sa.Text(), nullable=True))


def downgrade() -> None:
    for code in reversed(NEW_LANGS):
        op.drop_column("words", f"example_{code}")
        op.drop_column("words", f"translation_{code}")
