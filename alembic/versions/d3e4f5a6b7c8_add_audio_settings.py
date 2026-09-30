"""Настройки озвучки: выключатель и выбранный голос на каждый язык

Озвучка включена по умолчанию: её просили в отзывах, и это главное, за чем
человек придёт после обновления. Существующим пользователям она тоже
включается — server_default true, — иначе патч был бы для них невидим.

Голос хранится отдельной таблицей, а не колонками: он осмыслен только в паре
с изучаемым языком и должен подтягиваться свой при переключении языка.
Отсутствие записи означает голос по умолчанию, так что пустая таблица —
рабочее состояние.

Revision ID: d3e4f5a6b7c8
Revises: a0b1c2d3e4f5
"""

import sqlalchemy as sa
from alembic import op

revision = "d3e4f5a6b7c8"
down_revision = "a0b1c2d3e4f5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("audio_enabled", sa.Boolean(), nullable=False,
                  server_default=sa.true()),
    )

    op.create_table(
        "user_tts_voices",
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("lang", sa.String(length=2), nullable=False),
        sa.Column("voice", sa.String(length=64), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "lang"),
    )


def downgrade() -> None:
    op.drop_table("user_tts_voices")
    op.drop_column("users", "audio_enabled")
