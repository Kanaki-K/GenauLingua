# -*- coding: utf-8 -*-
"""
Проверка всех клипов озвучки: не обрезан ли, не пустой ли, той ли длины.

Зачем, если есть проверка распознаванием. Она дорогая и потому прошла только
по немецким клипам с примером — 12 746 из 105 478. Остальные 92 тысячи не
проверены ничем, а за часы синтеза любой из них мог выйти обрезанным: сетевая
заминка даёт корректный mp3 меньшей длины, и ни размер файла, ни отсутствие
ошибок этого не покажут.

Эта проверка дешёвая и потому идёт по всем клипам без исключения. Она не
слышит слов — она смотрит, похожа ли длительность на ожидаемую по тексту.
Обрезанный клип, пустой клип, клип из одной тишины и клип, в котором
произнесена часть фразы, находятся именно так.

Ожидаемая длительность считается от числа символов: речь при скорости −10%
идёт примерно с постоянным темпом, и отклонение вдвое от него означает, что
с клипом что-то не то.

    python -m app.scripts.tts_audit_clips                  # все языки
    python -m app.scripts.tts_audit_clips --lang de --show 20
    python -m app.scripts.tts_audit_clips --delete-broken   # удалить негодные
"""
from __future__ import annotations

import argparse
import asyncio
import os
import pathlib
import statistics
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
os.environ.setdefault("ENV_FILE", ".env.local")

from sqlalchemy import text

from app.database.session import AsyncSessionLocal
from app.services import audio_store
from app.services.audio_service import KIND_FULL, KIND_WORD
from app.services.language_service import LANGUAGES, SUPPORTED_LANGS
from app.services.tts_text import full_clip_text, word_clip_text
from app.services.tts_voices import default_voice

ORDER = ("de", "en", "uk", "ru", "tr", "pl")

# Клип короче этого — не звук. Тот же порог, что при синтезе и в хранилище.
MIN_BYTES = 500

# Во сколько раз длительность может отличаться от ожидаемой, прежде чем клип
# считается подозрительным. Порог широкий намеренно: темп речи зависит от
# состава звуков, и узкий порог дал бы ложные срабатывания на коротких словах.
TOLERANCE_LOW = 0.45
TOLERANCE_HIGH = 2.2

# Совсем короткие клипы проверяются только на непустоту: у слова из трёх букв
# длительность определяется не длиной, а произношением
MIN_CHARS_FOR_DURATION = 8


