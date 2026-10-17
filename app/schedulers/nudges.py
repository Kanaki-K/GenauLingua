"""
Распорядитель сообщений по инициативе бота — патч 2.1 «Вовлечение».

ОДИН ОТПРАВИТЕЛЬ ВМЕСТО ДВУХ. Прежде писали напоминания (каждую минуту,
кто включил) и сообщение второго дня (новичкам) — и аудит 2.1 поймал два
сообщения в одну минуту. Здесь решает одно правило (`nudge_plan.decide`),
текст собирается одним сборщиком (`nudge_texts.compose`), и каждое
решение пишется в журнал (`NudgeLog`).

ПОРЯДОК НА ЧЕЛОВЕКА:
  1. состояние из уже загруженных полей — без запросов;
  2. решение; контрольная группа (~10%) получает запись `holdout` вместо
     сообщения — кроме включивших напоминания: они их просили;
  3. ЗАХВАТ условным UPDATE до отправки: отметки сверяются с прочитанными,
     и второй процесс (выкатка) или второй тик не отправят повторно;
  4. отправка; сетевой сбой отпускает захват — следующий тик повторит.

Заблокировавший бота — явный отказ: больше не пишем, пока он сам не
включит напоминания.
"""
from __future__ import annotations

import logging
from datetime import date, datetime, time, timedelta, timezone
from typing import Optional

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError, TelegramNetworkError, TelegramRetryAfter
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy import case, func, select, update

from app.core.clock import utcnow
from app.database.models import NudgeLog, QuizSession, User, UserWord
from app.services import nudge_plan
from app.services.nudge_plan import DAILY, NudgeState

logger = logging.getLogger(__name__)

# Кнопка «⏰ Напоминать в это время» — в первых письмах тому, кто
# напоминаний не включал: с ними люди занимаются в 4.3 раза больше дней
OPTIN_KINDS = ("back1", "back3", "start1", "start3")


def _zone(user):
    from app.services.streak_service import _zone as zone

    return zone(user)


def _local(user, moment: Optional[datetime]) -> Optional[datetime]:
    if moment is None:
        return None
    return moment.replace(tzinfo=timezone.utc).astimezone(_zone(user)).replace(tzinfo=None)


def _parse_time(text: Optional[str]) -> Optional[time]:
    try:
        hour, minute = (int(part) for part in (text or "").split(":"))
        return time(hour, minute)
    except (ValueError, TypeError):
        return None


def build_state(user: User, now: datetime, last_done: Optional[datetime]) -> Optional[NudgeState]:
    """Состояние человека для `decide`. `last_done` — конец последнего занятия (UTC)."""
    from app.services.streak_service import user_day

    played = bool(user.quizzes_passed) and user.last_active_date is not None
    if played:
        anchor = user.last_active_date
        usual = _local(user, last_done).time() if last_done else None
    else:
        if user.created_at is None:
            return None
        anchor = user_day(user, user.created_at)
        usual = _local(user, user.created_at).time()
    declined = (getattr(user, "reminders_declined_at", None) is not None
                and not user.notifications_enabled)
    return NudgeState(
        now_local=_local(user, now),
        played=played,
        anchor_day=anchor,
        opted_in=bool(user.notifications_enabled),
        declined=declined,
        own_time=_parse_time(user.notification_time) if user.notifications_enabled else None,
        own_days=tuple(user.notification_days or (0, 1, 2, 3, 4, 5, 6)),
        usual_time=usual,
        sent_step_for_anchor=(user.nudge_step or 0) if user.nudge_anchor == anchor else 0,
        last_sent_local=_local(user, user.last_notification_sent),
    )


async def _last_done(session, user_ids) -> dict[int, datetime]:
    if not user_ids:
        return {}
    rows = (await session.execute(
        select(QuizSession.user_id, func.max(QuizSession.completed_at))
        .where(QuizSession.user_id.in_(list(user_ids)), QuizSession.is_completed.is_(True))
        .group_by(QuizSession.user_id)
    )).all()
    return {user_id: moment for user_id, moment in rows if moment}


