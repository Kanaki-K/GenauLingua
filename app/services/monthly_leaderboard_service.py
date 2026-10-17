"""
Сервис для месячной системы рейтинга

Файл: app/services/monthly_leaderboard_service.py
"""

from sqlalchemy import select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.enums import counted_channels
from app.database.models import (
    User, MonthlySeason, MonthlyStats, MonthlyQuizEvent, MonthlyAward, WinStreak,
    QuizQuestion, QuizSession, UserWord
)
from app.services.language_service import DEFAULT_LEARNING_LANG, pair_from_user
from typing import List, Dict, Optional
from datetime import datetime, date, timedelta
from app.core.clock import utcnow, utctoday
from app.services.streak_service import next_streak, user_day
import calendar

import logging

logger = logging.getLogger(__name__)


# ============================================================================
# КРУГ-ПОВТОР В МЕСЯЧНЫЙ ЗАЧЁТ НЕ ИДЁТ
# ============================================================================

# Чем помечен круг-повтор ошибок в `quiz_sessions.quiz_mode`. Колонка там
# строковая и держит сразу две вещи: настоящий режим человека («level»,
# «category») и вот эту пометку. Разделять их сейчас незачем — но знать о
# том, что они в одной колонке, обязательно.
REPEAT_QUIZ_MODE = "error_repeat"

# «ВСЕ ЯЗЫКИ» вместо кода языка (владелец, 17.10): «за месяц со всеми, за всё
# время со всеми и язык — с теми, кто учит тоже английский». Месяц и всё
# время теперь общие, по языку — отдельная вкладка. Баллы человека по
# разным языкам складываются. Награды месяца по-прежнему выдаются по языкам
# (`finalize_season`) — их и показывает вкладка языка
ALL_LANGS = "*"


def scored_sessions_filter():
    """
    Условие «это занятие идёт в месячный зачёт».

    ЗАЧЕМ ОДНОЙ ФУНКЦИЕЙ. Месячный балл считается ДВУМЯ путями: обычно
    инкрементом по одному занятию, а при сбое — полным пересчётом за месяц.
    Повтор ошибок не платит по первому пути (вызывающий его просто не зовёт)
    — и ПЛАТИЛ по второму, потому что пересчёт брал все завершённые занятия
    без отбора. Расхождение тихое и дорогое: замер по рабочей копии дал 314
    завершённых повторов у 25 человек на 986 верных ответов, то есть
    пересчёт раздал бы им 314 × 10 баллов за круги плюс сами ответы —
    порядка четырёх тысяч баллов из ничего. И выстрелило бы это не по
    команде, а само: пересчёт включается, когда круг закрылся на границе
    месяца или занятие не нашлось.

    Платить повтору нельзя по сути: тогда выгодно ошибаться нарочно —
    провалил круг, повторил, получил ещё десять баллов за круг.

    ПРО ПУСТОЕ ЗНАЧЕНИЕ. Проверка написана через `is_(None)` НАРОЧНО.
    Короткое `quiz_mode != REPEAT_QUIZ_MODE` выглядит тем же самым, но в SQL
    сравнение с NULL даёт NULL, а не истину, — и 1 069 занятий со старым
    пустым режимом (14 930 верных ответов) вылетели бы из пересчёта молча.
    Это была бы ровно та же беда с другим знаком.
    """
    return or_(
        QuizSession.quiz_mode.is_(None),
        QuizSession.quiz_mode != REPEAT_QUIZ_MODE,
    )


def counts_for_score(quiz: QuizSession) -> bool:
    """То же правило для одного занятия — для инкрементального пути."""
    return (quiz.quiz_mode or "") != REPEAT_QUIZ_MODE


# ============================================================================
# УПРАВЛЕНИЕ СЕЗОНАМИ
# ============================================================================

async def get_current_season(session: AsyncSession) -> Optional[MonthlySeason]:
    """Получить текущий активный сезон"""
    result = await session.execute(
        select(MonthlySeason)
        .where(MonthlySeason.is_active == True)
        .order_by(MonthlySeason.created_at.desc())
    )
    return result.scalar_one_or_none()


async def create_new_season(year: int, month: int, session: AsyncSession) -> MonthlySeason:
    """Создать новый месячный сезон"""
    existing = await session.execute(
        select(MonthlySeason).where(
            MonthlySeason.year == year,
            MonthlySeason.month == month
        )
    )
    # scalar_one_or_none() нельзя вызывать дважды: Result исчерпывается первым
    # вызовом, и повторный падал с ResourceClosedError вместо возврата сезона
    existing_season = existing.scalar_one_or_none()
    if existing_season:
        logger.warning(f"Сезон {month}/{year} уже существует")
        return existing_season

    start_date = date(year, month, 1)
    last_day = calendar.monthrange(year, month)[1]
    end_date = date(year, month, last_day)

    prev_seasons = await session.execute(
        select(MonthlySeason).where(MonthlySeason.is_active == True)
    )
    for prev in prev_seasons.scalars():
        prev.is_active = False

    season = MonthlySeason(
        year=year,
        month=month,
        start_date=start_date,
        end_date=end_date,
        is_active=True,
        winners_finalized=False
    )
    session.add(season)
    await session.commit()
    await session.refresh(season)

    logger.info(f"Создан новый сезон: {month}/{year} (id={season.id})")
    return season


async def get_or_create_current_season(session: AsyncSession) -> MonthlySeason:
    """Получить текущий сезон или создать если нет"""
    season = await get_current_season(session)
    if not season:
        today = utctoday()
        season = await create_new_season(today.year, today.month, session)
    return season


# ============================================================================
# ОБНОВЛЕНИЕ МЕСЯЧНОЙ СТАТИСТИКИ
# ============================================================================

