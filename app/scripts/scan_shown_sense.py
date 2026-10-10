"""ПРИМЕТА: карточка показывает не то значение, о котором её пример.

ОТКУДА ВЗЯЛАСЬ. Класс «в примере слово не из своего списка» всплывал три
блока подряд: три случая в блоке 37, пять в блоке 38, и в блоке 39 замер
назначен по правилу «повторилось дважды — замеряй по всей базе».

ПЕРВОЕ ПРАВИЛО ОТБРОШЕНО, И ЭТО ВАЖНЕЕ УЛОВА. Прямое «ни один вариант
ячейки не нашёлся в примере» даёт **4332 ячейки** — семь процентов базы.
Разбор по части речи показал, что правило мерит не базу, а МАТЧЕР:

    VERB        3418 из 12839 ячеек  26.6%
    PRONOUN       77 из   592        13.0%
    ADJECTIVE    332 из 10237         3.2%
    NOUN         411 из 28636         1.4%

У глаголов промах в двадцать раз чаще, чем у существительных, — потому
что условие `len(head) - common <= 3` предполагает, что словарная форма
длиннее общей основы не больше чем на три буквы. Для существительных так
и есть, для славянского и турецкого инфинитива — нет: «одеваться» и
«одеваюсь» совпадают на пяти буквах из девяти.

ВТОРОЕ ПРАВИЛО — ПЕРЕКРЁСТНОЕ, И ОНО РАБОТАЕТ. Шесть языков одного ряда
проверяют друг друга: если в трёх и более языках пример указал на НЕ
первый вариант, а в этом языке не нашлось ничего, то первый вариант здесь
почти наверняка не то значение. Это тот же приём, что «два ряда на одно
слово проверяют друг друга», применённый внутри ряда.

ЗАМЕР ДАЛ 84 ЯЧЕЙКИ, и разбор глазами разделил их надвое:

    19 — ТЕКСТ В ПОРЯДКЕ, нужное значение в примере стоит, матчер его не
         видит («сходиться» при примере «Цифры не сходятся»);
    65 — пример написан словом, которого в списке нет вовсе.

Первые 19 закрыты правкой `main_meaning`: выбор ЛУЧШЕГО совпадения
вместо первого плюс длинный хвост, разрешённый только после строгого
сравнения. Это сдвинуло 538 ячеек по всей базе в сторону «показывается
то слово, что в примере». Подробности и замеры — в самой функции и в
`tests/test_card_contract.py`.

ОСТАТОК 74. Он больше 65, потому что правка матчера изменила и то, какой
индекс находят соседние языки, — перекрёстный признак стал строже. После
правки матчера остаток был 75; `Veilchen` (tr — «menekşe», фиалка, на
примере о синяке под глазом) закрыт правкой блока 39, а `kahl` (ru и uk)
— правкой блока 40, где он попался в чтении сам, а `statuieren` (tr) —
правкой блока 41. Все три раза примета не поверила моему числу и упала
первой — за этим в каждой из них и стоит ожидаемый остаток.
Остаток не мусор, его надо разбирать: это ряды, где пример написан
синонимом, которого нет в своём списке. Три характерных вида:

    пример про другое значение многозначного слова:
        `wandeln`   (7650) ru «гуляет» при списке «изменять, превращать…»
        `einbuchten`(15766) ru «вдаётся в сушу» при «посадить в тюрьму…»
        `versetzen` (8630) ru «наносит удар» при «переводить…»
    пример написан синонимом, а нужное слово в списке ЕСТЬ, но короче
    порога основы — так был устроен `kahl` (7923): «голый» и «голая»
    совпадают лишь на трёх буквах при пороге четыре. Снять это
    послаблением матчера для коротких основ ПРОБОВАЛОСЬ и отложено —
    замер разобран в `fix_pass2_block_40.py`: 262 ячейки, почти все
    видовые пары, но счёт завышен и нашлась порча (`aufeinander` 13511).
    Пока такие ряды правятся со стороны списка
    самое длинное слово значения не то, по которому опознавать:
        `Bescheid`   (98) en «decision» при значении «official decision»:
                    `head_of` берёт самое длинное слово, а у «official»
                    и «decision» длина равна, и выбор решает порядок букв

Последний вид — названный предел `head_of`, а не дефект базы.

ПРЕДЕЛ ПРИМЕТЫ. Она молчит, если в ряду меньше четырёх языков со
списками из двух и более значений, и если соседние языки тоже указали на
первый вариант. То есть ряд, где ВСЕ шесть языков сбились одинаково, она
не увидит по устройству.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings
from app.services.language_service import (
    _TAIL_LOOSE,
    _TAIL_STRICT,
    _TOKEN_RE,
    _VARIANT_SPLIT_RE,
    _fold,
    _stem_in_loose,
    _stem_tail,
)

LANGS = ("en", "ru", "uk", "tr", "pl")
MIN_OTHERS = 3
EXPECTED = 71


def head_of(part: str) -> str:
    words = sorted(_TOKEN_RE.findall(part), key=len, reverse=True)
    return words[0] if words else ""


def chosen_index(parts: list[str], example: str) -> int | None:
    """Какой по счёту вариант выберет `main_meaning`, или None — не нашёл."""
    tokens = [_fold(t) for t in _TOKEN_RE.findall(example)]
    scored = []
    for index, part in enumerate(parts):
        head = head_of(part)
        if not head:
            continue
        tail = _stem_tail(head, tokens)
        if tail is not None:
            scored.append((tail, index))
    for limit in (_TAIL_STRICT, _TAIL_LOOSE):
        fit = sorted(s for s in scored if s[0] <= limit)
        if fit:
            return fit[0][1]
    loose = [
        i for i, p in enumerate(parts)
        if head_of(p) and _stem_in_loose(head_of(p), tokens)
    ]
    return loose[0] if len(loose) == 1 else None


def selfcheck() -> None:
    cases = [
        # ПЛОХО: пример указывает на второе значение, матчер его найдёт
        (["быть верным", "сходиться", "голосовать"], "Цифры не сходятся", 1),
        (["надевать", "одеваться", "притягивать"], "Я быстро одеваюсь", 1),
        # ХОРОШО: точное совпадение не должно уступать приблизительному
        (["частенько", "часто", "нередко"], "Я часто хожу в кино", 1),
        (["moralnosc", "morale", "etyka"], "Jego morale jest dobre", 1),
        # Не нашлось вовсе — это и есть улов приметы
        (["лысый", "оголённый"], "Гора была совсем голая", None),
    ]
    bad = 0
    for parts, example, want in cases:
        got = chosen_index(parts, example)
        if got != want:
            bad += 1
            print(f"САМОПРОВЕРКА ПРОВАЛЕНА: {example!r} -> {got}, ждали {want}")
    if bad:
        sys.exit(1)
    print("самопроверка правила: 5 из 5")


def main() -> None:
    if "--selfcheck" in sys.argv:
        selfcheck()
        return

    engine = create_engine(settings.DATABASE_URL_SYNC)
    with engine.connect() as conn:
        rows = conn.execute(text(
            "SELECT id, word_de, level, translation_ru, translation_en, "
            "translation_uk, translation_tr, translation_pl, example_de, "
            "example_ru, example_en, example_uk, example_tr, example_pl "
            "FROM words ORDER BY id"
        )).mappings().all()

    hits = []
    for row in rows:
        picked = {}
        for lang in LANGS:
            cell = row[f"translation_{lang}"]
            example = row[f"example_{lang}"]
            if not cell or not example:
                continue
            parts = [p.strip() for p in _VARIANT_SPLIT_RE.split(cell) if p.strip()]
            if len(parts) < 2:
                continue
            picked[lang] = (chosen_index(parts, example), parts, example)
        for lang, (index, parts, example) in picked.items():
            if index is not None:
                continue
            others = [
                j for other, (j, _, _) in picked.items()
                if other != lang and j is not None
            ]
            if len(others) >= MIN_OTHERS and all(j >= 1 for j in others):
                hits.append((row, lang, parts, example, others))

    for row, lang, parts, example, others in hits:
        print(f"{row['word_de']} ({row['id']}, {row['level']})  язык {lang}")
        print(f"    de        {row['example_de']}")
        print(f"    список    {' | '.join(parts)}  -> показывается «{parts[0]}»")
        print(f"    пример    {example}")
        print(f"    в других языках пример указал на вариант {others}")

    print(f"\nвсего: {len(hits)}")
    print(f"ожидаемый остаток: {EXPECTED} — разбор видов в docstring")
    if len(hits) != EXPECTED:
        print("ВНИМАНИЕ: остаток изменился — разбери и обнови docstring")
        sys.exit(1)


if __name__ == "__main__":
    main()
