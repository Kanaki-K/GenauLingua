"""Напоминания по умолчанию: отметка «включил бот, а не человек»

Решение владельца 16.10: напоминания новичку включаются сами, на час его
первого захода, а предложение «Напоминать раз в день?» уходит. Отметка
нужна контрольной группе: у включённых по умолчанию 10% не получают
сообщений, иначе работают ли они — не узнать. Кто включил или настроил сам,
получает всегда, и отметка снимается.

Тем, кто в боте уже есть, ничего не меняется: колонка у всех False.

Revision ID: b7d2f4a6c8e1
Revises: a1c3e5f7b9d2
"""

import sqlalchemy as sa
from alembic import op

revision = "b7d2f4a6c8e1"
down_revision = "a1c3e5f7b9d2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("reminders_auto", sa.Boolean(), nullable=False,
                                     server_default=sa.false()))


def downgrade() -> None:
    op.drop_column("users", "reminders_auto")
