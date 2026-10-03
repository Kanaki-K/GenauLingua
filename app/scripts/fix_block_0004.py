"""
Сплошная вычитка, блок 4: ряды 301–400 по рангу частотности.

Правок вдвое меньше, чем в первых трёх блоках: самые частые служебные
слова уже пройдены, а дальше идут существительные и глаголы, которые
переводились аккуратнее.

Находки:

* `kriegen` — польское «Dostaję głodu» так не говорят, украинский пример
  про новую работу, турецкий про купленный телефон. Немецкий — «я начинаю
  хотеть есть».
* `eben` — английский, украинский и турецкий взяли значение «только что»
  («I just arrived»), а немецкий пример про «тогда сделаем это завтра».
* `Entschuldigung` — турецкий спрашивает, где станция, а немецкий где
  туалет. Это осталось с прошлой партии: тогда я поправил польский и
  пропустил турецкий.
* `Sorge` — украинский «Дякую тобі за турботу» вместо «не волнуйся».
* `vier` — «Нас четверо людей»: «людей» лишнее.

    python -m app.scripts.fix_block_0004            # показать
    python -m app.scripts.fix_block_0004 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# (id, колонка, что стоит сейчас, на что менять, зачем)
FIXES: list[tuple[int, str, str, str, str]] = [

    # --- пример переводит другую фразу ----------------------------------------
    (900, "example_tr", "Akşam seni ararım", "Bir daire arıyorum",
     "взято другое значение: «позвоню» вместо «ищу»"),
    (1739, "example_en", "The lamp hangs above the table",
     "The book is up on the shelf",
     "в немецком книга на полке, а не лампа над столом"),
    (13354, "example_pl", "Mamy cztery bilety do kina", "Jest nas czworo",
     "в немецком «нас четверо», а не билеты"),
    (221, "example_pl", "Wreszcie jesteś", "Wreszcie jest tutaj",
     "в немецком «он наконец здесь», а не «ты»"),
    (234, "example_pl", "To mój pierwszy dzień w pracy",
     "To pierwsza lekcja", "в немецком первый урок, а не день на работе"),
    (338, "example_uk", "Вчора ми були в кіно", "Вчора я був у місті",
     "в немецком «я в городе», а не «мы в кино»"),
    (651, "example_tr", "Komşumuz çok kibar bir kadın", "O çok kibar",
     "в немецком «она милая», а не про соседку"),
    (10040, "example_pl", "Powiedz mi prawdę", "To jest prawda",
     "в немецком утверждение, а не просьба"),
    (10041, "example_pl", "Nie odważył się jej zapytać",
     "Po prostu się nie odważę",
     "в немецком «я просто не осмеливаюсь», а не «он не решился»"),
    (2948, "example_uk", "Не покидай мене зараз", "Я покидаю місто",
     "в немецком «я покидаю город»"),
    (1070, "example_uk", "Не треба показувати пальцем",
     "Покажи мені дорогу", "в немецком «покажи мне дорогу»"),
    (13355, "example_pl", "To są ludzie którym ufam",
     "Z tymi nie rozmawiam",
     "в немецком «с теми я не разговариваю»; и запятая пропущена"),
    (858, "example_uk", "Було задоволення з тобою поговорити",
     "Це було велике задоволення",
     "в немецком «это было большое удовольствие»"),
    (202, "example_en", "I just arrived",
     "Then we'll just do it tomorrow",
     "взято другое значение: «только что» вместо «тогда уж»"),
    (202, "example_uk", "Я щойно прибув", "Тоді зробимо це просто завтра",
     "взято другое значение: «только что» вместо «тогда уж»"),
    (202, "example_tr", "Az önce geldim", "O zaman bunu yarın yaparız",
     "взято другое значение: «только что» вместо «тогда уж»"),
    (10046, "example_pl", "To twoja ostatnia szansa",
     "To moja ostatnia szansa", "в немецком «мой», а не «твой»"),
    (236, "example_pl", "Babcia opowiada dzieciom bajki",
     "Ona opowiada historię",
     "в немецком «она рассказывает историю», а не про бабушку"),
    (1385, "example_tr", "Beni affet, bir daha olmayacak",
     "Affedersiniz, lütfen",
     "в немецком вежливое «извините, пожалуйста»"),
    (223, "example_tr", "Affedersiniz, istasyon nerede?",
     "Affedersiniz, tuvalet nerede?",
     "в немецком туалет, а не станция"),
    (793, "example_uk", "Я хочу спати, вже пізно", "Я сплю до восьмої",
     "в немецком «я сплю до восьми»"),
    (6261, "example_uk", "Він отримав нову роботу", "Я зголоднів",
     "в немецком «я начинаю хотеть есть»"),
    (6261, "example_tr", "Dün kendime yeni bir telefon aldım",
     "Karnım acılıyor", "в немецком «я начинаю хотеть есть»"),
    (2828, "example_uk", "Дякую тобі за турботу", "Не хвилюйся",
     "в немецком «не волнуйся»"),
    (268, "example_tr", "Akşam bizim evde parti var", "Kutlama harikaydı",
     "в немецком «праздник был прекрасен»"),
    (1060, "example_uk", "Як називається це слово?",
     "Як це слово звучить німецькою?", "потеряно «по-немецки»"),
    (1060, "example_tr", "Bu kelimenin adı ne?",
     "Bu kelime Almanca nasıl söylenir?",
     "потеряно «по-немецки», и так по-турецки не спрашивают"),

    # --- неестественно сказано ------------------------------------------------
    (1505, "example_tr", "Neden nedir?", "Sebep ne?",
     "«Neden nedir» по-турецки не говорят"),
    (1739, "example_tr", "Kitap yukarıda rafta yatıyor",
     "Kitap yukarıda rafta duruyor", "книга на полке «duruyor», не «yatıyor»"),
    (6261, "example_pl", "Dostaję głodu", "Zaczynam być głodny",
     "«dostaję głodu» по-польски не говорят"),
    (2828, "example_pl", "Nie rób sobie zmartwień", "Nie martw się",
     "по-польски говорят «nie martw się»"),

    # --- лишнее против немецкого ------------------------------------------------
    (13354, "example_uk", "Нас четверо людей", "Нас четверо",
     "«людей» лишнее"),
    (10045, "example_pl", "Mówię poważnie, nie żartuję",
     "Mówię poważnie", "«nie żartuję» в немецком нет"),
    (13365, "example_pl", "Kogo szukasz w domu?", "Kogo szukasz?",
     "«w domu» в немецком нет"),

    # --- повелительная форма и знак ---------------------------------------------
    (6245, "example_tr", "Kitabı yanına al", "Kitabı yanına al!",
     "потерян восклицательный знак, он есть во всех остальных языках"),
    (1070, "example_tr", "Yolu bana gösterin", "Yolu bana göster",
     "в немецком «Zeig» — ты, а не Вы"),
]


def main() -> None:
    apply_mode = "--apply" in sys.argv
    engine = create_engine(settings.DATABASE_URL_SYNC)

    ok, skipped = [], []
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
    for wid, col, was, now, why in ok:
        print(f"  {wid} {col} — {why}")
        print(f"      было:  {was!r}")
        print(f"      стало: {now!r}")
    for wid, col, cur in skipped:
        print(f"  ПРОПУЩЕНО {wid} {col}: {cur!r}")

    if not apply_mode:
        print("\nэто показ. Для применения — флаг --apply")
        return

    with engine.begin() as conn:
        for wid, col, _, now, _ in ok:
            conn.execute(text(f"UPDATE words SET {col} = :v WHERE id = :i"),
                         {"v": now, "i": wid})
    print(f"\nприменено: {len(ok)}")

    with engine.connect() as conn:
        bad = 0
        for wid, col, _, now, _ in ok:
            cur = conn.execute(text(f"SELECT {col} FROM words WHERE id = :i"),
                               {"i": wid}).scalar()
            if (cur or "").strip() != now:
                print(f"  ТРЕВОГА: {wid} {col} не записалось")
                bad += 1
        print(f"самопроверка: не записалось {bad}")


if __name__ == "__main__":
    main()
