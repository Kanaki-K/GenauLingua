# -*- coding: utf-8 -*-
"""
Обрезать тишину во всех клипах хранилища.

Движок добавляет вокруг речи около полутора секунд тишины: у слова «zum» речь
занимает 0,39 секунды из 1,87. На викторине из 25 вопросов это полминуты
мёртвого воздуха, и на слух заметно сразу.

Обрезка идёт по кадрам mp3, без перекодирования — звук не теряет качества.
Внутренняя пауза между словом и примером не трогается: она задана намеренно.

ПОРЯДОК РАБОТЫ. Сначала проверка на выборке (--verify), потом сама обрезка.
Проверка сверяет, что распознавание обрезанного клипа даёт тот же текст: если
срез задел речь, распознавание это увидит.

    python -m app.scripts.tts_trim_store --verify 200
    python -m app.scripts.tts_trim_store --lang de
    python -m app.scripts.tts_trim_store            # все языки

После обрезки кэш file_id становится недействительным: в Telegram лежат
необрезанные клипы, а в хранилище обрезанные. Скрипт чистит word_audio сам —
клипы загрузятся заново при показе.
"""
from __future__ import annotations

import argparse
import asyncio
import os
import pathlib
import random
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
os.environ.setdefault("ENV_FILE", ".env.local")

from sqlalchemy import text

from app.database.session import AsyncSessionLocal
from app.services import audio_store, mp3_trim
from app.services.language_service import SUPPORTED_LANGS
from app.services.tts_voices import default_voice

ORDER = ("de", "en", "uk", "ru", "tr", "pl")

# Ниже этого совпадения распознавания до и после считаем, что срез задел речь
VERIFY_THRESHOLD = 0.75


def clips_of(lang: str, voice: str) -> list[pathlib.Path]:
    root = audio_store.DEFAULT_ROOT / lang / voice
    return sorted(root.rglob("*.mp3")) if root.exists() else []


def trim_file(path: pathlib.Path, decode) -> tuple[bool, int, int]:
    """
    Обрезать один файл на месте. Возвращает (обрезан, было байт, стало байт).

    Запись через временный файл с переименованием: прерывание иначе оставило бы
    половину файла на месте целого.
    """
    try:
        data = path.read_bytes()
    except OSError:
        return False, 0, 0

    out = mp3_trim.trim(data, decode)
    if out is None or len(out) >= len(data):
        return False, len(data), len(data)

    try:
        temporary = path.with_suffix(".trim")
        temporary.write_bytes(out)
        temporary.replace(path)
    except OSError:
        return False, len(data), len(data)

    return True, len(data), len(out)


def verify_sample(langs: list[str], count: int, decode) -> bool:
    """
    Проверить на выборке, что обрезка не задевает речь.

    Сверяем распознавание до и после: если срез отрезал начало слова, текст
    изменится, и это видно сразу. Проверка на выборке, а не на всём массиве,
    потому что распознавание дорогое — но выборка случайная и по всем языкам.
    """
    from app.scripts.tts_asr_check import Recognizer, similarity

    print(f"проверка на {count} случайных клипах по языкам {' '.join(langs)}")
    recognizer = Recognizer()
    rng = random.Random(20260930)

    pool: list[tuple[str, pathlib.Path]] = []
    for lang in langs:
        for path in clips_of(lang, default_voice(lang)):
            pool.append((lang, path))
    if not pool:
        print("в хранилище нет клипов")
        return False

    sample = rng.sample(pool, min(count, len(pool)))
    damaged: list[tuple[str, str, str, float]] = []
    skipped = 0
    checked = 0

    for lang, path in sample:
        data = path.read_bytes()
        out = mp3_trim.trim(data, decode)
        if out is None:
            skipped += 1
            continue
        before = recognizer.transcribe(data, lang)
        after = recognizer.transcribe(out, lang)
        score = similarity(before, after, lang)
        checked += 1
        if score < VERIFY_THRESHOLD:
            damaged.append((lang, before, after, score))

    print(f"  проверено {checked}, обрезать нечего у {skipped}")
    print(f"  расхождений распознавания: {len(damaged)}")
    for lang, before, after, score in damaged[:12]:
        print(f"    {lang} {score:.2f}: {before[:40]!r} → {after[:40]!r}")

    if damaged:
        share = len(damaged) / checked * 100 if checked else 0
        print(f"\n  {share:.1f}% клипов изменили распознавание. Если это единицы —")
        print("  обычно распознаватель сам шумит на коротких словах; если больше")
        print("  нескольких процентов, обрезка задевает речь и запас надо увеличить.")
        return share < 3.0

    print("\n  обрезка речь не задевает")
    return True


