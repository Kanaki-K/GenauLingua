"""
Вид карточки — договорённость с владельцем, закреплённая тестом.

Договорённость сформулирована владельцем так:

  Одна карточка — это слово с правильным артиклем либо выражение. На том же
  языке пример, в котором это слово есть. В игре с четырьмя вариантами
  звучит слово; название клипа — слово с артиклем. После ответа карточка
  показывает слово и пример, а звучит слово вместе с примером; название
  такого клипа — слово, тире, не больше трёх слов примера и троеточие.
  И так на всех шести языках.

Зачем тест, если это уже работает. Выяснять заново, как устроена карточка,
дорого: код приходится перечитывать целиком, а словами договорённость
проверить нельзя. Если кто-то сдвинет формат, тест назовёт, что именно
сломалось, и спор закончится до него, а не после.

Проверяется ровно договорённость, не больше: длина обрезки, артикль,
совпадение названия со звуком, одинаковость поведения по языкам.
"""

from app.database.enums import PartOfSpeech
from app.services.audio_service import (
    KIND_FULL,
    KIND_WORD,
    audio_title,
    clip_kind_for_question,
    spoken_for,
)
from app.services.language_service import SUPPORTED_LANGS, main_meaning
from tests.conftest import make_word

# Ряд, на котором видно всё сразу: немецкий артикль, пример длиннее трёх слов
WORD = make_word(
    "Mann",
    article="der",
    pos=PartOfSpeech.NOUN,
    ru="мужчина, муж",
    uk="чоловік",
    en="man, husband",
    tr="adam, erkek",
    pl="mężczyzna",
)
WORD.example_de = "Der Mann arbeitet hier"
WORD.example_ru = "Мужчина работает здесь"
WORD.example_uk = "Чоловік працює тут"
WORD.example_en = "The man works here"
WORD.example_tr = "Adam burada çalışıyor"
WORD.example_pl = "Ten mężczyzna tutaj pracuje"


class TestCardHead:
    """Слово на карточке — с артиклем там, где артикль в языке есть."""

    def test_german_word_keeps_its_article(self):
        assert main_meaning(WORD, "de") == "der Mann"

    def test_languages_without_articles_show_bare_word(self):
        # Ни в одном из пяти артикля нет как явления — приписывать нечего
        assert main_meaning(WORD, "ru") == "мужчина"
        assert main_meaning(WORD, "uk") == "чоловік"
        assert main_meaning(WORD, "en") == "man"
        assert main_meaning(WORD, "tr") == "adam"
        assert main_meaning(WORD, "pl") == "mężczyzna"

    def test_shown_meaning_is_the_one_from_the_example(self):
        """
        Из многозначной ячейки берётся значение, которое стоит в примере.

        Прежде бралось первое по списку: показывалось «Swot», озвучивалось
        «Swot», а пример был про «overachiever» — три разных слова в одной
        карточке.
        """
        word = make_word("Streber", article="der", en="swot, overachiever, nerd")
        word.example_en = "He is a real overachiever at school"
        assert main_meaning(word, "en") == "overachiever"


class TestQuestionClip:
    """В вопросе звучит слово, и название клипа — ровно оно."""

    def test_question_speaks_the_word_alone(self):
        for lang in SUPPORTED_LANGS:
            assert clip_kind_for_question(WORD, lang) == KIND_WORD, lang

    def test_question_title_is_the_word_with_article(self):
        spoken = spoken_for(WORD, "de", KIND_WORD)
        assert spoken == "der Mann"
        assert audio_title(main_meaning(WORD, "de")) == "der Mann"

    def test_question_title_matches_what_sounds_in_every_language(self):
        for lang in SUPPORTED_LANGS:
            shown = main_meaning(WORD, lang)
            assert spoken_for(WORD, lang, KIND_WORD) == shown, lang
            assert audio_title(shown) == shown, lang

    def test_heteronym_gets_the_example_in_the_question(self):
        """
        Исключение, и оно намеренное: слово с двумя чтениями, произнесённое
        отдельно, движок прочтёт наугад. SSML недоступен, поэтому чтение
        задаётся контекстом.
        """
        word = make_word("modern", article=None, pos=PartOfSpeech.ADJECTIVE)
        assert clip_kind_for_question(word, "de") == KIND_FULL


class TestAnswerClip:
    """После ответа звучит слово вместе с примером."""

    def test_answer_speaks_word_and_example(self):
        for lang in SUPPORTED_LANGS:
            spoken = spoken_for(WORD, lang, KIND_FULL)
            shown = main_meaning(WORD, lang)
            assert spoken.startswith(shown), lang
            # Пример идёт вслед за словом, в том же клипе
            assert spoken != shown, lang

    def test_answer_title_is_word_dash_three_words_ellipsis(self):
        title = audio_title("der Mann", "Der Mann arbeitet hier und wohnt dort")
        assert title == "der Mann — Der Mann arbeitet…"

    def test_no_ellipsis_when_example_is_short(self):
        """Троеточие значит «обрезано». Резать нечего — его быть не должно."""
        title = audio_title("река", "Река широкая")
        assert title == "река — Река широкая"
        assert "…" not in title

    def test_every_language_follows_the_same_shape(self):
        for lang in SUPPORTED_LANGS:
            shown = main_meaning(WORD, lang)
            example = getattr(WORD, f"example_{lang}")
            title = audio_title(shown, example)
            assert title.startswith(f"{shown} — "), lang
            head = title.split(" — ", 1)[1]
            words = head.rstrip("…").split()
            assert len(words) <= 3, (lang, title)
            # Троеточие ровно тогда, когда пример длиннее трёх слов
            assert ("…" in title) == (len(example.split()) > 3), (lang, title)
