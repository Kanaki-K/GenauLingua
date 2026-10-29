"""
Итог занятия: завершение круга, разбор по словам, поощрение, кнопки итога.

Вынесено из `game.py` переносом, без правок поведения.
"""

import logging
from datetime import date, datetime, timedelta
from typing import Optional

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.handlers.quiz.question import _CHANNEL_MARKS
from app.bot.handlers.quiz.settings import RESULT_SETTINGS, get_level_offer_keyboard
from app.core.clock import utcnow, utctoday
from app.database.enums import QuizChannel
from app.database.models import QuizQuestion, QuizSession, User, UserWord, Word
from app.locales import get_text, plural
from app.services.language_service import LanguagePair, option_label
from app.services.level_service import (
    should_offer_lower_level, should_offer_next_level,
)
from app.services.monthly_leaderboard_service import update_monthly_stats
from app.services.quiz_service import FIRST_LESSON_LENGTH, get_user_progress_stats

logger = logging.getLogger(__name__)


def get_results_keyboard(has_errors: bool, lang: str = "ru") -> InlineKeyboardMarkup:
    """
    Итог круга. ПЕРВАЯ КНОПКА — «ещё круг», и это главное в этом экране.

    Прежде её не было вовсе. В самый высокий момент мотивации за день —
    человек только что закончил круг и видит результат — бот предлагал
    «изменить режим викторины» (экран настроек) и «сообщить об ошибке»
    (форму жалобы). Чтобы сыграть второй раз, надо было уйти из сообщения
    и найти клавиатуру внизу.

    Замер объясняет, чего это стоило: 79% тех, кто вообще играл, ни разу не
    занимались два дня подряд. Экран, которым кончается действие, обязан
    предлагать следующее действие первой кнопкой — а не настройки.

    Порядок дальше: сперва ошибки (они про только что пройденное), потом
    режим. Жалоба — на разборе каждого слова, не здесь.
    """
    buttons = [[
        InlineKeyboardButton(
            text=get_text("quiz_btn_one_more", lang),
            # «:again» — это кнопка «ещё круг» в итоге. Петля возврата
            # считается по этой пометке, и без неё круг-повтор
            # неотличим от входа с домашнего экрана
            callback_data="learn_now:again",
        )
    ]]

    if has_errors:
        buttons.append([
            InlineKeyboardButton(
                text=get_text("quiz_btn_repeat_errors", lang),
                callback_data="repeat_errors",
            )
        ])

    buttons.append([
        InlineKeyboardButton(
            text=get_text("quiz_btn_change_mode", lang),
            # «:result» говорит экрану уровня, ОТКУДА пришли: его «Назад»
            # ведёт на домашний экран, а не в настройки. Прежде человек,
            # поправив трудность после круга, оказывался в чужом месте —
            # находка владельца
            # Новым сообщением под итогом, и «Назад» его убирает
            # (`settings.RESULT_SETTINGS`): итог круга остаётся на месте
            callback_data=RESULT_SETTINGS,
        )
    ])
    # «Сообщить об ошибке» ЗДЕСЬ БОЛЬШЕ НЕТ (17.10): жалоба переехала на
    # разбор каждого слова (`report_inline`) — в итоге уже не вспомнить, где
    # было не так. Обработчики списка (`report.py`) оставлены для кнопок
    # в старых сообщениях

    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def update_user_activity(session: AsyncSession, user_id: int,
                               day: Optional[date]) -> None:
    """
    Отметить день занятий. Правило и лучшая серия — в `streak_service`.

    Логика переехала туда целиком: серию ЧИТАЮТ пять мест (домашний экран,
    напоминание, статистика, админка, месячный зачёт), а считало её это
    единственное. Из-за этого колонка врала всем, кто перестал заниматься:
    серия пересчитывается только на завершении круга, а значит у
    остановившегося навсегда остаётся последнее значение. Замер: устарела у
    128 человек из 128, последняя активность 236 дней назад.
    """
    from app.services.streak_service import register_activity

    user = await session.get(User, user_id)
    # День — тот, что записан в занятие при завершении (`local_day`), а не
    # часы в момент отметки: занятие, законченное в 23:59:59.8, отмечалось
    # через полсекунды уже следующим днём, сжигало заморозку и расходилось
    # с восстановлением по истории (аудит 2.1)
    register_activity(user, today=day)
    await session.commit()


