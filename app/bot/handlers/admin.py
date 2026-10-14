"""
Админ-панель: экраны видит только владелец, стилистика та же, что у бота.

ВНЕШНОСТЬ. Устав — `UI_CONCEPT.md`, сборка — `admin_ui`. Здесь не должно
появляться ни одного значка: в админке их было 178 пятидесяти видов, и
они не несли смысла, которого нет у слова. Единственное исключение — `✓`
и `✗` в решении по жалобе, они из разрешённого набора четырёх.

СТРОЕНИЕ. Пять групп, у каждой на главной своя строка с её же числом:

    Люди     приход по месяцам, отток, лучшие, карточка человека
    Занятия  четыре игры, удержание, внимание
    Слова    сложные и частые
    Жалобы   разбор с начислением баллов
    Выгрузка CSV

Прежде на главной лежали восемь плоских кнопок, а «Аналитика» была
свалкой из пяти несвязанных замеров на одном экране. Правило «один экран
— одна работа» разнесло их по смыслу.

ПОЧЕМУ КОМАНДЫ ОСТАЛИСЬ. `/admin_users`, `/admin_stats`, `/admin_user`,
`/broadcast` — это двери, набранные руками, и ломать их нельзя. Но текст
они теперь собирают теми же сборщиками, что и экраны: раньше «Топ-20» и
«Топ-15» были двумя копиями одного кода, и расходились.
"""

import asyncio
import csv
import io
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, BufferedInputFile
from sqlalchemy.ext.asyncio import AsyncSession
# text импортируется под псевдонимом: в этом модуле `text` — локальная
# переменная, в которой собираются сообщения, и импорт её бы затенял
from sqlalchemy import select, func, and_, distinct, case, desc, or_, text as sql_text
from typing import Optional
from datetime import datetime, timedelta, date
from app.core.clock import utcnow, utctoday
from app.database.enums import QuizChannel
from app.database.models import (
    MonthlyStats, QuizQuestion, QuizSession, TranslationReport, User, UserWord, Word,
)
from app.bot.handlers import admin_ui
from app.services.streak_service import current_streak
from app.services.quiz_service import get_user_progress_stats
from app.services.language_service import LANGUAGES, flag, pair_from_user, pair_label
from app.services.word_stats import MIN_SHOWS_FOR_DIFFICULTY, difficulty_rank_sql
from app.config import settings

import logging

logger = logging.getLogger(__name__)

router = Router()

ADMIN_USER_ID = settings.ADMIN_USER

# Сколько занятий уходит в выгрузку. Число было вписано в запрос, а экран
# выгрузки обещал «все»: на 2 320 занятиях разница незаметна, на двадцати
# тысячах файл молча оборвётся на последней тысяче
EXPORT_QUIZ_LIMIT = 1000

# Сколько людей в «Лучших». Прежде на экране было 15, а в команде
# `/admin_users` — 20, и это были две копии одного кода
TOP_PEOPLE = 15


def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_USER_ID


def _display_name(user: User) -> str:
    """Имя для отображения в админке"""
    if user.first_name:
        return user.first_name
    elif user.username:
        return f"@{user.username}"
    return f"User {user.id}"


def _lang_name(code: Optional[str]) -> str:
    """
    Название языка словом. Правило живёт в `language_service`: та же
    подпись нужна якорю, заголовку занятия и карточке, и приватная копия
    здесь разъехалась бы с ними при первой правке названий.
    """
    from app.services.language_service import language_word

    return language_word(code, "ru") or "не выбран"


def _full_word(word_de: str, article: Optional[str]) -> str:
    """
    Слово с артиклем. Правило было выписано в этом файле СЕМЬ раз, и в
    каждом месте проверка на прочерк повторялась заново.
    """
    if article and article != "-":
        return f"{article} {word_de}"
    return word_de


def get_admin_keyboard() -> InlineKeyboardMarkup:
    """
    Пять групп вместо восьми плоских кнопок.

    Прежде на главной лежали восемь равноправных кнопок: «Аналитика»,
    «Когорты», «Churn», «Экспорт», «Топ юзеры», «Детали», «Игры»,
    «Репорты». Половина названий не говорила, что внутри («Детали» — чего?
    «Churn» — по-английски в русской панели), а «Аналитика» была свалкой из
    пяти несвязанных замеров: удержание, двери входа, скорость ответа,
    точки выхода и самые медленные слова на одном экране.

    Теперь группы по вопросу, на который отвечают, и у каждой на главной
    своя строка с её же числом — чтобы не открывать раздел наугад.
    """
    return admin_ui.kb(
        [("Люди", "admin:people"), ("Занятия", "admin:lessons")],
        [("Слова", "admin:words"), ("Жалобы", "admin:reports")],
        [("Выгрузка", "admin:export")],
    )


async def _get_main_stats(session: AsyncSession) -> str:
    """Собрать базовую статистику для главной панели"""
    total_users_result = await session.execute(select(func.count()).select_from(User))
    total_users = total_users_result.scalar()

    # Активные сегодня — по last_active_date ИЛИ quiz_sessions (fallback)
    active_24h_result = await session.execute(
        select(func.count(distinct(User.id)))
        .select_from(User)
        .where(or_(
            User.last_active_date >= utctoday(),
            User.last_quiz_date >= utctoday()
        ))
    )
    active_24h = active_24h_result.scalar()

    week_ago = utctoday() - timedelta(days=7)
    active_7d_result = await session.execute(
        select(func.count(distinct(User.id)))
        .select_from(User)
        .where(or_(
            User.last_active_date >= week_ago,
            User.last_quiz_date >= week_ago
        ))
    )
    active_7d = active_7d_result.scalar()

    total_quizzes_result = await session.execute(
        select(func.count())
        .select_from(QuizSession)
        .where(QuizSession.completed_at.isnot(None))
    )
    total_quizzes = total_quizzes_result.scalar()

    day_ago = utcnow() - timedelta(hours=24)
    quizzes_24h_result = await session.execute(
        select(func.count())
        .select_from(QuizSession)
        .where(
            QuizSession.completed_at.isnot(None),
            QuizSession.completed_at >= day_ago
        )
    )
    quizzes_24h = quizzes_24h_result.scalar()

    # «Из напоминаний» искало значение 'notification', которого не писал
    # НИКТО: в `start_source` всегда уходило «menu». Метрика не могла стать
    # ненулевой ни при каких условиях и показывала 0 как факт. Пометка
    # берётся из того же места, откуда её пишет обработчик
    from app.bot.handlers.quiz.game import SOURCE_REMINDER

    notif_sessions_result = await session.execute(
        select(func.count())
        .select_from(QuizSession)
        .where(
            QuizSession.start_source == SOURCE_REMINDER,
            QuizSession.completed_at.isnot(None),
        )
    )
    notif_sessions = notif_sessions_result.scalar() or 0

    active_ever_result = await session.execute(
        select(func.count(distinct(QuizSession.user_id)))
        .select_from(QuizSession)
        .where(QuizSession.completed_at.isnot(None))
    )
    active_ever = active_ever_result.scalar() or 0

    # Точность по базе — по фактически отвеченным вопросам, а не по
    # плановым: брошенные занятия иначе выглядят сплошными ошибками
    totals = await session.execute(
        select(
            func.coalesce(func.sum(QuizSession.answered_questions), 0),
            func.coalesce(func.sum(QuizSession.correct_answers), 0),
        ).where(QuizSession.completed_at.isnot(None))
    )
    answered, correct = totals.one()

    words_total = (await session.execute(
        select(func.count()).select_from(Word)
    )).scalar() or 0

    pending = (await session.execute(
        select(func.count()).select_from(TranslationReport)
        .where(TranslationReport.status == "pending")
    )).scalar() or 0

    # Строка у каждой группы — чтобы не открывать раздел наугад: видно и
    # что внутри, и главное его число
    groups = "\n".join([
        f"Люди {admin_ui.DOT} {admin_ui.num(total_users)}, "
        f"сегодня {admin_ui.num(active_24h)}, играли {admin_ui.num(active_ever)}",
        f"Занятия {admin_ui.DOT} {admin_ui.num(total_quizzes)} кругов, "
        f"точность {admin_ui.pct(correct, answered)}",
        f"Слова {admin_ui.DOT} {admin_ui.num(words_total)} в базе",
        f"Жалобы {admin_ui.DOT} " + (
            f"{admin_ui.num(pending)} ждут решения" if pending else "решены все"
        ),
        f"Выгрузка {admin_ui.DOT} люди и занятия в CSV",
    ])

    return admin_ui.screen(
        "Панель",
        lead=(f"сегодня {admin_ui.num(active_24h)} "
              f"{admin_ui.DOT} за сутки {admin_ui.num(quizzes_24h)} кругов"),
        blocks=[
            admin_ui.table([
                ("Людей", total_users),
                ("Играли хоть раз", active_ever),
                ("Сегодня", active_24h),
                ("За 7 дней", active_7d),
                ("Кругов всего", total_quizzes),
                ("Из напоминаний", notif_sessions),
            ]),
            groups,
        ],
    )


