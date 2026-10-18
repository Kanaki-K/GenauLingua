"""
Админка → «Аналитика» (2.2.1): путь новичка, уходы, «Говорю», журнал.

Владелец 18.10: «админ панель обновить под новые реалии аналитики, языков,
игр — вижу что отстаём». Разбор прода 18.10 нашёл «микро-нюансы для роста»
(треть «брошенных» — перезапуск кнопкой; «Говорю» пропускают; половина
новичков уходит до 4-го вопроса) только запросами вручную: журнал пути
(`user_events`) админка не читала вовсе. Здесь — те же запросы, что в
`deploy/product_report.sql`, за 7 или 30 дней, владелец исключён.

Только чтение. Люди не называются — только числа.
"""
from __future__ import annotations

from datetime import timedelta

from aiogram import F, Router
from aiogram.types import CallbackQuery
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.handlers import admin_ui
from app.config import settings
from app.core.clock import utcnow

router = Router()

PERIODS = (7, 30)
GAME_NAMES = {"t": "Читаю", "r": "Вспоминаю", "a": "Слушаю", "s": "Говорю",
              "b": "Собираю", "m": "Доска"}
SOURCE_NAMES = {"menu": "меню «Учить»", "again": "«Ещё занятие»", "repeat": "повтор ошибок",
                "home": "главный экран", "channel": "игра с главного", "start": "знакомство",
                "reminder": "напоминание (до 2.1)", "release": "патчноут", "board": "доска"}


def _days(data: str) -> int:
    tail = data.rsplit(":", 1)[-1]
    return int(tail) if tail.isdigit() and int(tail) in PERIODS else PERIODS[0]


def _params(days: int) -> dict:
    return {"since": utcnow() - timedelta(days=days), "admin": int(settings.ADMIN_USER or 0)}


def _period_row(screen: str, days: int):
    return [(f"{'✓ ' if d == days else ''}{d} дней", f"admin:ins_{screen}:{d}") for d in PERIODS]


async def _guard(callback: CallbackQuery) -> bool:
    from app.bot.handlers.admin import is_admin

    if not is_admin(callback.from_user.id):
        await callback.answer("Доступа нет")
        return False
    await callback.answer()
    return True


async def _rows(session: AsyncSession, sql: str, days: int):
    return (await session.execute(text(sql), _params(days))).all()


# ============================================================================
# РАЗДЕЛ
# ============================================================================

@router.callback_query(F.data == "admin:insights")
async def insights_hub(callback: CallbackQuery, session: AsyncSession):
    if not await _guard(callback):
        return
    text_ = admin_ui.screen(
        "Аналитика",
        lead="по журналу пути и занятиям, без владельца",
        blocks=["\n".join([
            f"Путь {admin_ui.DOT} пришли → начали → 4 ответа → закончили → вернулись",
            f"Уходы {admin_ui.DOT} где и после чего бросают, перезапуски, «Продолжить»",
            f"Говорю {admin_ui.DOT} выбор людей, приглашения, пропуски, распознавание",
            f"Журнал {admin_ui.DOT} блокировки, ошибки, кнопки меню и команды",
        ]), "Полный разбор — <code>sh deploy/product_report.sh</code> на сервере"],
    )
    await callback.message.edit_text(text_, reply_markup=admin_ui.kb(
        [("Путь", "admin:ins_path:7"), ("Уходы", "admin:ins_leave:7")],
        [("Говорю", "admin:ins_speech:7"), ("Журнал", "admin:ins_log:7")],
        back="admin:back",
    ))


# ============================================================================
# ПУТЬ НОВИЧКА
# ============================================================================

PATH_SQL = """
with u as (select id, created_at from users where id <> :admin and created_at >= :since),
s as (select s.user_id, s.is_completed, coalesce(s.answered_questions, 0) a,
             coalesce(s.local_day, s.completed_at::date) d
      from quiz_sessions s join u on u.id = s.user_id)
select
  (select count(*) from u),
  (select count(distinct user_id) from s),
  (select count(distinct user_id) from s where a >= 1),
  (select count(distinct user_id) from s where a >= 4),
  (select count(distinct user_id) from s where is_completed),
  (select count(*) from (select user_id from s where is_completed group by 1 having count(*) >= 2) x),
  (select count(*) from (select user_id from s where is_completed group by 1 having count(distinct d) >= 2) x)
"""


