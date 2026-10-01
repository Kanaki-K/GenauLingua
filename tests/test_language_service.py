"""Реестр языков: стороны карточки, нормализация, разбор пары."""

import pytest

from app.database.enums import CEFRLevel, PartOfSpeech
from app.services.language_service import (
    INTERFACE_LANGS,
    LANGUAGES,
    LEARNABLE_LANGS,
    SUPPORTED_LANGS,
    LanguagePair,
    display_text,
    example_text,
    fallback_native_for,
    flag,
    legacy_mode_name,
    meaning_variants,
    normalize_headword,
    native_options,
    pair_from_legacy_mode,
    pair_from_user,
    pair_label,
    word_text,
)
from tests.conftest import make_word


class TestWordSides:
    def setup_method(self):
        self.word = make_word(
            "Tisch", article="der", ru="стол", uk="стіл", en="table", tr="masa"
        )

    def test_german_side_includes_article(self):
        assert word_text(self.word, "de") == "der Tisch"

    def test_german_side_without_article_on_request(self):
        assert word_text(self.word, "de", with_article=False) == "Tisch"

    def test_placeholder_article_is_ignored(self):
        word = make_word("gut", article="-")
        assert word_text(word, "de") == "gut"

    @pytest.mark.parametrize(
        "code,expected",
        [("ru", "стол"), ("uk", "стіл"), ("en", "table"), ("tr", "masa")],
    )
    def test_translation_sides(self, code, expected):
        assert word_text(self.word, code) == expected

    def test_examples_per_language(self):
        assert example_text(self.word, "de") == "Beispiel Tisch"
        assert example_text(self.word, "en") == "example Tisch"

    def test_display_capitalizes_translations_but_not_german(self):
        # Регистр в немецком значим, переводы приводим к заглавной — как было
        assert display_text(self.word, "de") == "der Tisch"
        assert display_text(self.word, "ru") == "Стол"
        assert display_text(self.word, "en") == "Table"

    def test_missing_translation_gives_empty_string(self):
        word = make_word("Leer")
        word.translation_en = None
        assert word_text(word, "en") == ""
        assert display_text(word, "en") == ""


class TestNormalization:
    @pytest.mark.parametrize(
        "text,lang,expected",
        [
            ("Tisch", "de", "tisch"),
            ("  Stuhl  ", "de", "stuhl"),
            ("to run", "en", "run"),
            ("the house", "en", "house"),
            ("a cat", "en", "cat"),
            ("an apple", "en", "apple"),
            # служебное слово само по себе остаётся
            ("to", "en", "to"),
            ("the", "en", "the"),
            # из многозначного берётся первый вариант
            ("a / an", "en", "a"),
            ("сразу, одинаковый", "ru", "сразу"),
            ("", "en", ""),
            (None, "en", ""),
        ],
    )
    def test_normalize(self, text, lang, expected):
        assert normalize_headword(text, lang) == expected

    def test_russian_has_no_particle_stripping(self):
        # «a» не является служебным словом в русском
        assert normalize_headword("a", "ru") == "a"


class TestMeaningVariants:
    def test_splits_all_separators(self):
        assert meaning_variants("one, two; three / four", "en") == {
            "one", "two", "three", "four"
        }

    def test_strips_particles_in_each_variant(self):
        assert meaning_variants("to run / to walk", "en") == {"run", "walk"}

    def test_empty_input(self):
        assert meaning_variants("", "en") == frozenset()
        assert meaning_variants("  ,  ; ", "en") == frozenset()


