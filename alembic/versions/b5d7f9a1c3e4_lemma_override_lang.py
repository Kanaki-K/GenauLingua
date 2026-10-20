"""Указание леммы — для одного изучаемого языка (2.3)

Свод естественности 20.10: книжное немецкое слово заменяется разговорным
(Checkpoint → Kontrolle, Nahrungsmittel → Lebensmittel), книжное выключается.
Для этого годится проверенное указание «эта строка — та же единица, что вон
та»: прогресс сливается, ничего не удаляется. Но прежде оно действовало на
все языки, а книжное оно только в немецком — английское «checkpoint» живое.

Пусто — указание для всех языков, как у прежних 140 (формы слов).

Revision ID: b5d7f9a1c3e4
Revises: a3c5e7f9b1d2
"""

import sqlalchemy as sa
from alembic import op

revision = "b5d7f9a1c3e4"
down_revision = "a3c5e7f9b1d2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("word_lemma_overrides", sa.Column("lang", sa.String(2), nullable=True))


def downgrade() -> None:
    op.drop_column("word_lemma_overrides", "lang")
