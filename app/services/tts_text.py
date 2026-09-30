"""
Подготовка текста к синтезу речи.

Синтезатор читает не то, что видит человек. «1990» он может произнести по
одной цифре, «z.B.» — по буквам, а гетероним прочтёт в одном из значений и
не обязательно в нужном. Здесь текст с экрана превращается в текст для
движка; на экране при этом ничего не меняется.

Проверено на живом движке: edge-tts не понимает SSML — тег phoneme он
зачитывает вслух как обычный текст (обычное «modern» даёт 11 КБ, оно же в
теге — 36 КБ). Значит задать чтение фонетической разметкой невозможно, и
единственный доступный способ управлять произношением — менять сам текст.

Разбор предполётной проверки базы (app/scripts/tts_preflight.py): под риском
954 слова из 53 190. Из них 840 лечатся правилами отсюда детерминированно,
114 — гетеронимы, которым нужен контекст.
"""

from __future__ import annotations

import re
from typing import Optional

from app.services.language_service import get_language

# ============================================================================
# СОКРАЩЕНИЯ
# ============================================================================

# Движок читает сокращение с точкой по буквам: «z.B.» звучит как «цет бе».
# Список закрытый и проверяемый глазами — в базе таких мест 113.
ABBREVIATIONS: dict[str, dict[str, str]] = {
    "de": {
        "z.B.": "zum Beispiel",
        "z. B.": "zum Beispiel",
        "usw.": "und so weiter",
        "bzw.": "beziehungsweise",
        "d.h.": "das heißt",
        "d. h.": "das heißt",
        "u.a.": "unter anderem",
        "ca.": "circa",
        "bspw.": "beispielsweise",
        "evtl.": "eventuell",
        "inkl.": "inklusive",
        "vgl.": "vergleiche",
        "Nr.": "Nummer",
        "Str.": "Straße",
        "Hr.": "Herr",
        "Fr.": "Frau",
        "Dr.": "Doktor",
        "Prof.": "Professor",
        "Abb.": "Abbildung",
        "Jh.": "Jahrhundert",
        "Mio.": "Millionen",
        "Mrd.": "Milliarden",
    },
    "en": {
        "e.g.": "for example",
        "i.e.": "that is",
        "etc.": "et cetera",
        "vs.": "versus",
        "Mr.": "Mister",
        "Mrs.": "Missus",
        "Ms.": "Miz",
        "Dr.": "Doctor",
        "Prof.": "Professor",
        "St.": "Street",
        "No.": "Number",
        "approx.": "approximately",
        "incl.": "including",
        "cf.": "compare",
    },
    "pl": {
        "np.": "na przykład",
        "itd.": "i tak dalej",
        "itp.": "i tym podobne",
        "tzn.": "to znaczy",
        "tj.": "to jest",
        "ok.": "około",
        "nr": "numer",
        "ul.": "ulica",
        "dr": "doktor",
        "prof.": "profesor",
        "godz.": "godzina",
        "tys.": "tysięcy",
        "mln": "milionów",
    },
    "ru": {
        "т.е.": "то есть",
        "т.д.": "так далее",
        "т.п.": "тому подобное",
        "и т.д.": "и так далее",
        "напр.": "например",
        "ул.": "улица",
        "г.": "год",
        "др.": "другие",
        "см.": "смотри",
        "стр.": "страница",
    },
    "uk": {
        "т.д.": "так далі",
        "т.п.": "тому подібне",
        "напр.": "наприклад",
        "вул.": "вулиця",
        "р.": "рік",
        "ін.": "інші",
        "див.": "дивись",
        "стор.": "сторінка",
    },
    "tr": {
        "vb.": "ve benzeri",
        "vs.": "vesaire",
        "örn.": "örneğin",
        "yy.": "yüzyıl",
        "sok.": "sokak",
        "cad.": "cadde",
        "Dr.": "Doktor",
        "Prof.": "Profesör",
    },
}


# ============================================================================
# ЧИСЛА
# ============================================================================

# Разворот чисел в слова снимает неоднозначность целиком: движку больше
# нечего угадывать. Числа в базе небольшие — годы и бытовые количества,
# поэтому хватает диапазона до 9999 без общего алгоритма на все случаи.

