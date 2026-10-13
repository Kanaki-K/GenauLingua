"""
Планировщик напоминаний и сезонов для бота
"""
import logging
from datetime import datetime
from app.core.clock import utcnow, utctoday
from zoneinfo import ZoneInfo
from typing import List

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select

from app.bot.keyboards.notifications import get_reminder_keyboard
from app.database.models import User
from app.services.streak_service import current_streak
from app.locales import get_text

logger = logging.getLogger(__name__)


# Шесть общих фраз («Шаг за шагом ты достигаешь результата!») отсюда
# ушли вместе с ключами из всех шести локалей. Они ничего не знали о
# человеке, а одна лгала по построению: фраза выбиралась только при
# ПУСТЫХ шкалах, то есть доставалась человеку без прогресса и без серии,
# и сообщала ему, что его серия растёт.
#
# Вместо них — измеренный повод вернуться, `app/services/reminder_reason.py`.


async def collect_reminder_facts(user: User, session, pair) -> "ReminderFacts":
    """
    Замерить то, из чего выбирается повод вернуться.

    Три запроса на человека, и один из них считает сразу три числа
    фильтрованными суммами: слова в работе, выученные и те, которым до
    «выучено» остался один верный ответ. Напоминания уходят всем 233
    людям в их час, и три отдельных запроса на каждого были бы расточением
    без нужды.
    """
    from sqlalchemy import case, func

    from app.database.models import UserWord
    from app.services.monthly_leaderboard_service import get_user_monthly_rank
    from app.services.quiz_service import MIN_ATTEMPTS_FOR_LEARNED, count_due_words
    from app.services.reminder_reason import ReminderFacts

    due = await count_due_words(user.id, session, pair, user=user)

    in_work, learned, almost = (await session.execute(
        select(
            func.count(),
            func.coalesce(func.sum(
                case((UserWord.learned.is_(True), 1), else_=0)
            ), 0),
            func.coalesce(func.sum(
                case((
                    (UserWord.learned.is_(False))
                    & (UserWord.correct_streak == MIN_ATTEMPTS_FOR_LEARNED - 1),
                    1,
                ), else_=0)
            ), 0),
        )
        .select_from(UserWord)
        .where(
            UserWord.user_id == user.id,
            UserWord.learning_lang == pair.learning,
            UserWord.times_shown > 0,
        )
    )).one()

    rank = await get_user_monthly_rank(
        user.id, session, learning_lang=pair.learning
    )

    last = getattr(user, "last_quiz_date", None)
    return ReminderFacts(
        due_words=due,
        # Серия — через `streak_service`: колонка пересчитывается только на
        # завершении круга, и у остановившегося в ней навсегда остаётся
        # последнее значение. Напоминание — худшее место, чтобы хвалить за
        # прерванную серию: человек открывает уведомление и видит «1 день
        # подряд» после восьми месяцев молчания
        streak_days=current_streak(user),
        best_streak=int(getattr(user, "best_streak_days", 0) or 0),
        active_today=last == utctoday(),
        words_in_work=int(in_work or 0),
        learned=int(learned or 0),
        almost_learned=int(almost or 0),
        rank=int(rank["rank"]) if rank else 0,
        rank_field=int(rank["total_users"]) if rank else 0,
        rounds_total=int(user.quizzes_passed or 0),
        days_away=max(0, (utctoday() - last).days) if last else 0,
    )


async def build_reminder_text(user: User, session) -> str:
    """
    Текст напоминания: три шкалы и ОДИН повод вернуться.

    Прежде здесь висело «Викторин пройдено: 12 · Слов изучено: 47 ·
    Точность: 88%» — четыре числа, из которых ни одно не говорит, ЧЕГО
    человеку не хватает. Три шкалы говорят: «написанное 107, на слух 12,
    вслух 0» — и разрыв между ними виден с первого взгляда.

    Блок шкал собирается той же функцией, что и на домашнем экране. Будь он
    написан здесь отдельно, два экрана об одном разошлись бы при первой
    правке, и разошёлся бы этот: напоминание человек видит, но не
    открывает, и расхождение заметили бы последним.

    ВТОРЫМ БЛОКОМ БЫЛА СЛУЧАЙНАЯ ФРАЗА ИЗ ШЕСТИ. «Шаг за шагом ты
    достигаешь результата», «Твоя серия растёт — продолжай в том же духе».
    Ни одна ничего не знала о человеке, а вторая ещё и лгала по
    построению: фраза выбиралась, только если шкалы ПУСТЫ, то есть
    доставалась человеку без прогресса и без серии. Бот сообщал о росте
    серии тому, у кого её нет.

    Теперь это измеренный повод — `reminder_reason`, тот же приём, что в
    поощрении за круг: факты, одно правило, один повод, и каждый обязан
    быть правдой на момент отправки.
    """
    from app.bot.handlers.quiz.home import _scope, scales_block
    from app.services.language_service import pair_from_user
    from app.services.quiz_service import get_channel_progress
    from app.services.reminder_reason import reason_line

    lang = user.interface_language or "ru"
    name = user.first_name or get_text("notif_default_name", lang)
    pair = pair_from_user(user)
    level, category = _scope(user)

    channels = await get_channel_progress(
        user.id, session, pair, level=level, category=category
    )

    text = get_text("notif_message_greeting", lang, name=name) + "\n\n"

    # Шкалы — только когда на них есть что смотреть: у новичка все три
    # полосы пусты, и встречать его тремя нулями незачем
    block = scales_block(channels, lang)
    if block:
        text += block + "\n\n"

    facts = await collect_reminder_facts(user, session, pair)
    text += reason_line(facts, lang)

    # ТЕКСТОВОГО ПРИЗЫВА НЕТ: им стала кнопка.
    #
    # Прежде последней строкой стояло «💪 Не прерывай свою серию!» — и
    # приходило оно в том числе людям, у которых серии нет ни одного дня.
    # Призывать не прерывать то, чего не было, — мелкая ложь, но ровно та
    # же по форме, что и прочие: текст говорит об одном поле, а смотреть
    # надо было в соседнее. Кнопка «▶️ Заниматься» зовёт честнее и не
    # зависит от состояния.
    return text.rstrip()


