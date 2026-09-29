"""multilang learning: language pair instead of translation_mode, per-language progress and seasons

Что делает:
  1. users        — learning_lang / native_lang / reverse_mode (бэкфилл из translation_mode)
  2. quiz_sessions— то же + translation_mode становится nullable
  3. user_words   — learning_lang в первичном ключе (прогресс отдельно по языкам)
  4. monthly_stats— learning_lang + уникальность (user_id, season_id, learning_lang)
  5. word_lang_groups — схлопывание строк, дающих одно слово на данном языке
  6. перепривязка существующего прогресса на канонические слова с объединением счётчиков

Существующие пользователи молча остаются на немецком: learning_lang='de',
native_lang из interface_language. Прогресс сохраняется.

Revision ID: d7e8f9a0b1c2
Revises: f61639c52096
Create Date: 2026-09-29

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "d7e8f9a0b1c2"
down_revision: Union[str, None] = "f61639c52096"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Разбор старого enum на пару языков. Значения в БД в верхнем регистре
# (закреплено миграцией aad3c50ea59b).
_LEGACY_PAIRS = {
    "DE_TO_RU": ("de", "ru", False),
    "RU_TO_DE": ("de", "ru", True),
    "DE_TO_UK": ("de", "uk", False),
    "UK_TO_DE": ("de", "uk", True),
    "DE_TO_EN": ("de", "en", False),
    "EN_TO_DE": ("de", "en", True),
    "DE_TO_TR": ("de", "tr", False),
    "TR_TO_DE": ("de", "tr", True),
}


def _backfill_pair_sql(table: str, reverse_col: str) -> str:
    """
    SQL для проставления пары языков из translation_mode.
    Изучаемый язык всегда немецкий — других пар в старом enum не было.
    """
    # Сравнение идёт через ::text, а не с enum-литералом. PostgreSQL запрещает
    # использовать значение enum, добавленное в этой же транзакции
    # (ALTER TYPE ... ADD VALUE в миграции aad3c50ea59b), и на чистой базе,
    # где все миграции выполняются одной транзакцией, enum-литерал падает
    # с UnsafeNewEnumValueUsage. Приведение к тексту от этого свободно.
    native_cases = "\n".join(
        f"            WHEN translation_mode::text = '{mode}' THEN '{native}'"
        for mode, (_, native, _) in _LEGACY_PAIRS.items()
    )
    reverse_modes = ", ".join(
        f"'{mode}'" for mode, (_, _, rev) in _LEGACY_PAIRS.items() if rev
    )
    # COALESCE обязателен: у части пользователей translation_mode = NULL
    # (поле стало nullable в миграции f1a2b3c4d5e6), а IN по NULL даёт NULL,
    # что нарушило бы NOT NULL на колонке направления.
    return f"""
        UPDATE {table} SET
            learning_lang = 'de',
            native_lang = CASE
{native_cases}
                ELSE COALESCE(NULLIF({_interface_expr(table)}, ''), 'ru')
            END,
            {reverse_col} = COALESCE(translation_mode::text IN ({reverse_modes}), false)
    """


def _interface_expr(table: str) -> str:
    """Откуда брать язык значения, если translation_mode не заполнен."""
    if table == "users":
        return "interface_language"
    # для quiz_sessions берём язык владельца сессии
    return "(SELECT u.interface_language FROM users u WHERE u.id = quiz_sessions.user_id)"


def upgrade() -> None:
    # ========================================================================
    # 1. users
    # ========================================================================
    op.add_column("users", sa.Column("learning_lang", sa.String(2), nullable=False, server_default="de"))
    op.add_column("users", sa.Column("native_lang", sa.String(2), nullable=False, server_default="ru"))
    op.add_column("users", sa.Column("reverse_mode", sa.Boolean(), nullable=False, server_default=sa.false()))

    op.execute(_backfill_pair_sql("users", "reverse_mode"))
    # Язык значения не может совпадать с изучаемым — иначе вопрос выродится
    # в «слово = слово». Немецкоязычного интерфейса нет, так что коллизия
    # возможна только при битых данных.
    op.execute("UPDATE users SET native_lang = 'ru' WHERE native_lang = learning_lang")

    # ========================================================================
    # 2. quiz_sessions
    # ========================================================================
    op.add_column("quiz_sessions", sa.Column("learning_lang", sa.String(2), nullable=False, server_default="de"))
    op.add_column("quiz_sessions", sa.Column("native_lang", sa.String(2), nullable=False, server_default="ru"))
    op.add_column("quiz_sessions", sa.Column("is_reverse", sa.Boolean(), nullable=False, server_default=sa.false()))

    op.execute(_backfill_pair_sql("quiz_sessions", "is_reverse"))
    op.execute("UPDATE quiz_sessions SET native_lang = 'ru' WHERE native_lang = learning_lang")

    # Пары без немецкого (ru→en и т.п.) в старом enum не выражаются
    op.alter_column("quiz_sessions", "translation_mode", existing_type=sa.Enum(name="translationmode"),
                    nullable=True)

    # ========================================================================
    # 3. user_words — learning_lang в PK
    # ========================================================================
    op.add_column("user_words", sa.Column("learning_lang", sa.String(2), nullable=False, server_default="de"))

    # Дублирующий UNIQUE на тех же колонках, что и PK — лишний индекс, убираем
    op.drop_constraint("uq_user_words_user_id_word_id", "user_words", type_="unique")
    op.drop_constraint("user_words_pkey", "user_words", type_="primary")
    op.create_primary_key("user_words_pkey", "user_words", ["user_id", "word_id", "learning_lang"])

    # ========================================================================
    # 4. monthly_stats — сезоны отдельно по языкам
    # ========================================================================
    op.add_column("monthly_stats", sa.Column("learning_lang", sa.String(2), nullable=False, server_default="de"))
    op.drop_constraint("uq_monthly_stats_user_season", "monthly_stats", type_="unique")
    op.create_unique_constraint(
        "uq_monthly_stats_user_season_lang", "monthly_stats", ["user_id", "season_id", "learning_lang"]
    )

    # ========================================================================
    # 5. word_lang_groups
    # ========================================================================
    op.create_table(
        "word_lang_groups",
        sa.Column("lang", sa.String(2), nullable=False),
        sa.Column("word_id", sa.Integer(), nullable=False),
        sa.Column("canonical_id", sa.Integer(), nullable=False),
        sa.Column("is_canonical", sa.Boolean(), nullable=False),
        sa.Column("norm_key", sa.String(255), nullable=False),
        sa.ForeignKeyConstraint(["word_id"], ["words.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["canonical_id"], ["words.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("lang", "word_id"),
    )
    op.create_index("ix_wlg_lang_canonical", "word_lang_groups", ["lang", "canonical_id"])
    op.create_index("ix_wlg_canonical_lookup", "word_lang_groups", ["lang", "is_canonical"])
    op.create_index("ix_wlg_lang_norm_key", "word_lang_groups", ["lang", "norm_key"])

    # ========================================================================
    # 6. Наполнение групп + перепривязка прогресса
    # ========================================================================
    # Нормализация живёт в app/services/language_service.py — она же
    # используется скриптом пересборки, так что логика не расходится.
    from app.services.word_groups import build_groups, remap_user_progress_to_canonical

    bind = op.get_bind()
    build_groups(bind)
    remap_user_progress_to_canonical(bind)


def downgrade() -> None:
    op.drop_index("ix_wlg_lang_norm_key", table_name="word_lang_groups")
    op.drop_index("ix_wlg_canonical_lookup", table_name="word_lang_groups")
    op.drop_index("ix_wlg_lang_canonical", table_name="word_lang_groups")
    op.drop_table("word_lang_groups")

    op.drop_constraint("uq_monthly_stats_user_season_lang", "monthly_stats", type_="unique")
    # Схлопываем языки обратно в одну строку на (user, season), иначе
    # прежний UNIQUE не создастся.
    op.execute(
        """
        DELETE FROM monthly_stats m
        USING monthly_stats keep
        WHERE m.user_id = keep.user_id
          AND m.season_id = keep.season_id
          AND m.id > keep.id
        """
    )
    op.create_unique_constraint("uq_monthly_stats_user_season", "monthly_stats", ["user_id", "season_id"])
    op.drop_column("monthly_stats", "learning_lang")

    # Прогресс по не-немецким языкам при откате теряется: в прежней схеме
    # его негде хранить.
    op.execute("DELETE FROM user_words WHERE learning_lang <> 'de'")
    op.drop_constraint("user_words_pkey", "user_words", type_="primary")
    op.create_primary_key("user_words_pkey", "user_words", ["user_id", "word_id"])
    op.create_unique_constraint("uq_user_words_user_id_word_id", "user_words", ["user_id", "word_id"])
    op.drop_column("user_words", "learning_lang")

    # Сессии без немецкого в старый enum не переводятся — им ставим DE_TO_RU,
    # иначе NOT NULL не вернуть.
    op.execute("UPDATE quiz_sessions SET translation_mode = 'DE_TO_RU' WHERE translation_mode IS NULL")
    op.alter_column("quiz_sessions", "translation_mode", existing_type=sa.Enum(name="translationmode"),
                    nullable=False)
    op.drop_column("quiz_sessions", "is_reverse")
    op.drop_column("quiz_sessions", "native_lang")
    op.drop_column("quiz_sessions", "learning_lang")

    op.drop_column("users", "reverse_mode")
    op.drop_column("users", "native_lang")
    op.drop_column("users", "learning_lang")
