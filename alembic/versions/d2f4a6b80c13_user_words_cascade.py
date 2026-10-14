"""user_words: каскадное удаление вслед за человеком и словом

ЗАЧЕМ. `user_words` оказалась единственной таблицей, ссылающейся на
человека без `ON DELETE CASCADE`. Все прочие — `quiz_sessions`,
`monthly_stats`, `translation_reports`, `win_streaks`, `user_tts_voices` —
каскадные. Из-за одной этой таблицы человека нельзя было удалить ВООБЩЕ:

    update or delete on table "users" violates foreign key constraint
    "user_words_user_id_fkey" on table "user_words"

То есть у бота с политикой приватности и живыми людьми не было способа
убрать чьи-то данные, кроме правки базы руками. То же со словом: ряд,
который кто-то хоть раз учил, держался намертво, и чистка словаря от
дефектных рядов упиралась в прогресс.

Нашлось при попытке завести и убрать подопытного в приёмке круга — то
есть ровно там, где удаление и потребовалось впервые.

Revision ID: d2f4a6b80c13
Revises: c5a81f3b7d90
"""

from alembic import op

revision = "d2f4a6b80c13"
down_revision = "c5a81f3b7d90"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Пересоздание с тем же именем: Postgres не умеет менять правило
    # удаления у существующего ключа, только снять и поставить заново
    op.drop_constraint("user_words_user_id_fkey", "user_words", type_="foreignkey")
    op.create_foreign_key(
        "user_words_user_id_fkey", "user_words", "users",
        ["user_id"], ["id"], ondelete="CASCADE",
    )

    op.drop_constraint("user_words_word_id_fkey", "user_words", type_="foreignkey")
    op.create_foreign_key(
        "user_words_word_id_fkey", "user_words", "words",
        ["word_id"], ["id"], ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("user_words_user_id_fkey", "user_words", type_="foreignkey")
    op.create_foreign_key(
        "user_words_user_id_fkey", "user_words", "users", ["user_id"], ["id"],
    )

    op.drop_constraint("user_words_word_id_fkey", "user_words", type_="foreignkey")
    op.create_foreign_key(
        "user_words_word_id_fkey", "user_words", "words", ["word_id"], ["id"],
    )
