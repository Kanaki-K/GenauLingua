"""
Озвучка слова: синтез, загрузка в Telegram один раз, дальше по file_id.

Как это работает. Клип нужен в двух видах: «слово» для вопроса и «слово с
примером» для разбора. При первом обращении клип синтезируется и уходит в
Telegram вместе с самой карточкой — отдельной загрузки нет, карточку всё
равно отправлять. Из ответа берётся file_id и кладётся в кэш; все следующие
показы этого слова идут по file_id: без синтеза, без загрузки, мгновенно.

Поэтому пустой кэш — рабочее состояние. Предгенерация базы ускоряет первый
показ, но ничего не блокирует: бот работает и с нуля.

Отправляется обычным аудио, а не голосовым сообщением. Голосовые может
запретить сам получатель настройкой приватности Telegram Premium
(VOICE_MESSAGES_FORBIDDEN — проверено, на ботов распространяется), и тогда
викторина падала бы на первом вопросе. Обычное аудио этой настройкой не
блокируется, а карточка получается такая же: звук, подпись и кнопки в одном
сообщении.

Озвучка нигде не является обязательной. Если синтез не удался, карточка
выходит текстовой — потерять звук допустимо, потерять викторину нет.
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from typing import Optional

import edge_tts
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User, UserTtsVoice, Word, WordAudio
from app.services.language_service import example_text, word_text
from app.services.tts_text import full_clip_text, needs_context, word_clip_text
from app.services.tts_voices import DEFAULT_RATE, resolve_voice

logger = logging.getLogger(__name__)

# Вид клипа
KIND_WORD = "word"   # только слово — в вопросе
KIND_FULL = "full"   # слово и пример — на разборе

# Сколько слов примера попадает в название клипа. Примеры разной длины, а
# карточки должны выглядеть одинаково, поэтому пример всегда обрезается.
TITLE_EXAMPLE_WORDS = 3

# Синтез — сетевой вызов к недокументированному endpoint. Ждать его дольше
# нескольких секунд нельзя: человек смотрит на карточку.
SYNTH_TIMEOUT = 8.0


@dataclass
class AudioClip:
    """
    Чем отправлять карточку.

    file_id заполнен — клип уже в Telegram, отправка бесплатная и мгновенная.
    data заполнен — клип синтезирован только что, уйдёт вместе с карточкой,
    и после отправки его file_id нужно запомнить через remember().
    """
    kind: str
    voice: str
    spoken_text: str
    title: str
    filename: str
    file_id: Optional[str] = None
    data: Optional[bytes] = None

    @property
    def needs_remembering(self) -> bool:
        return self.file_id is None and self.data is not None


def audio_title(word: str, example: Optional[str] = None) -> str:
    """
    Название клипа — ровно то, что в нём звучит, и ничего больше.

    Для клипа со словом это само слово. Для клипа с примером — слово и начало
    примера: полный пример сделал бы названия разной длины, и карточки
    выглядели бы неряшливо.
    """
    if not example:
        return word

    parts = example.split()
    head = " ".join(parts[:TITLE_EXAMPLE_WORDS]).rstrip(",.;:!?—–-")
    if len(parts) > TITLE_EXAMPLE_WORDS:
        head += "…"
    return f"{word} — {head}"


def audio_filename(title: str) -> str:
    """Имя файла из названия: его видно там, где плеер не читает теги."""
    safe = "".join(c if (c.isalnum() or c in " -_—…") else "" for c in title).strip()
    return f"{safe or 'audio'}.mp3"


def clip_kind_for_question(word: Word, lang: Optional[str]) -> str:
    """
    Какой клип ставить в вопрос.

    Обычно достаточно слова. Но гетероним, произнесённый отдельно, читается
    наугад — «modern» и «umfahren» имеют по два чтения, и движок выбирает
    сам. Управлять этим нельзя: SSML недоступен. Поэтому такому слову в
    вопрос идёт клип с примером: контекст задаёт чтение однозначно.
    """
    if needs_context(word_text(word, lang), lang):
        return KIND_FULL
    return KIND_WORD


def spoken_for(word: Word, lang: Optional[str], kind: str) -> str:
    """Текст, который произносится: после разворота сокращений и чисел."""
    raw_word = word_text(word, lang)
    if kind == KIND_FULL:
        return full_clip_text(raw_word, example_text(word, lang), lang)
    return word_clip_text(raw_word, lang)


async def voice_for_user(
    session: AsyncSession, user_id: int, lang: str
) -> str:
    """Выбранный голос для этого языка, иначе голос по умолчанию."""
    chosen = await session.scalar(
        select(UserTtsVoice.voice).where(
            UserTtsVoice.user_id == user_id,
            UserTtsVoice.lang == lang,
        )
    )
    return resolve_voice(chosen, lang)


async def set_voice_for_user(
    session: AsyncSession, user_id: int, lang: str, voice: str
) -> None:
    """Запомнить выбор голоса. Чужой для языка голос не сохраняется."""
    from app.services.tts_voices import is_valid_voice

    if not is_valid_voice(voice, lang):
        logger.warning("голос %r не принадлежит языку %r — не сохранён", voice, lang)
        return

    existing = await session.get(UserTtsVoice, (user_id, lang))
    if existing:
        existing.voice = voice
    else:
        session.add(UserTtsVoice(user_id=user_id, lang=lang, voice=voice))


async def clip_for_user(
    session: AsyncSession,
    user: User,
    word: Word,
    lang: str,
    kind: str,
) -> Optional["AudioClip"]:
    """
    Клип с учётом настроек ученика. None — озвучки не будет.

    Единственная точка, через которую карточка получает звук: и выключатель,
    и выбор голоса, и отказ синтеза сходятся здесь в один ответ «есть или нет».
    """
    if not getattr(user, "audio_enabled", True):
        return None
    voice = await voice_for_user(session, user.id, lang)
    return await get_clip(session, word, lang, kind, voice)


async def _synthesize(text: str, voice: str) -> Optional[bytes]:
    """Синтез в память. None, если движок не ответил или отдал пустоту."""
    async def run() -> bytes:
        data = b""
        stream = edge_tts.Communicate(text, voice, rate=DEFAULT_RATE).stream()
        async for chunk in stream:
            if chunk["type"] == "audio":
                data += chunk["data"]
        return data

    try:
        data = await asyncio.wait_for(run(), timeout=SYNTH_TIMEOUT)
    except asyncio.TimeoutError:
        logger.warning("синтез не успел за %.0f с: %r", SYNTH_TIMEOUT, text[:40])
        return None
    except Exception:
        logger.exception("синтез не удался: %r", text[:40])
        return None

    # Пустой или подозрительно короткий ответ — это не звук
    if len(data) < 500:
        logger.warning("синтез вернул %d байт для %r — слишком мало", len(data), text[:40])
        return None
    return data


async def get_clip(
    session: AsyncSession,
    word: Word,
    lang: str,
    kind: str,
    voice: Optional[str] = None,
) -> Optional[AudioClip]:
    """
    Клип для карточки: из кэша или синтезированный на месте.

    None означает «озвучки не будет» — карточка должна выйти текстовой.
    """
    voice = resolve_voice(voice, lang)
    spoken = spoken_for(word, lang, kind)
    if not spoken:
        return None

    raw_word = word_text(word, lang)
    example = example_text(word, lang) if kind == KIND_FULL else None
    title = audio_title(raw_word, example)

    cached = await session.scalar(
        select(WordAudio).where(
            WordAudio.word_id == word.id,
            WordAudio.lang == lang,
            WordAudio.kind == kind,
            WordAudio.voice == voice,
        )
    )
    # Кэш устаревает при правке перевода: текст изменился — клип не тот
    if cached and cached.spoken_text == spoken:
        return AudioClip(
            kind=kind, voice=voice, spoken_text=spoken, title=title,
            filename=audio_filename(title), file_id=cached.file_id,
        )

    data = await _synthesize(spoken, voice)
    if data is None:
        return None

    if cached:
        # Текст изменился — старый file_id больше не соответствует слову
        await session.delete(cached)
        await session.flush()

    return AudioClip(
        kind=kind, voice=voice, spoken_text=spoken, title=title,
        filename=audio_filename(title), data=data,
    )


async def remember(
    session: AsyncSession,
    word_id: int,
    lang: str,
    clip: AudioClip,
    file_id: str,
    duration_seconds: Optional[int] = None,
) -> None:
    """
    Запомнить file_id после отправки: больше этот клип не синтезируется.

    Гонка возможна — два ученика могли открыть одно слово одновременно.
    Проигравший вставку просто откатывается: в кэше уже есть годная запись.
    """
    session.add(
        WordAudio(
            word_id=word_id, lang=lang, kind=clip.kind, voice=clip.voice,
            file_id=file_id, file_kind="audio", spoken_text=clip.spoken_text,
            duration_seconds=duration_seconds,
        )
    )
    try:
        await session.flush()
    except IntegrityError:
        await session.rollback()
        logger.debug("кэш озвучки уже заполнен другим показом: word=%s", word_id)
