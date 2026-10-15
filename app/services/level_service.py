"""
Уровень: когда он стал лёгким и пора предложить следующий.

ЗАМЕР, ИЗ-ЗА КОТОРОГО ПРИЗНАК ПРИШЛОСЬ ПОМЕНЯТЬ

В `ROADMAP.md` §3.5 правило было записано так: «если 90% слов уровня
освоены — предложить следующий». Замер по всей базе показал, что оно не
сработало бы НИ РАЗУ:

    людей с уровнем                      233
    освоили >= 90% слов своего уровня      0
    освоили >= 10% слов своего уровня      0
    лучший показатель                    9.5%  (117 слов из 1235, A1)

Причина не в людях, а в арифметике: в A1 тысяча двести слов, и дойти до
девятисот — это сотни кругов. Правило описывало событие, которого в жизни
бота не случится.

ПРИЗНАК, КОТОРЫЙ СРАБАТЫВАЕТ, — НЕ ОХВАТ, А ТОЧНОСТЬ

Вопрос ведь не «прошёл ли человек уровень», а «не стал ли уровень лёгким»,
и на него отвечает доля верных ответов:

    уровень   людей с опытом 20+ вопросов   из них точность >= 90%
    A1                62                        35
    B1                41                        29
    A2                21                         8

Тридцать пять человек из шестидесяти двух на A1 отвечают верно в девяти
случаях из десяти. Им уровень и правда лёгок — и это видно СЕЙЧАС, а не
через сотни кругов.

СЧИТАЕТСЯ ПО ПОСЛЕДНИМ ОТВЕТАМ, А НЕ ЗА ВСЮ ЖИЗНЬ. Человек учится, и
точность первых кругов к сегодняшнему дню отношения не имеет: за всю
жизнь она усредняется и предложение приходит с опозданием на месяцы.
"""

from __future__ import annotations

import logging
from typing import Optional

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.enums import CEFRLevel, QuizMode
from app.database.models import QuizQuestion, QuizSession, User, Word

logger = logging.getLogger(__name__)

# Порядок уровней. Берётся отсюда, а не из порядка объявления перечисления:
# перечисление может быть пересортировано при любой правке, и «следующий»
# тихо поедет.
LEVEL_ORDER = [
    CEFRLevel.A1, CEFRLevel.A2, CEFRLevel.B1,
    CEFRLevel.B2, CEFRLevel.C1, CEFRLevel.C2,
]

# Сколько последних ответов смотреть. Тридцать — два круга по пятнадцать:
# меньше одного круга это шум, а больше трёх уже описывает не сегодняшнего
# человека.
RECENT_ANSWERS = 30

# Сколько ответов нужно, чтобы вообще судить. Двадцать — порог, на котором
# замерена таблица выше; при меньшем числе одна ошибка двигает точность на
# пять пунктов, и предложение становится лотереей.
MIN_ANSWERS = 20

# С какой точности уровень считается лёгким. Девяносто — не круглое число
# ради красоты: при четырёх вариантах случайное попадание даёт 25%, а
# девять верных из десяти подряд угадать нельзя. На этом пороге признак
# отделяет 35 человек из 62 на A1 — то есть он и различает, и не метит во
# всех подряд.
EASY_ACCURACY = 0.90

# Через сколько занятий после отказа предложить снова (при той же точности)
REOFFER_AFTER_ROUNDS = 5

# БЫСТРЫЙ ПУТЬ ДЛЯ НОВИЧКА. Прод 15.10: новички, знающие язык, отвечали на
# всё верно за 4–15 секунд и уходили после первых слов, не дождавшись
# двадцати ответов: A1 им был скучен. Один новичок дотерпел, на 30-м ответе
# принял B1 — и остался. Владелец: «2 круга с высокой точностью — явно
# знает», «плюс у него есть выбор остаться», «сделай по-умному».
#
# Поэтому первые занятия судятся по ОДНОМУ: шесть ответов (короткое первое
# занятие — семь вопросов) и не больше одной ошибки на семь. Человек,
# знающий язык, поднимается на уровень за занятие, пока не дойдёт до
# своего; дальше действует обычное правило — два занятия.
NEWCOMER_LESSONS = 3
NEWCOMER_MIN_ANSWERS = 6
NEWCOMER_ACCURACY = 0.85


