"""
Система локализации для GenauLingua Bot
"""

from typing import Optional
import app.locales.ru as ru
import app.locales.uk as uk
import app.locales.en as en
import app.locales.tr as tr
import app.locales.de as de
import app.locales.pl as pl

# Доступные локали.
#
# Немецкая и польская добавлены вместе с шестью изучаемыми языками: раз любая
# пара из шести доступна, то и читать бота человек может на своём. Набор ключей
# у всех локалей совпадает — это проверяет
# tests/test_locales.py::test_all_locales_have_identical_key_sets, и без него
# пропущенный ключ молча показывал бы текст на языке по умолчанию.
LOCALES = {
    "uk": uk.TEXTS,
    "en": en.TEXTS,
    "tr": tr.TEXTS,
    "ru": ru.TEXTS,
    "de": de.TEXTS,
    "pl": pl.TEXTS,
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