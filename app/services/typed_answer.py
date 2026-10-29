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
    "en": ("the", "to", "an", "a"),
}
TYPO_FROM_LETTERS = 6


def _plain(text: str, lang: str) -> str:
    text = (text or "").strip()
    if lang == "tr":
        # Турецкие «I» и «İ» — разные буквы: заглавная без точки — это «ı»
        text = text.replace("I", "ı").replace("İ", "i")
    text = unicodedata.normalize("NFC", text.casefold())
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


def mark_mistakes(typed: str, correct: Iterable[str], lang: str,
                  article: Optional[str] = None) -> str:
    """
    Написанное с подчёркнутыми ошибками — HTML для разбора (владелец,
    29.10.2026: «важно показать, в чём ошибка, как в грамматике»).

    Неверный артикль подчёркивается целиком. В слове подчёркиваются лишние и
    неверные буквы, пропущенная — подчёркнутым «_» на её месте. Буквы
    сверяются с ближайшим верным вариантом без регистра; «ae» вместо «ä» и
    снятая диакритика ошибкой не считаются и не подчёркиваются. Совсем другое
    слово (меньше половины общих букв) не размечается — подчёркнутым было бы
    всё, и пользы в этом нет: оно показывается как есть.
    """
    from difflib import SequenceMatcher
    from html import escape

    raw = re.sub(r"\s+", " ", (typed or "").strip())
    got_article, _ = _split_article(_plain(raw, lang), lang)
    head, body = "", raw
    if got_article:
        cut = len(raw.split(" ", 1)[0]) if not got_article.endswith("'") else len(got_article)
        head, body = raw[:cut], raw[cut:].lstrip()
    out = ""
    if head:
        wrong = article and lang == "de" and got_article != _plain(article, lang)
        out = (f"<u>{escape(head)}</u>" if wrong else escape(head)) + " "

    # Сравнение по буквам — в «простом» виде, но размечается то, что написано:
    # для этого простой вид строится побуквенно, со ссылкой на исходную букву
    def letters(text: str) -> list[tuple[str, int]]:
        pairs = []
        for i, ch in enumerate(text):
            for p in _plain(ch, lang) if ch.strip() else " ":
                pairs.append((p, i))
        return pairs

    mine = letters(body)
    want = max((_split_article(_plain(v, lang), lang)[1] for v in correct),
               key=lambda w: SequenceMatcher(None, "".join(p for p, _ in mine), w).ratio(),
               default="")
    matcher = SequenceMatcher(None, "".join(p for p, _ in mine), want)
    if not want or matcher.ratio() < 0.5:
        return out + escape(body)

    bad, holes = set(), set()
    got = "".join(p for p, _ in mine)
    diff = [k for k in range(len(got)) if len(got) == len(want) and got[k] != want[k]]
    # Переставлены две соседние буквы («Breif») — подчёркиваются обе, а не
    # «пропуск здесь и лишняя там», как разметил бы побуквенный дифф
    swapped = (len(diff) == 2 and diff[1] == diff[0] + 1
               and got[diff[0]] == want[diff[1]] and got[diff[1]] == want[diff[0]])
    for op, i1, i2, j1, j2 in ([] if swapped else matcher.get_opcodes()):
        if op in ("replace", "delete"):
            bad.update(mine[k][1] for k in range(i1, i2))
        if op == "insert" or (op == "replace" and j2 - j1 > i2 - i1):
            holes.add(mine[i1][1] if i1 < len(mine) else len(body))
    if swapped:
        bad = {mine[diff[0]][1], mine[diff[1]][1]}
    for i, ch in enumerate(body):
        if i in holes:
            out += "<u>_</u>"
        out += f"<u>{escape(ch)}</u>" if i in bad else escape(ch)
    if len(body) in holes:
        out += "<u>_</u>"
    return out


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
    # Пояснение в скобках писать не нужно: «сумувати (за кимось)» засчитывает
    # и «сумувати», немецкая подсказка «(auf Anhieb) napoprvé» — «napoprvé»
    correct = {v for c in correct for v in (c, re.sub(r"\([^)]*\)", " ", c).strip()) if v}
    for variant in correct:
        _, want = _split_article(_plain(variant, lang), lang)
        if not want:
            continue
        if got == want:
            return Verdict.EXACT
        if len(want) >= TYPO_FROM_LETTERS and _one_edit_apart(got, want):
            best = Verdict.CLOSE
    return best
