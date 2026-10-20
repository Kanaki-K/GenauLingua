"""Что показали и что выбрали: варианты и выбранное слово у ответа (2.2.4)

Владелец 20.10: «нужно записывать неправильные ответы, чтобы понимать и иметь
возможность разобрать». Прод 20.10: до 2.0 текст ответа пуст у всех 3156
ошибок; с 2.0 есть у 208 из 208, но без вариантов и без номера выбранного
слова. Колонки пустые у прежних строк — восстанавливать их нечем.

Обе колонки допускают пустое: добавление мгновенное, таблица не
переписывается.

Revision ID: a3c5e7f9b1d2
Revises: e9a2c4b6d8f0
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "a3c5e7f9b1d2"
down_revision = "e9a2c4b6d8f0"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("quiz_questions", sa.Column("options", postgresql.JSONB(), nullable=True))
    op.add_column("quiz_questions", sa.Column("chosen_word_id", sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column("quiz_questions", "chosen_word_id")
    op.drop_column("quiz_questions", "options")
