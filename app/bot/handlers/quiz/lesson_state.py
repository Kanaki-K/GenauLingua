"""
Состояние занятия: ключи, замок чата и «один вопрос — один ответ».

Общее для всех игр круга — карточки, слуха, речи, доски и сборки. Замок
чата (`_claim_locks`) — ОДИН словарь на всё приложение: ответы, «Далее»,
доска и сетка сборки решают про один и тот же чат.

Вынесено из `game.py` переносом, без правок поведения.
"""

import asyncio
import logging
import time
import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from aiogram.fsm.context import FSMContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


# ============================================================================
# ОДИН ВОПРОС — ОДИН ОТВЕТ
# ============================================================================

# Номер вопроса, на который ответ УЖЕ принят. Пока он равен текущему,
# второй ответ не считается.
S_ANSWERED = "answered_question"

# КТО И КОГДА ПОСТАВИЛ ОТМЕТКУ. С 2.1 состояние живёт в Redis и переживает
# процесс; отметка, поставленная процессом, который умер посреди ответа
# (выкатка, сбой), запирала вопрос на двое суток: следующее голосовое,
# «Пропустить» и «Далее» гасились как повтор (аудит 2.1). Отметка чужого
# процесса — уже не «ответ в пути»: её смотрим по базе (`_claim_answer`).
BOOT = uuid.uuid4().hex
S_CLAIM_BOOT = "claim_boot"
S_CLAIM_AT = "claim_at"

# Замки по чатам. Нужны потому, что отметка «ответ принят» читается и
# пишется двумя отдельными await, а aiogram обрабатывает обновления
# ПАРАЛЛЕЛЬНО: два нажатия, пришедшие в один миг, успели бы оба прочитать
# «ещё не отвечено». Замок на чат сводит решение к одному потоку.
#
# Словарь НЕ чистится. Прежде `_finish_quiz` выбрасывал замок, пока второе
# «Далее» его ещё ждало, — и следующий вызов получал НОВЫЙ замок, то есть
# два обработчика шли параллельно. Замок — несколько сотен байт на чат,
# у бота 233 человека: держать их все дешевле, чем ловить такую гонку.
_claim_locks: dict[int, asyncio.Lock] = {}


def _claim_lock(chat_id: int) -> asyncio.Lock:
    lock = _claim_locks.get(chat_id)
    if lock is None:
        lock = asyncio.Lock()
        _claim_locks[chat_id] = lock
    return lock


async def _answer_recorded_since(session: AsyncSession, session_id, since: float) -> bool:
    """Записан ли в занятии ответ после момента отметки (секунды эпохи, UTC)."""
    from app.database.models import QuizQuestion

    # База хранит наивное UTC; utcfromtimestamp устарел (в тестах — ошибка)
    moment = datetime.fromtimestamp(since, timezone.utc).replace(tzinfo=None) - timedelta(seconds=2)
    return (await session.execute(
        select(QuizQuestion.id).where(QuizQuestion.session_id == session_id,
                                      QuizQuestion.answered_at >= moment).limit(1)
    )).first() is not None


async def answered_by_dead_process(state: FSMContext, session: AsyncSession) -> bool:
    """
    Ответ на текущий вопрос записан процессом, который умер, не показав
    разбора (аудит 2.1: убит между записью в базу и правкой карточки).
    Тогда кнопки «Далее» на экране нет, а вариант гасится как повтор —
    вызывающий должен дать «Далее», не записывая ответ второй раз.
    Отметка переписывается на этот процесс: «Далее» выдаётся один раз.
    """
    data = await state.get_data()
    current = data.get("current_question")
    if (current is None or data.get(S_ANSWERED) != current
            or data.get(S_CLAIM_BOOT) in (None, BOOT) or data.get("session_id") is None):
        return False
    if not await _answer_recorded_since(session, data["session_id"],
                                        float(data.get(S_CLAIM_AT) or 0)):
        return False
    await state.update_data(**{S_CLAIM_BOOT: BOOT})
    return True


