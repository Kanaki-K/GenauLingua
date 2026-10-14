"""
Склейка значений перевода перед записью в базу.

Каждая проверка здесь появилась из настоящего дефекта, найденного на прогоне
по A1+A2, а не придумана заранее. Значения попадают в викторину как варианты
ответа и в озвучку как произносимый текст, поэтому мусор в них виден людям.
"""

import pytest

from app.scripts.retranslate_wordbase import (
    _diacritic_count,
    _diacritic_key,
    _fix_homoglyphs,
    _join_meanings,
)


def joined(primary, meanings, lang):
    return _join_meanings({"primary": primary, "meanings": meanings}, lang)


class TestHomoglyphs:
    """
    Латинская «a» внутри украинского слова выглядит как обычная буква, а для
    базы, поиска и озвучки это другое слово. Найдено на восьми словах из 3237.
    """

    @pytest.mark.parametrize("value,lang,expected", [
        ("удaритися", "uk", "ударитися"),
        ("нареченa", "uk", "наречена"),
        ("виставa", "uk", "вистава"),
        ("дорíжка", "uk", "доріжка"),
        ("babа", "pl", "baba"),
    ])
    def test_foreign_letter_inside_word_is_fixed(self, value, lang, expected):
        assert _fix_homoglyphs(value, lang) == expected

    @pytest.mark.parametrize("value,lang", [
        ("ID-карта", "ru"),
        ("HR-менеджер", "uk"),
        ("IT-специалист", "ru"),
        ("SMS-сообщение", "ru"),
    ])
    def test_intentional_abbreviations_untouched(self, value, lang):
        """
        Латиница в аббревиатуре намеренна. Первая версия работала по словам
        через пробел и превращала «ID-карта» в «ІD-карта» с кириллической І.
        """
        assert _fix_homoglyphs(value, lang) == value

    def test_own_script_untouched(self):
        assert _fix_homoglyphs("наречена", "uk") == "наречена"
        assert _fix_homoglyphs("kobieta", "pl") == "kobieta"


class TestSplittingMeanings:
    """
    Модель иногда кладёт несколько значений в один элемент списка. Без разбора
    по запятой «ремень» рядом с «ремень, пояс» давало в переводе
    «ремень, ремень, пояс».
    """

    def test_element_with_commas_is_split(self):
        assert joined("ремень", ["ремень, пояс", "пояс, зона"], "ru") == (
            "ремень, пояс, зона"
        )

    def test_no_duplicates_after_split(self):
        result = joined("ремінь", ["ремінь, пасок", "пояс, зона"], "uk")
        parts = [p.strip() for p in result.split(",")]
        assert len(parts) == len(set(parts)), result

    def test_semicolon_and_slash_also_split(self):
        assert joined("a", ["a; b", "c / d"], "en") == "a, b, c, d"


class TestDiacriticPreference:
    """
    Модель выдала primary «salatka» без польской ł при значении «sałatka».
    Оба попадали в перевод, и человек видел одно слово дважды.
    """

    def test_variant_with_diacritics_wins(self):
        assert joined("salatka", ["sałatka", "sałata"], "pl") == "sałatka, sałata"

    def test_turkish_dotted_capital_wins(self):
        # Транслит вместо İ — тот же класс дефекта
        assert joined("Iyi", ["İyi", "güzel"], "tr") == "İyi, güzel"

    def test_german_eszett_and_umlaut(self):
        assert joined("Fuss", ["Fuß"], "de") == "Fuß"
        assert joined("Madchen", ["Mädchen"], "de") == "Mädchen"

    def test_order_follows_first_appearance(self):
        # Вытеснение вариантом с диакритикой не должно менять порядок
        assert joined("zoo", ["zoo", "ogród zoologiczny"], "pl") == (
            "zoo, ogród zoologiczny"
        )


class TestKeys:
    def test_diacritic_key_folds(self):
        assert _diacritic_key("sałatka") == _diacritic_key("salatka")
        assert _diacritic_key("İyi") == _diacritic_key("Iyi")
        assert _diacritic_key("Fuß") == _diacritic_key("Fuss")

    def test_diacritic_key_distinguishes_real_words(self):
        assert _diacritic_key("sałatka") != _diacritic_key("sałata")

    def test_diacritic_count(self):
        assert _diacritic_count("sałatka") > _diacritic_count("salatka")
        assert _diacritic_count("İyi") > _diacritic_count("Iyi")
        assert _diacritic_count("zoo") == 0


class TestSimpleCases:
    def test_single_meaning(self):
        assert joined("октябрь", ["октябрь"], "ru") == "октябрь"

    def test_empty_is_empty(self):
        assert joined("", [], "ru") == ""

    def test_whitespace_trimmed(self):
        assert joined("  дом  ", ["  дом  ", " жильё "], "ru") == "дом, жильё"
