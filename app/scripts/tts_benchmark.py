# -*- coding: utf-8 -*-
"""
Замер: сколько реально займёт озвучка всей базы.

Считаем объём работы по базе и измеряем пропускную способность edge-tts
на настоящих словах — чтобы оценка времени была из замера, а не на глаз.
"""
import asyncio
import os
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
os.environ.setdefault("ENV_FILE", ".env.local")

import edge_tts
from sqlalchemy import text

from app.database.session import AsyncSessionLocal
from app.services.language_service import LANGUAGES, SUPPORTED_LANGS

VOICES = {
    "de": "de-DE-KatjaNeural",
    "en": "en-GB-SoniaNeural",
    "ru": "ru-RU-SvetlanaNeural",
    "uk": "uk-UA-PolinaNeural",
    "tr": "tr-TR-EmelNeural",
}


async def volume():
    """Сколько клипов нужно: канонические слова и сколько из них с примером."""
    rows = {}
    async with AsyncSessionLocal() as s:
        for lang in SUPPORTED_LANGS:
            cfg = LANGUAGES[lang]
            q = text(f"""
                SELECT
                    COUNT(*) AS words,
                    COUNT(*) FILTER (
                        WHERE {cfg.example_attr} IS NOT NULL
                          AND btrim({cfg.example_attr}) <> ''
                    ) AS with_example
                FROM words w
                JOIN word_lang_groups g
                  ON g.word_id = w.id AND g.lang = :lang AND g.is_canonical
                WHERE w.{cfg.word_attr} IS NOT NULL
                  AND btrim(w.{cfg.word_attr}) <> ''
            """)
            r = (await s.execute(q, {"lang": lang})).mappings().one()
            rows[lang] = dict(r)
    return rows


async def sample_texts(lang: str, limit: int):
    cfg = LANGUAGES[lang]
    async with AsyncSessionLocal() as s:
        q = text(f"""
            SELECT w.{cfg.word_attr} AS word, w.{cfg.example_attr} AS example
            FROM words w
            JOIN word_lang_groups g
              ON g.word_id = w.id AND g.lang = :lang AND g.is_canonical
            WHERE w.{cfg.word_attr} IS NOT NULL AND btrim(w.{cfg.word_attr}) <> ''
              AND w.{cfg.example_attr} IS NOT NULL AND btrim(w.{cfg.example_attr}) <> ''
            ORDER BY w.frequency_rank NULLS LAST
            LIMIT :limit
        """)
        return [(r["word"], r["example"]) for r in
                (await s.execute(q, {"lang": lang, "limit": limit})).mappings()]


async def synth(payload: str, voice: str, out: pathlib.Path) -> int:
    """Один клип. Возвращает размер в байтах, 0 при ошибке."""
    try:
        data = b""
        comm = edge_tts.Communicate(payload, voice, rate="-10%")
        async for chunk in comm.stream():
            if chunk["type"] == "audio":
                data += chunk["data"]
        out.write_bytes(data)
        return len(data)
    except Exception as exc:
        print(f"      ошибка на {payload[:30]!r}: {type(exc).__name__}: {exc}")
        return 0


async def benchmark(lang: str, n: int, concurrency: int):
    """n клипов «слово + пример» с заданной параллельностью."""
    pairs = await sample_texts(lang, n)
    if len(pairs) < n:
        print(f"   мало данных для {lang}: {len(pairs)}")
        n = len(pairs)
    tmp = pathlib.Path("tts_samples/_bench")
    tmp.mkdir(parents=True, exist_ok=True)

    sem = asyncio.Semaphore(concurrency)
    sizes: list[int] = []

    async def one(i, word, example):
        async with sem:
            size = await synth(f"{word} … {example}", VOICES[lang],
                              tmp / f"{lang}_{i}.mp3")
            sizes.append(size)

    started = time.monotonic()
    await asyncio.gather(*(one(i, w, e) for i, (w, e) in enumerate(pairs)))
    elapsed = time.monotonic() - started

    ok = [s for s in sizes if s > 0]
    failed = len(sizes) - len(ok)
    rate = len(ok) / elapsed if elapsed else 0
    avg_kb = (sum(ok) / len(ok) / 1024) if ok else 0

    for f in tmp.iterdir():
        f.unlink()
    tmp.rmdir()

    return {"n": n, "ok": len(ok), "failed": failed, "elapsed": elapsed,
            "rate": rate, "avg_kb": avg_kb, "concurrency": concurrency}


def human(seconds: float) -> str:
    if seconds < 90:
        return f"{seconds:.0f} с"
    if seconds < 5400:
        return f"{seconds / 60:.0f} мин"
    return f"{seconds / 3600:.1f} ч"


async def main():
    print("=== Объём работы ===")
    vol = await volume()
    total_words = total_examples = 0
    for lang, v in vol.items():
        total_words += v["words"]
        total_examples += v["with_example"]
        share = v["with_example"] / v["words"] * 100 if v["words"] else 0
        print(f"  {lang}: канонических слов {v['words']:>6}, "
              f"с примером {v['with_example']:>6} ({share:.1f}%)")
    print(f"  ИТОГО слов {total_words}, из них с примером {total_examples}")
    clips = total_words + total_examples   # «слово» + «слово и пример»
    print(f"  Клипов к генерации: {clips} "
          f"({total_words} только слово + {total_examples} слово с примером)")

    print("\n=== Пропускная способность edge-tts ===")
    results = []
    for concurrency in (4, 8, 16):
        r = await benchmark("de", 32, concurrency)
        results.append(r)
        print(f"  параллельность {concurrency:>2}: "
              f"{r['ok']}/{r['n']} за {r['elapsed']:.1f} с → "
              f"{r['rate']:.1f} клип/с, средний клип {r['avg_kb']:.0f} КБ"
              + (f", ОШИБОК {r['failed']}" if r["failed"] else ""))

    best = max(results, key=lambda r: r["rate"])
    print(f"\n=== Прогноз при {best['concurrency']} потоках "
          f"({best['rate']:.1f} клип/с) ===")
    print(f"  Вся база, {clips} клипов: {human(clips / best['rate'])}")
    print(f"  Только немецкий A1–A2 (оценочно 2600 слов → 5200 клипов): "
          f"{human(5200 / best['rate'])}")

    mb = clips * best["avg_kb"] / 1024
    print(f"\n  Если хранить файлы на сервере: ~{mb / 1024:.1f} ГБ")
    print(f"  Если хранить только file_id в базе: ~{clips * 100 / 1024 / 1024:.1f} МБ")


asyncio.run(main())