_ONES = {
    "de": ["null", "eins", "zwei", "drei", "vier", "fünf", "sechs", "sieben",
           "acht", "neun", "zehn", "elf", "zwölf", "dreizehn", "vierzehn",
           "fünfzehn", "sechzehn", "siebzehn", "achtzehn", "neunzehn"],
    "en": ["zero", "one", "two", "three", "four", "five", "six", "seven",
           "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen",
           "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"],
    "pl": ["zero", "jeden", "dwa", "trzy", "cztery", "pięć", "sześć", "siedem",
           "osiem", "dziewięć", "dziesięć", "jedenaście", "dwanaście",
           "trzynaście", "czternaście", "piętnaście", "szesnaście",
           "siedemnaście", "osiemnaście", "dziewiętnaście"],
    "ru": ["ноль", "один", "два", "три", "четыре", "пять", "шесть", "семь",
           "восемь", "девять", "десять", "одиннадцать", "двенадцать",
           "тринадцать", "четырнадцать", "пятнадцать", "шестнадцать",
           "семнадцать", "восемнадцать", "девятнадцать"],
    "uk": ["нуль", "один", "два", "три", "чотири", "п'ять", "шість", "сім",
           "вісім", "дев'ять", "десять", "одинадцять", "дванадцять",
           "тринадцять", "чотирнадцять", "п'ятнадцять", "шістнадцять",
           "сімнадцять", "вісімнадцять", "дев'ятнадцять"],
    "tr": ["sıfır", "bir", "iki", "üç", "dört", "beş", "altı", "yedi",
           "sekiz", "dokuz", "on", "on bir", "on iki", "on üç", "on dört",
           "on beş", "on altı", "on yedi", "on sekiz", "on dokuz"],
}

_TENS = {
    "de": ["", "", "zwanzig", "dreißig", "vierzig", "fünfzig", "sechzig",
           "siebzig", "achtzig", "neunzig"],
    "en": ["", "", "twenty", "thirty", "forty", "fifty", "sixty",
           "seventy", "eighty", "ninety"],
    "pl": ["", "", "dwadzieścia", "trzydzieści", "czterdzieści",
           "pięćdziesiąt", "sześćdziesiąt", "siedemdziesiąt",
           "osiemdziesiąt", "dziewięćdziesiąt"],
    "ru": ["", "", "двадцать", "тридцать", "сорок", "пятьдесят",
           "шестьдесят", "семьдесят", "восемьдесят", "девяносто"],
    "uk": ["", "", "двадцять", "тридцять", "сорок", "п'ятдесят",
           "шістдесят", "сімдесят", "вісімдесят", "дев'яносто"],
    "tr": ["", "", "yirmi", "otuz", "kırk", "elli", "altmış",
           "yetmiş", "seksen", "doksan"],
}

_HUNDRED = {
    "de": "hundert", "en": "hundred", "pl": "sto",
    "ru": "сто", "uk": "сто", "tr": "yüz",
}
_THOUSAND = {
    "de": "tausend", "en": "thousand", "pl": "tysiąc",
    "ru": "тысяча", "uk": "тисяча", "tr": "bin",
}

# В немецком, английском и турецком сотни складываются регулярно
# («zweihundert», «two hundred», «iki yüz»), а в славянских языках это
# отдельные слова: не «два сто», а «двести».
_HUNDREDS_IRREGULAR = {
    "ru": ["", "сто", "двести", "триста", "четыреста", "пятьсот",
           "шестьсот", "семьсот", "восемьсот", "девятьсот"],
    "uk": ["", "сто", "двісті", "триста", "чотириста", "п'ятсот",
           "шістсот", "сімсот", "вісімсот", "дев'ятсот"],
    "pl": ["", "sto", "dwieście", "trzysta", "czterysta", "pięćset",
           "sześćset", "siedemset", "osiemset", "dziewięćset"],
}

# «Тысяча» согласуется по числу: 1 тысяча, 2–4 тысячи, 5+ тысяч.
# Ключи — формы для (1, 2–4, 5+).
_THOUSAND_FORMS = {
    "ru": ("тысяча", "тысячи", "тысяч"),
    "uk": ("тисяча", "тисячі", "тисяч"),
    "pl": ("tysiąc", "tysiące", "tysięcy"),
}

# Перед «тысяча» двойка женского рода: «две тысячи», не «два тысячи».
# В польском tysiąc мужского рода, там обычное dwa.
_TWO_BEFORE_THOUSAND = {"ru": "две", "uk": "дві"}

_NUMBER_RE = re.compile(r"\d+")


def _below_hundred(n: int, lang: str) -> str:
    ones, tens = _ONES[lang], _TENS[lang]
    if n < 20:
        return ones[n]
    tens_part, ones_part = divmod(n, 10)
    if ones_part == 0:
        return tens[tens_part]
    # В немецком единицы идут перед десятками: einundzwanzig
    if lang == "de":
        unit = "ein" if ones_part == 1 else ones[ones_part]
        return f"{unit}und{tens[tens_part]}"
    if lang == "en":
        return f"{tens[tens_part]}-{ones[ones_part]}"
    return f"{tens[tens_part]} {ones[ones_part]}"


