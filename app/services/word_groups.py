"""
Построение word_lang_groups — схлопывание строк, дающих одно слово на языке.

База немецко-центричная: одна строка = немецкое слово + переводы. Если учить
не немецкий, разные строки начинают давать одинаковый headword:
Meeting / Sitzung / Treff / Versammlung все дают английское «meeting».
Без группировки это четыре карточки на одно слово и прогресс, размазанный
на четыре записи.

Дубли есть и в немецком — 131 слово повторяется на разных уровнях
(wirklich, einfach, genau), так что механизм нужен для всех пяти языков.

Таблица целиком производная от words. Пересобирается после любого изменения
словарной базы:
    python -m app.scripts.rebuild_word_groups
"""

from __future__ import annotations

import logging
from typing import Iterable, Optional

import sqlalchemy as sa
from sqlalchemy.engine import Connection

from app.services.language_service import (
    LANGUAGES,
    SUPPORTED_LANGS,
    get_language,
    normalize_headword,
)

logger = logging.getLogger(__name__)

_INSERT_CHUNK = 2000


def _group_key(
    norm: str,
    pos: Optional[str],
    article: Optional[str],
    lang: str,
) -> tuple:
    """
    Ключ схлопывания.

    Часть речи входит в ключ: «order» как существительное и как глагол —
    разные слова, объединять их нельзя.

    Для немецкого добавляется артикль: der See (озеро) и die See (море) —
    разные слова при одинаковом написании. В текущем датасете таких пар нет,
    но правка данных не должна ломать смысл.
    """
    if get_language(lang).uses_article:
        art = (article or "").strip().lower()
        if art == "-":
            art = ""
        return (norm, pos, art)
    return (norm, pos)


def _representative(rows: list[dict], prefer: Optional[set[int]] = None) -> dict:
    """
    Представитель группы: самое частотное слово, при равенстве — меньший id.
    Строки без frequency_rank уходят в конец, чтобы не побеждать по случайности.
    Выбор детерминирован — от него зависят прогресс и тесты.

    prefer — слова, которые обязаны победить, если они в группе. Это леммы из
    ручных указаний: форма может оказаться частотнее своей леммы, и тогда без
    этого канонической стала бы именно форма — ровно то, от чего указание и
    должно было избавить.
    """
    preferred = [r for r in rows if prefer and r["id"] in prefer]
    candidates = preferred or rows

    return min(
        candidates,
        key=lambda r: (
            r["frequency_rank"] is None,
            r["frequency_rank"] if r["frequency_rank"] is not None else 0,
            r["id"],
        ),
    )


def _load_overrides(connection: Connection) -> dict[int, int]:
    """
    Ручные указания «эта строка — форма, а лемма вот эта».

    Нужны для 99 пар, где форма и лемма лежат в базе как два отдельных слова:
    «komm» при существующем «kommen». Переименовать нельзя из-за уникальности
    (word_de, level), удалить нельзя из-за каскада на quiz_questions. Поэтому
    форма принудительно попадает в группу леммы.

    Отсутствие таблицы проверяется явно, а не через перехват любой ошибки.
    Прежде здесь стоял широкий except, и он спрятал настоящую причину, когда
    указания не применялись: пришлось искать её отладкой вместо чтения лога.
    Теперь «таблицы нет» — это одно, а любая другая ошибка выходит наружу.
    """
    if not sa.inspect(connection).has_table("word_lemma_overrides"):
        logger.debug("таблицы указаний лемм нет — схема старее нужной")
        return {}

    rows = connection.execute(
        sa.text("SELECT word_id, lemma_word_id FROM word_lemma_overrides")
    ).all()

    overrides = {word_id: lemma_id for word_id, lemma_id in rows if word_id != lemma_id}
    if overrides:
        logger.info("ручных указаний леммы: %d", len(overrides))
    return overrides


