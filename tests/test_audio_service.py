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

    def test_polysemous_takes_meaning_from_example(self):
        """
        Из нескольких значений озвучивается то, которое стоит в примере, —
        решение владельца (HANDOVER §8). Не первое по списку.
        """
        word = make_word("Ahnung", ru="представление, понятие, догадка")
        word.example_ru = "Я понятия не имею"
        assert spoken_for(word, "ru", KIND_WORD) == "понятие"
        assert spoken_for(word, "ru", KIND_FULL).startswith("понятие")


class TestClipCompositionHasOneSource:
    """
    Состав клипов считается в ОДНОМ месте и той же функцией, которой
    озвучивает карточка.

    Зачем тест. Это расходилось дважды. Во второй раз
    `tts_synthesize.expected_clips` брал всю ячейку перевода и резал
    первое значение, тогда как карточка давно шла через `main_meaning` —
    5561 карточка из 77 412 получила пакетно клип, которого никогда не
    запросит. И `tts_prune_orphans`, считающий сирот по тому же составу,
    удалил бы ПРАВИЛЬНЫЕ клипы, оставив неправильные.

    Поймать это тестом на длительность или на наличие файлов нельзя:
    оба пути работают, просто про разные тексты. Ловится только
    сравнением источников.
    """

    def test_audit_and_synthesize_share_the_function(self):
        from app.scripts import tts_audit_clips, tts_synthesize

        assert tts_audit_clips.expected_clips is tts_synthesize.expected_clips

    def test_prune_orphans_uses_the_same_function(self):
        from app.scripts import tts_prune_orphans, tts_synthesize

        assert tts_prune_orphans.expected_clips is tts_synthesize.expected_clips

    def test_composition_goes_through_spoken_for(self):
        """
        `expected_clips` не должен сам решать, что произносится: ровно эта
        самодеятельность и разошлась с карточкой.
        """
        import inspect

        from app.scripts import tts_synthesize

        # Без docstring: в нём описан прежний сломанный код, и искать
        # запрещённый вызов надо в теле, а не в объяснении. Отрезаем по
        # закрывающим кавычкам, а не вычитанием `__doc__`: в файле CRLF,
        # и дословное вычитание не сходится
        src = inspect.getsource(tts_synthesize.expected_clips)
        body = src.split('"""')[-1]

        assert "spoken_for(" in body, "состав обязан идти через spoken_for"
        assert "word_clip_text(" not in body, (
            "своё вычисление произносимого текста: именно так расходилось"
        )


class TestBotOwnership:
    """
    file_id принадлежит конкретному боту и другому боту не передаётся.
    Клип чужого бота Telegram отклонит, поэтому он должен считаться промахом
    кэша, а не использоваться.
    """

    @pytest.mark.parametrize("token,expected", [
        ("1234567890:AAFakeTokenForTestsOnly_notReal", 1234567890),
        ("123:abc", 123),
        ("мусор", None),
        ("", None),
        (None, None),
        (":нет-цифр", None),
    ])
    def test_bot_id_from_token(self, token, expected):
        from app.services.audio_service import _bot_id_from_token

        assert _bot_id_from_token(token) == expected

    def test_id_taken_from_token_without_network(self):
        # Запрос к Telegram для этого не нужен: id стоит перед двоеточием
        from app.services.audio_service import current_bot_id

        assert isinstance(current_bot_id(), (int, type(None)))


