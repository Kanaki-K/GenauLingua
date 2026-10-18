"""«Говорю» по желанию: выбор человека и когда спрашивали (2.2.1)

Владелец 18.10: игру «Говорю» — по желанию. Прод 14–18.10: показана 78 раз,
пропущена 42, голосом ответили 6 человек; одному показана 23 раза и 21 раз
пропущена.

Перенос смысла (урок 2.1 — новая отметка обязана перенести смысл старой):
  * говорил хотя бы раз верно — 'on': для него ничего не меняется;
  * сам убрал «Говорю» из игр (в составе нет 's') — 'off';
  * остальные — пусто: игры нет, пока не согласятся на приглашение.

Revision ID: e9a2c4b6d8f0
Revises: d8f1a3c5e7b9
"""

import sqlalchemy as sa
from alembic import op

revision = "e9a2c4b6d8f0"
down_revision = "d8f1a3c5e7b9"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("speech_choice", sa.String(8), nullable=True))
    op.add_column("users", sa.Column("speech_asked_at", sa.DateTime(), nullable=True))
    op.execute("""
        update users set speech_choice = 'on'
        where exists (select 1 from user_words w where w.user_id = users.id
                      and coalesce(w.correct_speech, 0) > 0)
    """)
    op.execute("""
        update users set speech_choice = 'off'
        where speech_choice is null and position('s' in coalesce(quiz_channels, 'tasrb')) = 0
    """)


def downgrade() -> None:
    op.drop_column("users", "speech_asked_at")
    op.drop_column("users", "speech_choice")