# Строка итога «сколько пришло этой игрой» — у каждой игры, кроме карточки.
# Таблицей, потому что подписи разные по смыслу («Вспомнили», «На слух»), но
# счётчики строятся по ней же: игра без строки здесь не уронит итог.
_RESULT_LINES = {
    QuizChannel.REVERSE.value: "quiz_result_recalled",
    QuizChannel.AUDIO.value: "quiz_result_by_ear",
    QuizChannel.SPEECH.value: "quiz_result_spoken",
    QuizChannel.BUILD.value: "quiz_result_built",
}


def _round_breakdown(
    items: list, pair: LanguagePair, lang: str
) -> tuple[list[str], list[str]]:
    """
    Разбор круга по словам и строки «сколько пришло каждым каналом».

    Канал берётся у ВОПРОСА, а не у слова: одно и то же слово в разных
    кругах приходит разными каналами, и отметка у слова врала бы про круг.

    Строка канала показывается ТОЛЬКО если такие вопросы были. «🎤 Вслух: 0»
    у человека с выключенной речью напоминало бы о неудаче там, где её нет.

    Прежде обе строки существовали в шести локалях и не печатались ни разу:
    счётчик слуха считался и НЕ ИСПОЛЬЗОВАЛСЯ, а речь не считалась вовсе.
    Новая игра растворялась в списке, и человек не замечал, что уже узнаёт
    слова ушами и произносит их, — то есть ровно того, за чем и затевались
    три канала.
    """
    details: list[str] = []
    counts = {value: 0 for value in _RESULT_LINES}

    # ЗНАК ИГРЫ — ТОЛЬКО ЕСЛИ ИГР БЫЛО БОЛЬШЕ ОДНОЙ.
    #
    # Знак здесь РАЗЛИЧАЕТ, а значит нужен там, где есть что различать.
    # У новичка весь круг идёт карточкой (слово допускается к остальным
    # играм после одного верного ответа глазами), и пятнадцать одинаковых
    # 📖 подряд — это рябь, которая ничего не говорит. В смешанном круге
    # тот же знак отвечает на «чем меня сейчас спросили».
    mixed = len({item.channel for item, _ in items}) > 1

    for item, word in items:
        icon = "✓" if item.is_correct else "✗"
        mark = _CHANNEL_MARKS.get(item.channel) if mixed else ""
        if mark:
            icon += f" {mark}"
        # Значок есть у четырёх каналов, а СЧЁТЧИК только у трёх: доска
        # значком помечается, но своей строки «сколько пришло» не имеет —
        # она не навык. Прибавлять по значку, а не по наличию ключа, значило бы
        # KeyError на первом же круге с доской, то есть падение ИТОГА, когда
        # круг уже пройден и записан. Хуже места для падения нет
        if item.channel in counts:
            counts[item.channel] += 1
        details.append(
            f"{icon} {option_label(word, pair.learning)} — {option_label(word, pair.native)}"
        )

    channel_lines: list[str] = []
    for value, key in _RESULT_LINES.items():
        if counts[value]:
            count = counts[value]
            channel_lines.append(get_text(key, lang, count=count))

    return details, channel_lines


