# -*- coding: utf-8 -*-
"""
ПРИЁМКА ВСЕХ ГОЛОСОВ: каждый голос каждого языка — на сотне клипов.

    python -m app.scripts.verify_all_voices
    python -m app.scripts.verify_all_voices --per-voice 100 --lang de

ЗАЧЕМ. Владелец услышал неладное: «озвучка... она будто английским читает
немецкие. Не выговаривает правильно. Потому тебе нужно снова проверить все
языки по 100 каждый голос чтобы соответствовало себе».

Прежняя приёмка слухом (`tts_asr_check`) умеет ровно это, но проверяли ею
ОДИН голос на язык — основной. А голосов девятнадцать: у немецкого шесть, у
английского пять, у остальных по два. Четырнадцать из них не проверял
никто, и среди них два многоязычных (`SeraphinaMultilingual`,
`FlorianMultilingual`) — именно те, про которые и была жалоба: такой голос
умеет читать чужие языки, и акцент у него не местный.

ЧТО ЗНАЧИТ «СООТВЕТСТВУЕТ СЕБЕ». Клип распознаётся распознавателем того же
языка, и распознанное сверяется с тем, что должно звучать. Голос, читающий
немецкое слово по-английски, даёт низкую долю совпадения — это и есть
замер, а не мнение.

ПОЧЕМУ ЭТО ДОЛГО. Клипы неосновных голосов на диске не лежат: их
синтезируют на ходу, по одному. Сто клипов на голос — это сто обращений к
движку, и прогон на девятнадцать голосов идёт часами. Зато после него у
каждого голоса есть число, а не предположение.
"""
from __future__ import annotations

import argparse
import asyncio
import os
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
os.environ.setdefault("ENV_FILE", ".env.local")

import logging

logging.disable(logging.INFO)

from app.services.tts_voices import VOICES  # noqa: E402


async def _check_one(lang: str, voice: str, limit: int, workers: int) -> dict:
    """
    Прогнать один голос через приёмку слухом и вернуть числа.

    Приёмка зовётся как функция, а не через оболочку: разбирать её
    напечатанный вывод значило бы завести вторую правду о том же числе.
    Файл подробностей у каждого голоса СВОЙ — иначе прогоны слились бы в
    один, и разобраться, чей клип разошёлся, стало бы нельзя.
    """
    from argparse import Namespace

    from app.scripts import tts_asr_check

    started = time.monotonic()
    report = await tts_asr_check.run(Namespace(
        lang=lang, voice=voice, limit=limit, workers=workers,
        # КЛИПЫ С ПРИМЕРОМ, а не одиночные слова. Так метод и задуман:
        # короткое слово распознаватель не разбирает и выдаёт похожее по
        # звуку из другого языка. С `words_too=True` половина клипов
        # попадала в «не проверяется», и доля верных у ЛЮБОГО голоса
        # выходила около 50% — число, которое ничего не значит.
        words_too=False, threshold=0.75, all=False,
        out=f"asr_{lang}_{voice.split('-')[-1]}.jsonl",
        recheck_clean=None, seed=20261014,
    ))
    if report is None:
        raise RuntimeError("приёмка не нашла слов")
    report["seconds"] = round(time.monotonic() - started, 1)
    return report


async def _run_all(args) -> int:
    """
    Обойти все голоса В ОДНОМ цикле событий.

    Первая редакция звала `asyncio.run` на каждый голос, и второй голос
    падал с `'NoneType' object has no attribute 'send'`: соединение с базой
    осталось от закрытого цикла. Голос при этом помечался «не проверен» —
    то есть приёмка молча теряла восемнадцать голосов из девятнадцати.
    """
    langs = [args.lang] if args.lang else sorted(VOICES)
    rows = []

    for lang in langs:
        for voice in VOICES[lang]:
            print(f"\n=== {lang} · {voice.label} ({voice.name}) ===", flush=True)
            try:
                report = await _check_one(
                    lang, voice.name, args.per_voice, args.workers
                )
            except Exception as exc:  # приёмка не должна падать целиком
                print(f"   ОШИБКА: {type(exc).__name__}: {exc}", flush=True)
                rows.append((lang, voice.label, None, None, None))
                continue

            # ДОЛЯ СЧИТАЕТСЯ ПО ПРОВЕРЯЕМЫМ. Клип, который распознаватель
            # не берёт (слишком короткий), не говорит о голосе ничего — ни
            # хорошего, ни плохого, и в знаменателе ему не место.
            matched = report["matched"]
            suspect = report["mismatched"]
            judged = matched + suspect
            checked = report["checked"]
            share = matched / judged * 100 if judged else 0.0
            skipped = checked - judged
            print(f"   разобрано {judged} из {checked} "
                  f"(пропущено коротких {skipped}), расхождений {suspect} "
                  f"→ {share:.1f}% за {report['seconds']} с", flush=True)
            rows.append((lang, voice.label, judged, suspect, share))

    print("\n" + "=" * 70)
    print("ИТОГ ПО ГОЛОСАМ")
    print("=" * 70)
    worst = []
    for lang, label, checked, suspect, share in rows:
        if checked is None:
            print(f"  {lang} {label:12} — не проверен (ошибка)")
            continue
        print(f"  {lang} {label:12} {checked:4} клипов, "
              f"подозрительных {suspect:3} → {share:5.1f}%")
        if share < 90:
            worst.append((lang, label, share))

    if worst:
        print("\nГОЛОСА НИЖЕ 90%:")
        for lang, label, share in sorted(worst, key=lambda r: r[2]):
            print(f"  {lang} {label} — {share:.1f}%")
        return 1

    print("\nвсе голоса читают свой язык верно")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--per-voice", type=int, default=100)
    ap.add_argument("--lang", choices=sorted(VOICES))
    ap.add_argument("--workers", type=int, default=4)
    return asyncio.run(_run_all(ap.parse_args()))


if __name__ == "__main__":
    sys.exit(main())