async def _recalc_monthly_stats_full(
    user_id: int,
    session: AsyncSession,
    learning_lang: Optional[str] = None,
) -> MonthlyStats:
    """Полный пересчёт (медленно). Оставлено для отладки/миграций."""
    season = await get_or_create_current_season(session)

    if learning_lang is None:
        learning_lang = await _user_learning_lang(user_id, session)

    result = await session.execute(
        select(MonthlyStats).where(
            MonthlyStats.user_id == user_id,
            MonthlyStats.season_id == season.id,
            MonthlyStats.learning_lang == learning_lang,
        )
    )
    monthly_stat = result.scalar_one_or_none()
    if not monthly_stat:
        monthly_stat = MonthlyStats(
            user_id=user_id, season_id=season.id, learning_lang=learning_lang
        )
        session.add(monthly_stat)

    quizzes_result = await session.execute(
        select(QuizSession).where(
            QuizSession.user_id == user_id,
            QuizSession.learning_lang == learning_lang,
            QuizSession.completed_at.isnot(None),
            # Сезону занятие принадлежит по ЗАВЕРШЕНИЮ — так его относит
            # инкрементальный путь. Прежде здесь стояло начало, и круг,
            # начатый 30-го в 23:58 и законченный 1-го, инкремент клал в
            # новый сезон, а пересчёт — в старый: один круг, два хозяина
            QuizSession.completed_at >= datetime.combine(season.start_date, datetime.min.time()),
            QuizSession.completed_at <= datetime.combine(season.end_date, datetime.max.time()),
            # Повтор ошибок в зачёт не идёт — тем же условием, что и у
            # инкрементального пути. Разбор — у `scored_sessions_filter`
            scored_sessions_filter(),
        )
    )
    month_quizzes = quizzes_result.scalars().all()

    monthly_stat.monthly_quizzes = len(month_quizzes)
    # Прежде направление определялось сравнением translation_mode.value со
    # строками в нижнем регистре, тогда как значения enum в верхнем — условие
    # не выполнялось никогда, и бонус за обратный режим не начислялся вообще.
    # Плюс пары с английским и турецким там не были перечислены.
    monthly_stat.monthly_reverse = sum(1 for q in month_quizzes if q.is_reverse)

    total_correct = sum(q.correct_answers for q in month_quizzes)
    # Точность — по фактически отвеченным вопросам, а не по плановым
    total_questions = sum(q.answered_questions for q in month_quizzes)
    monthly_stat.total_correct = total_correct
    monthly_stat.total_questions = total_questions
    monthly_stat.monthly_avg_percent = int((total_correct / total_questions * 100) if total_questions > 0 else 0)

    # Верные ответы по каналам: за слух и речь платят больше, чем за текст.
    # Текстовый канал не считается — он выводится вычитанием из total_correct.
    by_channel = await _correct_by_channel(
        session, [q.id for q in month_quizzes]
    )
    # Все каналы со своими колонками — правилом (`counted_channels`):
    # забытый здесь канал в балле стал бы карточкой, вычитанием
    for channel in counted_channels():
        setattr(monthly_stat, f"correct_{channel.key}",
                by_channel.get(channel.value, 0))

    monthly_stat.monthly_words = await month_words(
        session, user_id, learning_lang, season
    )

    user = await session.get(User, user_id)
    monthly_stat.monthly_streak, monthly_stat.last_quiz_date = month_streak(
        user, month_quizzes
    )

    monthly_stat.monthly_score = monthly_stat.calculate_monthly_score()
    monthly_stat.updated_at = utcnow()

    await session.commit()
    await session.refresh(monthly_stat)
    return monthly_stat


async def month_words(
    session: AsyncSession, user_id: int, learning_lang: str, season,
) -> int:
    """
    Сколько слов человек выучил в этом сезоне — за них «+3 за слово».

    ОДНО ПРАВИЛО НА ТРИ ПУТИ: инкремент занятия, полный пересчёт и починка
    (`repair_accounting`) зовут эту функцию, а не пишут запрос заново.

    СЧИТАЕТСЯ ПО ДАТЕ ПЕРЕХОДА В «ВЫУЧЕНО» (`learned_at`), а не по
    последнему показу. Прежде слово, выученное в сентябре и повторённое по
    расписанию в октябре, оплачивалось в обоих месяцах, а «за всё время»
    (сумма месяцев) брало его дважды; к тому же починка закрытых сезонов
    дала бы им другие числа — последний показ с тех пор уехал вперёд.
    """
    start = datetime.combine(season.start_date, datetime.min.time())
    end = datetime.combine(season.end_date, datetime.max.time())
    return int((await session.execute(
        select(func.count()).select_from(UserWord).where(
            UserWord.user_id == user_id,
            UserWord.learning_lang == learning_lang,
            UserWord.learned.is_(True),
            UserWord.learned_at >= start,
            UserWord.learned_at <= end,
        )
    )).scalar() or 0)


async def _user_learning_lang(user_id: int, session: AsyncSession) -> str:
    """Изучаемый язык пользователя — измерение месячного рейтинга."""
    user = await session.get(User, user_id)
    return pair_from_user(user).learning if user else DEFAULT_LEARNING_LANG


async def _correct_by_channel(
    session: AsyncSession, quiz_session_ids: list[int]
) -> dict[str, int]:
    """
    Сколько верных ответов дано каждым каналом в этих занятиях.

    Считается в базе, а не перебором в Python: у активного пользователя за
    месяц набирается несколько сотен вопросов, и тянуть их строками ради
    двух чисел незачем.

    Текстовый канал здесь НЕ возвращается, и это не упущение: у вопросов,
    заданных до появления каналов, колонка пуста, и считать их отдельно
    значило бы потерять. Текст выводится вычитанием из total_correct —
    тогда и пустые, и явные «t» попадают в него одинаково верно.
    """
    if not quiz_session_ids:
        return {}

    rows = await session.execute(
        select(QuizQuestion.channel, func.count())
        .where(
            QuizQuestion.session_id.in_(quiz_session_ids),
            QuizQuestion.is_correct.is_(True),
            QuizQuestion.channel.isnot(None),
        )
        .group_by(QuizQuestion.channel)
    )
    return {channel: count for channel, count in rows.all()}


