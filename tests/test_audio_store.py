"""
Файловое хранилище озвучки.

Смысл хранилища в том, что синтез — дорогая и невосполнимая часть, а загрузка
в Telegram дешёвая. Поэтому клип обязан переживать и смену бота, и недоступность
движка. Тесты держат именно это свойство.
"""

import pytest

from app.services import audio_store


@pytest.fixture
def root(tmp_path):
    return tmp_path / "tts"


class TestKey:
    """Ключ — от произносимого текста, а не от id слова."""

    def test_same_text_same_path(self, root):
        first = audio_store.clip_path("de", "v", "word", "das Haus", root)
        second = audio_store.clip_path("de", "v", "word", "das Haus", root)
        assert first == second

    def test_changed_text_changes_path(self, root):
        # Перевод исправили — клип обязан стать другим, иначе озвучивалось бы
        # уже не то слово
        old = audio_store.clip_path("de", "v", "word", "das Haus", root)
        new = audio_store.clip_path("de", "v", "word", "das Heim", root)
        assert old != new

    def test_voice_is_part_of_the_key(self, root):
        katja = audio_store.clip_path("de", "de-DE-KatjaNeural", "word", "Haus", root)
        conrad = audio_store.clip_path("de", "de-DE-ConradNeural", "word", "Haus", root)
        assert katja != conrad

    def test_kind_is_part_of_the_key(self, root):
        word = audio_store.clip_path("de", "v", "word", "Haus", root)
        full = audio_store.clip_path("de", "v", "full", "Haus", root)
        assert word != full

    def test_language_is_part_of_the_key(self, root):
        # «Bank» есть и в немецком, и в английском, но читается по-разному
        de = audio_store.clip_path("de", "v", "word", "Bank", root)
        en = audio_store.clip_path("en", "v", "word", "Bank", root)
        assert de != en

    def test_files_are_spread_across_directories(self, root):
        # В одном каталоге не должно оказаться 25 тысяч файлов
        paths = [
            audio_store.clip_path("de", "v", "word", f"слово {i}", root)
            for i in range(200)
        ]
        parents = {p.parent for p in paths}
        assert len(parents) > 20, "файлы свалены в один каталог"

    def test_path_stays_readable(self, root):
        path = audio_store.clip_path("de", "de-DE-KatjaNeural", "word", "das Haus", root)
        parts = path.relative_to(root).parts
        assert parts[0] == "de"
        assert parts[1] == "de-DE-KatjaNeural"
        assert parts[2] == "word"
        assert path.suffix == ".mp3"


class TestWriteRead:
    def test_roundtrip(self, root):
        data = b"x" * 3000
        assert audio_store.write("de", "v", "word", "Haus", data, root) is not None
        assert audio_store.read("de", "v", "word", "Haus", root) == data

    def test_missing_is_none(self, root):
        assert audio_store.read("de", "v", "word", "нет такого", root) is None

    def test_exists(self, root):
        assert audio_store.exists("de", "v", "word", "Haus", root) is False
        audio_store.write("de", "v", "word", "Haus", b"x" * 3000, root)
        assert audio_store.exists("de", "v", "word", "Haus", root) is True

    def test_directories_created_as_needed(self, root):
        assert not root.exists()
        audio_store.write("de", "v", "word", "Haus", b"x" * 3000, root)
        assert root.exists()

    def test_no_leftover_temporary_files(self, root):
        audio_store.write("de", "v", "word", "Haus", b"x" * 3000, root)
        # Запись идёт через временный файл с переименованием — «.part»
        # остаться не должен
        assert list(root.rglob("*.part")) == []


class TestCorruptionIsNotAClip:
    """
    Прерванный прогон мог оставить обрывок. Обрывок, выглядящий как готовый
    клип, хуже отсутствующего: он ушёл бы человеку как звук.
    """

    def test_tiny_data_is_not_written(self, root):
        assert audio_store.write("de", "v", "word", "Haus", b"abc", root) is None
        assert audio_store.exists("de", "v", "word", "Haus", root) is False

    def test_tiny_file_reads_as_missing(self, root):
        path = audio_store.clip_path("de", "v", "word", "Haus", root)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"abc")
        assert audio_store.read("de", "v", "word", "Haus", root) is None
        assert audio_store.exists("de", "v", "word", "Haus", root) is False

    def test_empty_file_reads_as_missing(self, root):
        path = audio_store.clip_path("de", "v", "word", "Haus", root)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"")
        assert audio_store.read("de", "v", "word", "Haus", root) is None


