"""ВТОРОЙ ПРОХОД, блок 1 (ряды 1–200): правки, найденные глазами.

Первый проход читал эти ряды, когда глаз ещё не знал классов, найденных
в блоках 60–72. Второй проход — те же ряды, сегодняшним глазом.

НАЙДЕНО 26 ЯЧЕЕК В 200 РЯДАХ. И это не хвост базы: это ряды с рангами
частотности от 1 до 267, то есть слова, которые учащийся видит первыми
и чаще всего. Девять из них — другая фраза или противоположный смысл:

    wird   de «Morgen wird es kalt»   tr «Yarın hava güzel olacak»
                                      (погода будет ХОРОШАЯ)
    war    de «Ich war gestern krank» tr «Geçen yıl öğretmen oldum»
                                      (в прошлом году стал учителем)
    wir    de «Wir gehen nach Hause»  tr «Biz de sinemaya geliyoruz»
                                      (мы тоже идём в кино)
    eine   de «Das ist eine Katze»    pl «Mam jedną siostrę»
                                      (у меня одна сестра)
    so     de «Das ist so»            en «It's so cold today!»

ДВА РЯДА — МОЙ СОБСТВЕННЫЙ НЕДОДЕЛАННЫЙ РЕМОНТ. Ряды 1687 (`ich`) и
1328 (`du`) я правил час назад по выводу `example_person_mismatch`.
Примета показала английскую и украинскую ячейки — я их и исправил, а
турецкую и польскую не тронул, потому что примета их не проверяет:
турецкий опускает местоимение, и определить лицо по нему она не может.

Урок жёсткий и его стоит записать: **если примета нашла дефект в одной
ячейке ряда, читать надо ВЕСЬ ряд.** Примета показывает там, где умеет
смотреть, а дефект сидит там, где его положили.

КЛАСС, КОТОРЫЙ ОСТАЁТСЯ СПОРНЫМ. Заголовки-артикли (`ein`, `eine`,
`einen`, `einem`) переведены как «один, какой-то, неопределённый
артикль», а примеры были «У меня есть ОДНА книга», «Это КАКАЯ-ТО
кошка». Немецкое «Ich habe ein Buch» значит «у меня есть книга», а не
«одна книга», так что перевод учил неверному — и это исправлено, как
уже было сделано в блоке 68 для ряда 204.

Но у правки есть цена, и её надо знать: в русском и украинском артикля
нет, поэтому после правки в примере не остаётся НИ ОДНОГО слова из
перевода. `main_meaning` в таком случае берёт первое — «один», — и на
карточке будет показано «один» при примере «У меня есть книга».
Сделать разом верным и смысл, и связность карточки нельзя: мешает
отсутствие артикля в языке. Вынесено владельцу.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ── подменённая или противоположная фраза ─────────────────────
    (13266, "example_tr",
     "Yarın hava güzel olacak",
     "Yarın hava soğuk olacak",
     "эталон «Morgen wird es kalt» — холодно, а не хорошая погода"),
    (13242, "example_tr",
     "Geçen yıl öğretmen oldum",
     "Dün hastaydım",
     "эталон «Ich war gestern krank» — вчера болел"),
    (1045, "example_tr",
     "Biz de sinemaya geliyoruz",
     "Biz eve gidiyoruz",
     "эталон «Wir gehen nach Hause» — идём домой, а не в кино"),
    (13233, "example_pl",
     "Mam jedną siostrę",
     "To jest kot",
     "эталон «Das ist eine Katze» — это кошка, а не «у меня одна сестра»"),
    (843, "example_en",
     "It's so cold today!",
     "That's how it is",
     "эталон «Das ist so»; про холод там нет"),

    # ── мой недоделанный ремонт: примета показала не все ячейки ───
    (1687, "example_tr",
     "Beni görüyor musun",
     "Ben zaten oldukça yorgunum",
     "эталон «Ich bin schon ziemlich müde»; примета турецкий не проверяет"),
    (1687, "example_pl",
     "Widzisz mnie?",
     "Jestem już całkiem zmęczony",
     "то же"),
    (1328, "example_en",
     "I see you",
     "Are you coming along tonight?",
     "эталон «Kommst du heute Abend mit?»"),
    (1328, "example_tr",
     "Seni görüyorum",
     "Bu akşam bizimle geliyor musun?",
     "то же"),
    (1328, "example_pl",
     "Widzę ciebie",
     "Czy idziesz z nami dziś wieczorem?",
     "то же"),

    # ── заголовок-артикль переведён числительным ──────────────────
    (13223, "example_ru",
     "У меня есть одна книга",
     "У меня есть книга",
     "«ein Buch» это книга, а не одна книга"),
    (13223, "example_uk",
     "У мене є одна книга",
     "У мене є книга",
     "то же"),
    (13223, "example_pl",
     "Mam jedną książkę",
     "Mam książkę",
     "то же"),
    (13233, "example_ru",
     "Это какая-то кошка",
     "Это кошка",
     "«eine Katze» это кошка; «какая-то» сдвигает в неопределённое местоимение"),
    (13233, "example_uk",
     "Це якась кішка",
     "Це кішка",
     "то же"),
    (13251, "example_ru",
     "Я покупаю одно яблоко",
     "Я покупаю яблоко",
     "«einen Apfel» это яблоко, а не одно яблоко"),
    (13251, "example_pl",
     "Kupuję jedno jabłko",
     "Kupuję jabłko",
     "то же"),
    (13286, "example_ru",
     "Я говорю с одним другом",
     "Я говорю с другом",
     "«mit einem Freund» это с другом, а не с одним другом"),
    (13286, "example_uk",
     "Я говорю з одним другом",
     "Я говорю з другом",
     "то же"),
    (13286, "example_pl",
     "Rozmawiam z jednym kolegą",
     "Rozmawiam z kolegą",
     "то же"),

    # ── потерянное и добавленное слово ────────────────────────────
    (180, "example_tr",
     "Bu kadın çok hoş",
     "Bu kadın hoş",
     "«çok» в эталоне нет: «Die Frau ist nett»"),
    (13274, "example_pl",
     "Chcę już iść do domu",
     "Chcę iść do domu",
     "«już» в эталоне нет"),
    (121, "example_uk",
     "Каву, будь ласка",
     "Одну каву, будь ласка",
     "потеряно «ein»: в русском и польском оно есть"),
    (240, "example_pl",
     "Powiem wam coś ciekawego",
     "Powiem wam coś",
     "«ciekawego» в эталоне нет: «Ich sage euch was»"),
    (13302, "example_tr",
     "İki ekmek istiyorum, lütfen",
     "İki küçük ekmek istiyorum, lütfen",
     "«Brötchen» это булочка, а «ekmek» без уточнения — хлеб"),
    (13315, "example_ru",
     "Я купил пиццу и уже съел половину от неё",
     "Я купил пиццу и уже съел половину",
     "«половину от неё» по-русски не говорят"),
]


def main() -> None:
    apply_mode = "--apply" in sys.argv
    engine = create_engine(settings.DATABASE_URL_SYNC)
    ok: list[tuple[int, str, str, str, str]] = []
    skipped: list[tuple[int, str, str | None]] = []
    with engine.connect() as conn:
        for wid, col, was, now, why in FIXES:
            cur = conn.execute(
                text(f"SELECT {col} FROM words WHERE id = :i"), {"i": wid}
            ).scalar()
            if (cur or "").strip() != was:
                skipped.append((wid, col, cur))
            else:
                ok.append((wid, col, was, now, why))

    print(f"=== правок {len(FIXES)}, совпало {len(ok)}, пропущено {len(skipped)} ===\n")
    for wid, col, cur in skipped:
        print(f"ПРОПУСК id={wid} {col}: в базе {cur!r}")

    if not apply_mode:
        for wid, col, was, now, why in ok:
            print(f"id={wid} {col}")
            print(f"  было:  {was}")
            print(f"  стало: {now}")
        print("\nсухой прогон. применить: --apply")
        return

    with engine.begin() as conn:
        for wid, col, _, now, _ in ok:
            conn.execute(
                text(f"UPDATE words SET {col} = :v WHERE id = :i"),
                {"v": now, "i": wid},
            )
    print(f"\nприменено: {len(ok)}")

    bad = 0
    with engine.connect() as conn:
        for wid, col, _, now, _ in ok:
            cur = conn.execute(
                text(f"SELECT {col} FROM words WHERE id = :i"), {"i": wid}
            ).scalar()
            if (cur or "").strip() != now:
                bad += 1
                print(f"НЕ ЗАПИСАЛОСЬ id={wid} {col}: {cur!r}")
    print(f"самопроверка: не записалось {bad}")


if __name__ == "__main__":
    main()
