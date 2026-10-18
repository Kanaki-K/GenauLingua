#!/usr/bin/env python3
"""
Правки слов по жалобам (апрель–июнь 2026), разобранные 15.10.2026.

Владелец: «возможно, пометка была о том, что не очень естественный бытовой
перевод». Девять жалоб на девять слов; правятся шесть — где перевод или
пример звучал книжно («От этого я могу тебя только отговаривать») или был
неверен («кто-то» для man — это jemand; «а также» для beziehungsweise).

Повторный запуск ничего не меняет: поле пишется, только если отличается.
По умолчанию — показать; `--apply` — записать. После записи пересобрать
группы: `python -m app.scripts.rebuild_word_groups`.

Звук перестраивается сам: клип в кэше сверяется с произносимым текстом.
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

FIXES: dict[str, dict[str, str]] = {
    "abraten": {
        "translation_ru": "не советовать, отговаривать, предостерегать",
        "translation_uk": "не радити, відраджувати, застерігати",
        "example_ru": "Я тебе этого очень не советую",
        "example_uk": "Я тобі цього дуже не раджу",
        "example_en": "I'd strongly advise you against it",
        "example_tr": "Bunu sana hiç tavsiye etmem",
    },
    "verdrängen": {
        "translation_ru": "вытеснять, гнать от себя (мысли), подавлять",
        "translation_uk": "витісняти, гнати від себе (думки), заглушувати",
        "example_ru": "Я гоню от себя это воспоминание",
        "example_uk": "Я жену від себе цей спогад",
        "example_en": "I push this memory away",
        "example_tr": "Bu anıyı aklımdan uzaklaştırıyorum",
    },
    "Zimmerlautstärke": {
        "translation_ru": "умеренная громкость, тихо (чтобы не мешать соседям)",
        "translation_uk": "помірна гучність, тихо (щоб не заважати сусідам)",
        "translation_en": "moderate volume, low volume (not disturbing the neighbours)",
        "example_ru": "Пожалуйста, потише, чтобы не мешать соседям",
        "example_uk": "Будь ласка, тихіше, щоб не заважати сусідам",
        "example_en": "Please keep the volume down",
        "example_tr": "Lütfen sesi kısık tutun",
        "example_pl": "Proszę ściszyć, żeby nie przeszkadzać sąsiadom",
    },
    "man": {
        "translation_ru": "люди, можно, все (безличное)",
        "translation_uk": "люди, можна, усі (безособове)",
        "translation_tr": "insan, kişi, genel olarak",
    },
    "Tempus": {
        "example_ru": "Это предложение в настоящем времени",
        "example_uk": "Це речення в теперішньому часі",
    },
    "beziehungsweise": {
        "translation_ru": "или, точнее, соответственно",
        "translation_uk": "або, точніше, відповідно",
        "example_de": "Ich rufe dich morgen an, beziehungsweise übermorgen",
        "example_ru": "Я позвоню тебе завтра, точнее, послезавтра",
        "example_uk": "Я подзвоню тобі завтра, точніше, післязавтра",
        "example_en": "I'll call you tomorrow, or rather the day after",
        "example_tr": "Seni yarın, daha doğrusu öbür gün ararım",
        "example_pl": "Zadzwonię do ciebie jutro, a właściwie pojutrze",
    },
}


async def main(apply: bool) -> int:
    changed = 0
    async with AsyncSessionLocal() as session:
        for word_de, fields in FIXES.items():
            rows = (await session.execute(
                select(Word).where(Word.word_de == word_de)
            )).scalars().all()
            if len(rows) != 1:
                print(f"! {word_de}: строк {len(rows)} — пропущено")
                continue
            word = rows[0]
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
    print(f"\nполей {'изменено' if apply else 'к изменению'}: {changed}")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    sys.exit(asyncio.run(main(ap.parse_args().apply)))
