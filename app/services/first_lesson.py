"""
Первый урок: три игры и доска на три пары (решение владельца 16.10).

Прежде первый урок шёл семью карточками подряд — «в первых 7 вопросах в
принципе только один вариант игры, когда можно разнообразить и вовлечь».
Теперь по номеру вопроса:

    1 Читаю    2 Слышу    3 Вспоминаю
    4 Читаю    5 Слышу    6 Вспоминаю
    7 Доска на 3 пары

Каждое слово — новое и лёгкое; ни одно не повторяется (9 слов за урок).
Голоса и «Собираю» в первом уроке нет: самые трудные (у «Собираю» 41%
верных на проде) и требуют микрофона. Владелец: «все игры, просто в самой
лёгкой версии для первого круга… кроме записи голоса и собираю».

ПОЧЕМУ СЛОВА ПОХОЖИЕ НА РОДНЫЕ. Обычное правило допуска пускает слово на
слух и в «Вспоминаю» только после верного ответа глазами: нельзя узнать на
слух то, чего ни разу не видел. Первый урок это правило обходит — и
решаемой игру делает не повтор, а выбор слова: Taxi, Hotel, Kaffee узнаются
и на слух, и по значению. Сходство считается на лету, по пулу частых
лёгких слов: слово и перевод приводятся к одной азбуке и сравниваются.
Не нашлось похожего — на этом месте карточка, а не загадка.
"""
from __future__ import annotations

import difflib
import unicodedata
from typing import Optional

from app.database.enums import QuizChannel

# Игра на каждом номере вопроса; 7-й — доска (`board_slot_for_first_lesson`)
PLAN = (
    QuizChannel.TEXT, QuizChannel.AUDIO, QuizChannel.REVERSE,
    QuizChannel.TEXT, QuizChannel.AUDIO, QuizChannel.REVERSE,
)
BOARD_PAIRS = 3

# Игры, которым нужно слово, похожее на родное
NEEDS_SIMILAR = (QuizChannel.AUDIO, QuizChannel.REVERSE)

# Порог сходства (difflib, 0..1). Замер на парах de→ru/uk/en/pl/tr: от 0.6
# идут Taxi/такси, Hotel/отель, Kaffee/кофе; ниже — случайные совпадения
# букв («Hand»/«рука» даёт 0.0, «Bett»/«кровать» — 0.2)
SIMILAR_ENOUGH = 0.6

# Сколько частых лёгких слов перебирать в поисках похожего
SIMILAR_POOL = 200


def planned_game(question_number: int, enabled: list[QuizChannel]) -> QuizChannel:
    """Игра на этом месте первого урока; выключенная человеком — карточка."""
    if not 1 <= question_number <= len(PLAN):
        return QuizChannel.TEXT
    game = PLAN[question_number - 1]
    return game if game in enabled else QuizChannel.TEXT


def board_slot(lesson_length: int) -> int:
    """Доска первого урока — ПОСЛЕДНИМ вопросом, а не в середине."""
    return lesson_length


# Кириллица → латиница, грубо и нарочно: сравниваются очертания звуков, а
# не правописание. «кофе» → «kofe» рядом с «kaffee», «отель» → «otel»
_CYR = {
    "а": "a", "б": "b", "в": "v", "г": "g", "ґ": "g", "д": "d", "е": "e", "є": "ye",
    "ё": "yo", "ж": "zh", "з": "z", "и": "i", "і": "i", "ї": "yi", "й": "y", "к": "k",
    "л": "l", "м": "m", "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t",
    "у": "u", "ф": "f", "х": "h", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "sch",
    "ъ": "", "ы": "y", "ь": "", "э": "e", "ю": "yu", "я": "ya",
}


def _skeleton(text: str) -> str:
    """Слово в одной азбуке, без знаков, регистра и удвоений."""
    text = text.lower()
    text = "".join(_CYR.get(ch, ch) for ch in text)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if ch.isalpha())
    # «kaffee» и «kofe», «hotel» и «otel»: удвоения и h в начале не различаем
    out = []
    for ch in text:
        if not out or out[-1] != ch:
            out.append(ch)
    return "".join(out).lstrip("h")


def similarity(learning_text: str, native_text: str) -> float:
    a, b = _skeleton(learning_text), _skeleton(native_text)
    if not a or not b:
        return 0.0
    return difflib.SequenceMatcher(None, a, b).ratio()


def word_similarity(word, pair) -> float:
    """Насколько слово изучаемого языка похоже на своё значение."""
    from app.services.language_service import main_meaning, normalize_headword, word_text

    learning = normalize_headword(word_text(word, pair.learning, with_article=False), pair.learning)
    native = normalize_headword(main_meaning(word, pair.native) or "", pair.native)
    return similarity(learning, native)


async def similar_new_word(session, user, pair, exclude_ids: list[int],
                           taken_meanings: set[str]) -> Optional[object]:
    """
    Новое лёгкое слово, похожее на родное, — для «Слышу» и «Вспоминаю».

    None — похожего в пуле нет; тогда место достаётся карточке.
    """
    from app.services.quiz_service import _meaning_key, easy_new_words

    candidates = await easy_new_words(session, user, pair, exclude_ids, limit=SIMILAR_POOL)
    best, best_score = None, SIMILAR_ENOUGH
    for word in candidates:
        meaning = _meaning_key(word, pair.native)
        if meaning and meaning in taken_meanings:
            continue
        score = word_similarity(word, pair)
        if score >= best_score:
            best, best_score = word, score
    return best
