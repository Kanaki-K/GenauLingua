"""
Реестр голосов озвучки.

Один регион на язык — сознательное решение: немецкий читается голосом из
Германии, английский британским. Без выбора акцента: одна норма для всех,
а не «выбери, какой английский правильнее».

Сколько голосов есть на самом деле (проверено перечислением у движка):
    de-DE  2 мужских, 2 женских (из 3 и 3 — см. ниже о многоязычных)
    en-GB  2 мужских, 3 женских
(в настройках из них по одному каждого пола — см. ниже)
    pl-PL  1 мужской,  1 женский
    ru-RU  1 мужской,  1 женский
    uk-UA  1 мужской,  1 женский
    tr-TR  1 мужской,  1 женский
    it-IT  1 мужской,  2 женских (Giuseppe — многоязычный, не берётся)
    es-ES  1 мужской,  2 женских
    fr-FR  1 мужской,  2 женских (Remy и Vivienne — многоязычные, не берутся)
    cs-CZ  1 мужской,  1 женский

МНОГОЯЗЫЧНЫХ ГОЛОСОВ НЕТ — Серафины и Флориана (`…MultilingualNeural`).
Такой голос сам угадывает язык каждой фразы и на немецком тексте местами
переходит на английское произношение; задать язык жёстко движок не даёт.
Владелец слышал это дважды: «будто английским читает немецкие» и 15.10 на
«Die Lieferung ist versandkostenfrei» — «как по-английски читает некоторые
звуки». Выбравшим их `resolve_voice` молча даёт голос по умолчанию.

Просили три и три на каждый язык, и прежде у немецкого их было четыре, у
английского пять. С 29.10 — ровно два на язык, женский и мужской: после
правок базы 28.10 только эти два озвучены целиком и проверены слухом, а
остальные отдавали бы новые примеры с задержкой синтеза или текстом
(решение владельца). Выбравшие убранный голос переходят на оставшийся того
же пола — см. `_RETIRED`.
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
    # Короткая подпись для экрана настроек — по-русски; на других языках
    # интерфейса её заменяет `shown(lang)`
    label: str

    def shown(self, lang: str | None) -> str:
        """
        Имя голоса на языке интерфейса.

        Подпись задана по-русски, и прежде показывалась как есть на любом
        языке: обход шести языков 14 октября нашёл «Voice: Катя» в
        английском, немецком, польском и турецком интерфейсе. Латинское
        имя берётся из самого идентификатора движка (`de-DE-KatjaNeural` →
        Katja) — правилом, а не списком: новый голос получит имя сам.
        Украинскому — украинское написание там, где оно отличается.
        """
        if lang in ("ru", None):
            return self.label
        if lang == "uk":
            return _UK_LABELS.get(self.label, self.label)
        latin = self.name.split("-")[2].replace("Multilingual", "").replace("Neural", "")
        return latin or self.label


# Где украинское написание имени отличается от русского
_UK_LABELS = {
    "Полина": "Поліна", "Светлана": "Світлана", "Дмитрий": "Дмитро",
    "Зофья": "Зоф'я", "Мейзи": "Мейзі", "Либби": "Ліббі", "Килиан": "Кіліан",
    "Эмель": "Емель", "Амала": "Амала", "Серафина": "Серафіна",
}


VOICES: dict[str, tuple[Voice, ...]] = {
    "de": (
        Voice("de-DE-KatjaNeural", "female", "Катя"),
        Voice("de-DE-ConradNeural", "male", "Конрад"),
    ),
    "en": (
        Voice("en-GB-SoniaNeural", "female", "Соня"),
        Voice("en-GB-RyanNeural", "male", "Райан"),
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
    "it": (
        Voice("it-IT-ElsaNeural", "female", "Эльза"),
        Voice("it-IT-DiegoNeural", "male", "Диего"),
    ),
    "es": (
        Voice("es-ES-ElviraNeural", "female", "Эльвира"),
        Voice("es-ES-AlvaroNeural", "male", "Альваро"),
    ),
    "fr": (
        Voice("fr-FR-DeniseNeural", "female", "Дениз"),
        Voice("fr-FR-HenriNeural", "male", "Анри"),
    ),
    "cs": (
        Voice("cs-CZ-VlastaNeural", "female", "Власта"),
        Voice("cs-CZ-AntoninNeural", "male", "Антонин"),
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
    "it": "Buongiorno! Ogni giorno imparo parole nuove.",
    "es": "¡Buenos días! Cada día aprendo palabras nuevas.",
    "fr": "Bonjour! J'apprends de nouveaux mots chaque jour.",
    "cs": "Dobrý den! Každý den se učím nová slova.",
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


# Голоса, убранные 29.10, и их пол: выбравший мужской голос должен
# остаться с мужским, а не молча получить женский по умолчанию
_RETIRED: dict[str, str] = {
    "de-DE-AmalaNeural": "female", "de-DE-KillianNeural": "male",
    "en-GB-LibbyNeural": "female", "en-GB-MaisieNeural": "female",
    "en-GB-ThomasNeural": "male", "it-IT-IsabellaNeural": "female",
    "es-ES-XimenaNeural": "female", "fr-FR-EloiseNeural": "female",
}


def resolve_voice(voice: Optional[str], lang: Optional[str]) -> str:
    """
    Голос, которым озвучивать. Негодный или чужой — заменяется на
    умолчание молча: сорванная озвучка хуже неожидаемого голоса.
    Убранный — на оставшийся того же пола.
    """
    if is_valid_voice(voice, lang):
        return voice
    same = by_gender(lang, _RETIRED.get(voice or "", ""))
    return same[0].name if same else default_voice(lang)


def preview_text(lang: Optional[str]) -> str:
    return PREVIEW_TEXT.get(lang or "", PREVIEW_TEXT["de"])


def by_gender(lang: Optional[str], gender: str) -> tuple[Voice, ...]:
    return tuple(v for v in voices_for(lang) if v.gender == gender)
