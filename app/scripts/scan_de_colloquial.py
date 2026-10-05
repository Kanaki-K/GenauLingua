"""
Ищет разговорные усечения в НЕМЕЦКОМ ЭТАЛОНЕ.

Зачем. Эталон — это то, по чему выверяются все пять переводов и то, что
читает ученик. В нём не должно быть проглоченных окончаний. В блоках 26
и 27 нашлись `Ich häng das Bild`, `Ich bring dich zum Bahnhof`,
`Ich schüttel den Baum`, `Ich brauch mal ne Auszeit` — четыре случая
подряд, значит это класс, а не случайность.

Две приметы:

1. `Ich <stem>` без конечного `-e` у слабого глагола. Модальные
   (`kann`, `will`, `muss`, `soll`, `darf`, `mag`), `bin`, `war`,
   `weiß`, `werde` так и пишутся — они в список не входят.
2. Та же основа при инверсии: `Morgen fahr ich weg`.
3. Усечённый артикль: `ne`, `nen`, `nem`, `'ne`, `so'n` вместо
   `eine`, `einen`, `einem`, `so ein`.

4. Проглоченное `es`, приклеенное к глаголу: `ich mags` вместо
   `ich mag es`. Добавлено после блока 40 вместе с основой `check`,
   расширено после блока 43 на повелительное с заглавной буквы
   (`Versuchs mal`) — и на основы `versuch`, `probier`, `guck`, `schau`.

5. Приставочные основы: `Ich widerruf meine Aussage` (блок 45). Общего
   шаблона у них нет, каждую приходится вносить поимённо.

Что примета принципиально не ловит: усечение при опущенном подлежащем —
`Ich gehe mal zu ihr hin und frag sie`. Голая основа после `und` это
ещё и законное повелительное (`Komm und hol es`), различить нельзя.
Такие случаи только глазами.

Пункты 2 и 3 добавлены после блока 28: первая версия приметы ловила
только `Ich <основа>` и `ne` перед заглавной буквой, и пропустила
`Morgen fahr ich weg`, `Auf der Autobahn fahr ich` и
`echt ne miese Tour`.

Самопроверка: на заведомо правильных строках срабатывать не должно, на
заведомо испорченных — должно. Если хоть одна не сошлась, скрипт падает
и ничего не печатает.

    python -m app.scripts.scan_de_colloquial
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# Слабые глаголы: в 1-м лице единственного числа обязательно «-e».
# Модальные и неправильные формы (bin, war, weiß, kann, will, muss,
# soll, darf, mag, werde) сюда не входят — они так и пишутся.
STEMS = (
    "bring|häng|hang|schüttel|brauch|hab|mach|komm|geh|seh|steh|nehm|"
    "geb|sag|frag|leg|setz|hol|kauf|zeig|such|spiel|lern|arbeit|wohn|"
    "denk|glaub|find|lauf|trag|fahr|ruf|schreib|les|trink|ess|schlaf|"
    "freu|wart|bleib|hör|red|zahl|hoff|wasch|koch|putz|räum|öffn|"
    # добавлено после блока 29: там нашлись «Morgen reis ich ab» и
    # «Ich pack meine Sachen» — основ в списке не было
    "pack|reis|schau|zieh|dreh|stell|steck|werf|schick|erzähl|versteh|"
    "verlier|verkauf|bezahl|probier|bestell|wink|kümmer|unterschreib|"
    # добавлено после блока 40: «Ich check mal mein Bankkonto»
    "check|"
    # добавлено после блока 45: «Ich widerruf meine Aussage». Приставочные
    # основы приходится вносить поимённо: `widerrufe`, `erkläre`,
    # `entschuldige` — у каждой своё начало, общего шаблона нет.
    "widerruf|erklär|entschuldig|überleg|verspät|beschwer|erinner"
)
# Строчное «ich» посреди фразы тоже считается: блок 33 показал
# «Lass mich, ich zieh mir gerade einen Film rein» — первая версия
# искала только «Ich» с заглавной.
VERB = re.compile(rf"\b[Ii]ch ({STEMS})\b")
# Та же основа при инверсии: «Morgen fahr ich weg», «brauch ich».
# Модальные и `bin`/`war`/`weiß` в список основ не входят, поэтому
# «kann ich», «muss ich», «bin ich» сюда не попадают.
INVERTED = re.compile(rf"\b({STEMS}) ich\b")
# Усечённый артикль. Отдельных слов «ne», «nen», «nem» в немецком нет —
# это всегда проглоченные `eine`, `einen`, `einem`, поэтому хватает
# границ слова, а буква после них может быть любой.
ARTICLE = re.compile(r"\b(ne|nen|nem)\b|\bso'n\b|'ne\b")
# Проглоченное «es», приклеенное к глаголу: «ich mags» вместо «ich mag
# es», «machs» вместо «mach es». Добавлено после блока 40.
# Заглавная буква нужна: в блоке 43 попалось `Versuchs mal mit einem
# anderen Ansatz` — повелительное в начале фразы. Основы, у которых
# «основа+s» это настоящее немецкое слово (`Pack` → `Packs`,
# `Dreh` → `Drehs`), в список не входят.
CONTRACTION = re.compile(
    r"\b([Mm]ag|[Hh]ab|[Hh]at|[Ww]ill|[Kk]ann|[Mm]ach|[Nn]ehm|[Gg]eb"
    r"|[Ff]ind|[Ss]eh|[Ss]ag|[Hh]ol|[Gg]ib|[Vv]ersuch|[Pp]robier"
    r"|[Gg]uck|[Ss]chau)s\b"
)

# Слова базы, для которых усечение — это и есть предмет ряда.
LEGIT_HEADWORDS = {"ne"}

GOOD = [
    "Ich kann das nicht machen",
    "Ich will nach Hause",
    "Ich muss noch arbeiten",
    "Ich soll das erledigen",
    "Ich darf hier parken",
    "Ich mag Schokolade",
    "Ich weiß die Antwort",
    "Ich bin sehr müde",
    "Ich war gestern dort",
    "Ich werde morgen kommen",
    "Ich bringe dich zum Bahnhof hin",
    "Ich hänge das Bild an die Wand auf",
    "Ich brauche eine Pause",
    "Ich habe keine Zeit",
    # «warte» и «öffne» — уже правильные формы, в список основ не входят
    "Ich warte auf deine Antwort",
    "Ich öffne das Übungsbuch",
    # «ne» как часть слова или конец предложения — не артикль
    "Die Sonne scheint heute warm",
    "Er hat eine Idee",
    "Ich nehme eine Kapsel Vitamin C jeden Morgen",
    "Morgen fahre ich weg",
    "Kann ich dir helfen",
    "Heute muss ich arbeiten",
    "Gestern war ich zu Hause",
    # приклеенное «s» — только к глаголу, не к существительному
    "Ich mag es sehr",
    "Er hat es gesagt",
    "Ich checke mal mein Bankkonto",
    # «основа+s» как настоящее слово: эти строки ловить нельзя
    "Er kaufte zwei Packs Bier",
    "Die Drehs für den Film dauerten drei Wochen",
    "Versuch es mal mit einem anderen Ansatz",
    # приставочные основы: правильные формы ловить нельзя
    "Ich widerrufe meine Aussage",
    "Ich erkläre dir den Weg",
    "Der Zug ist verspätet angekommen",
    "Ich erinnere mich an den Tag",
]
BAD = [
    "Ich bring dich zum Bahnhof hin",
    "Ich häng das Bild an die Wand auf",
    "Ich schüttel den Baum, um die Äpfel zu sammeln",
    "Ich brauch mal ne Auszeit vom Stress",
    "Ich hab keine Zeit",
    "Ich mach das später",
    "Gib mir mal nen Stift",
    "Das ist so'n Problem",
    "Morgen fahr ich weg",
    "Auf der Autobahn fahr ich schneller als auf normalen Straßen",
    "Das war echt ne miese Tour von dir",
    "Nach der Arbeit brauch ich eine Erfrischung",
    "Der Ladendiebstahl ist 'ne Straftat",
    "Morgen reis ich ab",
    "Ich pack meine Sachen für den Urlaub ein",
    "Wo stell ich das hin",
    "Lass mich, ich zieh mir gerade einen Film rein",
    # добавлено после блока 40
    "Ich check mal mein Bankkonto",
    "Das ist ja eine abgedrehte Idee, aber ich mags",
    "Ich machs später",
    # добавлено после блока 43: повелительное с приклеенным «es»
    "Versuchs mal mit einem anderen Ansatz",
    "Probiers doch einfach aus",
    # добавлено после блока 45
    "Ich widerruf meine Aussage",
    "Ich erklär dir den Weg",
    "Ich erinner mich an den Tag",
]


def hit(s: str) -> bool:
    return bool(VERB.search(s) or INVERTED.search(s)
                or ARTICLE.search(s) or CONTRACTION.search(s))


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

    # Ряд, который сам про усечение: слово базы — «ne», и пример
    # «Das ist gut, ne?» это и есть то, чему он учит. Чинить нельзя.
    found = [(i, w, e) for i, w, e in rows
             if hit(e) and w.lower() not in LEGIT_HEADWORDS]
    print(f"прочитано немецких примеров: {len(rows)}")
    print(f"с разговорным усечением: {len(found)}\n")
    for i, w, e in found:
        if VERB.search(e) or INVERTED.search(e):
            mark = "глагол"
        elif CONTRACTION.search(e):
            mark = "«es»"
        else:
            mark = "артикль"
        print(f"  {i:>6}  {w:<22} [{mark}]  {e}")


if __name__ == "__main__":
    main()
