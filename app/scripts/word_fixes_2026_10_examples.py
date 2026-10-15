#!/usr/bin/env python3
"""
Примеры, расходящиеся с немецким эталоном, — патч 2.1.

Разбор прода 15.10: польский новичок получил «mieć na myśli» с примером
«Co masz na myśli?» («Что ты имеешь в виду?») и переводом «Что ты об этом
думаешь?». Эталон — немецкий «Was meinst du dazu?» («Что ты об этом
думаешь?»): русский и украинский верны, английский, польский и турецкий
переведены как «что ты имеешь в виду».

Сверка выборки (16.10, 750 пар: по 150 слов A1–B1 на ru, uk, en, pl, tr
против немецкого примера) нашла ещё ~2% строк с изъяном: пропавшая или
лишняя деталь, изучаемого слова нет в примере, неуклюжая фраза. Здесь —
все найденные. Пример — ТОЧНЫЙ перевод немецкого, и в нём есть само слово.

    python -m app.scripts.word_fixes_2026_10_examples            # показать
    python -m app.scripts.word_fixes_2026_10_examples --apply    # записать
Повторный запуск ничего не меняет. Озвучка примеров переделается сама:
клип с прежним текстом считается устаревшим (`word_audio.spoken_text`).
"""
from __future__ import annotations

import argparse
import asyncio
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
os.environ.setdefault("ENV_FILE", ".env.local")

from app.database.models import Word  # noqa: E402
from app.database.session import AsyncSessionLocal, engine  # noqa: E402

# Номер ряда → (слово для сверки, поля): номер — потому что слова-дубли
# (meinen) встречаются не раз; слово сверяется, чтобы не поправить чужой ряд
FIXES: dict[int, tuple[str, dict[str, str]]] = {
    13300: ("meinen", {                      # «Was meinst du dazu?»
        "example_en": "What do you think about it?",
        "example_pl": "Co o tym sądzisz?",
        "example_tr": "Bu konuda ne düşünüyorsun?",
    }),
    # Польский
    2079: ("Vorsicht", {"example_pl": "Uwaga! Ten stopień jest wysoki"}),
    18690: ("andermal", {"example_pl": "Dziś nie mam czasu, może innym razem"}),
    7240: ("darstellen", {"example_pl": "Co ma przedstawiać ten obrazek?"}),
    # Турецкий
    15847: ("Hagel", {"example_tr": "Şiddetli dolu yağıyor"}),
    10356: ("locken", {"example_tr": "Teklif müşterileri cezbetmeli"}),
    13060: ("heiser", {"example_tr": "Münih'teki konserden sonra sesi kısıktı"}),
    2629: ("Kratzer", {"example_tr": "Arabaya bir çizik gelmiş"}),
    2236: ("ausstellen", {"example_tr": "Bir belge veriyorum"}),
    6330: ("fort", {"example_tr": "İki haftalığına gitti"}),
    14460: ("Instrumentalmusik", {"example_tr": "Rahatlamak için enstrümantal müzik dinlemeyi severim"}),
    # Русский
    8161: ("festgebunden", {"example_ru": "Посылка была крепко перевязана"}),
    359: ("Größe", {"example_ru": "Какой размер тебе нужен?"}),
    16346: ("beantragen", {"example_ru": "Я хочу подать заявление на паспорт"}),
    11994: ("Minibar", {"example_ru": "Мини-бар в номере отеля удобный, но дорогой"}),
    # Украинский
    1245: ("Beratungsgespräch", {"example_uk": "У нас консультація"}),
    2049: ("verrückt", {"example_uk": "Це ж божевільно"}),
    8444: ("unregelmäßig", {"example_uk": "Робочий час нерегулярний"}),
    # Английский
    6524: ("vorn", {"example_en": "I sit at the front of the bus"}),
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