async def _offer_what_fits(
    callback: CallbackQuery, session: AsyncSession, user: User, lang: str
) -> None:
    """
    Предложить человеку одно — и не больше одного за круг.

    После круга у бота бывает что сказать сверх результата: поднять или
    опустить уровень. Два предложения подряд превращают конец круга в
    допрос, поэтому здесь очередь, а не список.

    НАПОМИНАНИЙ ЗДЕСЬ БОЛЬШЕ НЕТ (16.10). Прежде они шли первыми, кроме
    случая, когда новичку явно легко. Теперь они включаются сами при
    знакомстве (`reminder_service.enable_by_default`), и после первого
    урока предлагается ОДНО — уровень, по прежней логике (владелец: «это
    может быть человек более высокого уровня… её я бы не трогал»).
    """
    following = await should_offer_next_level(user, session)
    if following is not None:
        await _send_level_offer(callback, user, lang, following)
        return

    # Слишком трудно — уровень ниже. Никогда вместе с подъёмом: оба
    # смотрят на одну точность, и выше 90% и ниже 60% разом не бывает
    previous = await should_offer_lower_level(user, session)
    if previous is not None:
        from app.bot.handlers.quiz.settings import get_level_down_keyboard

        try:
            await callback.bot.send_message(
                chat_id=callback.message.chat.id,
                text=get_text("level_down_offer", lang,
                              current=user.level.value, previous=previous.value),
                reply_markup=get_level_down_keyboard(user.level, previous, lang),
            )
        except Exception:
            logger.warning("не удалось предложить уровень ниже", exc_info=True)
        return

    # «Говорю» ПО ЖЕЛАНИЮ (2.2.1) — третьим в очереди: только когда об
    # уровне сказать нечего, чтобы конец занятия не стал допросом
    from app.bot.handlers.quiz.speech_invite import send_invite, should_invite

    try:
        if await should_invite(session, user):
            await send_invite(callback.bot, callback.message.chat.id, session, user, lang)
    except Exception:
        logger.warning("не удалось предложить «Говорю»", exc_info=True)


async def _place_by_answers(session: AsyncSession, user: User, pair: LanguagePair, items):
    """
    Уровень по ответам знакомства (`first_lesson.recommend`) — ставится сразу.
    Уровень слова — в изучаемом языке (`level_of`), как его подбирали.
    """
    from app.services import first_lesson, journal
    from app.services.level_service import set_level
    from app.services.word_level import level_of

    answers = [(await level_of(session, word, pair.learning), bool(question.is_correct))
               for question, word in items]
    if not answers:
        return None
    level = first_lesson.recommend(answers)
    journal.note(session, user.id, "level", "placement", to=level.value,
                 answers=[f"{getattr(lv, 'value', lv)}{'+' if ok else '-'}" for lv, ok in answers])
    if not await set_level(user, session, level, action="placed"):
        await session.commit()
    return level


async def _send_placement(callback: CallbackQuery, user: User, lang: str) -> None:
    """Итог знакомства: уровень по ответам и кнопки, чтобы поправить."""
    from app.bot.handlers.quiz.settings import get_level_set_keyboard

    try:
        await callback.bot.send_message(
            chat_id=callback.message.chat.id,
            text=get_text("placement_result", lang, level=user.level.value),
            reply_markup=get_level_set_keyboard(user.level, lang),
        )
    except Exception:
        logger.warning("не удалось показать итог знакомства", exc_info=True)


async def _send_level_offer(callback: CallbackQuery, user: User, lang: str, following) -> None:
    """
    Выбор уровня (A2 / B1 / B2 / C1) — всем, когда пора предложить подъём.

    Сильный человек встаёт на свой уровень одним нажатием, а не тремя
    скучными занятиями подряд (`level_service.jump_to_level`). Не только
    новичку: владелец, 15.10 — «у нас так же есть те, кто первую семёрку
    никогда не увидят». Многие давние стоят на A1 — старая версия ставила
    его всем. Новичок и давний различаются лишь тем, КОГДА пора
    (`level_service._thresholds`): после одного занятия или после двух.
    """
    from app.bot.handlers.quiz.settings import PICK_UP_TO, get_level_pick_keyboard

    # Выбор — пока выше есть что выбрать до C1; с C1 остаётся только C2, и
    # пустой ряд кнопок Telegram не примет — тогда обычный вопрос
    from app.services.level_service import LEVEL_ORDER

    if LEVEL_ORDER.index(following) <= LEVEL_ORDER.index(PICK_UP_TO):

        text = get_text("level_offer_pick", lang, current=user.level.value)
        keyboard = get_level_pick_keyboard(user.level, lang)
    else:
        text = get_text("level_offer", lang,
                        current=user.level.value, following=following.value)
        keyboard = get_level_offer_keyboard(following, lang)
    try:
        await callback.bot.send_message(
            chat_id=callback.message.chat.id, text=text, reply_markup=keyboard,
        )
    except Exception:
        logger.warning("не удалось предложить уровень", exc_info=True)


