"""
Планировщик: сообщения по инициативе бота и сезоны рейтинга.

С патча 2.1 все сообщения по инициативе бота — напоминания включившим,
лесенка возврата, приглашения не начавшим — шлёт ОДИН распорядитель,
`app/schedulers/nudges.py`. Прежние два отправителя (ежеминутные
напоминания и сообщение второго дня) удалены: аудит 2.1 поймал от них два
сообщения в одну минуту, а владелец забраковал сами тексты («Пора
позаниматься» + справка о боте — «это говно, а не напоминание»).
"""
import logging

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logger = logging.getLogger(__name__)


def setup_scheduler(bot: Bot) -> AsyncIOScheduler:
    """Настроить и запустить планировщик задач."""
    from app.schedulers.nudges import send_nudges
    from app.schedulers.season_scheduler import finalize_and_create_new_season, hourly_season_check

    scheduler = AsyncIOScheduler(timezone="UTC")

    # ═══════════════ СООБЩЕНИЯ ВОВЛЕЧЕНИЯ (патч 2.1) ═══════════════
    # Каждые 5 минут: окно у каждого вида — не меньше трёх часов, тик в пять
    # минут его не пропустит, а напоминание в час человека опоздает не больше
    # чем на пять минут
    scheduler.add_job(
        send_nudges,
        trigger="cron",
        minute="*/5",
        args=[bot],
        id="nudges",
        replace_existing=True,
    )

    # ═══════════════ СЕЗОНЫ РЕЙТИНГА ═══════════════
    # 1 числа каждого месяца в 00:05 UTC — завершение старого + создание нового
    scheduler.add_job(
        finalize_and_create_new_season,
        trigger="cron",
        day=1,
        hour=0,
        minute=5,
        args=[bot],
        id="finalize_season",
        replace_existing=True,
    )

    # Каждый час — страховочная проверка (если бот был выключен 1 числа)
    scheduler.add_job(
        hourly_season_check,
        args=[bot],
        trigger="cron",
        minute=30,
        id="hourly_season_check",
        replace_existing=True,
    )

    # ═══════════════ ВИСЯЩИЕ ЗАНЯТИЯ (2.2.1) ═══════════════
    # Раз в сутки, ночью по UTC: незаконченные без движения двое суток —
    # брошенные (`app/services/lesson_cleanup.py`). Людям не пишет ничего
    from app.services.lesson_cleanup import close_stale_lessons_job

    scheduler.add_job(
        close_stale_lessons_job,
        trigger="cron",
        hour=3,
        minute=15,
        id="close_stale_lessons",
        replace_existing=True,
    )

    scheduler.start()
    logger.info("Планировщик запущен: сообщения вовлечения + сезоны рейтинга")
    return scheduler
