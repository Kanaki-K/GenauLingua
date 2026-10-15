#!/usr/bin/env python3
"""
Сленг в переводах и примерах — патч 2.1.

Отзыв 15.10: «убрать сленг типа бабки». Сленг стоит там, где разговорное
и само немецкое слово (Klamotten, Knete, futtern) — перевод по смыслу
точный, но первое значение видно на карточке, и сленговое звучит грубо.

ПРАВИЛО: первое значение — нейтральное; разговорное остаётся вторым с
пометкой «(разг.)» / «(груб.)» — такие слова звучат в жизни, и знать их
полезно; в примерах — нейтральная речь. Ложные совпадения поиска не
трогались: «стачка» (забастовка), «приколачивать», «тачка» у Karre — это
буквальное значение (тележка).

    python -m app.scripts.word_fixes_2026_10_slang            # показать
    python -m app.scripts.word_fixes_2026_10_slang --apply    # записать
После записи: rebuild_word_groups, fill_word_frequency, fill_word_levels.
Повторный запуск ничего не меняет.
"""
from __future__ import annotations

import argparse
import asyncio
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
os.environ.setdefault("ENV_FILE", ".env.local")

from sqlalchemy import select  # noqa: E402

from app.database.models import Word  # noqa: E402
from app.database.session import AsyncSessionLocal, engine  # noqa: E402

# Номер ряда → (слово для сверки, поля). Номер — потому что слова-дубли
# (fressen, Typ) встречаются в базе не раз; слово сверяется, чтобы не
# поправить чужой ряд на другой базе
FIXES: dict[int, tuple[str, dict[str, str]]] = {
    485: ("Klamotten", {
        "translation_ru": "одежда, вещи, шмотки (разг.)",
        "example_ru": "Я убираю свою одежду",
        "translation_uk": "одяг, речі, шмотки (розм.)",
        "example_uk": "Я прибираю свій одяг",
    }),
    7165: ("beschissen", {
        "translation_ru": "паршивый, отвратительный (груб.)",
        "translation_uk": "паршивий, жахливий (груб.)",
    }),
    9828: ("Knete", {
        "translation_ru": "деньги (разг.), пластилин",
        "translation_uk": "гроші (розм.), пластилін",
        "translation_pl": "pieniądze (pot.), plastelina",
    }),
    10060: ("Mist", {
        "translation_en": "rubbish, manure, damn (interj.)",
        "example_en": "Oh no, I'm late",
    }),
    10128: ("irre", {
        "translation_ru": "безумный, сумасшедший, потрясающий",
    }),
    11656: ("fressen", {
        "translation_ru": "есть (о животных), пожирать",
        "translation_uk": "їсти (про тварин), пожирати",
        "translation_pl": "jeść (o zwierzętach), pożerać",
        "example_pl": "Kot znowu chce jeść",
    }),
    11833: ("auffressen", {
        "translation_ru": "съесть всё до конца, пожирать",
        "translation_uk": "з'їсти все, пожирати",
        "translation_pl": "zjeść wszystko, pożreć",
    }),
    11874: ("Knacker", {
        "translation_tr": "füme sosis, yaşlı adam (argo)",
    }),
    11892: ("futtern", {
        "translation_ru": "уплетать, наедаться, есть с аппетитом",
        "translation_uk": "наїдатися, уминати, їсти з апетитом",
        "translation_pl": "wcinać, opychać się, jeść z apetytem",
    }),
    12314: ("Gag", {
        "translation_ru": "шутка, гэг",
        "translation_uk": "жарт, ґеґ",
    }),
    14899: ("Typ", {
        "translation_ru": "парень, тип, человек",
        "translation_uk": "хлопець, тип, людина",
    }),
    15303: ("Landsmann", {
        "translation_pl": "rodak, krajan",
    }),
    17128: ("Karre", {
        "translation_ru": "тележка, тачка, развалюха (разг. о машине)",
    }),
}


async def main(apply: bool) -> int:
    changed = skipped = 0
    async with AsyncSessionLocal() as session:
        for word_id, (word_de, fields) in FIXES.items():
            word = await session.get(Word, word_id)
            if word is None or word.word_de != word_de:
                print(f"! {word_id} {word_de}: ряд не тот — пропущено")
                skipped += 1
                continue
            for field, value in fields.items():
                old = getattr(word, field)
                if old == value:
                    continue
                print(f"  {word_de}.{field}: {old!r} → {value!r}")
                setattr(word, field, value)
                changed += 1
        if apply:
            await session.commit()
    await engine.dispose()
    print(f"\nполей {'изменено' if apply else 'к изменению'}: {changed}, пропущено рядов: {skipped}")
    return 1 if skipped else 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    sys.exit(asyncio.run(main(ap.parse_args().apply)))
