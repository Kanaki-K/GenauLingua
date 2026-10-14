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
from app.services.language_service import (
    example_text,
    main_meaning,
    option_label,
    word_text,
)
from app.services.tts_text import full_clip_text, needs_context, word_clip_text
from app.services.tts_voices import DEFAULT_RATE, resolve_voice

logger = logging.getLogger(__name__)

# Вид клипа
KIND_WORD = "word"   # только слово — в вопросе
KIND_FULL = "full"   # слово и пример — на разборе

# КЛИП ВСЛЕПУЮ — для вопроса «Слушаю». Звучит то же слово, что в KIND_WORD,
# и лежит на диске тем же файлом, но в кэше Telegram это СВОЯ запись с
# нейтральным названием. Владелец, 14 октября: «Там на аудио написано
# название того, что прозвучало… в названии уже ответ». Telegram впечатывает
# название при загрузке и при отправке по file_id менять его не даёт, так
# что одна запись на два названия невозможна: карточка и вопрос
# перезаливали бы клип друг за другом без конца.
#
# Название одно на все языки интерфейса по той же причине: запись в кэше
# общая для всех людей, и «Слушай» на шести языках снова заставило бы её
# метаться.
KIND_BLIND = "blind"
BLIND_TITLE = "GenauLingua"

# МЕДЛЕННЫЙ КЛИП — для кнопки под вопросом «Говорю». Прежде кнопка
# «Послушать» присылала ТО ЖЕ аудио, что уже висит на карточке; владелец:
# «Зачем нам ещё 1 кнопка… которая присылает в чат такое же аудио?…
# пусть лучше будет кнопка, которая пришлёт эту озвучку, но медленнее».
# Свой файл на диске и своя запись в кэше: темп другой, звук другой.
KIND_SLOW = "slow"
SLOW_RATE = "-45%"
SLOW_TITLE_MARK = "· 0.6×"

# Сколько слов примера попадает в название клипа. Примеры разной длины, а
# карточки должны выглядеть одинаково, поэтому пример всегда обрезается.
TITLE_EXAMPLE_WORDS = 3

# ИСПОЛНИТЕЛЯ У КЛИПА НЕТ ВОВСЕ. На карточке должно стоять только то, что
# в ней звучит.
#
# Здесь было два неверных значения подряд. Сперва имя бота — и владелец
# спросил по делу: «почему в каждой записи, названии файла озвучки есть
# ГенауЛингва? Можно это убрать, чтобы в названии было то, про что
# озвучивается». Я заменил его на язык слова, и стало хуже: «сейчас ты
# сделал Дойч — Ди критик. Я хочу Ди Критик и всё. Для чего нам дойч этот
# постоянно?»
#
# Он прав оба раза, и правило из этого простое: подпись, одинаковая у всех
# клипов, не несёт ничего. Язык человек и так выбрал сам, имя бота стоит в
# заголовке чата. Остаётся название — слово и начало примера, — и этого
# достаточно.
#
# Поле просто не отправляется. Прежний довод «без него Telegram напишет
# „Неизвестен“» — не довод: пустая строка под названием тише, чем одно и
# то же слово на каждом клипе.
#
# Подпись впечатывается в файл при загрузке и по file_id не меняется —
# значит эта правка требует чистки кэша: DELETE FROM word_audio.

# Синтез — сетевой вызов к недокументированному endpoint.
#
# ДВА БЮДЖЕТА, И ЭТО ГЛАВНОЕ ЗДЕСЬ. Прежде был один: 8 секунд на попытку,
# попыток две, пауза между ними — до 16.4 секунды на ОДИН клип. А вопросу
# бывает нужно два (слово и фраза). У живого человека это и случилось:
# «сейчас пытался начать снова через Учить слова — не запускалось», и в
# журнале стоит `Duration 17542 ms` и `21422 ms` на одно нажатие. Бот не
# падал, он СИНТЕЗИРОВАЛ, а человек смотрел в пустой экран двадцать секунд
# и решил, что сломано. Он прав: двадцать секунд — это сломано.
#
#   путь человека   ждать нельзя: одна попытка и короткий потолок, а не
#                   успели — вопрос выходит текстовым, и это честный ответ
#   предсинтез      ждать можно и нужно: скрипт никого не держит, и каждый
#                   удавшийся клип избавляет от синтеза навсегда
SYNTH_TIMEOUT = 8.0
LIVE_SYNTH_TIMEOUT = 2.5

