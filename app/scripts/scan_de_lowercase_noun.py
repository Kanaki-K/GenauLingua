"""
Ищет СУЩЕСТВИТЕЛЬНОЕ СО СТРОЧНОЙ БУКВЫ в немецком эталоне.

Зачем. Блок 55 дал `Er verschloss alle Wertsachen in dem safe`.
В немецком заглавная у существительного — не стиль, а орфография: это
ошибка того же разряда, что пропущенная запятая, и ученик списывает её
вместе с фразой.

Словарь брать негде, но он уже есть: 7184 немецких заголовка-NOUN самой
базы. База проверяет сама себя.

Первая версия приметы искала ЛЮБОЕ строчное слово, у которого в базе
есть заголовок-NOUN с заглавной, — и дала 270 попаданий, почти все
ложные: `wir essen` (das Essen — субстантивированный инфинитив),
`sie macht` (die Macht), `ich frage` (die Frage), `ich reise`
(die Reise). Немецкий устроен так, что форма глагола постоянно
совпадает с существительным, и по одному слову их не различить.

Поэтому примета смотрит не слово, а ПОЗИЦИЮ: сразу после артикля или
другого определителя (`dem`, `einen`, `meiner`, `dieses`…). Там глагол
стоять не может — только существительное или прилагательное перед ним.
Прилагательные база тоже знает, и они из рассмотрения исключены.

Этого оказалось мало: 34 попадания, и снова все ложные — склонённые
прилагательные, чьи формы совпадают с существительными базы: `tiefe`
(die Tiefe), `alter` (der Alter), `junge` (der Junge), `antike`
(die Antike), `dichter` (der Dichter). Поэтому примета теперь ещё и
отбрасывает всё, что база умеет вывести от своих же заголовков
НЕ-существительных: `tief` + e, `alt` + er, `jung` + e. 110 тысяч форм
от 5326 заголовков — и ни одного ложного срабатывания.

После правки блока 55 примета показывает ноль. Это честный ноль ровно в
тех границах, что описаны ниже, и не больше.

Чего примета НЕ умеет:
  · найти строчное существительное БЕЗ артикля («Ich kaufe brot») —
    там позиция ничего не гарантирует;
  · отличить артикль от указательного местоимения: в «Das macht mir
    Freude» слово `das` — местоимение, а не артикль, и `macht` за ним
    это глагол. Такие случаи отсекаются уже проверкой форм, но на
    чужом слове примета бы ошиблась;
  · различить слова-двойники, у которых со строчной другая часть речи
    и артикль перед ними всё равно возможен (`das Gute` / `gut`).
    Такие перечислены в DOUBLES, список ведётся руками.

Самопроверка идёт на выдуманном словаре, не на базе: проверяется логика
приметы, а не содержимое базы.

    python -m app.scripts.scan_de_lowercase_noun
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

WORD = re.compile(r"[A-Za-zÄÖÜäöüß]+")

# Определители: после них глагол стоять не может.
DETERMINERS = {
    "der", "die", "das", "dem", "den", "des",
    "ein", "eine", "einen", "einem", "eines", "einer",
    "kein", "keine", "keinen", "keinem", "keines", "keiner",
    "mein", "meine", "meinen", "meinem", "meines", "meiner",
    "dein", "deine", "deinen", "deinem", "deines", "deiner",
    "sein", "seine", "seinen", "seinem", "seines", "seiner",
    "ihr", "ihre", "ihren", "ihrem", "ihres", "ihrer",
    "unser", "unsere", "unseren", "unserem", "unseres", "unserer",
    "euer", "eure", "euren", "eurem", "eures", "eurer",
    "dieser", "diese", "dieses", "diesen", "diesem",
    "jener", "jene", "jenes", "jenen", "jenem",
    "jeder", "jede", "jedes", "jeden", "jedem",
    "welcher", "welche", "welches", "welchen", "welchem",
    "manche", "mancher", "manches", "manchen", "manchem",
    "alle", "allen", "aller", "allem", "alles",
    "beide", "beiden", "beider",
}

# Слова, у которых со строчной законна другая часть речи, и артикль
# перед ними всё равно встречается. Ведётся руками.
DOUBLES = {
    "gut", "gute", "guten", "gutes", "guter", "gutem",
    "recht", "rechte", "rechten", "rechtes",
    "laut", "laute", "lauten", "lautes",
    "andere", "anderen", "anderes", "anderer", "anderem",
    "meiste", "meisten", "letzte", "letzten", "erste", "ersten",
    "ganze", "ganzen", "ganzes", "paar", "meisten", "beste", "besten",
}


ADJ_ENDINGS = ("", "e", "en", "er", "em", "es", "ere", "eren", "erem",
               "eres", "ste", "sten", "ster", "stes")
VERB_ENDINGS = ("", "e", "t", "st", "en", "te", "ten", "test", "end")


def inflections(others: set[str]) -> set[str]:
    """Все формы, которые база может образовать от своих же заголовков
    НЕ-существительных. Нужно затем, чтобы `tiefe` не приняли за
    `die Tiefe`, `alter` за `der Alter`, а `junge` за `der Junge`:
    это склонённые `tief`, `alt`, `jung`, и база их знает."""
    out = set()
    for w in others:
        for e in ADJ_ENDINGS:
            out.add(w + e)
        stem = w[:-2] if w.endswith("en") else w
        for e in VERB_ENDINGS:
            out.add(stem + e)
    return out


def candidates(example: str, nouns: set[str], others: set[str]) -> list[str]:
    """Строчные слова в позиции после определителя, которые база
    знает как существительное и не знает как другую часть речи."""
    out, prev = [], ""
    for m in WORD.finditer(example):
        w = m.group()
        low = w.lower()
        if (prev in DETERMINERS and w[0].islower()
                and low not in DOUBLES
                and low not in others
                and w.capitalize() in nouns):
            out.append(w)
        prev = low
    return out


FAKE_NOUNS = {"Safe", "Hund", "Tisch", "Brot", "Gut"}
FAKE_OTHERS = inflections({"rot", "alt", "neu", "machen"})
GOOD = [
    "Er verschloss alle Wertsachen in dem Safe",
    "Der Hund liegt unter dem Tisch",
    # прилагательное после артикля — законно
    "Ich kaufe das rote Auto",
    "Der alte Mann schläft",
    # без артикля примета молчит: позиция ничего не гарантирует
    "Ich kaufe brot",
    # слово-двойник
    "Das Gute siegt am Ende",
]
BAD = [
    "Er verschloss alle Wertsachen in dem safe",
    "Der hund liegt unter dem Tisch",
    "Das Buch liegt auf dem tisch",
    "Ich habe ein brot gekauft",
]


def selfcheck() -> None:
    for s in GOOD:
        if candidates(s, FAKE_NOUNS, FAKE_OTHERS):
            print(f"САМОПРОВЕРКА УПАЛА: ложное срабатывание на {s!r}")
            sys.exit(1)
    for s in BAD:
        if not candidates(s, FAKE_NOUNS, FAKE_OTHERS):
            print(f"САМОПРОВЕРКА УПАЛА: пропущено {s!r}")
            sys.exit(1)
    print(f"самопроверка: {len(GOOD)} правильных и {len(BAD)} "
          f"испорченных строк разобраны верно\n")


def main() -> None:
    selfcheck()
    engine = create_engine(settings.DATABASE_URL_SYNC)
    with engine.connect() as conn:
        nouns = {r[0] for r in conn.execute(text(
            "SELECT word_de FROM words WHERE pos = 'NOUN' "
            "AND word_de IS NOT NULL")).all()}
        others = {r[0].lower() for r in conn.execute(text(
            "SELECT word_de FROM words WHERE pos <> 'NOUN' "
            "AND word_de IS NOT NULL")).all()}
        rows = conn.execute(text(
            "SELECT id, word_de, example_de FROM words "
            "WHERE example_de IS NOT NULL ORDER BY id")).all()

    print(f"заголовков-существительных в базе: {len(nouns)}")
    print(f"заголовков прочих частей речи: {len(others)}")
    print(f"прочитано немецких примеров: {len(rows)}")

    forms = inflections(others)
    print(f"форм, выводимых от заголовков-неимён: {len(forms)}")

    found = [(i, w, e, c) for i, w, e in rows
             if (c := candidates(e, nouns, forms))]
    print(f"со строчным существительным после артикля: {len(found)}\n")
    for i, w, e, c in found:
        print(f"  {i:>6}  {w:<22} [{', '.join(c)}]  {e}")


if __name__ == "__main__":
    main()
