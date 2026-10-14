"""ВТОРОЙ ПРОХОД, блок 25 (ряды 4801–5000): 30 правок.

ЛОЖНЫЙ ДРУГ ВНУТРИ ОДНОГО КОРНЯ — находка блока.

    schweben (7329)  de «Der Ballon schwebt in der Luft»
        uk «Я люблю паритися в лазні»

Немецкое `schweben` это «парить» в воздухе. Украинское «парити» —
тоже. А «паритися» — это париться в бане. Перевод уехал от воздушного
шара в баню по одному корню, и фраза при этом совершенно правильная
по-украински: ни примета, ни грамматика её не тронут.

ВОСЬМАЯ И ДЕВЯТАЯ ТРОЙКИ en+uk+tr, обе в одном блоке:

    Haustier  (388)   de «Wir haben ein Haustier zu Hause» — МЫ
        en «They have a pet», uk «У них є», tr «Evcil hayvanları var»
        Все три перевели «они». ru и pl говорят «мы».

    Labyrinth (12211) de «Wir sind im Labyrinth verloren gegangen»
        en «in the maze OF THE PARK», uk «в лабіринті ПАРКУ»,
        tr «PARKIN labirentinde» — парк все три придумали вместе.
        ru и pl без парка.

ОШИБКА, КОТОРАЯ ГОВОРИТ ОБРАТНОЕ:

    Hausfrau (15084)  de «kümmert sich um den Haushalt» — ведёт дом
        tr «evi başına çıkarıyor» — турецкий оборот «evi başına
        çıkarmak» значит «разнести дом», то есть прямо противоположное.

Это второй случай за проход, когда перевод говорит обратное эталону
(первый — `wegwerfen` в блоке 18), и оба раза фраза была безупречна.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ ложный друг: шар уехал в баню ═══════════════════════════
    (7329, "example_uk",
     "Я люблю паритися в лазні",
     "Повітряна куля ширяє в повітрі",
     "«паритися» это баня; schweben — парить в воздухе"),

    # ══ КЛАСС: тройка en+uk+tr, восьмая и девятая ═══════════════
    (388, "example_en",
     "They have a pet",
     "We have a pet at home",
     "подменено лицо: эталон «Wir haben»; ru и pl верны"),
    (388, "example_uk",
     "У них є домашня тварина",
     "У нас дома є домашня тварина",
     "то же"),
    (388, "example_tr",
     "Evcil hayvanları var",
     "Evde bir evcil hayvanımız var",
     "то же"),
    (12211, "example_en",
     "We got lost in the maze of the park",
     "We got lost in the maze",
     "«парк» в эталоне «im Labyrinth» не упоминается"),
    (12211, "example_uk",
     "Ми заблудилися в лабіринті парку",
     "Ми заблудилися в лабіринті",
     "то же"),
    (12211, "example_tr",
     "Parkın labirentinde kaybolduk",
     "Labirentte kaybolduk",
     "то же"),

    # ══ перевод говорит ОБРАТНОЕ ════════════════════════════════
    (15084, "example_tr",
     "Annem ev kadını ve evi başına çıkarıyor",
     "Annem ev kadını ve ev işleriyle ilgileniyor",
     "«evi başına çıkarmak» значит разнести дом — обратное эталону"),

    # ══ КЛАСС: подмена ══════════════════════════════════════════
    (17813, "example_ru",
     "Он объявил себя банкротом",
     "Компания банкрот и должна закрыться",
     "подмена: эталон «Das Unternehmen ist bankrott und muss schließen»"),
    (13686, "example_pl",
     "Zapomniałem okularów przeciwsłonecznych w domu",
     "Noszę okulary przeciwsłoneczne, kiedy świeci słońce",
     "подмена: эталон не про забытые очки"),
    (11759, "example_pl",
     "Dodaj trochę czosnku do zupy",
     "Czosnek sprawia, że jedzenie jest smaczne",
     "подмена: эталон «Der Knoblauch macht das Essen lecker»"),
    (11762, "example_pl",
     "To mięso jest twarde jak podeszwa",
     "To mięso było za twarde do jedzenia",
     "подмена: идиома вместо эталона, и время не то"),

    # ══ формы, которых в языке нет ══════════════════════════════
    (13686, "example_uk",
     "Я носю сонячні окуляри на сонці",
     "Я ношу сонячні окуляри, коли світить сонце",
     "«носю» не форма: нужно «ношу»; и потеряна подчинённая фраза"),
    (16290, "example_uk",
     "Дві країни укладли перемир'я",
     "Дві країни уклали перемир'я",
     "«укладли» не форма: нужно «уклали»"),
    (10659, "example_uk",
     "Він почував себе дійсно принижений після критики",
     "Він почував себе дійсно приниженим після критики",
     "«почувати себе» требует орудного: «приниженим»"),
    (14521, "example_tr",
     "Yeni arabanın tasarımı bana hoşunuza gidiyor",
     "Yeni arabanın tasarımı hoşuma gidiyor",
     "«hoşunuza» второе лицо множественного; нужно «hoşuma»"),
    (15086, "example_tr",
     "Kuşun erkek cinsiyeti renkli tüylere sahip",
     "Kuşun erkeği renkli tüylere sahip",
     "«erkek cinsiyeti» это пол как понятие, а не самец"),
    (13686, "example_tr",
     "Güneşte güneş gözlüğü takıyorum",
     "Güneş çıktığında güneş gözlüğü takıyorum",
     "«güneş» дважды подряд — запинка при чтении"),
    (10657, "example_pl",
     "Samochód nagle nadjechał z przeciwka, ależ mnie napędził przestrachu",
     "Samochód nagle nadjechał z przeciwka, to był prawdziwy przestrach",
     "«napędzić przestrachu» не польский оборот: говорят «napędzić strachu»"),

    # ══ слово не из своего списка ═══════════════════════════════
    (14058, "example_uk",
     "Керівник на цьому тижні недосяжний",
     "Керівник на цьому тижні недоступний",
     "«недосяжний» о цели, а не о человеке; в списке «доступний»"),
    (10644, "example_tr",
     "Utançtan sinirli bir şekilde güldü",
     "Mahcubiyetten sinirli bir şekilde güldü",
     "«utanç» это Scham (отдельный ряд 10593); Verlegenheit — «mahcubiyet»"),
    (7318, "example_tr",
     "Şehir park için ücret alıyor",
     "Şehir park için ücret tahsil ediyor",
     "ни одного слова из списка не было; «tahsil etmek» есть"),
    (16290, "example_tr",
     "İki ülke silah bırakmayı kabul etti",
     "İki ülke ateşkesi kabul etti",
     "«ateşkes» это и есть перемирие, и оно первое в списке"),
    (16291, "example_tr",
     "Astsubay operasyonu yönetti",
     "Başçavuş operasyonu yönetti",
     "«astsubay» нет в списке, а «başçavuş» стоит первым"),
    (10660, "example_tr",
     "Çocuklar bugün çok heyecanlı ve her yerde oynuyorlar",
     "Çocuklar bugün çok neşeli ve her yerde oynuyorlar",
     "«heyecanlı» это взволнованный; в списке «neşeli»"),
    (15085, "example_uk",
     "Мій друг завжди мені допомагає, коли у мене проблеми",
     "Мій товариш завжди мені допомагає, коли у мене проблеми",
     "«друг» нет в списке, а «товариш» стоит первым"),
    (15085, "example_tr",
     "Dostum sorunum olduğunda her zaman bana yardım ediyor",
     "Arkadaşım sorunum olduğunda her zaman bana yardım ediyor",
     "«dost» нет в списке, а «arkadaş» стоит первым"),
    (17814, "example_tr",
     "Bir fikri getirebilir miyim?",
     "Fikrimi sunabilir miyim?",
     "потеряно «meine», и «getirmek» не из списка"),

    # ══ потерянное и добавленное слово ══════════════════════════
    (12672, "example_pl",
     "Zaraza rozprzestrzeniła się bardzo szybko",
     "Zaraza szybko rozprzestrzeniła się w mieście",
     "потеряно «in der Stadt», добавлено «bardzo»"),
    (7321, "example_pl",
     "Atak przeciwnika był zupełnie niespodziewany",
     "Atak przeciwnika był niespodziewany",
     "«zupełnie» в эталоне нет"),
    (7340, "example_pl",
     "Musisz stosować tę metodę w projekcie",
     "Musisz zastosować tę metodę w swoim projekcie",
     "потеряно «deinem»"),

    # ══ сочетаемость ════════════════════════════════════════════
    (18250, "example_ru",
     "Мне нужно почистить дом",
     "Мне нужно убрать дом",
     "дом не «чистят», а убирают; в pl «posprzątać»"),
    (18250, "example_uk",
     "Мені потрібно почистити будинок",
     "Мені потрібно прибрати будинок",
     "то же"),
    (18754, "example_ru",
     "Я неделями работал тяжело",
     "Я неделями тяжело работал",
     "порядок слов разрушал фразу"),
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