@router.callback_query(F.data.startswith("admin:ins_path"))
async def insights_path(callback: CallbackQuery, session: AsyncSession):
    if not await _guard(callback):
        return
    days = _days(callback.data)
    came, started, one, four, done1, done2, two_days = (await _rows(session, PATH_SQL, days))[0]
    steps = [("Пришли", came), ("Начали занятие", started), ("Ответили хоть раз", one),
             ("Ответили 4+ раза", four), ("Закончили первое", done1),
             ("Закончили 2+", done2), ("Занимались 2+ дня", two_days)]
    rows = [(name, f"{admin_ui.num(n)}  {admin_ui.pct(n, came)}") for name, n in steps]
    text_ = admin_ui.screen(
        f"Путь новичка · {days} дней",
        lead="пришедшие за период; доля — от пришедших",
        blocks=[admin_ui.table(rows),
                "Разбор 18.10: половина начавших уходила до 4-го ответа, а закончившие "
                "первое почти все возвращались — рычаг в первых трёх вопросах"],
    )
    await callback.message.edit_text(text_, reply_markup=admin_ui.kb(
        _period_row("path", days), back="admin:insights"))


# ============================================================================
# УХОДЫ
# ============================================================================

LEAVE_SQL = """
select coalesce(exit_reason, 'открыто'), count(*),
       count(*) filter (where coalesce(answered_questions, 0) = 0)
from quiz_sessions where user_id <> :admin and started_at >= :since and not is_completed
group by 1 order by 2 desc
"""
LEAVE_AT_SQL = """
select case when coalesce(answered_questions, 0) = 0 then '0' when answered_questions <= 2 then '1–2'
            when answered_questions <= 6 then '3–6' else '7+' end, count(*)
from quiz_sessions where user_id <> :admin and started_at >= :since and not is_completed
group by 1 order by 1
"""
LAST_GAME_SQL = """
with ab as (select id from quiz_sessions where user_id <> :admin and started_at >= :since
            and not is_completed),
last as (select distinct on (e.session_id) e.session_id, e.channel
         from user_events e join ab on ab.id = e.session_id
         where e.kind = 'question' order by e.session_id, e.at desc)
select channel, count(*) from last group by 1 order by 2 desc
"""
SOURCE_SQL = """
select coalesce(start_source, '?'), count(*), count(*) filter (where is_completed)
from quiz_sessions where user_id <> :admin and started_at >= :since
group by 1 order by 2 desc limit 8
"""
RESUME_SQL = """
select action, count(*) from user_events
where user_id <> :admin and at >= :since and kind = 'lesson' and action in ('resume', 'new_instead')
group by 1
"""


@router.callback_query(F.data.startswith("admin:ins_leave"))
async def insights_leave(callback: CallbackQuery, session: AsyncSession):
    if not await _guard(callback):
        return
    days = _days(callback.data)
    reasons = await _rows(session, LEAVE_SQL, days)
    reason_names = {"abandoned": "брошено", "restarted": "перезапуск",
                    "открыто": "открыто"}
    at = await _rows(session, LEAVE_AT_SQL, days)
    last = await _rows(session, LAST_GAME_SQL, days)
    sources = await _rows(session, SOURCE_SQL, days)
    resume = dict(await _rows(session, RESUME_SQL, days))

    def source_name(code):
        return SOURCE_NAMES.get(code) or ("сообщение " + code[3:] if code.startswith("nd_") else code)

    blocks = [
        admin_ui.section("Незаконченные", admin_ui.columns(
            [("", "всего", "без отв.")]
            + [(reason_names.get(r, r), n, z) for r, n, z in reasons]),
            note="перезапуск — «Учить» нажато снова в первые 10 минут без ответа"),
        admin_ui.section("Сколько ответов успели", admin_ui.table(
            [(f"{k} ответов", n) for k, n in at])),
        admin_ui.section("Последняя игра перед уходом", admin_ui.table(
            [(GAME_NAMES.get(c, c or "?"), n) for c, n in last]), note="по журналу, с 16.10"),
        admin_ui.section("Откуда начали → закончили", admin_ui.table(
            [(source_name(s), f"{admin_ui.num(done)} из {admin_ui.num(n)} "
              f"({admin_ui.pct(done, n)})") for s, n, done in sources])),
        admin_ui.section("Незаконченное при «Учить»", admin_ui.table([
            ("Продолжили", resume.get("resume", 0)),
            ("Начали новое", resume.get("new_instead", 0))]), note="с 2.2.1"),
    ]
    await callback.message.edit_text(
        admin_ui.screen(f"Уходы · {days} дней", lead="незаконченные занятия, без владельца",
                        blocks=blocks),
        reply_markup=admin_ui.kb(_period_row("leave", days), back="admin:insights"))