async def _guard(callback: CallbackQuery) -> bool:
    """
    Доступ и погашение «часиков» — одним вызовом на каждый экран.

    Прежде эти четыре строки были скопированы в каждый обработчик
    четырнадцать раз, и в одном из них (`admin:back`) ответ на callback
    стоял, а отказ не отправлялся вовсе.
    """
    if not is_admin(callback.from_user.id):
        await callback.answer("Доступа нет")
        return False
    await callback.answer()
    return True


# ============================================================================
# ГЛАВНАЯ ПАНЕЛЬ
# ============================================================================

@router.message(Command("admin"))
async def admin_panel(message: Message, session: AsyncSession):
    if not is_admin(message.from_user.id):
        await message.answer("Доступа к панели нет")
        return

    try:
        await message.delete()
    except Exception:
        pass

    text = await _get_main_stats(session)
    await message.answer(text, reply_markup=get_admin_keyboard())


# ============================================================================
# ГРУППЫ: ЛЮДИ И ЗАНЯТИЯ
# ============================================================================

@router.callback_query(F.data == "admin:people")
async def admin_people(callback: CallbackQuery, session: AsyncSession):
    """
    Группа «Люди»: приход, отток, лучшие, карточка одного человека.

    Экран сам ничего не считает, кроме четырёх чисел для строк групп: его
    работа — показать, что лежит за каждой кнопкой. Отдельные замеры
    стоят внутри, иначе на одном экране снова оказалось бы пять разных
    вопросов.
    """
    if not await _guard(callback):
        return

    total = (await session.execute(
        select(func.count()).select_from(User)
    )).scalar() or 0
    played = (await session.execute(
        select(func.count(distinct(QuizSession.user_id)))
        .where(QuizSession.completed_at.isnot(None))
    )).scalar() or 0

    # Через подзапрос, а не `group_by` + `having`: с группировкой запрос
    # отдаёт по строке на человека, и `.scalar()` взял бы первую вместо
    # количества — то есть показал бы единицу при любом числе пропавших
    week_ago = utctoday() - timedelta(days=7)
    last_round = (
        select(QuizSession.user_id,
               func.max(func.date(QuizSession.completed_at)).label("day"))
        .where(QuizSession.completed_at.isnot(None))
        .group_by(QuizSession.user_id)
        .subquery()
    )
    stale = (await session.execute(
        select(func.count()).select_from(last_round)
        .where(last_round.c.day < week_ago)
    )).scalar() or 0

    text = admin_ui.screen(
        "Люди",
        lead=f"{admin_ui.people(total)}, играли {admin_ui.num(played)}",
        blocks=[
            admin_ui.table([
                ("Всего", total),
                ("Играли хоть раз", played),
                ("Не играли", total - played),
                ("Пропали на 7+ дней", stale),
            ]),
            "\n".join([
                f"Приход {admin_ui.DOT} когорты по месяцам, уровни, языки",
                f"Отток {admin_ui.DOT} кто уходит и когда ушёл",
                f"Лучшие {admin_ui.DOT} пятнадцать по пройденным кругам",
                f"Человек {admin_ui.DOT} карточка по id или имени",
            ]),
        ],
    )
    keyboard = admin_ui.kb(
        [("Приход", "admin:cohorts"), ("Отток", "admin:churn")],
        [("Лучшие", "admin:top_users"), ("Человек", "admin:person_help")],
        back="admin:back",
    )
    await callback.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(F.data == "admin:lessons")
async def admin_lessons(callback: CallbackQuery, session: AsyncSession):
    """
    Группа «Занятия»: четыре игры, удержание, внимание.

    Прежде всё это лежало на одном экране «Аналитика» вместе с когортами:
    удержание, двери входа, скорость ответа, точки выхода и самые медленные
    слова. Пять вопросов на одном экране — ни на один нельзя было ответить,
    не прокручивая.
    """
    if not await _guard(callback):
        return

    rounds = (await session.execute(
        select(func.count()).select_from(QuizSession)
        .where(QuizSession.completed_at.isnot(None))
    )).scalar() or 0
    abandoned = (await session.execute(
        select(func.count()).select_from(QuizSession)
        .where(QuizSession.exit_reason == "abandoned")
    )).scalar() or 0
    answered, correct = (await session.execute(
        select(
            func.coalesce(func.sum(QuizSession.answered_questions), 0),
            func.coalesce(func.sum(QuizSession.correct_answers), 0),
        ).where(QuizSession.completed_at.isnot(None))
    )).one()

    text = admin_ui.screen(
        "Занятия",
        lead=(f"{admin_ui.num(rounds)} кругов пройдено "
              f"{admin_ui.DOT} точность {admin_ui.pct(correct, answered)}"),
        blocks=[
            admin_ui.table([
                ("Кругов пройдено", rounds),
                ("Брошено", abandoned),
                ("Ответов", answered),
                ("Из них верных", correct),
                ("Точность", admin_ui.pct(correct, answered)),
            ]),
            "\n".join([
                f"Игры {admin_ui.DOT} четыре канала, состав, доска, двери входа",
                f"Удержание {admin_ui.DOT} возвращаются ли на второй день",
                f"Внимание {admin_ui.DOT} скорость ответа и где бросают круг",
            ]),
        ],
    )
    keyboard = admin_ui.kb(
        [("Игры", "admin:games"), ("Удержание", "admin:retention")],
        [("Внимание", "admin:attention")],
        back="admin:back",
    )
    await callback.message.edit_text(text, reply_markup=keyboard)


# ============================================================================
# ИГРЫ
# ============================================================================

@router.callback_query(F.data == "admin:games")
async def admin_games(callback: CallbackQuery, session: AsyncSession):
    """
    ЧЕТЫРЕ ИГРЫ: чем играют, насколько получается, откуда приходят.

    ЗАЧЕМ ОТДЕЛЬНЫЙ РАЗДЕЛ. Игр в боте четыре, а в админке их не было видно
    НИ В ОДНОМ экране: ни сколько ответов пришло каждым каналом, ни с какой
    точностью, ни кто какие каналы включил, ни попадалась ли доска. То
    есть главную работу последних недель нельзя было ни подтвердить, ни
    опровергнуть числом.

    Второе здесь не менее важно: ОТКУДА начинают занятия. Прежде в
    `start_source` всегда писалось «menu», а метрика «Из напоминаний»
    искала значение, которого не писал никто, — петлю возврата нечем было
    измерить. Теперь у каждой двери своя пометка, и этот список и есть
    замер петли.
    """
    if not await _guard(callback):
        return

    from app.services.match_service import BOARD_CHANNEL

    names = {
        QuizChannel.TEXT.value: "Карточка",
        QuizChannel.REVERSE.value: "Вспомнить",
        QuizChannel.AUDIO.value: "На слух",
        QuizChannel.SPEECH.value: "Вслух",
        BOARD_CHANNEL: "Доска",
    }

    # Ответы и точность по каналам. Пустой канал — история до того, как
    # канал начали записывать; он показывается отдельной строкой, а не
    # подмешивается к тексту, иначе давняя история исказила бы свежую
    # картину
    rows = await session.execute(
        select(
            QuizQuestion.channel,
            func.count(),
            func.sum(case((QuizQuestion.is_correct.is_(True), 1), else_=0)),
        ).group_by(QuizQuestion.channel)
    )
    by_channel = {
        channel: (int(total), int(correct or 0))
        for channel, total, correct in rows.all()
    }

    known = [c for c in names if c in by_channel]
    channel_rows = []
    for code in known:
        total, correct = by_channel[code]
        channel_rows.append((names[code], total, admin_ui.pct(correct, total)))
    legacy = by_channel.get(None)
    if legacy:
        channel_rows.append(("Без канала", legacy[0], "—"))

    channels_block = admin_ui.section(
        "Ответы по каналам",
        admin_ui.columns(channel_rows) if channel_rows else None,
        note="ответов · точность",
        empty="ни одного ответа с записанным каналом",
    )

    # Кто какие каналы включил. Это НЕ то же, что ответы: человек мог
    # включить слух и ни разу не дойти до порога допуска по слову
    enabled = await session.execute(
        select(User.quiz_channels, func.count()).group_by(User.quiz_channels)
    )
    counts = {"t": 0, "r": 0, "a": 0, "s": 0}
    for channels, n in enabled.all():
        for letter in (channels or "t"):
            if letter in counts:
                counts[letter] += int(n)
    board_on = (await session.execute(
        select(func.count()).select_from(User).where(User.match_in_round.is_(True))
    )).scalar() or 0
    board_rounds = (await session.execute(
        select(func.count(distinct(QuizQuestion.session_id)))
        .where(QuizQuestion.channel == BOARD_CHANNEL)
    )).scalar() or 0
    reverse = (await session.execute(
        select(func.count()).select_from(QuizSession)
        .where(QuizSession.is_reverse.is_(True))
    )).scalar() or 0
    total_sessions = (await session.execute(
        select(func.count()).select_from(QuizSession)
    )).scalar() or 0

    setup_block = admin_ui.section(
        "Что включено у людей",
        admin_ui.table([
            ("Карточка", counts["t"]),
            ("Вспомнить", counts["r"]),
            ("На слух", counts["a"]),
            ("Вслух", counts["s"]),
            ("Доска в круге", board_on),
            ("Кругов с доской", board_rounds),
            ("Обратный перевод", f"{admin_ui.num(reverse)} из "
                                 f"{admin_ui.num(total_sessions)}"),
        ]),
        note="включено — не то же, что сыграно: слуху нужен порог по слову",
    )

    # ОТКУДА НАЧИНАЮТ — замер петли возврата. Подписи берутся из того же
    # места, где живут сами пометки (`game.SOURCE_LABELS`): прежде они были
    # выписаны здесь руками, и в соседнем экране — по-другому
    from app.bot.handlers.quiz.game import source_label

    sources = (await session.execute(
        select(QuizSession.start_source, func.count())
        .group_by(QuizSession.start_source)
        .order_by(func.count().desc())
    )).all()
    door_rows = [(source_label(source), n) for source, n in sources if source]
    doors_block = admin_ui.section(
        "Откуда начинают занятие",
        admin_ui.table(door_rows) if door_rows else None,
        note="это и есть замер петли возврата",
        empty="пометок пока нет: они появились 13 октября",
    )

    pairs = (await session.execute(
        select(QuizSession.learning_lang, QuizSession.native_lang, func.count())
        .group_by(QuizSession.learning_lang, QuizSession.native_lang)
        .order_by(func.count().desc()).limit(8)
    )).all()
    pairs_block = admin_ui.section(
        "Пары, в которых играют",
        admin_ui.table([(f"{learning} → {native}", n)
                        for learning, native, n in pairs]),
    )

    text = admin_ui.screen(
        "Игры",
        lead="четыре канала: карточка, слух, речь, доска",
        blocks=[channels_block, setup_block, doors_block, pairs_block],
    )
    await callback.message.edit_text(
        text, reply_markup=admin_ui.kb(back="admin:lessons")
    )


