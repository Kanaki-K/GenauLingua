"""
Текст сообщения по инициативе бота — из частей, о самом человеке.

Владелец 15.10, про прежнее «Пора позаниматься, Евгений! / Слово
запоминается, когда возвращается: день, три, неделя…»: «это говно, а не
напоминание». Справка о боте вместо человека. Правило теперь такое:

  заголовок   о нём: серия, сколько знает, вчерашние слова
  польза      числа его прогресса или его же слово под спойлером —
              мини-вопрос прямо в уведомлении («Помните, что значит …?»)
  шаг         маленький: «3 минуты», похвала за то, что уже сделано

РАЗНООБРАЗИЕ. Не двадцать готовых текстов, а части с вариантами: 8
заголовков × 3 строки пользы × 5 концовок у серии — 120 сочетаний из
строк, каждую из которых можно вычитать на шести языках. Главное же
разнообразие — сам человек: его слово и его числа меняются каждый раз.
Заголовок идёт по кругу (`seed` — число уже отправленных): тот же не
повторится, пока не пройдут все.
"""
from __future__ import annotations

import html
import zlib
from dataclasses import dataclass
from typing import Optional

from app.locales import LOCALES, get_text, plural


KNOWN_HEAD_FROM = 5
# Больше этого — число не зовёт, а придавливает («Пора освежить 2742
# слова», живой пример из базы): вместо числа — спокойная строка
DUE_MANY = 50
SECONDS_PER_QUESTION = 15


@dataclass(frozen=True)
class NudgeFacts:
    name: str                       # сырое: экранируется здесь
    flag: str = ""
    streak: int = 0                 # живая серия (0 — нет)
    in_work: int = 0
    known: int = 0                  # хоть раз отвечено верно
    learned: int = 0
    due: int = 0
    lessons: int = 0                # законченных занятий всего
    best: int = 0
    first_day: bool = False         # перерыв после самого первого дня
    away: int = 1                   # дней перерыва: «вчера» — только при 1
    first_day_words: int = 0
    word: Optional[tuple[str, str]] = None   # (слово, перевод) — сырые
    questions: int = 7


def variants(prefix: str) -> list[str]:
    """Ключи `prefix_1`, `prefix_2`… по русскому набору (остальные — тест)."""
    out, n = [], 1
    while f"{prefix}_{n}" in LOCALES["ru"]:
        out.append(f"{prefix}_{n}")
        n += 1
    return out


def _pick(keys: list[str], seed: int, salt: int = 0) -> str:
    """
    Заголовок (salt 0) — по кругу: тот же не повторится, пока не пройдут все.
    Остальные части — перемешанно, но воспроизводимо (crc32): иначе при
    длине, кратной множителю, часть застревала на одном варианте.
    """
    if salt == 0:
        return keys[seed % len(keys)]
    return keys[zlib.crc32(f"{seed}:{salt}".encode()) % len(keys)]


def _teaser(facts: NudgeFacts, lang: str, seed: int, new: bool) -> Optional[str]:
    if not facts.word:
        return None
    word, meaning = facts.word
    keys = variants("nd_teaser_new" if new else "nd_teaser_quiz")
    return get_text(_pick(keys, seed, 3), lang,
                    word=f"<b>{html.escape(word)}</b>",
                    meaning=f"<tg-spoiler>{html.escape(meaning)}</tg-spoiler>")


def _numbers(facts: NudgeFacts, lang: str) -> dict:
    return dict(
        name=html.escape(facts.name), flag=facts.flag,
        days=plural(facts.streak, "plural_days", lang),
        next_days=plural(facts.streak + 1, "plural_days", lang),
        known=plural(facts.known, "plural_words", lang), known_n=facts.known,
        in_work=facts.in_work, learned=facts.learned,
        due=plural(facts.due, "plural_words", lang), due_n=facts.due,
        lessons=plural(facts.lessons, "plural_lessons", lang), lessons_n=facts.lessons,
        best=plural(facts.best, "plural_days", lang),
        words=plural(facts.first_day_words, "plural_words", lang), first_n=facts.first_day_words,
        questions=facts.questions,
        # ~15 с на вопрос: медиана на проде 15.10 — 3,8 мин на 15 вопросов,
        # 1,7 мин на 7. Не меньше двух: «около 1 минут» не по-русски
        minutes_n=max(2, round(facts.questions * SECONDS_PER_QUESTION / 60)),
    )