class TestLanguagePair:
    def test_forward_asks_learning_answers_native(self):
        pair = LanguagePair(learning="de", native="ru", reverse=False)
        assert pair.prompt_lang == "de"
        assert pair.answer_lang == "ru"

    def test_reverse_swaps_sides(self):
        pair = LanguagePair(learning="de", native="ru", reverse=True)
        assert pair.prompt_lang == "ru"
        assert pair.answer_lang == "de"

    def test_label_matches_previous_format(self):
        # Прежде подписи были захардкожены как "🇩🇪 DE → 🏴 RU"
        assert pair_label(LanguagePair("de", "ru", False)) == f"{flag('de')} DE → {flag('ru')} RU"
        assert pair_label(LanguagePair("de", "ru", True)) == f"{flag('ru')} RU → {flag('de')} DE"

    def test_every_pair_is_expressible(self):
        """
        Подпись есть у каждой пары языков в каждом направлении.

        Число пар считается от LEARNABLE_LANGS, а не записано цифрой: прежде
        здесь стояло «== 40», и этот тест падал бы от добавления шестого языка,
        хотя проверяет он не количество, а выразимость. Тест, который ломается
        от расширения списка, заставляет править себя вместо того, чтобы
        поймать настоящую поломку.
        """
        count = len(LEARNABLE_LANGS)
        pairs = [
            LanguagePair(a, b, rev)
            for a in LEARNABLE_LANGS
            for b in LEARNABLE_LANGS
            for rev in (False, True)
            if a != b
        ]
        # Упорядоченные пары без совпадений × два направления
        assert len(pairs) == count * (count - 1) * 2
        assert all(pair_label(p) for p in pairs)


class TestPairFromUser:
    class FakeUser:
        def __init__(self, learning, native, reverse=False, interface="ru"):
            self.learning_lang = learning
            self.native_lang = native
            self.reverse_mode = reverse
            self.interface_language = interface

    def test_normal_case(self):
        pair = pair_from_user(self.FakeUser("en", "ru"))
        assert (pair.learning, pair.native) == ("en", "ru")

    def test_collision_is_resolved(self):
        """Язык значения не может совпадать с изучаемым."""
        pair = pair_from_user(self.FakeUser("ru", "ru"))
        assert pair.learning == "ru"
        assert pair.native != "ru"

    def test_unknown_learning_falls_back_to_german(self):
        pair = pair_from_user(self.FakeUser("xx", "ru"))
        assert pair.learning == "de"

    def test_missing_native_is_filled(self):
        pair = pair_from_user(self.FakeUser("de", None, interface="tr"))
        assert pair.native == "tr"


class TestNativeOptions:
    def test_excludes_learning_language(self):
        for learning in LEARNABLE_LANGS:
            options = native_options(learning)
            assert learning not in options
            assert len(options) == len(LEARNABLE_LANGS) - 1

    def test_fallback_never_equals_learning(self):
        for learning in LEARNABLE_LANGS:
            assert fallback_native_for(learning, preferred=learning) != learning


class TestLegacyCompat:
    """
    Старый TranslationMode должен читаться (миграция) и записываться
    (прежняя аналитика и возможность откатиться).
    """

    @pytest.mark.parametrize(
        "mode,learning,native,reverse",
        [
            ("DE_TO_RU", "de", "ru", False),
            ("RU_TO_DE", "de", "ru", True),
            ("DE_TO_EN", "de", "en", False),
            ("EN_TO_DE", "de", "en", True),
            ("DE_TO_TR", "de", "tr", False),
            ("TR_TO_DE", "de", "tr", True),
        ],
    )
    def test_parses_legacy_modes(self, mode, learning, native, reverse):
        pair = pair_from_legacy_mode(mode)
        assert (pair.learning, pair.native, pair.reverse) == (learning, native, reverse)

    def test_parsing_is_case_insensitive(self):
        assert pair_from_legacy_mode("de_to_ru") == pair_from_legacy_mode("DE_TO_RU")

    def test_roundtrip_for_german_pairs(self):
        for native in ("ru", "uk", "en", "tr"):
            for reverse in (False, True):
                pair = LanguagePair("de", native, reverse)
                mode = legacy_mode_name(pair)
                assert mode is not None
                assert pair_from_legacy_mode(mode.value) == pair

    def test_pairs_without_german_have_no_legacy_value(self):
        # ru→en в старом enum не выражается — поле остаётся пустым
        assert legacy_mode_name(LanguagePair("en", "ru", False)) is None
        assert legacy_mode_name(LanguagePair("tr", "uk", True)) is None

    def test_garbage_input(self):
        assert pair_from_legacy_mode(None) is None
        assert pair_from_legacy_mode("") is None
        assert pair_from_legacy_mode("NONSENSE") is None
        assert pair_from_legacy_mode("XX_TO_YY") is None


