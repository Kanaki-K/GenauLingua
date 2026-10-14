"""ВТОРОЙ ПРОХОД, блок 33 (ряды 6401–6600): 33 правки.

РОД АДРЕСАТА — НОВЫЙ ПОВОРОТ СТАРОГО КЛАССА, И ЗАМЕР ПО НЕМУ ЗАКРЫТ:

    silbern (7636)  de «Du hast silbernen Schmuck zur Party getragen»
        ru «Ты НАДЕЛА серебряные украшения»  — женщина
        uk «Ти НАДІЛА срібні прикраси»       — женщина
        pl «ZAŁOŻYŁEŚ srebrną biżuterię»     — мужчина

`scan_speaker_gender` во всех четырёх половинах смотрит на РАССКАЗЧИКА
(«я»), а здесь род показан у АДРЕСАТА («ты»). Немецкий нейтрален, и три
языка разошлись между собой.

ЗАМЕР ПОКАЗАЛ, ЧТО ПОЛОВИНУ ДЛЯ «ТЫ» ДОБАВИТЬ НЕЛЬЗЯ. По базе: 5
попаданий против 72 мужских ячеек — умолчание то же, что везде. Но из
пяти попаданий НАСТОЯЩЕЕ ОДНО, а четыре ложные, и все по одной причине
— женское окончание принадлежит не адресату, а существительному рядом:

    auserwählt   (10574) uk «Ти вибрана ЛЮДИНА» — согласовано с «людина»
    kritisieren  (14109) ru «критикуешь мою РАБОТУ» — это дополнение
    übertreffen   (7772) ru «хочешь меня превзойти» — формы вовсе нет
    manipulieren (10466) ru «пытаешься мною манипулировать» — тоже нет

Это ровно та беда, что названа у половины для «я» («ДВЕРЬ захлопнулась»,
«до вокзалА»), и приём, которым там спаслись — требовать, чтобы форма
стояла ПОДЛЕЖАЩИМ сразу после «я», — здесь не работает: ложные
срабатывания сидят как раз на дополнении сразу после глагола.

Польская половина чище (окончание «-łaś» второго лица однозначно), но по
базе даёт 0 — добавлять нечего. Замер записан как закрытый: класс
настоящий, формального признака у него нет, и находится он глазами.

ПОЛЕЗНОЕ СОВПАДЕНИЕ С СПИСКОМ ДУБЛЕЙ. Ряд `grob` (7629) — один из
ВОСЬМИ ПОЛНЫХ ДУБЛЕЙ из замера блока 24, и его английский пример говорил
«That was a GROSS insult», тогда как у двойника (7005) стоит верное «a
RUDE insult» — слово из списка. То есть дефект был именно в одном из
двух, и правка делает пару полностью одинаковой. Решению владельца это
только помогает: теперь ряды различаются лишь уровнем (B1 против C1).

ЕЩЁ ОДНА ПАРА НА СОСЕДНИХ ИДЕНТИФИКАТОРАХ. `anschreien` (14142) и
`angeschrien` (14143) — один глагол, и у второго заголовком стоит
причастие. Примеры разные, так что это не дубль, а класс «форма слова
вместо заголовка», уже знакомый. Записано в HANDOVER.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ род адресата ════════════════════════════════════════════
    (7636, "example_ru",
     "Ты надела серебряные украшения на вечеринку",
     "Ты надел серебряные украшения на вечеринку",
     "адресат женского рода при нейтральном эталоне; в pl мужской"),
    (7636, "example_uk",
     "Ти наділа срібні прикраси на вечірку",
     "Ти надів срібні прикраси на вечірку",
     "то же"),

    # ══ дефект в одном из двух полных дублей ════════════════════
    (7629, "example_en",
     "That was a gross insult",
     "That was a rude insult",
     "«gross» нет в списке; у двойника (7005) стоит верное «rude»"),

    # ══ КЛАСС: подменённое предложение ══════════════════════════
    (16417, "example_pl",
     "Blokada dróg wstrzymała dostawy",
     "Blokada uniemożliwiła dostarczenie towarów do miasta",
     "подмена: блокада дорог и поставки вместо товаров и города"),
    (14140, "example_pl",
     "Po tej decyzji podniósł się wielki krzyk",
     "Podniósł się wielki krzyk, gdy wyszła na jaw wiadomość o skandalu",
     "подмена: решение вместо новости о скандале"),
    (11816, "example_tr",
     "Köşedeki büfeden bir tost aldım",
     "Bir sandviç almak için hızlıca büfeye gidiyorum",
     "подмена: прошедшее и тост на углу вместо «ich gehe schnell»"),
    (16429, "example_pl",
     "Wszystkie poszlaki wskazują na niego",
     "Poszlaki świadczą przeciw podejrzanemu",
     "подмена: «на него» вместо «gegen den Verdächtigen»"),

    # ══ формы, которых в языке нет ══════════════════════════════
    (12777, "example_tr",
     "Neyse ki kaza sağlam çıktı",
     "Neyse ki kazadan sağlam çıktı",
     "без «-dan» получается, что целой вышла авария"),
    (16410, "example_tr",
     "Polis onu kundakçılıktan şüpheleniyor ve tutukluyor",
     "Polis onun kundakçılık yaptığından şüpheleniyor ve onu tutukluyor",
     "«onu şüphelenmek» не то управление: «-nden şüphelenmek»"),
    (17233, "example_tr",
     "Kuşlar güneye doğru yoluna devam ediyor",
     "Kuşlar güneye doğru yollarına devam ediyor",
     "подлежащее во множественном требует «yollarına»"),
    (7618, "example_tr",
     "Çok pratik yaparak bu zor tekniği ustalaşabilirsin",
     "Çok pratik yaparak bu zor teknikte ustalaşabilirsin",
     "«ustalaşmak» непереходный: «-de ustalaşmak»"),
    (14141, "example_uk",
     "Його сарказм іноді мене ображає, хоча я знаю, що він це не зі злості",
     "Його сарказм іноді мене ображає, хоча я знаю, що він це робить не зі злості",
     "в придаточном пропущено сказуемое"),

    # ══ слово не из своего списка и не то слово ═════════════════
    (15630, "translation_tr",
     "Amerika geyiği, mus geyiği",
     "mus geyiği, sığın",
     "«Amerika geyiği» это вапити; `Elch` — европейский лось"),
    (17608, "example_tr",
     "Telefonumun pili çabuk bitiyor ve şarj edilmesi gerekiyor",
     "Telefonumun bataryası çabuk bitiyor ve şarj edilmesi gerekiyor",
     "«pil» это одноразовая батарейка; `Akku` — «batarya», и оно первое"),
    (16428, "example_tr",
     "Başkan önemli bir konuşma yaptı",
     "Belediye başkanı önemli bir konuşma yaptı",
     "«başkan» это любой председатель; в списке «belediye başkanı»"),
    (16412, "example_tr",
     "Diktatör bütün ülkeyi kendi kontrolüne almaya çalıştı",
     "Diktatör bütün ülkeyi kendi kontrolüne tabi kılmaya çalıştı",
     "«almak» нет в списке, а «tabi kılmak» есть"),
    (10904, "example_tr",
     "Bana çok huysuzdu",
     "Bana karşı çok soğuk davrandı",
     "«huysuz» о характере, а не об обращении; «soğuk» стоит первым"),
    (7633, "example_tr",
     "Rüyamı gerçekleştireceğim",
     "Hayalimi gerçekleştireceğim",
     "«rüya» это сон; мечта — «hayal»"),
    (16429, "example_en",
     "The evidence points against the suspect",
     "The clues point against the suspect",
     "«evidence» нет в списке; `Indiz` это «clue»"),
    (18306, "example_ru",
     "Я отнес свою одежду в прачечную",
     "Я отнёс своё бельё в прачечную",
     "`Wäsche` это бельё, а не одежда; и пропущена «ё»"),

    # ══ управление и сочетаемость ═══════════════════════════════
    (7621, "example_tr",
     "Nehir denize doğru aşağı doğru akıyor",
     "Nehir denize doğru aşağı akıyor",
     "«doğru» дважды в одной фразе"),
    (13709, "example_tr",
     "Doktor hastaları muayene etmeden önce beyaz doktor önlüğünü giyiyor",
     "Doktor hastaları muayene etmeden önce beyaz önlüğünü giyiyor",
     "«doktor» дважды: «doktor önlüğü» уже содержит его"),
    (12771, "example_pl",
     "W muzeum stoi szkielet dinozaura",
     "Szkielet dinozaura można zobaczyć w muzeum",
     "«stoi» вместо «ist zu sehen»"),
    (12770, "example_pl",
     "Spacer dobrze ci zrobi",
     "Spacer dobrze by ci zrobił",
     "изъявительное вместо «würde dir guttun»"),

    # ══ потерянное и добавленное слово ══════════════════════════
    (11815, "example_pl",
     "Zbieramy jagody w lesie i robimy dżem",
     "Latem zbieramy jagody w lesie i robimy z nich dżem",
     "потеряно «Im Sommer» и «daraus»"),
    (16410, "example_pl",
     "Policja podejrzewa go o podpalenie",
     "Policja podejrzewa go o podpalenie i aresztuje go",
     "потеряно «und verhaftet ihn»"),
    (10888, "example_uk",
     "Вона здібна робітниця і добре виконує свою роботу",
     "Вона здібна робітниця і дуже добре виконує свою роботу",
     "потеряно «sehr»: в остальных четырёх оно есть"),
    (16414, "example_en",
     "The sniper had a good eye and hit his target",
     "The sniper had a very good eye and hit his target",
     "потеряно «sehr»"),
    (9853, "example_pl",
     "Chcę rozdać stare książki, zamiast je wyrzucać",
     "Chcę rozdać swoje stare książki, zamiast je wyrzucać",
     "потеряно «meine»"),
    (10892, "example_ru",
     "Любопытство побудило его расспрашивать дальше",
     "Его любопытство побудило его расспрашивать дальше",
     "потеряно «Seine»: в en, uk и tr оно есть"),
    (10892, "example_pl",
     "Ciekawość pchnęła go do zadawania dalszych pytań",
     "Jego ciekawość pchnęła go do zadawania dalszych pytań",
     "то же"),
    (15144, "example_pl",
     "Jego życie uczuciowe było bardzo skomplikowane",
     "Jego życie uczuciowe było dość skomplikowane",
     "«bardzo» вместо «ziemlich»"),

    # ══ время глагола ═══════════════════════════════════════════
    (13710, "example_pl",
     "Włożyła koszulę nocną i poszła spać",
     "Szybko wkłada koszulę nocną i idzie spać",
     "прошедшее против «zieht an und geht», и потеряно «schnell»"),
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