async def update_monthly_stats(
        user_id: int,
        session: AsyncSession,
        quiz_session_id: Optional[int] = None,
        force_full_recalc: bool = False
) -> MonthlyStats:
    """
    Инкрементально обновить статистику пользователя за текущий месяц.
    Идемпотентно через monthly_quiz_events.

    Рейтинг ведётся отдельно по каждому изучаемому языку: учащие английский
    соревнуются с учащими английский.
    """
    if force_full_recalc or quiz_session_id is None:
        return await _recalc_monthly_stats_full(user_id, session)

    quiz = await session.get(QuizSession, quiz_session_id)
    if not quiz or quiz.user_id != user_id:
        return await _recalc_monthly_stats_full(user_id, session)

    if quiz.completed_at is None:
        return await _recalc_monthly_stats_full(user_id, session, quiz.learning_lang)

    quiz_dt = quiz.completed_at or quiz.started_at
    quiz_date = quiz_dt.date()

    # СЕЗОН — ПО ДАТЕ КРУГА, а не «какой сейчас активен».
    #
    # Смена сезона идёт по расписанию в 00:05 UTC первого числа (а если бот
    # был выключен — в ближайшие :30). Круг, законченный в эти минуты, прежде
    # не попадал в активный сезон, уходил в полный пересчёт СТАРОГО сезона,
    # где по дате тоже не числился, — и не засчитывался нигде, никогда.
    # Теперь новый сезон открывается здесь же; старый закроет страховочная
    # проверка (`finalize_pending_seasons`), награды от этого не теряются.
    season = await get_or_create_current_season(session)
    if quiz_date > season.end_date:
        season = await create_new_season(quiz_date.year, quiz_date.month, session)
    if not (season.start_date <= quiz_date <= season.end_date):
        return await _recalc_monthly_stats_full(user_id, session, quiz.learning_lang)

    learning_lang = quiz.learning_lang or DEFAULT_LEARNING_LANG

    stat_result = await session.execute(
        select(MonthlyStats).where(
            MonthlyStats.user_id == user_id,
            MonthlyStats.season_id == season.id,
            MonthlyStats.learning_lang == learning_lang,
        )
    )
    monthly_stat = stat_result.scalar_one_or_none()
    if not monthly_stat:
        monthly_stat = MonthlyStats(
            user_id=user_id, season_id=season.id, learning_lang=learning_lang
        )
        session.add(monthly_stat)
        await session.flush()

    # КРУГ-ПОВТОР НЕ ПЛАТИТ, и правило стоит ЗДЕСЬ, а не только у
    # вызывающего. `_finish_quiz` повтор и так не передаёт, но держать такое
    # решение в обработчике значит ждать, когда следующий вызов его забудет.
    # Статистика возвращается нетронутой: это не ошибка, а «нечего считать».
    #
    # Отметка о событии тоже НЕ ставится: она служит идемпотентности, а
    # ставить её для занятия, которое ничего не прибавило, значит соврать
    # будущему пересчёту о том, что оно учтено.
    if not counts_for_score(quiz):
        return monthly_stat

    # Идемпотентность
    event_result = await session.execute(
        select(MonthlyQuizEvent).where(MonthlyQuizEvent.quiz_session_id == quiz_session_id)
    )
    if event_result.scalar_one_or_none():
        return monthly_stat

    session.add(MonthlyQuizEvent(
        quiz_session_id=quiz_session_id,
        user_id=user_id,
        season_id=season.id
    ))

    monthly_stat.monthly_quizzes = (monthly_stat.monthly_quizzes or 0) + 1

    # Направление берём из флага сессии. Прежнее сравнение
    # translation_mode.value со строками в нижнем регистре не срабатывало
    # никогда — значения enum в верхнем регистре, — поэтому бонус за
    # обратный режим не начислялся ни одному пользователю.
    if quiz.is_reverse:
        monthly_stat.monthly_reverse = (monthly_stat.monthly_reverse or 0) + 1

    monthly_stat.total_correct = (monthly_stat.total_correct or 0) + (quiz.correct_answers or 0)
    # Фактически отвеченные, а не плановые: иначе брошенные викторины
    # занижают средний процент и срезают бонусы за точность
    monthly_stat.total_questions = (monthly_stat.total_questions or 0) + (quiz.answered_questions or 0)
    if monthly_stat.total_questions > 0:
        monthly_stat.monthly_avg_percent = int((monthly_stat.total_correct / monthly_stat.total_questions) * 100)
    else:
        monthly_stat.monthly_avg_percent = 0

    by_channel = await _correct_by_channel(session, [quiz.id])
    # Тем же правилом, что полный пересчёт выше: два пути учёта с разными
    # списками каналов разошлись бы на первом же новом
    for channel in counted_channels():
        column = f"correct_{channel.key}"
        setattr(monthly_stat, column,
                (getattr(monthly_stat, column) or 0) + by_channel.get(channel.value, 0))

    # Серия месяца — в ДНЯХ ЧЕЛОВЕКА и по тому же правилу, что серия на
    # домашнем экране (`streak_service.next_streak`). Прежде здесь было своё
    # правило по UTC — вторая копия, которая разошлась бы с первой при
    # первой же правке.
    user = await session.get(User, user_id)
    day = user_day(user, quiz_dt)
    monthly_stat.monthly_streak = next_streak(
        monthly_stat.monthly_streak, monthly_stat.last_quiz_date, day
    )
    monthly_stat.last_quiz_date = day

    # СЛОВА — НА КАЖДОМ ЗАНЯТИИ. Прежде пересчёт шёл, только когда число
    # было нулём или занятий набиралось кратно десяти: замер 14 октября —
    # после второго занятия выучено 6 слов, записано 2, балл 55 вместо 67.
    # Итог занятия занижал «+N», десятое занятие прыгало разом, а слова
    # последних (до девяти) занятий месяца не попадали никуда — сезон
    # закрывался раньше пересчёта. Это один COUNT по индексу
    monthly_stat.monthly_words = await month_words(
        session, user_id, learning_lang, season
    )

    monthly_stat.monthly_score = monthly_stat.calculate_monthly_score()
    monthly_stat.updated_at = utcnow()

    await session.commit()
    await session.refresh(monthly_stat)
    return monthly_stat


def month_streak(user, month_quizzes: list) -> tuple[int, Optional[date]]:
    """
    Серия месяца и последний её день — по завершённым кругам сезона.

    ТО ЖЕ, ЧТО ДАЁТ ИНКРЕМЕНТ, и это главное. Прежняя редакция считала
    другое: череду, оканчивающуюся СЕГОДНЯ, по дням НАЧАЛА круга и по UTC.
    Инкремент же ведёт череду, оканчивающуюся последним днём занятий, по
    дням завершения. Два пути к одному числу давали два числа: человек,
    вчера закончивший пятый день подряд, имел 5 по инкременту и 0 по
    пересчёту — до того, как сегодня сядет заниматься.

    Дни — дни человека (`user_day`), правило продолжения — `next_streak`.
    """
    days = sorted({
        quiz.local_day or user_day(user, quiz.completed_at or quiz.started_at)
        for quiz in month_quizzes
    })
    streak, last = 0, None
    for day in days:
        streak = next_streak(streak, last, day)
        last = day
    return streak, last


# ============================================================================
# КТО В РЕЙТИНГЕ МЕСЯЦА
# ============================================================================

