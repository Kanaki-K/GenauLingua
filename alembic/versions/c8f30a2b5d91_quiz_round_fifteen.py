"""Круг занятия: 15 вопросов вместо 25

ПОЧЕМУ КОРОЧЕ. Решение владельца. Доводы, которые его поддерживают:

  * В занятии теперь есть вопросы на слух, а они дольше текстовых: клип надо
    дослушать, иногда переслушать. Двадцать пять таких — это уже не пять
    минут, а пятнадцать, и занятие начинают бросать на середине.
  * Короткий круг чаще ДОВОДЯТ до конца, а законченное занятие — это и
    отметка в стрике, и строка в рейтинге, и ощущение «сделал». Три круга по
    пятнадцать дают три таких ощущения, один по сорок пять — одно.

ПОЧЕМУ МЕНЯЕМ И УЖЕ СОХРАНЁННЫЕ СТРОКИ. Колонка `quiz_word_count` есть, но
ЭКРАНА, где её можно задать, в боте нет: поиск по app/bot находит ровно одно
место, и то чтение. Все 233 пользователя имеют 25 просто потому, что это
значение по умолчанию у модели, а не потому, что кто-то его выбрал.

Значит обновить их — не переписать чужой выбор, а поменять то же самое
значение по умолчанию. Если бы экран существовал, трогать можно было бы
только тех, у кого стоит ровно прежнее умолчание, — условие ниже именно
такое и есть, на случай если экран появится раньше, чем эта миграция
доедет до другого окружения.

Revision ID: c8f30a2b5d91
Revises: a5d81c06b4e2
"""

import sqlalchemy as sa
from alembic import op

revision = "c8f30a2b5d91"
down_revision = "a5d81c06b4e2"
branch_labels = None
depends_on = None

OLD_DEFAULT = 25
NEW_DEFAULT = 15


def upgrade() -> None:
    op.alter_column("users", "quiz_word_count", server_default=str(NEW_DEFAULT))
    op.execute(
        sa.text(
            "UPDATE users SET quiz_word_count = :new WHERE quiz_word_count = :old"
        ).bindparams(new=NEW_DEFAULT, old=OLD_DEFAULT)
    )


def downgrade() -> None:
    op.alter_column("users", "quiz_word_count", server_default=str(OLD_DEFAULT))
    op.execute(
        sa.text(
            "UPDATE users SET quiz_word_count = :old WHERE quiz_word_count = :new"
        ).bindparams(new=NEW_DEFAULT, old=OLD_DEFAULT)
    )
