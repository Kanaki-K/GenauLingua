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
import unicodedata
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
    # it, es, fr — существительное в переводе стоит с определённым артиклем
    # («il libro», «la casa», «l'uomo»): род виден только по нему, а ученику
    # он нужен, как немецкий der/die/das. Для схлопывания артикль снимается.
    # Word.article — немецкий, поэтому uses_article у них False: свой артикль
    # уже внутри перевода. Правила перевода — archive/new_langs/GUIDE.md.
    "it": Language(
        code="it",
        flag="🇮🇹",
        word_attr="translation_it",
        example_attr="example_it",
        uses_article=False,
        leading_particles=("il", "lo", "la", "i", "gli", "le", "l'"),
    ),
    "es": Language(
        code="es",
        flag="🇪🇸",
        word_attr="translation_es",
        example_attr="example_es",
        uses_article=False,
        leading_particles=("el", "la", "los", "las"),
    ),
    "fr": Language(
        code="fr",
        flag="🇫🇷",
        word_attr="translation_fr",
        example_attr="example_fr",
        uses_article=False,
        leading_particles=("le", "la", "les", "l'"),
    ),
    "cs": Language(
        code="cs",
        flag="🇨🇿",
        word_attr="translation_cs",
        example_attr="example_cs",
        uses_article=False,
        # Артиклей нет; возвратное «se/si» стоит после глагола и не снимается
    ),
}

# Языки, которые можно изучать.
#
# Польский открыт 2026-10-01, когда его колонки заполнились: 12 747 слов из
# 12 902. Оставшиеся 155 в викторину не попадают сами — отбор идёт через
# word_lang_groups, а туда слово без перевода на изучаемый язык не заносится.
#
# Итальянский, испанский, французский, чешский открыты 16.10 (решение
# владельца: «полностью интегрировать варианты новых 4 языков»): словарь
# 12 902 из 12 902 по каждому, проверен вычиткой и аудитом всех рядов,
# интерфейс — 464 ключа на «Вы». Звук синтезируется при первом показе и
# дальше живёт файлом (`audio_service.obtain_audio`).
LEARNABLE_LANGS: tuple[str, ...] = ("de", "en", "ru", "uk", "tr", "pl", "it", "es", "fr", "cs")

# Языки, для которых база слов может быть заполнена — включая ещё не
# открытые. По этому списку строятся группы слов и озвучка.
SUPPORTED_LANGS: tuple[str, ...] = ("de", "en", "ru", "uk", "tr", "pl", "it", "es", "fr", "cs")

# Языки интерфейса — локали, которые реально существуют в app/locales.
# Немецкого интерфейса нет, поэтому список короче LEARNABLE_LANGS.
# ПОРЯДОК ЗДЕСЬ — РЕШЕНИЕ ВЛАДЕЛЬЦА, и он не алфавитный и не по числу
# пользователей. Украинский первым, русский последним. Дословно: «русский
# только по одной причине — украинцы на нём говорят».
#
# Эта строка задаёт порядок ВСЮДУ: и кнопки выбора языка при первом запуске
# (`get_language_selection_keyboard` читает её, а не свой список), и
# перечисление языков в текстах. Один источник — потому и правится в одном
# месте.
#
# Порядок от 16.10 — сгруппированный: украинский первым, русский последним,
# между ними западные языки, затем турецкий. Закрытые языки встают на свои
# места из LANGUAGE_ORDER, когда открываются: открыть язык = добавить его код
# в _INTERFACE_OPEN, а не искать ему место в кортеже.
LANGUAGE_ORDER: tuple[str, ...] = ("uk", "en", "de", "pl", "cs", "es", "fr", "it", "tr", "ru")
_INTERFACE_OPEN = {"uk", "en", "de", "pl", "cs", "es", "fr", "it", "tr", "ru"}
INTERFACE_LANGS: tuple[str, ...] = tuple(c for c in LANGUAGE_ORDER if c in _INTERFACE_OPEN)

