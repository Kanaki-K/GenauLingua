"""
🧱 «Собираю» — шестая игра: собрать пример из кнопок-слов.

ЗАМЫСЕЛ ВЛАДЕЛЬЦА, дословно: «У нас есть пример — предложение. Показываем
его на родном языке, а человек тыкает в сетку слов и в правильном порядке
собирает предложение на изучаемом. Отправляет. Если верно — показывает
"верно"; если нет — показывает, в чём именно ошибка». И ещё: «хотелось бы
ещё круче сделать».

«КРУЧЕ» — ЭТО СЛОВА-ЛОВУШКИ. Если кнопок ровно столько, сколько слов,
последнее слово достаётся даром, а предпоследнее — монеткой: та же беда,
что у доски. Поэтому к словам примера добавляются 2–4 лишних — и не
случайных, а тех, что ловят ГРАММАТИКУ: к «der» — «den» и «dem», к «wir»
— «ihr», к «ist» — «sind». Человек, который знает слова, но не формы,
соберёт «Nach den Essen» и увидит ровно это место.

Здесь только ЧИСТАЯ ЛОГИКА: годность примера, слова-ловушки, сетка,
сравнение. Нажатия и экраны — в `app/bot/handlers/quiz/build.py`. Отделено
затем, чтобы правила проверялись без бота и без базы (кроме чужих
примеров — им база нужна).

ЧЕГО ЗДЕСЬ НЕТ НАРОЧНО: генерации словоформ. Ловушки берутся только из
закрытых списков по языкам (артикли, местоимения, формы «быть», частые
предлоги) и из чужих примеров. Склонять и спрягать на лету — значит
однажды предложить несуществующую форму и учить ей.
"""

from __future__ import annotations

import collections
import random
from dataclasses import dataclass, field
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.enums import CEFRLevel
from app.services.language_service import (
    LanguagePair, example_column, example_text, fold, upper_first,
)

# Сколько слов в примере, чтобы его можно было собирать. Пунктуация в счёт
# не идёт. Меньше трёх — не фраза, а пара слов, и порядок в ней угадывается;
# больше десяти — с ловушками кнопок станет больше двенадцати, и сетка не
# влезет в экран телефона. Замер по базе: у немецкого 4–8 слов в 81%
# примеров, больше двенадцати — ни одного.
MIN_WORDS = 3
MAX_WORDS = 10

# Сколько кнопок-слов самое большее. Двенадцать — это три ряда по четыре
# или четыре по три: больше — и сетка вместе с текстом вопроса уже не
# помещается на экране телефона без прокрутки.
MAX_TILES = 12

# ЛЕСТНИЦА ТРУДНОСТИ: сколько слов-ловушек по уровню слова (`Word.level`).
#
# Владелец: «многие примеры A1 реально простые». Замер dev-базы, немецкий:
#
#     уровень   медиана слов   примеров ≤4 слов   с запятой
#       A1           4               55%              4%
#       A2           5               40%              —
#       B1           6               22%              8%
#       B2           7                6%             12%
#       C1           7                2%             15%
#       C2           7                2%             17%
#
# Длина фразы растёт до B2 и дальше стоит на семи, значит трудность выше
# B2 может дать только число ловушек. «Der Baum ist grün» без ловушек —
# четыре кнопки и порядок, который угадывается; с двумя близнецами («Die»,
# «sind») уже надо знать род и число. Английский идёт почти так же.
#
# Всего кнопок не больше `MAX_TILES`: у длинной фразы ловушек меньше, но
# не меньше одной — без неё последнее слово достаётся даром.
LEVEL_DISTRACTORS: dict[CEFRLevel, int] = {
    CEFRLevel.A1: 2,
    CEFRLevel.A2: 3,
    CEFRLevel.B1: 3,
    CEFRLevel.B2: 4,
    CEFRLevel.C1: 5,
    CEFRLevel.C2: 5,
}
MIN_DISTRACTORS = 1
MAX_DISTRACTORS = max(LEVEL_DISTRACTORS.values())