def ranked_in_month():
    """
    Условие «ряд стоит в рейтинге месяца»: хоть одно занятие и балл больше 0.

    ОДНО ПРАВИЛО ДЛЯ ТАБЛИЦЫ, КАРТОЧКИ И ЗАКРЫТИЯ. Прежде таблица и
    карточка считали место среди всех рядов месяца, а закрытие — только
    среди занимавшихся. Ряд без занятий появляется от оплаты жалобы
    (15 баллов, ни одного занятия), и замер 14 октября показал, к чему это
    вело: такой человек с 200 баллами весь месяц стоял в таблице первым с
    🥇 и не получал при закрытии ничего, двое со 100 видели у себя «#2» и
    получали золото, а извещение «место 4» приходило тому, кто в таблице
    стоял пятым. Теперь человек без занятий в месяц не входит, пока не
    пройдёт занятие; баллы за жалобы при этом лежат в его ряду и идут в
    «за всё время».
    """
    return and_(
        func.coalesce(MonthlyStats.monthly_quizzes, 0) > 0,
        func.coalesce(MonthlyStats.monthly_score, 0) > 0,
    )


# ============================================================================
# УТИЛИТА: тип награды → эмодзи
# ============================================================================

# Знак награды. ОН И ЕСТЬ НАГРАДА, а не украшение к ней.
#
# Прежде здесь стояли пустые строки: медали сняли общей чисткой знаков, и
# золото стало неотличимо от седьмого места — только номер. Владелец
# попросил обратного: «награды, баджи за викторины (которые были в проде)
# — важно сохранить. Это повышает их ценность».
#
# Это тот же довод, что у знаков игр: знак, который НАЗЫВАЕТ вещь, остаётся;
# знак, который её украшает, уходит. Медаль называет: первое место.
AWARD_MARKS = {
    "gold": "🥇",
    "silver": "🥈",
    "bronze": "🥉",
    # У места с четвёртого по десятое своего знака нет нарочно: «вошёл в
    # десятку» — это номер, а не медаль, и медаль там обесценила бы три
    # первые.
    "top10": "",
}


def award_mark(award_type: str) -> str:
    return AWARD_MARKS.get(award_type, "")


def _award_type_to_emoji(award_type: str) -> str:
    """Прежнее имя: оставлено ради вызывающих."""
    return award_mark(award_type)


# ============================================================================
# ПОЛУЧЕНИЕ МЕСЯЧНОГО РЕЙТИНГА (для таблицы лидеров)
# ============================================================================

async def get_monthly_leaderboard(
        session: AsyncSession,
        season_id: Optional[int] = None,
        limit: int = 50,
        learning_lang: str = DEFAULT_LEARNING_LANG,
) -> List[Dict]:
    """
    Месячный рейтинг по конкретному изучаемому языку.

    Сравнивать учащих разные языки в одной таблице некорректно: объём базы,
    частотность и сложность у языков разные.
    """
    if season_id is None:
        season = await get_current_season(session)
        if not season:
            return []
        season_id = season.id

    if learning_lang == ALL_LANGS:
        return await _monthly_leaderboard_all(session, season_id, limit)

    result = await session.execute(
        select(MonthlyStats, User)
        .join(User, MonthlyStats.user_id == User.id)
        .where(
            MonthlyStats.season_id == season_id,
            MonthlyStats.learning_lang == learning_lang,
            ranked_in_month(),
        )
        # Второй ключ — чтобы равные не менялись местами от запроса к запросу
        .order_by(MonthlyStats.monthly_score.desc(), User.id)
        .limit(limit)
    )

    stats_users = result.all()

    # МЕСТО — «1 + сколько набрали больше», как в `get_user_monthly_rank`.
    # Прежде здесь стоял порядковый номер строки: двое с равными 40 баллами
    # стояли в таблице вторым и третьим, а строка «Ты: #N» под ней говорила
    # обоим «#2» — один и тот же человек на одном экране с двумя местами
    leaderboard = []
    rank = 0
    prev_score = None
    for position, (stat, user) in enumerate(stats_users, 1):
        if stat.monthly_score != prev_score:
            rank, prev_score = position, stat.monthly_score
        awards_result = await session.execute(
            select(MonthlyAward)
            .where(MonthlyAward.user_id == user.id)
            .order_by(MonthlyAward.created_at.desc())
            .limit(5)
        )
        user_awards = awards_result.scalars().all()

        win_streak_result = await session.execute(
            select(WinStreak).where(WinStreak.user_id == user.id)
        )
        win_streak = win_streak_result.scalar_one_or_none()

        leaderboard.append({
            'rank': rank,
            'user_id': user.id,
            'username': user.username,
            'display_name': user.display_name,
            'monthly_score': stat.monthly_score,
            'monthly_streak': stat.monthly_streak,
            'monthly_quizzes': stat.monthly_quizzes,
            'monthly_words': stat.monthly_words,
            'monthly_reverse': stat.monthly_reverse,
            'monthly_avg_percent': stat.monthly_avg_percent,
            'awards': [
                {
                    'type': a.award_type,
                    'emoji': _award_type_to_emoji(a.award_type),
                    'season_id': a.season_id
                }
                for a in user_awards
            ],
            'win_streak': {
                'current': win_streak.current_streak if win_streak else 0,
                'emoji': win_streak.streak_emoji if win_streak else '',
                'title': win_streak.streak_title if win_streak else ''
            } if win_streak else None
        })

    return leaderboard


# ============================================================================
# ПОЗИЦИЯ ПОЛЬЗОВАТЕЛЯ + ВСЕ ДЕТАЛИ (FIX: теперь возвращает полные данные)
# ============================================================================

async def get_waiting_month_score(
        user_id: int,
        session: AsyncSession,
        season_id: int,
        learning_lang: str,
) -> int:
    """
    Баллы ряда, который ещё не стоит в рейтинге месяца (`ranked_in_month`).

    Такой ряд появляется от оплаты жалобы: 15 баллов, ни одного занятия.
    Карточка прежде говорила такому человеку «Вы ещё не в рейтинге» —
    будто баллов нет вовсе, хотя они начислены. 0 — ряда нет или он в
    рейтинге.
    """
    result = await session.execute(
        select(MonthlyStats.monthly_score).where(
            MonthlyStats.user_id == user_id,
            MonthlyStats.season_id == season_id,
            MonthlyStats.learning_lang == learning_lang,
            func.coalesce(MonthlyStats.monthly_quizzes, 0) == 0,
        )
    )
    return int(result.scalar() or 0)