# ============================================================================
# ПООЩРЕНИЕ В КОНЦЕ КРУГА
# ============================================================================

def _days_since_last_round(user: User) -> int:
    """
    Сколько дней человек не заходил ДО этого круга.

    Нужно одному поводу — «с возвращением». Берётся `last_quiz_date`, пока
    она не перезаписана сегодняшним числом.
    """
    last = getattr(user, "last_quiz_date", None)
    if last is None:
        return 0
    return max(0, (utctoday() - last).days)


async def _season_score(
    session: AsyncSession, user: User, pair: LanguagePair, on: date,
) -> int:
    """
    Месячный балл человека по ЭТОМУ языку в сезоне месяца `on`.

    По языку, а не вообще: ряды сезона ведутся отдельно на каждый
    изучаемый язык, и балл из чужого ряда дал бы бессмысленную разность.

    СЕЗОН — ПО ДАТЕ ЗАВЕРШЕНИЯ ЗАНЯТИЯ, а не «какой сейчас активен». Так
    занятие относит к сезону и месячный счёт (`update_monthly_stats`).
    Прежде «до» и «после» брались из активного сезона, а он меняется ровно
    на границе месяца: занятие, законченное 1-го в 00:01, «до» читало
    октябрь, запись открывала ноябрь, «после» читало ноябрь — разность
    уходила в минус, и итог показывал «+0» за честно заработанные баллы.
    """
    from app.database.models import MonthlySeason, MonthlyStats

    row = (await session.execute(
        select(MonthlyStats.monthly_score)
        .join(MonthlySeason, MonthlySeason.id == MonthlyStats.season_id)
        .where(
            MonthlyStats.user_id == user.id,
            MonthlyStats.learning_lang == pair.learning,
            MonthlySeason.year == on.year,
            MonthlySeason.month == on.month,
        )
    )).scalar()
    return int(row or 0)


async def _month_place(session: AsyncSession, user_id: int) -> Optional[dict]:
    """Место и баллы человека в общем месяце — до и после занятия."""
    from app.services.monthly_leaderboard_service import ALL_LANGS, get_user_monthly_rank

    try:
        return await get_user_monthly_rank(user_id, session, learning_lang=ALL_LANGS)
    except Exception:
        logger.warning("место месяца не посчиталось (user=%s)", user_id, exc_info=True)
        return None


async def _race_lines(session: AsyncSession, user: User, lang: str,
                      before: Optional[dict]) -> list[str]:
    """
    Рывок в момент усилия (REWARDS.md §Е, К): «↑ Место в месяце: 3 · до Ольги
    9 баллов» — только когда место выросло; «Новый рекорд месяца» — только
    когда превзойдён лучший из прошлых ПОЛНЫХ месяцев (в первом месяце иначе
    каждое занятие было бы рекордом).
    """
    import html

    from app.database.models import MonthlySeason, MonthlyStats
    from app.services.monthly_leaderboard_service import ALL_LANGS, month_neighbours
    from app.services.standing import clean_name

    after = await _month_place(session, user.id)
    if not after:
        return []
    lines = []
    if before is None or after["rank"] < before["rank"]:
        rank = after["rank"]
        line = get_text("summary_place", lang, rank=rank)
        season_id = await _season_id(session)
        above, _ = (await month_neighbours(session, user.id, season_id, ALL_LANGS)
                    if season_id else (None, None))
        if above:
            name = html.escape(clean_name(above["display_name"]))
            gap = plural(max(0, above["monthly_score"] - after["monthly_score"]), "plural_points", lang)
            line += " · " + get_text("summary_gap", lang, name=name, gap=gap)
        lines.append(line)

    by_month = (
        select(func.sum(MonthlyStats.monthly_score).label("total"))
        .join(MonthlySeason, MonthlySeason.id == MonthlyStats.season_id)
        .where(MonthlyStats.user_id == user.id, MonthlySeason.winners_finalized.is_(True))
        .group_by(MonthlyStats.season_id)
        .subquery()
    )
    best_past = (await session.execute(select(func.max(by_month.c.total)))).scalar()
    score_before = (before or {}).get("monthly_score", 0)
    if best_past and score_before <= best_past < after["monthly_score"]:
        points = plural(after["monthly_score"], "plural_points", lang)
        lines.append(get_text("summary_record", lang, points=points))
    return lines