# Ширина сетки. В ряд по четыре на телефоне влезает слово около семи букв;
# длиннее — по три (около одиннадцати), ещё длиннее — по два. Решение по
# самому длинному слову ряда, а не всей сетки, разлиновало бы её в разнобой,
# и одно и то же слово прыгало бы между рядами разной ширины.
ROW_FOUR_UP_TO = 7
ROW_THREE_UP_TO = 11

# Чем обрамлена фраза и что ей не принадлежит. Внутренние знаки остаются:
# «don't», «Ali'nin», «E-Mail», «проб'є» — одно слово, а не три.
_EDGE_PUNCT = ".,!?;:…\"'«»„“”‚‘’()[]{}—–-¿¡*/"


# ============================================================================
# ЗАКРЫТЫЕ СПИСКИ: из них берутся слова-ловушки
# ============================================================================
#
# ГРУППЫ — это слова, которые путают ДРУГ С ДРУГОМ: формы одного артикля,
# падежи одного местоимения, лица одного глагола. Слово примера, найденное
# в группе, даёт ловушки из соседей по ней: к «der» — «den», «dem». Одно
# слово может стоять в нескольких группах («ihr» — и «вы», и «её»): тогда
# соседи берутся из всех.
#
# Списки маленькие нарочно. Это не словарь форм, а то, на чём изучающий
# спотыкается чаще всего; полнота тут не цель, цель — чтобы каждое
# предложенное слово существовало и было правдоподобным.
#
# Формы на «ты» здесь — СЛОВА ЯЗЫКА, а не обращение к человеку: правило
# «только на Вы» относится к тому, как бот говорит с ним, а «du»/«ты» в
# ловушке — то, что он должен уметь отличить.
SIBLINGS: dict[str, tuple[tuple[str, ...], ...]] = {
    "de": (
        ("der", "die", "das", "den", "dem", "des"),
        ("ein", "eine", "einen", "einem", "einer", "eines"),
        ("kein", "keine", "keinen", "keinem", "keiner"),
        ("ich", "du", "er", "sie", "es", "wir", "ihr"),
        ("mich", "mir"), ("dich", "dir"), ("ihn", "ihm"), ("uns", "euch"),
        ("mein", "meine", "meinen", "meinem", "meiner"),
        ("dein", "deine", "deinen", "deinem", "deiner"),
        ("sein", "seine", "seinen", "seinem", "seiner"),
        ("ihr", "ihre", "ihren", "ihrem", "ihrer"),
        ("unser", "unsere", "unseren", "unserem", "unserer"),
        ("dieser", "diese", "dieses", "diesen", "diesem"),
        ("bin", "bist", "ist", "sind", "seid"),
        ("war", "warst", "waren", "wart"),
        ("habe", "hast", "hat", "haben", "habt"),
        ("hatte", "hattest", "hatten"),
        ("werde", "wirst", "wird", "werden", "werdet"),
        ("wurde", "wurden"),
        ("kann", "kannst", "können"), ("muss", "musst", "müssen"),
        ("will", "willst", "wollen"),
        ("in", "im", "ins"), ("an", "am", "ans"), ("zu", "zum", "zur"),
        ("von", "vom"), ("bei", "beim"),
        ("in", "an", "auf"), ("mit", "bei"), ("aus", "von"), ("nach", "zu"),
        ("über", "unter"), ("vor", "hinter"), ("für", "gegen"),
        ("dass", "das"), ("weil", "denn"), ("wenn", "wann", "als", "ob"),
        ("nicht", "nichts"),
    ),
    "en": (
        ("a", "an", "the"),
        ("I", "me", "my", "mine"),
        ("you", "your", "yours"),
        ("he", "him", "his"),
        ("she", "her", "hers"),
        ("it", "its"),
        ("we", "us", "our"),
        ("they", "them", "their"),
        ("am", "is", "are", "was", "were", "be", "been"),
        ("have", "has", "had"),
        ("do", "does", "did"),
        ("this", "that", "these", "those"),
        ("in", "on", "at"), ("to", "for", "of"), ("from", "with", "by"),
        ("can", "could"), ("will", "would"), ("shall", "should"),
        ("some", "any"), ("much", "many"),
        ("who", "which", "what"),
    ),
    "ru": (
        ("я", "меня", "мне", "мной"),
        ("ты", "тебя", "тебе", "тобой"),
        ("он", "его", "ему", "него", "нему"),
        ("она", "её", "ей", "неё", "ней"),
        ("мы", "нас", "нам", "нами"),
        ("вы", "вас", "вам", "вами"),
        ("они", "их", "им", "ними"),
        ("был", "была", "было", "были", "будет"),
        ("мой", "моя", "моё", "мои", "моего", "моей"),
        ("твой", "твоя", "твоё", "твои"),
        ("наш", "наша", "наше", "наши"),
        ("ваш", "ваша", "ваше", "ваши"),
        ("свой", "своя", "своё", "свои", "своего", "своей"),
        ("этот", "эта", "это", "эти", "этого", "этой"),
        ("тот", "та", "то", "те"),
        ("в", "во", "на"), ("с", "со", "из", "от"), ("к", "по"),
        ("о", "об", "про"),
        ("не", "ни"),
        ("весь", "вся", "всё", "все"),
        ("который", "которая", "которое", "которые"),
        ("что", "чтобы"),
    ),
    "uk": (
        ("я", "мене", "мені", "мною"),
        ("ти", "тебе", "тобі", "тобою"),
        ("він", "його", "йому", "нього"),
        ("вона", "її", "їй", "неї"),
        ("ми", "нас", "нам", "нами"),
        ("ви", "вас", "вам", "вами"),
        ("вони", "їх", "їм", "ними"),
        ("був", "була", "було", "були", "буде"),
        ("мій", "моя", "моє", "мої", "мого", "моєї"),
        ("твій", "твоя", "твоє", "твої"),
        ("наш", "наша", "наше", "наші"),
        ("ваш", "ваша", "ваше", "ваші"),
        ("свій", "своя", "своє", "свої", "свого", "своєї"),
        ("цей", "ця", "це", "ці", "цього", "цієї"),
        ("той", "та", "те", "ті"),
        ("в", "у", "на"), ("з", "із", "зі", "від"), ("до", "по"),
        ("про", "о"),
        ("не", "ні"),
        ("весь", "вся", "все", "всі"),
        ("який", "яка", "яке", "які"),
        ("що", "щоб"),
    ),
    "pl": (
        ("ja", "mnie", "mi", "mną"),
        ("ty", "ciebie", "cię", "ci", "tobie"),
        ("on", "jego", "go", "jemu", "mu"),
        ("ona", "jej", "ją", "nią"),
        ("my", "nas", "nam", "nami"),
        ("wy", "was", "wam", "wami"),
        ("oni", "one", "ich", "im"),
        ("jest", "są", "jestem", "jesteś", "jesteśmy"),
        ("był", "była", "było", "byli", "były", "będzie"),
        ("mam", "masz", "ma", "mamy", "macie", "mają"),
        ("mój", "moja", "moje", "moi", "mojego", "mojej"),
        ("twój", "twoja", "twoje", "twoi"),
        ("nasz", "nasza", "nasze", "nasi"),
        ("swój", "swoja", "swoje", "swojego", "swojej"),
        ("ten", "ta", "to", "te", "tego", "tej"),
        ("w", "we", "na"), ("z", "ze", "od"), ("do", "dla"),
        ("o", "po", "przez"),
        ("nie", "ani"),
        ("się", "sobie"),
        ("który", "która", "które", "którzy"),
        ("że", "żeby"),
    ),
    "tr": (
        ("ben", "beni", "bana", "benim"),
        ("sen", "seni", "sana", "senin"),
        ("o", "onu", "ona", "onun"),
        ("biz", "bizi", "bize", "bizim"),
        ("siz", "sizi", "size", "sizin"),
        ("onlar", "onları", "onlara", "onların"),
        ("bu", "şu", "o"),
        ("bir", "birkaç"),
        ("ve", "ile", "veya"),
        ("için", "gibi", "kadar"),
        ("çok", "daha", "en"),
        ("değil", "yok", "var"),
        ("ne", "neden", "nasıl"),
        ("her", "hiç"),
    ),
}

