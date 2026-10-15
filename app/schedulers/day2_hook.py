"""
Сообщение второго дня новичку — патч 2.1.

ЗАЧЕМ. 79% новичков не возвращаются на второй день (замер сентября; база
21%, цель 35–40%). У Duolingo первые семь дней — самые хрупкие: кто прошёл
неделю, остаётся. Новичок закончил первое занятие — и через сутки, в то же
время, когда он занимался, получает ОДНО личное сообщение с конкретным
числом: «Вчера Вы узнали 7 новых слов — проверим, что запомнилось? 2 минуты».
Кнопка сразу начинает занятие: вчерашние ошибки вернутся по сроку, а
верно отвеченные — отработкой другой игрой (по сроку они ждут три дня,
`FIRST_SIGHT_STREAK`).

КОМУ:
  * закончил первое занятие ВЧЕРА (его днём) и с тех пор не занимался;
  * сейчас — около того же времени дня, что вчера (окно 4 ч, начиная за
    2 ч до вчерашнего), но только днём, 09:00–22:00 по его поясу;
  * сообщение второго дня ещё не получал (`users.day2_hook_sent_at`) —
    одно на всю жизнь;
  * от напоминаний ЯВНО не отказывался (`reminders_declined_at`);
  * сегодня (его днём) напоминания ещё не получал и за последние 12 ч
    сообщений от бота не было.

ПОЧЕМУ НЕ ПРОСТО «22–26 Ч ПОСЛЕ». Аудит 2.1 (15.10): первое занятие в 00:30
давало «Вчера Вы…» в 22:30 того же дня; в 23:50 — сообщение в полночь, через
4 часа после обычного напоминания, которое «одно в день» не останавливало,
потому что день сменился.

ОДНО СООБЩЕНИЕ В ДЕНЬ. Отправка ставит и `last_notification_sent`: обычное
напоминание в тот же день уже не придёт (`reminder_is_due`).

Заблокировал бота — напоминания выключаются, как у обычного напоминания.
"""
from __future__ import annotations

import logging
from datetime import datetime, time, timedelta, timezone
from typing import Optional

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError, TelegramNetworkError, TelegramRetryAfter
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy import func, select, update

from app.core.clock import utcnow
from app.database.models import QuizSession, User, UserWord

logger = logging.getLogger(__name__)

# Окно: на следующий день около того же часа, когда человек уже однажды
# нашёл минуту, — от «за 2 ч до вчерашнего» на 4 ч вперёд
WINDOW_BEFORE = timedelta(hours=2)
WINDOW_LENGTH = timedelta(hours=4)
# Ночью не пишем: окно сдвигается в день, а после 22:00 закрывается
DAY_STARTS = time(9, 0)
DAY_ENDS = time(22, 0)
# Последнее окно открывается не позже 20:00 — чтобы до 22:00 было 2 ч
LATEST_START = time(20, 0)
# Между двумя сообщениями бота — не меньше 12 ч, через полночь тоже
MIN_GAP = timedelta(hours=12)


