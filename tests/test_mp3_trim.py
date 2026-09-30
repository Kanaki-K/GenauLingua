"""
Обрезка тишины в mp3 по кадрам.

Главное свойство — идемпотентность: обрезку приходится запускать повторно
после каждого досинтеза, и без неё каждый прогон срезал бы оставленный запас,
а хвост слова постепенно съедался.
"""

import pytest

from app.services import mp3_trim


def make_frames(count: int) -> bytes:
    """
    Синтетический mp3: кадры с корректными заголовками и нулевым содержимым.

    Нужен, чтобы проверять разбор кадров и арифметику без настоящего звука.
    Заголовок: MPEG-2 Layer III, 48 кбит/с, 22,05 кГц — то же, что отдаёт движок.
    """
    # 0xFF 0xF3: MPEG-2, Layer III, без CRC; 0x40: 48 кбит/с, 22,05 кГц
    header = bytes([0xFF, 0xF3, 0x40, 0xC4])
    samples, bitrate, rate = 576, 48, 22050
    size = (samples // 8 * bitrate * 1000) // rate
    frame = header + bytes(size - 4)
    return frame * count


class TestFrameIndex:
    def test_counts_frames(self):
        frames = mp3_trim.frame_index(make_frames(10))
        assert len(frames) == 10

    def test_frame_duration_is_plausible(self):
        frames = mp3_trim.frame_index(make_frames(1))
        assert len(frames) == 1
        # 576 отсчётов при 22,05 кГц — это 26 мс
        assert 0.02 < frames[0][2] < 0.03

    def test_id3_tag_skipped(self):
        # Тег ID3v2 длиной 10 байт заголовка плюс нулевой размер
        tag = b"ID3" + bytes([3, 0, 0, 0, 0, 0, 0])
        frames = mp3_trim.frame_index(tag + make_frames(5))
        assert len(frames) == 5

    def test_garbage_gives_nothing(self):
        assert mp3_trim.frame_index(b"not an mp3 at all") == []

    def test_empty_gives_nothing(self):
        assert mp3_trim.frame_index(b"") == []


class TestSpeechBounds:
    def test_silence_has_no_bounds(self):
        import numpy as np

        assert mp3_trim.speech_bounds(np.zeros(16000, dtype=np.float32), 16000) is None

    def test_finds_loud_section(self):
        import numpy as np

        samples = np.zeros(16000, dtype=np.float32)
        samples[8000:12000] = 0.5      # речь с 0,5 по 0,75 секунды
        bounds = mp3_trim.speech_bounds(samples, 16000)
        assert bounds is not None
        start, end = bounds
        assert 0.4 < start < 0.55
        assert 0.7 < end < 0.85

    def test_empty_array(self):
        import numpy as np

        assert mp3_trim.speech_bounds(np.zeros(0, dtype=np.float32), 16000) is None


class TestTrimDecisions:
    """
    Решения обрезки проверяются через подставной декодер: настоящий звук для
    этого не нужен, а нужна арифметика границ.
    """

    def _decoder(self, speech_from: float, speech_to: float, total: float):
        import numpy as np

        def decode(data: bytes):
            samples = np.zeros(int(total * 16000), dtype=np.float32)
            samples[int(speech_from * 16000):int(speech_to * 16000)] = 0.5
            return samples

        return decode

    def test_trims_long_trailing_silence(self):
        data = make_frames(80)                       # около 1,9 секунды
        total = sum(f[2] for f in mp3_trim.frame_index(data))
        decode = self._decoder(0.2, 0.6, total)
        out = mp3_trim.trim(data, decode)
        assert out is not None
        assert len(out) < len(data)

    def test_already_trimmed_is_left_alone(self):
        """
        Без этого повторный прогон срезал бы оставленный запас, и хвост слова
        съедался бы с каждым разом.
        """
        data = make_frames(80)
        total = sum(f[2] for f in mp3_trim.frame_index(data))
        # Речь занимает почти весь клип, тишины ровно на запас
        decode = self._decoder(
            mp3_trim.MARGIN_SECONDS, total - mp3_trim.MARGIN_SECONDS, total
        )
        assert mp3_trim.trim(data, decode) is None

    def test_short_clip_padded_to_floor_is_left_alone(self):
        """
        У короткого слова хвост оставлен намеренно — чтобы Telegram не
        показывал «0:00». Такой клип тоже считается обрезанным.
        """
        # Число кадров считается из нижней границы, а не вписано: кадр длится
        # 26 мс, и вписанное число разъехалось бы с ней при правке константы
        frame = mp3_trim.frame_index(make_frames(1))[0][2]
        data = make_frames(int(mp3_trim.FLOOR_SECONDS / frame))
        total = sum(f[2] for f in mp3_trim.frame_index(data))
        assert total <= mp3_trim.FLOOR_SECONDS + mp3_trim.FRAME_SLACK
        decode = self._decoder(mp3_trim.MARGIN_SECONDS, 0.5, total)
        assert mp3_trim.trim(data, decode) is None

    def test_silence_only_clip_is_not_touched(self):
        import numpy as np

        data = make_frames(80)

        def decode(data_bytes):
            return np.zeros(16000, dtype=np.float32)

        assert mp3_trim.trim(data, decode) is None

    def test_very_short_clip_is_not_touched(self):
        data = make_frames(5)                        # около 0,12 секунды
        total = sum(f[2] for f in mp3_trim.frame_index(data))
        assert total < mp3_trim.MIN_DURATION
        assert mp3_trim.trim(data, self._decoder(0.0, total, total)) is None

    def test_result_is_still_a_valid_mp3(self):
        data = make_frames(80)
        total = sum(f[2] for f in mp3_trim.frame_index(data))
        out = mp3_trim.trim(data, self._decoder(0.8, 1.2, total))
        assert out is not None
        # Обрезанный файл по-прежнему разбирается на кадры
        assert mp3_trim.frame_index(out)

    def test_failing_decoder_leaves_file_alone(self):
        def decode(data_bytes):
            raise RuntimeError("декодер не смог")

        assert mp3_trim.trim(make_frames(80), decode) is None

    def test_garbage_input(self):
        import numpy as np

        assert mp3_trim.trim(b"not mp3", lambda d: np.zeros(100)) is None