# ВЗАИМОЗАМЕНЯЕМЫЕ: слова, которые в той же фразе часто ОБА верны. Ловушкой
# друг к другу они быть не могут — иначе человек соберёт правильную фразу,
# а бот, знающий один эталон, засчитает ошибку. Это хуже, чем отсутствие
# ловушки: игра учила бы неправде.
#
#   uk  в/у, з/із/зі — чередование для благозвучия, верны оба
#   en  a/the, this/that — с русского или немецкого не определить, какой
#       артикль или указатель стоит в эталоне; can/could и подобные —
#       вежливая и прямая форма просьбы равно верны
#   de  aus/von («aus/von der Arbeit»), weil/denn (порядок слов после них
#       разный, но кнопки те же — соберётся и так, и так), als/wenn
#   pl  краткие и полные формы местоимений: mi/mnie, cię/ciebie, go/jego
#   tr  bu/şu («это»), ve/ile («и»/«с» при перечислении)
#
# Отсев действует на ВСЕ источники ловушек, а не только на соседей: иначе
# «von» пришло бы к «aus» случайным словом из закрытого списка.
EQUIVALENT: dict[str, tuple[tuple[str, ...], ...]] = {
    "de": (("aus", "von"), ("weil", "denn"), ("als", "wenn")),
    "en": (("a", "the"), ("an", "the"), ("this", "that"), ("these", "those"),
           ("can", "could"), ("will", "would"), ("shall", "should"),
           ("some", "any"), ("which", "what")),
    "ru": (),
    "uk": (("в", "у"), ("з", "із", "зі")),
    "pl": (("mnie", "mi"), ("cię", "ciebie"), ("ci", "tobie"),
           ("go", "jego"), ("mu", "jemu")),
    "tr": (("bu", "şu"), ("ve", "ile")),
}