class TestSynthesisRetry:
    """
    Озвучка должна быть у каждого слова, поэтому одна сетевая заминка не
    должна оставлять карточку беззвучной.

    ЗАГЛУШКИ ПРИНИМАЮТ ТРЕТИЙ ПАРАМЕТР — потолок ожидания. Он появился,
    когда бюджетов стало два: предсинтез может ждать восемь секунд на
    попытку, а путь человека не может ждать вовсе. У живого человека это и
    вскрылось: нажатие «Учить слова» собиралось 21 секунду, и он решил,
    что бот сломан.
    """

    async def test_the_human_path_does_not_retry(self, monkeypatch):
        """
        В пути человека попытка одна, и потолок короткий.

        Без этого «две попытки по восемь секунд» вернулись бы незаметно:
        остальные проверки этого класса смотрят на предсинтез.
        """
        from app.services import audio_service as svc

        seen = []

        async def note(text, voice, timeout=None, rate=None):
            seen.append(timeout)
            return None

        monkeypatch.setattr(svc, "_synthesize_once", note)
        monkeypatch.setattr(svc, "RETRY_PAUSE", 0)

        assert await svc._synthesize("x", "de-DE-KatjaNeural", live=True) is None
        assert len(seen) == svc.LIVE_SYNTH_ATTEMPTS == 1, (
            f"в пути человека попыток {len(seen)}, а должна одна"
        )
        assert seen == [svc.LIVE_SYNTH_TIMEOUT]
        assert svc.LIVE_SYNTH_TIMEOUT < svc.SYNTH_TIMEOUT

    async def test_second_attempt_saves_the_clip(self, monkeypatch):
        from app.services import audio_service as svc

        attempts = {"n": 0}

        async def flaky(text, voice, timeout=None, rate=None):
            attempts["n"] += 1
            return None if attempts["n"] == 1 else b"x" * 2000

        monkeypatch.setattr(svc, "_synthesize_once", flaky)
        monkeypatch.setattr(svc, "RETRY_PAUSE", 0)

        data = await svc._synthesize("die Fahrkarte", "de-DE-KatjaNeural")
        assert data is not None
        assert attempts["n"] == 2

    async def test_gives_up_after_the_limit(self, monkeypatch):
        from app.services import audio_service as svc

        attempts = {"n": 0}

        async def always_fails(text, voice, timeout=None, rate=None):
            attempts["n"] += 1
            return None

        monkeypatch.setattr(svc, "_synthesize_once", always_fails)
        monkeypatch.setattr(svc, "RETRY_PAUSE", 0)

        # Отказ честный: карточка выйдет текстовой, а не повиснет
        assert await svc._synthesize("x", "de-DE-KatjaNeural") is None
        assert attempts["n"] == svc.SYNTH_ATTEMPTS

    async def test_first_success_does_not_retry(self, monkeypatch):
        from app.services import audio_service as svc

        attempts = {"n": 0}

        async def fine(text, voice, timeout=None, rate=None):
            attempts["n"] += 1
            return b"x" * 2000

        monkeypatch.setattr(svc, "_synthesize_once", fine)
        assert await svc._synthesize("x", "de-DE-KatjaNeural") is not None
        assert attempts["n"] == 1


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


# ============================================================================
# ВОПРОС «СЛУШАЮ»: НАЗВАНИЕ КЛИПА НЕ ВЫДАЁТ ОТВЕТ
#
# Владелец, 14 октября: «Там на аудио написано название того, что
# прозвучало… в названии уже ответ». Плеер Telegram показывает название
# клипа над вариантами, а название клипа-слова — само слово.
# ============================================================================

class TestBlindClip:
    async def test_the_question_clip_does_not_name_the_word(self, session, monkeypatch):
        from app.services import audio_service as svc

        word = make_word("Verspätung", ru="опоздание")
        session.add(word)
        await session.commit()

        async def fake_obtain(spoken, lang, kind, voice, *, live=False):
            return b"mp3"

        monkeypatch.setattr(svc, "obtain_audio", fake_obtain)

        card = await svc.get_clip(session, word, "de", svc.KIND_WORD)
        blind = await svc.get_clip(session, word, "de", svc.KIND_BLIND)

        assert "Verspätung" in card.title, "у карточки название — слово"
        assert "Verspätung" not in blind.title, f"название выдаёт ответ: {blind.title}"
        assert "Verspätung" not in blind.filename
        assert blind.spoken_text == card.spoken_text, "звучать обязано то же слово"

    async def test_the_question_clip_is_the_word_file_on_disk(self, monkeypatch):
        """Вслепую — тот же файл, что у слова: второй синтез не нужен."""
        from app.services import audio_service as svc

        asked = []

        def read(lang, voice, kind, spoken):
            asked.append(kind)
            return b"mp3"

        monkeypatch.setattr(svc.audio_store, "read", read)
        data = await svc.obtain_audio("Verspätung", "de", svc.KIND_BLIND, "de-DE-KatjaNeural")
        assert data == b"mp3"
        assert asked == [svc.KIND_WORD]

    def test_the_audio_question_asks_for_a_blind_clip(self):
        """Вопрос на слух берёт клип вслепую — проверка по коду обработчика."""
        import inspect

        from app.bot.handlers.quiz import game

        import re

        source = inspect.getsource(game._question_clip)
        audio_branch = source.split("if channel is QuizChannel.AUDIO:")[1].split("if pair.reverse")[0]
        # Ищется САМ ВЫЗОВ, а не упоминание: первая редакция проверки искала
        # слово «KIND_BLIND» во всей ветке, находила его в комментарии и
        # оставалась зелёной при вернувшемся KIND_WORD — проверено поломкой
        calls = re.findall(r"clip_for_user\([^)]*\)", audio_branch)
        assert calls and all("KIND_BLIND" in c for c in calls), (
            f"вопрос на слух снова получит клип с названием-ответом: {calls}"
        )