# Сколько раз пробовать. Одна сетевая заминка не должна лишать слово звука:
# без повтора карточка выходила бы текстовой из-за моргнувшего соединения.
# Попыток две, а не больше: третья заметна на глаз, а озвучка не настолько
# важна, чтобы держать человека перед пустой карточкой.
#
# В пути человека повтора нет вовсе: пауза между попытками — это ещё
# полсекунды его ожидания, а звук не настолько важен.
SYNTH_ATTEMPTS = 2
LIVE_SYNTH_ATTEMPTS = 1
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
    """
    Имя файла из названия: его видно там, где плеер не читает теги.

    Апостроф оставлен в разрешённых: без него «That's a good option» давало
    имя «Thats a good…», и человек видел слово с опечаткой. В именах файлов
    апостроф допустим и Telegram его принимает.
    """
    safe = "".join(c if (c.isalnum() or c in " -_—…'") else "" for c in title).strip()
    return f"{safe or 'audio'}.mp3"


def clip_kind_for_question(word: Word, lang: Optional[str]) -> str:
    """
    Какой клип ставить в вопрос.

    Обычно достаточно слова. Но гетероним, произнесённый отдельно, читается
    наугад — «modern» и «umfahren» имеют по два чтения, и движок выбирает
    сам. Управлять этим нельзя: SSML недоступен. Поэтому такому слову в
    вопрос идёт клип с примером: контекст задаёт чтение однозначно.

    СПРАШИВАТЬ НАДО ПРО ТО, ЧТО РЕАЛЬНО ПРОИЗНОСИТСЯ. Прежде сюда шёл
    `word_text` — ВСЯ ячейка перевода, «to live, to reside, to be alive».
    Список гетеронимов состоит из одиночных слов, такая строка в нём не
    находится, и ряд получал изолированный клип. А произносится в нём
    `main_meaning`, то есть именно «to live» — гетероним, отданный движку
    без контекста.

    Замер на момент правки: клип с примером получали 25 рядов, а должны
    были 109. **Восемьдесят четыре гетеронима читались наугад** — «to
    live» (/lɪv/ или /laɪv/), «to present», «to refuse», «to use»,
    «close», «subject», «number».

    Пересинтеза не требует: оба клипа у ряда уже есть, меняется только
    какой из них ставится в вопрос.
    """
    if needs_context(main_meaning(word, lang), lang):
        return KIND_FULL
    return KIND_WORD