async def _claim_answer(state: FSMContext, chat_id: int,
                        session: Optional[AsyncSession] = None) -> bool:
    """
    Принять ответ на текущий вопрос РОВНО ОДИН РАЗ.

    ЗАЧЕМ. Один вопрос умел записаться дважды, и замер по рабочей копии это
    подтвердил: 31 вопрос получил по две строки и больше, 50 лишних строк в
    30 занятиях. Разрыв между двойными ответами — от 0.00 с до 78 с, то
    есть беда приходила двумя разными путями:

        0.00 с   двойной тык: оба нажатия пришли раньше, чем карточка
                 успела перерисоваться и спрятать варианты
        78 с     правка карточки не удалась, варианты остались на экране,
                 и человек нажал снова

    Следствие в обоих случаях одно: балл за вопрос начисляется дважды,
    прогресс по слову двигается дважды, а в занятии оказывается больше
    отвеченных, чем было запланировано (таких занятий 14).

    Возвращает False, если ответ на этот вопрос уже принят, — тогда
    вызывающий молча гасит нажатие. Ругаться не за что: человек не
    виноват, что карточка не поспела.
    """
    async with _claim_lock(chat_id):
        data = await state.get_data()
        current = data.get("current_question")
        if current is None:
            # Круги, начатые до этой правки: номера в состоянии нет, и
            # отказывать им значило бы сломать уже идущее занятие
            return True
        if data.get(S_ANSWERED) == current:
            stale = (session is not None and data.get(S_CLAIM_BOOT) not in (None, BOOT)
                     and data.get("session_id") is not None)
            if not stale or await _answer_recorded_since(
                    session, data["session_id"], float(data.get(S_CLAIM_AT) or 0)):
                return False
            logger.warning("вопрос %s занят умершим процессом и не записан — освобождаю", current)
        await state.update_data(**{S_ANSWERED: current, S_CLAIM_BOOT: BOOT,
                                   S_CLAIM_AT: time.time()})
        return True


# Что переживает круг: ошибки для повтора и слова для жалобы на перевод
# относятся к ПРОШЛОМУ итогу и нужны его кнопкам.
#
# И отметка «повтор с этого итога уже начат» (`S_REPEAT_FROM`): повтор сам
# начинается со сброса состояния, и без неё второе нажатие той же кнопки
# не узнало бы, что первое уже прошло.
S_REPEAT_FROM = "repeat_started_from"
_KEEP_BETWEEN_ROUNDS = ("saved_errors", "report_session_id", "report_word_ids",
                        S_REPEAT_FROM)


async def _reset_round_state(state: FSMContext) -> dict:
    """
    Начать круг с чистого состояния. Возвращает то, что сохранено.

    Прежде новый круг ДОПИСЫВАЛ своё поверх прежнего. Из брошенного круга
    оставались `answered_question`, `board_shown` и ключи доски: бросил на
    первом вопросе, нажал «Учить» — и первый ответ нового круга гасился как
    повтор, человек застревал. Оставшийся `board_shown` к тому же убирал
    доску из нового круга.
    """
    data = await state.get_data()
    kept = {k: data[k] for k in _KEEP_BETWEEN_ROUNDS if k in data}
    await state.clear()
    if kept:
        await state.update_data(**kept)
    return kept


# Сообщения вокруг вопроса «Говорю», которые убираются при переходе дальше:
# голосовые человека, «Не разобрал…», присланный эталон.
S_STRAY = "stray_message_ids"

# Попытки голосом на текущем вопросе. ДВЕ: после второй неудачи вопрос
# проходит пропуском — без балла и без ошибки (`speech._give_up`)
S_SPEECH_TRIES = "speech_tries"
SPEECH_ATTEMPTS = 2


