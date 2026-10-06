"""
Ищет ЛИШНЕЕ `zu` в инфинитиве после модального глагола.

Зачем. Блок 59 дал две одинаковые ошибки в эталоне:

    Der Kurs ist erfolgversprechend und wir sollten ihn einzuschlagen
    Man kann ihm nicht viel vorzuwerfen

После модального (`können`, `müssen`, `sollen`, `wollen`, `dürfen`,
`mögen`) инфинитив идёт БЕЗ `zu`. Это не стиль, а правило, и ошибка
сразу видна носителю, но ученик её списывает.

В блоке 56 была обратная ошибка — `Hör auf, mich runterziehen`, где
`zu` наоборот потеряно: после `aufhören` оно обязательно. Обе ошибки
об одном и том же месте в языке, и обе приметой проверяемы.

Как ищется. Инфинитив с `zu` у приставочного глагола пишется одним
словом: `einzuschlagen`, `vorzuwerfen`, `anzufangen`. Такую форму видно
по строению: приставка + `zu` + основа, и основа обязана быть глаголом
САМОЙ БАЗЫ. Это тот же приём, что в scan_de_separable.

Дальше нужен модальный глагол перед ней — и больше ничего между ними,
иначе `zu` может относиться к другому сказуемому: в `Wir können
anfangen zu essen` инфинитив `anfangen` стоит между модальным и `zu`,
и там всё правильно. Поэтому примета требует, чтобы между модальным и
склеенной формой НЕ БЫЛО другого инфинитива.

Чего примета не умеет: раздельное `zu <инфинитив>` после модального
(`Wir sollten ihn zu wählen`). Там `zu` отдельное слово, и отличить
его от законного `zu` при другом сказуемом по одной позиции нельзя.

    python -m app.scripts.scan_de_zu_infinitive
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

WORD = re.compile(r"[A-Za-zÄÖÜäöüß]+")

MODALS = {
    "kann", "kannst", "können", "könnt", "konnte", "konnten", "könnte",
    "könnten", "muss", "musst", "müssen", "müsst", "musste", "mussten",
    "müsste", "müssten", "soll", "sollst", "sollen", "sollt", "sollte",
    "sollten", "will", "willst", "wollen", "wollt", "wollte", "wollten",
    "darf", "darfst", "dürfen", "dürft", "durfte", "durften", "dürfte",
    "dürften", "mag", "magst", "mögen", "mögt", "mochte", "mochten",
    "möchte", "möchten", "möchtest",
}

# Приставки, с которыми `zu` вставляется внутрь слова.
PREFIXES = (
    "zurück", "zusammen", "gegenüber", "entgegen", "herunter", "hinunter",
    "herein", "hinein", "heraus", "hinaus", "vorbei", "voraus", "weiter",
    "wieder", "runter", "rein", "raus", "auf", "aus", "ein", "mit",
    "nach", "vor", "ab", "an", "bei", "her", "hin", "los", "weg", "fest",
)


def zu_infinitive(word: str, verbs: set[str]) -> bool:
    """Склеенный инфинитив с `zu`: приставка + zu + глагол базы."""
    w = word.lower()
    for p in PREFIXES:
        if w.startswith(p + "zu"):
            rest = w[len(p) + 2:]
            if rest in verbs:
                return True
    return False


# Союзы, которые САМИ требуют инфинитива с `zu`. Если такой союз стоит
# между модальным и склеенной формой, конструкция законна:
# `Ich muss zum Postamt, um ein Paket abzugeben` — здесь `zu` принадлежит
# обороту `um … zu`, а не модальному. Первый проход без этой оговорки
# принял такую фразу за ошибку.
ZU_CONJUNCTIONS = {"um", "ohne", "anstatt", "statt"}


def hit(example: str, verbs: set[str]) -> list[str]:
    toks = WORD.findall(example)
    out = []
    for i, t in enumerate(toks):
        if t.lower() not in MODALS:
            continue
        for j in range(i + 1, len(toks)):
            nxt = toks[j].lower()
            if zu_infinitive(nxt, verbs):
                out.append(toks[j])
                break
            # другой инфинитив между модальным и `zu`-формой делает
            # конструкцию законной
            if nxt in verbs or nxt in ZU_CONJUNCTIONS:
                break
    return out


FAKE = {"schlagen", "werfen", "fangen", "essen", "wählen"}
GOOD = [
    # после модального инфинитив без `zu` — так и надо
    ("Wir sollten ihn einschlagen", FAKE),
    # `zu` относится к другому сказуемому: между ними стоит инфинитив
    ("Wir können anfangen zu essen", FAKE),
    # нет модального вообще
    ("Es ist schwer, ihn einzuschlagen", FAKE),
    # приставка есть, а основы в базе нет — значит не наш глагол
    ("Wir sollten das Anzugeschäft besuchen", FAKE),
    # оборот `um … zu`: `zu` принадлежит ему, а не модальному
    ("Ich muss zum Postamt, um ein Paket abzuwerfen", FAKE),
]
BAD = [
    ("Der Kurs ist gut und wir sollten ihn einzuschlagen", FAKE),
    ("Man kann ihm nicht viel vorzuwerfen", FAKE),
    ("Du musst heute anzufangen", FAKE),
]


def selfcheck() -> None:
    for s, v in GOOD:
        if hit(s, v):
            print(f"САМОПРОВЕРКА УПАЛА: ложное срабатывание на {s!r}")
            sys.exit(1)
    for s, v in BAD:
        if not hit(s, v):
            print(f"САМОПРОВЕРКА УПАЛА: пропущено {s!r}")
            sys.exit(1)
    print(f"самопроверка: {len(GOOD)} правильных и {len(BAD)} "
          f"испорченных строк разобраны верно\n")


def main() -> None:
    selfcheck()
    engine = create_engine(settings.DATABASE_URL_SYNC)
    with engine.connect() as conn:
        verbs = {r[0].lower() for r in conn.execute(text(
            "SELECT word_de FROM words WHERE pos = 'VERB' "
            "AND word_de IS NOT NULL")).all()}
        rows = conn.execute(text(
            "SELECT id, word_de, example_de FROM words "
            "WHERE example_de IS NOT NULL ORDER BY id")).all()

    print(f"глаголов-заголовков в базе: {len(verbs)}")
    print(f"прочитано немецких примеров: {len(rows)}")

    found = [(i, w, e, h) for i, w, e in rows if (h := hit(e, verbs))]
    print(f"с лишним «zu» после модального: {len(found)}\n")
    for i, w, e, h in found:
        print(f"  {i:>6}  {w:<22} [{', '.join(h)}]  {e}")


if __name__ == "__main__":
    main()