async def _mark_overtaken(session: AsyncSession, user_id: int,
                          before: Optional[dict]) -> None:
    """
    Отметить тех, кого человек только что обогнал в общем месяце.

    Сообщение «Вас обогнали» шлёт не этот код, а распорядитель сообщений —
    в общем бюджете и днём (`nudges.py`). Отметка — только тем, кто теперь
    в первой десятке: дальше обгон не новость. Ошибка здесь не должна
    ронять итог занятия.
    """
    from app.services.monthly_leaderboard_service import ALL_LANGS, get_monthly_leaderboard

    if not before:
        return
    try:
        after = await _month_place(session, user_id)
        if not after or after["rank"] >= before["rank"]:
            return
        board = await get_monthly_leaderboard(session, learning_lang=ALL_LANGS,
                                              limit=min(before["rank"], 10))
        passed = [e["user_id"] for e in board
                  if after["rank"] < e["rank"] <= before["rank"] and e["user_id"] != user_id]
        if passed:
            await session.execute(update(User).where(User.id.in_(passed)).values(
                overtaken_by_id=user_id, overtaken_at=utcnow()))
            await session.commit()
    except Exception:
        logger.warning("обгон не отмечен (user=%s)", user_id, exc_info=True)
        await session.rollback()


async def _season_id(session: AsyncSession) -> Optional[int]:
    from app.services.monthly_leaderboard_service import get_current_season

    season = await get_current_season(session)
    return season.id if season else None