DEFAULT_LEARNING_LANG = "de"
DEFAULT_NATIVE_LANG = "ru"


def is_learnable(code: Optional[str]) -> bool:
    """
    Можно ли учить этот язык (и показывать на нём значения) — ОТКРЫТ ли он.

    Прежде проверка шла по LANGUAGES, то есть по реестру. Пока в реестре
    были одни открытые языки, разницы не было; с приходом it/es/fr/cs
    поддельное нажатие `set_learning_it` поставило бы закрытый язык — круг
    без звука, интерфейса и выверенных пар (Н2).
    """
    return code in LEARNABLE_LANGS


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


def upper_first(text: str, code: Optional[str]) -> str:
    """
    Первая буква заглавной — по правилам ЯЗЫКА, а не питоновского `.upper()`.

    ЗАЧЕМ ЭТО ЕСТЬ. В турецком две разные буквы «i»: с точкой и без, и
    заглавные у них тоже разные — «i» → «İ», «ı» → «I». Питоновский
    `.upper()` обе превращает в «I», и карточка показывала «Iş» вместо
    «İş», «Ilan» вместо «İlan». Для турка это не опечатка, а другая буква:
    «ışık» (свет) и «işik» — разные слова.

    В базе это давно починено скриптом `fix_turkish_i` и закреплено тестом
    `test_turkish_i.py`, но показ ломал данные заново: `display_text` и
    `option_label` поднимали регистр на лету. Замер по базе: **531 турецкое
    слово из 561 показывалось с чужой буквой.**

    Остальные пять языков питоновское правило устраивает.
    """
    if not text:
        return text
    if (code or "") == "tr":
        if text[0] == "i":
            return "İ" + text[1:]
        if text[0] == "ı":
            return "I" + text[1:]
    return text[:1].upper() + text[1:]


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
    return upper_first(text, code)


def option_label(word, code: Optional[str]) -> str:
    """
    Подпись варианта ответа: одно слово, как было до правки многозначности.

    Почему одно. Многозначные слова получили в базе все значения вместо одного
    — это исправление, от которого точность на таких словах выросла с 71% до
    80%. Но на кнопку шёл весь перевод целиком, и после той правки он дорос до
    133 символов: «записывать, записывать на плёнку или видео, принимать, брать
    к себе, начинать, приступать…». Четыре таких кнопки превращали карточку в
    простыню, а вид карточки согласован был до этой правки.

    Поэтому значения остаются в данных, а на кнопке стоит одно — то, что
    стоит в примере. Полный набор виден на экране «Помилка перекладу»:
    жалуешься на перевод — видишь всё, на что жалуешься. В разборе после
    ответа его НЕТ, там тоже одно значение с каждой стороны.

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

    Какое именно значение берётся — решает main_meaning: то, что стоит в
    примере. Прежде бралось просто первое, и карточка показывала «Swot», звук
    произносил «Swot», а пример был про «overachiever» — три разных слова в
    одной карточке.
    """
    full = display_text(word, code)
    if not full:
        return full

    chosen = main_meaning(word, code)
    if not chosen:
        parts = [p.strip() for p in _VARIANT_SPLIT_RE.split(full) if p.strip()]
        return parts[0] if parts else full
    # display_text поднимает первую букву — повторяем для выбранного значения
    if get_language(code).uses_article:
        return chosen
    return upper_first(chosen, code)


def example_text(word, code: Optional[str]) -> str:
    lang = get_language(code)
    return (getattr(word, lang.example_attr, None) or "").strip()