def window_start(user: User, first: datetime, today) -> Optional[datetime]:
    """
    Начало окна (наивное UTC) в день `today` человека: вчерашнее время конца
    первого занятия минус 2 ч, сдвинутое в 09:00–20:00 его пояса.
    """
    from app.services.streak_service import _zone

    zone = _zone(user)
    local_first = first.replace(tzinfo=timezone.utc).astimezone(zone)
    minutes = local_first.hour * 60 + local_first.minute - int(WINDOW_BEFORE.total_seconds() // 60)
    lowest = DAY_STARTS.hour * 60 + DAY_STARTS.minute
    highest = LATEST_START.hour * 60 + LATEST_START.minute
    minutes = min(max(minutes, lowest), highest)
    start_local = datetime.combine(today, time(minutes // 60, minutes % 60), tzinfo=zone)
    return start_local.astimezone(timezone.utc).replace(tzinfo=None)


def may_write(user: User, now: Optional[datetime] = None) -> bool:
    """
    Можно ли писать: сообщение ещё не уходило, человек ЯВНО не отказывался
    от напоминаний и сегодня (его днём) напоминания ещё не получал.

    Отказ — только явный (`reminders_declined_at`). Прежде отказом считалось
    «предложение было, а напоминания выключены», но предложение отмечается в
    момент отправки, и новичок, который просто ушёл, — ровно тот, кого мы
    возвращаем, — попадал в «отказавшиеся» (независимая проверка 2.1).
    """
    from app.services.streak_service import user_day

    if user.day2_hook_sent_at is not None:
        return False
    if getattr(user, "reminders_declined_at", None) is not None and not user.notifications_enabled:
        return False
    sent = user.last_notification_sent
    if now is not None and sent is not None:
        if user_day(user, sent) == user_day(user, now):
            return False
        # Через полночь «другой день» наступает и через 4 ч после
        # напоминания в 20:00 — считаем ещё и часы
        if now - sent < MIN_GAP:
            return False
    return True


# Новичок — немного занятий; ограничение заодно не даёт группировать всю
# таблицу занятий каждые десять минут
NEWCOMER_MAX_LESSONS = 5


async def due_users(session, now: datetime) -> list[tuple[User, datetime]]:
    """
    Кому пора: первое законченное занятие было вчера (по поясу человека),
    после того дня — ни одного, и сейчас его окно (см. `window_start`).
    Несколько занятий в первый день — всё равно «не вернулся». Возвращает
    (человек, конец ПОСЛЕДНЕГО занятия первого дня) — до него и считаются
    слова: прежде — «первое + 2 ч», и вечернее занятие того же дня в число
    не входило (аудит 2.1).
    """
    from app.services.monthly_leaderboard_service import scored_sessions_filter
    from app.services.streak_service import user_day

    candidates = (await session.execute(
        select(User).where(
            User.day2_hook_sent_at.is_(None),
            User.quizzes_passed.between(1, NEWCOMER_MAX_LESSONS),
        )
    )).scalars().all()
    if not candidates:
        return []
    by_id = {user.id: user for user in candidates}
    rows = (await session.execute(
        select(QuizSession.user_id, QuizSession.completed_at).where(
            QuizSession.user_id.in_(list(by_id)),
            QuizSession.is_completed.is_(True),
            QuizSession.completed_at.isnot(None),
            scored_sessions_filter(),
        )
    )).all()
    done: dict[int, list[datetime]] = {}
    for user_id, moment in rows:
        done.setdefault(user_id, []).append(moment)

    due = []
    for user_id, moments in done.items():
        user = by_id[user_id]
        first = min(moments)
        first_day = user_day(user, first)
        today = user_day(user, now)
        # Только назавтра: «Вчера Вы…» должно быть правдой
        if today != first_day + timedelta(days=1):
            continue
        if any(user_day(user, m) > first_day for m in moments):
            continue                         # вернулся сам
        start = window_start(user, first, today)
        if not (start <= now < start + WINDOW_LENGTH):
            continue
        local_now = user_local_time(user, now)
        if not (DAY_STARTS <= local_now < DAY_ENDS):
            continue
        if may_write(user, now):
            # Конец ПОСЛЕДНЕГО занятия первого дня — для подсчёта его слов
            last = max(m for m in moments if user_day(user, m) == first_day)
            due.append((user, last))
    return due


def user_local_time(user: User, moment: datetime) -> time:
    from app.services.streak_service import _zone

    return moment.replace(tzinfo=timezone.utc).astimezone(_zone(user)).time()


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
            # ЗАНЯТЬ ДО ОТПРАВКИ — условным UPDATE: два тика или два процесса
            # (на время выкатки) не отправят дважды. И одно сообщение в день:
            # отметку обычного напоминания сверяем с прочитанной — если оно
            # успело уйти между чтением и этой строкой, не занимаем (аудит
            # 2.1: напоминание и это сообщение в одну минуту давали два)
            previous = user.last_notification_sent
            claimed = (await session.execute(
                update(User)
                .where(User.id == user.id, User.day2_hook_sent_at.is_(None),
                       User.last_notification_sent.is_not_distinct_from(previous))
                .values(day2_hook_sent_at=now, last_notification_sent=now)
                .returning(User.id)
            )).scalar()
            await session.commit()
            if claimed is None:
                continue
            key = "day2_hook_words" if words > 0 else "day2_hook"
            try:
                await bot.send_message(
                    user.id, get_text(key, lang, count=words),
                    reply_markup=day2_keyboard(lang, lesson_length(user)),
                )
                sent += 1
            except TelegramForbiddenError:
                await session.execute(
                    update(User).where(User.id == user.id).values(notifications_enabled=False))
                await session.commit()
                logger.warning("сообщение второго дня: бот заблокирован (%s)", user.id)
            except (TelegramRetryAfter, TelegramNetworkError):
                # Сбой не про человека — отпускаем захват: следующий тик в
                # пределах окна повторит. Иначе он не получал бы ничего —
                # ни этого сообщения, ни (из-за отметки) обычного напоминания
                await session.execute(
                    update(User)
                    .where(User.id == user.id, User.day2_hook_sent_at == now)
                    .values(day2_hook_sent_at=None, last_notification_sent=previous))
                await session.commit()
                logger.warning("сообщение второго дня: сбой сети, повторим (%s)", user.id)
            except Exception:
                logger.exception("сообщение второго дня не ушло (%s)", user.id)
    if sent:
        logger.info("Сообщений второго дня отправлено: %d", sent)
    return sent