async def clear_file_id_cache(langs: list[str]) -> int:
    """
    Кэш file_id после обрезки недействителен.

    В Telegram лежат необрезанные клипы, а в хранилище обрезанные. Оставить
    старые file_id значило бы навсегда отдавать людям то, что мы только что
    исправили. Записи удаляются, клипы загрузятся заново при показе.
    """
    async with AsyncSessionLocal() as s:
        result = await s.execute(
            text("DELETE FROM word_audio WHERE lang = ANY(:langs)"),
            {"langs": langs},
        )
        await s.commit()
        return result.rowcount or 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lang", choices=list(SUPPORTED_LANGS))
    ap.add_argument("--verify", type=int, metavar="N",
                    help="только проверить на N случайных клипах, ничего не менять")
    ap.add_argument("--keep-cache", action="store_true",
                    help="не чистить кэш file_id (по умолчанию чистится)")
    args = ap.parse_args()

    from app.scripts.tts_asr_check import decode_mp3

    langs = [args.lang] if args.lang else [
        c for c in ORDER if (audio_store.DEFAULT_ROOT / c).exists()
    ]
    if not langs:
        print("в хранилище нет клипов")
        return 1

    if args.verify:
        return 0 if verify_sample(langs, args.verify, decode_mp3) else 1

    started = time.monotonic()
    grand_trimmed = grand_total = 0
    grand_before = grand_after = 0

    for lang in langs:
        voice = default_voice(lang)
        paths = clips_of(lang, voice)
        if not paths:
            print(f"  {lang}: клипов нет")
            continue

        trimmed = before_bytes = after_bytes = 0
        for index, path in enumerate(paths, 1):
            ok, size_before, size_after = trim_file(path, decode_mp3)
            before_bytes += size_before
            after_bytes += size_after
            trimmed += 1 if ok else 0
            if index % 2000 == 0:
                print(f"     {index}/{len(paths)} обработано, обрезано {trimmed}")

        saved = before_bytes - after_bytes
        print(f"  {lang}: обрезано {trimmed} из {len(paths)}, "
              f"{before_bytes / 1024 / 1024:.0f} → {after_bytes / 1024 / 1024:.0f} МБ "
              f"(−{saved / before_bytes * 100:.0f}%)" if before_bytes else f"  {lang}: —")

        grand_trimmed += trimmed
        grand_total += len(paths)
        grand_before += before_bytes
        grand_after += after_bytes

    elapsed = time.monotonic() - started
    print()
    print("=== ИТОГО ===")
    print(f"  обрезано {grand_trimmed} из {grand_total} клипов за {elapsed / 60:.1f} мин")
    if grand_before:
        print(f"  объём: {grand_before / 1024 / 1024 / 1024:.2f} → "
              f"{grand_after / 1024 / 1024 / 1024:.2f} ГБ "
              f"(−{(grand_before - grand_after) / grand_before * 100:.0f}%)")

    if not args.keep_cache:
        removed = asyncio.run(clear_file_id_cache(langs))
        print(f"  кэш file_id очищен: {removed} записей — клипы загрузятся заново")

    return 0


if __name__ == "__main__":
    sys.exit(main())