async def gather_facts(session, user: User, kind: str, now: datetime):
    """Числа и слово человека для текста."""
    from app.locales import get_text
    from app.services.language_service import display_text, flag, main_meaning, pair_from_user
    from app.services.nudge_texts import NudgeFacts
    from app.services.quiz_service import count_due_words, get_due_words, get_new_words, lesson_length
    from app.services.streak_service import current_streak, user_day

    pair = pair_from_user(user)
    lang = user.interface_language or "ru"
    name = user.first_name or get_text("notif_default_name", lang)

    in_work, known, learned = (await session.execute(
        select(
            func.count(),
            func.coalesce(func.sum(case((UserWord.times_correct > 0, 1), else_=0)), 0),
            func.coalesce(func.sum(case((UserWord.learned.is_(True), 1), else_=0)), 0),
        ).select_from(UserWord).where(
            UserWord.user_id == user.id, UserWord.learning_lang == pair.learning,
            UserWord.times_shown > 0,
        )
    )).one()

    played = kind == DAILY or kind.startswith("back")
    word = None
    if played:
        word = await get_due_words(user.id, session, pair, [], user=user)
        if word is None:
            from app.database.models import Word

            word = (await session.execute(
                select(Word).join(UserWord, UserWord.word_id == Word.id).where(
                    UserWord.user_id == user.id, UserWord.learning_lang == pair.learning,
                    UserWord.times_shown > 0,
                ).order_by(UserWord.last_seen_at.desc().nullslast()).limit(1)
            )).scalars().first()
    else:
        word = await get_new_words(user.id, session, pair, [], user=user)
    teaser = None
    if word is not None:
        shown, meaning = display_text(word, pair.learning), main_meaning(word, pair.native)
        if shown and meaning:
            teaser = (shown, meaning)

    # Самый первый день: все законченные занятия — в один день
    first_day, first_day_words = False, 0
    if played and user.last_active_date is not None:
        days = (await session.execute(
            select(QuizSession.local_day, QuizSession.completed_at).where(
                QuizSession.user_id == user.id, QuizSession.is_completed.is_(True))
        )).all()
        distinct = {day or user_day(user, done) for day, done in days if done}
        if len(distinct) == 1:
            first_day = True
            first_day_words = int(in_work)

    away = 1
    if user.last_active_date is not None:
        away = (_local(user, now).date() - user.last_active_date).days

    return NudgeFacts(
        name=name, flag=flag(pair.learning), away=away,
        streak=current_streak(user) if played else 0,
        in_work=int(in_work), known=int(known), learned=int(learned),
        due=await count_due_words(user.id, session, pair, user=user) if played else 0,
        lessons=int(user.quizzes_passed or 0),
        best=int(user.best_streak_days or 0),
        first_day=first_day, first_day_words=first_day_words,
        word=teaser, questions=lesson_length(user),
    )


