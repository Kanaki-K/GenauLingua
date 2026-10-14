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


# Порядок уровней для выбора младшего. Держится здесь, а не берётся из
# перечисления: порядок по возрастанию сложности — часть правила, а не
# случайный порядок объявления
_LEVEL_ORDER = {"A1": 0, "A2": 1, "B1": 2, "B2": 3, "C1": 4, "C2": 5}


def _representative(rows: list[dict], prefer: Optional[set[int]] = None) -> dict:
    """
    Представитель группы: самое частотное слово, при равенстве — меньший id.
    Строки без frequency_rank уходят в конец, чтобы не побеждать по случайности.
    Выбор детерминирован — от него зависят прогресс и тесты.

    prefer — слова, которые обязаны победить, если они в группе. Это леммы из
    ручных указаний: форма может оказаться частотнее своей леммы, и тогда без
    этого канонической стала бы именно форма — ровно то, от чего указание и
    должно было избавить.

    Одно и то же немецкое слово встречается в базе дважды на разных уровнях —
    209 слов, 216 лишних строк. Уровень при этом произволен: «Taxifahrer»
    лежит и на A1, и на B2. Побеждала старшая запись, потому что частотный
    ранг достался при импорте именно ей, а у младшей его нет — и ключ
    «ранга нет» отправлял её в конец. Получалось, что слово есть на A1, а
    видят его только на B2: у 14 слов ровно так и было.

    Поэтому после выбора победителя берётся самый младший уровень среди строк
    С ТЕМ ЖЕ немецким заголовком. Группы синонимов это не задевает: у
    «gucken/schauen/zuschauen» заголовки разные, и представителем остаётся
    самое частотное слово.
    """
    preferred = [r for r in rows if prefer and r["id"] in prefer]
    candidates = preferred or rows

    winner = min(
        candidates,
        key=lambda r: (
            r["frequency_rank"] is None,
            r["frequency_rank"] if r["frequency_rank"] is not None else 0,
            r["id"],
        ),
    )

    # Тот же заголовок на более младшем уровне — это та же единица, а не
    # другое слово. Частотный ранг тут ничего не говорит: он просто есть у
    # одной строки из двух
    same_word = [
        r for r in candidates
        if (r.get("word_de") or "").strip().lower()
        == (winner.get("word_de") or "").strip().lower()
    ]
    if len(same_word) > 1:
        return min(
            same_word,
            key=lambda r: (_LEVEL_ORDER.get(r.get("level"), len(_LEVEL_ORDER)), r["id"]),
        )
    return winner


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

    # Берём только те языковые колонки, которые в базе действительно есть.
    #
    # Эту функцию вызывает миграция d7e8f9a0b1c2 — живым кодом, чтобы правило
    # нормализации не разошлось с ним. Цена такой связи: когда в приложении
    # появился польский, миграция стала выбирать translation_pl, которого на
    # её шаге цепочки ещё нет — польский добавляется тремя ревизиями позже. На
    # пустой базе `alembic upgrade head` падал, и новое окружение было не
    # собрать. Пересечение с фактическими колонками снимает это навсегда: язык,
    # которого в схеме пока нет, просто пропускается.
    present = {
        row[0] for row in connection.execute(sa.text(
            "SELECT column_name FROM information_schema.columns "
            "WHERE table_name = 'words'"
        ))
    }
    missing = [c for c in langs
               if c in LANGUAGES and LANGUAGES[c].word_attr not in present]
    if missing:
        logger.warning(
            "В таблице words ещё нет колонок для языков %s — пропущены",
            " ".join(missing),
        )
    langs = tuple(c for c in langs if c not in set(missing))

    word_attrs = sorted({LANGUAGES[c].word_attr for c in langs if c in LANGUAGES})
    if not word_attrs:
        return {}

    # word_de и level нужны выбору представителя: одно и то же немецкое слово
    # лежит в базе на двух уровнях, и показывать его надо на младшем
    select_list = ", ".join(dict.fromkeys([
        "id", "pos::text AS pos", "article", "frequency_rank",
        "word_de", "level::text AS level", *word_attrs,
    ]))
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

            groups.setdefault(key, []).append({
                "id": row["id"],
                "frequency_rank": row["frequency_rank"],
                # Заголовок и уровень нужны выбору представителя: одно и то же
                # немецкое слово лежит на двух уровнях, показывать надо младший
                "word_de": row["word_de"],
                "level": row["level"],
            })

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


# КАК СКЛЕИВАТЬ КАЖДУЮ КОЛОНКУ ПРОГРЕССА — ПРАВИЛОМ, А НЕ СПИСКОМ.
# Прежде колонки были перечислены в запросе руками, и всё, что добавили
# позже (`learned_at`, счётчики «на слух», «вслух», «обратно»), при
# перепривязке молча стиралось: репетиция 14.10 — `learned_at` у 1 454 из
# 1 454 выученных стал пустым, `shown_audio` обнулился. Теперь колонки
# читаются из самой таблицы, а незнакомая останавливает перепривязку:
# лучше упасть, чем снова тихо потерять прогресс людей.
_KEYS = ("user_id", "learning_lang")
_SUM_PREFIXES = ("times_", "shown_", "correct_")
_MAX = {"correct_streak", "last_seen_at", "updated_at"}
_MIN = {"created_at", "learned_at"}   # выучено — по самому раннему переходу
_OR = {"learned"}


def _merge_rule(column: str) -> str:
    if column in _MAX:
        return f"MAX(uw.{column})"
    if column in _MIN:
        return f"MIN(uw.{column})"
    if column in _OR:
        return f"BOOL_OR(uw.{column})"
    if column.startswith(_SUM_PREFIXES):
        return f"SUM(uw.{column})"
    raise RuntimeError(
        f"user_words.{column}: не знаю, как склеивать эту колонку при "
        f"перепривязке — допишите правило в word_groups._merge_rule"
    )


def remap_user_progress_to_canonical(connection: Connection) -> int:
    """
    Перевести существующий прогресс на канонические слова.

    Нужно после первой сборки групп: прогресс мог быть записан на строку,
    которая перестала быть представителем группы, и тогда стал бы невидимым.
    Счётчики объединяются: показы и правильные суммируются, streak и
    последний показ берутся максимальные, «выучено» — по логическому ИЛИ,
    дата перехода в выученные — самая ранняя.

    Строки без группы (нет перевода на этот язык) не трогаются.
    """
    columns = connection.execute(
        sa.text(
            "SELECT column_name FROM information_schema.columns "
            "WHERE table_name = 'user_words' AND table_schema = current_schema() "
            "ORDER BY ordinal_position"
        )
    ).scalars().all()
    merged = [c for c in columns if c not in _KEYS and c != "word_id"]
    select_list = ",\n                ".join(
        [f"uw.{key}" for key in _KEYS]
        + ["g.canonical_id AS word_id"]
        + [f"{_merge_rule(c)} AS {c}" for c in merged]
    )
    target = ", ".join([*_KEYS, "word_id", *merged])

    connection.execute(
        sa.text(
            f"""
            CREATE TEMPORARY TABLE uw_canonical AS
            SELECT
                {select_list}
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
        sa.text(f"INSERT INTO user_words ({target}) SELECT {target} FROM uw_canonical")
    )

    connection.execute(sa.text("DROP TABLE uw_canonical"))

    moved = result.rowcount or 0
    logger.info("Прогресс перепривязан на канонические слова: %d записей", moved)
    return moved
