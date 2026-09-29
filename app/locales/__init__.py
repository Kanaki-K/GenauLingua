"""
Система локализации для GenauLingua Bot
"""

from typing import Optional
import app.locales.ru as ru
import app.locales.uk as uk
import app.locales.en as en
import app.locales.tr as tr

# Доступные локали
LOCALES = {
    "uk": uk.TEXTS,
    "en": en.TEXTS,
    "tr": tr.TEXTS,
    "ru": ru.TEXTS,
}

# Язык по умолчанию
DEFAULT_LOCALE = "uk"


def get_text(key: str, lang: Optional[str] = None, **kwargs) -> str:
    if lang not in LOCALES:
        lang = DEFAULT_LOCALE

    text = LOCALES[lang].get(key)

    if text is None:
        # Ключ отсутствует в запрошенной локали — берём из локали по умолчанию
        text = LOCALES[DEFAULT_LOCALE].get(key)
    if text is None:
        return f"[MISSING: {key}]"

    try:
        return text.format(**kwargs)
    except KeyError as e:
        return f"[ERROR: {key} missing parameter {e}]"


def get_available_languages() -> list[str]:
    return list(LOCALES.keys())


def is_language_supported(lang: str) -> bool:
    return lang in LOCALES