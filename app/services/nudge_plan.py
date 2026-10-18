"""
Кому, когда и что написать — одно правило на все сообщения по инициативе
бота (патч 2.1 «Вовлечение»).

ЗАЧЕМ ОДНО. До 2.1 писали двое: напоминания (каждый день, кто включил) и
сообщение второго дня (новичкам). Аудит показал цену двух независимых
отправителей: в одну минуту человек получал два сообщения. И главное —
решение владельца 15.10: вовлечение для ВСЕХ, а не для новичков, и «нельзя
заебать напоминаниями: уместно, ненавязчиво, с интересом и с пользой».
79% тех, кто вообще занимался, ни разу не занимались два дня подряд.

КТО ЧТО ПОЛУЧАЕТ (`decide`):

  ни разу не занимался   приглашение: через 1, 3 и 7 дней после /start,
                         третье — последнее
  включил напоминания    в его час — в дни без занятий, пока перерыв не
                         больше 2 дней; дальше — только на 3, 7 и 14 день
                         перерыва, потом пауза до возвращения
  не включал             лесенка возврата: 1, 3, 7 и 14 день перерыва, в
                         час его обычных занятий; 14-й — последний

ЧТО ОБЩЕЕ (`may_send`): не больше одного сообщения в день человека, не
чаще раза в 12 ч, без явного отказа («Не присылать», выключил в
настройках). Ночью не пишем — кроме часа, который человек выбрал сам.

ПОЧЕМУ ЛЕСЕНКА ОБРЫВАЕТСЯ. Напоминание, на которое неделями не отвечают,
не возвращает, а учит отписываться (исследование приложения на 12 тыс.
учащихся: частые уведомления дают обратный эффект). Последнее письмо так и
говорит: «больше не побеспокою, пока не вернётесь».
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from typing import Optional

# Дни перерыва, на которые приходит письмо. Последний — прощальный
LADDER = (1, 3, 7, 14)
START_LADDER = (1, 3, 7)
# Включившему напоминания — каждый день, пока перерыв не длиннее этого
DAILY_WHILE_AWAY = 2

MIN_GAP = timedelta(hours=12)
DAY_STARTS = time(9, 0)
DAY_ENDS = time(22, 0)
# Окно «обычного часа» — с часа до него на три вперёд, сдвинутое в 10–20
WINDOW_BEFORE = timedelta(hours=1)
WINDOW_LENGTH = timedelta(hours=3)
EARLIEST_USUAL = time(10, 0)
LATEST_USUAL = time(20, 0)
# Своё время человека — окно 3 ч (перезапуск бота не теряет напоминание)
OWN_TIME_WINDOW = timedelta(hours=3)

# Контрольная группа: им лесенка и приглашения не приходят, но решение
# пишется в журнал — так видно, возвращаются ли люди и без нас. Включившим
# напоминания приходят всегда: они их просили
HOLDOUT_PER_MILLE = 100

DAILY = "daily"


def kind_for(step: int, played: bool) -> str:
    return f"{'back' if played else 'start'}{step}"


@dataclass(frozen=True)
class NudgeState:
    """Всё, что нужно для решения. Время — местное время человека."""
    now_local: datetime                 # без пояса, по часам человека
    played: bool                        # закончил хоть одно занятие
    anchor_day: date                    # последний день занятий / день /start
    opted_in: bool                      # включил напоминания
    declined: bool                      # явно отказался
    own_time: Optional[time] = None     # его час напоминаний
    own_days: tuple = (0, 1, 2, 3, 4, 5, 6)
    usual_time: Optional[time] = None   # когда обычно занимается / пришёл
    sent_step_for_anchor: int = 0       # какая ступень по этому перерыву уже была
    last_sent_local: Optional[datetime] = None


def days_away(state: NudgeState) -> int:
    return (state.now_local.date() - state.anchor_day).days


def _in_window(now: datetime, start: time, length: timedelta) -> bool:
    begin = datetime.combine(now.date(), start)
    return begin <= now < begin + length


def usual_window_start(usual: Optional[time]) -> time:
    base = usual or time(18, 0)
    minutes = base.hour * 60 + base.minute - int(WINDOW_BEFORE.total_seconds() // 60)
    low = EARLIEST_USUAL.hour * 60 + EARLIEST_USUAL.minute
    high = LATEST_USUAL.hour * 60 + LATEST_USUAL.minute
    minutes = min(max(minutes, low), high)
    return time(minutes // 60, minutes % 60)


def may_send(state: NudgeState) -> bool:
    """Общий бюджет: без отказа, ≤1 в день, ≥12 ч между сообщениями."""
    if state.declined:
        return False
    last = state.last_sent_local
    if last is not None:
        if last.date() == state.now_local.date():
            return False
        if state.now_local - last < MIN_GAP:
            return False
    return True


def decide(state: NudgeState) -> Optional[tuple[str, int]]:
    """
    (вид, ступень) — что отправить сейчас, или None.

    Ступень — день перерыва для лесенки (по ней одна отправка на перерыв) и
    0 для ежедневного напоминания (его держит «одно в день»).
    """
    if not may_send(state):
        return None
    away = days_away(state)
    if away < 1:
        return None                      # сегодня уже занимался
    now = state.now_local

    ladder = LADDER if state.played else START_LADDER
    on_ladder = away in ladder and state.sent_step_for_anchor < away

    if state.opted_in and state.own_time is not None:
        # Его час — его выбор: ночью тоже, если так поставил
        if not _in_window(now, state.own_time, OWN_TIME_WINDOW):
            return None
        if state.played and away <= DAILY_WHILE_AWAY:
            if now.weekday() not in tuple(state.own_days or ()):
                return None
            return DAILY, 0
        if on_ladder:
            return kind_for(away, state.played), away
        return None

    if not on_ladder:
        return None
    if not (DAY_STARTS <= now.time() < DAY_ENDS):
        return None
    if not _in_window(now, usual_window_start(state.usual_time), WINDOW_LENGTH):
        return None
    return kind_for(away, state.played), away


def in_holdout(user_id: int) -> bool:
    """Постоянная контрольная группа ~10%: по номеру, без случайности."""
    return (int(user_id) * 2654435761) % 1000 < HOLDOUT_PER_MILLE


def is_last(kind: str) -> bool:
    return kind in (f"back{LADDER[-1]}", f"start{START_LADDER[-1]}")
