"""
Файловое хранилище озвучки: синтезированные клипы на диске.

Зачем оно, если есть кэш file_id. Потому что это разные вещи с разной ценой.

Синтез — дорогая и невосполнимая часть: он занимает часы и идёт через
недокументированный endpoint, который Microsoft может закрыть в любой день.
Загрузка в Telegram — дешёвая: секунда на клип и никаких внешних зависимостей.

При этом file_id принадлежит конкретному боту и другому боту не передаётся.
Если хранить только его, всю дорогую работу пришлось бы повторять на каждом
боте — и каждый раз надеяться, что движок ещё работает.

Поэтому клипы лежат файлами, а file_id кэшируется поверх них отдельно на
каждого бота. Озвучка базы делается один раз, переносится копированием
каталога и от движка больше не зависит.

Раскладка по каталогам:
    tts/<язык>/<голос>/<вид>/<первые два символа хеша>/<хеш>.mp3

Хеш считается от произносимого текста, а не от id слова: если перевод
исправили, текст изменился, и клип должен быть другим. Заодно одинаковые
фразы не дублируются.

Разбиение по двум символам хеша нужно, чтобы в одном каталоге не оказалось
25 тысяч файлов — на этом спотыкаются и файловые системы, и прочие
инструменты.
"""

from __future__ import annotations

import hashlib
import logging
import os
import pathlib
from typing import Optional

logger = logging.getLogger(__name__)

# Каталог хранилища. Переопределяется через окружение: на сервере он может
# лежать на отдельном диске.
DEFAULT_ROOT = pathlib.Path(os.environ.get("TTS_STORE", "tts"))

# Клип короче этого — не звук, а обрывок. Тот же порог, что при синтезе.
MIN_CLIP_BYTES = 500


def text_hash(spoken_text: str) -> str:
    """
    Ключ клипа — от произносимого текста.

    Не от id слова: перевод могут исправить, и тогда клип обязан стать другим.
    Шестнадцати символов достаточно: столкновение на 25 тысячах записей
    практически невозможно, а путь остаётся читаемым.
    """
    digest = hashlib.sha256(spoken_text.encode("utf-8")).hexdigest()
    return digest[:16]


def clip_path(
    lang: str,
    voice: str,
    kind: str,
    spoken_text: str,
    root: Optional[pathlib.Path] = None,
) -> pathlib.Path:
    base = root or DEFAULT_ROOT
    digest = text_hash(spoken_text)
    return base / lang / voice / kind / digest[:2] / f"{digest}.mp3"


def read(
    lang: str,
    voice: str,
    kind: str,
    spoken_text: str,
    root: Optional[pathlib.Path] = None,
) -> Optional[bytes]:
    """Клип с диска. None, если его нет или он повреждён."""
    path = clip_path(lang, voice, kind, spoken_text, root)
    try:
        if not path.exists():
            return None
        data = path.read_bytes()
    except OSError:
        logger.warning("клип не читается: %s", path, exc_info=True)
        return None

    if len(data) < MIN_CLIP_BYTES:
        # Обрывок мог остаться от прерванной записи — лучше переделать
        logger.warning("клип подозрительно мал (%d Б), считаю отсутствующим: %s",
                       len(data), path)
        return None
    return data


def write(
    lang: str,
    voice: str,
    kind: str,
    spoken_text: str,
    data: bytes,
    root: Optional[pathlib.Path] = None,
) -> Optional[pathlib.Path]:
    """
    Записать клип.

    Сначала во временный файл, потом переименованием: иначе прерванный прогон
    оставил бы обрывок, который выглядел бы как готовый клип.
    """
    if len(data) < MIN_CLIP_BYTES:
        return None

    path = clip_path(lang, voice, kind, spoken_text, root)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix(".part")
        temporary.write_bytes(data)
        temporary.replace(path)
    except OSError:
        logger.warning("клип не записался: %s", path, exc_info=True)
        return None
    return path


def exists(
    lang: str,
    voice: str,
    kind: str,
    spoken_text: str,
    root: Optional[pathlib.Path] = None,
) -> bool:
    path = clip_path(lang, voice, kind, spoken_text, root)
    try:
        return path.exists() and path.stat().st_size >= MIN_CLIP_BYTES
    except OSError:
        return False


def stats(root: Optional[pathlib.Path] = None) -> dict:
    """Сколько клипов и сколько места — для отчёта о состоянии хранилища."""
    base = root or DEFAULT_ROOT
    if not base.exists():
        return {"clips": 0, "bytes": 0, "by_lang": {}}

    by_lang: dict[str, dict[str, int]] = {}
    total_clips = total_bytes = 0

    for path in base.rglob("*.mp3"):
        try:
            size = path.stat().st_size
        except OSError:
            continue
        # tts/<язык>/<голос>/<вид>/<xx>/<хеш>.mp3
        try:
            lang = path.relative_to(base).parts[0]
        except ValueError:
            continue
        entry = by_lang.setdefault(lang, {"clips": 0, "bytes": 0})
        entry["clips"] += 1
        entry["bytes"] += size
        total_clips += 1
        total_bytes += size

    return {"clips": total_clips, "bytes": total_bytes, "by_lang": by_lang}