# Форма единицы перед «тысяча»: «eintausend», а не «einstausend»;
# «тысяча», а не «один тысяча». Пустая строка означает, что единица
# не произносится вовсе.
_ONE_BEFORE_THOUSAND = {
    "de": "ein", "en": "one", "pl": "", "ru": "", "uk": "", "tr": "",
}

# Немецкий и английский читают годы этого диапазона сотнями:
# 1990 — «neunzehnhundertneunzig», «nineteen ninety», а не «одна тысяча…».
# В остальных языках год читается обычным числом.
_YEAR_AS_HUNDREDS = ("de", "en")


def _spell_hundreds(n: int, lang: str) -> str:
    """Сотни с остатком: 250, 900, 101."""
    hundreds, rest = divmod(n, 100)

    irregular = _HUNDREDS_IRREGULAR.get(lang)
    if irregular:
        head = irregular[hundreds]
    elif lang == "de":
        head = _HUNDRED[lang] if hundreds == 1 else f"{_ONES[lang][hundreds]}{_HUNDRED[lang]}"
    else:
        head = _HUNDRED[lang] if hundreds == 1 else f"{_ONES[lang][hundreds]} {_HUNDRED[lang]}"

    if rest == 0:
        return head
    # В немецком всё слитно: neunhundertneunzig
    joiner = "" if lang == "de" else " "
    return f"{head}{joiner}{_below_hundred(rest, lang)}"


def _spell_thousands(thousands: int, lang: str) -> str:
    """«Тысяча» с согласованием: 1 тысяча, 2 тысячи, 5 тысяч."""
    forms = _THOUSAND_FORMS.get(lang)
    if forms:
        if thousands == 1:
            return forms[0]
        if 2 <= thousands <= 4:
            count = _TWO_BEFORE_THOUSAND.get(lang) if thousands == 2 else None
            count = count or _ONES[lang][thousands]
            return f"{count} {forms[1]}"
        return f"{_ONES[lang][thousands]} {forms[2]}"

    if lang == "de":
        one = _ONE_BEFORE_THOUSAND[lang]
        return f"{one}{_THOUSAND[lang]}" if thousands == 1 else (
            f"{_ONES[lang][thousands]}{_THOUSAND[lang]}"
        )

    if thousands == 1:
        one = _ONE_BEFORE_THOUSAND[lang]
        return f"{one} {_THOUSAND[lang]}".strip()
    return f"{_ONES[lang][thousands]} {_THOUSAND[lang]}"


def _spell_number(n: int, lang: str) -> str:
    """
    Число словами. Чтение приблизительное по падежам и родам — задача не
    в грамматической точности, а в том, чтобы движок не читал по цифрам.
    """
    if n < 100:
        return _below_hundred(n, lang)

    if n < 1000:
        return _spell_hundreds(n, lang)

    if n < 10000:
        # Год сотнями: 1100–1999. Числа от 2000 читаются тысячами и там,
        # и там («zweitausendvierundzwanzig», «two thousand twenty-four»).
        if lang in _YEAR_AS_HUNDREDS and 1100 <= n <= 1999:
            hundreds, rest = divmod(n, 100)
            if lang == "de":
                head = f"{_below_hundred(hundreds, lang)}{_HUNDRED[lang]}"
                return head if rest == 0 else f"{head}{_below_hundred(rest, lang)}"
            # По-английски «hundred» звучит только в круглом году:
            # 1900 — «nineteen hundred», 1990 — «nineteen ninety»
            if rest == 0:
                return f"{_below_hundred(hundreds, lang)} {_HUNDRED[lang]}"
            return f"{_below_hundred(hundreds, lang)} {_below_hundred(rest, lang)}"

        thousands, rest = divmod(n, 1000)
        head = _spell_thousands(thousands, lang)
        if rest == 0:
            return head
        tail = _spell_hundreds(rest, lang) if rest >= 100 else _below_hundred(rest, lang)
        return f"{head}{tail}" if lang == "de" else f"{head} {tail}"

    # Больше 9999 в базе не встречается; отдаём как есть, чтобы не
    # придумывать чтение вслепую
    return str(n)


# ============================================================================
# ГЕТЕРОНИМЫ
# ============================================================================

