"""Напоминания — всем, к выкатке новой версии

Revision ID: d9a3f0c7e214
Revises: c5e2a7d41b90
Create Date: 2026-10-14

РЕШЕНИЕ ВЛАДЕЛЬЦА: к выкатке включить напоминания у всех — «ведь так они
увидят апгрейд». Без этого 112 из 233 человек узнали бы о пяти играх,
озвучке и шести языках, только если сами откроют бота, а замер петли
возврата показал, что сами не открывают: 79% ни разу не занимались два
дня подряд.

ПОЧЕМУ ЭТО ПОЧТИ НИКОГО НЕ ПЕРЕУБЕЖДАЕТ. По умолчанию у новичков
напоминания ВЫКЛЮЧЕНЫ (`default=False`), а последний раз их включали всем
в марте (`9194af87e5d4`). Значит выключенные — в основном те, кто пришёл
после марта и ни разу не выбирал. Явно отказавшихся отличить нельзя:
отметка «бот предлагал» (`reminder_offered_at`) появилась в этой же
версии, и у всех выключенных она пуста.

ЧТО ЗАЩИЩАЕТ ТЕХ, КТО ВСЁ ЖЕ ОТКАЗЫВАЛСЯ. Выключить можно одной кнопкой
под самим напоминанием. Заблокировавшим бота напоминание больше не
стучится: первая же попытка с `TelegramForbiddenError` выключает их сама.

Выбранные человеком время и дни НЕ ТРОГАЮТСЯ — меняется только флаг.
Пустые значения заполняются теми же, что ставит модель.

Отката нет, как и у мартовской: прежнее состояние флага не сохраняется, и
«вернуть как было» значит выключить напоминания у тех, кто успел их
захотеть.
"""
from typing import Sequence, Union

from alembic import op

revision: str = "d9a3f0c7e214"
down_revision: Union[str, None] = "c5e2a7d41b90"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("UPDATE users SET notification_time = '20:00' WHERE notification_time IS NULL")
    op.execute(
        "UPDATE users SET notification_days = '{0,1,2,3,4,5,6}' "
        "WHERE notification_days IS NULL OR cardinality(notification_days) = 0"
    )
    op.execute("UPDATE users SET timezone = 'Europe/Berlin' WHERE timezone IS NULL")
    op.execute("UPDATE users SET notifications_enabled = true WHERE notifications_enabled = false")


def downgrade() -> None:
    pass