@router.callback_query(F.data == "admin:retention")
async def admin_retention(callback: CallbackQuery, session: AsyncSession):
    """
    Возвращаются ли люди. Один вопрос — один экран.

    Прежде удержание стояло на экране «Аналитика» вместе со скоростью
    ответа, точками выхода и самыми медленными словами. Главное число
    проекта — доля вернувшихся на второй день — тонуло среди четырёх
    чужих замеров.
    """
    if not await _guard(callback):
        return

    # По когортам: «вернулся на СЛЕДУЮЩИЙ календарный день после
    # регистрации», а не «играл когда-нибудь позже». Прежний запрос считал
    # второе и завышал D1 примерно втрое: 31% вместо 11%.
    yesterday = utctoday() - timedelta(days=1)
    week_ago = utctoday() - timedelta(days=7)

    d1_cohort = (await session.execute(
        select(func.count()).select_from(User)
        .where(func.date(User.created_at) <= yesterday)
    )).scalar() or 0
    d1_returned = (await session.execute(
        select(func.count(distinct(User.id)))
        .select_from(User)
        .join(QuizSession, User.id == QuizSession.user_id)
        .where(
            func.date(User.created_at) <= yesterday,
            func.date(QuizSession.started_at) == func.date(User.created_at) + 1,
        )
    )).scalar() or 0

    # D7: вернулся на 7-й день или позже, но в пределах двух недель — иначе
    # метрика сливается с «когда-нибудь возвращался»
    d7_cohort = (await session.execute(
        select(func.count()).select_from(User)
        .where(func.date(User.created_at) <= week_ago)
    )).scalar() or 0
    d7_returned = (await session.execute(
        select(func.count(distinct(User.id)))
        .select_from(User)
        .join(QuizSession, User.id == QuizSession.user_id)
        .where(
            func.date(User.created_at) <= week_ago,
            func.date(QuizSession.started_at) >= func.date(User.created_at) + 7,
            func.date(QuizSession.started_at) <= func.date(User.created_at) + 14,
        )
    )).scalar() or 0

    # Не удержание когорты, а нынешняя живость базы: сколько вообще
    # заходило за неделю
    active_week = (await session.execute(
        select(func.count(distinct(QuizSession.user_id)))
        .select_from(QuizSession)
        .where(QuizSession.started_at
               >= datetime.combine(week_ago, datetime.min.time()))
    )).scalar() or 0

    text = admin_ui.screen(
        "Удержание",
        lead="второй день — главное число проекта",
        blocks=[
            admin_ui.table([
                ("Второй день", f"{admin_ui.pct(d1_returned, d1_cohort, digits=1)}"),
                ("  из них", f"{admin_ui.num(d1_returned)} из {admin_ui.num(d1_cohort)}"),
                ("Седьмой день", f"{admin_ui.pct(d7_returned, d7_cohort, digits=1)}"),
                ("  из них", f"{admin_ui.num(d7_returned)} из {admin_ui.num(d7_cohort)}"),
                ("Заходили за 7 дней", active_week),
            ]),
            ("<i>второй день — вернулись именно на следующий календарный день "
             "после знакомства. Седьмой — на 7–14-й. «Заходили за 7 дней» — "
             "не удержание, а нынешняя живость базы</i>"),
            admin_ui.section(
                "Шкалы",
                admin_ui.listing([
                    f"день 2  {admin_ui.bar(d1_returned, d1_cohort)} "
                    f"{admin_ui.pct(d1_returned, d1_cohort)}",
                    f"день 7  {admin_ui.bar(d7_returned, d7_cohort)} "
                    f"{admin_ui.pct(d7_returned, d7_cohort)}",
                ]),
            ),
        ],
    )
    await callback.message.edit_text(
        text, reply_markup=admin_ui.kb(back="admin:lessons")
    )


@router.callback_query(F.data == "admin:attention")
async def admin_attention(callback: CallbackQuery, session: AsyncSession):
    """
    Внимание в круге: быстро ли отвечают и где бросают.

    Три замера, и все три зависят от полей, которые долгое время не
    записывались: `response_time_seconds` и `exit_at_question` были пустыми
    на всей истории. Раньше такие разделы молча исчезали, и панель
    выглядела наполовину пустой без объяснения — отличить «данных нет» от
    «код сломался» было нельзя. Пустота проговаривается.
    """
    if not await _guard(callback):
        return

    NO_DATA = "замеры собираются только с последнего обновления бота"

    speed = (await session.execute(
        select(
            func.count(case((QuizQuestion.response_time_seconds <= 2, 1))),
            func.count(case((and_(QuizQuestion.response_time_seconds > 2,
                                  QuizQuestion.response_time_seconds <= 5), 1))),
            func.count(case((and_(QuizQuestion.response_time_seconds > 5,
                                  QuizQuestion.response_time_seconds <= 10), 1))),
            func.count(case((QuizQuestion.response_time_seconds > 10, 1))),
        ).select_from(QuizQuestion)
        .where(QuizQuestion.response_time_seconds.isnot(None))
    )).first()
    total_answers = sum(speed) if speed else 0

    speed_block = admin_ui.section(
        "Скорость ответа",
        admin_ui.table([
            ("до 2 сек (знает)", admin_ui.pct(speed[0], total_answers)),
            ("3–5 сек (думает)", admin_ui.pct(speed[1], total_answers)),
            ("6–10 сек (трудно)", admin_ui.pct(speed[2], total_answers)),
            ("больше 10 (гадает)", admin_ui.pct(speed[3], total_answers)),
        ]) if total_answers else None,
        empty=NO_DATA,
    )

    exits = (await session.execute(
        select(
            func.count(case((QuizSession.exit_at_question <= 5, 1))),
            func.count(case((and_(QuizSession.exit_at_question > 5,
                                  QuizSession.exit_at_question <= 10), 1))),
            func.count(case((and_(QuizSession.exit_at_question > 10,
                                  QuizSession.exit_at_question <= 15), 1))),
            func.count(case((QuizSession.exit_at_question > 15, 1))),
        ).select_from(QuizSession)
        .where(QuizSession.exit_reason == "abandoned")
    )).first()

    exits_block = admin_ui.section(
        "Где бросают круг",
        admin_ui.table([
            ("Вопросы 1–5", exits[0]),
            ("Вопросы 6–10", exits[1]),
            ("Вопросы 11–15", exits[2]),
            ("Дальше 15", exits[3]),
        ]) if exits and any(exits) else None,
        empty=NO_DATA,
    )

    slow = (await session.execute(
        select(Word.word_de, Word.article,
               func.avg(QuizQuestion.response_time_seconds).label("avg_time"))
        .select_from(Word)
        .join(QuizQuestion, Word.id == QuizQuestion.word_id)
        .where(QuizQuestion.response_time_seconds.isnot(None))
        .group_by(Word.id, Word.word_de, Word.article)
        .order_by(desc("avg_time"))
        .limit(5)
    )).all()

    slow_block = admin_ui.section(
        "Над чем думают дольше всего",
        admin_ui.table([
            (_full_word(word_de, article), f"{admin_ui.num(float(avg_time))} сек")
            for word_de, article, avg_time in slow
        ]) if slow else None,
        empty=NO_DATA,
    )

    text = admin_ui.screen(
        "Внимание",
        lead="быстро ли отвечают и на каком вопросе уходят",
        blocks=[speed_block, exits_block, slow_block],
    )
    await callback.message.edit_text(
        text, reply_markup=admin_ui.kb(back="admin:lessons")
    )



# ============================================================================
# КОГОРТЫ
# ============================================================================

