"""ПРИМЕТА: в немецком примере есть вторая часть, а в переводе её нет.

ОТКУДА ВЗЯЛАСЬ. В блоке 42 из четырнадцати правок восемь были польскими,
и пять из них — подмены целиком. Но подмены были особого вида: польская
фраза не перевод немецкой, а САМОСТОЯТЕЛЬНОЕ предложение с тем же словом
(`Zimt` — «добавь корицы в тесто» вместо «люблю корицу в кофе»,
`Nachttisch` — «очки лежат на столике» вместо «книга лежит на моём»).
Это другая гипотеза, чем «польский переводили отдельным прогоном»:
похоже, часть польских примеров СОЧИНЯЛИ по заголовку, а не переводили с
немецкого.

КАК ЭТО ЗАМЕРИТЬ, НЕ СРАВНИВАЯ СЛОВА РАЗНЫХ ЯЗЫКОВ. Признак чисто
структурный и считается по ПУНКТУАЦИИ: в немецком примере есть запятая
(то есть он из двух частей), а в примере одного языка запятой нет вовсе.

ПОЧЕМУ ПРИМЕТА ОГРАНИЧЕНА СЛАВЯНСКИМИ. Замер по всем пяти языкам:

    рядов с запятой в немецком: 1339
    без запятой: tr 843, en 818, uk 214, pl 217, ru 199

У английского и турецкого отсутствие запятой — НОРМА, и в этом вся суть:
английское определительное предложение запятой не требует («a bizarre
situation nobody expected»), а турецкий строит оборот причастием, где
запятая не нужна вовсе («Gitmeden önce», «Bildiğim kadarıyla»). Правило,
которое ловит две трети языка, мерит язык, а не базу.

Русский, украинский и польский ставят запятую при подчинении так же, как
немецкий. Поэтому примета смотрит ТОЛЬКО на них и только когда язык
промахнулся ОДИН:

    только ru — 0 рядов
    только uk — 1 ряд
    только pl — 15 рядов

ЗАМЕР: 16 рядов, и разбор глазами делит их ровно пополам.

ВОСЕМЬ ДЕФЕКТОВ — потеряна вторая часть эталона или фраза подменена:

    gefordert    (7499)  потеряно «es gibt viel zu tun»
    überbewertet (7978)  потеряно «ehrlich gesagt nicht so gut»
    Zier         (8532)  потеряно «das brauchen wir nicht», добавлена ваза
    sinnlos     (11122)  потеряно «lass es einfach sein»
    wegstecken  (11529)  «mnie posłuchaj» вместо «wir sprechen jetzt»
    entmutigen  (11550)  подмена целиком: первая неудача вместо его критики
    kitschig    (14614)  подмена целиком: фигурка на полке вместо комнаты
    Saustall    (18388)  потеряно «so dreckig ist es»

Исправлены `fix_pl_comma_clause.py`.

ВОСЕМЬ ЗАКОННЫХ, И ВСЕ ОДНОГО ВИДА: польский соединяет то, что немецкий
разделяет запятой, — союзом «i», «ani» или сложным словом.

    344   «Poproszę szklankę wody» при «Ein Glas Wasser, bitte»:
          «poproszę» само несёт вежливость, отдельного «bitte» нет
    1310  то же
    11120 «...i szybko wybacza» при «..., deshalb verzeiht er schnell»
    12686 «Nie ma kręgosłupa ani odwagi» при «kein Rückgrat, keinen Mut»
    12733 «...i muszę się położyć»
    16088 «czarno-czerwono-złota» при «schwarz, rot und gold»
    18219 «...i jest strasznie gorąco»
    8548  uk: тире вместо запятой — законный знак в этом месте

Поэтому примета — ПОДСКАЗКА с остатком 8, а не гейт.

**Примета нашла дефект в блоке, который я уже закрыл.** `sinnlos` (11122)
— ряд 8103, блок 41; я прочёл его глазами и потерю второй части не
увидел. Замер увидел. Это прямой аргумент за то, чтобы структурные
приметы писать РАНЬШЕ, а не после того, как класс наберёт пять случаев.

ПРЕДЕЛ ПРИМЕТЫ. Она видит только полное отсутствие запятой. Если вторая
часть потеряна, но запятая осталась от чего-то другого, примета молчит.
И она ничего не знает о случаях, где немецкий обходится без запятой, —
а `Zimt` и `Turnschuh` из блока 42 были именно такими.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

LANGS = ("en", "ru", "uk", "tr", "pl")
# Только те языки, что ставят запятую при подчинении так же, как немецкий
SLAVIC = ("ru", "uk", "pl")
EXPECTED = 8


def selfcheck() -> None:
    """Проверка самого правила на размеченных руками парах."""
    cases = [
        # ПЛОХО: вторая часть эталона потеряна
        ("Dieser sinnlose Streit führt zu nichts, lass es einfach sein",
         "Ta bezsensowna kłótnia do niczego nie prowadzi", True),
        ("Ich bin heute sehr gefordert bei der Arbeit, es gibt viel zu tun",
         "Dziś jestem w pracy bardzo obciążony", True),
        # ХОРОШО: запятая есть, претензий нет
        ("Dieser sinnlose Streit führt zu nichts, lass es einfach sein",
         "Ta kłótnia do niczego nie prowadzi, odpuść", False),
        # ХОРОШО: в эталоне запятой нет — примета не её дело
        ("Ich mag Zimt im Kaffee", "Lubię cynamon w kawie", False),
    ]
    bad = 0
    for german, other, want in cases:
        got = "," in german and "," not in other
        if got != want:
            bad += 1
            print(f"САМОПРОВЕРКА ПРОВАЛЕНА: {other!r} -> {got}, ждали {want}")
    if bad:
        sys.exit(1)
    print("самопроверка правила: 4 из 4")


def main() -> None:
    if "--selfcheck" in sys.argv:
        selfcheck()
        return

    engine = create_engine(settings.DATABASE_URL_SYNC)
    with engine.connect() as conn:
        rows = conn.execute(text(
            "SELECT id, word_de, level, example_de, example_en, example_ru, "
            "example_uk, example_tr, example_pl FROM words "
            "WHERE example_de LIKE '%,%' ORDER BY id"
        )).mappings().all()

    hits = []
    for row in rows:
        missing = [
            lang for lang in LANGS
            if "," not in (row[f"example_{lang}"] or "")
        ]
        if len(missing) == 1 and missing[0] in SLAVIC:
            hits.append((row, missing[0]))

    for row, lang in hits:
        print(f"{row['word_de']} ({row['id']}, {row['level']})  язык {lang}")
        print(f"    de  {row['example_de']}")
        print(f"    {lang}  {row[f'example_{lang}']}")

    print(f"\nрядов с запятой в немецком: {len(rows)}")
    print(f"всего: {len(hits)}")
    print(f"ожидаемый остаток: {EXPECTED} — разбор в docstring")
    if len(hits) != EXPECTED:
        print("ВНИМАНИЕ: остаток изменился — разбери и обнови docstring")
        sys.exit(1)


if __name__ == "__main__":
    main()