# Слова, у которых регистр — часть написания, а не место в предложении:
# английское «I» строчным не бывает
_ALWAYS_UPPER = {"I"}


def _closed_list(lang: str) -> list[str]:
    """Все слова закрытых списков языка, без повторов, в постоянном порядке."""
    return list(dict.fromkeys(w for group in SIBLINGS.get(lang, ()) for w in group))


# ============================================================================
# ГОДНОСТЬ ПРИМЕРА
# ============================================================================

def tokens(sentence: str) -> list[str]:
    """
    Слова фразы — то, что станет кнопками. Пунктуация по краям слова
    отбрасывается, слово из одной пунктуации («—») пропадает целиком.
    Регистр — как в предложении; первое слово из закрытых списков на
    кнопке потом станет строчным (`first_on_tile`), чтобы не выдать начало.
    """
    out = []
    for raw in (sentence or "").split():
        word = raw.strip(_EDGE_PUNCT)
        if word:
            out.append(word)
    return out


def sentence_tokens(word, pair: LanguagePair) -> Optional[list[str]]:
    """
    Слова примера на ИЗУЧАЕМОМ языке, если пример годится для сборки.

    Годен, когда в нём от `MIN_WORDS` до `MAX_WORDS` слов и есть его
    перевод на родной язык человека — то, что показывается вопросом. Без
    перевода собирать нечего: задания нет.

    Перевод бывает не дословным, и это не мешает: эталон — фраза на
    изучаемом языке, а перевод лишь говорит, ЧТО собрать.
    """
    if not example_text(word, pair.native):
        return None
    found = tokens(example_text(word, pair.learning))
    if not MIN_WORDS <= len(found) <= MAX_WORDS:
        return None
    return found


def fits(word, pair: LanguagePair) -> bool:
    """Можно ли спросить это слово сборкой. Одно правило для всего бота."""
    return sentence_tokens(word, pair) is not None