async def get_user_monthly_rank(
        user_id: int,
        session: AsyncSession,
        season_id: Optional[int] = None,
        learning_lang: Optional[str] = None,
) -> Optional[Dict]:
    """
    Получить позицию пользователя + все его месячные данные.
    Не зависит от leaderboard limit — всегда точные данные.

    Ранг считается среди учащих тот же язык.
    """
    if season_id is None:
        season = await get_current_season(session)
        if not season:
            return None
        season_id = season.id

    if learning_lang is None:
        learning_lang = await _user_learning_lang(user_id, session)

    if learning_lang == ALL_LANGS:
        return await _user_monthly_rank_all(user_id, session, season_id)

    # Стата пользователя. Ряд без занятий (одни баллы за жалобы) в
    # рейтинге месяца не стоит — `ranked_in_month`; карточка тогда говорит
    # «Вы ещё не в рейтинге / пройдите занятие», как и тому, у кого ряда нет
    stat_result = await session.execute(
        select(MonthlyStats).where(
            MonthlyStats.user_id == user_id,
            MonthlyStats.season_id == season_id,
            MonthlyStats.learning_lang == learning_lang,
            ranked_in_month(),
        )
    )
    stat = stat_result.scalar_one_or_none()
    if not stat:
        return None

    # Всего участников по этому языку — тех же, что стоят в таблице
    total_result = await session.execute(
        select(func.count()).select_from(MonthlyStats).where(
            MonthlyStats.season_id == season_id,
            MonthlyStats.learning_lang == learning_lang,
            ranked_in_month(),
        )
    )
    total_users = int(total_result.scalar() or 0)
    if total_users == 0:
        return None

    # Ранг
    higher_result = await session.execute(
        select(func.count()).select_from(MonthlyStats).where(
            MonthlyStats.season_id == season_id,
            MonthlyStats.learning_lang == learning_lang,
            ranked_in_month(),
            MonthlyStats.monthly_score > stat.monthly_score
        )
    )
    rank = int(higher_result.scalar() or 0) + 1

    return {
        'rank': rank,
        'total_users': total_users,
        'learning_lang': learning_lang,
        'monthly_score': stat.monthly_score,
        'monthly_quizzes': stat.monthly_quizzes,
        'monthly_words': stat.monthly_words,
        'monthly_streak': stat.monthly_streak,
        'monthly_avg_percent': stat.monthly_avg_percent,
        'monthly_reverse': stat.monthly_reverse,
    }


def _month_totals_all(season_id: int):
    """
    Подзапрос: месяц человека по ВСЕМ языкам — сумма его рядов.

    Ряд входит, только если сам стоит в рейтинге (`ranked_in_month`): баллы
    за жалобы без занятий не вводят и в общий месяц. Средний процент —
    взвешенный по занятиям, серия — лучшая из языков (дни общие).
    """
    quizzes = func.coalesce(MonthlyStats.monthly_quizzes, 0)
    return (
        select(
            MonthlyStats.user_id.label("user_id"),
            func.sum(MonthlyStats.monthly_score).label("score"),
            func.sum(quizzes).label("quizzes"),
            func.sum(func.coalesce(MonthlyStats.monthly_words, 0)).label("words"),
            func.sum(func.coalesce(MonthlyStats.monthly_reverse, 0)).label("reverse"),
            func.max(func.coalesce(MonthlyStats.monthly_streak, 0)).label("streak"),
            (func.sum(func.coalesce(MonthlyStats.monthly_avg_percent, 0) * quizzes)
             / func.nullif(func.sum(quizzes), 0)).label("avg_percent"),
        )
        .where(MonthlyStats.season_id == season_id, ranked_in_month())
        .group_by(MonthlyStats.user_id)
        .subquery()
    )


async def _monthly_leaderboard_all(session: AsyncSession, season_id: int,
                                   limit: int) -> List[Dict]:
    """Таблица месяца по всем языкам; место — «1 + сколько набрали больше»."""
    totals = _month_totals_all(season_id)
    rows = (await session.execute(
        select(User, totals)
        .join(totals, totals.c.user_id == User.id)
        .order_by(totals.c.score.desc(), User.id)
        .limit(limit)
    )).all()

    leaderboard = []
    rank, prev = 0, None
    for position, row in enumerate(rows, 1):
        user = row[0]
        score = int(row.score or 0)
        if score != prev:
            rank, prev = position, score
        leaderboard.append({
            'rank': rank,
            'user_id': user.id,
            'username': user.username,
            'display_name': user.display_name,
            'monthly_score': score,
            'monthly_streak': int(row.streak or 0),
            'monthly_quizzes': int(row.quizzes or 0),
            'monthly_words': int(row.words or 0),
            'monthly_reverse': int(row.reverse or 0),
            'monthly_avg_percent': int(round(float(row.avg_percent or 0))),
        })
    return leaderboard


async def _user_monthly_rank_all(user_id: int, session: AsyncSession,
                                 season_id: int) -> Optional[Dict]:
    """Карточка месяца по всем языкам — тем же расчётом, что таблица."""
    totals = _month_totals_all(season_id)
    mine = (await session.execute(
        select(totals).where(totals.c.user_id == user_id)
    )).first()
    if mine is None:
        return None
    score = int(mine.score or 0)
    total_users = int((await session.execute(
        select(func.count()).select_from(totals))).scalar() or 0)
    higher = int((await session.execute(
        select(func.count()).select_from(totals).where(totals.c.score > score)
    )).scalar() or 0)
    return {
        'rank': higher + 1,
        'total_users': total_users,
        'learning_lang': ALL_LANGS,
        'monthly_score': score,
        'monthly_quizzes': int(mine.quizzes or 0),
        'monthly_words': int(mine.words or 0),
        'monthly_streak': int(mine.streak or 0),
        'monthly_avg_percent': int(round(float(mine.avg_percent or 0))),
        'monthly_reverse': int(mine.reverse or 0),
    }


# ============================================================================
# ПОДВЕДЕНИЕ ИТОГОВ МЕСЯЦА
# ============================================================================

