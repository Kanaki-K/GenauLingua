"""СКВОЗНАЯ ПРАВКА КЛАССА: 44 польских числа словами против цифр.

Замер в `scan_number_as_word.py`. Коротко: в базе 168 рядов, где в
немецком примере стоит цифра. В 106 из них какой-то язык обходится без
цифры, и в 105 этот язык — польский (только польский — в 80).

Разделение на норму и дефект берётся из самого немецкого:

    порядковое («5. Klasse», «18. Jahrhundert») и десятилетие («70ern»)
        — 23 ряда, НОРМА: ru, uk и pl одинаково называют их словом;
    время (цифра перед «Uhr»)
        — 37 рядов, НОРМА: «в десять часов», «o ósmej»;
    ИЗМЕРЕНИЕ или КОЛИЧЕСТВО («50 Euro», «38 Grad», «100 PS»)
        — 46 рядов, и вот это дефект: цифра и есть предмет фразы.

Из 46 измерений польский промахнулся в 45, и в 44 был единственным
промахнувшимся. Эти 44 ячейки правятся здесь. Сорок пятый — `Bahnsteig`
(1211) — оставлен нарочно: там словом пишут все три славянских языка,
потому что это порядковый номер платформы, а не измерение.

ПОЧЕМУ ЭТО ДЕФЕКТ, А НЕ СТИЛЬ. Писать число словом по-польски не
запрещено. Но база держит правило «цифра переносится во все шесть
языков» — на нём стоит гейт `scan_number_mismatch`, и пять языков из
шести его соблюдают. Когда немецкая карточка показывает «50 Euro», а
польская «pięćdziesiąt euro», ученик не может сопоставить их глазами —
а вся затея карточки в том, чтобы мог.

САМОКРИТИКА. Я правил этот класс по одной ячейке в блоках 32, 36 и 38
(`Kaufmann`, `Radius`, `Quote`, `Franken`), прежде чем замерить. Правило
«повторилось дважды — замеряй по всей базе» существовало с начала
прохода. Это второй такой случай за проход после заголовков-повторов, и
оба раза замер стоил минуты, а экономил блоки.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

# (id, колонка, было, стало, почему) — во всех случаях причина одна,
# поэтому в поле «почему» стоит немецкий эталон с его цифрой.
FIXES: list[tuple[int, str, str, str, str]] = [
    (1101, "example_pl",
     "Chciałbym wypłacić sto euro",
     "Chciałbym wypłacić 100 euro",
     "de «Ich möchte 100 Euro abheben»"),
    (6701, "example_pl",
     "To kosztuje najwyżej dwadzieścia euro",
     "To kosztuje najwyżej 20 euro",
     "de «Das kostet höchstens 20 Euro»"),
    (2256, "example_pl",
     "Poświadczenie kosztuje dziesięć euro",
     "Poświadczenie kosztuje 10 euro",
     "de «Die Beglaubigung kostet 10 Euro»"),
    (9293, "example_pl",
     "Starszy partner w kancelarii adwokackiej ma czterdzieści lat doświadczenia",
     "Starszy partner w kancelarii adwokackiej ma 40 lat doświadczenia",
     "de «hat 40 Jahre Erfahrung»"),
    (8824, "example_pl",
     "W naszej firmie pracuje pięćdziesiąt osób",
     "W naszej firmie pracuje 50 osób",
     "de «In unserem Betrieb arbeiten 50 Leute»"),
    (9813, "example_pl",
     "Zaliczka za samochód wynosi pięć tysięcy euro",
     "Zaliczka za samochód wynosi 5000 euro",
     "de «beträgt 5000 Euro»"),
    (9805, "example_pl",
     "Spłacamy hipotekę jeszcze przez dwadzieścia lat",
     "Spłacamy hipotekę jeszcze przez 20 lat",
     "de «noch 20 Jahre»"),
    (2135, "example_pl",
     "Cena to sto euro plus wysyłka",
     "Cena to 100 euro plus wysyłka",
     "de «beträgt 100 Euro zuzüglich Versand»"),
    (2736, "example_pl",
     "To auto ma sto koni mechanicznych",
     "To auto ma 100 koni mechanicznych",
     "de «Das Auto hat 100 PS»"),
    (16133, "example_pl",
     "Król rządzi krajem już od dwudziestu lat",
     "Król rządzi krajem już od 20 lat",
     "de «schon 20 Jahre lang»"),
    (9733, "example_pl",
     "Dostaję czek na sto euro",
     "Dostaję czek na 100 euro",
     "de «einen Scheck über 100 Euro»"),
    (8063, "example_pl",
     "Koszty wynoszą w sumie pięćset euro",
     "Koszty wynoszą w sumie 500 euro",
     "de «betragen insgesamt 500 Euro»"),
    (2931, "example_pl",
     "Mam jeszcze dziesięć dni urlopu",
     "Mam jeszcze 10 dni urlopu",
     "de «noch 10 Urlaubstage»"),
    (12997, "example_pl",
     "Termometr pokazuje trzydzieści osiem stopni",
     "Termometr pokazuje 38 stopni",
     "de «zeigt 38 Grad»"),
    (14715, "example_pl",
     "Gra na skrzypcach od dziesięciu lat i jest naprawdę utalentowana",
     "Gra na skrzypcach od 10 lat i jest naprawdę utalentowana",
     "de «seit 10 Jahren»"),
    (9755, "example_pl",
     "Suma wynosi sto euro",
     "Suma wynosi 100 euro",
     "de «Die Summe beträgt 100 Euro»"),
    (16152, "example_pl",
     "Panowanie tego króla trwało czterdzieści lat",
     "Panowanie tego króla trwało 40 lat",
     "de «dauerte 40 Jahre»"),
    (7061, "example_pl",
     "Cena włącznie z podatkiem to pięćdziesiąt euro",
     "Cena włącznie z podatkiem to 50 euro",
     "de «ist 50 Euro»"),
    (18069, "example_pl",
     "Ta lampa daje osiemset lumenów jasności",
     "Ta lampa daje 800 lumenów jasności",
     "de «erzeugt 800 Lumen Helligkeit»"),
    (17931, "example_pl",
     "Dziecko ma sto dwadzieścia centymetrów wzrostu",
     "Dziecko ma 120 centymetrów wzrostu",
     "de «ist 120 Zentimeter groß»"),
    (2361, "example_pl",
     "Średnia wynosi pięćdziesiąt",
     "Średnia wynosi 50",
     "de «liegt bei 50»"),
    (8322, "example_pl",
     "Musieliśmy przebyć trzysta kilometrów",
     "Musieliśmy przebyć 300 kilometrów",
     "de «300 Kilometer zurücklegen»"),
    (12362, "example_pl",
     "Nowy tor wyścigowy ma pięć kilometrów długości",
     "Nowy tor wyścigowy ma 5 kilometrów długości",
     "de «ist 5 Kilometer lang»"),
    (1360, "example_pl",
     "Wstęp kosztuje dziesięć euro",
     "Wstęp kosztuje 10 euro",
     "de «Der Eintritt kostet 10 Euro»"),
    (2144, "example_pl",
     "Chcę schudnąć pięć kilo",
     "Chcę schudnąć 5 kilo",
     "de «Ich möchte 5 Kilo abnehmen»"),
    (9940, "example_pl",
     "Cena wynosi sto euro po odjęciu rabatu",
     "Cena wynosi 100 euro po odjęciu rabatu",
     "de «beträgt 100 Euro abzüglich Rabatt»"),
    (1636, "example_pl",
     "Opłata za kurs wynosi sto euro",
     "Opłata za kurs wynosi 100 euro",
     "de «beträgt 100 Euro»"),
    (2896, "example_pl",
     "Nocleg kosztuje pięćdziesiąt euro",
     "Nocleg kosztuje 50 euro",
     "de «kostet 50 Euro»"),
    (2725, "example_pl",
     "Opłata pocztowa wynosi jedno euro",
     "Opłata pocztowa wynosi 1 euro",
     "de «Das Porto beträgt 1 Euro»"),
    (2960, "example_pl",
     "Obowiązuje stała opłata za wysyłkę w wysokości pięciu euro",
     "Obowiązuje stała opłata za wysyłkę w wysokości 5 euro",
     "de «eine Versandkostenpauschale von 5 Euro»"),
    (9898, "example_pl",
     "Opłata wynosi pięćdziesiąt euro",
     "Opłata wynosi 50 euro",
     "de «Die Gebühr beträgt 50 Euro»"),
    (2362, "example_pl",
     "Średnia temperatura wynosi około dwudziestu stopni",
     "Średnia temperatura wynosi około 20 stopni",
     "de «liegt bei etwa 20 Grad»"),
    (17121, "example_pl",
     "Najbliższa stacja benzynowa jest za dwadzieścia kilometrów",
     "Najbliższa stacja benzynowa jest za 20 km",
     "de «noch 20 km weg»: в эталоне сокращение, в ru «20 км»"),
    (9810, "example_pl",
     "Ta koszula kosztuje pięćdziesiąt franków",
     "Ta koszula kosztuje 50 franków",
     "de «kostet 50 Franc»"),
    (16169, "example_pl",
     "To miasto ma około pięćdziesięciu tysięcy mieszkańców",
     "To miasto ma około 50000 mieszkańców",
     "de «etwa 50000 Einwohner»; ru тоже без разделителя"),
    (2604, "example_pl",
     "To jest dziesięć kilometrów",
     "To jest 10 kilometrów",
     "de «Das sind 10 Kilometer»"),
    (18057, "example_pl",
     "Ta żarówka zużywa sześćdziesiąt watów",
     "Ta żarówka zużywa 60 watów",
     "de «verbraucht 60 Watt»"),
    (2289, "example_pl",
     "Kwota wynosi sto euro",
     "Kwota wynosi 100 euro",
     "de «Der Betrag ist 100 Euro»"),
    (9832, "example_pl",
     "Dziś jest dwadzieścia procent rabatu",
     "Dziś jest 20 procent rabatu",
     "de «einen Rabatt von 20 Prozent»"),
    (9871, "example_pl",
     "Ten towar kosztuje w Szwajcarii pięćdziesiąt franków",
     "Ten towar kosztuje w Szwajcarii 50 franków",
     "de «kostet 50 Franken»"),
    (17684, "example_pl",
     "Wskazówka zegara wskazuje dwunastą",
     "Wskazówka zegara wskazuje na 12",
     "de «zeigt auf die 12»: это цифра на циферблате, ru «на 12»"),
    (6829, "example_pl",
     "Pięćdziesiąt euro za pizzę? To kompletnie przesadzone",
     "50 euro za pizzę? To kompletnie przesadzone",
     "de «50 Euro für Pizza?»"),
    (17935, "example_pl",
     "Kąt między tymi dwiema liniami ma dziewięćdziesiąt stopni",
     "Kąt między tymi dwiema liniami ma 90 stopni",
     "de «ist 90 Grad»"),
    (2245, "example_pl",
     "Moje ubezpieczenie samochodu kosztuje osiemdziesiąt euro miesięcznie",
     "Moje ubezpieczenie samochodu kosztuje 80 euro miesięcznie",
     "de «kostet 80 Euro im Monat»"),
]


def main() -> None:
    apply_mode = "--apply" in sys.argv
    engine = create_engine(settings.DATABASE_URL_SYNC)
    ok: list[tuple[int, str, str, str, str]] = []
    skipped: list[tuple[int, str, str | None]] = []
    seen: set[tuple[int, str]] = set()
    dupes: list[tuple[int, str]] = []
    with engine.connect() as conn:
        for wid, col, was, now, why in FIXES:
            if (wid, col) in seen:
                dupes.append((wid, col))
            seen.add((wid, col))
            cur = conn.execute(
                text(f"SELECT {col} FROM words WHERE id = :i"), {"i": wid}
            ).scalar()
            if (cur or "").strip() != was:
                skipped.append((wid, col, cur))
            else:
                ok.append((wid, col, was, now, why))

    print(f"=== правок {len(FIXES)}, совпало {len(ok)}, пропущено {len(skipped)} ===\n")
    for wid, col in dupes:
        print(f"ВНИМАНИЕ: одна ячейка правится дважды — id={wid} {col}")
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
