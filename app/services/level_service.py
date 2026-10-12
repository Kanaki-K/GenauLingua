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

from app.database.enums import CEFRLevel
from app.database.models import QuizQuestion, QuizSession, User

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


def next_level(level: Optional[CEFRLevel]) -> Optional[CEFRLevel]:
    """Следующий уровень или None, если дальше некуда."""
    if level is None or level not in LEVEL_ORDER:
        return None
    index = LEVEL_ORDER.index(level)
    if index + 1 >= len(LEVEL_ORDER):
        return None
    return LEVEL_ORDER[index + 1]


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

    # Отказ относится к конкретному уровню: поднявшись своей волей, человек
    # снова услышит предложение — уже про следующий
    if user.level_offer_declined == user.level.value:
        return None

    answered, accuracy = await recent_accuracy(user, session)
    if answered < MIN_ANSWERS or accuracy < EASY_ACCURACY:
        return None

    return following


async def raise_level(user: User, session: AsyncSession, level: CEFRLevel) -> None:
    """Поднять уровень по согласию человека."""
    user.level = level
    # Прежний отказ относился к прежнему уровню и больше ничего не значит
    user.level_offer_declined = None
    await session.commit()


async def decline_level(user: User, session: AsyncSession) -> None:
    """Запомнить отказ, чтобы не спрашивать об этом же уровне снова."""
    if user.level is not None:
        user.level_offer_declined = user.level.value
        await session.commit()