async def finalize_season(season_id: int, session: AsyncSession):
    """
    Подвести итоги месяца — ОДНОЙ транзакцией.

    ПОЧЕМУ ОДНОЙ. Прежде серия побед записывалась своим commit посреди
    раздачи наград. Упади закрытие после него — часть наград и бонусов уже
    в базе, а `winners_finalized` ещё ложь; планировщик тем временем
    открывал новый сезон и снимал со старого `is_active`, и старый не
    дозакрывался уже никогда. Теперь либо записано всё, либо ничего, и
    незакрытый сезон подберёт `finalize_pending_seasons`.

    ПОБЕДА СЧИТАЕТСЯ ПО СЕЗОНУ, А НЕ ПО ЯЗЫКУ. Первое место в двух языках
    одного месяца прежде дважды звало серию побед: второй вызов видел
    «прошлая победа — этот же сезон, не предыдущий» и сбрасывал серию на 1
    (было 3 → 4 → 1), а `total_wins` рос на два. Награды остаются по
    языкам — медаль за каждый, — а месяц побед один.
    """
    season = await session.get(MonthlySeason, season_id)
    if not season:
        logger.error(f"Сезон {season_id} не найден")
        return

    if season.winners_finalized:
        logger.warning(f"Сезон {season_id} уже завершён")
        return

    results = await session.execute(
        select(MonthlyStats)
        .where(MonthlyStats.season_id == season_id)
        .order_by(MonthlyStats.learning_lang, MonthlyStats.monthly_score.desc())
    )
    results = results.scalars().all()

    # Итоги подводятся отдельно по каждому изучаемому языку: в каждом свой
    # топ-10 и свои награды
    by_lang: Dict[str, list] = {}
    for stat in results:
        by_lang.setdefault(stat.learning_lang, []).append(stat)

    # Кто стоит в итогах — тем же условием, что таблица и карточка
    # (`ranked_in_month`), а не своей копией его на Python
    in_ranking = set((await session.execute(
        select(MonthlyStats.id).where(
            MonthlyStats.season_id == season_id, ranked_in_month())
    )).scalars())

    logger.info(f"Подводим итоги сезона {season.month}/{season.year}")
    logger.info(f"Участников: {len(results)} в {len(by_lang)} языках")

    awards_config = {
        1: ('gold', 100),
        2: ('silver', 50),
        3: ('bronze', 25),
    }

    # Награды, уже выданные в этом сезоне: закрытие, прерванное до
    # введения единой транзакции, могло оставить часть. Второй раз их не
    # выдаём — иначе и бонус к lifetime начислился бы дважды
    already = {
        (a.user_id, a.learning_lang)
        for a in (await session.execute(
            select(MonthlyAward).where(MonthlyAward.season_id == season_id)
        )).scalars()
    }
    winners: set[int] = set()

    for lang, lang_stats in by_lang.items():
        # В ИТОГАХ — ТОЛЬКО ТЕ, КТО ЗАНИМАЛСЯ. Прежде место и медаль получал
        # любой ряд месяца, включая ноль баллов и ни одного занятия: из двух
        # учащих язык второй, не открывавший бота, получал «серебро» за
        # присутствие. Владелец: «проверь логику, должно быть адекватно»
        ranked = [s for s in lang_stats if s.id in in_ranking]
        logger.info(f"  {lang}: {len(ranked)} в итогах из {len(lang_stats)}")

        # РАВНЫЕ БАЛЛЫ — РАВНОЕ МЕСТО И РАВНАЯ НАГРАДА («1, 1, 3»). Прежде
        # место было номером строки: при равенстве таблица показывала двух
        # 🥇, а золото доставалось одному — тому, кого база отдала первым.
        # Таблица считает место так же (`get_monthly_leaderboard`)
        scores = [s.monthly_score for s in ranked]
        for stat in lang_stats:
            stat.final_rank = None
        places = []
        for stat in ranked:
            rank = 1 + sum(1 for other in scores if other > stat.monthly_score)
            stat.final_rank = rank
            places.append((rank, stat))

        for rank, stat in places:
            if rank > 10:
                continue
            user = await session.get(User, stat.user_id)
            if not user:
                continue

            if rank <= 3:
                award_type, lifetime_bonus = awards_config[rank]
            else:
                award_type, lifetime_bonus = ('top10', 10)

            if (stat.user_id, lang) in already:
                continue

            session.add(MonthlyAward(
                user_id=stat.user_id,
                season_id=season_id,
                learning_lang=lang,
                rank=rank,
                award_type=award_type,
                lifetime_bonus=lifetime_bonus
            ))

            user.lifetime_score = (user.lifetime_score or 0) + lifetime_bonus

            if rank == 1:
                winners.add(stat.user_id)

            logger.info(
                f"  #{rank} [{lang}] {user.display_name} — {stat.monthly_score} баллов — {award_type}"
            )

    for user_id in winners:
        if await update_win_streak(user_id, season_id, session):
            user = await session.get(User, user_id)
            user.total_monthly_wins = (user.total_monthly_wins or 0) + 1

    season.winners_finalized = True
    season.is_active = False

    await session.commit()
    logger.info(f"Сезон {season.month}/{season.year} завершён")


async def finalize_pending_seasons(session: AsyncSession) -> int:
    """
    Закрыть прошедшие сезоны, итоги которых так и не подведены.

    Сезон остаётся незакрытым в двух случаях: закрытие упало (теперь оно
    откатывается целиком), или новый сезон открыл круг, законченный в
    первые минуты месяца (`update_monthly_stats`), раньше планировщика —
    тогда старый уже не активен, и обычная проверка его не видит.
    Возвращает число закрытых.
    """
    today = utctoday()
    # Номера, а не объекты: откат после неудачного сезона просрочивает все
    # объекты сессии, и обращение к `season.id` следующего в асинхронной
    # сессии упало бы с MissingGreenlet
    pending = (await session.execute(
        select(MonthlySeason.id, MonthlySeason.month, MonthlySeason.year)
        .where(MonthlySeason.winners_finalized.is_(False),
               MonthlySeason.end_date < today)
        .order_by(MonthlySeason.year, MonthlySeason.month)
    )).all()

    closed = 0
    for season_id, month, year in pending:
        try:
            await finalize_season(season_id, session)
            closed += 1
        except Exception:
            await session.rollback()
            logger.exception("сезон %s/%s не закрылся", month, year)
    return closed


async def update_win_streak(user_id: int, season_id: int, session: AsyncSession) -> bool:
    """
    Обновить серию побед пользователя. БЕЗ commit — его делает закрытие
    сезона, одной транзакцией за всё.

    Возвращает False, если победа в этом сезоне уже учтена: второй вызов
    за тот же сезон ничего не меняет.
    """
    result = await session.execute(
        select(WinStreak).where(WinStreak.user_id == user_id)
    )
    win_streak = result.scalar_one_or_none()

    if not win_streak:
        win_streak = WinStreak(
            user_id=user_id, current_streak=0, best_streak=0, total_wins=0
        )
        session.add(win_streak)
    elif win_streak.last_win_season == season_id:
        return False

    season = await session.get(MonthlySeason, season_id)

    prev_month = season.month - 1 if season.month > 1 else 12
    prev_year = season.year if season.month > 1 else season.year - 1

    prev_season_result = await session.execute(
        select(MonthlySeason).where(
            MonthlySeason.year == prev_year,
            MonthlySeason.month == prev_month
        )
    )
    prev_season = prev_season_result.scalar_one_or_none()

    if prev_season and win_streak.last_win_season == prev_season.id:
        win_streak.current_streak += 1
    else:
        win_streak.current_streak = 1

    if win_streak.current_streak > win_streak.best_streak:
        win_streak.best_streak = win_streak.current_streak

    win_streak.total_wins = (win_streak.total_wins or 0) + 1
    win_streak.last_win_season = season_id
    win_streak.updated_at = utcnow()

    await session.flush()
    logger.info(f"Серия побед: {win_streak.current_streak}")
    return True


