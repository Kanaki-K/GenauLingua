"""Подготовка текста к синтезу: сокращения, числа, гетеронимы."""

import pytest

from app.services.tts_text import (
    NEEDS_CONTEXT,
    PAUSE,
    expand_abbreviations,
    expand_numbers,
    full_clip_text,
    needs_context,
    speakable,
    word_clip_text,
)


class TestAbbreviations:
    """Сокращение с точкой движок читает по буквам: «z.B.» → «цет бе»."""

    @pytest.mark.parametrize("lang,source,expected_part", [
        ("de", "z.B. Hunde", "zum Beispiel"),
        ("de", "Äpfel usw.", "und so weiter"),
        ("de", "d.h. morgen", "das heißt"),
        ("en", "e.g. dogs", "for example"),
        ("en", "cats etc.", "et cetera"),
        ("pl", "np. psy", "na przykład"),
        ("pl", "koty itd.", "i tak dalej"),
        ("ru", "напр. собаки", "например"),
        ("uk", "напр. собаки", "наприклад"),
        ("tr", "kediler vb.", "ve benzeri"),
    ])
    def test_expanded(self, lang, source, expected_part):
        result = expand_abbreviations(source, lang)
        assert expected_part in result
        assert "." not in result.replace(expected_part, "")

    def test_longest_match_wins(self):
        # «и т.д.» должно сработать раньше «т.д.», иначе выйдет «и так далее»
        # с висящим «и» впереди
        assert expand_abbreviations("и т.д.", "ru") == "и так далее"

    def test_unknown_language_untouched(self):
        assert expand_abbreviations("z.B. Hunde", "xx") == "z.B. Hunde"


class TestNumbers:
    """Цифры движок может прочесть по одной: «1990» → «один девять девять ноль»."""

    @pytest.mark.parametrize("lang,number,expected", [
        ("de", "3", "drei"),
        ("de", "21", "einundzwanzig"),
        ("de", "100", "hundert"),
        ("de", "1990", "neunzehnhundertneunzig"),
        ("en", "3", "three"),
        ("en", "21", "twenty-one"),
        ("en", "100", "hundred"),
        ("pl", "5", "pięć"),
        ("pl", "30", "trzydzieści"),
        ("ru", "5", "пять"),
        ("ru", "40", "сорок"),
        ("uk", "7", "сім"),
        ("tr", "8", "sekiz"),
        ("tr", "20", "yirmi"),
    ])
    def test_spelled_out(self, lang, number, expected):
        assert expand_numbers(number, lang) == expected

    def test_german_1990_reads_as_year(self):
        # Немецкое чтение года: «neunzehnhundertneunzig», а не «eintausend...»
        assert expand_numbers("1990", "de") == "neunzehnhundertneunzig"

    def test_english_year_drops_hundred_when_not_round(self):
        assert expand_numbers("1990", "en") == "nineteen ninety"
        assert expand_numbers("1900", "en") == "nineteen hundred"

    def test_german_thousand_uses_ein_not_eins(self):
        assert expand_numbers("1000", "de") == "eintausend"

    @pytest.mark.parametrize("lang,expected", [
        ("ru", "двести пятьдесят"),
        ("uk", "двісті п'ятдесят"),
        ("pl", "dwieście pięćdziesiąt"),
    ])
    def test_slavic_hundreds_are_single_words(self, lang, expected):
        # В славянских языках сотни нерегулярны: не «два сто», а «двести»
        assert expand_numbers("250", lang) == expected

    @pytest.mark.parametrize("lang,expected", [
        ("ru", "девятьсот"),
        ("uk", "дев'ятсот"),
        ("pl", "dziewięćset"),
    ])
    def test_slavic_nine_hundred(self, lang, expected):
        assert expand_numbers("900", lang) == expected

    @pytest.mark.parametrize("lang,n,expected", [
        # 1 тысяча, 2 тысячи, 5 тысяч — согласование по числу
        ("ru", "1000", "тысяча"),
        ("ru", "2000", "две тысячи"),
        ("ru", "5000", "пять тысяч"),
        ("uk", "1000", "тисяча"),
        ("uk", "2000", "дві тисячі"),
        ("uk", "5000", "п'ять тисяч"),
        ("pl", "1000", "tysiąc"),
        ("pl", "2000", "dwa tysiące"),
        ("pl", "5000", "pięć tysięcy"),
    ])
    def test_thousand_agreement(self, lang, n, expected):
        assert expand_numbers(n, lang) == expected

    def test_feminine_two_before_thousand(self):
        # «две тысячи», не «два тысячи»
        assert expand_numbers("2000", "ru").startswith("две")
        assert expand_numbers("2000", "uk").startswith("дві")

    def test_regular_languages_keep_compound_hundreds(self):
        # Немецкий, английский и турецкий складывают сотни регулярно
        assert expand_numbers("250", "de") == "zweihundertfünfzig"
        assert expand_numbers("250", "en") == "two hundred fifty"
        assert expand_numbers("250", "tr") == "iki yüz elli"

    def test_number_inside_sentence(self):
        result = expand_numbers("Ich habe 3 Kinder", "de")
        assert result == "Ich habe drei Kinder"
        assert not any(ch.isdigit() for ch in result)

    def test_large_numbers_left_alone(self):
        # Выше 9999 чтение не выдумываем
        assert expand_numbers("123456", "de") == "123456"

    def test_no_digits_survive_in_base_range(self):
        for value in (0, 1, 7, 11, 19, 20, 21, 47, 99, 100, 101, 250, 999,
                      1000, 1984, 2024, 9999):
            for lang in ("de", "en", "pl", "ru", "uk", "tr"):
                result = expand_numbers(str(value), lang)
                assert not any(ch.isdigit() for ch in result), (lang, value, result)