def test_interface_langs_have_locales():
    from app.locales import LOCALES

    assert set(INTERFACE_LANGS) == set(LOCALES)


def test_every_learnable_language_has_an_interface():
    """
    На каждом изучаемом языке можно и читать бота.

    Прежде здесь стояло обратное: «немецкой локали нет, но учить немецкий
    можно». Это держалось, пока бот учил только немецкому — читать интерфейс
    по-немецки было некому. Когда доступной стала любая пара из шести языков,
    такой перекос потерял смысл: человек, который учит английский, может быть
    немцем.

    Польский в LEARNABLE_LANGS появится после заполнения колонок, а локаль у
    него уже есть — поэтому проверка идёт в одну сторону: интерфейс обязан
    существовать для всего, что открыто для изучения, но не наоборот.
    """
    missing = [code for code in LEARNABLE_LANGS if code not in INTERFACE_LANGS]
    assert not missing, f"изучаемые языки без локали: {missing}"


class TestPolish:
    """
    Польский описан в реестре, но ещё не открыт для изучения: колонки в базе
    заполняются отдельным прогоном. Тесты держат это состояние явным, чтобы
    язык не открылся по невнимательности с пустой базой — тогда викторина не
    нашла бы ни одного слова.
    """

    def test_described_in_registry(self):
        assert "pl" in LANGUAGES
        cfg = LANGUAGES["pl"]
        assert cfg.word_attr == "translation_pl"
        assert cfg.example_attr == "example_pl"
        assert cfg.uses_article is False

    def test_columns_exist_on_model(self):
        from app.database.models import Word

        assert hasattr(Word, "translation_pl")
        assert hasattr(Word, "example_pl")

    def test_included_in_supported_but_not_learnable_yet(self):
        """
        Польский описан, но ещё не открыт ученикам.

        Это намеренный замок, а не недоделка: открывать язык можно только когда
        его колонки заполнены на всех уровнях, иначе ученик уровня B1 получит
        пустую викторину. Когда переводы заполнятся, этот тест меняется на
        «"pl" in LEARNABLE_LANGS» вместе с одной строкой в language_service —
        и больше ничего менять не нужно, остальные тесты от числа языков не
        зависят.
        """
        assert "pl" in SUPPORTED_LANGS
        assert "pl" not in LEARNABLE_LANGS

    def test_every_learnable_lang_is_supported(self):
        # Обратное включение: открыть язык, не описав его, невозможно
        assert set(LEARNABLE_LANGS) <= set(SUPPORTED_LANGS)
        assert set(SUPPORTED_LANGS) <= set(LANGUAGES)

    def test_has_name_in_every_locale(self):
        from app.locales import LOCALES

        for code, texts in LOCALES.items():
            assert "langname_pl" in texts, f"нет langname_pl в локали {code}"

    def test_word_and_example_read_from_polish_columns(self):
        word = make_word(
            word_de="Buch",
            translation_pl="książka",
            example_pl="Czytam ciekawą książkę",
        )
        assert word_text(word, "pl") == "książka"
        # Как и для других неартиклевых языков, показ с заглавной
        assert display_text(word, "pl") == "Książka"
        assert example_text(word, "pl") == "Czytam ciekawą książkę"

    def test_diacritics_survive_normalization(self):
        # Ключ схлопывания не должен терять хвостики: иначе «żółty» и «zolty»
        # склеились бы в одно слово
        assert normalize_headword("Książka", "pl") == "książka"
        assert normalize_headword("żółty", "pl") != "zolty"

    def test_no_leading_particles_stripped(self):
        # В польском нет ни артикля, ни частицы инфинитива — снимать нечего
        assert normalize_headword("do domu", "pl") == "do domu"

    def test_flag(self):
        assert flag("pl") == "🇵🇱"