class TestStats:
    def test_empty_store(self, root):
        result = audio_store.stats(root)
        assert result["clips"] == 0
        assert result["bytes"] == 0

    def test_counts_by_language(self, root):
        audio_store.write("de", "v", "word", "Haus", b"x" * 3000, root)
        audio_store.write("de", "v", "full", "Haus ist", b"x" * 5000, root)
        audio_store.write("en", "v", "word", "house", b"x" * 2000, root)

        result = audio_store.stats(root)
        assert result["clips"] == 3
        assert result["bytes"] == 10000
        assert result["by_lang"]["de"]["clips"] == 2
        assert result["by_lang"]["en"]["clips"] == 1


class TestObtainAudio:
    """
    Порядок обращения: сначала диск, потом синтез. Клип, уже лежащий файлом,
    не должен синтезироваться повторно — в этом весь смысл хранилища.
    """

    async def test_disk_hit_skips_synthesis(self, root, monkeypatch):
        from app.services import audio_service

        monkeypatch.setattr(audio_store, "DEFAULT_ROOT", root)
        audio_store.write("de", "v", "word", "das Haus", b"x" * 3000, root)

        calls = {"n": 0}

        async def must_not_run(text, voice):
            calls["n"] += 1
            return b"y" * 3000

        monkeypatch.setattr(audio_service, "_synthesize", must_not_run)

        data = await audio_service.obtain_audio("das Haus", "de", "word", "v")
        assert data == b"x" * 3000
        assert calls["n"] == 0, "клип был на диске, синтез не нужен"

    async def test_miss_synthesizes_and_stores(self, root, monkeypatch):
        from app.services import audio_service

        monkeypatch.setattr(audio_store, "DEFAULT_ROOT", root)

        async def fake(text, voice):
            return b"z" * 3000

        monkeypatch.setattr(audio_service, "_synthesize", fake)

        data = await audio_service.obtain_audio("das Haus", "de", "word", "v")
        assert data == b"z" * 3000
        # Синтезированный клип остался на диске: второй раз он не понадобится
        assert audio_store.exists("de", "v", "word", "das Haus", root)

    async def test_failed_synthesis_stores_nothing(self, root, monkeypatch):
        from app.services import audio_service

        monkeypatch.setattr(audio_store, "DEFAULT_ROOT", root)

        async def fails(text, voice):
            return None

        monkeypatch.setattr(audio_service, "_synthesize", fails)

        assert await audio_service.obtain_audio("das Haus", "de", "word", "v") is None
        assert not audio_store.exists("de", "v", "word", "das Haus", root)

    async def test_fresh_clip_is_trimmed(self, root, monkeypatch):
        """
        Клип, синтезированный на ходу, должен звучать так же, как взятый из
        хранилища. Иначе человек слышал бы часть слов с пустотой в конце, а
        часть без — заметнее всего при смене голоса, где на ходу синтезируется
        каждое слово.
        """
        from app.services import audio_service

        monkeypatch.setattr(audio_store, "DEFAULT_ROOT", root)

        async def fake(text, voice):
            return b"x" * 4000

        trimmed = {"called": False}

        def fake_trim(data):
            trimmed["called"] = True
            return b"x" * 2000

        monkeypatch.setattr(audio_service, "_synthesize", fake)
        monkeypatch.setattr(audio_service, "_trimmed", fake_trim)

        data = await audio_service.obtain_audio("das Haus", "de", "word", "v")
        assert trimmed["called"], "новый клип не прошёл обрезку"
        assert data == b"x" * 2000
        # На диск попадает обрезанное, а не исходное
        assert audio_store.read("de", "v", "word", "das Haus", root) == b"x" * 2000

    async def test_stored_clip_is_not_trimmed_again(self, root, monkeypatch):
        from app.services import audio_service

        monkeypatch.setattr(audio_store, "DEFAULT_ROOT", root)
        audio_store.write("de", "v", "word", "das Haus", b"y" * 3000, root)

        def must_not_run(data):
            raise AssertionError("клип с диска обрезали повторно")

        monkeypatch.setattr(audio_service, "_trimmed", must_not_run)

        assert await audio_service.obtain_audio("das Haus", "de", "word", "v") == b"y" * 3000

    async def test_trim_failure_keeps_the_clip(self, root, monkeypatch):
        """Обрезка не критична: со звуком всё в порядке, просто длиннее."""
        from app.services import audio_service, mp3_trim

        monkeypatch.setattr(audio_store, "DEFAULT_ROOT", root)

        async def fake(text, voice):
            return b"x" * 4000

        def broken(data, decode):
            raise RuntimeError("декодер недоступен")

        monkeypatch.setattr(audio_service, "_synthesize", fake)
        monkeypatch.setattr(mp3_trim, "trim", broken)

        assert await audio_service.obtain_audio("das Haus", "de", "word", "v") == b"x" * 4000
