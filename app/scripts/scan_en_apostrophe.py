"""
Ищет пропущенный апостроф в АНГЛИЙСКИХ примерах.

Зачем. Класс держится с блока 22 и всплывал в каждом блоке после:
`its there` вместо `it's there`, `8 oclock`, `the teams mood`,
`My grandpas hug`. Поодиночке это опечатки, вместе — класс, который
надо вымести сплошь.

Сложность в том, что почти каждая форма без апострофа — настоящее
английское слово: `its` (притяжательное), `were` (глагол), `id`, `im`,
`lets` (третье лицо от `let`), `hes`, `shed`. Поэтому примета ищет не
слово, а слово в такой обстановке, где другое чтение невозможно:

* `its` + прилагательное/наречие + ничего притяжательного дальше —
  например `its so hot here`. Чистое `its` перед существительным
  (`its colour`) не трогаем.
* `oclock`, `wasnt`, `dont`, `didnt`, `couldnt`, `youre`, `theyre`,
  `thats`, `whats`, `theres`, `ive`, `wouldnt` — таких английских слов
  нет вовсе, их можно брать без оглядки на обстановку.
* `Lets` с большой буквы в начале фразы — это всегда `Let's`.
* `I'll rather` — грамматически невозможно, нужно `I'd rather`.

Самопроверка: на заведомо правильных строках срабатывать не должно, на
заведомо испорченных — должно.

    python -m app.scripts.scan_en_apostrophe
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# Форм без апострофа, которых в английском нет вовсе.
NO_SUCH_WORD = re.compile(
    r"\b("
    r"oclock|wasnt|werent|dont|doesnt|didnt|isnt|arent|havent|hasnt|hadnt|"
    r"wont|wouldnt|couldnt|shouldnt|cant|aint|youre|theyre|thats|whats|"
    r"theres|heres|ive|youve|theyve|weve|youll|theyll|thatll|"
    r"wouldve|couldve|shouldve|mustnt|neednt"
    r")\b", re.IGNORECASE)

# `its` в обстановке, где притяжательное чтение невозможно: дальше идёт
# слово, к которому нельзя «принадлежать» — наречие или предлог места.
ITS_IS = re.compile(
    r"\bits\s+(so|too|very|really|already|not|here|there|time|because|"
    r"always|still|getting|going|raining|snowing|cold|hot|warm|late|early|"
    r"easy|hard|true|false|okay|ok|fine|good|bad|better|worse|possible|"
    r"important|interesting|broken|open|closed|free|busy|full|empty)\b",
    re.IGNORECASE)

# `Lets` в начале фразы — всегда `Let's`.
LETS = re.compile(r"(?:^|[.!?]\s+)Lets\b")

# «I'll rather» вместо «I'd rather».
RATHER = re.compile(r"\b(I|we|you|he|she|they)'ll rather\b", re.IGNORECASE)

# Названия праздников с притяжательным: `Valentines Day` вместо
# `Valentine's Day`. Добавлено после блока 30 — там примета это
# пропустила, потому что искала только общие слова.
HOLIDAY = re.compile(
    r"\b(Valentines|Mothers|Fathers|Teachers|Childrens|Womens|Veterans|"
    r"Presidents|Saints|April Fools|New Years)\s+(Day|Eve)\b")

GOOD = [
    # притяжательное `its` — настоящее слово
    "The bird's feather is beautiful and its colour is white",
    "The company changed its name last year",
    "The dog wagged its tail",
    # `were` как глагол
    "Were all the students present",
    "They were very happy",
    # уже с апострофом
    "The air conditioner is broken, it's so hot here",
    "The bell rings at 8 o'clock",
    "My grandpa's hug was so warm and nice",
    "That's the least of my problems",
    "I'd rather stay home",
    "Let's swap, you give me your sandwich",
    # `lets` как третье лицо
    "He lets the dog out every morning",
    # прочее
    "I will deliver the message",
    "He has a scholarship",
    # «shell» — настоящее слово (ракушка), а не «she'll».
    # Первая версия приметы на нём ложно сработала.
    "The shell lay on the beach",
    "On Valentine's Day people give flowers",
    "We celebrate New Year's Eve at home",
]
BAD = [
    "The air conditioner is broken, its so hot here",
    "Look under it, maybe its there",
    "The bell rings at 8 oclock",
    "The weather is terrible today, I'll rather stay home",
    "Lets go to the cinema",
    "He wasnt at home yesterday",
    "I dont know the answer",
    "Thats a good idea",
    "Youre very kind",
    "Theres no time left",
    "On Valentines Day people give flowers",
    "We celebrate New Years Eve at home",
]


def hit(s: str) -> bool:
    return bool(NO_SUCH_WORD.search(s) or ITS_IS.search(s)
                or LETS.search(s) or RATHER.search(s)
                or HOLIDAY.search(s))


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
            "SELECT id, word_de, example_en FROM words "
            "WHERE example_en IS NOT NULL ORDER BY id"
        )).all()

    found = [(i, w, e) for i, w, e in rows if hit(e)]
    print(f"прочитано английских примеров: {len(rows)}")
    print(f"с пропущенным апострофом: {len(found)}\n")
    for i, w, e in found:
        print(f"  {i:>6}  {w:<22}  {e}")


if __name__ == "__main__":
    main()
