"""ВТОРОЙ ПРОХОД, блок 39 (ряды 7601–7800): 27 правок.

ГЛАВНОЕ В БЛОКЕ — ЗАМЕР, КОТОРЫЙ ПРИВЁЛ К ПРАВКЕ ПРОДАКШН-КОДА. Класс
«в примере слово не из своего списка» шёл три блока подряд (3 случая в
блоке 37, 5 в блоке 38), и по правилу «повторилось дважды — замеряй»
здесь он замерен. Разбор — в `scan_shown_sense.py`, коротко:

ПЕРВОЕ ПРАВИЛО ОТБРОШЕНО, и это важнее улова. Прямое «ни один вариант
ячейки не нашёлся в примере» дало 4332 ячейки. Разбивка по части речи
показала, что правило мерит не базу, а МАТЧЕР: у глаголов промах 26.6%,
у существительных 1.4%. Условие `len(head) - common <= 3` предполагает,
что словарная форма длиннее общей основы не больше чем на три буквы — для
существительных верно, для славянского и турецкого инфинитива нет.

ВТОРОЕ ПРАВИЛО — ПЕРЕКРЁСТНОЕ: если в трёх языках и более пример указал
на НЕ первый вариант, а в этом языке не нашлось ничего, то здесь
показывается не то значение. Шесть языков ряда проверяют друг друга —
тот же приём, что «два ряда на одно слово проверяют друг друга». Дало 84
ячейки, и разбор глазами разделил их надвое: у 19 ТЕКСТ В ПОРЯДКЕ и
виноват матчер, у 65 пример написан словом, которого в списке нет.

ЧТО СДЕЛАНО С МАТЧЕРОМ, И ПОЧЕМУ ИМЕННО ТАК. Простое послабление порога
до 5 оказалось ОПАСНЫМ: из 531 изменённой ячейки примерно треть — порча,
и вся порча одного вида — ранний приблизительный вариант затеняет поздний
точный («частенько» вместо «часто», «moralność» вместо «morale»,
«zehirlenmiş» вместо «zehirli»). Причина не в пороге, а в том, что
правило возвращало ПЕРВОЕ совпадение, а не лучшее.

Поэтому правка двойная и проверена замером на каждом шаге:

    выбор ЛУЧШЕГО совпадения (ключ: остаток основы, затем место в списке)
        — 217 ячеек, ни одной порчи из названных;
    длинный хвост до 5, разрешённый ТОЛЬКО когда строгое не нашло ничего
        — ещё 321 ячейка, из пробы в 21 случай 19 явных улучшений.

Итого 538 ячеек сдвинулось к «показывается то слово, что в примере».
Порог 5 замерен: на 4 закрывается 14 известных случаев из 19, на 5 — все
19, на 6 и 7 не добавляется ничего. Три названных ложных попадания
оставлены в журнале: `Wechsel` («перемена» находится внутри «переход»),
`ermorden`, `Verdeck`.

**Момент выбран не случайно: озвучка остановлена.** Имя клипа равно
показываемому слову, и 538 изменений означали бы 538 переименований, если
бы клипы уже были нарезаны. Сейчас это бесплатно.

ОСТАТОК ПРИМЕТЫ 75 — ряды, где пример написан синонимом, которого в
списке нет вовсе. Это следующая сквозная работа, вид разобран в примете.

В САМОМ БЛОКЕ: пятая польская полоса подряд, и в ней две подмены целиком
— `Transfer` (17263, «трансфер из аэропорта в отель включён в цену»
вместо «Transfer von Spieler A zu Klub B») и `Hosentasche` (13730,
«ключи у меня в кармане» вместо «Ich habe mein Handy verloren»).

`Hunderter` (9874): в польском списке стоял «banknot studolarowy» —
купюра в сто ДОЛЛАРОВ при немецком «Hunderter» о евро. Неверная валюта
прямо в списке значений.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ подмена целиком, пятая польская полоса подряд ════════════
    (17263, "example_pl",
     "Transfer z lotniska do hotelu jest w cenie",
     "Transfer gracza A do klubu B kosztuje dużo pieniędzy",
     "подмена: трансфер из аэропорта вместо перехода игрока"),
    (13730, "example_pl",
     "Klucze mam w kieszeni spodni",
     "Zgubiłem telefon w kieszeni spodni",
     "подмена: ключи вместо «Ich habe mein Handy verloren»"),
    (15184, "example_tr",
     "Çocuklara bakacak bir dadı tuttular",
     "Sütanne kraliyet ailesinin çocuğuna baktı",
     "подмена: наняли няню вместо «Die Amme kümmerte sich um das Kind»"),
    (15184, "example_pl",
     "Mamka opiekowała się małym księciem",
     "Mamka opiekowała się dzieckiem rodziny królewskiej",
     "«małym księciem» вместо «das Kind der königlichen Familie»"),
    (11034, "example_uk",
     "Боже, оберігай його від біди",
     "Боже, оберігай тебе від усякого зла",
     "третье лицо против «Gott behüte DICH», и «від біди» вместо «vor allem Bösen»"),

    # ══ неверное значение прямо в списке ════════════════════════
    (9874, "translation_pl",
     "setka, banknot studolarowy, banknot stueurowy",
     "setka, banknot stueurowy, liczba sto",
     "«studolarowy» это сто ДОЛЛАРОВ, а `Hunderter` о евро"),

    # ══ вид карточки: слово не из своего списка ═════════════════
    (7880, "example_tr",
     "Oda oldukça yıpranmış görünüyordu",
     "Oda oldukça eski püskü görünüyordu",
     "«yıpranmış» не из списка; «eski püskü» в нём есть"),
    (15688, "example_tr",
     "Gözünün altında morluk var",
     "Gözünün altı morarmış",
     "«morluk» не из списка; показывалось «menekşe» — фиалка вместо синяка"),
    (14190, "example_tr",
     "Hatalarından dolayı af diliyor",
     "Hataları için af rica ediyor",
     "«af dilemek» не из списка; «rica etmek» в нём есть"),
    (17638, "example_ru",
     "Звонок телефона в кинотеатре был очень раздражающим",
     "Звонок мобильного в кинотеатре очень раздражал",
     "`Handy` это мобильный, и так стоит в списке"),
    (17638, "example_uk",
     "Дзвінок телефону в кінотеатрі дуже дратував",
     "Дзвінок мобільного в кінотеатрі дуже дратував",
     "то же"),

    # ══ потерянное и добавленное слово ══════════════════════════
    (11038, "example_ru",
     "Примирение между друзьями было искренним",
     "Примирение между двумя друзьями было искренним",
     "потеряно «den beiden»: в en, tr и pl оно есть"),
    (11038, "example_uk",
     "Примирення між друзями було щирим",
     "Примирення між двома друзями було щирим",
     "то же"),
    (18829, "example_pl",
     "We wtorki chodzę na trening piłki nożnej",
     "We wtorki zawsze chodzę na trening piłki nożnej",
     "потеряно «immer»: в остальных четырёх оно есть"),
    (7882, "example_pl",
     "To była oddzielona część sali",
     "To była oddzielona strefa",
     "«część sali» в эталоне «ein abgetrennter Bereich» нет"),
    (15190, "example_tr",
     "Küçük ufaklık bütün gün bahçede oynadı",
     "Ufaklık bütün gün bahçede oynadı",
     "«küçük ufaklık» тавтология: «ufaklık» и значит малыш"),
    (16546, "example_ru",
     "Проверки на границе всегда занимают вечность",
     "Проверки на границе всегда занимают очень много времени",
     "«вечность» преувеличение, которого в «sehr lange» нет"),

    # ══ не то слово ═════════════════════════════════════════════
    (7907, "example_pl",
     "Orzeł chwyta zdobycz szponami",
     "Orzeł chwyta kurę swoim szponem",
     "«zdobycz» вместо «das Huhn», и множественное против «mit seiner Klaue»"),
    (17642, "example_pl",
     "Musi przeładować broń",
     "Musi przeładować karabin",
     "«broń» это оружие вообще; в эталоне «das Gewehr»"),
    (11871, "example_uk",
     "Він допиває свій кухоль пива",
     "Він допиває свою склянку пива",
     "«кухоль» это кружка; в эталоне «Glas», в ru и pl стакан"),
    (11068, "example_pl",
     "Przed starą świątynią poczuła głęboką cześć",
     "Przed starą świątynią poczuła głęboki szacunek",
     "«cześć» в этом значении книжное; «głęboki szacunek» стоит в списке"),
    (11058, "example_uk",
     "Я не можу йому дорікати, що він образився",
     "Я не можу йому дорікати, що він сердиться",
     "«образився» это обиделся; `sauer sein` — сердиться"),
    (12859, "example_uk",
     "Обморожені рослини довелося видалити з саду",
     "Замерзлі рослини довелося видалити з саду",
     "«обморожений» о людях; растения «замерзлі», как и в ru"),
    (11040, "example_tr",
     "Bütün zaman boyunca huysuzdu",
     "Baştan sona huysuzdu",
     "«bütün zaman boyunca» не оборот"),
    (18350, "example_ru",
     "Подоконник покрыт пылью и старыми украшениями",
     "Подоконник весь в пыли и старых украшениях",
     "«покрыт украшениями» не по-людски: «voller Staub und Dekorationen»"),

    # ══ ложное попадание матчера, снятое со стороны списка ══════
    (1012, "translation_ru",
     "смена, перемена, обмен, размен денег, вексель",
     "смена, переход, перемена, обмен, размен денег, вексель",
     "пример «Переход в новую фирму» — слова нет в списке, и «перемена» "
     "находилась внутри «переход»"),
    (1012, "translation_uk",
     "зміна, переміна, обмін, розмін, вексель",
     "зміна, перехід, переміна, обмін, розмін, вексель",
     "то же"),
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