# ============================================================================
# РЕЙТИНГ ЗА ВСЁ ВРЕМЯ
# ============================================================================
#
# ЗА ВСЁ ВРЕМЯ = ВСЕ МЕСЯЧНЫЕ БАЛЛЫ (ЗАКРЫТЫЕ СЕЗОНЫ И ТЕКУЩИЙ) + НАГРАДЫ.
#
# Прежде таблица и карточка брали колонку `users.lifetime_score`. Её
# пополняет только `finalize_season`, и только БОНУСОМ ЗА МЕСТО (+100/50/25/
# 10) — месячные баллы туда не шли никогда, хотя README обещал
# «sum(monthly_scores) + award_bonuses». На dev-базе 14 октября у всех 26
# человек с ненулевой колонкой она равна сумме `monthly_awards.lifetime_bonus`
# до балла: у Juri 575 = 575 бонусов, а заработано в закрытых сезонах 2 603.
# Владелец набрал 189 за октябрь и видел «Баллы: 0, не в рейтинге»: труд
# вне десятки за всё время не считался вовсе, а текущего месяца — ни у кого.
#
# ПОЧЕМУ ИЗ ИСТОЧНИКА, А НЕ КОЛОНКОЙ. Сумма считается по `monthly_stats` и
# `monthly_awards`, а закрытие сезона месячные строки не трогает (пишет
# только `final_rank`). Поэтому в момент закрытия сумма не скачет: баллы
# октября стоят в ней весь октябрь и остаются после, а прибавляется ровно
# бонус за место — та награда, о которой человеку приходит извещение.
# Колонку пришлось бы при закрытии дописывать месячным баллом — и тогда
# текущий месяц до закрытия не входил бы, а после входил бы дважды, стоит
# сложить колонку с `monthly_stats`. Одна величина — один источник.
#
# ПО ИЗУЧАЕМОМУ ЯЗЫКУ, КАК ТАБЛИЦА МЕСЯЦА. Месяц сравнивает учащих один язык
# («объём базы, частотность и сложность у языков разные»), награды тоже
# выдаются по языкам. Таблица «за всё время» по всем языкам сразу
# противоречила бы этому доводу и разошлась бы с месячной: человек, учивший
# английский и перешедший на немецкий, стоял бы в немецком месяце со своими
# немецкими баллами, а в общей — с английскими. Поэтому всё здесь — баллы,
# награды, победы, выученные слова, число участников — по одному
# `learning_lang`.

def _lang_is(model, learning_lang: str) -> tuple:
    """Условие на язык; для `ALL_LANGS` — никакого: все языки сразу."""
    return () if learning_lang == ALL_LANGS else (model.learning_lang == learning_lang,)


def _lifetime_totals(learning_lang: str):
    """
    Подзапрос (user_id, total) — сумма за всё время по одному языку.

    Участник — тот, у кого есть хоть одна месячная строка на этом языке:
    ровно как в месяце, где «из N» — число строк сезона.
    """
    scored = (
        select(
            MonthlyStats.user_id.label("user_id"),
            func.sum(MonthlyStats.monthly_score).label("scored"),
        )
        .where(*_lang_is(MonthlyStats, learning_lang))
        .group_by(MonthlyStats.user_id)
        .subquery()
    )
    bonus = (
        select(
            MonthlyAward.user_id.label("user_id"),
            func.sum(MonthlyAward.lifetime_bonus).label("bonus"),
        )
        .where(*_lang_is(MonthlyAward, learning_lang))
        .group_by(MonthlyAward.user_id)
        .subquery()
    )
    total = func.coalesce(scored.c.scored, 0) + func.coalesce(bonus.c.bonus, 0)
    return (
        select(scored.c.user_id, total.label("total"))
        .outerjoin(bonus, bonus.c.user_id == scored.c.user_id)
        .subquery()
    )


async def _wins_by_user(session: AsyncSession, user_ids: list,
                        learning_lang: str) -> Dict[int, int]:
    """Первых мест на этом языке — по наградам, как и баллы."""
    if not user_ids:
        return {}
    rows = await session.execute(
        select(MonthlyAward.user_id, func.count())
        .where(
            MonthlyAward.user_id.in_(user_ids),
            *_lang_is(MonthlyAward, learning_lang),
            MonthlyAward.award_type == "gold",
        )
        .group_by(MonthlyAward.user_id)
    )
    return {uid: int(n) for uid, n in rows.all()}


async def _learned_by_user(session: AsyncSession, user_ids: list,
                           learning_lang: str) -> Dict[int, int]:
    """
    Выученных слов на этом языке — по `user_words`.

    Колонка `users.words_learned` пересчитывается в конце круга по ТЕКУЩЕМУ
    языку человека: у сменившего язык она показала бы в немецкой таблице
    английские слова.
    """
    if not user_ids:
        return {}
    rows = await session.execute(
        select(UserWord.user_id, func.count())
        .where(
            UserWord.user_id.in_(user_ids),
            *_lang_is(UserWord, learning_lang),
            UserWord.learned.is_(True),
        )
        .group_by(UserWord.user_id)
    )
    return {uid: int(n) for uid, n in rows.all()}


async def get_lifetime_leaderboard(
        session: AsyncSession,
        limit: int = 50,
        learning_lang: str = DEFAULT_LEARNING_LANG,
) -> List[Dict]:
    """
    Таблица за всё время по одному изучаемому языку.

    МЕСТО — «1 + сколько набрали больше», как в `get_user_lifetime_rank`:
    при равенстве порядковый номер строки дал бы в таблице одно место, а в
    строке «Ты: #N» под ней — другое.
    """
    totals = _lifetime_totals(learning_lang)
    rows = (await session.execute(
        select(User, WinStreak, totals.c.total)
        .join(totals, totals.c.user_id == User.id)
        .outerjoin(WinStreak, User.id == WinStreak.user_id)
        # Второй ключ — чтобы равные не менялись местами от запроса к запросу
        .order_by(totals.c.total.desc(), User.id)
        .limit(limit)
    )).all()

    ids = [user.id for user, _, _ in rows]
    wins = await _wins_by_user(session, ids, learning_lang)
    learned = await _learned_by_user(session, ids, learning_lang)

    leaderboard = []
    rank = 0
    prev_total = None
    for position, (user, win_streak, total) in enumerate(rows, 1):
        total = int(total or 0)
        if total != prev_total:
            rank, prev_total = position, total
        leaderboard.append({
            'rank': rank,
            'user_id': user.id,
            'display_name': user.display_name,
            'lifetime_score': total,
            'total_wins': wins.get(user.id, 0),
            'words_learned': learned.get(user.id, 0),
            'best_streak_days': user.best_streak_days,
            'win_streak': {
                'current': win_streak.current_streak if win_streak else 0,
                'best': win_streak.best_streak if win_streak else 0,
                'total': win_streak.total_wins if win_streak else 0
            } if win_streak else None
        })

    return leaderboard


