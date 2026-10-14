"""
Ищет НЕОТДЕЛЁННУЮ ПРИСТАВКУ у немецкого глагола в эталоне.

Зачем. Блок 56 дал `Der Zug eintraf pünktlich am Bahnhof`. По-немецки
у глагола с отделяемой приставкой личная форма рвётся: `Der Zug traf
pünktlich am Bahnhof ein`. Склеенная форма в главном предложении —
грубая ошибка, и ученик списывает её вместе с фразой.

Словарь опять берём из базы: она сама знает свои глаголы с отделяемой
приставкой — `eintreffen`, `abspringen`, `anlocken`, `wegschmeißen`.
Для ряда с таким заголовком примета разбирает заголовок на приставку
и основу и ищет в примере склеенную личную форму.

Что НЕ ошибка и отсекается:
  · инфинитив — он и пишется слитно (`Der Zug soll eintreffen`);
  · инфинитив с `zu` — `einzutreffen`;
  · причастие — `eingetroffen`;
  · ПРИДАТОЧНОЕ предложение: там приставка остаётся на месте, и это
    правильно — `..., weil der Zug pünktlich eintraf`.

Последнее и есть главная трудность. Отличить главное предложение от
придаточного без разбора синтаксиса нельзя — зато можно по позиции:
в придаточном глагол стоит В КОНЦЕ, перед запятой или точкой, а в
главном — вторым словом, и после него ещё идут слова. Поэтому примета
срабатывает только когда склеенная форма НЕ последняя в своей части
фразы. Правило грубое, но решаемое и проверяемое.

После правки блока 56 примета прочла 654 приставочных глагола и
показала ноль. Это честный ноль в границах, описанных ниже.

Чего примета не умеет:
  · найти ошибку, если склеенная форма случайно оказалась последней
    в главном предложении («Der Zug eintraf») — там позиция совпадает
    с правильной придаточной;
  · проверить глаголы с `über`, `unter`, `um`, `durch`, `wider`,
    `hinter`: эти приставки бывают и отделяемыми, и неотделяемыми,
    и 863 глагола сузились до 654 именно из-за этого;
  · увидеть склеенную форму в начале фразы: там заглавная буква, а по
    заглавной примета отсекает существительные от того же корня.

    python -m app.scripts.scan_de_separable
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# ВСЕГДА отделяемые приставки. Длинные стоят первыми: `zurück` надо
# отрезать целиком, иначе от него останется `ück`.
#
# `über`, `unter`, `um`, `durch`, `wider`, `hinter` в список НЕ входят:
# они бывают и отделяемыми, и неотделяемыми, и по написанию это не
# различить. В `übernehmen`, `unterstützen`, `umarmen`, `durchqueren`,
# `widerrufen` они неотделяемые, и слитная форма там правильная.
# Первый проход без этой оговорки дал 40 попаданий, из них 31 — ровно
# такие глаголы.
PREFIXES = (
    "zurück", "zusammen", "gegenüber", "entgegen", "herunter", "hinunter",
    "herein", "hinein", "heraus", "hinaus", "herauf", "hinauf", "herüber",
    "vorbei", "voraus", "vorher", "weiter", "wieder", "zurecht", "fort",
    "runter", "rüber", "rein", "raus", "statt", "teil", "heim",
    "auf", "aus", "ein", "mit", "nach", "vor", "zu", "ab", "an", "bei",
    "her", "hin", "los", "weg", "da", "fest", "frei",
)

WORD = re.compile(r"[A-Za-zÄÖÜäöüß]+|[,.;:!?]")


def split_prefix(word_de: str, verbs: set[str]) -> tuple[str, str] | None:
    """Разобрать заголовок на отделяемую приставку и основу.

    Основа обязана быть глаголом САМОЙ БАЗЫ: `eintreffen` → `treffen`,
    и `treffen` в базе есть. Без этой проверки примета резала корни:
    `antworten` → `an` + `worten`, `danken` → `da` + `nken`,
    `rauschen` → `raus` + `chen`, `zucken` → `zu` + `cken`.
    Девять ложных срабатываний из сорока были ровно такие.
    """
    w = word_de.lower()
    if not w.endswith("en") or len(w) < 6:
        return None
    for p in PREFIXES:
        if w.startswith(p) and len(w) - len(p) >= 4:
            base = w[len(p):]
            if base in verbs:
                return p, base
    return None


def glued(example: str, prefix: str, base: str) -> list[str]:
    """Склеенные личные формы, стоящие НЕ в конце части фразы."""
    toks = WORD.findall(example)
    out = []
    for i, t in enumerate(toks):
        if t[0].isupper():
            # существительное, образованное от того же глагола:
            # `Anhänger` от `anhängen`, `Abschleppwagen` от
            # `abschleppen`. Они пишутся с заглавной и слитно —
            # это не глагол и не ошибка.
            continue
        low = t.lower()
        if not low.startswith(prefix):
            continue
        rest = low[len(prefix):]
        if len(rest) < 3 or not rest:
            continue
        if rest == base or rest == "zu" + base or rest.startswith("ge"):
            continue
        if rest[0] != base[0]:          # другая основа, не наш глагол
            continue
        tail = toks[i + 1:]
        # в конце своей части фразы приставка остаётся законно
        if not tail or tail[0] in ",.;:!?":
            continue
        out.append(t)
    return out


GOOD = [
    # инфинитив, инфинитив с zu, причастие — слитно и правильно
    ("eintreffen", "Der Zug soll pünktlich eintreffen"),
    ("eintreffen", "Der Zug scheint einzutreffen heute"),
    ("eintreffen", "Der Zug ist pünktlich eingetroffen am Bahnhof"),
    # придаточное: приставка на месте, и это верно
    ("eintreffen", "Ich weiß, dass der Zug pünktlich eintraf"),
    ("abspringen", "Er sagte, dass der Fallschirmspringer absprang"),
    # правильная разорванная форма
    ("eintreffen", "Der Zug traf pünktlich am Bahnhof ein"),
    ("anlocken", "Der Duft lockt die Kunden in den Laden an"),
]
BAD = [
    ("eintreffen", "Der Zug eintraf pünktlich am Bahnhof"),
    ("abspringen", "Der Fallschirmspringer absprang aus dem Flugzeug"),
    ("anlocken", "Der Duft anlockt die Kunden in den Laden"),
    ("mitnehmen", "Ich mitnehme das Buch nach Hause"),
]


FAKE_VERBS = {"treffen", "springen", "locken", "nehmen", "schmeißen"}
# Заголовки, у которых приставка только кажется приставкой: основа
# не глагол, и примета обязана молчать.
GOOD_ROOTS = [
    ("antworten", "Bitte antworte schnell und ohne Umschweife"),
    ("danken", "Ich danke dir sehr für die Hilfe"),
    ("zucken", "Sein Auge zuckte nervös den ganzen Abend"),
    ("rauschen", "Das Wasser rauscht laut über die Steine"),
]


def selfcheck() -> None:
    for w, s in GOOD:
        p = split_prefix(w, FAKE_VERBS)
        if p and glued(s, *p):
            print(f"САМОПРОВЕРКА УПАЛА: ложное срабатывание на {s!r}")
            sys.exit(1)
    for w, s in GOOD_ROOTS:
        if split_prefix(w, FAKE_VERBS):
            print(f"САМОПРОВЕРКА УПАЛА: {w!r} разобран как приставочный")
            sys.exit(1)
    for w, s in BAD:
        p = split_prefix(w, FAKE_VERBS)
        if not p or not glued(s, *p):
            print(f"САМОПРОВЕРКА УПАЛА: пропущено {s!r}")
            sys.exit(1)
    print(f"самопроверка: {len(GOOD) + len(GOOD_ROOTS)} правильных и "
          f"{len(BAD)} испорченных строк разобраны верно\n")


def main() -> None:
    selfcheck()
    engine = create_engine(settings.DATABASE_URL_SYNC)
    with engine.connect() as conn:
        rows = conn.execute(text(
            "SELECT id, word_de, example_de FROM words "
            "WHERE pos = 'VERB' AND example_de IS NOT NULL ORDER BY id"
        )).all()
        verbs = {r[0].lower() for r in conn.execute(text(
            "SELECT word_de FROM words WHERE pos = 'VERB' "
            "AND word_de IS NOT NULL")).all()}

    print(f"глаголов-заголовков в базе: {len(verbs)}")

    checked, found = 0, []
    for i, w, e in rows:
        p = split_prefix(w, verbs)
        if not p:
            continue
        checked += 1
        if hits := glued(e, *p):
            found.append((i, w, e, hits))

    print(f"глаголов в базе: {len(rows)}")
    print(f"из них с отделяемой приставкой: {checked}")
    print(f"с неотделённой приставкой в примере: {len(found)}\n")
    for i, w, e, hits in found:
        print(f"  {i:>6}  {w:<22} [{', '.join(hits)}]  {e}")


if __name__ == "__main__":
    main()