def pair_label(pair: "LanguagePair", interface_lang: Optional[str] = None) -> str:
    """
    Подпись направления СЛОВАМИ: «Немецкий → Русский».

    Прежде собиралась из флагов и кодов — «🇩🇪 DE → 🏴 RU», — и это был
    третий способ обозначить язык в одном боте: на выборе стояло «🏴
    Русский», в заголовке занятия «🇩🇪 Немецкий → 🏴» вообще без названия, а
    здесь код из двух букв. Решение владельца: языки пишутся словами, и
    тогда подпись одна на все двадцать пар.

    Язык интерфейса необязателен ради вызывающих, которым он недоступен:
    без него берётся язык по умолчанию, как и везде в `get_text`.
    """
    return (f"{language_word(pair.prompt_lang, interface_lang)}"
            f" → {language_word(pair.answer_lang, interface_lang)}")


def pair_flags(pair: "LanguagePair", interface_lang: Optional[str] = None) -> str:
    """
    Короткая подпись пары. Имя осталось прежним, флагов в ней больше нет.

    Переименовать её заодно значило бы править семь мест вызова одной
    правкой с двумя смыслами; имя поправится отдельно.
    """
    return pair_label(pair, interface_lang)


_WS_RE = re.compile(r"\s+")
# Разделитель значений — только вне скобок: «ваш (ваша, ваше)» одно значение
# с формами, а не три. Прежде резалось и внутри, и карточка показывала
# «ваш (ваша» — 43 карточки в восьми языках (замер 29.10)
_OUTSIDE_PARENS = r"(?![^()]*\))"
_VARIANT_RE = re.compile(r"\s*[/;,]" + _OUTSIDE_PARENS + r".*$")
_VARIANT_SPLIT_RE = re.compile(r"[/;,]" + _OUTSIDE_PARENS)
_PUNCT_RE = re.compile(r"[!?.…]+$")

# Сколько букв основы должно совпасть, чтобы счесть слово тем же. Четыре —
# компромисс: короче начинает склеивать разные слова («вел» и «величие»),
# длиннее теряет словоизменение с чередованием.
_STEM_MIN = 4
_TOKEN_RE = re.compile(r"\w+", re.UNICODE)


def fold(s: str) -> str:
    """
    Привести текст к виду, пригодному для СРАВНЕНИЯ: без регистра и диакритики.

    ЭТИМ, А НЕ `.lower()`. Питоновский `.lower()` на турецкой «İ» даёт «i» с
    ОТДЕЛЬНОЙ комбинирующей точкой (U+0307), и сравнение с обычным «i»
    расходится. Ловушка срабатывала уже четырежды: дважды в проверках
    озвучки, один раз в гейте названий клипов и один раз в приёмке трёх
    игр — каждый раз давая десятки ложных тревог при полностью верных
    данных.

    Здесь после `.lower()` строка раскладывается в NFD и комбинирующие
    знаки выбрасываются, поэтому «İstisna» и «istisna» сходятся, как и
    «Häuser» с «hauser».

    Если где-то в коде появится сравнение текста через `.lower()` — это
    почти наверняка пятый случай той же ошибки.
    """
    s = s.lower().replace("ß", "ss").replace("ł", "l").replace("Ł", "l")
    decomposed = unicodedata.normalize("NFD", s)
    bare = "".join(c for c in decomposed if not unicodedata.combining(c))
    # Турецкая БЕСТОЧЕЧНАЯ «ı» — вторая половина той же ловушки. Снятие
    # комбинирующих знаков приводит к общему виду пару «İ»/«i», но не пару
    # «I»/«ı»: Python переводит «I» в «i», тогда как по-турецки — в «ı»,
    # и «Islık» со «ıslık» расходятся на первой же букве. Сводим обе к «i»
    # — ровно так же, как уже сводим немецкие умляуты к голым гласным.
    return bare.replace("ı", "i")


_TAIL_STRICT = 3
_TAIL_LOOSE = 5