@router.callback_query(F.data == "admin:cohorts")
async def admin_cohorts(callback: CallbackQuery, session: AsyncSession):
    """Приход по месяцам, уровни и языки."""
    if not await _guard(callback):
        return

    # Все месяцы, а не только текущий и предыдущий: раньше заголовок обещал
    # «по месяцам регистрации», а показывались два последних — и когорта
    # запуска, единственная с заметным удержанием, была не видна вообще.
    #
    # «Играли» и «дошли до привычки» считаются в пределах своей когорты:
    # прежний запрос спрашивал «завершал ли когда-нибудь хоть одну викторину»
    # без привязки к месяцу регистрации.
    cohort_result = await session.execute(
        sql_text(
            """
            WITH per_user AS (
                SELECT u.id,
                       to_char(u.created_at, 'YYYY-MM') AS cohort,
                       COUNT(DISTINCT date(q.started_at)) AS active_days
                FROM users u
                LEFT JOIN quiz_sessions q ON q.user_id = u.id
                GROUP BY u.id, to_char(u.created_at, 'YYYY-MM')
            )
            SELECT cohort,
                   COUNT(*) AS registered,
                   COUNT(*) FILTER (WHERE active_days > 0) AS played,
                   COUNT(*) FILTER (WHERE active_days >= 5) AS retained
            FROM per_user
            GROUP BY cohort
            ORDER BY cohort
            """
        )
    )
    monthly_cohorts = [
        (row.cohort, row.registered, row.played, row.retained)
        for row in cohort_result
    ]

    levels_stats_result = await session.execute(
        select(
            User.level,
            func.count(distinct(User.id)).label('users'),
            func.avg(User.quizzes_passed).label('avg_quizzes')
        )
        .select_from(User)
        .where(User.level.isnot(None))
        .group_by(User.level)
    )
    levels_stats = levels_stats_result.all()

    langs_result = await session.execute(
        select(User.interface_language, func.count())
        .select_from(User)
        .group_by(User.interface_language)
    )
    langs = langs_result.all()
    total_lang_users = sum(count for _, count in langs)

    # Разбивка по изучаемому и родному языку. Прежде этого экрана не было
    # вовсе: показывался только язык интерфейса, а какой язык люди изучают —
    # не видно. Пока языков было два, это ещё читалось из общей картины, при
    # шести уже нет.
    learning_result = await session.execute(
        select(User.learning_lang, func.count())
        .select_from(User)
        .group_by(User.learning_lang)
        .order_by(func.count().desc())
    )
    learning_stats = learning_result.all()

    native_result = await session.execute(
        select(User.native_lang, func.count())
        .select_from(User)
        .group_by(User.native_lang)
        .order_by(func.count().desc())
    )
    native_stats = native_result.all()

    # Месяц одной строкой: пришло, заиграли, дошли до привычки. Прежде на
    # каждый месяц уходило по две строки с ветвлением на три уровня, и
    # девять месяцев не влезали на экран
    months_rows = [
        (month, registered, admin_ui.pct(played, registered),
         admin_ui.pct(retained, registered))
        for month, registered, played, retained in monthly_cohorts
    ]
    months_block = admin_ui.section(
        "Приход по месяцам",
        admin_ui.columns(months_rows) if months_rows else None,
        note="пришло · заиграли · дошли до привычки (5+ дней с занятиями)",
    )

    levels_block = admin_ui.section(
        "По уровням",
        admin_ui.columns([
            (level.value, users, admin_ui.num(float(avg_quizzes or 0)))
            for level, users, avg_quizzes in levels_stats if level
        ]),
        note="людей · в среднем кругов на человека",
    )

    def lang_block(title: str, rows: list, total: int) -> str:
        return admin_ui.section(title, admin_ui.columns([
            (_lang_name(code), count, admin_ui.pct(count, total))
            for code, count in rows
        ]))

    total_users = sum(count for _, count in learning_stats) or 1

    text = admin_ui.screen(
        "Приход",
        lead="кто пришёл, когда и на каком языке",
        blocks=[
            months_block,
            levels_block,
            lang_block("Что изучают", learning_stats, total_users),
            lang_block("Язык значений", native_stats, total_users),
            lang_block("Язык бота", langs, total_lang_users),
        ],
    )
    await callback.message.edit_text(
        text, reply_markup=admin_ui.kb(back="admin:people")
    )


# ============================================================================
# CHURN
# ============================================================================

@router.callback_query(F.data == "admin:churn")
async def admin_churn(callback: CallbackQuery, session: AsyncSession):
    """Кто уходит: по давности последнего круга."""
    if not await _guard(callback):
        return

    today = utctoday()
    week_ago = today - timedelta(days=7)
    three_days_ago = today - timedelta(days=3)
    month_ago = today - timedelta(days=30)

    # Высокий риск: играли, но не заходили 7+ дней
    # Используем subquery для получения реальной последней даты из quiz_sessions
    last_quiz_subq = (
        select(
            QuizSession.user_id,
            func.max(func.date(QuizSession.completed_at)).label('real_last_quiz')
        )
        .where(QuizSession.completed_at.isnot(None))
        .group_by(QuizSession.user_id)
    ).subquery()

    high_risk_result = await session.execute(
        select(User.first_name, User.username, last_quiz_subq.c.real_last_quiz)
        .join(last_quiz_subq, User.id == last_quiz_subq.c.user_id)
        .where(last_quiz_subq.c.real_last_quiz < week_ago)
        .order_by(last_quiz_subq.c.real_last_quiz.asc())
        .limit(10)
    )
    high_risk = high_risk_result.all()

    high_risk_count_result = await session.execute(
        select(func.count())
        .select_from(last_quiz_subq)
        .where(last_quiz_subq.c.real_last_quiz < week_ago)
    )
    high_risk_count = high_risk_count_result.scalar() or 0

    medium_risk_count_result = await session.execute(
        select(func.count())
        .select_from(last_quiz_subq)
        .where(
            last_quiz_subq.c.real_last_quiz >= week_ago,
            last_quiz_subq.c.real_last_quiz < three_days_ago
        )
    )
    medium_risk_count = medium_risk_count_result.scalar() or 0

    # Churn rate: из тех кто играл 30+ дней назад — сколько не вернулись
    players_month_ago_result = await session.execute(
        select(func.count())
        .select_from(User)
        .where(
            User.created_at <= datetime.combine(month_ago, datetime.min.time()),
            User.id.in_(
                select(distinct(QuizSession.user_id))
                .where(QuizSession.completed_at.isnot(None))
            )
        )
    )
    players_month_ago = players_month_ago_result.scalar() or 0

    churned_result = await session.execute(
        select(func.count())
        .select_from(last_quiz_subq)
        .join(User, User.id == last_quiz_subq.c.user_id)
        .where(
            User.created_at <= datetime.combine(month_ago, datetime.min.time()),
            last_quiz_subq.c.real_last_quiz < month_ago
        )
    )
    churned = churned_result.scalar() or 0
    churn_rate = (churned / players_month_ago * 100) if players_month_ago > 0 else 0

    # Два разных счётчика, которые раньше были свалены в один.
    # Прежний запрос считал «нет ЗАВЕРШЁННЫХ викторин», а подпись говорила
    # «ни разу не начали». Разница большая: в старых данных completed_at
    # часть времени не записывался, и счётчик был завышен вчетверо —
    # 104 вместо реальных 23.
    never_started_result = await session.execute(
        select(func.count())
        .select_from(User)
        .where(~User.id.in_(select(distinct(QuizSession.user_id))))
    )
    never_started = never_started_result.scalar() or 0

    started_never_finished_result = await session.execute(
        select(func.count())
        .select_from(User)
        .where(
            User.id.in_(select(distinct(QuizSession.user_id))),
            ~User.id.in_(
                select(distinct(QuizSession.user_id))
                .where(QuizSession.completed_at.isnot(None))
            ),
        )
    )
    started_never_finished = started_never_finished_result.scalar() or 0

    names_body = None
    if high_risk:
        lines = []
        for first_name, username, last_quiz in high_risk[:5]:
            name = first_name or (f"@{username}" if username else "—")
            days = f"{(today - last_quiz).days} дн." if last_quiz else "—"
            lines.append(f"{name:<20}{days:>8}")
        names_body = admin_ui.listing(lines)
        if high_risk_count > 5:
            names_body += f"\n<i>и ещё {high_risk_count - 5}</i>"

    names_block = admin_ui.section(
        "Кто пропал дольше всех", names_body, empty="таких нет",
    )

    text = admin_ui.screen(
        "Отток",
        lead=f"не заходят 7+ дней: {admin_ui.people(high_risk_count)}",
        blocks=[
            admin_ui.table([
                ("Молчат 7+ дней", high_risk_count),
                ("Молчат 3–7 дней", medium_risk_count),
                ("Ушли за 30 дней", f"{admin_ui.num(churned)} из "
                                    f"{admin_ui.num(players_month_ago)}"),
                ("  доля ушедших",
                 admin_ui.pct(churned, players_month_ago, digits=1)),
                ("Не начали ни разу", never_started),
                ("Начали и не кончили", started_never_finished),
            ]),
            ("<i>«ушли за 30 дней» — из тех, кто играл больше месяца назад, "
             "сколько не вернулось. «Начали и не кончили» — хотя бы один круг "
             "начат, ни один не завершён</i>"),
            names_block,
        ],
    )
    await callback.message.edit_text(
        text, reply_markup=admin_ui.kb(back="admin:people")
    )


