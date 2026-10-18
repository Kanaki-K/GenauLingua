"""
Уровень слова в изучаемом языке — одно правило для всего бота.

Немецкий — `Word.level` (списки Goethe). Остальные — `WordLevel` своего
языка (английский по Oxford, прочие — понятие + частота в языке); строки
нет — `Word.level`. Почему так, а не уровни Goethe для всех — в модели
`WordLevel`: сверка с Oxford 15.10 дала 22% слов, расходящихся на два
уровня и больше.

Отдельный модуль, а не функция в quiz_service: им пользуются и подбор слов,
и `level_service` (точность для подъёма), и доска — без кольцевых импортов.
"""
from __future__ import annotations

from typing import Optional

from sqlalchemy import func, select

from app.database.models import Word, WordLevel


def level_expr(lang: Optional[str]):
    """Выражение «уровень этого слова в языке `lang`» для запроса по `Word`."""
    if not lang or lang == "de":
        return Word.level
    own = (
        select(WordLevel.level)
        .where(WordLevel.word_id == Word.id, WordLevel.lang == lang)
        .correlate(Word)
        .scalar_subquery()
    )
    return func.coalesce(own, Word.level)


async def level_of(session, word: Word, lang: Optional[str]):
    """Уровень ЭТОГО слова в языке `lang` — значение, не выражение."""
    if not lang or lang == "de":
        return word.level
    own = (await session.execute(
        select(WordLevel.level).where(WordLevel.word_id == word.id, WordLevel.lang == lang)
    )).scalar()
    return own or word.level