# ПОНИЖЕНИЕ — ОБРАТНАЯ СТОРОНА ВЫБОРА. Раз уровень можно выбрать одним
# нажатием, человек может и переоценить себя: встать на C1 и ошибаться
# через слово. Признак — меньше 60% верных за два занятия (20 ответов):
# угадывание из четырёх даёт 25%, нормальная учёба — 85–90% (прод 15.10:
# «Читаю» 87%, «Вспоминаю» 90%). Тоже предложение, а не молча; отказ —
# спросим снова через те же 5 занятий. Отказ записывается как «B2:down»,
# чтобы не путать его с отказом подняться
LOWER_ACCURACY = 0.60
LOWER_MIN_ANSWERS = MIN_ANSWERS
DOWN_MARK = ":down"


def previous_level(level: Optional[CEFRLevel]) -> Optional[CEFRLevel]:
    """Предыдущий уровень или None, если ниже некуда."""
    if level is None or level not in LEVEL_ORDER:
        return None
    index = LEVEL_ORDER.index(level)
    return LEVEL_ORDER[index - 1] if index > 0 else None


def _declined_recently(user: User, mark: str) -> bool:
    """Отказывался ли человек от этого предложения меньше 5 занятий назад."""
    if user.level_offer_declined != mark:
        return False
    declined_at = getattr(user, "level_offer_declined_round", None)
    played_since = (user.quizzes_passed or 0) - (declined_at or 0)
    return declined_at is None or played_since < REOFFER_AFTER_ROUNDS


async def should_offer_lower_level(
    user: User, session: AsyncSession
) -> Optional[CEFRLevel]:
    """Слишком ли трудно: меньше 60% верных за два занятия. Возвращает уровень ниже."""
    previous = previous_level(user.level)
    if previous is None or not level_drives_words(user):
        return None
    if _declined_recently(user, user.level.value + DOWN_MARK):
        return None
    answered, accuracy = await recent_accuracy(user, session)
    if answered < LOWER_MIN_ANSWERS or accuracy >= LOWER_ACCURACY:
        return None
    return previous


async def lower_level(user: User, session: AsyncSession, target: CEFRLevel) -> bool:
    """Опустить на уровень ниже по согласию. Только на соседний; иначе кнопка устарела."""
    if target is None or target != previous_level(user.level):
        return False
    user.level = target
    # Без качелей: человек только что ушёл с уровня выше, и предлагать его
    # снова через два лёгких занятия значило бы гонять туда-сюда. Записано
    # как отказ подняться с нового уровня — спросим через те же 5 занятий
    user.level_offer_declined = target.value
    user.level_offer_declined_round = user.quizzes_passed or 0
    await session.commit()
    return True


async def decline_lower_level(
    user: User, session: AsyncSession, offered: Optional[CEFRLevel]
) -> bool:
    """Остаться на трудном уровне: спросим снова через 5 занятий."""
    if offered is None or offered != previous_level(user.level):
        return False
    user.level_offer_declined = user.level.value + DOWN_MARK
    user.level_offer_declined_round = user.quizzes_passed or 0
    await session.commit()
    return True


def is_newcomer(user: User) -> bool:
    """Первые занятия человека — уровень судится по одному занятию."""
    return (getattr(user, "quizzes_passed", 0) or 0) <= NEWCOMER_LESSONS


def _thresholds(user: User) -> tuple[int, float]:
    """Сколько ответов и какая точность нужны, чтобы предложить уровень."""
    if is_newcomer(user):
        return NEWCOMER_MIN_ANSWERS, NEWCOMER_ACCURACY
    return MIN_ANSWERS, EASY_ACCURACY


