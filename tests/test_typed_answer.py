# -*- coding: utf-8 -*-
"""Сравнение ответа вводом: прощает не-ошибки, не прощает ошибки."""
from app.services.typed_answer import Verdict, judge

E, C, W = Verdict.EXACT, Verdict.CLOSE, Verdict.WRONG


def test_forgives_what_is_not_a_mistake():
    assert judge("Bank", ["Bank"], "de", "die") is E
    assert judge("  bank. ", ["Bank"], "de", "die") is E
    assert judge("die Bank", ["Bank"], "de", "die") is E, "артикль писать можно"
    assert judge("Baer", ["Bär"], "de", "der") is E
    assert judge("Strasse", ["Straße"], "de", "die") is E
    assert judge("nino", ["niño"], "es") is E
    assert judge("cafe", ["le café"], "fr") is E
    assert judge("bank", ["bank, shore"], "en") is W  # ячейка не делится здесь
    assert judge("shore", ["bank", "shore"], "en") is E, "любой вариант ячейки"


def test_one_typo_in_a_long_word_is_close():
    assert judge("Fenstr", ["Fenster"], "de", "das") is C
    assert judge("Fesnter", ["Fenster"], "de", "das") is C, "перестановка соседних"
    assert judge("Fnstr", ["Fenster"], "de", "das") is W, "две опечатки — не знает"
    assert judge("Bnak", ["Bank"], "de", "die") is W, "в коротком слове опечатка — другое слово"


def test_does_not_forgive_mistakes():
    assert judge("der Bank", ["Bank"], "de", "die") is W, "неверный артикль"
    assert judge("Band", ["Bank"], "de", "die") is W
    assert judge("", ["Bank"], "de", "die") is W
    assert judge("die", ["Bank"], "de", "die") is W