def sql_prefilter(pair: LanguagePair) -> tuple:
    """
    Дешёвый предварительный отсев в базе: оба примера не пусты. Число слов
    в SQL не выразить честно (пунктуация, «—» отдельным словом), поэтому
    решает `fits` уже в Python.
    """
    learning_col = example_column(pair.learning)
    native_col = example_column(pair.native)
    return (
        learning_col.isnot(None), func.btrim(learning_col) != "",
        native_col.isnot(None), func.btrim(native_col) != "",
    )


# ============================================================================
# СЛОВА-ЛОВУШКИ
# ============================================================================

def _lower(word: str, lang: str) -> str:
    """
    Строчными — по правилам языка: турецкие «I»/«İ» становятся «ı»/«i»,
    а не «i»/«i̇», как у питоновского `.lower()`.
    """
    if lang == "tr":
        word = word.replace("I", "ı").replace("İ", "i")
    return word.lower()


def _like(source: str, candidate: str, lang: str) -> str:
    """
    Ловушка в РЕГИСТРЕ слова, которое она подменяет.

    «Der» в начале фразы даёт «Den», а не «den»: иначе строчная кнопка
    подсказывала бы, что на первое место она не годится, — и ловушка не
    ловила бы ничего.
    """
    if candidate in _ALWAYS_UPPER:
        return candidate
    if source[:1].isupper() and source not in _ALWAYS_UPPER:
        return upper_first(candidate, lang)
    return candidate


def _siblings(token: str, lang: str) -> list[str]:
    """Соседи слова по закрытым спискам: с кем его путают."""
    low = _lower(token, lang)
    out: list[str] = []
    for group in SIBLINGS.get(lang, ()):
        if low in (_lower(w, lang) for w in group):
            out.extend(w for w in group if _lower(w, lang) != low)
    return list(dict.fromkeys(out))


def distractor_count(words: int, level: Optional[CEFRLevel] = None) -> int:
    """
    Сколько ловушек положено фразе из `words` слов этого уровня — по
    лестнице `LEVEL_DISTRACTORS`; уровень неизвестен — как у B1.
    """
    want = LEVEL_DISTRACTORS.get(level, LEVEL_DISTRACTORS[CEFRLevel.B1])
    return max(MIN_DISTRACTORS, min(want, MAX_TILES - words))


def first_on_tile(target: list[str], lang: str) -> list[str]:
    """
    Слова фразы так, как они стоят НА КНОПКАХ: первое — строчным, если оно
    из закрытых списков (артикль, местоимение, предлог, союз).

    Заглавная иначе подсказывала бы начало: «Der» с большой буквы среди
    «die», «den» сразу говорит, что ему стоять первым, — и выбор артикля,
    ради которого ловушки и ставятся, пропадает. Остальные первые слова не
    трогаются: немецкое существительное пишется с большой всегда, это часть
    грамматики, а не место во фразе; имя собственное строчным стало бы
    ошибкой. Английское «I» строчным не бывает.

    Проверка регистр первого слова не сравнивает (`judge`), а эталон на
    итоге показывается фразой из базы — с правильной заглавной.
    """
    if not target or target[0] in _ALWAYS_UPPER:
        return list(target)
    closed = {fold(w) for w in _closed_list(lang)}
    if fold(target[0]) not in closed:
        return list(target)
    return [_lower(target[0], lang), *target[1:]]


