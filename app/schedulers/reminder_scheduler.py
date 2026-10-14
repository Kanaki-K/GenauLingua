"""
Планировщик напоминаний и сезонов для бота
"""
import logging
from datetime import datetime, timedelta
from app.core.clock import utcnow
from zoneinfo import ZoneInfo
from typing import List, Optional

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select

from app.bot.keyboards.notifications import get_reminder_keyboard
from app.database.models import User
from app.services.streak_service import current_streak, user_today
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

    new_next_round = await count_new_in_next_round(user, session, pair, due)

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
        # «Сегодня» — день ЧЕЛОВЕКА, тот же, по которому считается серия.
        # По UTC выходило, что занимавшийся в 19:00 в Нью-Йорке в 20:58
        # получал «5 дн. подряд · сегодня ещё нет»
        active_today=last == user_today(user),
        words_in_work=int(in_work or 0),
        learned=int(learned or 0),
        almost_learned=int(almost or 0),
        rank=int(rank["rank"]) if rank else 0,
        rank_field=int(rank["total_users"]) if rank else 0,
        rounds_total=int(user.quizzes_passed or 0),
        days_away=max(0, (user_today(user) - last).days) if last else 0,
        new_next_round=new_next_round,
    )


async def count_new_in_next_round(user: User, session, pair, due: int) -> int:
    """
    Сколько НОВЫХ слов принесёт ближайший круг — без запаса в обещании.

    ЗАЧЕМ. Повод «Слов в работе: 44 · до 50 ещё 6, это один круг» обещал
    рубеж за круг при любом составе. А новых в круге по правилу состава —
    три, если повторять есть что (`wants_new_word`: места 5, 10, 15 из
    пятнадцати); остальные места занимают просроченные и трудные. Замер
    14 октября: повод получали 72 человека, и у 12 из них «один круг» был
    невозможен по построению — например, 44 просроченных и 3 новых за круг
    при шести до рубежа.

    Места считаются ТОЙ ЖЕ функцией, что расставляет их в круге. Прочие места
    отдаются новым, только когда просроченных и трудных на них не хватает
    (порядок подбора: просроченное → трудное → новое). Трудные и просроченные
    частично совпадают, и сумма их завышает занятость — значит число новых
    занижено, а обещание даётся только наверняка.
    """
    from app.database.enums import QuizMode
    from app.services.quiz_service import (
        DEFAULT_ROUND_LENGTH, count_difficult_words, get_new_words, wants_new_word,
    )

    # Режим «сложные слова» новых не берёт вовсе
    if user.quiz_mode == QuizMode.DIFFICULT:
        return 0
    # Новые в выбранном уровне или теме кончились — рубеж кругом не взять
    if await get_new_words(user.id, session, pair, [], user=user) is None:
        return 0

    length = user.quiz_word_count or DEFAULT_ROUND_LENGTH
    new_slots = sum(1 for place in range(length) if wants_new_word(place, length))
    busy = due + await count_difficult_words(user.id, session, pair)
    return new_slots + max(0, (length - new_slots) - busy)


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


# Исход одной попытки. Три, а не «да/нет»: заблокировавший бота — не сбой
# сети, и обращаться с ним надо иначе (см. check_and_send_notifications)
SENT = "sent"
FORBIDDEN = "forbidden"
FAILED = "failed"

# Насколько поздно напоминание ещё догоняет. Прежде окно было ±2 минуты:
# перезапуск бота в 11:58–12:02 UTC оставлял без напоминания на весь день
# 117 человек из 121 включивших — у всех стоит 14:00 по Берлину. Три часа —
# догнать после перезапуска, но не прислать «дневное» напоминание ночью
CATCH_UP = timedelta(hours=3)

# Насколько РАНЬШЕ назначенного уходит напоминание: тик раз в минуту, и
# первый тик окна — за две минуты до срока
EARLY = timedelta(minutes=2)


async def send_notification_to_user(bot: Bot, user: User, session) -> str:
    """Отправить напоминание конкретному пользователю. Возвращает исход."""
    lang = user.interface_language or "ru"

    try:
        text = await build_reminder_text(user, session)
    except Exception:
        logger.exception("не удалось собрать текст напоминания (user=%s)", user.id)
        # Ошибка базы оставила бы транзакцию сессии сломанной, и все
        # следующие люди этого тика упали бы на ней же — сессия одна на тик
        await session.rollback()
        return FAILED

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
        logger.info(f"Напоминание отправлено пользователю {user.id} ({user.username})")
        return SENT
    except TelegramForbiddenError as e:
        logger.warning("напоминание: бот заблокирован (user=%s): %s", user.id, e)
        return FORBIDDEN
    except Exception as e:
        logger.error(f"Ошибка отправки напоминания пользователю {user.id}: {e}")
        return FAILED


