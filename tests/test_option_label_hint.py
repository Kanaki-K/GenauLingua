# -*- coding: utf-8 -*-
"""
Кнопка — на одном языке (владелец, 29.10.2026): немецкая подсказка в скобках
перед значением, «(schläfrig sein) клонит в сон», на кнопку не попадает, даже
когда пример написан именно про это значение.
"""
from app.services.language_service import main_meaning, option_label
from tests.conftest import make_word


def test_hinted_meaning_gives_way_to_a_plain_one():
    word = make_word("schläfrig", ru="сонный, (schläfrig sein) клонит в сон")
    word.example_ru = "Меня клонит в сон"
    assert main_meaning(word, "ru").startswith("("), "пример выбирает значение с подсказкой"
    assert option_label(word, "ru") == "Сонный"


def test_only_hinted_meanings_lose_the_brackets():
    word = make_word("statuieren", uk="(ein Exempel statuieren) покарати для прикладу")
    assert option_label(word, "uk") == "Покарати для прикладу"


def test_brackets_at_the_end_stay():
    word = make_word("fehlen", uk="сумувати (за кимось)")
    assert option_label(word, "uk") == "Сумувати (за кимось)"
