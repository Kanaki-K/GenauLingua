"""
Единая точка получения текущего времени.

datetime.utcnow() объявлен устаревшим в Python 3.12 и будет удалён.
Прямая замена на datetime.now(UTC) вернула бы datetime с таймзоной, а все
колонки в схеме — timestamp without time zone; смешивание наивных и
timezone-aware значений ломает сравнения на стороне Python.

Поэтому возвращаем наивный UTC, как и раньше, но без устаревшего вызова.
"""

from datetime import UTC, date, datetime


def utcnow() -> datetime:
    """Текущее время UTC без таймзоны — совместимо с колонками схемы."""
    return datetime.now(UTC).replace(tzinfo=None)


def utctoday() -> date:
    """Текущая дата по UTC."""
    return utcnow().date()
