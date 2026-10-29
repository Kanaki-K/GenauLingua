"""
Исключённые слова (`app/data/excluded_words.json`) — владелец, 29.10.2026:
«у нас культурный бот». Строка в базе остаётся, но в группы не попадает, а
все выборки слов идут только через канонические строки групп.
"""
import json

import pytest

from app.services import word_groups
from app.services.word_groups import EXCLUDED_WORDS_FILE, load_excluded


def _listed():
    return json.loads(EXCLUDED_WORDS_FILE.read_text(encoding="utf-8"))["words"]


def test_every_entry_is_unique_and_explained():
    listed = _listed()
    assert len({e["id"] for e in listed}) == len(listed)
    assert all(e["word_de"] and e["why"] for e in listed)


def test_bumsen_and_the_crude_words_are_listed():
    words = {e["word_de"] for e in _listed()}
    for word in ("Porno", "Mistkerl", "kotzen", "Knast", "Fresse", "Vergewaltigung"):
        assert word in words


def test_matching_rows_are_excluded_and_absent_ids_skipped():
    first = _listed()[0]
    rows = [{"id": first["id"], "word_de": first["word_de"]}, {"id": -1, "word_de": "Haus"}]
    assert load_excluded(rows) == {first["id"]}


def test_wrong_word_under_the_id_stops_the_rebuild():
    first = _listed()[0]
    with pytest.raises(RuntimeError, match="не сходится"):
        load_excluded([{"id": first["id"], "word_de": "Haus"}])


def test_excluded_row_never_reaches_a_group(monkeypatch):
    """Пересборка на подставной базе: исключённая строка не попадает в группу."""
    first = _listed()[0]
    inserted = []

    class Result:
        def __init__(self, rows): self.rows = rows
        def mappings(self): return self
        def all(self): return self.rows
        def __iter__(self): return iter(self.rows)

    class Conn:
        def execute(self, stmt, params=None):
            sql = str(stmt)
            if "information_schema" in sql:
                return Result([("word_de",), ("translation_ru",)])
            if sql.startswith("SELECT") and "FROM words" in sql:
                return Result([
                    {"id": first["id"], "pos": "NOUN", "article": "", "frequency_rank": 1,
                     "word_de": first["word_de"], "level": "B2", "translation_ru": "слово"},
                    {"id": -5, "pos": "NOUN", "article": "", "frequency_rank": 2,
                     "word_de": "Haus", "level": "A1", "translation_ru": "дом"},
                ])
            if "INSERT INTO word_lang_groups" in sql:
                inserted.extend(params)
            return Result([])

    monkeypatch.setattr(word_groups, "_load_overrides", lambda conn: {})
    word_groups.build_groups(Conn(), ["ru"])
    assert [p["word_id"] for p in inserted] == [-5]
