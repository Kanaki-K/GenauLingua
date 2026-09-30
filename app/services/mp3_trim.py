"""
Обрезка тишины в mp3 по кадрам, без перекодирования.

Зачем. Движок добавляет вокруг речи около полутора секунд тишины: у слова
«zum» речь занимает 0,39 секунды из 1,87, то есть 1,28 секунды в конце
человек слушает пустоту. На викторине из 25 вопросов это полминуты мёртвого
воздуха, и на слух это заметно сразу.

Почему по кадрам, а не перекодированием. mp3 состоит из кадров по 26 мс,
и лишние кадры в начале и конце можно просто выбросить: файл остаётся
правильным mp3, а звук не перекодируется и потому не теряет качества.
Перекодирование дало бы второе сжатие поверх первого — для речи это слышно.

Внутренняя тишина не трогается: пауза между словом и примером задана
намеренно, и без неё слово слиплось бы с началом фразы.
"""

from __future__ import annotations

import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Оставляемый запас вокруг речи. Без него срез приходится ровно на первый
# звук, и слово начинается с обрубленного согласного.
MARGIN_SECONDS = 0.08

# Доля от громчайшего места, ниже которой считаем тишиной. Речь имеет большой
# размах, и порог в два процента отделяет её от шумовой полки движка.
SILENCE_RATIO = 0.02

# Ниже этой длительности обрезать нечего: клип и так короткий
MIN_DURATION = 0.3

# Нижняя граница длительности готового клипа.
#
# Telegram показывает длительность с округлением вниз, и клип на 0,84 секунды
# отображается как «0:00» — выглядит битым файлом, хотя играет. Поэтому короткий
# клип добирается тишиной до секунды с небольшим: это дешевле, чем объяснять
# человеку, что нулевая длительность нормальна.
FLOOR_SECONDS = 1.05

_BITRATES_V1 = [0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, 0]
_BITRATES_V2 = [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160, 0]
_RATES_V1 = [44100, 48000, 32000, 0]
_RATES_V2 = [22050, 24000, 16000, 0]


def _id3_size(data: bytes) -> int:
    """Длина тега ID3v2 в начале файла, если он есть."""
    if len(data) > 10 and data[:3] == b"ID3":
        return 10 + (((data[6] & 0x7F) << 21) | ((data[7] & 0x7F) << 14)
                     | ((data[8] & 0x7F) << 7) | (data[9] & 0x7F))
    return 0


def frame_index(data: bytes) -> list[tuple[int, int, float]]:
    """
    Кадры файла: смещение, длина, длительность.

    Идём по заголовкам, а не по фиксированному шагу: битрейт в принципе может
    меняться между кадрами, и предполагать постоянный было бы догадкой.
    """
    frames: list[tuple[int, int, float]] = []
    offset = _id3_size(data)
    length = len(data)

    while offset + 4 <= length:
        if data[offset] != 0xFF or (data[offset + 1] & 0xE0) != 0xE0:
            offset += 1
            continue

        header = data[offset:offset + 4]
        version = (header[1] >> 3) & 0x03
        layer = (header[1] >> 1) & 0x03
        bitrate_index = (header[2] >> 4) & 0x0F
        rate_index = (header[2] >> 2) & 0x03
        padding = (header[2] >> 1) & 0x01

        if layer != 0x01 or bitrate_index in (0, 15) or rate_index == 3:
            offset += 1
            continue

        if version == 0x03:
            bitrate, rate, samples = _BITRATES_V1[bitrate_index], _RATES_V1[rate_index], 1152
        else:
            bitrate, rate, samples = _BITRATES_V2[bitrate_index], _RATES_V2[rate_index], 576

        if not bitrate or not rate:
            offset += 1
            continue

        size = (samples // 8 * bitrate * 1000) // rate + padding
        if size <= 0:
            offset += 1
            continue

        frames.append((offset, size, samples / rate))
        offset += size

    return frames


def speech_bounds(samples, sample_rate: int) -> Optional[tuple[float, float]]:
    """
    Где начинается и заканчивается речь, в секундах.

    По огибающей громкости, сглаженной окном в 10 мс: мгновенная амплитуда
    речи проходит через нуль много раз, и по ней границу не найти.
    """
    import numpy as np

    if samples.size == 0:
        return None

    window = max(1, sample_rate // 100)
    smooth = np.convolve(np.abs(samples), np.ones(window) / window, mode="same")
    peak = smooth.max()
    if peak <= 0:
        return None

    loud = np.where(smooth > peak * SILENCE_RATIO)[0]
    if loud.size == 0:
        return None
    return loud[0] / sample_rate, loud[-1] / sample_rate


def trim(data: bytes, decode) -> Optional[bytes]:
    """
    Убрать тишину в начале и конце, оставив запас.

    decode — функция, превращающая mp3 в массив отсчётов; передаётся снаружи,
    чтобы этот модуль не тянул за собой декодер.

    None означает «обрезать нечего или не получилось» — в этом случае надо
    оставить исходный файл, а не портить его.
    """
    frames = frame_index(data)
    if not frames:
        return None

    total = sum(f[2] for f in frames)
    if total < MIN_DURATION:
        return None

    try:
        samples = decode(data)
    except Exception:
        logger.debug("клип не декодировался, обрезка пропущена", exc_info=True)
        return None

    # Частота дискретизации нужна для перевода отсчётов в секунды; декодер
    # приводит к 16 кГц
    bounds = speech_bounds(samples, 16000)
    if bounds is None:
        return None

    start = max(0.0, bounds[0] - MARGIN_SECONDS)
    end = min(total, bounds[1] + MARGIN_SECONDS)
    if end - start < MIN_DURATION:
        return None

    # Добрать до нижней границы за счёт хвоста: он всё равно тишина, а плеер
    # не будет показывать нулевую длительность
    if end - start < FLOOR_SECONDS:
        end = min(total, start + FLOOR_SECONDS)

    # Нечего резать — не переписываем файл зря
    if start < 0.02 and total - end < 0.02:
        return None

    kept: list[bytes] = []
    elapsed = 0.0
    for offset, size, duration in frames:
        frame_end = elapsed + duration
        # Кадр пересекается с полезным отрезком — оставляем целиком
        if frame_end > start and elapsed < end:
            kept.append(data[offset:offset + size])
        elapsed = frame_end

    if not kept:
        return None

    head = data[:_id3_size(data)]
    return head + b"".join(kept)
