"""Жалоба на перевод знает пару языков (Н4–Н6, 16.10)

Прежде у жалобы не было языков: какой язык человек учил, угадывалось по
занятию, а без занятия — по НЫНЕШНЕМУ языку человека, и вторая сторона пары
не была известна вовсе. С десятью языками жалоба «перевод неверный» без
пары не говорит, какую из девяти колонок править.

Старые жалобы заполняются по занятию, из которого пришли, а без занятия —
по нынешней паре человека (лучшее, что есть). Уникальность — с парой: на
одно слово можно пожаловаться в каждой паре отдельно.

Revision ID: c3e5a7b9d1f2
Revises: b7d2f4a6c8e1
"""

import sqlalchemy as sa
from alembic import op

revision = "c3e5a7b9d1f2"
down_revision = "b7d2f4a6c8e1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("translation_reports", sa.Column("learning_lang", sa.String(2), nullable=True))
    op.add_column("translation_reports", sa.Column("native_lang", sa.String(2), nullable=True))
    op.execute("""
        UPDATE translation_reports r
           SET learning_lang = q.learning_lang, native_lang = q.native_lang
          FROM quiz_sessions q
         WHERE r.quiz_session_id = q.id AND r.learning_lang IS NULL
    """)
    op.execute("""
        UPDATE translation_reports r
           SET learning_lang = coalesce(u.learning_lang, 'de'),
               native_lang = coalesce(u.native_lang, 'ru')
          FROM users u
         WHERE r.user_id = u.id AND r.learning_lang IS NULL
    """)
    op.drop_constraint("uq_translation_reports_user_word_kind", "translation_reports",
                       type_="unique")
    op.create_unique_constraint(
        "uq_translation_reports_user_word_kind_pair", "translation_reports",
        ["user_id", "word_id", "kind", "learning_lang", "native_lang"],
    )


def downgrade() -> None:
    op.drop_constraint("uq_translation_reports_user_word_kind_pair", "translation_reports",
                       type_="unique")
    # Жалобы на одно слово в разных парах при откате схлопываются в одну
    op.execute("""
        DELETE FROM translation_reports a USING translation_reports b
         WHERE a.user_id = b.user_id AND a.word_id = b.word_id
           AND a.kind = b.kind AND a.id > b.id
    """)
    op.create_unique_constraint(
        "uq_translation_reports_user_word_kind", "translation_reports",
        ["user_id", "word_id", "kind"],
    )
    op.drop_column("translation_reports", "native_lang")
    op.drop_column("translation_reports", "learning_lang")
