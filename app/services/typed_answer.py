"""
Ответ вводом — «Вспоминаю» для выученного слова (владелец, 29.10.2026:
тренажёр должен быть труднее; самая честная проверка «знаю» — написать слово
самому, без вариантов).

Сравнение прощает то, что не ошибка в знании:

  регистр, пробелы, точка в конце     «Bank.» = «bank»
  немецкие буквы двумя                ae = ä, oe = ö, ue = ü, ss = ß
  диакритика других языков            «nino» = «niño», «cafe» = «café»: на
                                      телефоне раскладки может не быть
  одна опечатка в слове от 6 букв     «Fenstr» = «Fenster» — но это «почти»,
                                      человек увидит, как пишется верно

И НЕ прощает то, что ошибка: неверный артикль (die Tisch), другое слово,
две опечатки. Артикль писать не обязательно — спрашивают слово; но если
написан, он должен быть верным.

Верными считаются все варианты ячейки изучаемого языка: «Вспоминаю»
спрашивает по значению, и под ним может стоять несколько слов.
"""
from __future__ import annotations

import re
import unicodedata
from enum import Enum
from typing import Iterable, Optional


class Verdict(Enum):
    EXACT = "exact"       # верно
    CLOSE = "close"       # верно с одной опечаткой
    WRONG = "wrong"


_GERMAN = str.maketrans({"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"})
_ARTICLES = {
    "de": ("der", "die", "das"),
    "it": ("il", "lo", "la", "l'", "i", "gli", "le"),
    "es": ("el", "la", "los", "las"),
    "fr": ("le", "la", "l'", "les"),
    "en": ("the", "to"),
}
TYPO_FROM_LETTERS = 6


def _plain(text: str, lang: str) -> str:
    text = unicodedata.normalize("NFC", (text or "").strip().casefold())
    text = re.sub(r"[.!?,;:«»\"“”]+$", "", text).strip()
    text = re.sub(r"\s+", " ", text)
    if lang == "de":
        text = text.translate(_GERMAN)
    # Диакритика — снимается у всех: немецкие буквы уже переведены выше
    text = "".join(ch for ch in unicodedata.normalize("NFKD", text)
                   if not unicodedata.combining(ch))
    return text


def _split_article(text: str, lang: str) -> tuple[Optional[str], str]:
    for article in sorted(_ARTICLES.get(lang, ()), key=len, reverse=True):
        if article.endswith("'") and text.startswith(article):
            return article, text[len(article):].strip()
        if text.startswith(article + " "):
            return article, text[len(article) + 1:].strip()
    return None, text


def _one_edit_apart(a: str, b: str) -> bool:
    """Одна вставка, удаление, замена или перестановка соседних букв."""
    if a == b or abs(len(a) - len(b)) > 1:
        return False
    if len(a) == len(b):
        diff = [i for i in range(len(a)) if a[i] != b[i]]
        if len(diff) == 1:
            return True
        return (len(diff) == 2 and diff[1] == diff[0] + 1
                and a[diff[0]] == b[diff[1]] and a[diff[1]] == b[diff[0]])
    short, long_ = (a, b) if len(a) < len(b) else (b, a)
    i = j = 0
    skipped = False
    while i < len(short) and j < len(long_):
        if short[i] != long_[j]:
            if skipped:
                return False
            skipped = True
            j += 1
            continue
        i += 1
        j += 1
    return True


def judge(typed: str, correct: Iterable[str], lang: str,
          article: Optional[str] = None) -> Verdict:
    """
    Оценить написанное против верных вариантов изучаемого языка.

    `article` — артикль слова (немецкий), если он есть: написанный артикль
    обязан с ним совпасть.
    """
    got_article, got = _split_article(_plain(typed, lang), lang)
    if not got:
        return Verdict.WRONG
    if got_article and article and lang == "de" and got_article != _plain(article, lang):
        return Verdict.WRONG
    best = Verdict.WRONG
    for variant in correct:
        _, want = _split_article(_plain(variant, lang), lang)
        if not want:
            continue
        if got == want:
            return Verdict.EXACT
        if len(want) >= TYPO_FROM_LETTERS and _one_edit_apart(got, want):
            best = Verdict.CLOSE
    return best