async def _praise_lines(
    session: AsyncSession,
    user: User,
    pair: LanguagePair,
    lang: str,
    items: list,
    *,
    quiz_session: Optional[QuizSession],
    answered: int,
    correct: int,
    learned_before: int,
    score_before: int,
    days_away: int,
    season_day: Optional[date] = None,
) -> list[str]:
    """
    Собрать факты круга и отдать готовые строки поощрения.

    Решение «за что хвалить» живёт в `praise_service` и проверяется без
    базы; здесь только ЗАМЕРЫ. Разделение нарочное: выбор повода — правило,
    и спорить о нём надо на числах, а не гоняя круги.
    """
    from app.services.praise_service import RoundFacts, build_lines

    progress = await get_user_progress_stats(user.id, session, pair)
    words_in_work = int(progress["seen_words"])

    word_ids = [word.id for _, word in items]
    started = quiz_session.started_at if quiz_session else None

    new_words = 0
    returned_right = 0
    if word_ids:
        rows = (await session.execute(
            select(UserWord.word_id, UserWord.created_at)
            .where(
                UserWord.user_id == user.id,
                UserWord.learning_lang == pair.learning,
                UserWord.word_id.in_(word_ids),
            )
        )).all()
        # Слово считается новым, если его ряд прогресса создан В ЭТОМ круге
        fresh = {
            word_id for word_id, created in rows
            if started is not None and created is not None and created >= started
        }
        new_words = len(fresh)
        returned_right = sum(
            1 for question, word in items
            if question.is_correct and word.id not in fresh
        )

    # Первый в жизни верный ответ каналом: сумма по всем словам равна
    # числу верных этим каналом в этом круге — значит прежде их не было
    first_audio, first_speech = False, False
    for channel, column, flag in (
        (QuizChannel.AUDIO.value, UserWord.correct_audio, "audio"),
        (QuizChannel.SPEECH.value, UserWord.correct_speech, "speech"),
    ):
        here = sum(
            1 for question, _ in items
            if question.is_correct and question.channel == channel
        )
        if not here:
            continue
        total = int((await session.execute(
            select(func.coalesce(func.sum(column), 0)).where(
                UserWord.user_id == user.id,
                UserWord.learning_lang == pair.learning,
            )
        )).scalar() or 0)
        if total == here:
            if flag == "audio":
                first_audio = True
            else:
                first_speech = True

    # Серия читается через `streak_service`, а не из колонки: колонка
    # пересчитывается только на завершении круга, и у остановившегося в ней
    # навсегда остаётся последнее значение
    from app.services.streak_service import current_streak, user_day, user_today

    # Первое ли это законченное занятие за день человека: рубеж серии и
    # заморозка празднуются один раз — в занятие, которое серию и сдвинуло
    # Тот же день, что у отметки серии: по моменту завершения занятия
    today = getattr(quiz_session, "local_day", None) or user_today(user)
    from app.services.monthly_leaderboard_service import scored_sessions_filter

    # Только зачётные занятия: повтор ошибок в 00:05 не делает настоящее
    # первое занятие дня «вторым» (независимая проверка 2.1)
    recent = (await session.execute(
        select(QuizSession.completed_at).where(
            QuizSession.user_id == user.id,
            QuizSession.completed_at.isnot(None),
            QuizSession.completed_at >= utcnow() - timedelta(days=2),
            scored_sessions_filter(),
        )
    )).scalars().all()
    rounds_today = sum(1 for moment in recent if user_day(user, moment) == today)

    facts = RoundFacts(
        points=max(0, await _season_score(
            session, user, pair, season_day or utctoday()
        ) - score_before),
        answered=answered,
        correct=correct,
        rounds_total=int(user.quizzes_passed or 0),
        learned_before=learned_before,
        learned_now=int(user.words_learned or 0),
        streak_days=current_streak(user),
        best_streak=int(getattr(user, "best_streak_days", 0) or 0),
        words_in_work=words_in_work,
        words_in_work_before=max(0, words_in_work - new_words),
        new_words=new_words,
        returned_right=returned_right,
        days_away=days_away,
        first_audio=first_audio,
        first_speech=first_speech,
        first_round_today=rounds_today <= 1,
        freeze_used_today=getattr(user, "streak_freeze_on", None) == today,
    )
    return build_lines(facts, lang)


