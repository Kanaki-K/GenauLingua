# -*- coding: utf-8 -*-
"""
Предсинтез МУЖСКОГО голоса для всех шести языков.

    python -m app.scripts.tts_synthesize_male

ЗАЧЕМ. Предсинтезирован был только голос по умолчанию — в каждом языке
женский, 121 269 клипов. Выбор голоса в настройках при этом работает на
всех шести языках, но любой НЕ основной голос синтезируется на лету:
секунда ожидания на карточку, и примерно одна попытка из десяти срывается
на рукопожатии с движком (WSServerHandshakeError), то есть карточка иногда
приходит вовсе без звука.

Поймано тем, что владелец переключил польский на Marek и в логе бота
немедленно появились неудачи синтеза, которых до переключения не было ни
одной. Решение владельца: предсинтезировать мужской голос на всех шести —
он закрывает настоящий выбор «женский или мужской», а остальные голоса
(немецкий даёт 6, английский 5) остаются ленивыми.

ЦЕНА: около 121 271 клипа, +1.9 ГБ, порядка девяти часов при восьми
потоках (замерено: 223 клипа в минуту).

ПОЧЕМУ ВОСЕМЬ ПОТОКОВ, А НЕ ШЕСТНАДЦАТЬ. Движок недокументированный и
ограничивает частоту: на двадцати клипах в восемь потоков два сорвались
по рукопожатию. Больше потоков — больше отказов, а не больше скорости.
Сорвавшееся добирается повторным прогоном: скрипт синтеза не переделывает
уже существующее, поэтому его можно запускать сколько угодно раз.

ПРЕРЫВАТЬ МОЖНО В ЛЮБОЙ МОМЕНТ. Готовые клипы лежат файлами, и следующий
прогон начнёт с того, чего нет.
"""
from __future__ import annotations

import os
import pathlib
import subprocess
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
os.environ.setdefault("ENV_FILE", ".env.local")

from app.services.language_service import SUPPORTED_LANGS  # noqa: E402
from app.services.tts_voices import voices_for  # noqa: E402

WORKERS = 8
PASSES = 2  # второй проход добирает сорвавшееся по сети


def male_voice(lang: str) -> str | None:
    for v in voices_for(lang):
        if v.gender == "male":
            return v.name
    return None


def main() -> int:
    plan = [(lang, male_voice(lang)) for lang in SUPPORTED_LANGS]
    missing = [lang for lang, v in plan if not v]
    if missing:
        print(f"нет мужского голоса для: {', '.join(missing)}")
        return 1

    print("ПЛАН:")
    for lang, voice in plan:
        print(f"   {lang}: {voice}")
    print()

    t0 = time.time()
    for attempt in range(1, PASSES + 1):
        print(f"═══ проход {attempt} из {PASSES} ═══")
        for lang, voice in plan:
            print(f"--- {lang} / {voice} ---", flush=True)
            subprocess.run(
                [sys.executable, "-u", "-m", "app.scripts.tts_synthesize",
                 "--lang", lang, "--voice", voice, "--workers", str(WORKERS)],
                env={**os.environ, "ENV_FILE": ".env.local",
                     "PYTHONIOENCODING": "utf-8"},
                check=False,
            )
    print(f"\nвсего заняло {(time.time() - t0) / 3600:.1f} ч")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
