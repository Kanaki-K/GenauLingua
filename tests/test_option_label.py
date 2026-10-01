# -*- coding: utf-8 -*-
"""
Подпись варианта ответа на кнопке: одно слово.

Так было до правки многозначности, и так решено оставить. Многозначные слова
получили в базе все значения вместо одного — от этого точность на них выросла
с 71% до 80%, — но на кнопку шёл весь перевод целиком и дорастал до 133
символов. Четыре таких кнопки превращали карточку в простыню, а вид карточки
согласован был раньше.

Значения не потеряны: полный набор показывается в разборе сразу после ответа.
"""
import pytest

from app.services.language_service import display_text, option_label


class FakeWord:
    def __init__(self, **values):
        for key, value in values.items():
            setattr(self, key, value)


def ru(text: str) -> FakeWord:
    return FakeWord(translation_ru=text)


def test_single_meaning_is_shown_as_is():
    assert option_label(ru("ещё"), "ru") == "Ещё"


def test_only_first_meaning_of_many():
    word = ru("записывать, записывать на плёнку или видео, принимать, "
              "брать к себе, начинать, приступать, поднимать, подбирать")
    assert option_label(word, "ru") == "Записывать"


def test_no_ellipsis():
    """
    Многоточия быть не должно.

    Подпись — не обрезанный перевод, а главное значение. Многоточие читалось бы
    как «тут что-то потерялось», хотя потеряно ничего: остальное в разборе.
    """
    word = ru("брать, взять, принимать, садиться на транспорт")
    assert "…" not in option_label(word, "ru")
    assert "..." not in option_label(word, "ru")


@pytest.mark.parametrize("separator", [",", ";", "/"])
def test_every_separator_is_understood(separator):
    """Значения в базе разделены запятой, точкой с запятой или косой чертой."""
    word = ru(f"первое{separator} второе{separator} третье")
    assert option_label(word, "ru") == "Первое"


def test_long_single_meaning_stays_whole():
    """
    Одно длинное значение без разделителей не обрезается.

    «Удостоверение лично…» читалось бы как ошибка. Если значение одно и оно
    длинное — пусть будет длинным, это честнее обрезка.
    """
    text = "удостоверение личности государственного образца"
    assert option_label(ru(text), "ru").lower() == text


def test_empty_translation_gives_empty_label():
    assert option_label(ru(""), "ru") == ""
    assert option_label(FakeWord(), "ru") == ""


def test_label_is_never_longer_than_full_text():
    for text in ("ещё", "брать, взять, принимать", "a, b, c, d, e"):
        word = ru(text)
        assert len(option_label(word, "ru")) <= len(display_text(word, "ru"))


def test_works_for_every_language():
    word = FakeWord(
        translation_ru="брать, взять, принимать",
        translation_en="to take, to accept, to receive",
        translation_tr="almak, kabul etmek",
        translation_pl="brać, przyjmować",
        translation_uk="брати, взяти, приймати",
    )
    assert option_label(word, "ru") == "Брать"
    assert option_label(word, "en") == "To take"
    assert option_label(word, "tr") == "Almak"
    assert option_label(word, "pl") == "Brać"
    assert option_label(word, "uk") == "Брати"


def test_german_keeps_its_case():
    """
    Регистр немецкого слова значим и подписью не меняется.

    Существительные пишутся с заглавной, остальное со строчной — display_text
    это учитывает, и option_label не должен ломать.
    """
    assert option_label(FakeWord(word_de="gehen"), "de") == "gehen"
    assert option_label(FakeWord(word_de="Haus"), "de") == "Haus"


def test_keeps_whole_phrase_with_internal_space():
    """Значение из нескольких слов — это одно значение, а не два."""
    assert option_label(ru("садиться на транспорт, брать"), "ru") == "Садиться на транспорт"