# ============================================================================
# «ГОВОРЮ»
# ============================================================================

CHOICE_SQL = """
select coalesce(speech_choice, 'не спрашивали'), count(*) from users where id <> :admin
group by 1 order by 2 desc
"""
SPEECH_EVENTS_SQL = """
select kind, action, count(*), count(distinct user_id) from user_events
where user_id <> :admin and at >= :since and kind in ('speech_invite', 'speech_offer')
group by 1, 2 order by 1, 2
"""
SPEECH_PLAY_SQL = """
select count(*) filter (where kind = 'question' and channel = 's'),
       count(*) filter (where kind = 'skip' and channel = 's'),
       count(*) filter (where kind = 'speech'),
       count(*) filter (where kind = 'speech' and action = 'matched' and data->>'attempt' = '1'),
       count(distinct user_id) filter (where kind = 'speech')
from user_events where user_id <> :admin and at >= :since
"""


@router.callback_query(F.data.startswith("admin:ins_speech"))
async def insights_speech(callback: CallbackQuery, session: AsyncSession):
    if not await _guard(callback):
        return
    days = _days(callback.data)
    choice_names = {"on": "согласились", "off": "убрали", "later": "«не сейчас»"}
    choices = await _rows(session, CHOICE_SQL, days)
    events = await _rows(session, SPEECH_EVENTS_SQL, days)
    shown, skipped, voiced, first_try, speakers = (await _rows(session, SPEECH_PLAY_SQL, days))[0]
    event_names = {("speech_invite", "shown"): "приглашение показано",
                   ("speech_invite", "try"): "→ «Попробовать»",
                   ("speech_invite", "later"): "→ «Не сейчас»",
                   ("speech_offer", "shown"): "«убрать?» показано",
                   ("speech_offer", "off"): "→ убрали",
                   ("speech_offer", "keep"): "→ оставили"}
    blocks = [
        admin_ui.section("Выбор людей (все)", admin_ui.table(
            [(choice_names.get(c, c), n) for c, n in choices])),
        admin_ui.section("Игра", admin_ui.table([
            ("Показано вопросов", shown),
            ("Пропущено", f"{admin_ui.num(skipped)} ({admin_ui.pct(skipped, shown)})"),
            ("Попыток голосом", f"{admin_ui.num(voiced)} у {admin_ui.people(speakers)}"),
            ("Засчитано с первой попытки", f"{admin_ui.num(first_try)} ({admin_ui.pct(first_try, voiced)})"),
        ])),
        admin_ui.section("Вопросы бота", admin_ui.table(
            [(event_names.get((k, a), f"{k} {a}"), f"{admin_ui.num(n)} у {admin_ui.people(p)}")
             for k, a, n, p in events]), note="с 2.2.1: по желанию, приглашение под итогом"),
    ]
    await callback.message.edit_text(
        admin_ui.screen(f"Говорю · {days} дней", lead="по желанию с 2.2.1, без владельца",
                        blocks=blocks),
        reply_markup=admin_ui.kb(_period_row("speech", days), back="admin:insights"))


# ============================================================================
# ЖУРНАЛ: БЛОКИРОВКИ, ОШИБКИ, МЕНЮ
# ============================================================================

