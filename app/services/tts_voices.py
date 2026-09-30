"""
Реестр голосов озвучки.

Один регион на язык — сознательное решение: немецкий читается голосом из
Германии, английский британским. Без выбора акцента: одна норма для всех,
а не «выбери, какой английский правильнее».

Сколько голосов есть на самом деле (проверено перечислением у движка):
    de-DE  3 мужских, 3 женских
    en-GB  2 мужских, 3 женских
    pl-PL  1 мужской,  1 женский
    ru-RU  1 мужской,  1 женский
    uk-UA  1 мужской,  1 женский
    tr-TR  1 мужской,  1 женский

Просили три и три на каждый язык. Для немецкого это выполнимо ровно,
для английского почти, для остальных — нет: у движка больше голосов не
существует. Там, где выбора нет, экран настроек показывает два голоса,
и это честнее, чем выдавать один голос за три, меняя ему скорость.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

# Скорость на 10% ниже обычной. Для A1 разборчивость важнее естественности:
# слово должно быть слышно по частям, а не проглатываться.
DEFAULT_RATE = "-10%"


@dataclass(frozen=True)
class Voice:
    # Идентификатор движка, он же хранится в кэше озвучки
    name: str
    gender: str          # 'male' | 'female'
    # Короткая подпись для экрана настроек
    label: str


VOICES: dict[str, tuple[Voice, ...]] = {
    "de": (
        Voice("de-DE-KatjaNeural", "female", "Катя"),
        Voice("de-DE-AmalaNeural", "female", "Амала"),
        Voice("de-DE-SeraphinaMultilingualNeural", "female", "Серафина"),
        Voice("de-DE-ConradNeural", "male", "Конрад"),
        Voice("de-DE-KillianNeural", "male", "Килиан"),
        Voice("de-DE-FlorianMultilingualNeural", "male", "Флориан"),
    ),
    "en": (
        Voice("en-GB-SoniaNeural", "female", "Соня"),
        Voice("en-GB-LibbyNeural", "female", "Либби"),
        Voice("en-GB-MaisieNeural", "female", "Мейзи"),
        Voice("en-GB-RyanNeural", "male", "Райан"),
        Voice("en-GB-ThomasNeural", "male", "Томас"),
    ),
    "pl": (
        Voice("pl-PL-ZofiaNeural", "female", "Зофья"),
        Voice("pl-PL-MarekNeural", "male", "Марек"),
    ),
    "ru": (
        Voice("ru-RU-SvetlanaNeural", "female", "Светлана"),
        Voice("ru-RU-DmitryNeural", "male", "Дмитрий"),
    ),
    "uk": (
        Voice("uk-UA-PolinaNeural", "female", "Полина"),
        Voice("uk-UA-OstapNeural", "male", "Остап"),
    ),
    "tr": (
        Voice("tr-TR-EmelNeural", "female", "Эмель"),
        Voice("tr-TR-AhmetNeural", "male", "Ахмет"),
    ),
}

# Голос по умолчанию — первый в списке языка. Именно он предгенерируется:
# остальные заполняются лениво, у тех, кто их выбрал.
DEFAULT_VOICE: dict[str, str] = {
    lang: voices[0].name for lang, voices in VOICES.items()
}

# Фраза для прослушивания в настройках. Своя на каждом языке, потому что
# демонстрировать акцент чужим текстом бессмысленно. Короткая: в настройках
# слушают подряд несколько голосов.
PREVIEW_TEXT: dict[str, str] = {
    "de": "Guten Tag! Ich lerne jeden Tag neue Wörter.",
    "en": "Good afternoon! I learn new words every day.",
    "pl": "Dzień dobry! Codziennie uczę się nowych słów.",
    "ru": "Добрый день! Я каждый день учу новые слова.",
    "uk": "Добрий день! Я щодня вчу нові слова.",
    "tr": "İyi günler! Her gün yeni kelimeler öğreniyorum.",
}


def voices_for(lang: Optional[str]) -> tuple[Voice, ...]:
    return VOICES.get(lang or "", ())


def default_voice(lang: Optional[str]) -> str:
    """
    Голос по умолчанию. Для неизвестного языка — немецкий: озвучка не должна
    падать на старых данных, где изучаемый язык мог не быть записан.
    """
    return DEFAULT_VOICE.get(lang or "", DEFAULT_VOICE["de"])


def is_valid_voice(voice: Optional[str], lang: Optional[str]) -> bool:
    """Принадлежит ли голос этому языку. Защита от чужого значения в настройках."""
    if not voice:
        return False
    return any(v.name == voice for v in voices_for(lang))


def resolve_voice(voice: Optional[str], lang: Optional[str]) -> str:
    """
    Голос, которым озвучивать. Негодный или чужой — заменяется на
    умолчание молча: сорванная озвучка хуже неожидаемого голоса.
    """
    return voice if is_valid_voice(voice, lang) else default_voice(lang)


def preview_text(lang: Optional[str]) -> str:
    return PREVIEW_TEXT.get(lang or "", PREVIEW_TEXT["de"])


def by_gender(lang: Optional[str], gender: str) -> tuple[Voice, ...]:
    return tuple(v for v in voices_for(lang) if v.gender == gender)