def pick_distractors(
    target: list[str], lang: str, foreign: list[str],
    rng: Optional[random.Random] = None, count: Optional[int] = None,
) -> tuple[list[str], dict[str, int]]:
    """
    Слова-ловушки и откуда они взяты.

    ПОРЯДОК ИСТОЧНИКОВ — от самой коварной ловушки к самой простой:

        похожие   соседи слов фразы по закрытым спискам: der → den, dem
        список    любые слова закрытых списков языка
        чужие     слова из других примеров того же уровня (`foreign`)

    Похожие берутся ПО КРУГУ от разных слов фразы, а не все от одного:
    четыре формы артикля ловят одно место, а четыре ловушки к четырём
    разным словам — всю фразу.

    НИ ОДНА ЛОВУШКА НЕ СОВПАДАЕТ СО СЛОВОМ ФРАЗЫ — ни буквой, ни регистром,
    ни диакритикой (сравнение через `fold`). Иначе две одинаковые на вид
    кнопки сделали бы проверку неоднозначной: человек нажал «правильную»
    «den», а засчиталась бы не та. По той же причине ловушки не повторяют
    друг друга.
    """
    rng = rng or random
    if count is None:
        count = distractor_count(len(target))

    taken = {fold(t) for t in target}
    # Взаимозаменяемые со словами фразы — тоже под запретом (см. EQUIVALENT)
    for group in EQUIVALENT.get(lang, ()):
        keys = {fold(w) for w in group}
        if keys & taken:
            taken |= keys
    picked: list[str] = []
    sources = collections.Counter()

    def take(word: str, source: str) -> bool:
        key = fold(word)
        if not key or key in taken:
            return False
        taken.add(key)
        picked.append(word)
        sources[source] += 1
        return True

    # 1. ПОХОЖИЕ — по кругу от разных слов фразы
    pools = []
    for token in target:
        options = [_like(token, s, lang) for s in _siblings(token, lang)]
        options = [o for o in options if fold(o) not in taken]
        if options:
            rng.shuffle(options)
            pools.append(options)
    rng.shuffle(pools)
    while len(picked) < count and any(pools):
        for pool in pools:
            while pool and len(picked) < count:
                if take(pool.pop(), "similar"):
                    break

    # 2. ЛЮБЫЕ СЛОВА ЗАКРЫТЫХ СПИСКОВ
    if len(picked) < count:
        closed = _closed_list(lang)
        rng.shuffle(closed)
        for word in closed:
            if len(picked) >= count:
                break
            take(word, "closed")

    # 3. ЧУЖИЕ ПРИМЕРЫ ТОГО ЖЕ УРОВНЯ
    if len(picked) < count:
        pool = list(foreign)
        rng.shuffle(pool)
        for word in pool:
            if len(picked) >= count:
                break
            take(word, "foreign")

    return picked, dict(sources)


async def foreign_words(
    session: AsyncSession, word, pair: LanguagePair, limit: int = 8,
) -> list[str]:
    """
    Слова из чужих примеров того же уровня — последний запас ловушек.

    Первое слово чужой фразы не берётся: оно с заглавной лишь потому, что
    стоит первым, и в середине чужой сборки выдавало бы себя регистром.
    Слишком длинные — тоже: они расширили бы сетку ради ловушки.
    """
    from app.database.models import Word

    column = example_column(pair.learning)
    rows = (await session.execute(
        select(column)
        .where(Word.id != word.id, Word.level == word.level,
               column.isnot(None), func.btrim(column) != "")
        .order_by(func.random())
        .limit(limit)
    )).scalars().all()
    out: list[str] = []
    for sentence in rows:
        out.extend(t for t in tokens(sentence)[1:] if 2 <= len(t) <= ROW_THREE_UP_TO)
    return out


# ============================================================================
# ЗАДАЧА ЦЕЛИКОМ
# ============================================================================

@dataclass
class Puzzle:
    """Одна сборка: что собрать, из чего и откуда взялись ловушки."""
    target: list[str]          # слова фразы по порядку — эталон, как на кнопках
    tiles: list[str]           # кнопки в порядке на экране
    distractors: list[str]
    sentence: str              # фраза на изучаемом, с пунктуацией
    translation: str           # она же на родном — это и есть задание
    sources: dict[str, int] = field(default_factory=dict)


def shuffle_tiles(target: list[str], distractors: list[str],
                  rng: Optional[random.Random] = None) -> list[str]:
    """
    Кнопки вперемешку — но НЕ в порядке фразы.

    Случайная перестановка трёх слов с вероятностью 1/6 оставляет их на
    месте, и тогда ответ стоит в первом ряду готовым: нажми подряд.
    Перемешиваем заново, пока начало сетки совпадает с фразой.
    """
    rng = rng or random
    tiles = list(target) + list(distractors)
    for _ in range(50):
        rng.shuffle(tiles)
        if tiles[:len(target)] != list(target):
            return tiles
    # Пятьдесят неудач подряд — только у фразы из одинаковых слов; сдвиг
    # на одну позицию честно ломает порядок, если его вообще можно сломать
    return tiles[1:] + tiles[:1]


