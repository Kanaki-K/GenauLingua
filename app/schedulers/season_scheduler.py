"""
Планировщик сезонов рейтинга

Задачи:
1. 1 числа каждого месяца в 00:05 UTC:
   - Завершить предыдущий сезон (раздать награды, обновить lifetime)
   - Создать новый сезон

2. Каждый час — проверка что активный сезон соответствует текущему месяцу
   (страховка на случай если бот был выключен 1 числа)
"""

import logging
from datetime import date

from app.core.clock import utctoday

from app.database.session import AsyncSessionLocal
from app.services.monthly_leaderboard_service import (
    get_current_season,
    create_new_season,
    finalize_pending_seasons,
    finalize_season,
    notify_season_awards,
)

logger = logging.getLogger(__name__)


async def finalize_and_create_new_season(bot=None):
    """
    Завершить старый сезон + создать новый.
    Вызывается 1 числа каждого месяца.

    `bot` нужен, чтобы СООБЩИТЬ победителям. Прежде сезон закрывался молча:
    награды записаны, lifetime вырос — и ни один человек об этом не узнавал.
    Необязательный он потому, что страховочная часовая проверка зовёт эту
    же работу, и бот у неё тоже есть; а приёмки зовут без бота, им
    сообщать некому.
    """
    today = utctoday()
    logger.info(f"Проверка смены сезона: {today}")

    async with AsyncSessionLocal() as session:
        # 1. Получаем текущий активный сезон
        current_season = await get_current_season(session)

        if not current_season:
            # Нет активного сезона — просто создаём новый
            logger.info(f"Нет активного сезона, создаю {today.month}/{today.year}")
            await create_new_season(today.year, today.month, session)
            return

        # 2. Проверяем — сезон от текущего месяца или от прошлого?
        if current_season.year == today.year and current_season.month == today.month:
            # Сезон уже текущий — ничего делать не нужно
            logger.debug(f"Сезон {current_season.month}/{current_season.year} актуален")
            return

        # 3. Сезон от прошлого месяца — завершаем его!
        logger.info(f"Завершаю сезон {current_season.month}/{current_season.year} (id={current_season.id})")

        if not current_season.winners_finalized:
            try:
                await finalize_season(current_season.id, session)
                logger.info(
                    f"Сезон {current_season.month}/{current_season.year} "
                    f"завершён, награды розданы"
                )
                # СООБЩИТЬ ПОБЕДИТЕЛЯМ. Отдельным шагом и после commit:
                # награда уже записана, и неудачная отправка её не отменит
                # — непомеченная уйдёт при следующем прогоне.
                if bot is not None:
                    await notify_season_awards(bot, session)
            except Exception as e:
                logger.error(f"Ошибка завершения сезона: {e}")
                # Закрытие идёт одной транзакцией — откатываем её целиком.
                # Новый сезон всё равно создаём, чтобы круги шли в зачёт, а
                # незакрытый старый подберёт `finalize_pending_seasons` в
                # ближайшей часовой проверке
                await session.rollback()
        else:
            logger.info(f"ℹ Сезон {current_season.month}/{current_season.year} уже был завершён")

        # 4. Создаём новый сезон
        logger.info(f"Создаю новый сезон {today.month}/{today.year}")
        try:
            new_season = await create_new_season(today.year, today.month, session)
            logger.info(f"Новый сезон создан: {new_season.month}/{new_season.year} (id={new_season.id})")
        except Exception as e:
            logger.error(f"Ошибка создания нового сезона: {e}")


async def hourly_season_check(bot=None):
    """
    Страховочная проверка каждый час.
    Если бот был выключен 1 числа — подхватит смену сезона.
    """
    today = utctoday()

    async with AsyncSessionLocal() as session:
        current_season = await get_current_season(session)

        if not current_season:
            # Нет сезона — создаём
            logger.warning(f"Нет активного сезона! Создаю {today.month}/{today.year}")
            await create_new_season(today.year, today.month, session)
            return

        # Если сезон от прошлого месяца — запускаем полную процедуру
        if current_season.year != today.year or current_season.month != today.month:
            logger.warning(f"Активный сезон {current_season.month}/{current_season.year} устарел")
            await finalize_and_create_new_season(bot)
            return

        # ПРОШЕДШИЕ СЕЗОНЫ БЕЗ ИТОГОВ. Активный сезон уже текущий, а старый
        # не закрыт в двух случаях: закрытие упало и откатилось, или новый
        # сезон открыл круг, законченный в первые минуты месяца, раньше
        # планировщика. Прежде такой сезон оставался без наград навсегда:
        # проверка смотрела только на активный
        closed = await finalize_pending_seasons(session)
        if closed:
            # Без `return`: награды только что закрытого сезона извещаются
            # ниже, в этом же прогоне, а не через час
            logger.warning(f"Закрыто сезонов, оставшихся без итогов: {closed}")

    # ДОСЫЛКА ИЗВЕЩЕНИЙ — каждый час, а не только в момент закрытия.
    #
    # Прежде извещение звалось ровно один раз, внутри ветки «сезон ещё не
    # закрыт». Недоставленное (сбой сети, бот перезапускался) не повторялось
    # никогда: через час сезон уже новый, и почасовая проверка ничего не
    # делала. Замер подменённым планировщиком: 720 почасовых прогонов за
    # месяц — 1 вызов извещения. Выборка сама ограничена тремя сутками после
    # закрытия (`AWARD_NOTICE_WINDOW`), поэтому прогон дешёвый и старое не
    # досылает
    await send_pending_award_notices(bot)


async def send_pending_award_notices(bot) -> int:
    """Досылка извещений о наградах отдельной сессией: ошибка не валит проверку."""
    if bot is None:
        return 0
    try:
        async with AsyncSessionLocal() as session:
            return await notify_season_awards(bot, session)
    except Exception:
        logger.exception("досылка извещений о наградах не удалась")
        return 0