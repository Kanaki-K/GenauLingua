"""ВТОРОЙ ПРОХОД, блок 59 (ряды 11601–11800): 20 правок.

УЧАСТОК КОНЧИЛСЯ: 10% против 20% и 21.5% в блоках 57–58. И подмен
целиком здесь три, а не пятнадцать.

ДЕВЯТЫЙ ВИНОВАТЫЙ НЕМЕЦКИЙ ЭТАЛОН, и это слово, а не грамматика:

    Muttermilch (15328) de «Muttermilch ist das beste FUTTER für
                             Neugeborene»

«Futter» по-немецки это КОРМ — то, что дают скоту. О человеческом
младенце так не говорят, нужно «Nahrung». И все пять переводов дают
нейтральное слово: «пища», «продукт», «food», «besin», «pożywienie» —
то есть переводчики читали замысел, а не это слово.

ПОДМЕНЫ ЦЕЛИКОМ, три ряда:

    Kronprinz   (16961) pl «Następca tronu WYSTĄPIŁ WCZORAJ W TELEWIZJI»
                        de «Der Kronprinz war bereit, den Thron zu
                            übernehmen»
    durchkreuzen (8665) pl «DESZCZ pokrzyżował NAM WSZYSTKIE plany»
                        de «Die neuen Regeln durchkreuzten SEINE Pläne»
    besudeln     (8664) pl «TEN SKANDAL splamił jego DOBRE IMIĘ»
                        de «Sein RUF war durch die SKANDALE besudelt»

ТУРЕЦКИЙ, четыре ряда: `Plankton` (15870) без связки («temeli» вместо
«temelidir»); `verbarrikadieren` (16942) «barikatladılar» — такого
глагола нет, в списке «kendini içeri kapatmak»; `Doppelagent` (16946)
«Çift» вместо «Çifte» из списка; `stinkig` (11572) потеряно «Dein» и
время прошедшее при немецком настоящем.

СЛОВО НЕ ИЗ СВОЕГО СПИСКА, четыре ряда: `Vagabund` (15333) en «vagrant»
при «vagabond, tramp, drifter»; `Bescherung` (18946) uk «розподіл»
(казённое) при «вручення подарунків»; `volltanken` (17404) uk
«заправитися» при «заправити повний бак»; `durchkreuzen` (8665) uk
«розстроєні» — русизм, в списке «зірвати, зруйнувати, перекреслити».

ДОБАВЛЕНО, ЧЕГО НЕТ В ЭТАЛОНЕ: `Dämpfer` (17402) tr «planlarımıza»
(нашим планам) и pl «dla nas» — в «Die Nachricht war ein echter Dämpfer»
адресата нет вовсе.

ОПЕЧАТКА В АНГЛИЙСКОМ: `Trainerin` (12407) «the teams play» без
апострофа. Первая такая за проход, и её не поймала ни одна примета:
`scan_en_apostrophe` ищет пропущенный апостроф в сокращениях
(«dont», «isnt»), а не в притяжательном падеже.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ немецкий эталон ════════════════════════════════════════
    (15328, "example_de",
     "Muttermilch ist das beste Futter für Neugeborene",
     "Muttermilch ist die beste Nahrung für Neugeborene",
     "«Futter» это корм для скота; о младенце нужно «Nahrung»"),

    # ══ подмены целиком ════════════════════════════════════════
    (16961, "example_pl",
     "Następca tronu wystąpił wczoraj w telewizji",
     "Następca tronu był gotów przejąć tron",
     "«выступил вчера на телевидении» вместо готовности занять трон"),
    (8665, "example_pl",
     "Deszcz pokrzyżował nam wszystkie plany",
     "Nowe przepisy pokrzyżowały jego plany",
     "дождь и «нам» вместо «Die neuen Regeln ... SEINE Pläne»"),
    (8664, "example_pl",
     "Ten skandal splamił jego dobre imię",
     "Jego reputacja została splamiona przez skandale",
     "один скандал и «доброе имя» вместо «Sein Ruf ... durch die Skandale»"),

    # ══ турецкий ═══════════════════════════════════════════════
    (15870, "example_tr",
     "Plankton denizde gıda zincirinin temeli",
     "Plankton denizde gıda zincirinin temelidir",
     "потеряна связка «-dir»"),
    (16942, "example_tr",
     "Evde kendilerini barikatladılar ve polisi aradılar",
     "Evde kendilerini içeri kapattılar ve polisi aradılar",
     "«barikatlamak» такого глагола нет; в списке «kendini içeri kapatmak»"),
    (16946, "example_tr",
     "Çift ajan her iki tarafı birbirine karşı oynattı",
     "Çifte ajan her iki tarafı birbirine karşı oynattı",
     "в списке «çifte ajan», а не «çift»"),
    (11572, "example_tr",
     "Balık bana çok kötü kokuyordu",
     "Balığın bana çok pis kokuyor",
     "потеряно «Dein», прошедшее при немецком настоящем"),

    # ══ слово не из своего списка ══════════════════════════════
    (15333, "example_en",
     "A vagrant slept under the bridge",
     "A vagabond slept under the bridge",
     "«vagrant» не из списка; «vagabond» в нём первое"),
    (18946, "example_uk",
     "На Різдво був гарний розподіл подарунків",
     "На Різдво було гарне вручення подарунків",
     "«розподіл» казённое и не из списка; «вручення подарунків» в нём первое"),
    (17404, "example_uk",
     "Я повинен заправитися, перш ніж почнеться поїздка",
     "Я повинен заправити повний бак, перш ніж почнеться поїздка",
     "«заправитися» не из списка; «заправити повний бак» в нём первое"),
    (8665, "example_uk",
     "Його плани були розстроєні новими правилами",
     "Нові правила зірвали його плани",
     "«розстроєні» — русизм и не из списка; «зірвати» в нём первое"),

    # ══ добавлено, чего нет в эталоне ══════════════════════════
    (17402, "example_tr",
     "Bu haber planlarımıza büyük bir darbe oldu",
     "Bu haber gerçek bir darbe oldu",
     "«planlarımıza» (нашим планам) в эталоне нет"),
    (17402, "example_pl",
     "Ta wiadomość była dla nas prawdziwym ciosem",
     "Ta wiadomość była prawdziwym ciosem",
     "«dla nas» в эталоне нет"),

    # ══ потеря слова ═══════════════════════════════════════════
    (11580, "example_pl",
     "Jego cynizm utrudnia rozmowę",
     "Jego cynizm utrudnia rozmowę z nim",
     "потеряно «mit ihm»"),
    (13154, "example_pl",
     "Woda jest niezbędna do życia",
     "Woda jest niezbędna do życia dla wszystkich organizmów",
     "потеряно «für alle Organismen»"),
    (15330, "example_en",
     "The old man sat on the park bench every day",
     "The old man sat on the bench in the Berlin park every day",
     "потеряно «Berliner»; ru, uk, tr, pl его держат"),

    # ══ время и опечатка ═══════════════════════════════════════
    (13155, "example_pl",
     "Po długiej jazdzie dokuczają mu hemoroidy",
     "Po długiej jazdzie dostał hemoroidów",
     "настоящее при немецком «bekam»"),
    (11563, "example_ru",
     "Это прощание навсегда, я буду скучать по тебе",
     "Прощай навсегда, я буду скучать по тебе",
     "утверждение вместо прощального оборота «Auf Nimmerwiedersehen»"),
    (12407, "example_en",
     "The coach criticized the teams play",
     "The coach criticized the team's play",
     "пропущен апостроф в притяжательном падеже"),
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
