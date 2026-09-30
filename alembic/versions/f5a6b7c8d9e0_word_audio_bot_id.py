"""Чей file_id: привязка клипа озвучки к боту

По документации Telegram file_id принадлежит конкретному боту и другому боту
не передаётся. Значит клипы, сделанные тестовым ботом, для боевого
недействительны — и наоборот.

Без этой колонки перенос базы между ботами ломал бы озвучку молча: бот
отправлял бы чужие file_id, Telegram отвечал бы ошибкой, и карточки падали бы
одна за другой без объяснения причины. Теперь чужая запись считается промахом
кэша и клип переделывается.

Колонка nullable: у записей, сделанных до этой миграции, бот неизвестен.
Они тоже считаются чужими и переделываются — это дешевле, чем угадывать.

Revision ID: f5a6b7c8d9e0
Revises: e4f5a6b7c8d9
"""

import sqlalchemy as sa
from alembic import op

revision = "f5a6b7c8d9e0"
down_revision = "e4f5a6b7c8d9"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "word_audio",
        sa.Column("bot_id", sa.BigInteger(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("word_audio", "bot_id")
