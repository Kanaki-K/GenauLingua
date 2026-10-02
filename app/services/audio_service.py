"""
Озвучка слова: клип с диска, загрузка в Telegram один раз, дальше по file_id.

Три уровня, и разделены они по цене.

  1. Файл на диске. Синтез — дорогая и невосполнимая часть: часы работы через
     недокументированный endpoint, который Microsoft может закрыть в любой
     день. Поэтому клип сохраняется файлом и больше не зависит ни от движка,
     ни от того, каким ботом его отправят. См. app/services/audio_store.py.
  2. file_id в базе. Загрузка дешёвая, но file_id принадлежит конкретному
     боту и другому не передаётся. Кэшируется отдельно на каждого бота, и
     чужая запись считается промахом.
  3. Синтез. Последняя линия: только если на диске клипа нет.

Клип нужен в двух видах: «слово» для вопроса и «слово с примером» для разбора.
Загрузка совмещена с показом карточки — отдельного шага нет, карточку всё
равно отправлять. Из ответа берётся file_id, и все следующие показы идут по
нему: мгновенно и бесплатно.

Поэтому пустые и диск, и кэш — рабочее состояние. Предгенерация ускоряет
первый показ, но ничего не блокирует: бот работает с нуля.

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
from app.services import audio_store
from app.services.language_service import example_text, main_meaning, word_text
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

# Сколько раз пробовать. Одна сетевая заминка не должна лишать слово звука:
# без повтора карточка выходила бы текстовой из-за моргнувшего соединения.
# Попыток две, а не больше: третья заметна на глаз, а озвучка не настолько
# важна, чтобы держать человека перед пустой карточкой.
SYNTH_ATTEMPTS = 2
RETRY_PAUSE = 0.4


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
    """
    Текст, который произносится: после разворота сокращений и чисел.

    Берётся не вся ячейка перевода, а одно значение — то, которое стоит в
    примере и показано на карточке. Прежде сюда шла вся ячейка, а
    word_clip_text отрезал первое значение: для «Swot, overachiever, nerd»
    голос говорил «Swot», тогда как пример был про «overachiever». Теперь
    показанное, произнесённое и то, что в примере, — одно и то же слово.
    """
    raw_word = main_meaning(word, lang)
    if kind == KIND_FULL:
        return full_clip_text(raw_word, example_text(word, lang), lang)
    return word_clip_text(raw_word, lang)


# Вид клипа для образца голоса. Отдельный от слов, чтобы образцы не мешались
# с озвучкой базы и не попадали в её проверки.
KIND_PREVIEW = "preview"


async def synthesize_preview(lang: str, voice: str) -> Optional[bytes]:
    """
    Образец голоса для настроек: одна фраза на языке этого голоса.

    Идёт через то же хранилище, что и слова, по двум причинам. Образец
    обрезается от тишины — в настройках человек слушает несколько голосов
    подряд, и полторы секунды пустоты после каждого заметны сильнее всего.
    И второй раз он уже не синтезируется: голосов на все языки девятнадцать,
    файлов выходит девятнадцать.

    В word_audio не кэшируется: это не слово из базы, и file_id ему незачем.
    """
    from app.services.tts_voices import preview_text

    resolved = resolve_voice(voice, lang)
    return await obtain_audio(preview_text(lang), lang, KIND_PREVIEW, resolved)


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


async def _synthesize_once(text: str, voice: str) -> Optional[bytes]:
    """Одна попытка синтеза. None, если движок не ответил или отдал пустоту."""
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
    except Exception as exc:
        logger.warning("синтез не удался (%s): %r", type(exc).__name__, text[:40])
        return None

    # Пустой или подозрительно короткий ответ — это не звук
    if len(data) < 500:
        logger.warning("синтез вернул %d байт для %r — слишком мало", len(data), text[:40])
        return None
    return data


async def _synthesize(text: str, voice: str) -> Optional[bytes]:
    """
    Синтез с повтором.

    Озвучка должна быть у каждого слова, поэтому одна сетевая заминка не должна
    оставлять карточку без звука. Повтор дешевле, чем потерянный клип: после
    успеха file_id сохраняется навсегда, а после отказа слово осталось бы
    беззвучным до следующего показа.
    """
    for attempt in range(1, SYNTH_ATTEMPTS + 1):
        data = await _synthesize_once(text, voice)
        if data is not None:
            if attempt > 1:
                logger.info("синтез удался со второй попытки: %r", text[:40])
            return data
        if attempt < SYNTH_ATTEMPTS:
            await asyncio.sleep(RETRY_PAUSE)

    logger.warning(
        "озвучка недоступна после %d попыток, карточка будет текстовой: %r",
        SYNTH_ATTEMPTS, text[:40],
    )
    return None


def _trimmed(data: bytes) -> bytes:
    """
    Убрать тишину вокруг речи.

    Обязательно здесь, а не только в пакетном прогоне: движок добавляет около
    полутора секунд тишины, и клип, синтезированный на ходу, звучал бы иначе,
    чем взятый из хранилища. Человек слышал бы часть слов с пустотой в конце,
    а часть без — и это было бы виднее всего при смене голоса, где на ходу
    синтезируется каждое слово.

    Обрезка не критична: не получилось — отдаём как есть, со звуком всё
    в порядке, просто длиннее.
    """
    from app.services import mp3_trim

    try:
        out = mp3_trim.trim(data, mp3_trim.decode)
    except Exception:
        # Декодер тянет av и numpy: если их на сервере нет, обрезки не будет,
        # и это не повод терять озвучку
        logger.debug("обрезка не удалась", exc_info=True)
        return data

    return out if out is not None else data


async def obtain_audio(
    spoken: str, lang: str, kind: str, voice: str
) -> Optional[bytes]:
    """
    Клип: с диска, а если там нет — синтезом, и тогда сразу на диск.

    Порядок именно такой, потому что синтез — дорогая и невосполнимая часть.
    Один раз синтезированный клип живёт файлом и больше не зависит ни от
    работоспособности движка, ни от того, каким ботом его потом отправят.

    Синтезированное здесь же обрезается: в хранилище клипы уже без тишины, и
    новый клип должен звучать так же.
    """
    stored = audio_store.read(lang, voice, kind, spoken)
    if stored is not None:
        return stored

    data = await _synthesize(spoken, voice)
    if data is None:
        return None

    data = _trimmed(data)

    # Запись на диск не критична: не получилось — клип всё равно отдаём,
    # просто в следующий раз он синтезируется снова
    audio_store.write(lang, voice, kind, spoken, data)
    return data


def _bot_id_from_token(token: Optional[str]) -> Optional[int]:
    """
    Числовой id бота из токена: он стоит перед двоеточием.

    Нужен, чтобы отличать свои клипы от чужих. Запрос к Telegram для этого
    делать незачем — id есть в самом токене.
    """
    if not token or ":" not in token:
        return None
    head = token.split(":", 1)[0]
    return int(head) if head.isdigit() else None


def current_bot_id() -> Optional[int]:
    from app.config import settings

    return _bot_id_from_token(getattr(settings, "BOT_TOKEN", None))


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

    # Название клипа — ровно то, что в нём звучит. Прежде сюда шла вся
    # ячейка перевода, и в заголовке стояло «Swot, overachiever, nerd», тогда
    # как голос произносил одно слово.
    raw_word = main_meaning(word, lang)
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
    bot_id = current_bot_id()

    # Запись годна, только если совпали и текст, и бот:
    #   текст — перевод могли исправить, тогда клип озвучивает не то слово;
    #   бот   — file_id принадлежит конкретному боту, чужой Telegram отклонит.
    usable = (
        cached is not None
        and cached.spoken_text == spoken
        and cached.bot_id == bot_id
    )
    if usable:
        return AudioClip(
            kind=kind, voice=voice, spoken_text=spoken, title=title,
            filename=audio_filename(title), file_id=cached.file_id,
        )

    data = await obtain_audio(spoken, lang, kind, voice)
    if data is None:
        return None

    if cached:
        # Либо текст изменился, либо клип чужого бота — в обоих случаях
        # старый file_id к делу не относится
        if cached.bot_id != bot_id:
            logger.info(
                "клип слова %s сделан другим ботом (%s вместо %s) — переделываю",
                word.id, cached.bot_id, bot_id,
            )
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
            duration_seconds=duration_seconds, bot_id=current_bot_id(),
        )
    )
    try:
        await session.flush()
    except IntegrityError:
        await session.rollback()
        logger.debug("кэш озвучки уже заполнен другим показом: word=%s", word_id)
