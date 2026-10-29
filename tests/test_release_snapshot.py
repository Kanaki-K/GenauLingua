"""
Сверка выкатки пропускает склейку прогресса, но ловит потерю выученного.

Репетиция на копии прода 14.10: перенос словаря склеил 127 строк прогресса
(«kuck» → «gucken»), выученных стало 1 573 → 1 566 без единой потери, а
сверка сказала «СТОП» — и по инструкции выкатку пришлось бы откатить.
"""
import pytest

from app.scripts.release_snapshot import merge_bound_ok

BEFORE = {"user_words_rows": 21554, "uw_learned": 1573}


@pytest.mark.parametrize("rows,learned,ok", [
    (21427, 1566, True),    # склейка: убыль 7 при 127 склеенных строках
    (21427, 1573, True),    # склейка без двух выученных в одной паре
    (21554, 1566, False),   # строк столько же, а выученные пропали — потеря
    (21550, 1560, False),   # убыль выученных больше, чем склеено строк
    (21427, 1580, False),   # выученных больше, чем было, — не склейка
])
def test_learned_may_drop_only_within_merged_rows(rows, learned, ok):
    now = {"user_words_rows": rows, "uw_learned": learned}
    assert merge_bound_ok("uw_learned", BEFORE, now) is ok


def test_progress_rows_never_grow():
    assert merge_bound_ok("user_words_rows", BEFORE, {"user_words_rows": 21427})
    assert not merge_bound_ok("user_words_rows", BEFORE, {"user_words_rows": 21600})


def test_the_dictionary_may_only_grow():
    """2.3: перенос добавил 81 строку вторых значений — это не потеря; убыль — каскад прогресса."""
    from app.scripts.release_snapshot import merge_bound_ok
    assert merge_bound_ok("words", {"words": 12902}, {"words": 12983})
    assert not merge_bound_ok("words", {"words": 12902}, {"words": 12901})
