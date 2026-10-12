# -*- coding: utf-8 -*-
"""
Проверка произнесённого вслух: услышал ли бот нужное слово.

ЧЕГО ЭТА СЛУЖБА НЕ ДЕЛАЕТ, И ЭТО ВАЖНЕЕ ТОГО, ЧТО ДЕЛАЕТ.

Она НЕ оценивает качество произношения и не выдаёт процентов. Распознаватель
обучен ПОНИМАТЬ акцент, а не судить его — это его работа. Сильный русский
акцент в «Entschuldigung» он расшифрует правильно, и проверка «услышал ли он
нужное слово» поставила бы сто процентов всем подряд.

Доказательство из нашей же работы: один и тот же синтезированный клип со
словом «IBAN» распознаватель записал как «E-Bahn», «I ban», «Айбран»,
«ібан», «İban» и «i ban» — шесть разных написаний одного звука, и все шесть
были справедливо засчитаны совпадением. Он нормализует услышанное к
ближайшему правдоподобному слову, то есть прощает ровно то, что оценка
произношения должна замечать.

Поэтому ответ здесь ДВОИЧНЫЙ: слово узнано или нет. Честная оценка
произношения требует выравнивания записи по известному тексту с разбором по
каждому звуку — это отдельная работа, и делать вид, что она уже сделана,
хуже, чем не делать её вовсе: человек поверит проценту.

ПОЧЕМУ РАСПОЗНАВАНИЕ ИДЁТ В ОТДЕЛЬНОМ ПОТОКЕ. Оно занимает три-шесть секунд
ПРОЦЕССОРНОГО времени. Выполни его прямо в обработчике — и бот замрёт для
ВСЕХ пользователей на эти секунды, потому что обработчики делят один цикл
событий. Отсюда `asyncio.to_thread` и ограничение на число одновременных
распознаваний: больше двух на процессоре не ускоряют, а замедляют.
"""
from __future__ import annotations

import asyncio
import logging
import os
import re
import unicodedata
from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import Optional

logger = logging.getLogger(__name__)

# Модель распознавания. «small» — та же, на которой проверялась вся озвучка
# (7 176 клипов из 7 200 совпали), то есть её поведение здесь известно.
MODEL_SIZE = os.environ.get("ASR_MODEL", "small")

# Сколько распознаваний пускать одновременно. Работа процессорная: третий
# поток отбирает время у первых двух, а не добавляет пропускной способности.
MAX_PARALLEL = 2

# С какой доли совпадения считать слово узнанным.
#
# 0.75, а не 0.9: расшифровка короткого слова почти всегда приходит с чужой
# пунктуацией и капитализацией, иногда с артиклем, которого человек не
# произнёс. Требовать точного совпадения значило бы браковать верные ответы.
MATCH_THRESHOLD = 0.75

# Короче этого распознавать нечего: человек нажал и отпустил.
MIN_DURATION_SECONDS = 0.3

_PUNCT = re.compile(r"[^\w\s]", re.UNICODE)
_WS = re.compile(r"\s+")

_model = None
_model_lock = asyncio.Lock()
_slots = asyncio.Semaphore(MAX_PARALLEL)

# Коды языков, отличающиеся от наших двухбуквенных
ASR_LANG = {"uk": "uk", "tr": "tr", "pl": "pl", "de": "de", "en": "en", "ru": "ru"}


@dataclass(frozen=True)
class SpeechVerdict:
    """Ответ службы. `heard` пуст, если распознать не удалось вовсе."""

    heard: str
    matched: bool
    similarity: float
    failed: bool = False   # техническая неудача, а не ошибка ученика

    @property
    def empty(self) -> bool:
        return not self.heard.strip()


def _normalize(text: str, lang: Optional[str] = None) -> str:
    """
    Привести к виду для сравнения: без регистра, пунктуации и диакритики.

    Через `fold` из language_service, а не через `.lower()`: турецкая «İ» в
    Python даёт «i» с ОТДЕЛЬНОЙ комбинирующей точкой, и сравнение рвётся при
    полностью верной записи. Эта ловушка срабатывала уже четыре раза.
    """
    from app.services.language_service import fold

    text = unicodedata.normalize("NFC", text or "")
    text = _PUNCT.sub(" ", text)
    return _WS.sub(" ", fold(text)).strip()


def _strip_article(text: str, lang: Optional[str]) -> str:
    """
    Убрать ведущий артикль: человек его часто не произносит.

    «der Krieg» в задании, «Krieg» в ответе — ответ верный. Сравнение без
    этого браковало бы его из-за слова, которое к произношению САМОГО слова
    отношения не имеет.
    """
    parts = text.split(None, 1)
    if len(parts) == 2 and parts[0] in {"der", "die", "das", "the", "a", "an"}:
        return parts[1]
    return text


async def _get_model():
    global _model
    if _model is None:
        async with _model_lock:
            if _model is None:
                from faster_whisper import WhisperModel

                logger.info("загружаю модель распознавания речи (%s)", MODEL_SIZE)
                _model = await asyncio.to_thread(
                    WhisperModel, MODEL_SIZE, device="cpu", compute_type="int8"
                )
    return _model


def _transcribe_blocking(model, audio, lang: str) -> str:
    segments, _ = model.transcribe(
        audio, language=ASR_LANG.get(lang, lang), beam_size=1,
        vad_filter=False, condition_on_previous_text=False,
    )
    return " ".join(seg.text for seg in segments).strip()


async def check_pronunciation(
    data: bytes, target: str, lang: str
) -> SpeechVerdict:
    """
    Услышал ли бот слово `target` в записи `data`.

    `data` — голосовое сообщение Telegram как есть (OGG/Opus). Декодер один
    на весь проект (`mp3_trim.decode`): он опирается на PyAV, а тот
    определяет формат сам, поэтому второй копии под другой контейнер не
    нужно.
    """
    from app.services.mp3_trim import DECODE_SAMPLE_RATE, decode

    try:
        audio = await asyncio.to_thread(decode, data)
    except Exception:
        logger.exception("не удалось раскодировать голосовое")
        return SpeechVerdict(heard="", matched=False, similarity=0.0, failed=True)

    if audio.size < DECODE_SAMPLE_RATE * MIN_DURATION_SECONDS:
        # Нажал и отпустил — это не ответ, и засчитывать ошибку нечестно
        return SpeechVerdict(heard="", matched=False, similarity=0.0, failed=True)

    try:
        model = await _get_model()
        async with _slots:
            heard = await asyncio.to_thread(_transcribe_blocking, model, audio, lang)
    except Exception:
        logger.exception("распознавание речи не удалось")
        return SpeechVerdict(heard="", matched=False, similarity=0.0, failed=True)

    want = _strip_article(_normalize(target, lang), lang)
    got = _strip_article(_normalize(heard, lang), lang)
    if not want:
        return SpeechVerdict(heard=heard, matched=False, similarity=0.0, failed=True)

    ratio = SequenceMatcher(None, want, got).ratio()

    # Слово, произнесённое внутри фразы, тоже засчитывается: человек мог
    # сказать «das ist ein Krieg» вместо одного слова, и это не ошибка
    if want and want in got:
        ratio = max(ratio, 1.0)

    return SpeechVerdict(
        heard=heard, matched=ratio >= MATCH_THRESHOLD, similarity=ratio
    )
