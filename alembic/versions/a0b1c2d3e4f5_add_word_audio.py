"""Кэш озвучки: file_id уже загруженных в Telegram клипов

Полная озвучка базы — 106 380 клипов и 2,2 ГБ файлами. Но Telegram отдаёт
однажды загруженный файл по file_id бесконечно, поэтому на диске держать
нечего: вся озвучка весит здесь около 10 МБ.

Таблица заполняется лениво при первом показе слова, так что пустая таблица —
рабочее состояние, а не незавершённая миграция.

Revision ID: a0b1c2d3e4f5
Revises: f9a0b1c2d3e4
"""

import sqlalchemy as sa
from alembic import op

revision = "a0b1c2d3e4f5"
down_revision = "f9a0b1c2d3e4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "word_audio",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("word_id", sa.Integer(), nullable=False),
        sa.Column("lang", sa.String(length=2), nullable=False),
        sa.Column("kind", sa.String(length=8), nullable=False),
        sa.Column("voice", sa.String(length=64), nullable=False),
        sa.Column("file_id", sa.String(length=255), nullable=False),
        sa.Column("file_kind", sa.String(length=8), nullable=False),
        sa.Column("spoken_text", sa.Text(), nullable=False),
        sa.Column("duration_seconds", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["word_id"], ["words.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        # Уникальный ключ, а не просто индекс: при ленивом заполнении два
        # одновременных показа одного слова иначе создали бы две записи
        sa.UniqueConstraint("word_id", "lang", "kind", "voice",
                            name="uq_word_audio_key"),
    )
    op.create_index(
        "ix_word_audio_lookup", "word_audio",
        ["word_id", "lang", "kind", "voice"], unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_word_audio_lookup", table_name="word_audio")
    op.drop_table("word_audio")
