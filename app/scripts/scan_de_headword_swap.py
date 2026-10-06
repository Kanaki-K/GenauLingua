"""
Ищет эталон, в котором вместо СЛОВА РЯДА стоит ПОХОЖЕЕ ДРУГОЕ слово.

Зачем. Блок 64 дал это дважды:

    ряд  der Skalp
    de   Der Chirurg benutzte das Skalpell für die Operation

    ряд  der Quell
    de   Die Quelle des Flusses liegt in den Bergen

`Skalp` это скальп, `Skalpell` — скальпель. Слова похожи началом и не
связаны ничем больше. Четыре перевода из пяти пошли за эталоном и
написали про хирурга со скальпелем; только польский перевёл слово ряда.
Это та же семья, что `Holder` и `vermöbeln` из блоков 60 и 63, но
единственная её часть, которую можно поймать формально: похожее слово
видно по строению, а не по смыслу.

Как ищется. Берётся заголовок без артикля. Если в немецком примере нет
ни самого слова, ни его склонённой формы, ни составного слова с ним на
конце, — но есть слово, которое с заголовка НАЧИНАЕТСЯ и длиннее его
хотя бы на два знака, — значит в примере стоит что-то другое.

Отсюда же вторая, мягкая находка: слово в примере может оказаться
законным СОСТАВНЫМ с заголовком в начале — `Rubel` показан через
`Rubelkurs`, `Chrom` через `Chromteile`, `Parkett` через
`Parkettboden`. Это не ошибка: фраза верна, слово в ней есть. Но
ученику показывают не то слово, которое он учит, и такие ряды выведены
отдельным списком — решать владельцу, а не проверке.

Чего примета не умеет: второй случай блока 64 она как раз НЕ нашла.
Заголовок `der Quell`, в примере `Die Quelle des Flusses` — а `Quelle`
это `Quell` плюс `e`, то есть ровно законное окончание из списка ниже.
Отличить подмену от склонения тут нельзя никаким правилом: обе формы
существуют и различаются одной буквой. Ряд найден глазами и правится
вручную.

ПОЧЕМУ ПРИМЕТА ТОЛЬКО ПРО СУЩЕСТВИТЕЛЬНЫЕ. Общая версия — «в эталоне
вообще нет слова ряда» — построена и отброшена. По всей базе она дала
1537 попаданий, и настоящих среди них единицы. Причина в немецком
спряжении: `arbeiten` в примере стоит как `arbeite`, `anfangen` как
`fängt … an`, `halten` как `hält`, `nehmen` как `nimmt`. Чтобы свести
форму к заголовку, нужен морфологический разбор немецкого, а базе он
взяться негде: её собственный словарь даёт заголовки, но не их
спряжение. Для существительных склонение беднее и перечислимо, поэтому
примета работает только там.

    python -m app.scripts.scan_de_headword_swap
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

WORD = re.compile(r"[A-Za-zÄÖÜäöüß]+")
ARTICLES = ("der ", "die ", "das ")

# Окончания склонения и уменьшительные. Список пришлось дополнять
# дважды: сначала не было `sse`/`se` (и девять законных форм на -nisse
# шли как дефекты), потом `ien`/`ia` (Mineralien, Prinzipien, Indizien).
ENDINGS = {
    "", "e", "en", "er", "es", "s", "n", "em", "ern", "nen",
    "in", "innen", "chen", "lein", "se", "sse", "ses", "ien", "ia",
    "a", "i", "ten", "te",
}

MIN_LEN = 4        # короткие заголовки дают слишком много совпадений
MIN_EXTRA = 2      # насколько слово должно быть длиннее заголовка


def bare(word: str) -> str:
    low = (word or "").lower()
    for a in ARTICLES:
        if low.startswith(a):
            return (word or "")[len(a):].strip()
    return (word or "").strip()


def has_headword(hw: str, tokens: list[str]) -> bool:
    h = hw.lower()
    forms = {h + e for e in ENDINGS}
    for t in tokens:
        tl = t.lower()
        if tl in forms or tl.endswith(h):
            return True
    return False


def longer_words(hw: str, tokens: list[str]) -> list[str]:
    h = hw.lower()
    return [t for t in tokens
            if t.lower().startswith(h)
            and len(t) >= len(hw) + MIN_EXTRA
            and t.lower()[len(hw):] not in ENDINGS]


def selfcheck() -> None:
    cases = [
        # слово ряда подменено похожим
        ("Skalp", "Der Chirurg benutzte das Skalpell für die Operation",
         ["Skalpell"]),
        # законная форма множественного — не трогать
        ("Gefängnis", "Die Gefängnisse sind oft voll", []),
        ("Mineral", "Der Körper braucht Mineralien und Vitamine", []),
        ("Prinzip", "Ich halte mich an meine Prinzipien", []),
        # составное с заголовком в начале — мягкий случай
        ("Rubel", "Der Rubelkurs ist gestern gestiegen", ["Rubelkurs"]),
        # составное с заголовком на конце — законно
        ("Transfusion", "Der Patient brauchte eine Bluttransfusion", []),
        # слово стоит как есть
        ("Minibar", "Die Minibar im Hotelzimmer ist teuer", []),
    ]
    for hw, ex, want in cases:
        toks = WORD.findall(ex)
        got = [] if has_headword(hw, toks) else longer_words(hw, toks)
        if got != want:
            print(f"САМОПРОВЕРКА УПАЛА: {hw} в {ex!r} дало {got}, "
                  f"а надо {want}")
            sys.exit(1)
    print(f"самопроверка: {len(cases)} пар заголовок-пример разобраны "
          f"верно\n")


def main() -> None:
    selfcheck()
    engine = create_engine(settings.DATABASE_URL_SYNC)
    with engine.connect() as conn:
        rows = conn.execute(text(
            "SELECT id, word_de, example_de FROM words "
            "WHERE example_de IS NOT NULL AND pos = 'NOUN' "
            "ORDER BY id")).all()

    print(f"прочитано рядов NOUN: {len(rows)}")

    swapped, compound = [], []
    for wid, word, ex in rows:
        hw = bare(word)
        if len(hw) < MIN_LEN:
            continue
        toks = WORD.findall(ex or "")
        if has_headword(hw, toks):
            continue
        got = longer_words(hw, toks)
        if not got:
            continue
        # составное ли это слово: заголовок плюс ещё один корень,
        # то есть остаток сам начинается с согласной и не короток
        rest = got[0].lower()[len(hw):]
        (compound if len(rest) >= 4 else swapped).append(
            (wid, word, got, ex))

    print(f"эталонов с подменённым словом: {len(swapped)}")
    for wid, word, got, ex in swapped:
        print(f"  {wid:>6}  {word:<24} [{', '.join(got)}]")
        print(f"          {ex}")

    print(f"\nэталонов, где слово показано только внутри составного: "
          f"{len(compound)}")
    print("(не дефект: фраза верна и слово в ней есть, но ученику "
          "показывают не его)")
    for wid, word, got, ex in compound:
        print(f"  {wid:>6}  {word:<24} [{', '.join(got)}]")
        print(f"          {ex}")


if __name__ == "__main__":
    main()