class TestHeteronyms:
    """Без контекста движок выбирает одно из чтений — и не обязательно нужное."""

    @pytest.mark.parametrize("word,lang", [
        ("modern", "de"),
        ("umfahren", "de"),
        ("übersetzen", "de"),
        ("read", "en"),
        ("present", "en"),
        ("record", "en"),
    ])
    def test_flagged(self, word, lang):
        assert needs_context(word, lang) is True

    @pytest.mark.parametrize("word,lang", [
        ("Haus", "de"),
        ("gehen", "de"),
        ("table", "en"),
        ("książka", "pl"),
        ("рыба", "ru"),
    ])
    def test_not_flagged(self, word, lang):
        assert needs_context(word, lang) is False

    def test_article_does_not_hide_heteronym(self):
        # «die Montage» — артикль не должен мешать опознать слово
        assert needs_context("die Montage", "de") is True

    def test_english_particle_stripped(self):
        assert needs_context("to read", "en") is True

    def test_empty_is_safe(self):
        assert needs_context("", "de") is False
        assert needs_context(None, "de") is False

    def test_languages_with_regular_orthography_have_no_list(self):
        # Польский, русский, украинский, турецкий читаются по написанию
        for lang in ("pl", "ru", "uk", "tr"):
            assert lang not in NEEDS_CONTEXT


class TestSpeakable:
    def test_first_meaning_only_for_word(self):
        # Многозначный перевод хранится через запятую; озвучивать перечисление
        # значений вместо слова бессмысленно
        assert word_clip_text("к, в, на, слишком", "ru") == "к"

    def test_example_keeps_commas(self):
        # В примере запятая — часть фразы, резать нельзя
        assert speakable("Wir kommen gleich, warte bitte", "de") == (
            "Wir kommen gleich, warte bitte"
        )

    def test_parentheticals_removed(self):
        assert speakable("идти (о человеке)", "ru") == "идти"

    def test_whitespace_collapsed(self):
        assert speakable("  das   Haus  ", "de") == "das Haus"

    def test_empty(self):
        assert speakable("", "de") == ""
        assert speakable(None, "de") == ""


class TestFullClip:
    def test_word_first_then_example(self):
        result = full_clip_text("die Fahrkarte", "Ich kaufe eine Fahrkarte", "de")
        assert result == f"die Fahrkarte{PAUSE}Ich kaufe eine Fahrkarte"
        assert result.startswith("die Fahrkarte")

    def test_without_example_is_just_word(self):
        assert full_clip_text("das Haus", None, "de") == "das Haus"
        assert full_clip_text("das Haus", "", "de") == "das Haus"

    def test_rules_apply_inside_full_clip(self):
        result = full_clip_text("Beispiel", "z.B. 3 Hunde", "de")
        assert "zum Beispiel" in result
        assert "drei" in result
        assert not any(ch.isdigit() for ch in result)