async def _finish_quiz(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
    user: User,
    pair: LanguagePair,
    lang: str,
    data: dict,
) -> None:
    """Завершение викторины: итоги, статистика, кнопки."""
    session_id = data["session_id"]
    correct_answers = data["correct_answers"]
    errors = data.get("errors", [])
    is_error_repeat = data.get("is_error_repeat", False)

    # ЗАВЕРШИТЬ МОЖНО ОДИН РАЗ — и это решает база, а не память процесса.
    # Двойное «Далее» гасит `_claim_advance`, но состояние живёт в памяти и
    # не переживает двух экземпляров бота или повтора обновления после
    # перезапуска. Условное обновление атомарно: второй вызов не получит
    # строки и уйдёт, не прибавив `quizzes_passed` и не прислав второй итог.
    from app.services.streak_service import lesson_day

    done_at = utcnow()
    # День занятия пишется в занятие и тот же идёт в серию (`lesson_day`)
    done_day = lesson_day(user, done_at)
    claimed = await session.execute(
        update(QuizSession)
        .where(QuizSession.id == session_id, QuizSession.is_completed.isnot(True))
        .values(
            completed_at=done_at, local_day=done_day,
            is_completed=True, exit_reason="completed",
            exit_at_question=QuizSession.answered_questions,
        )
        .returning(QuizSession.id)
    )
    if claimed.first() is None:
        await session.rollback()
        logger.info("круг %s уже завершён — повтор завершения пропущен", session_id)
        return
    await session.commit()
    quiz_session = await session.get(QuizSession, session_id)
    if quiz_session is not None:
        await session.refresh(quiz_session)

    answered = quiz_session.answered_questions if quiz_session else 0

    # Конец занятия — в журнал пути (2.2.1): итог, длина и дверь входа одной
    # строкой, рядом с нажатиями и вопросами этого же занятия
    if quiz_session is not None:
        from app.services import journal

        started = quiz_session.started_at
        journal.note(session, user.id, "lesson", "finished", session_id=session_id,
                     answered=answered, correct=quiz_session.correct_answers,
                     total=quiz_session.total_questions, source=quiz_session.start_source,
                     repeat=is_error_repeat or None,
                     seconds=int((done_at - started).total_seconds()) if started else None)

    # ЧТО БЫЛО ДО КРУГА. Поощрение должно хвалить за то, что случилось
    # ИМЕННО СЕЙЧАС, а оба числа — накопительные: «выучено» пересчитывается
    # целиком, месячный балл считается по формуле от всех занятий сезона.
    # Прирост виден только разностью, и снять «до» надо раньше записи.
    learned_before = int(user.words_learned or 0)
    days_away = _days_since_last_round(user)
    # Сезон занятия — по его завершению, как его относит месячный счёт
    season_day = (quiz_session.completed_at
                  if quiz_session is not None and quiz_session.completed_at
                  else utcnow()).date()
    score_before = await _season_score(session, user, pair, season_day)

    # Первое законченное занятие — знакомство с уровнем (`first_lesson`):
    # «до» снимается раньше, чем счётчик прибавится
    first_completed = not is_error_repeat and not (user.quizzes_passed or 0)
    if not is_error_repeat:
        user.quizzes_passed = (user.quizzes_passed or 0) + 1
        # Первый урок кончился (патч 2.1, `quiz_service.in_first_lesson`)
        if getattr(user, "onboarded_at", None) is None:
            user.onboarded_at = utcnow()
        user.last_quiz_date = utctoday()
        if user.first_quiz_at is None:
            user.first_quiz_at = utcnow()

        learned_count = await session.execute(
            select(func.count())
            .select_from(UserWord)
            .where(
                UserWord.user_id == user.id,
                UserWord.learning_lang == pair.learning,
                UserWord.learned.is_(True),
            )
        )
        user.words_learned = int(learned_count.scalar() or 0)

    # Общая точность — по фактически отвеченным вопросам ВСЕХ завершённых
    # занятий, повторы ошибок включительно. Сумма их включала и прежде, а
    # пересчёт стоял только после обычного круга: круг 0/4, потом повтор
    # 4/4 — по данным 50%, у человека оставалось 0%.
    totals = await session.execute(
        select(
            func.coalesce(func.sum(QuizSession.answered_questions), 0),
            func.coalesce(func.sum(QuizSession.correct_answers), 0),
        ).where(
            QuizSession.user_id == user.id,
            QuizSession.completed_at.isnot(None),
        )
    )
    total_answered, total_correct = totals.one()
    user.success_rate = int(total_correct / total_answered * 100) if total_answered else 0

    await session.commit()

    place_before = None
    if not is_error_repeat:
        place_before = await _month_place(session, user.id)
        try:
            await update_monthly_stats(
                user_id=user.id, session=session, quiz_session_id=session_id
            )
        except Exception:
            logger.exception("Ошибка обновления месячной статистики (user=%s)", user.id)

        await update_user_activity(session, user.id, day=getattr(quiz_session, "local_day", None))

    # Разбор по словам
    result_items = await session.execute(
        select(QuizQuestion, Word)
        .join(Word, QuizQuestion.word_id == Word.id)
        .where(QuizQuestion.session_id == session_id)
        .order_by(QuizQuestion.answered_at)
    )
    items = result_items.all()

    details, channel_lines = _round_breakdown(items, pair, lang)

    placed: Optional[object] = None
    if (first_completed and quiz_session is not None
            and quiz_session.total_questions == FIRST_LESSON_LENGTH):
        placed = await _place_by_answers(session, user, pair, items)

    percentage = (correct_answers / answered * 100) if answered else 0.0

    prefix = "" if is_error_repeat else ""
    result_text = (
        f"{prefix}{get_text('quiz_completed', lang)}\n\n"
        f"{get_text('quiz_result_correct', lang, correct=correct_answers, total=answered)}\n"
        # Без десятой доли: «25.0%» обещает точность, которой в четырёх
        # вопросах нет
        f"{get_text('quiz_result_percentage', lang, percentage=round(percentage))}\n\n"
    )
    if channel_lines:
        result_text += "\n".join(channel_lines) + "\n\n"
    result_text += (
        f"{get_text('quiz_result_details', lang)}\n" + "\n".join(details)
    )

    if errors and not is_error_repeat:
        result_text += "\n\n" + get_text("quiz_result_errors", lang, count=len(errors))

    # ПООЩРЕНИЕ. Отдельным блоком в конце итога: разбор отвечает «что
    # вышло», поощрение — «ради чего возвращаться». Правило одно: хвалить
    # только за измеренное, иначе похвала обесценивает остальные числа.
    #
    # Круг-повтор поощрения НЕ получает: он не платит баллов, не двигает
    # серию и не считается пройденным кругом — сказать «+0 баллов» значило
    # бы сообщить о награде, которой нет.
    if not is_error_repeat:
        praise = await _praise_lines(
            session, user, pair, lang, items,
            quiz_session=quiz_session,
            answered=answered,
            correct=correct_answers,
            learned_before=learned_before,
            score_before=score_before,
            days_away=days_away,
            season_day=season_day,
        )
        if praise:
            result_text += "\n\n" + "\n".join(praise)
        race = await _race_lines(session, user, lang, place_before)
        if race:
            result_text += "\n\n" + "\n".join(race)
        await _mark_overtaken(session, user.id, place_before)

    # Сначала новое, потом удаление прежнего: иначе между ними на экране
    # один якорь (владелец, 15.10: «пропадает карточка и остаётся якорь,
    # как в начале, так и в конце»)
    await callback.bot.send_message(
        chat_id=callback.message.chat.id,
        text=result_text,
        reply_markup=get_results_keyboard(has_errors=bool(errors), lang=lang),
    )
    try:
        await callback.message.delete()
    except Exception:
        logger.debug("Не удалось удалить сообщение с вопросом", exc_info=True)

    # ПРЕДЛОЖИТЬ НАПОМИНАНИЯ — ЗДЕСЬ И БОЛЬШЕ НИГДЕ.
    #
    # Момент выбран не случайно: человек только что ЗАКОНЧИЛ круг, то есть
    # у нас есть доказательство, что бот ему годится, и это единственная
    # точка, где предложение не выглядит выпрашиванием. В онбординге
    # спрашивать нельзя — там он ещё не знает, нужны ли мы ему, и ответит
    # «нет», а второго раза правило не даёт.
    #
    # Отдельным сообщением, а не строкой в итоге: итог человек читает, а
    # предложение требует ответа, и смешивать их значит потерять либо
    # внимание к разбору, либо ответ.
    #
    # Отказ предложения не ломает ничего: круг уже засчитан и показан.
    if placed is not None:
        await _send_placement(callback, user, lang)
    elif not is_error_repeat:
        await _offer_what_fits(callback, session, user, lang)

    # Данные для повтора ошибок и репорта. После повтора ошибок сохраняем
    # список слов ОСНОВНОЙ викторины — репортить нужно её содержимое.
    saved_errors = list(errors)
    old_report_word_ids = data.get("report_word_ids", [])
    old_report_session_id = data.get("report_session_id")

    await state.clear()

    if is_error_repeat:
        await state.update_data(
            saved_errors=saved_errors,
            report_session_id=old_report_session_id,
            report_word_ids=old_report_word_ids,
        )
    else:
        await state.update_data(
            saved_errors=saved_errors,
            report_session_id=session_id,
            report_word_ids=[w.id for _, w in items],
        )