async def get_user_lifetime_rank(
        user_id: int,
        session: AsyncSession,
        learning_lang: Optional[str] = None,
) -> Dict:
    """
    Карточка «за всё время»: место, баллы, победы, выученные слова.

    Не зависит от размера таблицы: прежде место искалось в её первых десяти
    строках, и одиннадцатый получал «Позиция: —».

    Словарь возвращается всегда; `rank` — None, если на этом языке у
    человека нет ни одной месячной строки (баллов тогда ноль).
    """
    if learning_lang is None:
        learning_lang = await _user_learning_lang(user_id, session)

    totals = _lifetime_totals(learning_lang)
    mine = (await session.execute(
        select(totals.c.total).where(totals.c.user_id == user_id)
    )).scalar_one_or_none()
    total_users = int((await session.execute(
        select(func.count()).select_from(totals)
    )).scalar() or 0)

    rank = None
    if mine is not None:
        mine = int(mine)
        higher = int((await session.execute(
            select(func.count()).select_from(totals).where(totals.c.total > mine)
        )).scalar() or 0)
        rank = higher + 1

    wins = await _wins_by_user(session, [user_id], learning_lang)
    learned = await _learned_by_user(session, [user_id], learning_lang)
    return {
        'rank': rank,
        'total_users': total_users,
        'learning_lang': learning_lang,
        'lifetime_score': mine or 0,
        'total_wins': wins.get(user_id, 0),
        'words_learned': learned.get(user_id, 0),
    }

# ============================================================================
# ИЗВЕЩЕНИЕ О НАГРАДЕ
# ============================================================================

# Сколько дней после закрытия сезона извещение о награде ещё досылается.
# Почасовая проверка повторяет неотправленные, но не вечно: поздравление с
# местом за прошлый месяц, пришедшее через месяц, — то самое «поздравить с
# местом, о котором человек забыл», ради которого 65 старых наград и были
# помечены сообщёнными при миграции. Трое суток покрывают выключенный бот
# и сбой сети, но не следующий сезон
AWARD_NOTICE_WINDOW = timedelta(days=3)


async def notify_season_awards(
    bot, session: AsyncSession, now: Optional[datetime] = None,
) -> int:
    """
    Сообщить людям о наградах, о которых им ещё не сообщали.

    ЗАЧЕМ. Сезон закрывался так: награды записаны, `lifetime_score` вырос,
    серия побед обновлена — и ни один человек об этом не узнавал. Владелец
    просил прямо обратного: «награды, баджи за викторины (которые были в
    проде) — важно сохранить. Это повышает их ценность». Награда, о которой
    не сказали, ценности не добавляет: она не видна даже тому, кто её взял.

    Та же форма дефекта уже встречалась у жалобы на перевод: баллы
    начислялись, а автору не сообщалось ничего, хотя бот обещал награду.

    ИДЕМПОТЕНТНОСТЬ ОБЯЗАТЕЛЬНА. Закрытие сезона вызывается первого числа
    по расписанию И каждый час страховкой — на случай выключенного бота.
    Без отметки `notified_at` победитель получал бы поздравление каждый
    час. Отметка ставится ПОСЛЕ успешной отправки, иначе сбой сети отнял
    бы поздравление навсегда.

    Ошибка доставки не валит ничего: человек мог закрыть бота, и награда от
    этого не хуже. Такая награда остаётся непомеченной и уйдёт при
    следующем прогоне.

    Возвращает число отправленных.
    """
    from app.bot.handlers.leaderboard.utils import format_month_name
    from aiogram.exceptions import TelegramForbiddenError

    from app.locales import DEFAULT_LOCALE, get_text

    now = now or utcnow()
    pending = (await session.execute(
        select(MonthlyAward)
        .where(
            MonthlyAward.notified_at.is_(None),
            # Только свежезакрытый сезон: прежде выборка не знала срока, и
            # недоставленная в октябре награда ушла бы при закрытии ноября
            MonthlyAward.created_at >= now - AWARD_NOTICE_WINDOW,
        )
        .order_by(MonthlyAward.rank)
    )).scalars().all()

    if not pending:
        return 0

    sent = 0
    for award in pending:
        user = await session.get(User, award.user_id)
        if not user:
            # Человека больше нет — награда остаётся в истории сезона, но
            # сообщать некому; помечаем, чтобы не перебирать её вечно
            award.notified_at = utcnow()
            continue

        season = await session.get(MonthlySeason, award.season_id)
        lang = user.interface_language or DEFAULT_LOCALE

        # Значения считаются ДО вызова: выражение с запятыми внутри
        # `get_text(...)` не разбирается проверкой соответствия параметров
        # (`test_format_parameters_match`), и ключ с подстановками прошёл бы
        # мимо неё молча
        #
        # У десятки медали нет, и знак остаётся пустым. Прежде на его место
        # вставал «#5» — и строка выходила «#5 Ты в зачёте за октябрь: место
        # 5», номер дважды; ровно этот повтор («🥇 1.») снимали в таблице
        mark = award_mark(award.award_type)
        month = format_month_name(season.month, lang, inline=True) if season else ""

        try:
            await bot.send_message(
                award.user_id,
                get_text(
                    "award_won", lang,
                    mark=mark,
                    rank=award.rank,
                    month=month,
                    bonus=award.lifetime_bonus,
                ).strip(),
            )
            award.notified_at = utcnow()
            sent += 1
        except TelegramForbiddenError:
            # Заблокировал бота — доставить нельзя ни сейчас, ни через час.
            # Без отметки попытка повторялась бы каждый час все трое суток.
            # `notified_at` здесь значит «извещение закрыто», а не «прочитано»:
            # отдельной колонки под отказ в схеме нет
            logger.info(
                "о награде не сообщить: бот заблокирован (user=%s, сезон=%s)",
                award.user_id, award.season_id,
            )
            award.notified_at = utcnow()
        except Exception:
            logger.info(
                "не удалось сообщить о награде (user=%s, сезон=%s)",
                award.user_id, award.season_id, exc_info=True,
            )

    await session.commit()
    logger.info("о наградах сообщено: %s из %s", sent, len(pending))
    return sent