def next_level(level: Optional[CEFRLevel]) -> Optional[CEFRLevel]:
    """Следующий уровень или None, если дальше некуда."""
    if level is None or level not in LEVEL_ORDER:
        return None
    index = LEVEL_ORDER.index(level)
    if index + 1 >= len(LEVEL_ORDER):
        return None
    return LEVEL_ORDER[index + 1]


def level_drives_words(user: User) -> bool:
    """
    Подбирает ли уровень слова в текущем режиме человека.

    То же правило, что `quiz_service._apply_quiz_mode_filter`: уровнем
    отбирают «По уровню» и «По теме» без выбранной темы (там откат на
    уровень); «По теме» с темой, «Все слова» и «Сложные» уровня не
    смотрят вовсе — «Сложные» берут трудные слова человека по всей базе.

    Зачем: предложение «перейти на A2» приходило и в этих режимах, где от
    смены уровня не меняется ни одно слово, — согласие было бы обманом.
    """
    mode = getattr(user, "quiz_mode", None)
    if mode == QuizMode.CATEGORY:
        return not getattr(user, "quiz_category", None)
    return mode not in (QuizMode.ALL_WORDS, QuizMode.DIFFICULT)


async def recent_accuracy(user: User, session: AsyncSession) -> tuple[int, float]:
    """
    Доля верных ответов по последним `RECENT_ANSWERS` вопросам.

    Считается по вопросам ЭТОГО ЖЕ уровня и этого же изучаемого языка:
    точность на английском ничего не говорит о трудности немецкого A1, а
    ответы, данные на другом уровне, — тем более.

    Возвращает (сколько ответов учтено, доля верных).
    """
    rows = (await session.execute(
        select(QuizQuestion.is_correct)
        .join(QuizSession, QuizSession.id == QuizQuestion.session_id)
        # ТОЛЬКО СЛОВА ЭТОГО УРОВНЯ. Повторение начатых слов идёт с любого
        # уровня (`quiz_service._review_scoped`), и половину занятия может
        # занять отработка прежнего: прыгнувший A1→B1 набрал бы 90% на
        # повторах A1 и получил бы «выше» снова, а на C1 лёгкие повторы не
        # дали бы сработать понижению. Находка независимой проверки 15.10
        .join(Word, Word.id == QuizQuestion.word_id)
        .where(Word.level == user.level)
        .where(
            QuizSession.user_id == user.id,
            QuizSession.learning_lang == user.learning_lang,
            QuizSession.level == user.level,
            QuizQuestion.is_correct.isnot(None),
        )
        # Порядок по времени ответа, а `id` вторым ключом — не для красоты:
        # `answered_at` у вопроса может не стоять вовсе (круг брошен,
        # вопрос показан и не отвечен), и на одних только NULL порядок
        # становится произвольным. Тогда «последние тридцать» оказываются
        # случайными тридцатью, и предложение приходит невпопад — молча,
        # потому что ответ всё равно похож на правду. `id` монотонен всегда.
        .order_by(desc(QuizQuestion.answered_at), desc(QuizQuestion.id))
        .limit(RECENT_ANSWERS)
    )).scalars().all()

    if not rows:
        return 0, 0.0
    return len(rows), sum(1 for ok in rows if ok) / len(rows)