def mp3_duration(data: bytes) -> float | None:
    """
    Длительность mp3 по его собственным кадрам.

    Считаем сами, а не через стороннюю библиотеку: нужна одна величина, а
    поднимать ради неё декодер на 105 тысячах файлов расточительно. Разбор
    заголовков кадров надёжен для того, что отдаёт edge-tts, — это постоянный
    битрейт и одна частота дискретизации.
    """
    # Таблицы битрейтов и частот для MPEG-1/2 Layer III
    bitrates_v1 = [0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, 0]
    bitrates_v2 = [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160, 0]
    rates_v1 = [44100, 48000, 32000, 0]
    rates_v2 = [22050, 24000, 16000, 0]

    offset = 0
    length = len(data)

    # Пропустить тег ID3v2, если он есть
    if data[:3] == b"ID3" and length > 10:
        size = ((data[6] & 0x7F) << 21) | ((data[7] & 0x7F) << 14) \
               | ((data[8] & 0x7F) << 7) | (data[9] & 0x7F)
        offset = 10 + size

    total = 0.0
    frames = 0

    while offset + 4 <= length:
        if data[offset] != 0xFF or (data[offset + 1] & 0xE0) != 0xE0:
            offset += 1
            continue

        header = data[offset:offset + 4]
        version_bits = (header[1] >> 3) & 0x03
        layer = (header[1] >> 1) & 0x03
        bitrate_index = (header[2] >> 4) & 0x0F
        rate_index = (header[2] >> 2) & 0x03
        padding = (header[2] >> 1) & 0x01

        if layer != 0x01 or bitrate_index in (0, 15) or rate_index == 3:
            offset += 1
            continue

        if version_bits == 0x03:          # MPEG-1
            bitrate = bitrates_v1[bitrate_index]
            rate = rates_v1[rate_index]
            samples = 1152
        else:                              # MPEG-2 / 2.5
            bitrate = bitrates_v2[bitrate_index]
            rate = rates_v2[rate_index]
            samples = 576

        if not bitrate or not rate:
            offset += 1
            continue

        frame_size = (samples // 8 * bitrate * 1000) // rate + padding
        if frame_size <= 0:
            offset += 1
            continue

        total += samples / rate
        frames += 1
        offset += frame_size

    return total if frames else None


async def expected_clips(lang: str) -> list[tuple[str, str]]:
    """Что должно быть в хранилище: пары (вид клипа, произносимый текст)."""
    cfg = LANGUAGES[lang]
    async with AsyncSessionLocal() as s:
        rows = (await s.execute(text(f"""
            SELECT w.{cfg.word_attr}    AS word,
                   w.{cfg.example_attr} AS example,
                   w.article
            FROM words w
            JOIN word_lang_groups g
              ON g.word_id = w.id AND g.lang = :lang AND g.is_canonical
            WHERE w.{cfg.word_attr} IS NOT NULL
              AND btrim(w.{cfg.word_attr}) <> ''
        """), {"lang": lang})).mappings().all()

    seen: set[tuple[str, str]] = set()
    for row in rows:
        word = (row["word"] or "").strip()
        if cfg.uses_article:
            article = (row["article"] or "").strip()
            if article and article != "-":
                word = f"{article} {word}"
        for kind, spoken in (
            (KIND_WORD, word_clip_text(word, lang)),
            (KIND_FULL, full_clip_text(word, row["example"], lang)),
        ):
            if spoken:
                seen.add((kind, spoken))
    return sorted(seen)


def audit_language(lang: str, voice: str, clips: list[tuple[str, str]],
                   show: int, delete_broken: bool) -> dict:
    """
    Пройти по клипам языка и собрать отклонения.

    Ожидаемая длительность калибруется по самим клипам этого языка и голоса:
    темп зависит от языка, и заранее заданное число было бы гаданием.
    """
    measured: list[tuple[str, str, float, int]] = []
    missing: list[tuple[str, str]] = []
    empty: list[tuple[str, str, int]] = []
    unreadable: list[tuple[str, str]] = []

    for kind, spoken in clips:
        data = audio_store.read(lang, voice, kind, spoken)
        if data is None:
            path = audio_store.clip_path(lang, voice, kind, spoken)
            if path.exists():
                empty.append((kind, spoken, path.stat().st_size))
            else:
                missing.append((kind, spoken))
            continue

        duration = mp3_duration(data)
        if duration is None or duration <= 0:
            unreadable.append((kind, spoken))
            continue
        measured.append((kind, spoken, duration, len(data)))

    # Темп по срединному значению: он устойчив к выбросам, а выбросы —
    # это ровно то, что мы ищем
    long_enough = [(d, len(s)) for _, s, d, _ in measured
                   if len(s) >= MIN_CHARS_FOR_DURATION]
    if long_enough:
        per_char = statistics.median(d / n for d, n in long_enough)
    else:
        per_char = 0.06

    too_short: list[tuple[str, str, float, float]] = []
    too_long: list[tuple[str, str, float, float]] = []

    for kind, spoken, duration, size in measured:
        if len(spoken) < MIN_CHARS_FOR_DURATION:
            continue
        expected = len(spoken) * per_char
        if duration < expected * TOLERANCE_LOW:
            too_short.append((kind, spoken, duration, expected))
        elif duration > expected * TOLERANCE_HIGH:
            too_long.append((kind, spoken, duration, expected))

    broken = empty + [(k, s) for k, s in unreadable]
    if delete_broken:
        for kind, spoken, *_ in empty:
            audio_store.clip_path(lang, voice, kind, spoken).unlink(missing_ok=True)
        for kind, spoken in unreadable:
            audio_store.clip_path(lang, voice, kind, spoken).unlink(missing_ok=True)

    print(f"\n=== {lang} — ожидалось {len(clips)} клипов, голос {voice} ===")
    print(f"   прочитано:            {len(measured)}")
    print(f"   темп речи:            {per_char * 1000:.1f} мс на символ")
    print(f"   отсутствует:          {len(missing)}")
    print(f"   пустой или обрывок:   {len(empty)}")
    print(f"   не разбирается:       {len(unreadable)}")
    print(f"   короче ожидаемого:    {len(too_short)}")
    print(f"   длиннее ожидаемого:   {len(too_long)}")

    suspicious = len(missing) + len(empty) + len(unreadable) + len(too_short) + len(too_long)
    if measured:
        print(f"   → в норме {len(measured) - len(too_short) - len(too_long)} "
              f"из {len(clips)} "
              f"({(len(measured) - len(too_short) - len(too_long)) / len(clips) * 100:.2f}%)")

    for title, items in (("короче ожидаемого", too_short), ("длиннее ожидаемого", too_long)):
        for kind, spoken, duration, expected in items[:show]:
            print(f"      {title}: [{kind}] {duration:.1f} с вместо {expected:.1f} — "
                  f"{spoken[:60]!r}")
    for kind, spoken in missing[:show]:
        print(f"      отсутствует: [{kind}] {spoken[:60]!r}")
    for kind, spoken, size in empty[:show]:
        print(f"      обрывок {size} Б: [{kind}] {spoken[:60]!r}")

    return {
        "expected": len(clips), "measured": len(measured),
        "missing": len(missing), "empty": len(empty),
        "unreadable": len(unreadable),
        "too_short": len(too_short), "too_long": len(too_long),
        "suspicious": suspicious, "deleted": len(broken) if delete_broken else 0,
    }


async def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lang", choices=list(SUPPORTED_LANGS))
    ap.add_argument("--voice", help="голос (по умолчанию основной для языка)")
    ap.add_argument("--show", type=int, default=5,
                    help="сколько отклонений печатать по каждому виду")
    ap.add_argument("--delete-broken", action="store_true",
                    help="удалить пустые и неразбираемые клипы — они пересоздадутся")
    args = ap.parse_args()

    langs = [args.lang] if args.lang else [c for c in ORDER if c in SUPPORTED_LANGS]
    total: dict[str, int] = {}

    for lang in langs:
        clips = await expected_clips(lang)
        if not clips:
            print(f"\n=== {lang}: слов нет (колонка не заполнена) ===")
            continue
        voice = args.voice or default_voice(lang)
        result = audit_language(lang, voice, clips, args.show, args.delete_broken)
        for key, value in result.items():
            total[key] = total.get(key, 0) + value

    if len(langs) > 1 and total:
        good = total["measured"] - total["too_short"] - total["too_long"]
        print("\n=== ИТОГО ===")
        print(f"   ожидалось клипов:  {total['expected']}")
        print(f"   прочитано:         {total['measured']}")
        print(f"   подозрительных:    {total['suspicious']}")
        print(f"   в норме:           {good} "
              f"({good / total['expected'] * 100:.2f}%)")
        if total.get("deleted"):
            print(f"   удалено негодных:  {total['deleted']} — пересоздадутся")

    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
