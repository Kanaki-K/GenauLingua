"""Озвучка: названия клипов, выбор вида, кэш, голоса."""

import pytest

from app.database.enums import PartOfSpeech
from app.services.audio_service import (
    KIND_FULL,
    KIND_WORD,
    audio_filename,
    audio_title,
    clip_kind_for_question,
    spoken_for,
)
from app.services.tts_voices import (
    DEFAULT_VOICE,
    PREVIEW_TEXT,
    VOICES,
    by_gender,
    default_voice,
    is_valid_voice,
    preview_text,
    resolve_voice,
    voices_for,
)
from tests.conftest import make_word


class TestAudioTitle:
    """
    В названии только то, что звучит. Пример обрезается до трёх слов, чтобы
    названия были одной длины и карточки выглядели ровно.
    """

    def test_word_only(self):
        assert audio_title("die Fahrkarte") == "die Fahrkarte"

    def test_word_with_example_truncated(self):
        assert audio_title("die Fahrkarte", "Ich kaufe eine Fahrkarte") == (
            "die Fahrkarte — Ich kaufe eine…"
        )

    def test_short_example_without_ellipsis(self):
        # Три слова и меньше — обрезать нечего
        assert audio_title("ja", "Ja") == "ja — Ja"
        assert audio_title("gut", "Das ist gut") == "gut — Das ist gut"

    def test_punctuation_at_cut_removed(self):
        # «Wir kommen gleich,…» выглядело бы неряшливо
        assert audio_title("gleich", "Wir kommen gleich, warte bitte") == (
            "gleich — Wir kommen gleich…"
        )

    def test_titles_stay_close_in_length(self):
        cases = [
            ("die Fahrkarte", "Ich kaufe eine Fahrkarte"),
            ("arbeiten", "Ich arbeite jeden Tag von acht bis fünf Uhr im Büro"),
            ("der Bahnhof", "Der Bahnhof ist weit von hier entfernt"),
        ]
        lengths = [len(audio_title(w, e)) for w, e in cases]
        # Разброс небольшой: длина примера на название не влияет
        assert max(lengths) - min(lengths) < 12, lengths

    def test_no_project_name_anywhere(self):
        title = audio_title("das Haus", "Das Haus ist groß")
        assert "GenauLingua" not in title
        assert "Genau" not in title


class TestAudioFilename:
    def test_extension_and_dash_kept(self):
        name = audio_filename("die Fahrkarte — Ich kaufe eine…")
        assert name.endswith(".mp3")
        assert "—" in name

    def test_unsafe_characters_dropped(self):
        assert "/" not in audio_filename("a/b")
        assert ":" not in audio_filename("a:b")

    def test_never_empty(self):
        assert audio_filename("") == "audio.mp3"
        assert audio_filename("???") == "audio.mp3"


class TestClipKind:
    def test_ordinary_word_needs_only_itself(self):
        word = make_word("Haus", pos=PartOfSpeech.NOUN, article="das")
        assert clip_kind_for_question(word, "de") == KIND_WORD

    def test_heteronym_gets_context(self):
        # «modern» читается двояко; изолированно движок выберет наугад
        word = make_word("modern", pos=PartOfSpeech.ADJECTIVE)
        assert clip_kind_for_question(word, "de") == KIND_FULL

    def test_heteronym_with_article_still_detected(self):
        word = make_word("Montage", pos=PartOfSpeech.NOUN, article="die")
        assert clip_kind_for_question(word, "de") == KIND_FULL


class TestSpokenText:
    def test_word_clip_is_just_the_word(self):
        word = make_word("Haus", article="das")
        assert spoken_for(word, "de", KIND_WORD) == "das Haus"

    def test_full_clip_puts_word_first(self):
        word = make_word("Haus", article="das")
        spoken = spoken_for(word, "de", KIND_FULL)
        assert spoken.startswith("das Haus")
        assert "Beispiel Haus" in spoken

    def test_rules_applied(self):
        # Сокращения и числа разворачиваются и в озвучке слова тоже
        word = make_word("Nummer", ru="номер")
        word.word_de = "Nr."
        assert "Nummer" in spoken_for(word, "de", KIND_WORD)

    def test_polysemous_translation_takes_first_meaning(self):
        # Озвучивать «к, в, на, слишком» вместо слова незачем
        word = make_word("zu", ru="к, в, на, слишком")
        assert spoken_for(word, "ru", KIND_WORD) == "к"


class TestVoices:
    def test_every_language_has_at_least_two_voices(self):
        for lang, voices in VOICES.items():
            assert len(voices) >= 2, lang
            assert by_gender(lang, "male"), lang
            assert by_gender(lang, "female"), lang

    def test_german_has_three_of_each(self):
        # Ровно то, что просили: три мужских и три женских
        assert len(by_gender("de", "male")) == 3
        assert len(by_gender("de", "female")) == 3

    def test_one_region_per_language(self):
        # Немецкий — Германия, английский — Британия, без выбора акцента
        prefixes = {"de": "de-DE", "en": "en-GB", "pl": "pl-PL",
                    "ru": "ru-RU", "uk": "uk-UA", "tr": "tr-TR"}
        for lang, prefix in prefixes.items():
            for voice in voices_for(lang):
                assert voice.name.startswith(prefix), (lang, voice.name)

    def test_default_is_first_in_list(self):
        for lang, voices in VOICES.items():
            assert default_voice(lang) == voices[0].name

    def test_every_language_has_default_and_preview(self):
        for lang in VOICES:
            assert lang in DEFAULT_VOICE
            assert lang in PREVIEW_TEXT
            assert preview_text(lang)

    def test_labels_are_unique_within_language(self):
        for lang, voices in VOICES.items():
            labels = [v.label for v in voices]
            assert len(labels) == len(set(labels)), lang

    @pytest.mark.parametrize("voice,lang,expected", [
        ("de-DE-KatjaNeural", "de", True),
        ("de-DE-KatjaNeural", "en", False),   # чужой язык
        ("en-GB-SoniaNeural", "en", True),
        ("de-DE-NoSuchNeural", "de", False),
        (None, "de", False),
        ("", "de", False),
    ])
    def test_validation(self, voice, lang, expected):
        assert is_valid_voice(voice, lang) is expected

    def test_foreign_voice_falls_back_silently(self):
        # Сорванная озвучка хуже неожидаемого голоса
        assert resolve_voice("de-DE-KatjaNeural", "en") == default_voice("en")
        assert resolve_voice(None, "ru") == default_voice("ru")
        assert resolve_voice("чушь", "tr") == default_voice("tr")

    def test_unknown_language_does_not_crash(self):
        # Изучаемый язык мог не быть записан на старых данных
        assert default_voice(None) == DEFAULT_VOICE["de"]
        assert default_voice("xx") == DEFAULT_VOICE["de"]
        assert voices_for("xx") == ()

    def test_preview_text_is_in_its_own_language(self):
        # Показывать акцент чужим текстом бессмысленно
        assert "lerne" in PREVIEW_TEXT["de"]
        assert "learn" in PREVIEW_TEXT["en"]
        assert "uczę" in PREVIEW_TEXT["pl"]
        assert "учу" in PREVIEW_TEXT["ru"]
        assert "вчу" in PREVIEW_TEXT["uk"]
        assert "öğreniyorum" in PREVIEW_TEXT["tr"]
