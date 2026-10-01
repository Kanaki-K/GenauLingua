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
from typing import TYPE_CHECKING, Iterable, Optional

from sqlalchemy.orm import InstrumentedAttribute

if TYPE_CHECKING:  # только для аннотаций: в рантайме импорт был бы циклическим
    from app.database.enums import TranslationMode


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
    "pl": Language(
        code="pl",
        flag="🇵🇱",
        word_attr="translation_pl",
        example_attr="example_pl",
        uses_article=False,
        # В польских словарях глагол даётся инфинитивом без частицы,
        # существительное без артикля — снимать нечего.
    ),
}

# Языки, которые можно изучать.
#
# Польский открыт 2026-10-01, когда его колонки заполнились: 12 747 слов из
# 12 902. Оставшиеся 155 в викторину не попадают сами — отбор идёт через
# word_lang_groups, а туда слово без перевода на изучаемый язык не заносится.
LEARNABLE_LANGS: tuple[str, ...] = ("de", "en", "ru", "uk", "tr", "pl")

# Языки, для которых база слов может быть заполнена — включая ещё не
# открытые. По этому списку строятся группы слов и озвучка.
SUPPORTED_LANGS: tuple[str, ...] = ("de", "en", "ru", "uk", "tr", "pl")

# Языки интерфейса — локали, которые реально существуют в app/locales.
# Немецкого интерфейса нет, поэтому список короче LEARNABLE_LANGS.
INTERFACE_LANGS: tuple[str, ...] = ("ru", "uk", "en", "tr", "de", "pl")

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


def option_label(word, code: Optional[str]) -> str:
    """
    Подпись варианта ответа: одно слово, как было до правки многозначности.

    Почему одно. Многозначные слова получили в базе все значения вместо одного
    — это исправление, от которого точность на таких словах выросла с 71% до
    80%. Но на кнопку шёл весь перевод целиком, и после той правки он дорос до
    133 символов: «записывать, записывать на плёнку или видео, принимать, брать
    к себе, начинать, приступать…». Четыре таких кнопки превращали карточку в
    простыню, а вид карточки согласован был до этой правки.

    Поэтому значения остаются в данных и показываются в разборе сразу после
    ответа, а на кнопке стоит первое — то, что считается самым частотным.

    Чем за это платим, честно: ученик, знающий «gleich» как «сразу», увидит
    «Одинаковый» и может не опознать. Полный набор он получит в разборе и
    выучит оттуда. Решение принято осознанно: это выбор между видом карточки и
    узнаваемостью, и вид выбран.

    Многоточия нет намеренно. Подпись — не обрезанный перевод, а главное
    значение; многоточие читалось бы как «тут что-то потерялось».

    На подбор дистракторов это не влияет: там сравниваются ВСЕ значения через
    meaning_variants, а не подпись. Иначе вариант, совпадающий с правильным по
    скрытому значению, прошёл бы в карточку — и выбрать правильный было бы
    невозможно.
    """
    full = display_text(word, code)
    if not full:
        return full

    parts = [p.strip() for p in _VARIANT_SPLIT_RE.split(full) if p.strip()]
    return parts[0] if parts else full


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


def learnable_names(interface_lang: str, *, with_flags: bool = False) -> str:
    """
    Перечисление изучаемых языков на языке интерфейса: «немецкий, английский…».

    Нужно текстам помощи и приветствия. Прежде список был вписан в них руками,
    и в четырёх локалях сразу — при добавлении языка его надо было не забыть в
    каждом месте. Теперь он собирается из LEARNABLE_LANGS, и включение языка
    обновляет тексты само.

    Флаги по умолчанию сняты: внутри фразы они дробят строку, а в списке
    настроек они уместны и там берутся отдельно.
    """
    return _names_of(LEARNABLE_LANGS, interface_lang, with_flags=with_flags)


def interface_names(interface_lang: str, *, with_flags: bool = False) -> str:
    """
    Перечисление языков интерфейса: «русский, украинский, английский…».

    Заведено по той же причине, что и learnable_names, и на том же ожоге.
    В текстах «О боте» список интерфейсных языков был вписан руками сразу в
    трёх локалях: «Інтерфейс російською, українською, англійською та
    турецькою». К моменту, когда локалей стало шесть, эти три строки врали —
    немецкого и польского в них не было. Теперь список берётся из
    INTERFACE_LANGS и расходиться с действительностью не может.
    """
    return _names_of(INTERFACE_LANGS, interface_lang, with_flags=with_flags)


def interface_count() -> int:
    """Сколько языков у интерфейса. Для фразы «интерфейс на шести языках»."""
    return len(INTERFACE_LANGS)


def _names_of(codes: tuple[str, ...], interface_lang: str, *,
              with_flags: bool = False) -> str:
    from app.locales import get_text

    # Приводить к строчным можно не везде. По-английски и по-турецки названия
    # языков пишутся с заглавной, а турецкое «İngilizce» при str.lower() даёт
    # «i̇ngilizce» — «i» с отдельной точкой сверху: заглавная «İ» разбирается на
    # две кодовые позиции. Это та же турецкая буква, на которой я уже
    # спотыкался в словарной базе.
    LOWERCASE_IN_TEXT = {"ru", "uk", "pl"}

    names = []
    for code in codes:
        name = get_text(language_name_key(code), interface_lang)
        if not with_flags:
            # Название приходит с флагом впереди — отрезаем его вместе с пробелом
            parts = name.split(" ", 1)
            name = parts[1] if len(parts) == 2 else name
            if interface_lang in LOWERCASE_IN_TEXT:
                name = name.lower()
        names.append(name)
    if len(names) < 2:
        return "".join(names)
    return ", ".join(names[:-1]) + f" {get_text('and_word', interface_lang)} " + names[-1]


def learnable_count() -> int:
    """Сколько языков открыто для изучения. Для фразы «шесть языков на выбор»."""
    return len(LEARNABLE_LANGS)


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
