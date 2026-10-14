"""
Второй круг вычитки: правки руками, 300 рядов (зерно 20261002).

Самое заметное за круг:

* `abgelegen` — в польском примере стояло немецкое слово: «**Ich** dom stoi
  w odludnym miejscu». Ни одна формальная проверка такого не ловит: буквы
  латинские, диакритика на месте.
* `letzen` — сломан сам немецкий пример. «Der Bulle letzte den Reiter mit
  seinen Hörnern» означает примерно «бык услаждал всадника рогами»: глагол
  letzen — это «подкреплять, освежать», а не «бодать». Русский перевод честно
  повторил бессмыслицу. Правлю немецкий пример и перевод за ним.
* `Peinlichkeit` — польской колонки нет вовсе, а в украинской «неловкість»,
  русизм вместо «ніяковість».
* `Kavallerie` — «коноtа»: латинские буквы внутри украинского слова.
* `Hauptschule` — в немецком «sie», в английском и украинском «он».

Как и в прошлых партиях, у каждой правки записано ожидаемое текущее значение.

    python -m app.scripts.fix_manual_round2            # показать
    python -m app.scripts.fix_manual_round2 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# (id, колонка, что стоит сейчас, на что менять, зачем)
FIXES: list[tuple[int, str, str, str, str]] = [

    # --- чужой язык и битые буквы -------------------------------------------
    (8381, "example_pl",
     "Ich dom stoi w odludnym miejscu w górach",
     "Ta wieś leży w bardzo odludnym miejscu w górach",
     "немецкое «Ich» в польском примере"),
    (16219, "translation_uk",
     "кавалерія, коноtа",
     "кавалерія, кіннота",
     "латинские буквы внутри украинского слова"),
    (15858, "example_tr",
     "Hiena karanlıkta avını bekliyor",
     "Sırtlan karanlıkta avını bekliyor",
     "«Hiena» — не турецкое слово, нужно «sırtlan»"),

    # --- сломанный ряд letzen -----------------------------------------------
    (8082, "example_de",
     "Der Bulle letzte den Reiter mit seinen Hörnern",
     "Ein kühles Getränk letzte uns nach der Wanderung",
     "letzen — «подкреплять», а не «бодать»; фраза бессмысленна"),
    (8082, "example_ru",
     "Бык услаждал всадника своими рогами",
     "Прохладный напиток подкрепил нас после похода",
     "перевод повторял бессмыслицу немецкого примера"),

    # --- Peinlichkeit --------------------------------------------------------
    (11575, "translation_uk",
     "Неловкість",
     "ніяковість, незручність",
     "«неловкість» — русизм"),
    (11575, "example_uk",
     "Ця ситуація була для мене просто неловкою",
     "Цю ніяковість я ніколи не забуду",
     "русизм и пример про другое"),
    (11575, "translation_pl",
     "",
     "zażenowanie, niezręczność",
     "польской колонки не было вовсе"),
    (11575, "example_pl",
     "",
     "Tego zażenowania nigdy nie zapomnę",
     "польского примера не было вовсе"),
    (11575, "example_tr",
     "Durum dayanılmazdı",
     "Bu utancı asla unutmayacağım",
     "пример был про другое"),

    # --- несуществующие слова и русизмы -------------------------------------
    (866, "example_uk",
     "Я ходю до мовної школи",
     "Я ходжу до мовної школи",
     "«ходю» — не литературная форма"),
    (15064, "example_uk",
     "Помічник привіз раненого в лікарню",
     "Помічник везе пораненого до лікарні",
     "«раненого» — русизм"),
    (12593, "translation_uk",
     "блідий, тусклий",
     "блідий, тьмяний",
     "«тусклий» — русизм"),
    (12808, "example_uk",
     "Його покашлювання порушило всіх у бібліотеці",
     "Покашлювання заважало всім у бібліотеці",
     "«порушило всіх» — не то слово"),
    (16237, "example_uk",
     "Корупція у уряді — велика проблема",
     "Корупція в уряді — велика проблема",
     "«у уряді» — неверный предлог"),
    (14121, "example_uk",
     "Його мова невиразна і важко розуміти",
     "Його мова невиразна, і її важко зрозуміти",
     "оборванная конструкция"),

    # --- турецкая грамматика и опечатки -------------------------------------
    (9555, "example_tr",
     "İlk harf A'dir",
     "İlk harf A'dır",
     "нарушена гармония гласных"),
    (11865, "example_tr",
     "Restoranda karidesleri çok taze idi",
     "Restorandaki karidesler çok tazeydi",
     "неверный падеж"),
    (14509, "example_tr",
     "O, kemanda harika bir şekilde çalıyor",
     "O, harika keman çalıyor",
     "«kemanda çalmak» — неверная конструкция"),
    (12593, "example_tr",
     "Korktuymuş gibi solgun görünüyordu",
     "Korkmuş gibi solgun görünüyordu",
     "«korktuymuş» — такой формы нет"),
    (15608, "example_tr",
     "Çiftçiler samanlığında samanı depoluyor",
     "Çiftçiler samanı samanlıkta depoluyor",
     "лишний изафет"),
    (2884, "example_tr",
     "Moda trendine ait yeni trend vintage giyim giymektir",
     "Modadaki yeni trend vintage giysiler giymek",
     "фраза путается в собственных словах"),
    (7701, "example_tr",
     "Talihsiz olarak evde cüzdanımı unuttum",
     "Ne yazık ki cüzdanımı evde unuttum",
     "«talihsiz olarak» — калька"),
    (11152, "example_tr",
     "Bu akıl almaz bir hikâye",
     "Bu akıl almaz bir yalan",
     "в немецком ложь, а не история"),

    # --- неверный смысл ------------------------------------------------------
    (246, "example_pl",
     "Pasażerowie wysiadają z autobusu",
     "Pasażerowie wysiadają z pociągu",
     "автобус вместо поезда"),
    (14638, "example_pl",
     "Skrzypek zagrał piękną melodię",
     "Skrzypek zagrał piękny koncert",
     "мелодия вместо концерта"),
    (9812, "example_en",
     "The cardboard is too heavy to carry",
     "The box is too heavy to carry",
     "картон вместо коробки"),
    (9812, "example_uk",
     "Картон занадто важкий для перенесення",
     "Коробка занадто важка, щоб її нести",
     "картон вместо коробки"),
    (1517, "example_en",
     "He goes to secondary school",
     "She goes to secondary school",
     "в немецком «sie» — она"),
    (1517, "example_uk",
     "Він навчається в основній школі",
     "Вона навчається в основній школі",
     "в немецком «sie» — она"),
    (6780, "example_en",
     "Well meet in front of the cinema",
     "We'll meet in front of the cinema",
     "пропущен апостроф"),

    # --- примеры про другое --------------------------------------------------
    (13559, "example_pl",
     "Moja córka ma czternaście lat",
     "Moja córka skończy w przyszłym miesiącu czternaście lat",
     "немецкий про «исполнится в следующем месяце»"),
    (14400, "example_uk",
     "Моя сестра ще незаймана",
     "Діва — це знак зодіаку",
     "пример про другое и не к месту"),
    (14400, "example_tr",
     "Ablam Başak burcu",
     "Başak bir burçtur",
     "пример про другое"),
    (8168, "example_en",
     "We'll meet tomorrow to discuss this",
     "The two bosses will meet tomorrow",
     "в немецком встречаются два начальника"),
    (8168, "example_uk",
     "Ми зустрінемося завтра, щоб це обговорити",
     "Завтра обидва керівники зустрінуться",
     "в немецком встречаются два начальника"),
    (8168, "example_tr",
     "Bunu tartışmak için yarın buluşacağız",
     "İki patron yarın bir araya gelecek",
     "в немецком встречаются два начальника"),
    (8168, "example_pl",
     "Spotkaliśmy się przypadkiem na dworcu",
     "Jutro obaj szefowie spotkają się",
     "пример про другое"),
    (7849, "example_pl",
     "Policja w końcu zwolniła drogę dla aut",
     "Lekarz w końcu go wypisał i powiedział, że może iść do domu",
     "пример про полицию, а немецкий про врача"),
    (15719, "example_tr",
     "Bozkırda tek bir ağaç bile yok",
     "Amerika'daki preri uçsuz bucaksızdır",
     "пример про другое"),
    (7739, "example_en",
     "Please present your ticket at the gate",
     "Can you present the contract?",
     "в немецком вопрос про договор"),
    (7739, "example_uk",
     "Він представив свої результати",
     "Ти можеш подати договір?",
     "в немецком вопрос про договор"),
    (7739, "example_tr",
     "Sonuçlarını sundu",
     "Sözleşmeyi sunabilir misin?",
     "в немецком вопрос про договор"),
    (14149, "example_en",
     "Don't let him talk you into it",
     "You always tell me I can't do it, but I believe in myself",
     "пример про другое"),
    (14149, "example_pl",
     "Nie wmawiaj mi, że to moja wina",
     "Zawsze mi wmawiasz, że nie dam rady, ale wierzę w siebie",
     "пример про другое"),
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
            cur_norm = (cur or "").strip()
            if cur_norm != was:
                skipped.append((wid, col, cur))
            else:
                ok.append((wid, col, was, now, why))

    print(f"=== правок {len(FIXES)}, совпало {len(ok)}, пропущено {len(skipped)} ===\n")
    for wid, col, was, now, why in ok:
        print(f"  {wid} {col} — {why}")
        print(f"      было:  {was!r}")
        print(f"      стало: {now!r}")
    if skipped:
        print("\n--- пропущено, в базе другое ---")
        for wid, col, cur in skipped:
            print(f"  {wid} {col}: {cur!r}")

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