def spoken_for(word: Word, lang: Optional[str], kind: str) -> str:
    """
    Текст, который произносится: после разворота сокращений.

    Числа не разворачиваются — их нормализует сам движок, и делает это
    лучше: наш разворот ломал падеж и порядковую форму (см. раздел ЧИСЛА
    в `tts_text`).

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
    # live=True — это путь ЧЕЛОВЕКА: он смотрит на карточку и ждать не
    # должен. Нет готового клипа и синтез не успел за две с половиной
    # секунды — вопрос выйдет текстовым.
    return await get_clip(session, word, lang, kind, voice, live=True)


async def _synthesize_once(
    text: str, voice: str, timeout: float = SYNTH_TIMEOUT, rate: str = DEFAULT_RATE,
) -> Optional[bytes]:
    """Одна попытка синтеза. None, если движок не ответил или отдал пустоту."""
    async def run() -> bytes:
        data = b""
        stream = edge_tts.Communicate(text, voice, rate=rate).stream()
        async for chunk in stream:
            if chunk["type"] == "audio":
                data += chunk["data"]
        return data

    try:
        data = await asyncio.wait_for(run(), timeout=timeout)
    except asyncio.TimeoutError:
        logger.warning("синтез не успел за %.1f с: %r", timeout, text[:40])
        return None
    except Exception as exc:
        logger.warning("синтез не удался (%s): %r", type(exc).__name__, text[:40])
        return None

    # Пустой или подозрительно короткий ответ — это не звук
    if len(data) < 500:
        logger.warning("синтез вернул %d байт для %r — слишком мало", len(data), text[:40])
        return None
    return data


async def _synthesize(
    text: str, voice: str, *, live: bool = False, rate: str = DEFAULT_RATE,
) -> Optional[bytes]:
    """
    Синтез с повтором.

    Озвучка должна быть у каждого слова, поэтому одна сетевая заминка не должна
    оставлять карточку без звука. Повтор дешевле, чем потерянный клип: после
    успеха file_id сохраняется навсегда, а после отказа слово осталось бы
    беззвучным до следующего показа.
    """
    attempts = LIVE_SYNTH_ATTEMPTS if live else SYNTH_ATTEMPTS
    timeout = LIVE_SYNTH_TIMEOUT if live else SYNTH_TIMEOUT

    for attempt in range(1, attempts + 1):
        data = await _synthesize_once(text, voice, timeout, rate)
        if data is not None:
            if attempt > 1:
                logger.info("синтез удался со второй попытки: %r", text[:40])
            return data
        if attempt < attempts:
            await asyncio.sleep(RETRY_PAUSE)

    logger.warning(
        "озвучка недоступна после %d попыток (%s), карточка будет текстовой: %r",
        attempts, "путь человека" if live else "предсинтез", text[:40],
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
    spoken: str, lang: str, kind: str, voice: str, *, live: bool = False
) -> Optional[bytes]:
    """
    Клип: с диска, а если там нет — синтезом, и тогда сразу на диск.

    Порядок именно такой, потому что синтез — дорогая и невосполнимая часть.
    Один раз синтезированный клип живёт файлом и больше не зависит ни от
    работоспособности движка, ни от того, каким ботом его потом отправят.

    Синтезированное здесь же обрезается: в хранилище клипы уже без тишины, и
    новый клип должен звучать так же.
    """
    # Клип вслепую — тот же звук, что у слова: и на диске это тот же файл
    if kind == KIND_BLIND:
        kind = KIND_WORD

    stored = audio_store.read(lang, voice, kind, spoken)
    if stored is not None:
        return stored

    rate = SLOW_RATE if kind == KIND_SLOW else DEFAULT_RATE
    data = await _synthesize(spoken, voice, live=live, rate=rate)
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
    *,
    live: bool = False,
) -> Optional[AudioClip]:
    """
    Клип для карточки: из кэша или синтезированный на месте.

    None означает «озвучки не будет» — карточка должна выйти текстовой.
    """
    voice = resolve_voice(voice, lang)
    spoken = spoken_for(word, lang, kind)
    if not spoken:
        return None

    # Название клипа — ровно то, что в нём звучит, и в той же записи, что
    # на карточке. Прежде сюда шла вся ячейка перевода, и в заголовке
    # стояло «Swot, overachiever, nerd», тогда как голос произносил одно
    # слово; это было исправлено на `main_meaning`.
    #
    # Теперь берётся `option_label` — то же значение, но с заглавной по
    # правилам языка. Разница видна на русском: карточка показывала
    # «Автобус», а название клипа было «автобус». Владелец попросил, чтобы
    # совпадало буква в букву: «если написано der Bus, то и на аудиофайле
    # der Bus». По-немецки регистр и так не трогается — там он значим.
    #
    # На имя файла в хранилище это не влияет: ключ там хеш ПРОИЗНОСИМОГО
    # текста, а не названия, поэтому переименование ничего не осиротило.
    example = example_text(word, lang) if kind == KIND_FULL else None
    title = (BLIND_TITLE if kind == KIND_BLIND
             else audio_title(option_label(word, lang), example))
    if kind == KIND_SLOW:
        title = f"{title} {SLOW_TITLE_MARK}"

    cached = await session.scalar(
        select(WordAudio).where(
            WordAudio.word_id == word.id,
            WordAudio.lang == lang,
            WordAudio.kind == kind,
            WordAudio.voice == voice,
        )
    )
    bot_id = current_bot_id()

    # Запись годна, только если совпали текст, название и бот:
    #   текст    — перевод могли исправить, тогда клип озвучивает не то слово;
    #   название — при отправке по file_id Telegram параметр title ИГНОРИРУЕТ
    #              и берёт метаданные первой загрузки. Правка правила названия
    #              текста не меняет, и без этой сверки карточка молча
    #              показывала бы старое название при верном звуке;
    #   бот      — file_id принадлежит конкретному боту, чужой Telegram
    #              отклонит.
    #
    # Записи, сделанные до появления колонки, хранят title = NULL и потому
    # негодны: переделать дешевле, чем гадать, с каким названием их грузили.
    usable = (
        cached is not None
        and cached.spoken_text == spoken
        and cached.title == title
        and cached.bot_id == bot_id
    )
    if usable:
        return AudioClip(
            kind=kind, voice=voice, spoken_text=spoken, title=title,
            filename=audio_filename(title), file_id=cached.file_id,
        )

    data = await obtain_audio(spoken, lang, kind, voice, live=live)
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


# Из чего состоит настоящий file_id, и почему это проверяется.
#
# Telegram отдаёт длинную строку в base64url. Поддельный — короткий и с
# посторонними знаками: `fake-file-3292`. Отправь такой обратно, и Telegram
# ответит «wrong remote file identifier: Wrong padding in the string», а
# ученик увидит оборвавшийся круг.
#
# ЭТО НЕ ПАРАНОЙЯ, А СЛЕД НАСТОЯЩЕЙ БЕДЫ. В рабочей копии базы оказалось
# 3 251 такой запись. Написали их собственные приёмки — `show_screens` и
# `audit_round` играют круг через ПОДДЕЛЬНОГО бота, а запоминание клипа
# складывает его «file_id» в ОБЩИЙ кэш озвучки, а не в данные подопытного.
# Обе клялись в своих описаниях, что только читают и что подопытного за
# собой убирают, — и обе травили озвучку всем, кто пользуется той же базой.
#
# Правило вместо запрета на поддельного бота: проверяется САМ file_id в
# единственном месте, где он попадает в кэш. Любой другой путь к подделке
# закрыт тем же условием.
_FILE_ID_ALPHABET = set(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_="
)
FILE_ID_MIN_LENGTH = 30


def plausible_file_id(file_id: Optional[str]) -> bool:
    """Похоже ли это на file_id Telegram. Коротким и с чужими знаками — нет."""
    if not file_id or len(file_id) < FILE_ID_MIN_LENGTH:
        return False
    return set(file_id) <= _FILE_ID_ALPHABET


async def forget(session: AsyncSession, word_id: int, lang: str,
                 kind: str, voice: str) -> None:
    """
    Забыть запись кэша: её file_id Telegram отклонил.

    Удаление, а не правка: следующий показ переделает запись целиком, с
    верными названием, текстом и ботом. Чинить мёртвую запись по частям
    значит гадать, что именно в ней устарело.
    """
    from sqlalchemy import delete as sa_delete

    await session.execute(
        sa_delete(WordAudio).where(
            WordAudio.word_id == word_id,
            WordAudio.lang == lang,
            WordAudio.kind == kind,
            WordAudio.voice == voice,
        )
    )
    await session.commit()
    logger.info(
        "кэш озвучки очищен: слово %s %s %s %s — Telegram отклонил file_id",
        word_id, lang, kind, voice,
    )


async def reobtain(clip: AudioClip, lang: str) -> Optional[AudioClip]:
    """
    Тот же клип, но ЗВУКОМ, а не ссылкой: с диска, иначе синтезом.

    Нужен, когда file_id оказался мёртвым. Без этого вопрос на слух просто
    не появлялся бы: отправить нечего.

    Язык передаётся, а не берётся из клипа: в `AudioClip` его нет, и
    дописывать поле ради одного вызова значит менять то, что собирается в
    пяти местах.
    """
    data = await obtain_audio(clip.spoken_text, lang, clip.kind, clip.voice, live=True)
    if data is None:
        return None
    return AudioClip(
        kind=clip.kind, voice=clip.voice, spoken_text=clip.spoken_text,
        title=clip.title, filename=clip.filename, data=data,
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

    Название сохраняется вместе с file_id, и это обязательно: Telegram
    впечатывает его в клип при загрузке и при отправке по file_id менять не
    даёт. Без записи названия проверка годности в `get_clip` не находила бы
    совпадения никогда и переделывала бы клип при каждом показе.
    """
    if not plausible_file_id(file_id):
        logger.warning(
            "file_id %r не похож на телеграмный — в кэш не пишу (слово %s %s)",
            file_id, word_id, lang,
        )
        return

    session.add(
        WordAudio(
            word_id=word_id, lang=lang, kind=clip.kind, voice=clip.voice,
            file_id=file_id, file_kind="audio", spoken_text=clip.spoken_text,
            title=clip.title,
            duration_seconds=duration_seconds, bot_id=current_bot_id(),
        )
    )
    try:
        await session.flush()
    except IntegrityError:
        await session.rollback()
        logger.debug("кэш озвучки уже заполнен другим показом: word=%s", word_id)
