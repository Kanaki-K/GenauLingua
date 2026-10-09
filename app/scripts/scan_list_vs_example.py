"""
Примета: ни одно значение из ячейки перевода не встречается в своём примере.

Это формальный след правила §8 — показано = озвучено = слово в примере.
Если в ячейке «сокол», а пример про улитку, человек видит на карточке одно
слово, слышит его же и читает фразу про другое. Ровно это и нашлось: ряд
`Schnecke` (15563) унаследовал все пять списков от соседнего `Falke`
(15562), а примеры у него свои и верные.

ЧЕМ ЗАМЕРЕН ПОРОГ. Прямая проверка по всем частям речи даёт 154 ряда, и
почти все ложные: у глаголов в списке инфинитивы, которых в примере не
бывает, а русское чередование основы рвёт сравнение — «писать» и «пишу»
совпадают на двух буквах. По существительным остаётся 35.

Отсечка по числу языков выбрана замером, а не на глаз. Три языка дают 13
рядов, четыре — 4, пять — 1. На тринадцати ряды ещё читаются глазами, и
среди них оба настоящих дефекта; на четырёх `Arche` уже теряется.

ОТСЕЧКА, КОТОРУЮ ПРИШЛОСЬ ОТМЕНИТЬ. Сначала требовалось, чтобы в ячейке
было два и более значения: при одном `main_meaning` всё равно вернёт его, и
расхождения человек не увидит. Это выглядело разумно и давало 8 рядов — но
теряло `Schnecke`, самый грубый дефект класса, потому что три его списка
из одного слова. Работу этой отсечки сделало исправленное сравнение основ
(`_stem_in_loose`): оно убрало 35 рядов до 13 и убрало именно ложные.

ЧТО ОСТАЛОСЬ И ПОЧЕМУ ЭТО НЕ ДЕФЕКТЫ (5 рядов):

    Daumen  (1323)  «Ich drücke dir die Daumen» — идиома. Русское
        «Скрещиваю за тебя пальцы» и украинское «Тримаю за тебе кулачки»
        верны, и заголовок в них потерян неизбежно.
    Appetit (1153)  «Guten Appetit!» — то же: «Смачного!», «Afiyet olsun!».
    Laus    (13009) «вошь» и «вши» — словоизменение с чередованием.
    Gott    (13811) «Бог» и «Боже» — три буквы, поблажке решать нельзя.
    Tänze   (14744) заголовок стоит во множественном числе вместо `Tanz`.
        Это класс «форма слова вместо заголовка», он в списке решений
        владельца, а не правка текста.

ЧТО ПРИМЕТА НАЙТИ НЕ МОЖЕТ. Многословное значение проверяется по самому
длинному слову — так задумано в `main_meaning`, чтобы «leczenie
sanatoryjne» опознавалось по «sanatoryjne». Поэтому ряд `Verdeck` с
украинским «складний дах» и примером про «дах» в примету попадает, хотя
слово на месте. Вреда нет: первое значение там и так верное.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings
from app.services.language_service import (
    _TOKEN_RE,
    _VARIANT_SPLIT_RE,
    _fold,
    _stem_in,
    _stem_in_loose,
)

LANGS = ("en", "ru", "uk", "tr", "pl")
MIN_LANGS = 3


def misses(translation: str | None, example: str | None) -> bool:
    """Ни одно значение ячейки не нашлось в примере — ни в какой форме."""
    if not translation or not example:
        return False
    parts = [p.strip() for p in _VARIANT_SPLIT_RE.split(translation) if p.strip()]
    tokens = [_fold(t) for t in _TOKEN_RE.findall(example)]
    for part in parts:
        words = sorted(_TOKEN_RE.findall(part), key=len, reverse=True)
        if not words:
            continue
        if _stem_in(words[0], tokens) or _stem_in_loose(words[0], tokens):
            return False
    return True


def selfcheck() -> bool:
    """Примета должна отличать подмену от словоизменения."""
    ok = True

    # Так было в ряду `Schnecke`: список унаследован от соседнего `Falke`
    if not misses("сокол", "Улитка медленно движется по дорожке"):
        print("  ПЛОХО: подменённый список не пойман")
        ok = False

    # А это обычное словоизменение, трогать нечего
    if misses("шина, рельс", "После аварии он носил шину на руке"):
        print("  ПЛОХО: словоизменение принято за дефект")
        ok = False

    # Падежное окончание четырёхбуквенного слова тоже не дефект
    if misses("вода", "Я пью воду"):
        print("  ПЛОХО: падежное окончание принято за дефект")
        ok = False

    # Немецкое словосложение: основа внутри слова
    if misses("gehen", "Ich will weggehen"):
        print("  ПЛОХО: основа внутри составного слова не найдена")
        ok = False

    print("  примета отличает подмену от словоизменения" if ok else "  примета сломана")
    return ok


def main() -> None:
    if not selfcheck():
        sys.exit(1)

    engine = create_engine(settings.DATABASE_URL_SYNC)
    cols = ", ".join(f"translation_{l}, example_{l}" for l in LANGS)
    with engine.connect() as conn:
        rows = (
            conn.execute(
                text(f"SELECT id, word_de, {cols} FROM words WHERE pos = 'NOUN'")
            )
            .mappings()
            .all()
        )

    print(f"\n=== существительных: {len(rows)} ===\n")
    hits = []
    for r in rows:
        bad = [l for l in LANGS if misses(r[f"translation_{l}"], r[f"example_{l}"])]
        if len(bad) >= MIN_LANGS:
            hits.append((len(bad), r["id"], r["word_de"], bad))

    for n, wid, word, bad in sorted(hits, reverse=True):
        print(f"  {n} яз.  {wid:6} {word:24} {', '.join(bad)}")
    print(f"\nвсего: {len(hits)}")


if __name__ == "__main__":
    main()
