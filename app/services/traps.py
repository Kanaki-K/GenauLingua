"""
Варианты-ловушки для знакомых слов (владелец, 29.10.2026: «чтобы сами
карточки были сложнее в плане — тяжелее угадать… у нас тренажёр в первую
очередь»).

Прежде неверные варианты брались случайно из той же части речи и уровня, и
слово угадывалось без знания: «яблоко» среди «стол, бежать, синий»
отсекается по смыслу. Ловушка — вариант, который можно перепутать только не
зная слова. Три источника, по убыванию силы:

1. С ЧЕМ ПУТАЮТ ЛЮДИ. С 2.2.4 записывается, какой вариант выбран вместо
   верного (`quiz_questions.chosen_word_id`). Частая путаница учащих этот
   язык — лучшая ловушка: её не придумали, её показали ответы.
2. ПОХОЖИЕ НА ВИД. Bank — Band — Bart, kochen — kosten: то же начало и почти
   то же написание на изучаемом языке.
3. ИЗ ТОЙ ЖЕ ТЕМЫ. Слова одной категории и уровня — «вилка» среди «ложка,
   тарелка, кастрюля», а не среди «облако, бежать».

Всё считается на ИЗУЧАЕМОМ языке пары и по номерам слов — одно правило для
всех языков, без списков под язык.

ЛОВУШЕК НЕ БОЛЬШЕ ДВУХ: хотя бы один вариант остаётся обычным, вопрос
трудный, но честный. И только для знакомых слов (`is_familiar`): новое слово
человек видит впервые — с ловушками это была бы лотерея, а не тренировка.
"""
from __future__ import annotations

import difflib

from sqlalchemy import func, select

from app.database.models import QuizQuestion, QuizSession, UserWord, Word
from app.services.language_service import LanguagePair, fold, normalize_headword, word_column, word_text
from app.services.word_level import level_expr, level_of

TRAPS_MAX = 2
# Знакомое — с этой серии верных подряд (первое верное знакомство даёт 2)
FAMILIAR_STREAK = 2
# Похоже на вид — от этой доли совпадения написания (difflib, 0..1). Начало
# обязано совпасть двумя буквами, поэтому 0.5 не ловит случайного: Bank —
# Bart даёт ровно 0.5, Bank — Wolke ноль
LOOKALIKE_ENOUGH = 0.5
# Сколько слов того же начала перебирать в поисках похожих
LOOKALIKE_POOL = 200
CONFUSION_POOL = 5


async def is_familiar(session, user, word: Word, pair: LanguagePair) -> bool:
    """Слово знакомо человеку: серия верных от `FAMILIAR_STREAK` или выучено."""
    if user is None:
        return False
    row = (await session.execute(
        select(UserWord.correct_streak, UserWord.learned).where(
            UserWord.user_id == user.id,
            UserWord.word_id == word.id,
            UserWord.learning_lang == pair.learning,
        )
    )).first()
    return bool(row) and ((row.correct_streak or 0) >= FAMILIAR_STREAK or bool(row.learned))


def _headword(word: Word, lang: str) -> str:
    return fold(normalize_headword(word_text(word, lang, with_article=False), lang) or "")


def lookalike(a: str, b: str) -> float:
    """Похожесть написания двух заголовков (0..1)."""
    if not a or not b or a == b:
        return 0.0
    return difflib.SequenceMatcher(None, a, b).ratio()


async def trap_candidates(session, base, correct_word: Word, pair: LanguagePair) -> list[Word]:
    """
    Кандидаты в ловушки, сильнейшие первыми. `base` — запрос годных слов
    (`quiz_service._usable_words`): ловушка обязана быть словом, которое бот
    вообще показывает. Проверку «не совпадает ли значение» делает вызывающий.
    """
    found: list[Word] = []
    seen = {correct_word.id}

    def add(words):
        for w in words:
            if w.id not in seen:
                seen.add(w.id)
                found.append(w)

    # 1. С чем путают люди, учащие этот язык
    confused = (await session.execute(
        select(QuizQuestion.chosen_word_id, func.count().label("n"))
        .join(QuizSession, QuizSession.id == QuizQuestion.session_id)
        .where(
            QuizQuestion.word_id == correct_word.id,
            QuizQuestion.chosen_word_id.isnot(None),
            QuizQuestion.chosen_word_id != correct_word.id,
            QuizQuestion.is_correct.is_(False),
            QuizSession.learning_lang == pair.learning,
        )
        .group_by(QuizQuestion.chosen_word_id)
        .order_by(func.count().desc())
        .limit(CONFUSION_POOL)
    )).all()
    if confused:
        ids = [row.chosen_word_id for row in confused]
        rows = (await session.execute(base.where(Word.id.in_(ids)))).scalars().all()
        order = {wid: i for i, wid in enumerate(ids)}
        add(sorted(rows, key=lambda w: order[w.id]))

    # 2. Похожие на вид: та же часть речи, то же начало, близкое написание
    own = _headword(correct_word, pair.learning)
    if len(own) >= 3:
        column = func.lower(func.btrim(func.split_part(word_column(pair.learning), ",", 1)))
        rows = (await session.execute(
            base.where(Word.pos == correct_word.pos, func.left(column, 2) == own[:2])
            .limit(LOOKALIKE_POOL)
        )).scalars().all()
        scored = [(lookalike(own, _headword(w, pair.learning)), w) for w in rows]
        add(w for score, w in sorted(scored, key=lambda p: (-p[0], p[1].id))
            if score >= LOOKALIKE_ENOUGH)

    # 3. Та же тема, та же часть речи и уровень
    if correct_word.category:
        own_level = await level_of(session, correct_word, pair.learning)
        rows = (await session.execute(
            base.where(Word.category == correct_word.category, Word.pos == correct_word.pos,
                       level_expr(pair.learning) == own_level)
            .order_by(func.random()).limit(8)
        )).scalars().all()
        add(rows)

    return found
