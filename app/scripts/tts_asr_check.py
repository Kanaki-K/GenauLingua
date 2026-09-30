# -*- coding: utf-8 -*-
"""
Замкнутая проверка озвучки: распознать сгенерированное и сверить с текстом.

Зачем. Утверждать «озвучка верная», не послушав 12 746 файлов, нельзя.
Но проверку можно замкнуть машинно: синтезировать клип, прогнать через
распознавание речи и сравнить расшифровку с исходным текстом. Расхождение —
подозрительный клип, который идёт на разбор.

Это даёт измеренную цифру вместо обещания: «проверено 12 746, расхождений 37».

ПРОВЕРЯЮТСЯ КЛИПЫ С ПРИМЕРОМ, а не изолированные слова. Это выяснилось
замером: на 24 словах все 24 клипа с примером совпали, а из клипов с одним
словом 7 дали расхождение — и все семь оказались односложными служебными
словами: sie → «See», es → «S», zu → «So», der → «Dea». Синтез там верный,
просто распознаватель не может расшифровать один слог без контекста и
угадывает. Проверять по таким клипам означало бы отбраковывать годное.

Клип с примером содержит то же слово и синтезируется тем же движком из того
же текста, так что верный клип с примером подтверждает и слово. Короткие
изолированные слова помечаются «не проверяется» — это признанный предел
метода, а не скрытая ошибка.

ЧЕГО МЕТОД НЕ ЛОВИТ. Ударение: слово с неверным ударением распознаётся
правильно. И гетеронимы — для них есть отдельный механизм, клип с контекстом
в самом вопросе.

    python -m app.scripts.tts_asr_check --lang de --limit 200
    python -m app.scripts.tts_asr_check --lang de --all --workers 4
    python -m app.scripts.tts_asr_check --lang de --recheck-clean 300
"""
from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import pathlib
import re
import sys
import unicodedata

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
os.environ.setdefault("ENV_FILE", ".env.local")

from sqlalchemy import text

from app.database.session import AsyncSessionLocal
from app.services.audio_service import KIND_FULL, KIND_WORD, obtain_audio
from app.services.language_service import LANGUAGES, SUPPORTED_LANGS
from app.services.tts_text import expand_numbers, full_clip_text, word_clip_text
from app.services.tts_voices import default_voice

logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(message)s")
logging.getLogger("sqlalchemy.engine").setLevel(logging.ERROR)
logging.getLogger("faster_whisper").setLevel(logging.ERROR)
logger = logging.getLogger("asr")

# Модель распознавания. small — компромисс: tiny слишком часто ошибается сам
# и даёт ложные расхождения, medium втрое медленнее без выигрыша на коротких
# фразах. Прогон по немецким словам занимает порядка часа.
MODEL_SIZE = os.environ.get("ASR_MODEL", "small")

# Коды языков для распознавания совпадают с нашими
ASR_LANG = {"de": "de", "en": "en", "ru": "ru", "uk": "uk", "tr": "tr", "pl": "pl"}

_PUNCT = re.compile(r"[^\w\s]", re.UNICODE)
_WS = re.compile(r"\s+")


def normalize(s: str) -> str:
    """
    Сравнение по существу: без регистра, пунктуации и различий в записи.

    Распознавание ставит свою пунктуацию и капитализацию, и сравнивать
    посимвольно означало бы утонуть в шуме.
    """
    s = unicodedata.normalize("NFC", s or "").lower()
    s = _PUNCT.sub(" ", s)
    return _WS.sub(" ", s).strip()


def similarity(a: str, b: str, lang: str | None = None) -> float:
    """
    Доля совпадения — грубо, но для отбора хватает.

    Расшифровка приходит с цифрами: «Ich habe sechs Äpfel» распознаватель
    записывает как «Ich habe 6 Äpfel». Звук при этом верный, поэтому цифры
    в расшифровке разворачиваются теми же правилами, что и при синтезе, —
    иначе каждое число давало бы ложное расхождение.
    """
    from difflib import SequenceMatcher

    left, right = normalize(a), normalize(b)
    if lang:
        right = normalize(expand_numbers(right, lang))
    return SequenceMatcher(None, left, right).ratio()


# Частота, которую ждёт распознаватель
ASR_SAMPLE_RATE = 16000


