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

# Модель распознавания — «base» (2.2.1, владелец: «скорость важнее, больше
# 5 секунд ждать нельзя»). Прод 14–18.10 на «small»: медиана 4,8 с, у
# каждого десятого 9,4 с, максимум 18,2 с — сверх пяти секунд. Замер 18.10
# на 80 клипах четырёх языков, 2 потока как на сервере: «base» с подсказкой
# слова — в 3,3 раза быстрее, 78 из 80 верно (у «small» с подсказкой 79),
# ложных засчитываний 0. Не понял дважды — вопрос и так проходит пропуском,
# а не ошибкой. Переопределяется `ASR_MODEL` (образ кладёт её же).
MODEL_SIZE = os.environ.get("ASR_MODEL", "base")

# Сколько распознаваний пускать одновременно. Работа процессорная: третий
# поток отбирает время у первых двух, а не добавляет пропускной способности.
MAX_PARALLEL = 2

# С какой доли совпадения считать слово узнанным.
#
# 0.75, а не 0.9: расшифровка короткого слова почти всегда приходит с чужой
# пунктуацией и капитализацией, иногда с артиклем, которого человек не
# произнёс. Требовать точного совпадения значило бы браковать верные ответы.
MATCH_THRESHOLD = 0.75

# ПОДСКАЗКА ОЖИДАЕМОГО СЛОВА — СРАЗУ, ОДНИМ ПРОХОДОМ (2.2.1).
#
# Зачем подсказка. Живой тест владельца 14 октября: сказал «der Streit»,
# распознаватель услышал «Verstrahlt!». Короткое слово без контекста модель
# путает с созвучным, а мы ЗНАЕМ, какое слово ждём.
#
# Прежде она давалась ВТОРЫМ проходом и только «созвучному промаху» (сходство
# 0.4–0.75): боялись, что подсказка заставит засчитывать что попало. Второй
# проход удваивал время — 8 голосовых из 44 на проде, отсюда хвосты до 18 с.
# Замер 18.10 этот страх снял: клип слова A с подсказкой слова B — 0 ложных
# засчитываний на всех трёх моделях, а верных с подсказкой больше (78 против
# 68 из 80 у «base»). И раньше проверено: «die Stadt» и «der Stern» с
# подсказкой «der Streit» остались собой.

# Короче этого распознавать нечего: человек нажал и отпустил.
MIN_DURATION_SECONDS = 0.3

_PUNCT = re.compile(r"[^\w\s]", re.UNICODE)
_WS = re.compile(r"\s+")

_model = None
_model_lock = asyncio.Lock()
_slots = asyncio.Semaphore(MAX_PARALLEL)

# Коды языков, отличающиеся от наших двухбуквенных
ASR_LANG = {"uk": "uk", "tr": "tr", "pl": "pl", "de": "de", "en": "en", "ru": "ru",
            "it": "it", "es": "es", "fr": "fr", "cs": "cs"}


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
    if len(parts) == 2 and parts[0] in articles_for(lang):
        return parts[1]
    return text


def articles_for(lang: Optional[str]) -> frozenset[str]:
    """
    Ведущие служебные слова языка — из реестра (`leading_particles`), в том
    виде, какой они принимают после `_normalize`.

    Н3 (16.10): прежде здесь стояли только der/die/das/the/a/an, и
    итальянское «il libro», сказанное как «libro», могло не засчитаться.
    Элизия — отдельная ловушка: `_normalize` снимает апостроф, и «l'uomo»
    приходит как «l uomo». Поэтому «l'» из реестра хранится как «l».
    """
    from app.services.language_service import LANGUAGES

    base = {"der", "die", "das", "the", "a", "an"}
    language = LANGUAGES.get(lang or "")
    extra = language.leading_particles if language else ()
    return frozenset(base | {_normalize(p.rstrip("'’"), lang) for p in extra})


async def _get_model():
    global _model
    if _model is None:
        async with _model_lock:
            if _model is None:
                from faster_whisper import WhisperModel

                logger.info("загружаю модель распознавания речи (%s)", MODEL_SIZE)
                model = await asyncio.to_thread(
                    WhisperModel, MODEL_SIZE, device="cpu", compute_type="int8"
                )
                # ПРОГРЕВ: первое распознавание после загрузки медленнее
                # остальных — его платит бот при старте, а не первый человек
                try:
                    import numpy as np

                    await asyncio.to_thread(
                        _transcribe_blocking, model, np.zeros(16000, dtype=np.float32), "de")
                except Exception:
                    logger.debug("прогрев распознавания не удался", exc_info=True)
                _model = model
    return _model


