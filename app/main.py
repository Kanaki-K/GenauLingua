"""
Главный файл запуска бота GenauLingua
"""

import sys
from pathlib import Path

# Добавляем корневую папку проекта в sys.path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import ErrorEvent
from aiogram.fsm.storage.memory import MemoryStorage

from app.bot.routers import all_routers, attach_routers
from app.config import settings

from app.database.session import AsyncSessionLocal
from app.core.logging import setup_logging
from app.core.sentry import setup_sentry
from app.schedulers import setup_scheduler

logger = logging.getLogger(__name__)


async def check_database() -> None:
    """
    Убедиться, что база достижима, ДО начала опроса Telegram.

    Иначе бот стартует нормально, а первое же нажатие кнопки падает
    стострочной трассировкой внутри обработчика. Самая частая причина —
    запуск с .env, где DATABASE_URL указывает на хост `postgres` из
    docker-сети: с машины разработчика это имя не резолвится.
    """
    from sqlalchemy import text

    from app.config import ENV_FILE
    from app.database.session import engine

    # Показываем хост, но не логин с паролем
    dsn = settings.DATABASE_URL
    location = dsn.split("@")[-1] if "@" in dsn else dsn

    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception as exc:
        logger.error("❌ Нет подключения к базе: %s", location)
        logger.error("   настройки читались из: %s", ENV_FILE)
        logger.error("   причина: %s", exc)
        if "getaddrinfo" in str(exc) or "could not translate host name" in str(exc):
            logger.error(
                "   Имя хоста не резолвится. Для запуска не в докере нужен "
                "ENV_FILE=.env.local (база на localhost:5434), "
                "а не .env (там хост postgres из docker-сети)."
            )
        raise SystemExit(1)

    logger.info("🗄️  База на связи: %s (настройки из %s)", location, ENV_FILE)


async def main():
    setup_logging()
    setup_sentry()

    logger.info("🚀 Starting GenauLingua Bot...")

    await check_database()

    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher(storage=MemoryStorage())

    @dp.errors()
    async def global_error_handler(event: ErrorEvent):
        logger.exception("Unhandled error: %s", event.exception)
        return True

    # ПОРЯДОК РЕГИСТРАЦИИ ЖИВЁТ В ОДНОМ МЕСТЕ — `app.bot.routers`.
    #
    # Прежде он был выписан здесь, в приёмке меню и в сценарных
    # тестах, то есть трижды. Три списка об одном расходятся всегда, и
    # разошлись: четвёртая игра попала только сюда, а приёмка объявила
    # её кнопку мёртвой — обработчик есть, просто не в её копии списка.
    attach_routers(dp)

    @dp.update.middleware()
    async def db_session_middleware(handler, event, data):
        async with AsyncSessionLocal() as session:
            data["session"] = session
            try:
                return await handler(event, data)
            except Exception:
                await session.rollback()
                raise

    # Список в логе ТОЖЕ собирается из источника, а не выписан рядом.
    # Выписанный отставал: в нём не было ни домашнего экрана, ни
    # доски — четвёртый список об одном и том же.
    logger.info("📦 Роутеров подключено: %d", len(all_routers()))
    for router in all_routers():
        logger.info("   ✅ %s", router.name or type(router).__name__)

    scheduler = setup_scheduler(bot)
    logger.info("⏰ Планировщик запущен, работ: %d", len(scheduler.get_jobs()))

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())