def decode_mp3(data: bytes):
    """
    mp3 в массив для распознавателя.

    Декодируем сами, а не через faster-whisper: его decode_audio вызывает
    av.open с параметром metadata_errors, которого в av 19 больше нет, а
    ставить старый av под Python 3.13 нельзя — нет готовых сборок, а
    компиляция требует инструментов. Передать массив напрямую проще, чем
    удерживать совместимость версий.
    """
    import io

    import av
    import numpy as np
    from av.audio.resampler import AudioResampler

    resampler = AudioResampler(format="s16", layout="mono", rate=ASR_SAMPLE_RATE)
    chunks: list = []

    with av.open(io.BytesIO(data), mode="r") as container:
        for frame in container.decode(audio=0):
            for resampled in resampler.resample(frame):
                chunks.append(resampled.to_ndarray().reshape(-1))

    if not chunks:
        return np.zeros(0, dtype=np.float32)

    samples = np.concatenate(chunks).astype(np.float32)
    # Целые со знаком в диапазон [-1, 1], как ждёт модель
    return samples / 32768.0


class Recognizer:
    """Обёртка над faster-whisper: модель грузится один раз."""

    def __init__(self, model_size: str = MODEL_SIZE):
        from faster_whisper import WhisperModel

        # int8 на процессоре: втрое быстрее float32, разницы на коротких
        # фразах не даёт
        self.model = WhisperModel(model_size, device="cpu", compute_type="int8")

    def transcribe(self, data: bytes, lang: str) -> str:
        audio = decode_mp3(data)
        if audio.size == 0:
            return ""
        segments, _ = self.model.transcribe(
            audio, language=ASR_LANG.get(lang, lang), beam_size=1,
            vad_filter=False, condition_on_previous_text=False,
        )
        return " ".join(seg.text for seg in segments).strip()


async def load_words(lang: str, limit: int | None, ids: list[int] | None) -> list[dict]:
    cfg = LANGUAGES[lang]
    where = ["w.%s IS NOT NULL" % cfg.word_attr,
             "btrim(w.%s) <> ''" % cfg.word_attr]
    params: dict = {"lang": lang}
    if ids:
        where.append("w.id = ANY(:ids)")
        params["ids"] = ids

    sql = text(f"""
        SELECT w.id,
               w.{cfg.word_attr}    AS word,
               w.{cfg.example_attr} AS example,
               w.article,
               w.level::text        AS level
        FROM words w
        JOIN word_lang_groups g
          ON g.word_id = w.id AND g.lang = :lang AND g.is_canonical
        WHERE {' AND '.join(where)}
        ORDER BY w.frequency_rank NULLS LAST, w.id
        {f'LIMIT {int(limit)}' if limit else ''}
    """)
    async with AsyncSessionLocal() as s:
        return [dict(r) for r in (await s.execute(sql, params)).mappings()]


def spoken_text_for(row: dict, lang: str, kind: str) -> str:
    cfg = LANGUAGES[lang]
    word = (row["word"] or "").strip()
    if cfg.uses_article:
        article = (row.get("article") or "").strip()
        if article and article != "-":
            word = f"{article} {word}"
    if kind == KIND_FULL:
        return full_clip_text(word, row.get("example"), lang)
    return word_clip_text(word, lang)


# Короче этого изолированное слово распознаванием не проверяется: модели
# не за что зацепиться, и она выдаёт похожее по звуку слово другого языка.
#
# Порог поднят с 5 до 9 по второму замеру: на пяти символах расхождения всё
# ещё давали годные клипы — immer → «demo», sehen → «See you in»,
# einer → «Aina». Проверка изолированных слов вообще вспомогательная, основа
# проверки — клипы с примером.
MIN_CHARS_FOR_ASR = 9


async def check_one(row: dict, lang: str, kind: str, voice: str,
                    recognizer: Recognizer, threshold: float) -> dict:
    spoken = spoken_text_for(row, lang, kind)
    result = {"id": row["id"], "level": row["level"], "kind": kind,
              "spoken": spoken, "heard": None, "ratio": None, "verdict": None}

    if not spoken:
        result["verdict"] = "пусто"
        return result

    # Признанный предел метода, а не скрытая ошибка: клип с примером для
    # этого же слова проверяется полноценно и подтверждает синтез
    if kind == KIND_WORD and len(normalize(spoken)) < MIN_CHARS_FOR_ASR:
        result["verdict"] = "не проверяется"
        return result

    # С диска, если клип там уже есть: после прогона синтеза проверка
    # становится чисто вычислительной и идёт заметно быстрее
    data = await obtain_audio(spoken, lang, kind, voice)
    if data is None:
        result["verdict"] = "синтез не удался"
        return result

    # Распознавание блокирующее, поэтому в отдельном потоке: иначе синтез
    # остальных клипов встал бы в очередь за ним
    try:
        heard = await asyncio.get_running_loop().run_in_executor(
            None, recognizer.transcribe, data, lang
        )
    except Exception as exc:
        result["verdict"] = "распознавание не удалось"
        result["heard"] = f"{type(exc).__name__}: {exc}"
        return result

    ratio = similarity(spoken, heard, lang)
    result["heard"] = heard
    result["ratio"] = round(ratio, 3)
    result["verdict"] = "совпало" if ratio >= threshold else "расхождение"
    return result