def build_groups(
    connection: Connection,
    langs: Optional[Iterable[str]] = None,
) -> dict[str, dict[str, int]]:
    """
    Пересобрать группы для указанных языков (по умолчанию все).

    Возвращает статистику по языкам: сколько строк учтено, сколько групп
    получилось, сколько строк схлопнулось.
    """
    langs = tuple(langs or SUPPORTED_LANGS)
    overrides = _load_overrides(connection)

    word_attrs = sorted({LANGUAGES[c].word_attr for c in langs if c in LANGUAGES})
    if not word_attrs:
        return {}

    select_list = ", ".join(["id", "pos::text AS pos", "article", "frequency_rank", *word_attrs])
    words = connection.execute(sa.text(f"SELECT {select_list} FROM words")).mappings().all()

    stats: dict[str, dict[str, int]] = {}

    for lang in langs:
        if lang not in LANGUAGES:
            logger.warning("Неизвестный язык %r — пропущен", lang)
            continue

        attr = LANGUAGES[lang].word_attr
        groups: dict[tuple, list[dict]] = {}

        # Ключ группы по слову: нужен, чтобы форма могла присоединиться к
        # группе своей леммы, а не образовать свою
        key_of: dict[int, tuple] = {}

        for row in words:
            norm = normalize_headword(row[attr], lang)
            if not norm:
                # Нет слова на этом языке — строка для него непригодна
                continue
            key_of[row["id"]] = _group_key(norm, row["pos"], row["article"], lang)

        for row in words:
            key = key_of.get(row["id"])
            if key is None:
                continue

            # Форма присоединяется к группе леммы, если на неё есть указание
            # и лемма пригодна для этого языка
            lemma_id = overrides.get(row["id"])
            if lemma_id is not None and lemma_id in key_of:
                key = key_of[lemma_id]

            groups.setdefault(key, []).append(
                {"id": row["id"], "frequency_rank": row["frequency_rank"]}
            )

        # Леммы из указаний обязаны быть каноническими в своих группах
        lemma_ids = set(overrides.values())

        payload: list[dict] = []
        for key, members in groups.items():
            canonical = _representative(members, lemma_ids)
            norm_key = key[0]
            for m in members:
                payload.append(
                    {
                        "lang": lang,
                        "word_id": m["id"],
                        "canonical_id": canonical["id"],
                        "is_canonical": m["id"] == canonical["id"],
                        "norm_key": norm_key[:255],
                    }
                )

        connection.execute(
            sa.text("DELETE FROM word_lang_groups WHERE lang = :lang"), {"lang": lang}
        )

        insert_sql = sa.text(
            """
            INSERT INTO word_lang_groups (lang, word_id, canonical_id, is_canonical, norm_key)
            VALUES (:lang, :word_id, :canonical_id, :is_canonical, :norm_key)
            """
        )
        for start in range(0, len(payload), _INSERT_CHUNK):
            connection.execute(insert_sql, payload[start:start + _INSERT_CHUNK])

        stats[lang] = {
            "rows": len(payload),
            "groups": len(groups),
            "collapsed": len(payload) - len(groups),
        }
        logger.info(
            "%s: %d строк → %d слов (схлопнуто %d)",
            lang, len(payload), len(groups), len(payload) - len(groups),
        )

    return stats


def remap_user_progress_to_canonical(connection: Connection) -> int:
    """
    Перевести существующий прогресс на канонические слова.

    Нужно после первой сборки групп: прогресс мог быть записан на строку,
    которая перестала быть представителем группы, и тогда стал бы невидимым.
    Счётчики объединяются: показы и правильные суммируются, streak и
    последний показ берутся максимальные, «выучено» — по логическому ИЛИ.

    Строки без группы (нет перевода на этот язык) не трогаются.
    """
    connection.execute(
        sa.text(
            """
            CREATE TEMPORARY TABLE uw_canonical AS
            SELECT
                uw.user_id,
                uw.learning_lang,
                g.canonical_id                AS word_id,
                MAX(uw.correct_streak)        AS correct_streak,
                SUM(uw.times_shown)           AS times_shown,
                SUM(uw.times_correct)         AS times_correct,
                MAX(uw.last_seen_at)          AS last_seen_at,
                BOOL_OR(uw.learned)           AS learned,
                MIN(uw.created_at)            AS created_at,
                MAX(uw.updated_at)            AS updated_at
            FROM user_words uw
            JOIN word_lang_groups g
              ON g.lang = uw.learning_lang AND g.word_id = uw.word_id
            GROUP BY uw.user_id, uw.learning_lang, g.canonical_id
            """
        )
    )

    connection.execute(
        sa.text(
            """
            DELETE FROM user_words uw
            USING word_lang_groups g
            WHERE g.lang = uw.learning_lang AND g.word_id = uw.word_id
            """
        )
    )

    result = connection.execute(
        sa.text(
            """
            INSERT INTO user_words
                (user_id, word_id, learning_lang, correct_streak, times_shown,
                 times_correct, last_seen_at, learned, created_at, updated_at)
            SELECT
                user_id, word_id, learning_lang, correct_streak, times_shown,
                times_correct, last_seen_at, learned, created_at, updated_at
            FROM uw_canonical
            """
        )
    )

    connection.execute(sa.text("DROP TABLE uw_canonical"))

    moved = result.rowcount or 0
    logger.info("Прогресс перепривязан на канонические слова: %d записей", moved)
    return moved