def _transcribe_blocking(model, audio, lang: str, hint: Optional[str] = None) -> str:
    # beam_size=5, а не 1: точнее на коротких словах, а по времени замер
    # 14.10 разницы почти не показал (3.6 с против 3.8 на одном слове)
    segments, _ = model.transcribe(
        audio, language=ASR_LANG.get(lang, lang), beam_size=5,
        vad_filter=False, condition_on_previous_text=False,
        initial_prompt=hint,
    )
    return " ".join(seg.text for seg in segments).strip()


# Артикли, которые распознаватель приклеивает к слову: «Derstreit»
_ARTICLES = ("der", "die", "das", "the", "a", "an")


def _glue_articles(lang: Optional[str]) -> tuple[str, ...]:
    """Артикли для склейки: прежние плюс артикли языка («luomo», «illibro»)."""
    return tuple(sorted(set(_ARTICLES) | articles_for(lang)))

# Короткое слово сверяется ТОЛЬКО ЦЕЛИКОМ. Доля совпадения у него ничего не
# говорит: «Eis» и «Reise» дают ровно 0.75, «Ohr» и «Rohr» — 0.86, то есть
# порог «узнано» проходит чужое слово. Таких целей в немецкой базе 191.
SHORT_WORD = 4


def _contains(want: str, got: str, lang: Optional[str] = None) -> bool:
    """
    Есть ли искомое в услышанном ЦЕЛЫМИ СЛОВАМИ.

    Прежде сверка шла подстрокой — `want in got`, — и искомое внутри
    ЧУЖОГО слова засчитывалось: «das Ei» по записи «nein» и «Bleistift»,
    «in» по «Kino», «an» по «Mann», «die Uhr» по «Fuhrmann». Проверено
    исполнением, сходство 1.00 у всех.

    Теперь — по границам слов:

      * искомое стоит в услышанном подряд идущими словами («das ist ein
        Krieg» — Krieg засчитан);
      * склейка — только СОСЕДНИХ слов: распознаватель пишет «Derstreit»
        или «Stra ße», и такое слово, склеенное из соседей, совпадает с
        искомым без пробелов (с артиклем впереди или без).
    """
    if not want:
        return False
    w_tokens = want.split()
    g_tokens = got.split()
    n = len(w_tokens)
    for i in range(len(g_tokens) - n + 1):
        if g_tokens[i:i + n] == w_tokens:
            return True

    bare = want.replace(" ", "")
    glued = {bare} | {article + bare for article in _glue_articles(lang)}
    longest = max(len(g) for g in glued)
    for i in range(len(g_tokens)):
        joined = ""
        for token in g_tokens[i:]:
            joined += token
            if joined in glued:
                return True
            if len(joined) >= longest:
                break
    return False


def _threshold(want: str) -> float:
    """С какой доли совпадения слово узнано: короткое — только целиком."""
    return 1.0 if len(want.replace(" ", "")) <= SHORT_WORD else MATCH_THRESHOLD


def _similarity(want: str, got: str, lang: Optional[str] = None) -> float:
    if _contains(want, got, lang):
        return 1.0
    return SequenceMatcher(None, want, got).ratio()


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
            # Один проход с подсказкой ожидаемого слова (см. выше)
            heard = await asyncio.to_thread(_transcribe_blocking, model, audio, lang, target)
    except Exception:
        logger.exception("распознавание речи не удалось")
        return SpeechVerdict(heard="", matched=False, similarity=0.0, failed=True)

    want = _strip_article(_normalize(target, lang), lang)
    got = _strip_article(_normalize(heard, lang), lang)
    if not want:
        return SpeechVerdict(heard=heard, matched=False, similarity=0.0, failed=True)

    ratio = _similarity(want, got, lang)
    threshold = _threshold(want)

    return SpeechVerdict(
        heard=heard, matched=ratio >= threshold, similarity=ratio
    )
