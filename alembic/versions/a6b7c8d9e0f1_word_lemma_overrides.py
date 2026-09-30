"""Ручные указания «эта строка — форма, а лемма вот эта»

В базе 99 пар, где форма и лемма лежат как два отдельных слова на одном
уровне: «komm» при существующем «kommen», «tu» при «tun», «gibt» при «geben».
Человек учит их как разные слова, хотя это одно.

Переименовать форму нельзя: уникальность (word_de, level) не даст двум строкам
совпасть. Удалить форму тоже нельзя — у quiz_questions каскадное удаление, и
вместе со словом исчезли бы 326 исторических ответов, а точность в завершённых
сессиях стала бы неверной.

Поэтому форма остаётся строкой, но при сборке групп слов принудительно попадает
в группу леммы, и дальше работает уже проверенный механизм: в викторине
участвует только каноническое слово, а прогресс сливается тем же кодом, что
переносил его при переходе на многоязычность.

Откат — удаление строк отсюда и пересборка групп.

Revision ID: a6b7c8d9e0f1
Revises: f5a6b7c8d9e0
"""

import sqlalchemy as sa
from alembic import op

revision = "a6b7c8d9e0f1"
down_revision = "f5a6b7c8d9e0"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "word_lemma_overrides",
        sa.Column("word_id", sa.Integer(), nullable=False),
        sa.Column("lemma_word_id", sa.Integer(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["word_id"], ["words.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["lemma_word_id"], ["words.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("word_id"),
    )
    op.create_index(
        op.f("ix_word_lemma_overrides_lemma_word_id"),
        "word_lemma_overrides", ["lemma_word_id"], unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_word_lemma_overrides_lemma_word_id"),
                  table_name="word_lemma_overrides")
    op.drop_table("word_lemma_overrides")