async def should_offer_next_level(
    user: User, session: AsyncSession
) -> Optional[CEFRLevel]:
    """
    Пора ли предложить следующий уровень. Возвращает его или None.

    ПРЕДЛОЖИТЬ, А НЕ ПЕРЕКЛЮЧИТЬ. Уровень человек ставил руками, и молча
    менять то, что человек выставил сам, читается как поломка, а не как
    забота. Правило из `ROADMAP.md` §3.5 дословно: «Не переключать молча, а
    СПРОСИТЬ».
    """
    following = next_level(user.level)
    if following is None:
        return None

    # Уровень не подбирает слова в этом режиме — поднимать его незачем
    if not level_drives_words(user):
        return None

    # Отказ относится к конкретному уровню: поднявшись своей волей, человек
    # снова услышит предложение — уже про следующий.
    #
    # И ОТКАЗ НЕ НАВСЕГДА. Прежде на этом уровне бот не спрашивал больше
    # никогда, даже когда человек давно его перерос. Владелец, 14 октября:
    # «если он ещё 5 игр будет на высоком уровне — предлагаем перейти».
    # Через пять занятий после отказа — снова, если точность всё ещё высокая
    # (ниже); новый отказ начинает отсчёт заново
    if user.level_offer_declined == user.level.value:
        declined_at = getattr(user, "level_offer_declined_round", None)
        played_since = (user.quizzes_passed or 0) - (declined_at or 0)
        if declined_at is None or played_since < REOFFER_AFTER_ROUNDS:
            return None

    answered, accuracy = await recent_accuracy(user, session)
    need_answers, need_accuracy = _thresholds(user)
    if answered < need_answers or accuracy < need_accuracy:
        return None

    return following


async def raise_level(user: User, session: AsyncSession, level: CEFRLevel) -> bool:
    """
    Поднять уровень по согласию человека. False — кнопка устарела.

    ТОЛЬКО НА СЛЕДУЮЩИЙ ЗА ТЕКУЩИМ. Предложение остаётся в переписке, и
    кнопка «Да, перейти на A2», нажатая, когда человек уже сам поднялся до
    B1, прежде ОПУСКАЛА его на A2: уровень ставился из кнопки как есть.
    Устаревшая кнопка теперь ничего не меняет.
    """
    if level is None or level != next_level(user.level):
        logger.info("устаревшее предложение уровня: у человека %s, в кнопке %s",
                    getattr(user.level, "value", user.level),
                    getattr(level, "value", level))
        return False
    user.level = level
    # Прежний отказ относился к прежнему уровню и больше ничего не значит
    user.level_offer_declined = None
    user.level_offer_declined_round = None
    await session.commit()
    return True


async def decline_level(
    user: User, session: AsyncSession, offered: Optional[CEFRLevel] = None,
) -> bool:
    """
    Запомнить отказ, чтобы не спрашивать об этом же уровне снова.

    `offered` — уровень, который предлагала нажатая кнопка. Если он уже не
    следующий за текущим (человек сменил уровень сам), кнопка устарела:
    отказ от «A1 → A2», нажатый на A2, записал бы отказ от «A2 → B1», о
    котором человека не спрашивали. Без `offered` (кнопки старого вида)
    отказ пишется к текущему уровню, как прежде. False — ничего не записано.
    """
    if offered is not None and offered != next_level(user.level):
        return False
    if user.level is not None:
        user.level_offer_declined = user.level.value
        user.level_offer_declined_round = user.quizzes_passed or 0
        await session.commit()
        return True
    return False


async def jump_to_level(user: User, session: AsyncSession, target: CEFRLevel) -> bool:
    """
    Перейти сразу на выбранный уровень — выше текущего. False — кнопка устарела.

    ВЫБОР ДЛЯ НОВИЧКА, А НЕ ЛЕСЕНКА. Подъём по одной ступени за занятие
    заставлял сильного человека гонять A1, A2, B1 подряд — три скучных
    занятия, прежде чем станет интересно. Владелец, 15.10: «нужно угодить и
    новичкам и более продвинутым. Людям не очень интересно несколько кругов
    гонять, и скорее всего не полезут в настройки». Поэтому новичку под
    итогом — выбор A2 / B1 / B2 / C1 одним нажатием.

    Только ВВЕРХ: кнопка, нажатая после того, как человек уже поднялся сам,
    не должна опустить его обратно.
    """
    if (target not in LEVEL_ORDER or user.level not in LEVEL_ORDER
            or LEVEL_ORDER.index(target) <= LEVEL_ORDER.index(user.level)):
        return False
    user.level = target
    user.level_offer_declined = None
    user.level_offer_declined_round = None
    await session.commit()
    return True