async def _remember_stray(state: FSMContext, *message_ids: int) -> None:
    # Под замком чата: две записи, пришедшие разом, дописывают список
    # одновременно, и без замка одна из них терялась бы. Вызывающие замок
    # не держат — иначе здесь была бы взаимная блокировка
    async with _claim_lock(state.key.chat_id):
        data = await state.get_data()
        stray = list(data.get(S_STRAY) or [])
        stray.extend(i for i in message_ids if i)
        await state.update_data(**{S_STRAY: stray})


async def _sweep_stray(bot, chat_id: int, state: FSMContext) -> None:
    """
    Убрать голосовые и служебные сообщения прошлого вопроса.

    Живой тест владельца 14 октября: «после голосового ответа — новый
    вопрос не удаляет сообщения юзера, и его аудио просто висит в чате».
    Карточка круга одна и правится на месте, а голосовое человек присылает
    сам — его карточка не накрывает. Пока виден разбор, голосовое остаётся:
    его можно сравнить с эталоном. Уходит оно при переходе дальше.
    """
    data = await state.get_data()
    stray = data.get(S_STRAY) or []
    if not stray:
        return
    await state.update_data(**{S_STRAY: []})
    for message_id in stray:
        try:
            await bot.delete_message(chat_id, message_id)
        except Exception:
            logger.debug("сообщение %s не удалилось", message_id, exc_info=True)


async def _recover(session: AsyncSession, *objects) -> None:
    """
    Откатить сессию после упавшей записи и перечитать нужные дальше объекты.

    Откат помечает все объекты сессии просроченными, а ленивая подгрузка в
    асинхронной сессии невозможна: первое же чтение поля упало бы. Поэтому
    перечитываем явно.
    """
    await session.rollback()
    for obj in objects:
        if obj is not None:
            await session.refresh(obj)


async def _release_answer(state: FSMContext, chat_id: int) -> None:
    """
    Вернуть вопрос в «не отвечен», если ответ на него так и не записан.

    Нужна речи: голосовое занимает вопрос ДО распознавания, а неразобранная
    запись ответом не считается — бот просит записать ещё раз. Без возврата
    вопрос оставался занятым навсегда: следующее голосовое и «Пропустить»
    гасились как повтор, и выйти из круга было нельзя.
    """
    async with _claim_lock(chat_id):
        data = await state.get_data()
        if data.get(S_ANSWERED) == data.get("current_question"):
            await state.update_data(**{S_ANSWERED: None})


DEFAULT_QUIZ_LENGTH = 15

# Длина занятия — `quiz_service.lesson_length` (первое занятие короче)
from app.services.quiz_service import FIRST_LESSON_LENGTH, lesson_length  # noqa: E402,F401


# Ключ состояния: доска в этом круге уже была. Один круг — одна доска:
# вторая превратила бы занятие в сопоставление с довеском из вопросов.
S_BOARD_DONE = "board_shown"


# С какого номера круг уже продвинут кнопкой «Далее»
S_ADVANCED = "advanced_from"
S_ADVANCE_BOOT = "advanced_boot"


async def _claim_advance(state: FSMContext, chat_id: int) -> bool:
    """
    Продвинуть круг с текущего номера РОВНО ОДИН РАЗ.

    Двойное «Далее» на последнем вопросе завершало круг дважды: два экрана
    итога, `quizzes_passed` +2, а однажды второй обработчик упал на
    уникальном ключе месячного счёта. На середине круга двойной тык
    пропускал вопрос. Замок тот же, что у ответа: оба решения про один чат.
    """
    async with _claim_lock(chat_id):
        data = await state.get_data()
        current = data.get("current_question")
        if current is None:
            return True
        if data.get(S_ADVANCED) == current:
            # «Далее» умершего процесса: следующий вопрос так и не показан.
            # Двойного продвижения тут нет — тот процесс мёртв (аудит 2.1)
            if data.get(S_ADVANCE_BOOT) in (None, BOOT):
                return False
            logger.warning("«Далее» с вопроса %s оборвано перезапуском — повторяю", current)
        await state.update_data(**{S_ADVANCED: current, S_ADVANCE_BOOT: BOOT})
        return True