# ============================================================================
# ЭКСПОРТ
# ============================================================================

@router.callback_query(F.data == "admin:export")
async def admin_export_menu(callback: CallbackQuery, session: AsyncSession):
    """Выгрузка в CSV. Экран говорит, что именно будет в файле."""
    if not await _guard(callback):
        return

    users = (await session.execute(select(func.count()).select_from(User))).scalar() or 0
    quizzes = (await session.execute(
        select(func.count()).select_from(QuizSession)
        .where(QuizSession.completed_at.isnot(None))
    )).scalar() or 0

    text = admin_ui.screen(
        "Выгрузка",
        lead="CSV в кодировке UTF-8, открывается в Excel",
        blocks=[
            admin_ui.table([
                ("Людей в файле", users),
                ("Занятий в файле", min(quizzes, EXPORT_QUIZ_LIMIT)),
            ]),
            (f"Люди {admin_ui.DOT} id, имя, язык, уровень, серия, круги, "
             f"выученные, напоминания\n"
             f"Занятия {admin_ui.DOT} последние {admin_ui.num(EXPORT_QUIZ_LIMIT)} "
             f"завершённых: время, язык, ответы, точность, дверь входа"),
        ],
    )
    keyboard = admin_ui.kb(
        [("Люди", "admin:export_users")],
        [("Занятия", "admin:export_quizzes")],
        back="admin:back",
    )
    await callback.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(F.data == "admin:export_users")
async def admin_export_users(callback: CallbackQuery, session: AsyncSession):
    if not is_admin(callback.from_user.id):
        await callback.answer("Доступа нет")
        return

    await callback.answer("Собираю файл")

    result = await session.execute(
        select(User).order_by(User.created_at.desc())
    )
    users = result.scalars().all()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        'ID', 'Username', 'First Name', 'Created At', 'Level',
        'Streak Days', 'Quizzes Passed', 'Words Learned',
        'Last Quiz Date', 'Interface Language', 'Timezone',
        'Notifications Enabled'
    ])

    for user in users:
        writer.writerow([
            user.id,
            user.username or '',
            user.first_name or '',
            user.created_at.strftime('%Y-%m-%d %H:%M:%S') if user.created_at else '',
            user.level.value if user.level else '',
            current_streak(user),
            user.quizzes_passed or 0,
            user.words_learned or 0,
            user.last_quiz_date.strftime('%Y-%m-%d') if user.last_quiz_date else '',
            user.interface_language or '',
            user.timezone or '',
            'Yes' if user.notifications_enabled else 'No'
        ])

    output.seek(0)
    csv_bytes = output.getvalue().encode('utf-8-sig')

    file = BufferedInputFile(csv_bytes, filename=f"users_{utctoday()}.csv")
    await callback.message.answer_document(
        file, caption=f"Люди {admin_ui.DOT} {admin_ui.num(len(users))} строк"
    )
    await callback.message.delete()


@router.callback_query(F.data == "admin:export_quizzes")
async def admin_export_quizzes(callback: CallbackQuery, session: AsyncSession):
    if not is_admin(callback.from_user.id):
        await callback.answer("Доступа нет")
        return

    await callback.answer("Собираю файл")

    result = await session.execute(
        select(QuizSession, User.username, User.first_name)
        .join(User, QuizSession.user_id == User.id)
        .where(QuizSession.completed_at.isnot(None))
        .order_by(QuizSession.started_at.desc())
        .limit(EXPORT_QUIZ_LIMIT)
    )
    quizzes = result.all()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        'Session ID', 'User ID', 'Name', 'Started At', 'Completed At',
        'Level', 'Total Questions', 'Correct Answers', 'Score %',
        'Start Source', 'Exit Reason', 'Exit At Question'
    ])

    for quiz, username, first_name in quizzes:
        score = quiz.accuracy_percent
        name = first_name or username or ''
        writer.writerow([
            quiz.id,
            quiz.user_id,
            name,
            quiz.started_at.strftime('%Y-%m-%d %H:%M:%S'),
            quiz.completed_at.strftime('%Y-%m-%d %H:%M:%S') if quiz.completed_at else '',
            quiz.level.value if quiz.level else '',
            quiz.answered_questions,
            quiz.correct_answers,
            f"{score:.1f}",
            quiz.start_source or '',
            quiz.exit_reason or '',
            quiz.exit_at_question
        ])

    output.seek(0)
    csv_bytes = output.getvalue().encode('utf-8-sig')

    file = BufferedInputFile(csv_bytes, filename=f"quizzes_{utctoday()}.csv")
    await callback.message.answer_document(
        file, caption=f"Занятия {admin_ui.DOT} {admin_ui.num(len(quizzes))} строк"
    )
    await callback.message.delete()


# ============================================================================
# ЛУЧШИЕ И КАРТОЧКА ЧЕЛОВЕКА
# ============================================================================

async def _build_top_people(session: AsyncSession, limit: int = TOP_PEOPLE) -> str:
    """
    Экран «Лучшие» и команда `/admin_users` собирают его ОДИН раз.

    Прежде это были две копии: экран брал 15 человек, команда — 20, и ряды
    у них отличались подписями. Номер места пишется числом: медали за
    второе и третье место были значками, которых устав не разрешает, а
    четвёртое и далее отмечались одной и той же булавкой — то есть значок
    не различал ничего.
    """
    users = (await session.execute(
        select(User)
        .where(User.quizzes_passed > 0)
        .order_by(User.quizzes_passed.desc(), User.words_learned.desc())
        .limit(limit)
    )).scalars().all()

    if not users:
        return admin_ui.screen(
            "Лучшие", lead="пока никто не прошёл ни круга",
        )

    # Через столбцы, а не руками: собранная вручную строка не влезала в
    # ширину телефона, и последний столбец обрезался многоточием
    rows = [
        (f"{place}. {_display_name(user)}",
         user.quizzes_passed or 0,
         user.words_learned or 0,
         user.best_streak_days or 0)
        for place, user in enumerate(users, 1)
    ]

    return admin_ui.screen(
        "Лучшие",
        lead=f"{admin_ui.people(len(users))} по пройденным кругам",
        blocks=[
            admin_ui.columns(rows),
            "<i>круги · выученные слова · лучшая серия</i>",
        ],
    )


@router.callback_query(F.data == "admin:top_users")
async def admin_top_users_callback(callback: CallbackQuery, session: AsyncSession):
    if not await _guard(callback):
        return

    text = await _build_top_people(session)
    await callback.message.edit_text(
        text, reply_markup=admin_ui.kb(back="admin:people")
    )


@router.callback_query(F.data == "admin:person_help")
async def admin_person_help(callback: CallbackQuery, session: AsyncSession):
    """
    Карточка человека открывается командой, и экран об этом говорит.

    Ввод id кнопками не наберёшь, а держать ради одного поля состояние FSM
    в админке — лишняя машинерия. Поэтому экран не притворяется, что умеет
    спросить, а показывает ровно то, что надо набрать.
    """
    if not await _guard(callback):
        return

    text = admin_ui.screen(
        "Человек",
        lead="карточка открывается командой",
        blocks=[
            "<pre>/admin_user 123456789\n/admin_user @имя</pre>",
            ("Внутри: настройки, напоминания, прогресс по словам на всех "
             "уровнях и на своём, круги, точность, двери входа и последние "
             "пять занятий."),
        ],
    )
    await callback.message.edit_text(
        text, reply_markup=admin_ui.kb(back="admin:people")
    )


# ============================================================================
# ДЕТАЛЬНАЯ СТАТИСТИКА
# ============================================================================

async def _build_words_screen(session: AsyncSession) -> str:
    """
    Слова: самые трудные и самые частые. Экран и `/admin_stats` — один код.

    Сортировка по ВЕРХНЕЙ границе Вильсона, а не по сырой доле верных: при
    пороге «больше 5 показов» список был почти целиком статистическим
    шумом — 3 из 8 это обычный разброс для слова, которое знают на 70%.
    Граница именно верхняя: слово трудное, если даже оптимистичная оценка
    низка. По нижней наверх полезло бы шумное 3/8 (нижняя 0.14) вместо
    по-настоящему трудного 13/28 (нижняя 0.30).
    """
    difficulty = difficulty_rank_sql(Word.times_correct, Word.times_shown)

    difficult = (await session.execute(
        select(Word.word_de, Word.article, Word.translation_ru,
               Word.times_shown, Word.times_correct)
        .select_from(Word)
        .where(Word.times_shown >= MIN_SHOWS_FOR_DIFFICULTY)
        .order_by(difficulty.asc())
        .limit(10)
    )).all()

    popular = (await session.execute(
        select(Word.word_de, Word.article, Word.times_shown)
        .select_from(Word)
        .order_by(Word.times_shown.desc())
        .limit(10)
    )).all()

    hard_rows = [
        (_full_word(word_de, article),
         f"{admin_ui.pct(correct, shown)} из {admin_ui.num(shown)}")
        for word_de, article, trans_ru, shown, correct in difficult
    ]
    popular_rows = [
        (_full_word(word_de, article), shown)
        for word_de, article, shown in popular
    ]

    return admin_ui.screen(
        "Слова",
        lead="что даётся труднее всего и что попадается чаще",
        blocks=[
            admin_ui.section(
                "Самые трудные",
                admin_ui.table(hard_rows),
                note=(f"не меньше {MIN_SHOWS_FOR_DIFFICULTY} показов, по "
                      f"верхней границе Вильсона — чтобы редкое слово с "
                      f"тремя промахами не обогнало по-настоящему трудное"),
                empty=f"ни одного слова с {MIN_SHOWS_FOR_DIFFICULTY}+ показами",
            ),
            admin_ui.section(
                "Самые частые",
                admin_ui.table(popular_rows),
                note="сколько раз слово попадалось в занятиях",
            ),
        ],
    )