def reminder_is_due(user: User, now_utc: datetime) -> bool:
    """
    Пора ли слать человеку напоминание в этот тик. Без базы и без сети.

    Пора, если: сегодня (по его поясу) день напоминаний, сегодня ещё не
    было ни отправки, ни попытки, и назначенное время наступило — не раньше
    чем за две минуты и не позже чем три часа назад.

    ПОЧЕМУ «НЕ ПОЗЖЕ ТРЁХ ЧАСОВ», А НЕ «±2 МИНУТЫ». Прежнее окно в пять
    тиков терялось целиком при перезапуске бота около срока, и человек
    оставался без напоминания на сутки. Двойной отправки окно не даёт: её
    держит отметка `last_notification_sent`, а не ширина окна.
    """
    if not user.timezone or not user.notification_time:
        return False
    try:
        user_tz = ZoneInfo(user.timezone)
    except Exception:
        logger.error(f"Неверный timezone для пользователя {user.id}: {user.timezone}")
        return False

    now_local = now_utc.replace(tzinfo=ZoneInfo("UTC")).astimezone(user_tz)

    if now_local.weekday() not in (user.notification_days or []):
        return False

    if user.last_notification_sent:
        last_local = user.last_notification_sent.replace(
            tzinfo=ZoneInfo("UTC")).astimezone(user_tz)
        if last_local.date() == now_local.date():
            return False

    try:
        hour_text, minute_text = user.notification_time.split(":")
        hour, minute = int(hour_text), int(minute_text)
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            return False
    except ValueError:
        return False

    scheduled = now_local.replace(hour=hour, minute=minute, second=0, microsecond=0)
    return scheduled - EARLY <= now_local <= scheduled + CATCH_UP


async def check_and_send_notifications(bot: Bot, now_utc: Optional[datetime] = None):
    """
    Проверить и отправить напоминания пользователям.

    ОДНА ПОПЫТКА В ДЕНЬ, чем бы она ни кончилась. Прежде неудача не
    отмечалась, и окно в пять тиков давало пять попыток в день — каждый
    день, вечно: заблокировавший бота получал их, пока база жива.

      доставлено      отметка дня
      заблокирован    напоминания выключаются: человек ответил ясно, и
                      спрашивать его каждый день — то же самое, что спам
      прочий сбой     отметка дня: завтра попытка будет, сегодня — нет
    """
    from app.database.session import AsyncSessionLocal

    now_utc = now_utc or utcnow()
    sent_count = 0

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.notifications_enabled == True)
        )
        users: List[User] = result.scalars().all()

        logger.debug(f"Найдено {len(users)} пользователей с включенными уведомлениями")

        # Сначала решается, КОМУ пора, — по уже загруженным полям, без
        # запросов. Потом каждый берётся заново через `session.get`: откат
        # после сбоя у одного человека делает просроченными ВСЕ объекты
        # сессии, и чтение поля у следующего в асинхронной сессии упало бы
        # (MissingGreenlet) — один сбой оставлял бы без напоминания весь тик
        due_ids = [user.id for user in users if reminder_is_due(user, now_utc)]

        for user_id in due_ids:
            try:
                user = await session.get(User, user_id)
                if user is None or not user.notifications_enabled:
                    continue

                logger.info(f"Отправляю напоминание пользователю {user_id}")
                outcome = await send_notification_to_user(bot, user, session)

                if outcome == FORBIDDEN:
                    user.notifications_enabled = False
                    logger.warning(
                        "напоминания выключены: пользователь %s заблокировал бота",
                        user_id,
                    )
                user.last_notification_sent = now_utc
                await session.commit()
                if outcome == SENT:
                    sent_count += 1

            except Exception as e:
                logger.error(f"Ошибка обработки пользователя {user_id}: {e}")
                await session.rollback()
                continue

    if sent_count > 0:
        logger.info(f"Отправлено {sent_count} напоминаний")


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
        args=[bot],
        id="finalize_season",
        replace_existing=True
    )

    # Каждый час — страховочная проверка (если бот был выключен 1 числа)
    scheduler.add_job(
        hourly_season_check,
        args=[bot],
        trigger="cron",
        minute=30,  # каждый час в :30
        id="hourly_season_check",
        replace_existing=True
    )

    scheduler.start()
    logger.info("Планировщик запущен: напоминания + сезоны рейтинга")

    return scheduler