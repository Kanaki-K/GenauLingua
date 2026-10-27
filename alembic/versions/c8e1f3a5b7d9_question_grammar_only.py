"""Сборка по фразе из общей базы — ответ «только грамматика» (2.3)

Владелец 27.10: «грамматика должна быть по сути всегда разная». Своих слов,
доросших до сборки, у человека 10–20, и фразы крутились по кругу. Решение:
сначала фразы своих слов, ещё не собранные, потом — любые фразы базы его
уровня. Такой ответ идёт в «Грамматику» и прогресс слова НЕ трогает: слово
человек не учил, и сборка его фразы не делает его начатым.

Пусто — обычный ответ, как у всех прежних строк: добавление мгновенное.

Revision ID: c8e1f3a5b7d9
Revises: b5d7f9a1c3e4
"""

import sqlalchemy as sa
from alembic import op

revision = "c8e1f3a5b7d9"
down_revision = "b5d7f9a1c3e4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("quiz_questions", sa.Column("grammar_only", sa.Boolean(), nullable=True))


def downgrade() -> None:
    op.drop_column("quiz_questions", "grammar_only")
