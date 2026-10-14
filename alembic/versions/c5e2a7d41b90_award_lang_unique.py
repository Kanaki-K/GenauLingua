"""Награда сезона: язык и уникальность (человек, сезон, язык)

ЗАЧЕМ. Закрытие сезона зовётся первого числа по расписанию и каждый час
страховкой. Пока оно делало commit посреди раздачи (серия побед), сбой
после него оставлял часть наград в базе, а повторный прогон выдал бы их
снова — с бонусом к lifetime. База этому не мешала ничем: у
`monthly_awards` не было уникальности.

Уникальность по (человек, сезон) нельзя: топ-10 подводится ПО ЯЗЫКАМ, и
две награды одного человека за один месяц (немецкий и английский) —
законны. Отсюда сперва колонка языка, потом тройная уникальность.

ЯЗЫК ПРЕЖНИХ НАГРАД берётся из месячной статистики того же человека и
сезона с тем же итоговым местом (`final_rank = rank`). Замер 14 октября
2026: 65 наград, у каждой ровно один такой ряд; дублей по (человек, сезон)
нет. Не нашлось ряда — остаётся «de», язык всех сезонов до шести языков.

Revision ID: c5e2a7d41b90
Revises: b8d4f1a26c37
Create Date: 2026-10-14
"""
from alembic import op
import sqlalchemy as sa

revision = "c5e2a7d41b90"
down_revision = "b8d4f1a26c37"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "monthly_awards",
        sa.Column("learning_lang", sa.String(length=2), nullable=False,
                  server_default="de"),
    )
    op.execute(
        """
        UPDATE monthly_awards a SET learning_lang = ms.learning_lang
        FROM monthly_stats ms
        WHERE ms.user_id = a.user_id
          AND ms.season_id = a.season_id
          AND ms.final_rank = a.rank
        """
    )
    op.create_unique_constraint(
        "uq_monthly_awards_user_season_lang",
        "monthly_awards",
        ["user_id", "season_id", "learning_lang"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_monthly_awards_user_season_lang", "monthly_awards", type_="unique"
    )
    op.drop_column("monthly_awards", "learning_lang")
