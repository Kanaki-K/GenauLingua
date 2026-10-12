# -*- coding: utf-8 -*-
"""
ПРИЁМКА ОЗВУЧКИ ПО КАЖДОМУ ГОЛОСУ, А НЕ ТОЛЬКО ПО ОСНОВНОМУ.

    python -m app.scripts.verify_voices

ЗАЧЕМ ОТДЕЛЬНО ОТ `state_report`. Тот отвечает «не хватает 0» — и это
правда, но правда только про ОДИН голос: внутри стоит `default_voice(lang)`,
то есть женский. Про мужские голоса он не говорит ничего и сказать не
может.

Это сделалось ловушкой 12 октября. Мужские голоса досинтезировались весь
день, и полноту их я проверил... счётом файлов mp3 в каталогах — сравнил
мужской каталог с женским и доложил владельцу о недостаче в семь клипов.
Недостачи не было: разница оказалась сиротами от правки примеров. Счёт
файлов не умеет ответить на вопрос «хватает ли», потому что не знает ни
про каноничность, ни про то, какие тексты вообще нужно произносить.

Отвечать на этот вопрос умеет только обход тех же данных, по которым клип
ищет сам бот, — и он здесь, по каждому голосу порознь.

Скрипт ТОЛЬКО ЧИТАЕТ.
"""
from __future__ import annotations

import argparse
import asyncio
import collections
import logging
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
os.environ.setdefault("ENV_FILE", ".env.local")

logging.disable(logging.INFO)

from sqlalchemy import text  # noqa: E402

from app.database.models import Word  # noqa: E402
from app.database.session import AsyncSessionLocal  # noqa: E402
from app.services import audio_store  # noqa: E402
from app.services.audio_service import (  # noqa: E402
    KIND_FULL, KIND_WORD, spoken_for,
)
from app.services.language_service import SUPPORTED_LANGS  # noqa: E402
from app.services.tts_voices import voices_for  # noqa: E402

CANONICAL_SQL = text("""
    SELECT w.id FROM words w
    JOIN word_lang_groups g
      ON g.word_id = w.id AND g.lang = :lang AND g.is_canonical
    ORDER BY w.id
""")


# Какую долю базы должен покрывать голос, чтобы счесть его используемым.
# Половина — с большим запасом в обе стороны: озвученные голоса покрывают
# 100%, случайные пробы — доли процента, и промежутка между ними нет.
USED_VOICE_SHARE = 0.5


async def run(only_lang: str | None) -> int:
    langs = [only_lang] if only_lang else list(SUPPORTED_LANGS)
    rows: list[tuple[str, str, str, int, int]] = []
    unused: list[tuple[str, str, int]] = []
    failures = 0
    checked = 0

    async with AsyncSessionLocal() as session:
        for lang in langs:
            ids = (await session.execute(CANONICAL_SQL, {"lang": lang})).scalars().all()

            # Произносимые тексты собираются ОДИН раз на язык: они одни и те
            # же для всех голосов, а обход базы дорог
            wanted: set[tuple[str, str]] = set()
            for word_id in ids:
                word = await session.get(Word, word_id)
                for kind in (KIND_WORD, KIND_FULL):
                    spoken = spoken_for(word, lang, kind)
                    if spoken:
                        wanted.add((kind, spoken))

            for voice in voices_for(lang):
                present = sum(
                    1 for kind, spoken in wanted
                    if audio_store.read(lang, voice.name, kind, spoken) is not None
                )

                # ГОЛОС СЧИТАЕТСЯ ИСПОЛЬЗУЕМЫМ ПО ДОЛЕ, А НЕ ПО НАЛИЧИЮ.
                #
                # Первая редакция отсекала по «ни одного клипа» — и назвала
                # недостачей `de-DE-SeraphinaMultilingualNeural`: 24 699 из
                # 24 714 «не хватает» у голоса, которым база не озвучивалась
                # никогда. Пятнадцать клипов у него есть (кто-то когда-то
                # попробовал), и этого хватило, чтобы сойти за используемый.
                #
                # Доля различает честно: озвученный голос покрывает базу
                # целиком или почти, случайные пробы — единицы процента.
                share = present / len(wanted) if wanted else 0
                if share < USED_VOICE_SHARE:
                    unused.append((lang, voice.name, present))
                    continue

                missing = len(wanted) - present
                checked += 1
                failures += 1 if missing else 0
                rows.append((lang, voice.name, voice.gender, len(wanted), missing))

    print(f"\n{'язык':<5}{'голос':<32}{'пол':<8}{'нужно':>8}{'не хватает':>12}")
    for lang, name, gender, need, missing in rows:
        mark = "" if not missing else "   <<<"
        print(f"{lang:<5}{name:<32}{gender:<8}{need:>8}{missing:>12}{mark}")

    by_gender = collections.Counter(g for _, _, g, _, _ in rows)
    print(f"\nголосов проверено: {checked} "
          f"({', '.join(f'{g} {n}' for g, n in sorted(by_gender.items()))})")

    # Неиспользуемые голоса печатаются, а не замалчиваются: молчание о том,
    # чего проверка НЕ смотрела, — главный способ соврать отчётом
    if unused:
        print(f"голосов движка не в работе: {len(unused)} "
              f"(" + ", ".join(f"{lang}/{name}: {n}" for lang, name, n in unused) + ")")

    if checked == 0:
        print("ПРОВЕРЯТЬ БЫЛО НЕЧЕГО — это неудача, а не успех")
        return 1
    if failures:
        print(f"\nГОЛОСОВ С НЕДОСТАЧЕЙ: {failures}")
        return 1

    print("\nозвучка полна по каждому использованному голосу")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", choices=list(SUPPORTED_LANGS),
                        help="проверить один язык")
    args = parser.parse_args()
    return asyncio.run(run(args.lang))


if __name__ == "__main__":
    raise SystemExit(main())
