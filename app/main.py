"""
Главный файл запуска бота GenauLingua
"""

import sys
from pathlib import Path

# Добавляем корневую папку проекта в sys.path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import asyncio
import time
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import ErrorEvent
from aiogram.fsm.storage.memory import SimpleEventIsolation

from app.bot.fsm_storage import make_storage
from app.bot.slow_log import install_slow_log

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
        logger.error("Нет подключения к базе: %s", location)
        logger.error("настройки читались из: %s", ENV_FILE)
        logger.error("причина: %s", exc)
        if "getaddrinfo" in str(exc) or "could not translate host name" in str(exc):
            logger.error(
                "   Имя хоста не резолвится. Для запуска не в докере нужен "
                "ENV_FILE=.env.local (база на localhost:5434), "
                "а не .env (там хост postgres из docker-сети)."
            )
        raise SystemExit(1)

    logger.info("База на связи: %s (настройки из %s)", location, ENV_FILE)


async def check_speech() -> None:
    """
    Есть ли чем судить произношение, если игра вслух кому-то включена.

    ЗАЧЕМ ОТДЕЛЬНАЯ ПРОВЕРКА. Отсутствие распознавателя выглядит СНАРУЖИ
    РОВНО КАК ШУМ В МИКРОФОНЕ, и это худший вид поломки. `check_pronunciation`
    ловит любое исключение и возвращает `failed`, а `failed` по правилам
    проекта — «не разобрал», то есть НЕ ошибка ученика: вопрос остаётся,
    человеку предлагают записать ещё раз. Значит без библиотеки он записывал
    бы голосовое, ждал и получал «не разобрал» — каждый раз, молча, без
    единой строки в журнале.

    Так и было: `faster-whisper` стоял только в `requirements-dev.txt` с
    комментарием «боту не нужно» — верным в тот день, когда игры вслух ещё
    не было. Боевой образ собирался без распознавателя. Пока речь имел один
    человек из 233, это и не всплыло бы; 13 октября её включили всем.

    Бот при этом НЕ ОСТАНАВЛИВАЕТСЯ: три других игры работают, и ронять их
    из-за четвёртой неправильно. Но в журнале остаётся ошибка, которую
    видно и в Sentry.
    """
    from sqlalchemy import func, select

    from app.database.enums import QuizChannel
    from app.database.models import User
    from app.database.session import AsyncSessionLocal

    async with AsyncSessionLocal() as session:
        with_speech = (await session.execute(
            select(func.count()).select_from(User)
            .where(User.quiz_channels.contains(QuizChannel.SPEECH.value))
        )).scalar() or 0

    if not with_speech:
        logger.info("Игра вслух никому не включена — распознаватель не нужен")
        return

    missing = []
    try:
        import faster_whisper  # noqa: F401
    except Exception as exc:
        missing.append(f"faster-whisper ({exc})")
    try:
        import av  # noqa: F401
        import numpy  # noqa: F401
    except Exception as exc:
        missing.append(f"av/numpy ({exc})")

    if missing:
        logger.error(
            "❌ Игра вслух включена у %d человек, а судить произношение НЕЧЕМ: "
            "не хватает %s", with_speech, "; ".join(missing)
        )
        logger.error(
            "   Снаружи это выглядит как «не разобрал» на каждое голосовое — "
            "то есть как шум в микрофоне, а не как сбой. Поставить: "
            "pip install -r requirements.txt"
        )
        return

    logger.info("Игра вслух включена у %d человек, распознаватель на месте",
                with_speech)


async def main():
    setup_logging()
    setup_sentry()

    logger.info("Starting GenauLingua Bot...")

    await check_database()
    await check_speech()

    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    # Занятие — в Redis, если он задан: выкатка не обрывает уроки
    # Нажатия одного человека — по очереди (SimpleEventIsolation): в Redis
    # между чтением и записью состояния есть настоящее ожидание, и два
    # быстрых нажатия по сетке «Собираю» могли бы потерять одно обновление
    dp = Dispatcher(storage=make_storage(settings.REDIS_URL),
                    events_isolation=SimpleEventIsolation())
    logger.info("Хранилище занятий: %s", type(dp.storage).__name__)

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

    # Медленные нажатия — в журнал с видом действия (патч 2.1, `slow_log`)
    install_slow_log(dp)

    @dp.update.middleware()
    async def db_session_middleware(handler, event, data):
        async with AsyncSessionLocal() as session:
            data["session"] = session
            try:
                return await handler(event, data)
            except Exception:
                await session.rollback()
                raise

    # Журнал пути человека (патч 2.1) — после сессии: пишет в неё же
    from app.services.journal import install_journal

    install_journal(dp)

    # Список в логе ТОЖЕ собирается из источника, а не выписан рядом.
    # Выписанный отставал: в нём не было ни домашнего экрана, ни
    # доски — четвёртый список об одном и том же.
    logger.info("Роутеров подключено: %d", len(all_routers()))
    for router in all_routers():
        logger.info("   %s", router.name or type(router).__name__)

    scheduler = setup_scheduler(bot)
    logger.info("Планировщик запущен, работ: %d", len(scheduler.get_jobs()))

    # Модель распознавания речи — в память СРАЗУ, в фоне. Прежде она
    # грузилась при первом голосовом ответе после каждого перезапуска, и
    # этот человек ждал загрузку сверх распознавания (прод 15.10: 3 с).
    # Владелец: «проверки голосовых ответов достаточно долгие»
    from app.services.speech_check import _get_model

    preload = asyncio.create_task(_get_model())
    preload.add_done_callback(
        lambda t: t.cancelled() or t.exception() is None
        or logger.warning("модель распознавания не загружена заранее: %s", t.exception())
    )

    dp.shutdown.register(waiter_for(dp))
    await dp.start_polling(bot)


SHUTDOWN_WAIT_SECONDS = 25


def waiter_for(dispatcher: Dispatcher):
    """Обработчик `shutdown` для этого диспетчера (aiogram не передаёт его сам)."""
    async def wait_in_flight() -> None:
        await _wait_in_flight(dispatcher)
    return wait_in_flight


async def _wait_in_flight(dispatcher: Dispatcher) -> None:
    """
    ДОЖДАТЬСЯ НАЧАТЫХ ОТВЕТОВ при остановке (выкатка).

    Остановка прекращает опрос, а обработчики в пути отменялись вместе с
    циклом. С 2.1 их отметки живут в Redis, и оборванный посреди
    распознавания ответ запирал вопрос (аудит 2.1). Ждём здесь — в
    `shutdown`, — потому что после него aiogram закрывает соединение с
    Telegram, и дождавшиеся обработчики уже не смогли бы ответить. До 25 с:
    голосовой ответ на проде шёл до 21,5 с.
    """
    in_flight = {task for task in getattr(dispatcher, "_handle_update_tasks", ())
                 if task is not asyncio.current_task()}
    if in_flight:
        logger.info("Остановка: жду начатых ответов: %d", len(in_flight))
        await asyncio.wait(in_flight, timeout=SHUTDOWN_WAIT_SECONDS)

if __name__ == "__main__":
    asyncio.run(main())