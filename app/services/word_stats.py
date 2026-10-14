"""
Статистика по словам: какие действительно трудные, а какие просто редко показывались.

Прежде «сложные слова» отбирались по порогу «больше 5 показов» и сортировались
по доле верных ответов. При таком пороге список почти целиком состоит из шума:
при 8 показах результат 3/8 — обычный разброс для слова, которое знают на 70%.
На проде из 1359 слов с 5–8 показами ниже 50% оказалось 21 — ровно столько,
сколько и должно быть случайно.

Решение — доверительный интервал Вильсона. Важно взять правильную границу:

  * нижняя граница отвечает на вопрос «насколько хорошо слово знают в худшем
    случае» и используется, когда ищут заведомо хорошее (сортировка по убыванию);
  * верхняя граница отвечает «насколько хорошо слово знают в лучшем случае».
    Для поиска трудных слов нужна именно она: слово трудное, если даже
    оптимистичная оценка точности низкая.

Наглядно, почему нижняя граница здесь не годится:
    3/8   → нижняя 0.14, верхняя 0.70   (шум, мало данных)
    13/28 → нижняя 0.30, верхняя 0.65   (реально трудное слово)
По нижней границе первым окажется шумное 3/8, по верхней — 13/28.
"""

from __future__ import annotations

import math

from sqlalchemy import Float, cast, func

# Порог 95% — стандартный для доверительного интервала
Z_95 = 1.959963984540054

# Минимальное число показов, при котором вывод о слове осмысленен
MIN_SHOWS_FOR_DIFFICULTY = 15


def _wilson_parts(successes: int, total: int, z: float) -> tuple[float, float, float]:
    p = successes / total
    z2 = z * z
    center = p + z2 / (2 * total)
    margin = z * math.sqrt((p * (1 - p) + z2 / (4 * total)) / total)
    denominator = 1 + z2 / total
    return center, margin, denominator


def wilson_lower_bound(successes: int, total: int, z: float = Z_95) -> float:
    """Пессимистичная оценка доли верных ответов (95%)."""
    if total <= 0:
        return 0.0
    center, margin, denominator = _wilson_parts(successes, total, z)
    return max(0.0, (center - margin) / denominator)


def wilson_upper_bound(successes: int, total: int, z: float = Z_95) -> float:
    """
    Оптимистичная оценка доли верных ответов (95%).

    По возрастанию этой величины строится честный список трудных слов:
    наверху окажутся слова, которые плохо знают даже при благоприятной
    трактовке данных.
    """
    if total <= 0:
        return 1.0
    center, margin, denominator = _wilson_parts(successes, total, z)
    return min(1.0, (center + margin) / denominator)


def _wilson_parts_sql(successes, total, z: float):
    total_f = cast(total, Float)
    p = cast(successes, Float) / total_f
    z2 = z * z
    center = p + z2 / (2 * total_f)
    margin = z * func.sqrt((p * (1 - p) + z2 / (4 * total_f)) / total_f)
    denominator = 1 + z2 / total_f
    return center, margin, denominator


def wilson_lower_bound_sql(successes, total, z: float = Z_95):
    """Нижняя граница как SQL-выражение."""
    center, margin, denominator = _wilson_parts_sql(successes, total, z)
    return (center - margin) / denominator


def wilson_upper_bound_sql(successes, total, z: float = Z_95):
    """
    Верхняя граница как SQL-выражение — чтобы отбирать топ-N трудных слов
    на стороне БД, а не выгружать тысячи строк в Python.
    """
    center, margin, denominator = _wilson_parts_sql(successes, total, z)
    return (center + margin) / denominator


def difficulty_rank_sql(times_correct, times_shown, z: float = Z_95):
    """
    Выражение для сортировки по трудности: по возрастанию — от самых
    трудных к самым лёгким.
    """
    return wilson_upper_bound_sql(times_correct, times_shown, z)