@router.callback_query(F.data == "admin:words")
async def admin_words(callback: CallbackQuery, session: AsyncSession):
    if not await _guard(callback):
        return

    text = await _build_words_screen(session)
    await callback.message.edit_text(
        text, reply_markup=admin_ui.kb(back="admin:back")
    )


# ============================================================================
# РЕПОРТЫ ПЕРЕВОДОВ
# ============================================================================

# Баллов за подтверждённую жалобу. Число живёт в `MonthlyStats` рядом с
# остальными ценами, а здесь только читается: прежде оно было вписано сюда
# числом, а в шести локалях — ещё и словами («получишь +1 балл»), то есть в
# семи местах. Поправь одно — остальные соврут человеку в лицо.
REPORT_REWARD_POINTS = MonthlyStats.POINTS_PER_REPORT


def _voice_short_name(voice: str) -> str:
    """
    Понятная подпись голоса вместо «de-DE-KatjaNeural».

    Имена берутся из реестра озвучки, а не выписываются здесь: иначе они
    разъехались бы с тем, что видит пользователь в настройках.
    """
    from app.services.tts_voices import VOICES

    for lang, voices in VOICES.items():
        for item in voices:
            if item.name == voice:
                gender = "м" if item.gender == "male" else "ж"
                return f"{lang} {item.label} ({gender})"
    return voice


async def _build_reports_text_and_keyboard(session: AsyncSession) -> tuple:
    """Собрать текст и клавиатуру для страницы репортов"""
    from app.database.models import MonthlyStats

    # Топ-10 слов по количеству pending репортов.
    # Жалобы на текст и на озвучку считаются отдельно: это разные починки,
    # и по одному числу непонятно, что править — перевод или произношение.
    reports_result = await session.execute(
        select(
            Word.id,
            Word.word_de,
            Word.article,
            Word.level,
            Word.translation_ru,
            Word.translation_uk,
            func.count(TranslationReport.id).label('report_count'),
            func.count(
                case((TranslationReport.kind == 'audio', 1))
            ).label('audio_count'),
        )
        .join(TranslationReport, Word.id == TranslationReport.word_id)
        .where(TranslationReport.status == 'pending')
        .group_by(Word.id, Word.word_de, Word.article, Word.level,
                  Word.translation_ru, Word.translation_uk)
        .order_by(desc(func.count(TranslationReport.id)))
        .limit(10)
    )
    top_words = reports_result.all()

    # Общая статистика
    total_reports_result = await session.execute(
        select(func.count()).select_from(TranslationReport)
    )
    total_reports = total_reports_result.scalar() or 0

    pending_result = await session.execute(
        select(func.count()).select_from(TranslationReport)
        .where(TranslationReport.status == 'pending')
    )
    pending = pending_result.scalar() or 0

    unique_words_result = await session.execute(
        select(func.count(distinct(TranslationReport.word_id)))
        .select_from(TranslationReport)
        .where(TranslationReport.status == 'pending')
    )
    unique_words = unique_words_result.scalar() or 0

    unique_users_result = await session.execute(
        select(func.count(distinct(TranslationReport.user_id)))
        .select_from(TranslationReport)
    )
    unique_users = unique_users_result.scalar() or 0

    # Сколько баллов выдано за всё время
    fixed_count_result = await session.execute(
        select(func.count()).select_from(TranslationReport)
        .where(TranslationReport.status == 'fixed')
    )
    fixed_count = fixed_count_result.scalar() or 0

    # Разбивка по виду жалобы: перевод правится в базе, произношение —
    # пересборкой клипа, это разная работа
    by_kind_result = await session.execute(
        select(TranslationReport.kind, func.count())
        .where(TranslationReport.status == 'pending')
        .group_by(TranslationReport.kind)
    )
    by_kind = {kind or 'text': count for kind, count in by_kind_result.all()}

    # По каким голосам жалуются на произношение: если жалобы сошлись на одном
    # голосе, дело в голосе, а не в слове
    voices_result = await session.execute(
        select(TranslationReport.voice, func.count())
        .where(
            TranslationReport.status == 'pending',
            TranslationReport.kind == 'audio',
            TranslationReport.voice.isnot(None),
        )
        .group_by(TranslationReport.voice)
        .order_by(desc(func.count()))
        .limit(5)
    )
    top_voices = voices_result.all()

    counts_block = admin_ui.table([
        ("Ждут решения", pending),
        ("  на перевод", by_kind.get("text", 0)),
        ("  на произношение", by_kind.get("audio", 0)),
        ("Слов под жалобой", unique_words),
        ("Жаловались людей", unique_users),
        ("Приняли за всё время", fixed_count),
        ("Жалоб всего", total_reports),
    ])

    voices_block = None
    if top_voices:
        voices_block = admin_ui.section(
            "Жалобы на произношение по голосам",
            admin_ui.table([(_voice_short_name(voice), count)
                            for voice, count in top_voices]),
            note="если жалобы сошлись на одном голосе — дело в голосе, "
                 "а не в словах",
        )

    buttons: list[list[InlineKeyboardButton]] = []
    queue_block = None

    if top_words:
        lines = []
        for wid, word_de, article, level, trans_ru, trans_uk, count, audio_count in top_words:
            full_word = _full_word(word_de, article)
            trans = trans_ru or trans_uk or "—"
            # Видно, что именно править: перевод в базе или клип озвучки
            kinds = []
            if count - audio_count:
                kinds.append(f"перевод {count - audio_count}")
            if audio_count:
                kinds.append(f"звук {audio_count}")
            lines.append(f"{full_word} {admin_ui.DOT} {level.value} "
                         f"{admin_ui.DOT} {', '.join(kinds)}")
            lines.append(f"  {trans}")

            # Решение по слову: `✓` и `✗` — из разрешённого набора четырёх
            buttons.append([
                InlineKeyboardButton(
                    text=f"✓ {full_word}",
                    callback_data=f"admin:report_approve_{wid}",
                ),
                InlineKeyboardButton(
                    text="✗",
                    callback_data=f"admin:report_reject_{wid}",
                ),
            ])

        queue_block = admin_ui.section(
            "Разобрать",
            admin_ui.listing(lines),
            note=(f"✓ принять — все, кто жаловался, получат "
                  f"+{REPORT_REWARD_POINTS} "
                  f"{admin_ui.plural(REPORT_REWARD_POINTS, 'балл', 'балла', 'баллов')}"
                  f". ✗ отклонить — без баллов"),
        )

    text = admin_ui.screen(
        "Жалобы",
        lead=(f"{admin_ui.num(pending)} ждут решения"
              if pending else "решены все"),
        blocks=[counts_block, voices_block, queue_block],
    )

    buttons.append([InlineKeyboardButton(text="Назад", callback_data="admin:back")])
    return text, InlineKeyboardMarkup(inline_keyboard=buttons)


@router.callback_query(F.data == "admin:reports")
async def admin_reports(callback: CallbackQuery, session: AsyncSession):
    """Показать жалобы с кнопками решения"""
    if not await _guard(callback):
        return

    text, keyboard = await _build_reports_text_and_keyboard(session)
    await callback.message.edit_text(text, reply_markup=keyboard)


async def _reporter_lang(report: TranslationReport, session: AsyncSession) -> str:
    """
    КАКОЙ ЯЗЫК учил человек, когда жаловался.

    Нужно потому, что `monthly_stats` ведётся ОТДЕЛЬНО ПО ЯЗЫКАМ (тройная
    уникальность user + сезон + язык): учащие английский соревнуются с
    учащими английский. Балл, положенный не в тот ряд, в рейтинге человека
    не появится вовсе.

    Сперва спрашиваем занятие, из которого пришла жалоба: это язык, на
    котором ошибка и была замечена. Если занятие не сохранилось — берём
    текущий язык человека, тем же способом, которым его берёт сам рейтинг.
    """
    if report.quiz_session_id:
        quiz = await session.get(QuizSession, report.quiz_session_id)
        if quiz and quiz.learning_lang:
            return quiz.learning_lang

    user = await session.get(User, report.user_id)
    return pair_from_user(user).learning if user else "de"


