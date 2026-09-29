"""
Реестр языков и абстракция «стороны карточки».

Слово в базе — одна строка с немецким headword и переводами. Для обучения
любому из языков нужна одна операция: «дай текст слова на языке L» и
«дай пример на языке L». Всё остальное (какой язык учим, на какой переводим,
в какую сторону спрашиваем) выражается через пару (learning_lang, native_lang)
и флаг reverse.

Здесь же нормализация headword — она нужна, чтобы схлопывать строки,
которые для конкретного языка дают одно и то же слово
(Meeting / Sitzung / Treff / Versammlung → «meeting»).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable, Optional

from sqlalchemy.orm import InstrumentedAttribute


@dataclass(frozen=True)
class Language:
    code: str
    flag: str
    # Атрибуты модели Word, в которых лежит слово и пример на этом языке
    word_attr: str
    example_attr: str
    # Показывать ли артикль из Word.article рядом со словом
    uses_article: bool
    # Служебные слова, которые снимаются при нормализации headword
    leading_particles: tuple[str, ...] = ()


LANGUAGES: dict[str, Language] = {
    "de": Language(
        code="de",
        flag="🇩🇪",
        word_attr="word_de",
        example_attr="example_de",
        uses_article=True,
        leading_particles=("der", "die", "das"),
    ),
    "ru": Language(
        code="ru",
        flag="🏴",
        word_attr="translation_ru",
        example_attr="example_ru",
        uses_article=False,
    ),
    "uk": Language(
        code="uk",
        flag="🇺🇦",
        word_attr="translation_uk",
        example_attr="example_uk",
        uses_article=False,
    ),
    "en": Language(
        code="en",
        flag="🇬🇧",
        word_attr="translation_en",
        example_attr="example_en",
        uses_article=False,
        leading_particles=("to", "the", "a", "an"),
    ),
    "tr": Language(
        code="tr",
        flag="🇹🇷",
        word_attr="translation_tr",
        example_attr="example_tr",
        uses_article=False,
    ),
}

# Языки, которые можно изучать
LEARNABLE_LANGS: tuple[str, ...] = ("de", "en", "ru", "uk", "tr")

# Языки интерфейса — локали, которые реально существуют в app/locales.
# Немецкого интерфейса нет, поэтому список короче LEARNABLE_LANGS.
INTERFACE_LANGS: tuple[str, ...] = ("ru", "uk", "en", "tr")

DEFAULT_LEARNING_LANG = "de"
DEFAULT_NATIVE_LANG = "ru"


def is_learnable(code: Optional[str]) -> bool:
    return code in LANGUAGES


def get_language(code: Optional[str]) -> Language:
    """Язык по коду. Неизвестный код — немецкий, чтобы не падать на старых данных."""
    return LANGUAGES.get(code or "", LANGUAGES[DEFAULT_LEARNING_LANG])


def flag(code: Optional[str]) -> str:
    return get_language(code).flag


def word_column(code: Optional[str]) -> InstrumentedAttribute:
    """Колонка Word со словом на этом языке — для использования в SQL-запросах."""
    from app.database.models import Word

    return getattr(Word, get_language(code).word_attr)


def example_column(code: Optional[str]) -> InstrumentedAttribute:
    from app.database.models import Word

    return getattr(Word, get_language(code).example_attr)


def word_text(word, code: Optional[str], *, with_article: bool = True) -> str:
    """
    Текст слова на языке `code`, готовый к показу.

    Для немецкого подклеивается артикль, если он есть и осмысленный.
    """
    lang = get_language(code)
    raw = getattr(word, lang.word_attr, None) or ""
    raw = raw.strip()
    if not raw:
        return ""

    if with_article and lang.uses_article:
        article = (getattr(word, "article", None) or "").strip()
        if article and article != "-":
            return f"{article} {raw}"

    return raw


def display_text(word, code: Optional[str]) -> str:
    """
    Текст слова для показа пользователю.

    Переводы приводятся к заглавной первой букве — так было в прежней версии.
    Немецкое слово не трогаем: регистр в немецком значим, существительные
    пишутся с большой буквы, остальное со строчной.
    """
    text = word_text(word, code)
    if not text or get_language(code).uses_article:
        return text
    return text[:1].upper() + text[1:]


def example_text(word, code: Optional[str]) -> str:
    lang = get_language(code)
    return (getattr(word, lang.example_attr, None) or "").strip()


def pair_label(pair: "LanguagePair") -> str:
    """
    Подпись направления в прежнем стиле: «🇩🇪 DE → 🏴 RU».

    Собирается из флагов и кодов, поэтому для любой из двадцати пар выглядит
    так же, как раньше выглядели восемь захардкоженных вариантов.
    """
    src, dst = pair.prompt_lang, pair.answer_lang
    return f"{flag(src)} {src.upper()} → {flag(dst)} {dst.upper()}"


def pair_flags(pair: "LanguagePair") -> str:
    """Короткая подпись только флагами: «🇩🇪 → 🏴» (для статистики)."""
    return f"{flag(pair.prompt_lang)} → {flag(pair.answer_lang)}"


_WS_RE = re.compile(r"\s+")
_VARIANT_RE = re.compile(r"\s*[/;,].*$")
_VARIANT_SPLIT_RE = re.compile(r"[/;,]")
_PUNCT_RE = re.compile(r"[!?.…]+$")


def meaning_variants(text: Optional[str], code: Optional[str]) -> frozenset[str]:
    """
    Все значения, записанные в одной ячейке перевода.

    Многие переводы содержат несколько значений через разделитель: «a / an»,
    «сразу, одинаковый». Это источник главной проблемы качества: многозначному
    слову присвоено одно значение из нескольких, и в тесте из четырёх вариантов
    ученик угадывает не язык, а выбор базы.

    Для сборки вариантов ответа нужно сравнивать по всем значениям сразу —
    иначе дистрактор может оказаться таким же верным ответом, как правильный.
    """
    if not text:
        return frozenset()

    variants = set()
    for part in _VARIANT_SPLIT_RE.split(str(text)):
        norm = normalize_headword(part, code)
        if norm:
            variants.add(norm)

    return frozenset(variants)


def normalize_headword(text: Optional[str], code: Optional[str]) -> str:
    """
    Ключ для схлопывания слов, которые на языке `code` выглядят одинаково.

    Снимает регистр, служебные префиксы («to run» → «run»), берёт первый
    вариант из многозначных («a / an» → «a») и сводит пробелы.

    Пустая строка означает «слово на этом языке непригодно» — такие строки
    в группы не попадают.
    """
    if not text:
        return ""

    s = text.strip().lower()
    s = _VARIANT_RE.sub("", s)
    s = _PUNCT_RE.sub("", s)
    s = _WS_RE.sub(" ", s).strip()

    particles = get_language(code).leading_particles
    if particles:
        # Префикс снимаем только если после него что-то осталось:
        # «to» и «the» сами по себе — полноценные слова.
        for p in particles:
            prefix = f"{p} "
            if s.startswith(prefix):
                rest = s[len(prefix):].strip()
                if rest:
                    s = rest
                break

    return s


# ============================================================================
# ПАРА ЯЗЫКОВ: что учим, на что переводим, в какую сторону спрашиваем
# ============================================================================


@dataclass(frozen=True)
class LanguagePair:
    """
    learning — язык, который пользователь изучает.
    native   — язык, на котором даётся значение.
    reverse  — False: показываем learning, просим выбрать native (узнавание).
               True:  показываем native, просим выбрать learning (производство).
    """

    learning: str
    native: str
    reverse: bool = False

    @property
    def prompt_lang(self) -> str:
        """Язык, на котором задаётся вопрос."""
        return self.native if self.reverse else self.learning

    @property
    def answer_lang(self) -> str:
        """Язык, на котором даются варианты ответа."""
        return self.learning if self.reverse else self.native

    @property
    def prompt_flag(self) -> str:
        return flag(self.prompt_lang)

    @property
    def answer_flag(self) -> str:
        return flag(self.answer_lang)

    def describe(self) -> str:
        """Короткое «🇩🇪 → 🏴» для показа в статистике и настройках."""
        return f"{self.prompt_flag} → {self.answer_flag}"


def pair_from_user(user) -> LanguagePair:
    """
    Пара языков пользователя с подстраховкой на неполные данные.

    Если learning и native совпали (или native не задан), native
    подбирается автоматически — иначе викторина выродится в «слово = слово».
    """
    learning = user.learning_lang if is_learnable(user.learning_lang) else DEFAULT_LEARNING_LANG
    native = user.native_lang if is_learnable(user.native_lang) else None

    if native is None or native == learning:
        native = fallback_native_for(learning, preferred=user.interface_language)

    return LanguagePair(
        learning=learning,
        native=native,
        reverse=bool(getattr(user, "reverse_mode", False)),
    )


def fallback_native_for(learning: str, preferred: Optional[str] = None) -> str:
    """Подобрать язык значения, отличный от изучаемого."""
    if is_learnable(preferred) and preferred != learning:
        return preferred
    if learning != DEFAULT_NATIVE_LANG:
        return DEFAULT_NATIVE_LANG
    return "en"


def native_options(learning: str) -> list[str]:
    """Языки, на которые можно переводить при изучении `learning`."""
    return [code for code in LEARNABLE_LANGS if code != learning]


def language_name_key(code: str) -> str:
    """Ключ локализации с названием языка: 'en' → 'langname_en'."""
    return f"langname_{code}"


def iter_languages(codes: Optional[Iterable[str]] = None) -> list[Language]:
    return [LANGUAGES[c] for c in (codes or LEARNABLE_LANGS) if c in LANGUAGES]


# ============================================================================
# СОВМЕСТИМОСТЬ СО СТАРЫМ TranslationMode
# ============================================================================

# Старый enum описывал только пары с немецким. Нужен в обе стороны:
# читаем при миграции старых пользователей, пишем — чтобы аналитика
# и откат на предыдущую версию продолжали работать.
def _legacy_modes() -> dict[tuple[str, str, bool], "TranslationMode"]:
    from app.database.enums import TranslationMode

    return {
        ("de", "ru", False): TranslationMode.DE_TO_RU,
        ("de", "ru", True): TranslationMode.RU_TO_DE,
        ("de", "uk", False): TranslationMode.DE_TO_UK,
        ("de", "uk", True): TranslationMode.UK_TO_DE,
        ("de", "en", False): TranslationMode.DE_TO_EN,
        ("de", "en", True): TranslationMode.EN_TO_DE,
        ("de", "tr", False): TranslationMode.DE_TO_TR,
        ("de", "tr", True): TranslationMode.TR_TO_DE,
    }


def legacy_mode_name(pair: LanguagePair):
    """
    Значение старого TranslationMode для пары, если она в нём выразима.
    Для пар без немецкого (например ru→en) — None.
    """
    return _legacy_modes().get((pair.learning, pair.native, pair.reverse))


def pair_from_legacy_mode(mode_value: Optional[str]) -> Optional[LanguagePair]:
    """Разобрать 'DE_TO_RU' / 'ru_to_de' в пару языков. Регистр не важен."""
    if not mode_value:
        return None

    parts = str(mode_value).strip().lower().split("_to_")
    if len(parts) != 2:
        return None

    src, dst = parts
    if not (is_learnable(src) and is_learnable(dst)):
        return None

    if src == "de":
        return LanguagePair(learning="de", native=dst, reverse=False)
    if dst == "de":
        return LanguagePair(learning="de", native=src, reverse=True)
    return LanguagePair(learning=dst, native=src, reverse=False)