def _stem_tail(needle: str, haystack_tokens: list[str],
               whole_letter: bool = True) -> int | None:
    """
    Насколько ПЛОХО слово `needle` сходится с лучшим словом примера.

    Возвращает, сколько букв основы осталось лишними при самом удачном
    совпадении: 0 — слово нашлось целиком, 4 — совпали все буквы кроме
    четырёх последних. `None` — не нашлось вовсе.

    Нужно, чтобы выбирать ЛУЧШЕЕ значение, а не первое подошедшее. Пока
    правило было «первое, что совпало», в `öfters` показывалось «частенько»
    при примере «часто», а в `Moral` — «moralność» при примере «morale»:
    ранний приблизительный вариант затенял поздний точный.
    """
    head = fold(needle)
    if not head:
        return None
    # Слово из одной буквы сравнивается только целиком: иначе чешское «k»
    # находилось в «kamarády», и ряд `zum` с примером «na pláž» показывал и
    # озвучивал «k» (проверка слухом 29.10). Двух букв это не касается:
    # турецкие «iş», «ad», «at» стоят в примере с окончаниями. И не касается
    # окончаний вроде «-a» — они и есть часть слова (whole_letter=False)
    if len(head) == 1 and whole_letter:
        return 0 if head in haystack_tokens else None
    need = min(_STEM_MIN, len(head))
    best: int | None = None
    for token in haystack_tokens:
        common = 0
        for a, b in zip(head, token):
            if a != b:
                break
            common += 1
        if common >= need:
            tail = len(head) - common
            best = tail if best is None else min(best, tail)
        # Основа может прятаться внутри составного слова: «gehen» в «weggehen»
        if len(head) >= _STEM_MIN and head[: max(need, len(head) - 2)] in token:
            best = 0
    return best


def _stem_in(needle: str, haystack_tokens: list[str]) -> bool:
    """Есть ли слово `needle` в словах примера, пусть и в другой форме."""
    head = fold(needle)
    if not head:
        return False
    need = min(_STEM_MIN, len(head))
    for token in haystack_tokens:
        common = 0
        for a, b in zip(head, token):
            if a != b:
                break
            common += 1
        # Совпала основа и от слова осталось немного — это словоизменение
        if common >= need and len(head) - common <= 3:
            return True
        # Основа может прятаться внутри составного слова: «gehen» в «weggehen»
        if len(head) >= _STEM_MIN and head[:max(need, len(head) - 2)] in token:
            return True
    return False


def _stem_in_loose(needle: str, haystack_tokens: list[str]) -> bool:
    """
    То же, но с поблажкой на одну букву — для коротких слов.

    Зачем. Четырёх букв основы хватает почти везде, но ровно у
    четырёхбуквенного слова падежное окончание съедает нужную четвёртую
    букву: «вода» и «воду» совпадают только на трёх, «шина» и «шину» тоже.
    Строгое правило объявляло их разными словами, и карточка показывала не
    то значение, что стоит в примере: ряд `Schiene` показывал «рельс», хотя
    пример был про шину на руке, а `Messe` показывал «виставка», хотя пример
    про мессу в церкви.

    Поблажка узкая, и каждое её условие отрезает замеренный ложный случай:

    · только сравнение с начала слова. Поиск основы внутри слова с тремя
      буквами находит «ес» внутри «ресторане» — ветвь составного слова
      поблажки не получает;
    · не меньше трёх общих букв и слово не короче четырёх. Иначе «они» и
      «она» становятся одним словом;
    · слово примера должно быть длиннее основы. Иначе «then» цепляется за
      «the», а «что?» за «что».

    Решать поблажке позволено только при однозначности: если под неё
    подходит больше одного значения из ячейки, выбор остаётся за строгим
    правилом. На трёх буквах разные формы одного слова («живий» и «живе»,
    «один в одного» и «одне в одне») неразличимы, и угадывать тут нечего.
    """
    head = fold(needle)
    if len(head) < _STEM_MIN:
        return False
    need = max(3, min(_STEM_MIN, len(head) - 1))
    for token in haystack_tokens:
        if len(token) <= need:
            continue
        common = 0
        for a, b in zip(head, token):
            if a != b:
                break
            common += 1
        if common >= need and len(head) - common <= 3:
            return True
    return False