async def make_puzzle(
    session: Optional[AsyncSession], word, pair: LanguagePair,
    rng: Optional[random.Random] = None,
) -> Optional[Puzzle]:
    """
    Сборка по примеру слова или None, если пример не годится.

    None — это не поломка, а откат: вызывающий задаёт вопрос другой игрой,
    ровно как слух откатывается в текст без созвучных соседей.
    """
    target = sentence_tokens(word, pair)
    if target is None:
        return None
    # Эталон — В ВИДЕ КНОПОК: первое слово уже строчным, если оно из
    # закрытых списков (`first_on_tile`). Ловушки к нему берутся тоже
    # строчными (`_like`), и ни одна кнопка не выдаёт начало фразы
    target = first_on_tile(target, pair.learning)
    count = distractor_count(len(target), getattr(word, "level", None))

    # Чужие примеры — только если закрытых списков не хватило: запрос к
    # базе на каждую сборку незачем, когда ловушки уже набраны
    distractors, sources = pick_distractors(target, pair.learning, [], rng, count)
    if len(distractors) < count and session is not None:
        foreign = await foreign_words(session, word, pair)
        distractors, sources = pick_distractors(
            target, pair.learning, foreign, rng, count)

    return Puzzle(
        target=target,
        tiles=shuffle_tiles(target, distractors, rng),
        distractors=distractors,
        sentence=example_text(word, pair.learning),
        translation=example_text(word, pair.native),
        sources=sources,
    )


def row_width(tiles: list[str]) -> int:
    """Сколько кнопок в ряд: по самому длинному слову сетки."""
    longest = max((len(t) for t in tiles), default=0)
    if longest <= ROW_FOUR_UP_TO:
        return 4
    if longest <= ROW_THREE_UP_TO:
        return 3
    return 2


# ============================================================================
# СРАВНЕНИЕ
# ============================================================================

@dataclass
class Verdict:
    correct: bool
    same_words: bool                 # слова те же, порядок другой
    marks: list[bool]                # по позиции: слово на своём месте?
    extra: list[str]                 # лишние слова в ответе
    missing: list[str]               # каких слов фразы не хватило


def judge(target: list[str], answer: list[str], lang: str) -> Verdict:
    """
    Сравнить собранное с эталоном — ПО ПОСЛЕДОВАТЕЛЬНОСТИ СЛОВ.

    Пунктуации тут нет вовсе: её нет и на кнопках. Регистр сравнивается
    точно — кроме слова, стоящего первым: «Wir gehen raus» и «Raus gehen
    wir» отличаются порядком, а не тем, что «wir» стало строчным. Поэтому
    всё, что совпадает с первым словом фразы без учёта регистра, сводится
    к строчным с обеих сторон. В немецком регистр значим («Essen» и
    «essen» — разные слова), и прочие слова сравниваются как есть.
    """
    first = _lower(target[0], lang) if target else ""

    def norm(word: str) -> str:
        low = _lower(word, lang)
        return low if low == first else word

    want = [norm(w) for w in target]
    got = [norm(w) for w in answer]
    marks = [i < len(want) and g == want[i] for i, g in enumerate(got)]
    correct = got == want

    extra_c = collections.Counter(got) - collections.Counter(want)
    missing_c = collections.Counter(want) - collections.Counter(got)
    # Лишние — в том виде, в каком их нажал человек, и в его порядке
    extra: list[str] = []
    left = collections.Counter(extra_c)
    for original, key in zip(answer, got):
        if left[key]:
            extra.append(original)
            left[key] -= 1
    missing: list[str] = []
    left = collections.Counter(missing_c)
    for original, key in zip(target, want):
        if left[key]:
            missing.append(original)
            left[key] -= 1

    same = not correct and not extra and not missing
    return Verdict(correct=correct, same_words=same, marks=marks,
                   extra=extra, missing=missing)
