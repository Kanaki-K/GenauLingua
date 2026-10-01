# -*- coding: utf-8 -*-
"""
Подпись варианта ответа на кнопке.

Зачем она понадобилась. Многозначные слова получили все значения вместо
одного — это было исправлением главной проблемы качества, из-за которой
точность на таких словах была 71% против 80%. Но переводы от этого выросли: у
русского 379 значений длиннее 60 символов, самое длинное 133. Кнопка в Telegram
показывает около 30–35 символов в строке, и четыре таких варианта превращают
карточку в простыню.

Значения при этом нужны. Поэтому полный набор остаётся в разборе сразу после
ответа, а на кнопке стоит столько, сколько уместится.
"""
import pytest

from app.services.language_service import OPTION_LABEL_BUDGET, display_text, option_label


class FakeWord:
    def __init__(self, **values):
        for key, value in values.items():
            setattr(self, key, value)


def ru(text: str) -> FakeWord:
    return FakeWord(translation_ru=text)


def test_short_translation_is_untouched():
    assert option_label(ru("ещё"), "ru") == "Ещё"


def test_long_translation_is_cut_with_ellipsis():
    word = ru("записывать, записывать на плёнку или видео, принимать, "
              "брать к себе, начинать, приступать, поднимать, подбирать")
    label = option_label(word, "ru")
    assert label.endswith("…")
    assert len(label) <= OPTION_LABEL_BUDGET + 1
    # Первое значение обязано сохраниться целиком
    assert label.startswith("Записывать")


def test_cut_happens_on_meaning_boundary():
    """Значение не рвётся посередине: обрезка только по разделителю."""
    word = ru("брать, взять, принимать, садиться на транспорт")
    label = option_label(word, "ru").rstrip("…")
    for part in label.split(", "):
        assert part.strip(), "пустое значение после обрезки"
    assert "садитьс" not in label, "значение обрезано посередине"


def test_single_long_meaning_stays_whole():
    """
    Одно длинное значение без разделителей не обрезается.

    Обрезать слово посередине хуже, чем выйти за бюджет: «удостоверение лично…»
    читается как ошибка, а не как сокращение.
    """
    text = "очень длинное одиночное значение без всяких разделителей вообще"
    label = option_label(ru(text), "ru")
    assert label.lower() == text.lower()
    assert "…" not in label


def test_first_meaning_kept_even_if_over_budget():
    long_first = "а" * (OPTION_LABEL_BUDGET + 10)
    word = ru(f"{long_first}, второе")
    label = option_label(word, "ru")
    assert label.lower().startswith(long_first)


def test_empty_translation_gives_empty_label():
    assert option_label(ru(""), "ru") == ""
    assert option_label(FakeWord(), "ru") == ""


def test_label_never_longer_than_full_text():
    """Подпись не может оказаться длиннее того, что сокращает."""
    for text in ("ещё", "брать, взять, принимать",
                 "a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p"):
        word = ru(text)
        assert len(option_label(word, "ru")) <= len(display_text(word, "ru")) + 1


@pytest.mark.parametrize("lang,text,expected_start", [
    ("ru", "брать, взять, принимать, садиться на транспорт", "Брать"),
    ("en", "to wiretap, to bug, to listen in on, to listen to a chest", "To wiretap"),
])
def test_works_for_every_language(lang, text, expected_start):
    word = FakeWord(translation_ru=text, translation_en=text)
    assert option_label(word, lang).startswith(expected_start)


def test_german_keeps_its_case():
    """
    Регистр немецкого слова значим и подписью не меняется.

    Существительные пишутся с заглавной, остальное со строчной — display_text
    это уже учитывает, и option_label не должен ломать.
    """
    word = FakeWord(word_de="gehen")
    assert option_label(word, "de") == "gehen"