async def _tell_reporter(
    callback: CallbackQuery, session: AsyncSession, report: TranslationReport,
    word_display: str,
) -> bool:
    """
    Сказать автору жалобы, что её приняли и балл начислен.

    БЕЗ ЭТОГО НАГРАДЫ НЕТ, сколько бы её ни начисляли. Бот обещает прямо в
    сообщении об отправке: «если ошибка подтвердится — получишь баллы», — а
    подтверждение проходило молча, и балл растворялся в общем счёте. То
    есть обещание выполнялось технически и не выполнялось по существу.

    Ошибка доставки не должна валить подтверждение: человек мог закрыть
    бота, и жалоба от этого хуже не стала.
    """
    from app.locales import DEFAULT_LOCALE, get_text

    user = await session.get(User, report.user_id)
    lang = (user.interface_language if user else None) or DEFAULT_LOCALE
    key = "report_approved_audio" if report.kind == "audio" else "report_approved"

    try:
        await callback.bot.send_message(
            report.user_id,
            get_text(key, lang, word=word_display, points=REPORT_REWARD_POINTS),
        )
        return True
    except Exception:
        logger.info(
            "не удалось известить автора жалобы (user=%s)", report.user_id,
            exc_info=True,
        )
        return False


@router.callback_query(F.data.startswith("admin:report_approve_"))
async def admin_report_approve(callback: CallbackQuery, session: AsyncSession):
    """Подтвердить жалобу → статус fixed, баллы автору, извещение автору."""
    if not is_admin(callback.from_user.id):
        await callback.answer("Доступа нет")
        return

    word_id = int(callback.data.replace("admin:report_approve_", ""))

    from app.services.monthly_leaderboard_service import get_or_create_current_season

    # Находим всех юзеров с pending репортами на это слово
    reports_result = await session.execute(
        select(TranslationReport)
        .where(
            TranslationReport.word_id == word_id,
            TranslationReport.status == 'pending'
        )
    )
    reports = reports_result.scalars().all()

    if not reports:
        await callback.answer("По этому слову нечего решать", show_alert=True)
        return

    # Получаем текущий сезон
    season = await get_or_create_current_season(session)

    rewarded_users = 0
    for report in reports:
        report.status = 'fixed'

        # ЯЗЫК ОБЯЗАТЕЛЕН, И ЭТО НЕ ПРИДИРКА.
        #
        # `monthly_stats` ведётся отдельно по языкам — тройная уникальность
        # user + сезон + язык. Прежний запрос спрашивал только user и сезон,
        # и давал две беды сразу: у двуязычного `scalar_one_or_none()`
        # ПАДАЛ с MultipleResultsFound прямо под рукой админа (жалобы
        # остались бы висеть), а при создании ряда язык брался из значения
        # по умолчанию — «de», — и балл за польскую ошибку ложился в
        # немецкий ряд, где человека в рейтинге нет.
        #
        # Сейчас у двух языков в одном сезоне ноль человек, то есть не
        # выстрелило ещё ни разу. Но язык в боте уже шесть, и ряд с «en»
        # в базе есть.
        learning_lang = await _reporter_lang(report, session)

        stat_result = await session.execute(
            select(MonthlyStats).where(
                MonthlyStats.user_id == report.user_id,
                MonthlyStats.season_id == season.id,
                MonthlyStats.learning_lang == learning_lang,
            )
        )
        stat = stat_result.scalar_one_or_none()

        if stat:
            stat.report_bonus = (stat.report_bonus or 0) + REPORT_REWARD_POINTS
            stat.monthly_score = stat.calculate_monthly_score()
        else:
            # Ряда нет — человек жаловался, но в этом месяце не играл
            stat = MonthlyStats(
                user_id=report.user_id,
                season_id=season.id,
                learning_lang=learning_lang,
                report_bonus=REPORT_REWARD_POINTS,
                monthly_score=REPORT_REWARD_POINTS,
            )
            session.add(stat)

        rewarded_users += 1

    # Подтверждённая жалоба на произношение означает, что клип негодный.
    # Без сброса кэша он остался бы в Telegram навсегда: file_id живёт вечно,
    # и пересобрать озвучку было бы нечем.
    audio_kinds = {r.kind for r in reports}
    dropped_clips = 0
    if 'audio' in audio_kinds:
        dropped = await session.execute(
            sql_text("DELETE FROM word_audio WHERE word_id = :wid"),
            {"wid": word_id},
        )
        dropped_clips = dropped.rowcount or 0

    await session.commit()

    # Получаем слово для лога
    word = await session.get(Word, word_id)
    word_display = (_full_word(word.word_de, word.article)
                    if word else str(word_id))

    logger.info(f"Admin approved report for word '{word_display}' (id={word_id}), rewarded {rewarded_users} users with +{REPORT_REWARD_POINTS}")

    if dropped_clips:
        logger.info(
            "Сброшено клипов озвучки для слова %s: %d — пересоберутся при "
            "следующем показе", word_id, dropped_clips,
        )

    # ИЗВЕСТИТЬ АВТОРОВ — после коммита, чтобы ничего не обещать прежде,
    # чем начислено. Шлётся каждому пожаловавшемуся на своём языке
    told = 0
    for report in reports:
        if await _tell_reporter(callback, session, report, word_display):
            told += 1

    await callback.answer(
        f"✓ {word_display} — принято\n"
        f"балла получили {rewarded_users}, извещено {told}"
        + (f"\nозвучка сброшена ({dropped_clips} клипов), пересоберётся"
           if dropped_clips else ""),
        show_alert=True
    )

    # Обновляем страницу репортов
    text, keyboard = await _build_reports_text_and_keyboard(session)
    try:
        await callback.message.edit_text(text, reply_markup=keyboard)
    except Exception:
        pass


@router.callback_query(F.data.startswith("admin:report_reject_"))
async def admin_report_reject(callback: CallbackQuery, session: AsyncSession):
    """Отклонить репорт → статус rejected, баллы не начисляются"""
    if not is_admin(callback.from_user.id):
        await callback.answer("Доступа нет")
        return

    word_id = int(callback.data.replace("admin:report_reject_", ""))

    # Находим все pending репорты на это слово
    reports_result = await session.execute(
        select(TranslationReport)
        .where(
            TranslationReport.word_id == word_id,
            TranslationReport.status == 'pending'
        )
    )
    reports = reports_result.scalars().all()

    if not reports:
        await callback.answer("По этому слову нечего решать", show_alert=True)
        return

    rejected_count = 0
    for report in reports:
        report.status = 'rejected'
        rejected_count += 1

    await session.commit()

    word = await session.get(Word, word_id)
    word_display = (_full_word(word.word_de, word.article)
                    if word else str(word_id))

    logger.info(f"Admin rejected report for word '{word_display}' (id={word_id}), {rejected_count} reports")

    await callback.answer(
        f"✗ {word_display} — отклонено ({rejected_count} жалоб)",
        show_alert=True
    )

    # Обновляем страницу репортов
    text, keyboard = await _build_reports_text_and_keyboard(session)
    try:
        await callback.message.edit_text(text, reply_markup=keyboard)
    except Exception:
        pass


# ============================================================================
# НАЗАД
# ============================================================================

@router.callback_query(F.data == "admin:back")
async def admin_back(callback: CallbackQuery, session: AsyncSession):
    """Возврат на главную. Отказ здесь прежде не отправлялся вовсе."""
    if not await _guard(callback):
        return

    text = await _get_main_stats(session)
    await callback.message.edit_text(text, reply_markup=get_admin_keyboard())


# ============================================================================
# СТАРЫЕ КОМАНДЫ (совместимость)
# ============================================================================

@router.message(Command("admin_users"))
async def admin_users(message: Message, session: AsyncSession):
    if not is_admin(message.from_user.id):
        return

    try:
        await message.delete()
    except Exception:
        pass

    # Тот же сборщик, что у экрана «Лучшие»: прежде это были две копии
    # одного кода на 15 и на 20 человек, и ряды у них отличались подписями
    await message.answer(await _build_top_people(session, 20))


@router.message(Command("admin_stats"))
async def admin_detailed_stats(message: Message, session: AsyncSession):
    """То же, что экран «Слова», но командой: сборщик один."""
    if not is_admin(message.from_user.id):
        return

    try:
        await message.delete()
    except Exception:
        pass

    await message.answer(await _build_words_screen(session))