BLOCKS_SQL = """
select to_char(at, 'DD.MM'), count(*) filter (where action = 'blocked'),
       count(*) filter (where action = 'unblocked')
from user_events where user_id <> :admin and at >= :since and kind = 'chat'
group by 1, at::date order by at::date desc limit 10
"""
ERRORS_SQL = """
select action, coalesce(data->>'where', '?'), count(*), count(distinct user_id) from user_events
where user_id <> :admin and at >= :since and kind = 'error'
group by 1, 2 order by 3 desc limit 8
"""
MENU_SQL = """
select action, count(*), count(distinct user_id) from user_events
where user_id <> :admin and at >= :since and kind = 'msg'
  and (action like 'меню %' or action like 'команда %')
group by 1 order by 2 desc limit 10
"""


@router.callback_query(F.data.startswith("admin:ins_log"))
async def insights_log(callback: CallbackQuery, session: AsyncSession):
    if not await _guard(callback):
        return
    days = _days(callback.data)
    blocks_rows = await _rows(session, BLOCKS_SQL, days)
    errors = await _rows(session, ERRORS_SQL, days)
    menu = await _rows(session, MENU_SQL, days)
    blocks = [
        admin_ui.section("Блокировки по дням", admin_ui.table(
            [(day, f"ушли {b}, вернулись {u}") for day, b, u in blocks_rows]),
            note="в момент блокировки, с 2.2.1", empty="ни одной"),
        admin_ui.section("Ошибки", admin_ui.table(
            [(f"{kind} · {where}", f"{n} у {admin_ui.people(p)}") for kind, where, n, p in errors]),
            empty="ни одной"),
        admin_ui.section("Кнопки меню и команды", admin_ui.table(
            [(action, f"{n} у {admin_ui.people(p)}") for action, n, p in menu]),
            note="по имени с 2.2.1"),
    ]
    await callback.message.edit_text(
        admin_ui.screen(f"Журнал · {days} дней", lead="без владельца", blocks=blocks),
        reply_markup=admin_ui.kb(_period_row("log", days), back="admin:insights"))


# ============================================================================
# КАРТОЧКА ЧЕЛОВЕКА: ПУТЬ (2.2.1)
# ============================================================================

async def person_journey_block(session: AsyncSession, user_id: int) -> str:
    """
    Что с человеком было: бросал ли, блокировал ли, ошибки, сообщения бота и
    последние события журнала — компактно, чтобы карточка влезла в экран.
    Полный путь за день — `python -m app.scripts.journey --user <хеш> --day <дата>`.
    """
    params = {"u": user_id}
    abandoned, restarted = (await session.execute(text(
        "select count(*) filter (where exit_reason = 'abandoned'), "
        "count(*) filter (where exit_reason = 'restarted') "
        "from quiz_sessions where user_id = :u and not is_completed"), params)).one()
    status = (await session.execute(text(
        "select action, at from user_events where user_id = :u and kind = 'chat' "
        "order by at desc limit 1"), params)).first()
    errors = (await session.execute(text(
        "select count(*) from user_events where user_id = :u and kind = 'error'"), params)).scalar()
    nudges = (await session.execute(text(
        "select kind, outcome, sent_at from nudge_log where user_id = :u "
        "order by sent_at desc nulls last limit 4"), params)).all()
    events = (await session.execute(text(
        "select at, kind, coalesce(action, ''), coalesce(channel, '') from user_events "
        "where user_id = :u and kind not in ('tap', 'msg') order by at desc limit 8"), params)).all()

    blocked = "заблокировал " + status[1].strftime("%d.%m") if status and status[0] == "blocked" \
        else ("вернулся " + status[1].strftime("%d.%m") if status else "—")
    head = admin_ui.table([
        ("Брошено", f"{abandoned}, перезапуск {restarted}"),
        ("Бот", blocked),
        ("Ошибок у него", errors or 0),
    ])
    lines = [f"{(n[2].strftime('%d.%m %H:%M') if n[2] else '—')} {n[0]} · {n[1]}" for n in nudges]
    sent = admin_ui.listing(lines) if lines else "сообщений бота не было"
    trail = admin_ui.listing(
        f"{at.strftime('%d.%m %H:%M')} {kind} {action}{(' · ' + GAME_NAMES.get(ch, ch)) if ch else ''}"
        for at, kind, action, ch in events) if events else "событий нет (журнал с 16.10)"
    return admin_ui.section("Путь", f"{head}\n\nСообщения бота\n{sent}\n\nПоследнее в журнале\n{trail}")
