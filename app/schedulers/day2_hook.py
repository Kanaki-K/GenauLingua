"""
Сообщение второго дня новичку — патч 2.1.

ЗАЧЕМ. 79% новичков не возвращаются на второй день (замер сентября; база
21%, цель 35–40%). У Duolingo первые семь дней — самые хрупкие: кто прошёл
неделю, остаётся. Новичок закончил первое занятие — и через сутки, в то же
время, когда он занимался, получает ОДНО личное сообщение с конкретным
числом: «Вчера Вы узнали 7 новых слов — проверим, что запомнилось? 2 минуты».
Кнопка сразу начинает занятие — в нём как раз и вернутся вчерашние слова.

КОМУ:
  * закончил первое занятие 22–26 часов назад и с тех пор не занимался;
  * сообщение второго дня ещё не получал (`users.day2_hook_sent_at`) —
    одно на всю жизнь;
  * от напоминаний НЕ отказался: предложение было, а он их не включил —
    значит, не хочет, и писать ему нельзя. Не предлагали или включены —
    можно.

ОДНО СООБЩЕНИЕ В ДЕНЬ. Отправка ставит и `last_notification_sent`: обычное
напоминание в тот же день уже не придёт (`reminder_is_due`).

Заблокировал бота — напоминания выключаются, как у обычного напоминания.
"""
from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Optional

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy import func, select

from app.core.clock import utcnow
from app.database.models import QuizSession, User, UserWord

logger = logging.getLogger(__name__)

# Окно: сутки ± пара часов от конца первого занятия — в то время, когда
# человек уже однажды нашёл минуту
WINDOW_FROM = timedelta(hours=22)
WINDOW_TO = timedelta(hours=26)


def may_write(user: User) -> bool:
    """Можно ли писать: не отказался от напоминаний и сообщение ещё не уходило."""
    if user.day2_hook_sent_at is not None:
        return False
    declined = user.reminder_offered_at is not None and not user.notifications_enabled
    return not declined


async def due_users(session, now: datetime) -> list[tuple[User, datetime]]:
    """
    Кому пора: первое законченное занятие было 22–26 ч назад, после него —
    ни одного. Возвращает (человек, конец первого занятия).
    """
    finished = (
        select(
            QuizSession.user_id,
            func.min(QuizSession.completed_at).label("first"),
            func.max(QuizSession.completed_at).label("last"),
        )
        .where(QuizSession.is_completed.is_(True), QuizSession.completed_at.isnot(None))
        .group_by(QuizSession.user_id)
        .subquery()
    )
    rows = (await session.execute(
        select(User, finished.c.first)
        .join(finished, finished.c.user_id == User.id)
        .where(
            finished.c.first.between(now - WINDOW_TO, now - WINDOW_FROM),
            # Вернулся сам — писать незачем. Несколько занятий в первый
            # день — всё равно «не вернулся»: последнее тоже в окне
            finished.c.last <= now - WINDOW_FROM + timedelta(hours=2),
            User.day2_hook_sent_at.is_(None),
        )
    )).all()
    return [(user, first) for user, first in rows if may_write(user)]


async def words_of_first_day(session, user: User, first_done: datetime) -> int:
    """Сколько слов человек впервые встретил в первый день (по изучаемому языку)."""
    return int((await session.execute(
        select(func.count()).select_from(UserWord).where(
            UserWord.user_id == user.id,
            UserWord.learning_lang == user.learning_lang,
            UserWord.created_at <= first_done + timedelta(hours=2),
        )
    )).scalar() or 0)


def day2_keyboard(lang: str, count: int) -> InlineKeyboardMarkup:
    from app.locales import get_text

    return InlineKeyboardMarkup(inline_keyboard=[
        # Пометка «:day2» — чтобы возврат по этому сообщению было чем измерить
        [InlineKeyboardButton(text=get_text("home_btn_learn", lang, count=count),
                              callback_data="learn_now:day2")],
        [InlineKeyboardButton(text=get_text("notif_message_btn_disable", lang),
                              callback_data="notif_off")],
    ])


async def send_day2_hooks(bot: Bot, now_utc: Optional[datetime] = None) -> int:
    """Отправить сообщения второго дня тем, кому пора. Возвращает число доставленных."""
    from app.database.session import AsyncSessionLocal
    from app.locales import DEFAULT_LOCALE, get_text
    from app.services.quiz_service import lesson_length

    now = now_utc or utcnow()
    sent = 0
    async with AsyncSessionLocal() as session:
        for user, first_done in await due_users(session, now):
            lang = user.interface_language or DEFAULT_LOCALE
            words = await words_of_first_day(session, user, first_done)
            key = "day2_hook_words" if words > 0 else "day2_hook"
            try:
                await bot.send_message(
                    user.id, get_text(key, lang, count=words),
                    reply_markup=day2_keyboard(lang, lesson_length(user)),
                )
                sent += 1
            except TelegramForbiddenError:
                user.notifications_enabled = False
                logger.warning("сообщение второго дня: бот заблокирован (%s)", user.id)
            except Exception:
                logger.exception("сообщение второго дня не ушло (%s)", user.id)
            # Одна попытка на жизнь, чем бы ни кончилась; и одно сообщение в день
            user.day2_hook_sent_at = now
            user.last_notification_sent = now
            await session.commit()
    if sent:
        logger.info("Сообщений второго дня отправлено: %d", sent)
    return sent