async def run(args) -> int:
    lang = args.lang
    voice = args.voice or default_voice(lang)
    # Клип с примером — то, что проверяется по существу. Изолированное
    # слово добавляется по флагу и в основном ради длинных слов.
    kinds = [KIND_FULL, KIND_WORD] if args.words_too else [KIND_FULL]

    ids = None
    if args.recheck_clean:
        # Отдельный режим: перепроверить то, что признано верным, — не
        # обманулся ли распознаватель. Берётся случайная выборка из
        # совпавших, потому что весь чистый массив переслушать нельзя.
        previous = pathlib.Path(args.out)
        if not previous.exists():
            print(f"нет {previous} — сначала обычный прогон")
            return 1
        clean = [
            json.loads(line)["id"]
            for line in previous.read_text(encoding="utf-8").splitlines()
            if line.strip() and json.loads(line)["verdict"] == "совпало"
        ]
        import random
        random.seed(args.seed)
        ids = random.sample(clean, min(args.recheck_clean, len(clean)))
        print(f"перепроверка {len(ids)} из {len(clean)} признанных верными")

    words = await load_words(lang, None if (args.all or ids) else args.limit, ids)
    if not words:
        print("слов не найдено")
        return 1

    total_clips = len(words) * len(kinds)
    print(f"язык {lang}, голос {voice}, модель {MODEL_SIZE}")
    print(f"слов {len(words)}, клипов к проверке {total_clips}, "
          f"потоков {args.workers}, порог совпадения {args.threshold}")
    print()

    recognizer = Recognizer()
    out_path = pathlib.Path(args.out if not ids else args.out + ".recheck")
    # Возобновление: уже проверенное не переделываем
    done: set[tuple[int, str]] = set()
    if out_path.exists() and not ids:
        for line in out_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                done.add((r["id"], r["kind"]))
        if done:
            print(f"в {out_path} уже есть {len(done)} проверок — пропускаю их")

    sem = asyncio.Semaphore(args.workers)
    stats = {"совпало": 0, "расхождение": 0, "не проверяется": 0,
             "синтез не удался": 0, "распознавание не удалось": 0, "пусто": 0}
    lock = asyncio.Lock()
    processed = 0

    async def one(row: dict, kind: str):
        nonlocal processed
        if (row["id"], kind) in done:
            return
        async with sem:
            res = await check_one(row, lang, kind, voice, recognizer, args.threshold)
        async with lock:
            processed += 1
            stats[res["verdict"]] = stats.get(res["verdict"], 0) + 1
            with out_path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(res, ensure_ascii=False) + "\n")
            if processed % 25 == 0 or res["verdict"] == "расхождение":
                mark = "!" if res["verdict"] == "расхождение" else " "
                print(f" {mark} {processed}/{total_clips - len(done)}  "
                      f"совпало {stats['совпало']}, расхождений {stats['расхождение']}"
                      + (f"   {res['spoken']!r} → {res['heard']!r}"
                         if res["verdict"] == "расхождение" else ""))

    await asyncio.gather(*(one(row, kind) for row in words for kind in kinds))

    checked = sum(stats.values())
    print()
    print("=== ИТОГ ===")
    for name, count in stats.items():
        if count:
            share = count / checked * 100 if checked else 0
            print(f"  {name:<20} {count:>6}  ({share:.2f}%)")
    if checked:
        clean_share = stats["совпало"] / checked * 100
        print(f"\n  озвучка подтверждена распознаванием: {clean_share:.2f}%")
    print(f"  подробности: {out_path}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lang", default="de", choices=list(SUPPORTED_LANGS))
    ap.add_argument("--limit", type=int, default=100)
    ap.add_argument("--all", action="store_true", help="вся база этого языка")
    ap.add_argument("--words-too", action="store_true",
                    help="проверять и клипы с одним словом (короткие всё равно "
                         "не проверяются — распознаватель их не разбирает)")
    ap.add_argument("--voice", help="голос (по умолчанию основной для языка)")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--threshold", type=float, default=0.75,
                    help="ниже этой доли совпадения клип считается подозрительным")
    ap.add_argument("--out", default="asr_check.jsonl")
    ap.add_argument("--recheck-clean", type=int, metavar="N",
                    help="перепроверить N случайных из признанных верными")
    ap.add_argument("--seed", type=int, default=20260930)
    return asyncio.run(run(ap.parse_args()))


if __name__ == "__main__":
    # Под защитой, чтобы similarity и normalize можно было импортировать
    # в тесты, не запуская прогон
    sys.exit(main())