def situation(kind: str, facts: NudgeFacts) -> str:
    """Какой набор частей: первый день, серия, прогресс, «всё на месте», прощание, приглашение."""
    if kind.startswith("start"):
        return "start_last" if kind == "start7" else ("start3" if kind == "start3" else "start")
    if kind == "back14":
        return "farewell"
    if kind == "back7":
        return "kept"
    if facts.first_day and facts.away == 1 and kind in ("back1", "daily"):
        return "first"
    if facts.streak >= 2:
        return "streak"
    return "progress"


def _body_numbers(facts: NudgeFacts, lang: str, seed: int, n: dict) -> Optional[str]:
    if facts.known <= 0 and facts.in_work <= 0:
        return None
    keys = variants("nd_body_learned" if facts.learned > 0 else "nd_body_known")
    return get_text(_pick(keys, seed, 1), lang, **n)


def compose(kind: str, facts: NudgeFacts, lang: str, seed: int) -> str:
    """Готовый HTML-текст. `seed` — сколько сообщений человек уже получил."""
    n = _numbers(facts, lang)
    sit = situation(kind, facts)
    lines: list[Optional[str]] = []

    if sit == "start":
        lines.append(get_text(_pick(variants("nd_start_head"), seed), lang, **n))
        lines.append(get_text(_pick(variants("nd_start_body"), seed, 1), lang, **n))
        lines.append(_teaser(facts, lang, seed, new=True))
    elif sit == "start3":
        lines.append(get_text(_pick(variants("nd_start3_head"), seed), lang, **n))
        lines.append(get_text(_pick(variants("nd_start_body"), seed, 1), lang, **n))
        lines.append(_teaser(facts, lang, seed, new=True))
    elif sit == "start_last":
        lines.append(get_text("nd_start_last_head", lang, **n))
        lines.append(get_text("nd_start_last_body", lang, **n))
    elif sit == "farewell":
        lines.append(get_text(_pick(variants("nd_farewell_head"), seed), lang, **n))
        # Варианты с числами — только когда оба числа не ноль: «выучено 0»
        # в прощальном письме звучит как упрёк, а не польза
        bodies = (variants("nd_farewell_body") if facts.known > 0 and facts.learned > 0
                  else ["nd_farewell_body_2"])
        lines.append(get_text(_pick(bodies, seed, 1), lang, **n))
    elif sit == "kept":
        lines.append(get_text(_pick(variants("nd_kept_head"), seed), lang, **n))
        bodies = (variants("nd_kept_body") if facts.known > 0 and facts.learned > 0
                  else ["nd_kept_body_2", "nd_kept_body_3"])
        lines.append(get_text(_pick(bodies, seed, 1), lang, **n))
        if facts.best >= 3:
            lines.append(get_text("nd_kept_best", lang, **n))
        lines.append(get_text(_pick(variants("nd_short"), seed, 2), lang, **n))
    elif sit == "first":
        heads = variants("nd_first_head")
        if facts.first_day_words > 0:
            heads = ["nd_first_head_words"] + heads
        lines.append(get_text(_pick(heads, seed), lang, **n))
        lines.append(get_text(_pick(variants("nd_first_body"), seed, 1), lang, **n))
        lines.append(_teaser(facts, lang, seed, new=False))
        lines.append(get_text(_pick(variants("nd_first_close"), seed, 2), lang, **n))
    elif sit == "streak":
        lines.append(get_text(_pick(variants("nd_streak_head"), seed), lang, **n))
        lines.append(_body_numbers(facts, lang, seed, n))
        lines.append(_teaser(facts, lang, seed, new=False))
        lines.append(get_text(_pick(variants("nd_streak_close"), seed, 2), lang, **n))
    else:  # progress
        heads = variants("nd_progress_head")
        # «Вы уже знаете 1 слово» звучит не пользой, а укором — число в
        # заголовке с пяти
        if facts.known >= KNOWN_HEAD_FROM:
            heads = ["nd_progress_head_known"] + heads
        lines.append(get_text(_pick(heads, seed), lang, **n))
        lines.append(_teaser(facts, lang, seed, new=False))
        if facts.due > DUE_MANY:
            lines.append(get_text(_pick(variants("nd_due_many"), seed, 1), lang, **n))
        elif facts.due > 0:
            lines.append(get_text(_pick(variants("nd_due"), seed, 1), lang, **n))
        if facts.lessons >= 2:
            lines.append(get_text(_pick(variants("nd_praise"), seed, 2), lang, **n))
        else:
            lines.append(get_text(_pick(variants("nd_short"), seed, 2), lang, **n))

    head, *rest = [line for line in lines if line]
    return head + "\n\n" + "\n".join(rest) if rest else head