# Одно написание, разное чтение по смыслу. Движок выбирает чтение сам, и без
# контекста ошибается примерно в половине случаев. Управлять этим фонетикой
# нельзя — SSML недоступен. Единственный работающий приём: не озвучивать такое
# слово изолированно, а дать его внутри примера, где смысл задан однозначно.
#
# Список тот же, что в предполётной проверке. Немецкий 11 слов, английский 103.
NEEDS_CONTEXT: dict[str, frozenset[str]] = {
    "de": frozenset({
        "umfahren", "umschreiben", "umstellen", "übersetzen", "durchschauen",
        "modern", "montage", "tenor", "august", "weckglas", "hochzeit",
        "umgehen", "durchsetzen", "übergehen", "ausführen",
    }),
    "en": frozenset({
        "read", "lead", "live", "bow", "tear", "close", "record", "present",
        "object", "desert", "minute", "wind", "wound", "row", "sow", "bass",
        "content", "contract", "refuse", "produce", "progress", "project",
        "rebel", "subject", "conduct", "console", "contest", "convert",
        "escort", "excuse", "export", "import", "insult", "permit", "perfect",
        "polish", "separate", "use", "abuse", "house", "estimate", "moderate",
        "number", "does", "dove", "entrance", "invalid", "lima", "mobile",
        "resume", "second", "sewer", "slough", "supply", "tier",
    }),
}


def needs_context(word: str, lang: Optional[str]) -> bool:
    """
    Прочитается ли слово неоднозначно, если озвучить его отдельно.

    Для таких слов в вопросе ставится клип с примером вместо изолированного
    слова: контекст задаёт чтение, и ошибиться движку уже негде.
    """
    if not word:
        return False
    bare = word.strip().lower()
    # Артикль на неоднозначность не влияет, но мешает сравнению
    particles = get_language(lang).leading_particles
    for p in particles:
        if bare.startswith(f"{p} "):
            bare = bare[len(p) + 1:].strip()
            break
    return bare in NEEDS_CONTEXT.get(lang or "", frozenset())


# ============================================================================
# ГЛАВНОЕ
# ============================================================================

# Многозначный перевод хранится через запятую («к, в, на, слишком»). Озвучивать
# перечисление значений бессмысленно: учат слово, а не список. Берём первое.
_VARIANT_SPLIT = re.compile(r"\s*[,;/]\s*")

# Пометки в скобках — «(разг.)», «(о человеке)» — на экране полезны,
# в звуке это мусор
_PARENTHETICAL = re.compile(r"\s*\([^)]*\)")

_WS = re.compile(r"\s+")


def expand_abbreviations(text: str, lang: Optional[str]) -> str:
    table = ABBREVIATIONS.get(lang or "", {})
    if not table:
        return text
    # Длинные сокращения первыми: «и т.д.» должно сработать раньше «т.д.»
    for short in sorted(table, key=len, reverse=True):
        if short in text:
            text = text.replace(short, table[short])
    return text


def expand_numbers(text: str, lang: Optional[str]) -> str:
    if (lang or "") not in _ONES:
        return text

    def replace(match: re.Match) -> str:
        raw = match.group(0)
        try:
            value = int(raw)
        except ValueError:
            return raw
        if value > 9999:
            return raw
        return _spell_number(value, lang)

    return _NUMBER_RE.sub(replace, text)


def speakable(text: Optional[str], lang: Optional[str], *, first_only: bool = False) -> str:
    """
    Текст, готовый к отправке в синтезатор.

    first_only — оставить только первое значение из перечисления. Нужно для
    слова: озвучивать «к, в, на, слишком» вместо слова незачем. Для примера
    False: там запятая — часть фразы.
    """
    if not text:
        return ""

    result = str(text).strip()
    if first_only:
        result = _VARIANT_SPLIT.split(result)[0].strip()

    result = _PARENTHETICAL.sub("", result)
    result = expand_abbreviations(result, lang)
    result = expand_numbers(result, lang)
    result = _WS.sub(" ", result).strip()

    return result


# Пауза между словом и примером в одном клипе. Многоточие движок отрабатывает
# как паузу, и слово не слипается с началом фразы.
PAUSE = " … "


def word_clip_text(word: str, lang: Optional[str]) -> str:
    """Что произносится в клипе «только слово»."""
    return speakable(word, lang, first_only=True)


def full_clip_text(word: str, example: Optional[str], lang: Optional[str]) -> str:
    """
    Что произносится в клипе «слово и пример».

    Слово идёт первым: сначала то, что учат, потом оно же в живой речи.
    """
    spoken_word = word_clip_text(word, lang)
    spoken_example = speakable(example, lang)
    if not spoken_example:
        return spoken_word
    if not spoken_word:
        return spoken_example
    return f"{spoken_word}{PAUSE}{spoken_example}"