async def send_notification_to_user(bot: Bot, user: User, session) -> bool:
    """Отправить напоминание конкретному пользователю."""
    lang = user.interface_language or "ru"

    try:
        text = await build_reminder_text(user, session)
    except Exception:
        logger.exception("не удалось собрать текст напоминания (user=%s)", user.id)
        return False

    try:
        await bot.send_message(
            chat_id=user.id,
            text=text,
            parse_mode="HTML",
            # БЕЗ КЛАВИАТУРЫ ЭТО СООБЩЕНИЕ БЫЛО ТУПИКОМ. Текст звал
            # заниматься, нажать было нечего, и человек должен был сам
            # вспомнить про реплай-клавиатуру. См. get_reminder_keyboard.
            reply_markup=get_reminder_keyboard(lang, count=user.quiz_word_count or 15),
        )
        logger.info(f"✅ Напоминание отправлено пользователю {user.id} ({user.username})")
        return True
    except Exception as e:
        logger.error(f"❌ Ошибка отправки напоминания пользователю {user.id}: {e}")
        return False


async def check_and_send_notifications(bot: Bot):
    """
    Проверить и отправить напоминания пользователям
    """
    from app.database.session import AsyncSessionLocal

    now_utc = utcnow()
    sent_count = 0

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.notifications_enabled == True)
        )
        users: List[User] = result.scalars().all()

        logger.debug(f"🔍 Найдено {len(users)} пользователей с включенными уведомлениями")

        for user in users:
            try:
                if not user.timezone:
                    continue

                try:
                    user_tz = ZoneInfo(user.timezone)
                    now_local = now_utc.replace(tzinfo=ZoneInfo("UTC")).astimezone(user_tz)
                except Exception:
                    logger.error(f"❌ Неверный timezone для пользователя {user.id}: {user.timezone}")
                    continue

                current_weekday = now_local.weekday()
                if current_weekday not in user.notification_days:
                    continue

                if user.last_notification_sent:
                    last_sent_local = user.last_notification_sent.replace(tzinfo=ZoneInfo("UTC")).astimezone(user_tz)
                    if last_sent_local.date() == now_local.date():
                        continue

                try:
                    if ':' not in user.notification_time:
                        continue
                    time_parts = user.notification_time.split(':')
                    if len(time_parts) != 2:
                        continue
                    notification_hour = int(time_parts[0])
                    notification_minute = int(time_parts[1])
                    if not (0 <= notification_hour <= 23 and 0 <= notification_minute <= 59):
                        continue
                except (ValueError, IndexError):
                    continue

                notification_datetime = now_local.replace(
                    hour=notification_hour,
                    minute=notification_minute,
                    second=0,
                    microsecond=0
                )
                time_diff_minutes = abs((now_local - notification_datetime).total_seconds() / 60)

                if time_diff_minutes > 2:
                    continue

                logger.info(f"⏰ Отправляю напоминание пользователю {user.id}")

                success = await send_notification_to_user(bot, user, session)

                if success:
                    user.last_notification_sent = now_utc
                    await session.commit()
                    sent_count += 1

            except Exception as e:
                logger.error(f"❌ Ошибка обработки пользователя {user.id}: {e}")
                continue

    if sent_count > 0:
        logger.info(f"✅ Отправлено {sent_count} напоминаний")


def setup_scheduler(bot: Bot) -> AsyncIOScheduler:
    """
    Настроить и запустить планировщик задач
    """
    scheduler = AsyncIOScheduler(timezone="UTC")

    # ═══════════════ НАПОМИНАНИЯ ═══════════════
    # Каждую минуту — проверка и отправка напоминаний
    scheduler.add_job(
        check_and_send_notifications,
        trigger="cron",
        minute="*",
        args=[bot],
        id="check_notifications",
        replace_existing=True
    )

    # ═══════════════ СЕЗОНЫ РЕЙТИНГА ═══════════════
    from app.schedulers.season_scheduler import (
        finalize_and_create_new_season,
        hourly_season_check
    )

    # 1 числа каждого месяца в 00:05 UTC — завершение старого + создание нового
    scheduler.add_job(
        finalize_and_create_new_season,
        trigger="cron",
        day=1,
        hour=0,
        minute=5,
        id="finalize_season",
        replace_existing=True
    )

    # Каждый час — страховочная проверка (если бот был выключен 1 числа)
    scheduler.add_job(
        hourly_season_check,
        trigger="cron",
        minute=30,  # каждый час в :30
        id="hourly_season_check",
        replace_existing=True
    )

    scheduler.start()
    logger.info("⏰ Планировщик запущен: напоминания + сезоны рейтинга")

    return scheduler