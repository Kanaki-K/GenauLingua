"""Шестая игра: «Собираю» — собрать пример из кнопок-слов

Пример слова показан на родном языке, человек собирает его на изучаемом,
нажимая слова в нужном порядке. Среди кнопок — слова-ловушки из того же
языка (der/den/dem, ist/sind), поэтому игра проверяет не только слова, но
и грамматику: порядок и формы. Решение владельца: игра входит в текущее
большое обновление, выкатка после неё.

ЧТО ДОБАВЛЯЕТСЯ

    user_words.shown_build / correct_build
        Своя пара счётчиков — как у каждой игры: без неё «узнаю слово» и
        «соберу с ним фразу» слились бы в одно число, а текстовый счёт
        выводится ВЫЧИТАНИЕМ всех каналов из итога и врал бы на каждую
        сборку.

    monthly_stats.correct_build
        Балл сезона считается по каналам (сборка стоит 3, как речь), а
        текстовый — вычитанием; без колонки сборки оплачивались бы как
        карточки.

    users.quiz_channels: дописать «b» ВСЕМ
        Значение по умолчанию и есть решение о том, увидят ли люди новое:
        прошлые игры (`e4b7d2906f51` — речь, `a7c3e9f10b22` — припоминание)
        включались всем, и эта — тоже. Дописывается каждому, у кого буквы
        «b» ещё нет, а не только составу «tasr»: игра не требует звука, и
        человек, выключивший слух и речь («tr»), получить её может — а
        выключить сам, в настройках, одним нажатием.

Длина колонки — 8, состав «tasrb» — 5: расширять не нужно.

Revision ID: b6d1e3f7a920
Revises: f2c7a9d4e801
Create Date: 2026-10-14
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "b6d1e3f7a920"
down_revision: Union[str, None] = "f2c7a9d4e801"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "user_words",
        sa.Column("shown_build", sa.Integer(), nullable=False, server_default="0"),
    )
    op.add_column(
        "user_words",
        sa.Column("correct_build", sa.Integer(), nullable=False, server_default="0"),
    )
    op.add_column(
        "monthly_stats",
        sa.Column("correct_build", sa.Integer(), nullable=False, server_default="0"),
    )

    op.alter_column(
        "users", "quiz_channels",
        existing_type=sa.String(length=8),
        existing_nullable=False,
        server_default="tasrb",
    )

    # Буква дописывается В КОНЕЦ: порядок букв в строке не значим
    # (`enabled_channels` идёт по перечислению), а конец не трогает
    # остальной состав
    op.execute(
        "UPDATE users SET quiz_channels = quiz_channels || 'b' "
        "WHERE position('b' in quiz_channels) = 0"
    )


def downgrade() -> None:
    # До этой ревизии буквы «b» не было ни у кого — убрать её у всех и
    # есть точная обратная операция
    op.execute("UPDATE users SET quiz_channels = replace(quiz_channels, 'b', '')")
    op.alter_column(
        "users", "quiz_channels",
        existing_type=sa.String(length=8),
        existing_nullable=False,
        server_default="tasr",
    )
    op.drop_column("monthly_stats", "correct_build")
    op.drop_column("user_words", "correct_build")
    op.drop_column("user_words", "shown_build")