def keyboard(lang: str, kind: str, opted_in: bool, local_now: datetime,
             change_time: bool = False) -> InlineKeyboardMarkup:
    from app.locales import get_text

    rows = [[InlineKeyboardButton(text=get_text("home_btn_learn", lang),
                                  callback_data=f"learn_now:nd_{kind}")]]
    if not opted_in and kind in OPTIN_KINDS:
        at = f"{local_now.hour:02d}:00"
        rows.append([InlineKeyboardButton(text=get_text("nd_btn_optin", lang, time=at),
                                          callback_data=f"nd_optin:{at}")])
    if change_time:
        rows.append([InlineKeyboardButton(text=get_text("nd_btn_change_time", lang),
                                          callback_data="notif_change_time")])
    if not nudge_plan.is_last(kind):
        rows.append([InlineKeyboardButton(text=get_text("nd_btn_stop", lang),
                                          callback_data="notif_off")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


async def _sent_before(session, user_id: int) -> int:
    return int((await session.execute(
        select(func.count()).select_from(NudgeLog).where(
            NudgeLog.user_id == user_id, NudgeLog.outcome == "sent")
    )).scalar() or 0)


async def send_nudges(bot: Bot, now_utc: Optional[datetime] = None) -> dict[str, int]:
    """Один тик. Возвращает счёт исходов — для журнала и тестов."""
    from app.database.session import AsyncSessionLocal
    from app.services.nudge_texts import compose, situation

    now = now_utc or utcnow()
    counts: dict[str, int] = {}
    async with AsyncSessionLocal() as session:
        users = (await session.execute(select(User))).scalars().all()
        done = await _last_done(session, [u.id for u in users])
        states = {}
        for user in users:
            state = build_state(user, now, done.get(user.id))
            if state is not None:
                states[user.id] = state

        # СОРЕВНОВАНИЕ — ВМЕСТО обычного сообщения дня, а не вдобавок к нему
        # (17.10): у кого есть «Вас обогнали» или финишная прямая, тому в этот
        # тик напоминание не планируется, а бюджет общий (`may_send`)
        from app.schedulers import competition

        try:
            race = await competition.plan(session, users, states, now)
        except Exception:
            logger.exception("план сообщений соревнования не собран")
            await session.rollback()
            race = {}
        by_id = {u.id: u for u in users}
        for user_id, (kind, data) in race.items():
            try:
                outcome = await competition.deliver(bot, session, by_id[user_id],
                                                    states[user_id], kind, data, now)
            except Exception:
                logger.exception("сообщение %s не обработано (%s)", kind, user_id)
                await session.rollback()
                outcome = "error"
            if outcome:
                counts[outcome] = counts.get(outcome, 0) + 1

        plans = []
        for user in users:
            state = states.get(user.id)
            if state is None or user.id in race:
                continue
            decision = nudge_plan.decide(state)
            if decision:
                # Отметки, по которым решено, — для захвата: см. _deliver
                seen = (user.last_notification_sent, user.nudge_anchor, user.nudge_step or 0)
                plans.append((user.id, state, decision, seen))

        for user_id, state, (kind, step), seen in plans:
            try:
                outcome = await _deliver(bot, session, user_id, state, kind, step, now,
                                         compose, situation, seen)
            except Exception:
                logger.exception("сообщение %s не обработано (%s)", kind, user_id)
                await session.rollback()
                outcome = "error"
            if outcome:
                counts[outcome] = counts.get(outcome, 0) + 1
    if counts:
        logger.info("Сообщения вовлечения: %s", counts)
    return counts


async def _deliver(bot, session, user_id, state, kind, step, now, compose, situation,
                   seen) -> Optional[str]:
    user = await session.get(User, user_id, populate_existing=True)
    if user is None:
        return None
    # Контрольная группа: у не включавших — кроме ежедневного (его нет), у
    # включённых БОТОМ (`reminders_auto`, 16.10) — всё: иначе с напоминаниями
    # по умолчанию сравнивать стало бы не с кем. Кто включил сам, получает всегда
    holdout = nudge_plan.in_holdout(user_id) and (
        (kind != DAILY and not user.notifications_enabled)
        or bool(getattr(user, "reminders_auto", False))
    )

    # ЗАХВАТ: отметки сверяются с теми, по которым РЕШЕНО писать, — кто
    # успел раньше, тот и пишет. Не с перечитанными: полный прогон 16.10
    # поймал второй процесс, решивший до коммита первого, а перечитавший
    # после, — его условие совпало с новыми отметками, и ушло два сообщения
    previous_sent, previous_anchor, previous_step = seen
    values = {}
    # Ежедневное в контрольной группе тоже отмечается отправленным: у него
    # нет ступени, и без отметки его «удерживали» бы каждые 5 минут окна
    if not holdout or kind == DAILY:
        values["last_notification_sent"] = now
    if kind != DAILY:
        values.update(nudge_anchor=state.anchor_day, nudge_step=step)
    claimed = (await session.execute(
        update(User).where(
            User.id == user_id,
            User.last_notification_sent.is_not_distinct_from(previous_sent),
            User.nudge_anchor.is_not_distinct_from(previous_anchor),
            User.nudge_step == previous_step,
        ).values(**values).returning(User.id)
    )).scalar()
    await session.commit()
    if claimed is None:
        return None

    lang = user.interface_language or "ru"
    facts = await gather_facts(session, user, kind, now)
    sit = situation(kind, facts)
    if holdout:
        session.add(NudgeLog(user_id=user_id, kind=kind, situation=sit, outcome="holdout", sent_at=now))
        await session.commit()
        return "holdout"

    sent_before = await _sent_before(session, user_id)
    text = compose(kind, facts, lang, seed=user_id % 97 + sent_before)
    # Напоминания включил бот, а не человек: в ПЕРВОМ сообщении сказать, на
    # какой час, и дать сменить его одним нажатием (16.10)
    first_auto = bool(getattr(user, "reminders_auto", False)) and sent_before == 0
    if first_auto:
        from app.locales import get_text

        text += "\n\n<i>" + get_text("nd_auto_time", lang, time=user.notification_time) + "</i>"
    try:
        await bot.send_message(user_id, text, parse_mode="HTML",
                               reply_markup=keyboard(lang, kind, state.opted_in, state.now_local,
                                                     change_time=first_auto))
        outcome = "sent"
    except TelegramForbiddenError:
        # Заблокировал — это ответ: больше не пишем
        await session.execute(update(User).where(User.id == user_id).values(
            notifications_enabled=False, reminders_declined_at=now))
        outcome = "forbidden"
    except (TelegramRetryAfter, TelegramNetworkError):
        # Сбой не про человека — отпускаем захват, следующий тик повторит
        await session.execute(update(User).where(
            User.id == user_id, User.last_notification_sent.is_not_distinct_from(values.get("last_notification_sent", previous_sent)),
        ).values(last_notification_sent=previous_sent, nudge_anchor=previous_anchor,
                 nudge_step=previous_step))
        await session.commit()
        logger.warning("сообщение %s: сбой сети, повторим (%s)", kind, user_id)
        return "retry"
    except Exception:
        logger.exception("сообщение %s не ушло (%s)", kind, user_id)
        outcome = "failed"
    session.add(NudgeLog(user_id=user_id, kind=kind, situation=sit, outcome=outcome, sent_at=now))
    await session.commit()
    return outcome


async def preview(session, user: User, kind: str, now: Optional[datetime] = None, seed: int = 0):
    """Текст и клавиатура, которые получил бы человек, — без отправки (обход экранов, тесты)."""
    from app.services.nudge_texts import compose

    now = now or utcnow()
    facts = await gather_facts(session, user, kind, now)
    lang = user.interface_language or "ru"
    return (compose(kind, facts, lang, seed),
            keyboard(lang, kind, bool(user.notifications_enabled), _local(user, now)))
