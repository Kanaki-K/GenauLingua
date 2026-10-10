"""ГЕЙТ: пример начинается со строчной буквы.

Ни один из шести языков базы не начинает предложение со строчной буквы.
Значит у приметы нет законного остатка вовсе, и она может быть гейтом —
седьмым.

ОТКУДА ВЗЯЛАСЬ. В блоке 43 попался ряд `Bewunderer` (11188): турецкий
пример «**d**ünyanın her yerinde birçok hayranı var». Опечатка, которую
не видит ни одна другая примета: грамматика цела, слово ряда на месте,
смысл верен — просто первая буква строчная.

По правилу из блока 42 («признак не требует знания языка — пиши примету
сразу») замер сделан не после второго случая, а в тот же час.

ПЕРВОЕ ПРАВИЛО БЫЛО СЛИШКОМ ШИРОКИМ, И ЗАМЕР ЭТО ПОКАЗАЛ. «Первая
БУКВЕННАЯ литера строчная» даёт 22 попадания, но 21 из них законны:
фраза начинается с ЦИФРЫ, и следующее за ней слово строчное по правилам
языка.

    tr «5. sınıftayım», «100 euro çekmek istiyorum», «21. yüzyıl»
    ru «50 евро за пиццу? Это совершенно преувеличено»
    pl «50 euro za pizzę? To kompletnie przesadzone»

Во всех этих рядах и немецкий эталон начинается с цифры, то есть перевод
ведёт себя правильно. Правило сужено до «ПЕРВЫЙ символ — строчная буква»,
и остаток стал ровно 1 — тот самый `Bewunderer`.

ПОЧЕМУ ЭТО ГЕЙТ, А НЕ ПОДСКАЗКА. У правила нет ни одного законного
случая: язык, в котором предложение начинается со строчной, в базе не
представлен. После правки `Bewunderer` примета показывает 0 и падает при
любом новом попадании.

РАСПРЕДЕЛЕНИЕ ПО ЯЗЫКАМ У ШИРОКОГО ПРАВИЛА: tr 17, en 2, ru 1, uk 1,
pl 1, de 0. Турецкий впереди не из-за дефектов, а потому что в нём чаще
всего фраза начинается с числа («5. sınıftayım» вместо «Я в пятом
классе»). Немецкий чист полностью.

ПРЕДЕЛ. Примета смотрит только на первый символ примера. Строчная буква
после точки внутри фразы — другой класс, и его она не видит.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

LANGS = ("de", "en", "ru", "uk", "tr", "pl")


def starts_lowercase(sentence: str | None) -> bool:
    text_value = (sentence or "").strip()
    if not text_value:
        return False
    first = text_value[0]
    return first.isalpha() and first.islower()


def selfcheck() -> None:
    cases = [
        # ПЛОХО: предложение с строчной буквы
        ("dünyanın her yerinde birçok hayranı var", True),
        ("это было вчера", True),
        # ХОРОШО: начинается с цифры, следующее слово строчное по правилам
        ("5. sınıftayım", False),
        ("50 euro za pizzę? To kompletnie przesadzone", False),
        ("100 euro çekmek istiyorum", False),
        # ХОРОШО: обычное начало
        ("Dünyanın her yerinde birçok hayranı var", False),
        ("Ich gehe nach Hause", False),
    ]
    bad = 0
    for sentence, want in cases:
        got = starts_lowercase(sentence)
        if got != want:
            bad += 1
            print(f"САМОПРОВЕРКА ПРОВАЛЕНА: {sentence!r} -> {got}, ждали {want}")
    if bad:
        sys.exit(1)
    print("самопроверка правила: 7 из 7")


def main() -> None:
    if "--selfcheck" in sys.argv:
        selfcheck()
        return

    engine = create_engine(settings.DATABASE_URL_SYNC)
    with engine.connect() as conn:
        rows = conn.execute(text(
            "SELECT id, word_de, example_de, example_en, example_ru, "
            "example_uk, example_tr, example_pl FROM words ORDER BY id"
        )).mappings().all()

    hits = []
    for row in rows:
        for lang in LANGS:
            if starts_lowercase(row[f"example_{lang}"]):
                hits.append((row, lang))

    for row, lang in hits:
        print(f"{row['word_de']} ({row['id']}) {lang}: {row[f'example_{lang}']}")

    print(f"\nпримеров со строчной первой буквы: {len(hits)}")
    if hits:
        print("ГЕЙТ НЕ ПРОЙДЕН: предложение не может начинаться со строчной")
        sys.exit(1)
    print("гейт пройден: все примеры начинаются как положено")


if __name__ == "__main__":
    main()