def main_meaning(word, code: Optional[str]) -> str:
    """
    Одно значение из перевода — то самое, которое стоит в примере.

    Зачем не просто первое. В ячейке «Swot, overachiever, nerd» первое
    значение «Swot», а пример написан про «overachiever». Раньше на карточке
    показывалось первое, голос произносил первое, а пример приводил третье —
    человек видел одно слово, слышал его же и читал фразу про другое. Три
    разных слова в одной карточке.

    Поэтому значение выбирается по примеру: берётся первое из тех, что в
    примере действительно встречаются, пусть и в другой грамматической форме.
    Если ни одно не встретилось — остаётся первое, как было: пример в таком
    случае всё равно не про это слово, и выбирать не из чего.

    Сравнение по основе, а не по точному совпадению: «рыба» и «рыбу» — одно
    слово, «Haus» и «Häuser» тоже. Если строгое сравнение не нашло ничего,
    пробуется поблажка на одну букву — см. `_stem_in_loose`, там же почему
    она применяется только при однозначном попадании.
    """
    full = word_text(word, code)
    if not full:
        return full

    parts = [p.strip() for p in _VARIANT_SPLIT_RE.split(full) if p.strip()]
    if len(parts) < 2:
        return full

    example = example_text(word, code)
    if not example:
        return parts[0]

    tokens = [fold(t) for t in _TOKEN_RE.findall(example)]

    def head_of(part: str) -> str:
        # У многословного значения проверяем самое длинное слово: в «leczenie
        # sanatoryjne» опознавать надо по «sanatoryjne», а не по «leczenie»
        words = sorted(_TOKEN_RE.findall(part), key=len, reverse=True)
        return words[0] if words else ""

    # Выбирается ЛУЧШЕЕ совпадение, а не первое по списку: иначе ранний
    # неточный вариант затеняет поздний точный. Замерено — «часто» против
    # «частенько» в `öfters`, «morale» против «moralność», «zehirli» против
    # «zehirlenmiş»: во всех случаях пример содержит слово ровно, а
    # показывалось соседнее. Ключ сортировки — (остаток основы, место в
    # списке), поэтому при равной точности порядок ячейки по-прежнему решает.
    scored = []
    for index, part in enumerate(parts):
        head = head_of(part)
        if not head:
            continue
        tail = _stem_tail(head, tokens, whole_letter=not part.startswith("-"))
        if tail is not None:
            # При равном хвосте короткое значение, стоящее в примере отдельным
            # словом, важнее совпавшего началом: «na» в «na zahradě», а не
            # «ve» в «ven». Только для одной-двух букв: на длинных словах
            # выбор формы решается порядком в ячейке, а не правилом
            whole = len(fold(head)) > 2 or fold(head) in tokens
            scored.append((tail, not whole, index, part))

    strict = sorted(t for t in scored if t[0] <= _TAIL_STRICT)
    if strict:
        return strict[0][3]

    # Строгое сравнение не нашло ничего. Тогда разрешается длинный хвост:
    # в славянском и турецком инфинитив длиннее общей со формой основы
    # больше чем на три буквы («одеваться» против «одеваюсь», «masayı
    # toplamak» против «topluyorum»), и строгое правило объявляло их
    # разными словами. Порог 5 замерен: на 4 закрывается 14 из 19 известных
    # случаев, на 5 — все 19, на 6 и 7 не добавляется ни одного.
    long_tail = sorted(t for t in scored if t[0] <= _TAIL_LOOSE)
    if long_tail:
        return long_tail[0][3]

    # Поблажка на одну букву для коротких слов решает только тогда, когда
    # под неё подходит ровно одно значение: иначе выбирать не из чего.
    loose = [p for p in parts if head_of(p) and _stem_in_loose(head_of(p), tokens)]
    if len(loose) == 1:
        return loose[0]
    return parts[0]


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
            # Элизия пишется слитно: «l'uomo», «l'homme» — без пробела
            prefix = p if p.endswith("'") else f"{p} "
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
        """Короткое «изучаемый → значение» для статистики и настроек."""
        return pair_label(self)

    def flipped(self) -> "LanguagePair":
        """
        Та же пара в обратную сторону.

        Нужна пятой игре: она спрашивает значением, а отвечают словом
        изучаемого языка. Новый объект, а не правка поля: пара ходит по
        коду как значение, и менять её на месте значило бы развернуть
        вопрос у всех, кто держит ссылку.
        """
        return LanguagePair(
            learning=self.learning, native=self.native,
            reverse=not self.reverse,
        )


