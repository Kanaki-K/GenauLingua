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
import app.locales.it as it
import app.locales.es as es
import app.locales.fr as fr
import app.locales.cs as cs

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
    # Итальянская, испанская, французская, чешская — с 16.10 выбираются
    # наравне с остальными (INTERFACE_LANGS)
    "it": it.TEXTS,
    "es": es.TEXTS,
    "fr": fr.TEXTS,
    "cs": cs.TEXTS,
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

    # ЧИСЛО ДНЕЙ СЛОВОМ — правилом здесь, а не формой в каждой строке.
    # Обход шести языков 14 октября: «1 days», «1 Tage», «1 dni» — а
    # серия в 1 день бывает у каждого в первый же день. Строка пишет
    # `{days_word}`, вызывающий передаёт число `days`, форма — по языку
    if "{days_word}" in text and "days" in kwargs:
        kwargs = {**kwargs, "days_word": plural(int(kwargs["days"]), "plural_days", lang)}

    try:
        return text.format(**kwargs)
    except KeyError as e:
        return f"[ERROR: {key} missing parameter {e}]"


# ============================================================================
# ЧИСЛО СО СЛОВОМ
#
# Прежде форма слова при числе стояла в строке намертво: «{score} баллов»,
# «Отправлено {count} репортов». При 1 выходило «1 баллов», при 21 —
# «21 баллов»; в английском «1 points». Аудит 14 октября нашёл пять таких
# строк в трёх языках сразу.
#
# Формы лежат в локали одной строкой через «|» (`plural_points`:
# «балл|балла|баллов»), а выбор формы — правило языка здесь. Языку с одной
# формой (турецкий: после числа множественного нет) хватает одной.
# ============================================================================

def _plural_index(count: int, lang: str) -> int:
    """Номер формы: 0 — «один», 1 — «два-четыре», 2 — «пять»."""
    n = abs(int(count))
    if lang in ("ru", "uk"):
        if n % 10 == 1 and n % 100 != 11:
            return 0
        if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
            return 1
        return 2
    if lang in ("pl", "cs"):
        # В польском и чешском «один» — только сама единица: 21 — уже
        # «punktów» / «bodů»; 2–4 — своя форма («2 body»), 5+ — третья
        if n == 1:
            return 0
        if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
            return 1
        return 2
    if lang == "tr":
        return 0
    if lang == "fr":
        # Во французском и ноль — единственное число: «0 point», «1 point»
        return 0 if n in (0, 1) else 1
    # en, de, it, es: единственное только у единицы
    return 0 if n == 1 else 1


def plural(count: int, forms_key: str, lang: Optional[str] = None) -> str:
    """«21 балл», «2 балла», «5 баллов» — число вместе со словом в нужной форме."""
    if lang not in LOCALES:
        lang = DEFAULT_LOCALE
    forms = get_text(forms_key, lang).split("|")
    form = forms[min(_plural_index(count, lang), len(forms) - 1)]
    return f"{count} {form}"


def get_available_languages() -> list[str]:
    return list(LOCALES.keys())


def is_language_supported(lang: str) -> bool:
    return lang in LOCALES