@router.message(Command("admin_user"))
async def admin_user_details(message: Message, session: AsyncSession):
    """
    Карточка человека: настройки, напоминания, прогресс, последние занятия.

    ПАДЕНИЕ, КОТОРОЕ ТУТ БЫЛО. Блок уровня собирался как
    `f"Уровень {user.level.value}"` без проверки на пустоту, хотя блок
    настройками выше ту же колонку проверял. Людей без уровня в базе сейчас
    ноль, так что падения никто не видел, — но новый человек до конца
    знакомства именно такой, и карточка на нём валилась бы с AttributeError.
    """
    if not is_admin(message.from_user.id):
        return

    try:
        await message.delete()
    except Exception:
        pass

    parts = (message.text or "").split(maxsplit=1)
    if len(parts) < 2:
        await message.answer(admin_ui.screen(
            "Человек",
            lead="нужен id или имя",
            blocks=["<pre>/admin_user 123456789\n/admin_user @имя</pre>"],
        ))
        return

    identifier = parts[1].strip().lstrip("@")

    if identifier.isdigit():
        found = await session.execute(select(User).where(User.id == int(identifier)))
    else:
        found = await session.execute(
            select(User).where(func.lower(User.username) == identifier.lower())
        )
    user = found.scalar_one_or_none()

    if not user:
        await message.answer("Такого человека нет")
        return

    pair = pair_from_user(user)
    overall = await get_user_progress_stats(user.id, session, pair)
    level_progress = (
        await get_user_progress_stats(user.id, session, pair, level=user.level)
        if user.level else None
    )

    rounds = (await session.execute(
        select(QuizSession)
        .where(QuizSession.user_id == user.id,
               QuizSession.completed_at.isnot(None))
        .order_by(QuizSession.started_at.desc())
    )).scalars().all()

    answered = sum(r.answered_questions for r in rounds)
    # По фактически отвеченным, а не по плановым: брошенные занятия иначе
    # выглядят сплошными ошибками и занижают точность на ~27 п.п.
    correct = sum(r.correct_answers for r in rounds)
    best = max((r.accuracy_percent for r in rounds), default=0)

    avg_answer = (await session.execute(
        select(func.avg(QuizQuestion.response_time_seconds))
        .select_from(QuizQuestion)
        .join(QuizSession, QuizQuestion.session_id == QuizSession.id)
        .where(QuizSession.user_id == user.id,
               QuizQuestion.response_time_seconds.isnot(None))
    )).scalar() or 0

    # Двери входа — подписями из одного источника, а не сырыми пометками:
    # прежде здесь выводилось «menu: 3, again: 1»
    from app.bot.handlers.quiz.game import source_label

    doors = (await session.execute(
        select(QuizSession.start_source, func.count())
        .where(QuizSession.user_id == user.id,
               QuizSession.start_source.isnot(None))
        .group_by(QuizSession.start_source)
        .order_by(func.count().desc())
    )).all()

    channels = user.quiz_channels or "t"
    ways = ", ".join(filter(None, [
        "карточка" if "t" in channels else None,
        "слух" if "a" in channels else None,
        "речь" if "s" in channels else None,
    ])) or "—"

    def progress_rows(stats: dict) -> list[tuple[str, object]]:
        return [
            ("Выучено", stats["learned_words"]),
            ("В работе", stats["seen_words"] - stats["learned_words"]),
            ("Трудные", stats["struggling_words"]),
            ("Не начаты", stats["new_words"]),
        ]

    blocks = [
        admin_ui.table([
            ("id", str(user.id)),
            ("Имя в боте", f"@{user.username}" if user.username else "—"),
            ("Пришёл", user.created_at.strftime("%d.%m.%Y")
                       if user.created_at else "—"),
            ("Учит", _lang_name(pair.learning)),
            ("Значения на", _lang_name(pair.native)),
            ("Уровень", user.level.value if user.level else "не выбран"),
            ("Бот на языке", _lang_name(user.interface_language)),
            ("Часовой пояс", user.timezone or "Europe/Berlin"),
        ]),
        # «Способы» — строкой, а не рядом таблицы: значение из трёх слов
        # съедало ширину подписей, и соседние ряды обрезались в «Доска в кр…»
        admin_ui.section("Состав занятия", admin_ui.table([
            ("Доска в круге", "да" if user.match_in_round else "нет"),
            ("Слов в круге", user.quiz_word_count or "—"),
            ("Озвучка", "включена" if user.audio_enabled else "выключена"),
        ]) + f"\nСпособы {admin_ui.DOT} {ways}"),
        admin_ui.section("Напоминания", admin_ui.table([
            ("Включены", "да" if user.notifications_enabled else "нет"),
            ("Время", user.notification_time or "—"),
            ("Дней в неделю",
             f"{len(user.notification_days) if user.notification_days else 0} из 7"),
        ])),
        admin_ui.section("Занятия", admin_ui.table([
            ("Кругов пройдено", len(rounds)),
            ("Ответов", answered),
            ("Точность", admin_ui.pct(correct, answered, digits=1)),
            ("Лучший круг", f"{round(best)}%"),
            ("Серия дней", current_streak(user)),
            ("Лучшая серия", user.best_streak_days or 0),
            ("Последний круг", str(user.last_quiz_date or "—")),
            ("Ответ в среднем", f"{admin_ui.num(float(avg_answer))} сек"),
        ])),
        admin_ui.section(
            "Слова на всех уровнях", admin_ui.table(progress_rows(overall))
        ),
    ]

    if level_progress:
        blocks.append(admin_ui.section(
            f"Слова на уровне {user.level.value}",
            admin_ui.table(progress_rows(level_progress)),
        ))

    blocks.append(admin_ui.section(
        "Откуда входит",
        admin_ui.table([(source_label(door), n) for door, n in doors]),
        empty="пометок нет: они появились 13 октября",
    ))

    blocks.append(admin_ui.section(
        "Последние занятия",
        admin_ui.listing([
            f"{r.started_at.strftime('%d.%m %H:%M')} {r.learning_lang} "
            f"{r.level.value if r.level else '—'} "
            f"{r.correct_answers}/{r.answered_questions}"
            for r in rounds[:5]
        ]),
        empty="ни одного завершённого",
    ))

    await message.answer(admin_ui.screen(
        _display_name(user),
        lead=(f"{admin_ui.num(len(rounds))} кругов "
              f"{admin_ui.DOT} точность {admin_ui.pct(correct, answered)}"),
        blocks=blocks,
    ))



@router.message(Command("broadcast"))
async def broadcast_message(message: Message, session: AsyncSession):
    if not is_admin(message.from_user.id):
        return

    parts = (message.text or "").split(maxsplit=1)
    if len(parts) < 2:
        await message.answer(
            "Как пользоваться:\n"
            "<pre>/broadcast текст сообщения</pre>"
        )
        return

    broadcast_text = parts[1]

    # Бот отправляет всё с parse_mode=HTML. Любой символ < в тексте рассылки
    # Telegram считает началом тега и отклоняет сообщение — для КАЖДОГО
    # получателя. Раньше это означало «Ошибок: 232» без объяснения причины.
    # Поэтому разметку проверяем заранее: предпросмотр уходит самому админу
    # ровно тем же вызовом, каким пойдёт рассылка.
    try:
        await message.bot.send_message(message.from_user.id, broadcast_text)
    except Exception as exc:
        if "parse entities" in str(exc):
            await message.answer(
                "<b>Текст не проходит разметку HTML</b>\n\n"
                f"<code>{str(exc)[:200]}</code>\n\n"
                "Такое сообщение не дойдёт ни до кого. Символы &lt; и &gt; нужно "
                "писать как <code>&amp;lt;</code> и <code>&amp;gt;</code>, "
                "а теги — закрывать."
            )
        else:
            await message.answer(f"Предпросмотр не ушёл: {exc}")
        return

    count_result = await session.execute(select(func.count()).select_from(User))
    recipients = count_result.scalar() or 0

    _PENDING_BROADCASTS[message.from_user.id] = broadcast_text

    confirm = admin_ui.kb(
        [(f"Отправить {admin_ui.people(recipients)}", "admin:broadcast_confirm")],
        [("Отмена", "admin:broadcast_cancel")],
    )

    await message.answer(
        admin_ui.screen(
            "Рассылка",
            lead="предпросмотр выше — ровно то, что получат люди",
            blocks=[admin_ui.table([
                ("Получателей", recipients),
                ("Разметка", "проверена"),
            ])],
        ),
        reply_markup=confirm,
    )


# Текст ждёт подтверждения. В памяти процесса: рассылка — операция на минуты,
# переживать рестарт ей не нужно, а неотправленный черновик после рестарта
# лучше потерять, чем отправить неожиданно.
_PENDING_BROADCASTS: dict[int, str] = {}

# Telegram ограничивает бота примерно 30 сообщениями в секунду.
BROADCAST_CHUNK = 25
BROADCAST_PAUSE = 1.0


@router.callback_query(F.data == "admin:broadcast_cancel")
async def broadcast_cancel(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("Доступа нет")
        return

    _PENDING_BROADCASTS.pop(callback.from_user.id, None)
    await callback.answer("Отменено")
    await callback.message.edit_text("Рассылка отменена")


@router.callback_query(F.data == "admin:broadcast_confirm")
async def broadcast_confirm(callback: CallbackQuery, session: AsyncSession):
    if not is_admin(callback.from_user.id):
        await callback.answer("Доступа нет")
        return

    broadcast_text = _PENDING_BROADCASTS.pop(callback.from_user.id, None)
    if not broadcast_text:
        await callback.answer("Текст не найден — отправь /broadcast заново", show_alert=True)
        return

    await callback.answer()
    await callback.message.edit_text("Рассылка пошла")

    result = await session.execute(select(User.id))
    user_ids = [row[0] for row in result.all()]

    success = 0
    blocked = 0
    failed = 0

    for index, user_id in enumerate(user_ids):
        try:
            await callback.bot.send_message(user_id, broadcast_text)
            success += 1
        except Exception as exc:
            # Заблокировавшие бота — это норма, а не сбой рассылки
            if "blocked" in str(exc).lower() or "deactivated" in str(exc).lower():
                blocked += 1
            else:
                failed += 1
                logger.warning("Рассылка: не доставлено %s: %s", user_id, exc)

        if (index + 1) % BROADCAST_CHUNK == 0:
            await asyncio.sleep(BROADCAST_PAUSE)

    await callback.message.edit_text(admin_ui.screen(
        "Рассылка разослана",
        blocks=[admin_ui.table([
            ("Доставлено", success),
            ("Заблокировали бота", blocked),
            ("Прочие ошибки", failed),
        ])],
    ))