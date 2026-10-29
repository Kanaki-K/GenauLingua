"""
Первое занятие — знакомство с уровнем (решение владельца 29.10.2026).

Восемь карточек «Читаю», по два новых слова уровней A1, A2, B1, B2 — от
лёгкого к трудному. Ответы показывают уровень, и с него человек учится
дальше (`recommend`, итог — `summary`).

ПОЧЕМУ ТАК, А НЕ ТРИ ИГРЫ ПО КРУГУ (прежний план 16.10: Читаю · Слышу ·
Вспоминаю и доска). Журнал 16–29.10: из 18 новичков, начавших занятие, 9
бросили первое же, и 7 из них — на втором вопросе, «Слышу», или сразу
после него: «не могу слушать», уход в настройки и рейтинг. И второе: взрослые
в первую минуту сами переставляли уровень с A1 на B1–C1 — для них A1
скучен, а спрашивать уровень на входе нельзя: «люди просто не знают свой
уровень» (владелец). Знакомство отвечает на оба: без звука, и уровень
определяется ответами, а не вопросом.

Слух, «Вспоминаю», доска приходят со второго занятия — по обычному правилу
допуска: на слух спрашивается слово, которое человек уже видел глазами.

Слова — частые и однословные (`quiz_service._easy`) и НЕ похожие на родные:
Taxi/такси угадывается без знания языка и уровень не показал бы.
"""
from __future__ import annotations

import difflib
import random
import unicodedata
from typing import Iterable, Optional

from app.database.enums import CEFRLevel

# Уровень слова на каждом номере вопроса знакомства
PLACEMENT = (
    CEFRLevel.A1, CEFRLevel.A1, CEFRLevel.A2, CEFRLevel.A2,
    CEFRLevel.B1, CEFRLevel.B1, CEFRLevel.B2, CEFRLevel.B2,
)
LADDER = (CEFRLevel.A1, CEFRLevel.A2, CEFRLevel.B1, CEFRLevel.B2)

# Доска первому занятию больше не ставится; размер остался для доски,
# открытой с домашнего экрана до первого занятия (`match.py`)
BOARD_PAIRS = 3

# Похоже на родное от этого порога (difflib, 0..1). Замер на парах
# de→ru/uk/en/pl/tr: от 0.6 идут Taxi/такси, Hotel/отель, Kaffee/кофе
SIMILAR_ENOUGH = 0.6

# Из скольких самых частых слов уровня выбирать
PLACEMENT_POOL = 40


def placement_level(question_number: int) -> CEFRLevel:
    """Уровень слова на этом месте знакомства; за его пределами — последний."""
    if question_number < 1:
        return PLACEMENT[0]
    return PLACEMENT[min(question_number, len(PLACEMENT)) - 1]


def recommend(answers: Iterable[tuple[CEFRLevel, bool]]) -> CEFRLevel:
    """
    Уровень по ответам знакомства: первая ступень, где ответ не сплошь
    верный. A1 2/2, A2 2/2, B1 1/2 — учиться на B1. Всё верно — B2, выше
    поднимает обычное предложение уровня по точности.

    Ступень засчитывается только ЦЕЛИКОМ: при четырёх вариантах один ответ
    угадывается в четверти случаев, два подряд — в шестнадцатой доле.
    Ступени, которой не было (оборванное занятие, нет слов уровня), —
    граница: выше неё ответы ничего не говорят.
    """
    by_level: dict[CEFRLevel, list[bool]] = {}
    for level, correct in answers:
        by_level.setdefault(level, []).append(bool(correct))
    for level in LADDER:
        got = by_level.get(level)
        if not got or not all(got):
            return level
    return LADDER[-1]


# Кириллица → латиница, грубо и нарочно: сравниваются очертания звуков, а
# не правописание. «кофе» → «kofe» рядом с «kaffee», «отель» → «otel»
_CYR = {
    "а": "a", "б": "b", "в": "v", "г": "g", "ґ": "g", "д": "d", "е": "e", "є": "ye",
    "ё": "yo", "ж": "zh", "з": "z", "и": "i", "і": "i", "ї": "yi", "й": "y", "к": "k",
    "л": "l", "м": "m", "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t",
    "у": "u", "ф": "f", "х": "h", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "sch",
    "ъ": "", "ы": "y", "ь": "", "э": "e", "ю": "yu", "я": "ya",
}


def _skeleton(text: str) -> str:
    """Слово в одной азбуке, без знаков, регистра и удвоений."""
    text = text.lower()
    text = "".join(_CYR.get(ch, ch) for ch in text)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if ch.isalpha())
    # «kaffee» и «kofe», «hotel» и «otel»: удвоения и h в начале не различаем
    out = []
    for ch in text:
        if not out or out[-1] != ch:
            out.append(ch)
    return "".join(out).lstrip("h")


def similarity(learning_text: str, native_text: str) -> float:
    a, b = _skeleton(learning_text), _skeleton(native_text)
    if not a or not b:
        return 0.0
    return difflib.SequenceMatcher(None, a, b).ratio()


def word_similarity(word, pair) -> float:
    """Насколько слово изучаемого языка похоже на своё значение."""
    from app.services.language_service import main_meaning, normalize_headword, word_text

    learning = normalize_headword(word_text(word, pair.learning, with_article=False), pair.learning)
    native = normalize_headword(main_meaning(word, pair.native) or "", pair.native)
    return similarity(learning, native)


async def placement_word(session, user, pair, level: CEFRLevel,
                         exclude_ids: list[int], taken_meanings: set[str]):
    """
    Новое слово уровня `level` для знакомства — частое, однословное, не
    похожее на родное и со значением, ещё не спрошенным в этом занятии.

    None — таких слов уровня нет (тонкий язык); тогда место займёт обычный
    подбор новых слов.
    """
    from sqlalchemy import and_

    from app.database.models import Word, WordFrequency
    from app.services.quiz_service import _easy, _function_word_penalty, _meaning_key, _unseen_query
    from app.services.word_level import level_expr

    query = _easy(_unseen_query(user.id, pair, exclude_ids, None, None), pair)
    query = query.where(level_expr(pair.learning) == level)
    rows = await session.execute(
        query.outerjoin(
            WordFrequency,
            and_(WordFrequency.word_id == Word.id, WordFrequency.lang == pair.learning),
        )
        .order_by((WordFrequency.zipf - _function_word_penalty()).desc().nulls_last(), Word.id)
        .limit(PLACEMENT_POOL)
    )
    candidates = list(rows.scalars().all())
    random.shuffle(candidates)
    for word in candidates:
        meaning = _meaning_key(word, pair.native)
        if meaning and meaning in taken_meanings:
            continue
        if word_similarity(word, pair) >= SIMILAR_ENOUGH:
            continue
        return word
    return None