def pair_for_channel(pair: "LanguagePair", channel) -> "LanguagePair":
    """
    Пара языков для вопроса ЭТИМ каналом.

    Направление перестало быть настройкой человека и стало свойством игры:

        карточка       слово → значение
        припоминание   значение → слово      (пятая игра, `QuizChannel.REVERSE`)
        на слух        звук слова → значение
        вслух          слово → произнести

    СЛУХ И РЕЧЬ НЕ ПЕРЕВОРАЧИВАЮТСЯ. У вопроса на слух самого слова на
    экране нет, его заменяет звук на изучаемом языке, — «обратный слух»
    означал бы «услышь немецкое слово и выбери немецкое», то есть вопрос
    без вопроса. Речь и так производство: там показано слово, а ответ
    голосом.

    Функция одна на весь проект нарочно: её спрашивают и сборка вопроса, и
    показ карточки, и разбор ответа. Разойдись они — задание окажется на
    одном языке, а варианты на другом, и человек не поймёт, что от него
    хотят.
    """
    from app.database.enums import QuizChannel

    if channel is QuizChannel.REVERSE:
        return pair if pair.reverse else pair.flipped()
    # Остальные каналы идут В ПРЯМУЮ сторону, даже если у человека
    # осталась включённой прежняя настройка обратного перевода
    return pair.flipped() if pair.reverse else pair


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

    # ПРЕЖНЯЯ НАСТРОЙКА ОБРАТНОГО ПЕРЕВОДА БОЛЬШЕ НЕ ЧИТАЕТСЯ. Реверс стал
    # пятой игрой (706ee78), направление — свойство игры, а не человека. Но
    # у 10 человек колонка `reverse_mode` осталась включённой, и пара у них
    # переворачивалась везде, где код не шёл через `pair_for_channel`:
    # повтор ошибок показывал слово в одну сторону, а варианты в другую,
    # доска стояла задом наперёд, занятие писалось как `is_reverse`.
    # Колонка оставлена в схеме ради истории, но в пару не идёт.
    return LanguagePair(learning=learning, native=native, reverse=False)


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
    LOWERCASE_IN_TEXT = {"ru", "uk", "pl", "it", "es", "fr", "cs"}

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


def language_word(code: Optional[str], interface_lang: Optional[str] = None) -> str:
    """
    Название языка СЛОВОМ, без флага.

    По решению владельца языки в боте обозначаются словами, а не флагами:
    флаг работал тремя разными способами на трёх экранах («🏴 Русский» в
    выборе, «🇩🇪 Немецкий → 🏴» в заголовке занятия, где второй язык вообще
    без названия, и четыре флага на одной короткой карточке).

    Флаг снимается здесь, а не выписыванием названий заново: названия уже
    живут в локалях (`langname_*`), и второй список разъехался бы с первым.
    Когда флаги уйдут из самих значений, снимать станет нечего — и код не
    сломается.

    Прежде такой же помощник лежал приватной копией в админке; это один
    смысл в двух местах, и первая же правка названий развела бы их.
    """
    if not code:
        return ""
    if code not in LANGUAGES:
        return code

    from app.locales import get_text

    name = get_text(language_name_key(code), interface_lang)
    for index, char in enumerate(name):
        if char.isalpha():
            return name[index:]
    return code


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
