"""
Ищет усечённое ПОВЕЛИТЕЛЬНОЕ в немецком эталоне.

Зачем. Блок 53 показал `Bitte betätig den Knopf`. Семь прошлых проходов
по разговорному усечению (scan_de_colloquial) искали `Ich <основа>`,
инверсию `<основа> ich`, проглоченное `es` и `is`/`-n`. Голая основа в
повелительном под ни один из них не подходила — и в докстринге той
приметы прямо написано, что повелительное различить нельзя, потому что
`Komm und hol es` законно.

Но нельзя — не всегда. У сильных глаголов повелительное и правда без
`-e` (`komm`, `geh`, `hol`, `lass`, `nimm`). А у слабых, чья основа
кончается на `-t`, `-d`, `-ig` или на `-n` после согласной, `-e`
ОБЯЗАТЕЛЬНО: `betätige`, `arbeite`, `antworte`, `beruhige`, `öffne`.
Без него формы просто не существует. Это решаемое правило, а не догадка.

Вторая половина правила — про регистр. Немецкие существительные пишутся
с заглавной, поэтому `arbeit` со строчной это всегда усечённый глагол,
а `Arbeit` с заглавной — существительное. Отсюда два списка: строчные
основы ищем все, с заглавной — только те, у которых нет
существительного-двойника.

Что примета не ловит. Основы на `-el`/`-er` (`ändere`/`ändre`,
`handle`) в немецком законно сокращаются двумя способами, и голая
основа от них отличима только на слух — в список они не входят.
`wart` выброшено нарочно: `Wo wart ihr?` это прошедшее от `sein`.
`halt` и `acht` выброшены тоже — это частица и числительное.

Ещё одно слепое место следует из того же правила регистра: `Arbeit
nicht so viel` в начале фразы примета не отличит от существительного и
промолчит. Усечение основ-двойников видно только посреди фразы, где они
со строчной.

Самопроверка: на заведомо правильных строках срабатывать не должно, на
заведомо испорченных — должно. Если хоть одна не сошлась, скрипт падает
и ничего не печатает.

    python -m app.scripts.scan_de_imperative
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# Основы, у которых «-e» в повелительном обязательно. Со строчной буквы
# любая из них — усечение: существительных со строчной в немецком нет.
LOWER_STEMS = (
    "betätig|beruhig|entschuldig|erledig|bestätig|benachrichtig|kündig"
    "|verständig|beschäftig|genehmig"
    "|arbeit|antwort|beobacht|erwart|verwend|beend|gründ|richt|rett"
    "|find|bind|send|wend|lad|red|bad"
    "|öffn|rechn|ordn|zeichn|wappn"
)
# Те же основы, но с заглавной — только без существительного-двойника.
# `Arbeit`, `Antwort`, `Bad`, `Rat` с заглавной это существительные,
# поэтому их здесь нет.
UPPER_STEMS = (
    "Betätig|Beruhig|Entschuldig|Erledig|Bestätig|Benachrichtig"
    "|Verständig|Beschäftig|Genehmig"
    "|Beobacht|Erwart|Verwend|Beend|Gründ|Rett"
    "|Find|Bind|Send|Wend|Richt"
    "|Öffn|Rechn|Ordn|Zeichn"
)

LOWER = re.compile(rf"\b({LOWER_STEMS})\b")
UPPER = re.compile(rf"\b({UPPER_STEMS})\b")

GOOD = [
    # правильные формы: «-e» на месте
    "Bitte betätige den Knopf",
    "Beruhige dich erst einmal",
    "Entschuldige die Verspätung",
    "Arbeite nicht so viel",
    "Antworte mir bitte sofort",
    "Öffne das Fenster",
    "Finde den Fehler im Text",
    "Erledige das heute noch",
    # сильные глаголы: там «-e» и не нужно
    "Komm und hol es",
    "Geh nach Hause",
    "Nimm dir ein Stück Kuchen",
    "Lass mich in Ruhe",
    "Gib mir das Buch",
    # существительные с заглавной — не глаголы
    "Die Arbeit ist fertig",
    "Ich warte auf deine Antwort",
    "Das Bad ist frei",
    "Er gab mir einen guten Rat",
    "Die Rechnung liegt auf dem Tisch",
    # «wart» это прошедшее от «sein», не усечение
    "Wo wart ihr gestern",
    "Ihr wart sehr hilfsbereit",
    # «halt» частица, «acht» числительное
    "Das ist halt so",
    "Es ist acht Uhr",
    # основы на «-el»/«-er» сокращаются законно, их не ищем
    "Ändere das bitte noch",
    "Handle jetzt, nicht später",
]
BAD = [
    "Bitte betätig den Knopf",
    "Beruhig dich erst einmal",
    "Entschuldig die Verspätung",
    "Du arbeit zu viel",
    "Sie antwort mir nicht",
    "Öffn das Fenster",
    "Find den Fehler im Text",
    "Erledig das heute noch",
    "Beobacht ihn genau",
    "Erwart nicht zu viel von ihm",
    "Rechn das noch einmal nachher",
    "Gründ deine eigene Firma",
    "Rett dich selbst zuerst",
    "Ordn die Papiere nach Datum",
    "Bestätig den Termin bitte",
]


def hit(s: str) -> bool:
    return bool(LOWER.search(s) or UPPER.search(s))


def selfcheck() -> None:
    for s in GOOD:
        if hit(s):
            print(f"САМОПРОВЕРКА УПАЛА: ложное срабатывание на {s!r}")
            sys.exit(1)
    for s in BAD:
        if not hit(s):
            print(f"САМОПРОВЕРКА УПАЛА: пропущено {s!r}")
            sys.exit(1)
    print(f"самопроверка: {len(GOOD)} правильных и {len(BAD)} "
          f"испорченных строк разобраны верно\n")


def main() -> None:
    selfcheck()
    engine = create_engine(settings.DATABASE_URL_SYNC)
    with engine.connect() as conn:
        rows = conn.execute(text(
            "SELECT id, word_de, example_de FROM words "
            "WHERE example_de IS NOT NULL ORDER BY id"
        )).all()

    found = [(i, w, e) for i, w, e in rows if hit(e)]
    print(f"прочитано немецких примеров: {len(rows)}")
    print(f"с усечённым повелительным: {len(found)}\n")
    for i, w, e in found:
        print(f"  {i:>6}  {w:<22}  {e}")


if __name__ == "__main__":
    main()
