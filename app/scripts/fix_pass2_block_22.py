"""ВТОРОЙ ПРОХОД, блок 22 (ряды 4201–4400).

СЕДЬМОЙ РЯД С ТРОЙКОЙ en+uk+tr, и он показателен тем, насколько далеко
расходятся три перевода от одного эталона:

    Bruch (12643)  de «Er hat einen Bruch im Arm» — у него перелом руки
        en «There's a crack in the window»      — трещина в ОКНЕ
        uk «На чашці з'явилася тріщина»          — трещина в ЧАШКЕ
        tr «Duvarda büyük bir çatlak var»        — трещина в СТЕНЕ
        ru «У него перелом руки»                 — верно
        pl «Lekarz powiedział, że to złamanie ręki» — добавлен врач

Три языка выбрали три разных предмета, и ни один из них не рука. При
этом слово ряда (`Bruch` = перелом/трещина) во всех трёх на месте,
длина правдоподобная, грамматика в порядке — то есть ни одна примета
этого не возьмёт.

ПРИЁМ «ПОСМОТРИ БЛИЗНЕЦОВ» СРАБОТАЛ ВТОРОЙ РАЗ. `Klingel` (18228)
по-украински писал «Дзвоник на дверях» при списке «дзвінок» — ровно та
же ошибка, что у `Türklingel` (18211) в блоке 19. Ряды-близнецы в базе
держат одинаковые дефекты, и после правки одного стоит открыть второй.

ПОЛЬСКИХ ПОДМЕН СНОВА МНОГО — шесть:

    einschlagen (7223)  «Piorun uderzył w drzewo przed domem»
    gelähmt     (12639) «Po wypadku ma sparaliżowaną nogę»
    Pflege      (12641) «Babcia wymaga stałej opieki»
    Heimweg     (18738) «W drodze do domu kupiłem chleb»
    Gehör       (12642) «Dziadek ma jeszcze dobry słuch»
    rausbringen (7206)  «Możesz wynieść śmieci na podwórko?»

Это второй блок подряд с таким перекосом (в блоке 21 было девять).
Закономерность стоит того, чтобы её назвать: в польских ячейках подмена
встречается чаще, чем в остальных, и приходит ПООДИНОЧКЕ, а не тройкой.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ КЛАСС: тройка en+uk+tr, седьмой раз ═════════════════════
    (12643, "example_en",
     "There's a crack in the window",
     "He has a fracture in his arm",
     "подмена: трещина в окне вместо перелома руки"),
    (12643, "example_uk",
     "На чашці з'явилася тріщина",
     "У нього перелом руки",
     "подмена: трещина в чашке"),
    (12643, "example_tr",
     "Duvarda büyük bir çatlak var",
     "Kolunda bir kırık var",
     "подмена: трещина в стене"),
    (12643, "example_pl",
     "Lekarz powiedział, że to złamanie ręki",
     "Ma złamanie ręki",
     "никакого врача в эталоне нет"),

    # ══ КЛАСС: подмена в польском, поодиночке ═══════════════════
    (7206, "example_pl",
     "Możesz wynieść śmieci na podwórko?",
     "Możesz to wynieść?",
     "подмена: ни мусора, ни двора в эталоне нет"),
    (7223, "example_pl",
     "Piorun uderzył w drzewo przed domem",
     "Piorun uderza w drzewo i rozłupuje je",
     "подмена: «перед домом» вместо «и расщепляет его»"),
    (12639, "example_pl",
     "Po wypadku ma sparaliżowaną nogę",
     "Moja noga jest sparaliżowana, nie mogę chodzić",
     "подмена: эталон от первого лица и без аварии"),
    (12641, "example_pl",
     "Babcia wymaga stałej opieki",
     "Dobra pielęgnacja jest ważna dla twojej skóry",
     "подмена: эталон про уход за кожей, а не про бабушку"),
    (18738, "example_pl",
     "W drodze do domu kupiłem chleb",
     "Droga do domu była długa i ciemna",
     "подмена: эталон «Der Heimweg war lang und dunkel»"),
    (12642, "example_pl",
     "Dziadek ma jeszcze dobry słuch",
     "Jego słuch jest jeszcze bardzo dobry",
     "подмена: никакого дедушки в эталоне нет"),

    # ══ ряд-близнец: та же ошибка, что в блоке 19 ═══════════════
    (18228, "example_uk",
     "Дзвоник на дверях не працює",
     "Дзвінок на дверях не працює",
     "в списке «дзвінок»; та же ошибка, что у `Türklingel` (18211)"),

    # ══ формы, которых в языке нет ══════════════════════════════
    (16222, "example_tr",
     "Yanlış parklanmak için ceza belgesi aldım",
     "Yanlış park ettiğim için ceza aldım",
     "«parklanmak» не слово, и «için» требует причастия"),
    (13675, "example_pl",
     "Ta kurtka jest ze prawdziwej skóry",
     "Ta kurtka jest z prawdziwej skóry",
     "«ze» ставится только перед скоплением согласных"),
    (10557, "example_uk",
     "Ніжний дотик його руки її заспокоїло",
     "Ніжний дотик його руки її заспокоїв",
     "узгодження з «дотик»: «заспокоїв»"),
    (10558, "example_uk",
     "Здійснення мого мрії було чудовим",
     "Здійснення моєї мрії було чудовим",
     "«мрія» жіночого роду: «моєї»"),
    (7211, "example_uk",
     "Стара дворняга кожен ранок гавкає на сусідів",
     "Стара дворняга щоранку гавкає на сусідів",
     "«кожен ранок» не той падеж"),
    (14498, "example_tr",
     "Bu şiirin şairliği okuyucunun kalbini dokunuyor",
     "Bu şiirin şiirselliği okuyucunun kalbine dokunuyor",
     "«şairlik» это поэтство, а не поэзия; и «dokunmak» требует дательного"),
    (12639, "example_tr",
     "Bacağım felç geçirdi, yürüyemiyorum",
     "Bacağım felçli, yürüyemiyorum",
     "«felç geçirmek» говорят о человеке, а не о ноге"),
    (10559, "example_tr",
     "İçten çok üzüntülüydü ama gülümsedi",
     "İçten çok üzgündü ama gülümsedi",
     "«üzüntülü» не форма: нужно «üzgün»"),

    # ══ русизм в украинском ═════════════════════════════════════
    (7223, "example_uk",
     "Молнія вдаряє в дерево і розколює його",
     "Блискавка вдаряє в дерево і розколює його",
     "«молнія» русское: по-украински «блискавка»"),
    (10561, "translation_uk",
     "смілий, ризикований, дерзкий, відвертий",
     "смілий, ризикований, зухвалий, відвертий",
     "«дерзкий» русское: по-украински «зухвалий»"),

    # ══ слово не из своего списка и не то слово ═════════════════
    (14497, "example_en",
     "The preacher delivers a sermon",
     "The preacher delivers a speech",
     "эталон «hält eine Rede» — речь, а не проповедь"),
    (17161, "example_tr",
     "Gemi sağ yana dönüyor",
     "Gemi sancak tarafına dönüyor",
     "«sancak» это и есть штирборт, и оно первое в списке"),
    (7219, "example_pl",
     "Nie mogę wywabić tej plamy z koszuli",
     "Nie mogę wywabić plam z ubrania",
     "в эталоне «aus der Kleidung» и множественное «Flecken»"),
    (15537, "example_tr",
     "Vay be, bu çok yakındı!",
     "Vay canına, kıl payıydı!",
     "«yakındı» о расстоянии; «knapp» это «на волосок»"),
    (8906, "example_uk",
     "Приватний детектив розв'язав справу",
     "Приватний детектив розкрив справу",
     "справу «розкривають», а не «розв'язують»"),

    # ══ потерянное слово ════════════════════════════════════════
    (18226, "example_uk",
     "Я дзвоню у двері й чекаю",
     "Я дзвоню у вхідні двері й чекаю",
     "карточка показывает «вхідні двері», а пример говорил просто «двері»"),
    (18226, "example_tr",
     "Kapı zilini çalıyorum ve bekliyorum",
     "Ön kapının zilini çalıyorum ve bekliyorum",
     "то же: потеряно «ön kapı»"),
    (16227, "example_pl",
     "Rodzina została wypędzona z domu",
     "Rodzina została wypędzona z domu i musiała uciekać",
     "потеряно «und musste fliehen»"),

    # ══ не то слово в эталоне переведено ════════════════════════
    (12641, "example_en",
     "Daily care is important for your skin",
     "Good care is important for your skin",
     "эталон «Gute Pflege», а не ежедневный"),
    (12641, "example_uk",
     "Щоденний догляд важливий для твоєї шкіри",
     "Гарний догляд важливий для твоєї шкіри",
     "то же"),

    # ══ вид глагола ═════════════════════════════════════════════
    (923, "example_uk",
     "Давай грати у теніс",
     "Давай зіграємо в теніс",
     "«Lass uns spielen» однократное; в ru, tr и pl совершенный вид"),

    # ══ часы двоеточием и обрубленное сокращение ════════════════
    (2027, "example_ru",
     "Мероприятие начинается в 19:00",
     "Мероприятие начинается в 19 часов",
     "двоеточие в часах озвучка не читает"),
    (2027, "example_uk",
     "Захід починається о 19:00",
     "Захід починається о 19 годині",
     "то же"),
    (2027, "example_en",
     "The event starts at 7 pm",
     "The event starts at 7 in the evening",
     "«pm» без точек озвучка прочитает как две буквы"),
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
