"""
Напоминания: когда их предлагать и на какой час ставить.

Напоминания — единственный замеренный рычаг возврата. У тех, кто их
включил, 6.85 дней занятий против 1.59 у остальных, то есть в 4.3 раза.
Это корреляция, не причинность — человек, включивший напоминания, и так был
настроен заниматься, — но ни один другой признак в данных не даёт разницы
такого порядка.

При этом сами напоминания остаются настройкой, которую надо найти, а
настройки не находят: 117 человек из 121 не менял даже время, 232 из 233 не
менял часовой пояс. Поэтому бот и предлагает их сам, и сам же выбирает час.

Разбор целиком — `MENU_CONCEPT.md`.
"""

from __future__ import annotations

import logging
from zoneinfo import ZoneInfo

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.clock import utcnow
from app.database.models import QuizSession, User

logger = logging.getLogger(__name__)

# Час UTC, на который ставить напоминание человеку БЕЗ истории занятий.
#
# Не круглое число и не «20:00 как принято»: замерено по всем 2 318 кругам
# базы. Пик приходится на 12–13 UTC, плато тянется до 17, и 13 — его начало.
# Прежнее значение по умолчанию (14:00 в Europe/Berlin, то есть 12–13 UTC)
# попало в этот же пик случайно: его никто не выбирал, оно просто стояло в
# коде. Теперь оно хотя бы названо тем, что есть.
FALLBACK_HOUR_UTC = 13

# Сколько кругов должно быть за человеком, чтобы верить его собственному
# расписанию. Один круг — это не привычка, а случай: ткнул в ссылку в
# обеденный перерыв, и напоминание навсегда село бы на этот час.
MIN_ROUNDS_FOR_OWN_TIME = 3


async def suggest_reminder_time(user: User, session: AsyncSession) -> str:
    """
    Час, в который человек обычно занимается, — в ЕГО часовом поясе, «HH:00».

    Планировщик сравнивает `notification_time` с местным временем человека,
    поэтому замеренный час UTC надо перевести в его зону. Шаг этот легко
    забыть, и тогда напоминание приходит со сдвигом на пару часов — молча,
    потому что оно всё равно приходит.

    Минуты всегда нулевые нарочно: точность до минуты тут мнимая, а
    планировщик и так допускает расхождение в две минуты.
    """
    rows = (await session.execute(
        select(
            func.extract("hour", QuizSession.started_at).label("h"),
            func.count().label("n"),
        )
        .where(QuizSession.user_id == user.id)
        .group_by("h")
        .order_by(func.count().desc(), "h")
    )).all()

    total = sum(int(n) for _, n in rows)
    if total >= MIN_ROUNDS_FOR_OWN_TIME and rows:
        hour_utc = int(rows[0][0])
    else:
        hour_utc = FALLBACK_HOUR_UTC

    zone = user.timezone or "UTC"
    try:
        local = (
            utcnow()
            .replace(hour=hour_utc, minute=0, second=0, microsecond=0,
                     tzinfo=ZoneInfo("UTC"))
            .astimezone(ZoneInfo(zone))
        )
    except Exception:
        # Неизвестная зона — отдаём час как есть, это всё равно лучше, чем
        # не поставить напоминание вовсе
        logger.warning("неизвестный часовой пояс %r у пользователя %s", zone, user.id)
        return f"{hour_utc:02d}:00"

    return f"{local.hour:02d}:00"


async def enable_reminders(user: User, session: AsyncSession) -> str:
    """
    Включить напоминания одним нажатием. Возвращает поставленное время.

    Часовой пояс НЕ СПРАШИВАЕТСЯ. Общий переключатель в настройках ведёт
    сперва на выбор города, и это уместно там, где человек сам пришёл
    настраивать. Здесь же вопрос стоит ровно один — «напоминать?», — и
    второй экран поверх него убил бы весь смысл: нажатий должно быть одно.
    Зона остаётся прежней, а час берётся из фактической активности, то есть
    приходит напоминание всё равно тогда, когда человек обычно здесь.
    """
    user.notifications_enabled = True
    user.notification_time = await suggest_reminder_time(user, session)
    user.reminders_auto = False
    user.reminder_offered_at = utcnow()
    await session.commit()
    return user.notification_time


async def mark_reminders_offered(user: User, session: AsyncSession) -> None:
    """Запомнить, что предлагали, — чтобы не предложить второй раз."""
    user.reminder_offered_at = utcnow()
    await session.commit()


# Час напоминания по умолчанию — в тех же границах, что и час лесенки
# (`nudge_plan.EARLIEST_USUAL`/`LATEST_USUAL`): зашедший в 02:00 не должен
# получать напоминание в 02:00 каждую ночь, а свой час он выбирал не сам
DEFAULT_EARLIEST_HOUR = 10
DEFAULT_LATEST_HOUR = 20


def default_reminder_time(user: User, now_utc=None) -> str:
    """Час первого захода по поясу человека, «HH:00», в пределах 10–20."""
    zone = user.timezone or "Europe/Berlin"
    moment = (now_utc or utcnow()).replace(tzinfo=ZoneInfo("UTC"))
    try:
        hour = moment.astimezone(ZoneInfo(zone)).hour
    except Exception:
        logger.warning("неизвестный часовой пояс %r у пользователя %s", zone, user.id)
        hour = FALLBACK_HOUR_UTC
    hour = min(max(hour, DEFAULT_EARLIEST_HOUR), DEFAULT_LATEST_HOUR)
    return f"{hour:02d}:00"


def enable_by_default(user: User, now_utc=None) -> None:
    """
    Включить напоминания новичку при знакомстве — без вопроса (16.10).

    Решение владельца: «поставил бы базово на то время, как человек зашёл —
    хочет? меняет сам». Прежде бот спрашивал «Напоминать раз в день?» после
    первого урока; спрашивать включённое незачем. Выключить — одной кнопкой
    «Не напоминать» под любым сообщением или в настройках.

    Отметка `reminders_auto` — для контрольной группы: см. `nudges._deliver`.
    `reminder_offered_at` ставится, чтобы старая логика предложения (её
    кнопки ещё лежат в чатах) не сочла человека «не спрошенным».
    """
    user.notifications_enabled = True
    user.notification_time = default_reminder_time(user, now_utc)
    user.reminders_auto = True
    user.reminder_offered_at = now_utc or utcnow()


def mark_reminders_own(user: User) -> None:
    """Человек сам включил или настроил напоминания — отметка «по умолчанию» снимается."""
    user.reminders_auto = False
