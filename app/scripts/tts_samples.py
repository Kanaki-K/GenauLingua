# -*- coding: utf-8 -*-
"""
Образцы озвучки: по одному файлу на язык, чтобы услышать качество
до того как генерировать десятки тысяч.

Голос берётся по ИЗУЧАЕМОМУ языку — тогда слышен родной акцент. Если
подать немецкий текст русскому голосу, получится русский, читающий
по-немецки, а нужно наоборот.

Формат: слово, пауза, пример — как и просили, слово первым.
"""
import asyncio
import pathlib
import sys

import edge_tts

OUT = pathlib.Path(__file__).resolve().parent.parent.parent / "tts_samples"

# Женский и мужской голос на каждый язык — выбрать можно на слух
VOICES = {
    "de": ("de-DE-KatjaNeural", "de-DE-ConradNeural"),
    "en": ("en-GB-SoniaNeural", "en-GB-RyanNeural"),
    "ru": ("ru-RU-SvetlanaNeural", "ru-RU-DmitryNeural"),
    "uk": ("uk-UA-PolinaNeural", "uk-UA-OstapNeural"),
    "tr": ("tr-TR-EmelNeural", "tr-TR-AhmetNeural"),
}

# Реальные слова из базы с примерами
SAMPLES = {
    "de": ("die Verantwortung", "Er übernimmt die Verantwortung für das Projekt."),
    "en": ("responsibility", "He takes responsibility for the project."),
    "ru": ("ответственность", "Он берёт ответственность за проект."),
    "uk": ("відповідальність", "Він бере відповідальність за проект."),
    "tr": ("sorumluluk", "Proje için sorumluluğu üstleniyor."),
}

# Пауза между словом и примером: SSML-разметка через edge-tts недоступна,
# поэтому пауза задаётся многоточием — движок её отрабатывает как вдох
PAUSE = " … "


async def synth(text: str, voice: str, path: pathlib.Path, rate: str = "-10%") -> None:
    # Замедление на 10%: для учебной озвучки разборчивость важнее живости
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(str(path))


async def main() -> None:
    OUT.mkdir(exist_ok=True)
    made = []

    for lang, (word, example) in SAMPLES.items():
        female, male = VOICES[lang]

        # только слово
        p = OUT / f"{lang}_1_word.mp3"
        await synth(word, female, p)
        made.append(p)

        # слово + пауза + пример, одним файлом
        p = OUT / f"{lang}_2_word_and_example.mp3"
        await synth(f"{word}{PAUSE}{example}", female, p)
        made.append(p)

        # мужской голос для сравнения
        p = OUT / f"{lang}_3_male.mp3"
        await synth(f"{word}{PAUSE}{example}", male, p)
        made.append(p)

    print(f"Готово, файлов: {len(made)}\n")
    print(f"{'файл':36} {'размер':>9}")
    total = 0
    for p in made:
        size = p.stat().st_size
        total += size
        print(f"  {p.name:34} {size / 1024:7.1f} КБ")
    print(f"\nвсего: {total / 1024:.0f} КБ")

    words_only = sum(p.stat().st_size for p in made if "_1_word" in p.name) / 5
    with_example = sum(p.stat().st_size for p in made if "_2_" in p.name) / 5
    print(f"\nсредний размер: слово {words_only / 1024:.1f} КБ, "
          f"слово+пример {with_example / 1024:.1f} КБ")
    print(f"на 12 902 слова одного языка:")
    print(f"  только слова:     {words_only * 12902 / 1024 / 1024:.0f} МБ")
    print(f"  слово и пример:   {with_example * 12902 / 1024 / 1024:.0f} МБ")
    print(f"\nПослушать: {OUT.resolve()}")


asyncio.run(main())
