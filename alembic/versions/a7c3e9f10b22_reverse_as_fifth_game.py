"""Пятая игра: припоминание слова по значению

Направление перестаёт быть настройкой на весь круг и становится игрой
среди пятнадцати вопросов. Решение владельца дословно: «реверс будет игрой
5, которая логически будет расставлена среди 15ти вопросов».

ЗАМЕР, НА КОТОРОМ ЭТО СТОИТ:

    у кого «режим перевода» включён        10 из 233
    кругов в обратную сторону              65 из 1 769
    ответов в них                       1 002 из 28 204
    точность прямых вопросов                  87.9%
    точность обратных                         87.1%

Настройка, которой пользуются десять человек, — не выбор, а балласт. При
этом точность в обе стороны одинаковая, и это не довод против игры, а
довод против её ЦЕНЫ: припоминание платит столько же, сколько карточка
(1 балл), пока свои числа не покажут обратное.

ЧТО ДОБАВЛЯЕТСЯ

    user_words.shown_reverse / correct_reverse
        Своя пара счётчиков — по той же причине, по какой она есть у слуха
        и речи: без неё бот не отличит «узнаю das Metall» от «вспомню, что
        металл — это das Metall», и подбор не сможет догружать слабую
        сторону. Прежде направление в прогрессе слова не отражалось ВОВСЕ.

    monthly_stats.correct_reverse
        Чтобы балл сезона считался по каналам, а текстовый выводился
        вычитанием и не мог разойтись с итогом.

    users.quiz_channels: «tas» → «tasr»
        Значение по умолчанию и есть решение о том, увидят ли люди новое:
        223 человека из 233 ни разу не меняли режим викторины. Новый канал
        дописывается ВСЕМ, у кого состав был «tas», — то есть всей базе;
        у кого состав свой, он не трогается.

    users.reverse_mode остаётся в базе и перестаёт влиять на круг
        Колонка не удаляется: по ней видно, кто пользовался прежним
        режимом, и прежние занятия (`quiz_sessions.is_reverse`) остаются
        объяснимыми. Удалять данные, которые ещё могут понадобиться для
        разбора, — отдельное решение, и к этому оно не относится.

Revision ID: a7c3e9f10b22
Revises: e4b7d2906f51
Create Date: 2026-10-14
"""
from alembic import op
import sqlalchemy as sa

revision = "a7c3e9f10b22"
down_revision = "e4b7d2906f51"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "user_words",
        sa.Column("shown_reverse", sa.Integer(), nullable=False,
                  server_default="0"),
    )
    op.add_column(
        "user_words",
        sa.Column("correct_reverse", sa.Integer(), nullable=False,
                  server_default="0"),
    )
    op.add_column(
        "monthly_stats",
        sa.Column("correct_reverse", sa.Integer(), nullable=False,
                  server_default="0"),
    )

    op.alter_column(
        "users", "quiz_channels",
        existing_type=sa.String(length=8),
        existing_nullable=False,
        server_default="tasr",
    )

    # Дописываем пятую игру ТЕМ, У КОГО СОСТАВ НЕ ТРОНУТ. Условие на «tas»
    # нарочно: человек, собравший состав сам, своего выбора не терял — а
    # таких по замеру 13 октября не было ни одного, и условие бережёт
    # будущих, а не нынешних.
    op.execute("UPDATE users SET quiz_channels = 'tasr' WHERE quiz_channels = 'tas'")


def downgrade() -> None:
    op.execute("UPDATE users SET quiz_channels = 'tas' WHERE quiz_channels = 'tasr'")
    op.alter_column(
        "users", "quiz_channels",
        existing_type=sa.String(length=8),
        existing_nullable=False,
        server_default="tas",
    )
    op.drop_column("monthly_stats", "correct_reverse")
    op.drop_column("user_words", "correct_reverse")
    op.drop_column("user_words", "shown_reverse")
