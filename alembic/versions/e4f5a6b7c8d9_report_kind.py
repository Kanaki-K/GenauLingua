"""Вид репорта: ошибка в тексте или в озвучке

С появлением озвучки жалоба перестала быть однозначной: перевод может быть
верным, а произношение нет. Прежние репорты все про текст — озвучки тогда
не существовало, поэтому server_default 'text' и заполнять нечего.

Уникальность расширяется до тройной: одно слово можно зарепортить и по
тексту, и по озвучке, но каждое по одному разу. Прежнее ограничение на пару
(user_id, word_id) запрещало бы вторую жалобу.

Revision ID: e4f5a6b7c8d9
Revises: d3e4f5a6b7c8
"""

import sqlalchemy as sa
from alembic import op

revision = "e4f5a6b7c8d9"
down_revision = "d3e4f5a6b7c8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "translation_reports",
        sa.Column("kind", sa.String(length=8), nullable=False,
                  server_default="text"),
    )
    op.add_column(
        "translation_reports",
        sa.Column("voice", sa.String(length=64), nullable=True),
    )

    op.drop_constraint("uq_translation_reports_user_word",
                       "translation_reports", type_="unique")
    op.create_unique_constraint(
        "uq_translation_reports_user_word_kind",
        "translation_reports", ["user_id", "word_id", "kind"],
    )
    op.create_index("ix_translation_reports_kind", "translation_reports", ["kind"])


def downgrade() -> None:
    op.drop_index("ix_translation_reports_kind", table_name="translation_reports")
    op.drop_constraint("uq_translation_reports_user_word_kind",
                       "translation_reports", type_="unique")
    # Возврат к парной уникальности возможен только если на слово нет двух
    # репортов от одного человека. Жалобы на озвучку убираем — их в прежней
    # схеме представить нечем.
    op.execute("DELETE FROM translation_reports WHERE kind <> 'text'")
    op.create_unique_constraint(
        "uq_translation_reports_user_word",
        "translation_reports", ["user_id", "word_id"],
    )
    op.drop_column("translation_reports", "voice")
    op.drop_column("translation_reports", "kind")
