"""ВТОРОЙ ПРОХОД, блок 35 (ряды 6801–7000): 46 правок.

САМАЯ ДЛИННАЯ ПОЛЬСКАЯ ПОЛОСА ЗА ПРОХОД: тринадцать подмен в одном
блоке против прежнего рекорда девять (блок 21).

    Krümel             (11835) «Na stole zostały okruszki PO ŚNIADANIU»
    Gebrüll            (14151) «Ryk kibiców było słychać NA CAŁEJ ULICY»
    Sexualität         (15154) «W DOMU ROZMAWIAMY OTWARCIE o seksualności»
    Ehrengast          (14622) «Był gościem honorowym NA NASZYM WESELU»
    Schürze            (13718) «ZAŁOŻYŁA fartuch PRZED GOTOWANIEM»
    Bankett            (11839) «Bankiet WESELNY trwał DO RANA»
    Schlafanzug        (13719) «DZIECI są już w piżamach»
    Mitfahrgelegenheit (17238) «...przejazdu do KRAKOWA» вместо Мюнхена
    lauschen           (14153) «DZIECI NASŁUCHIWAŁY KROKÓW NA SCHODACH»
    Tourist            (17239) «LATEM JEST TU DUŻO turystów»
    Reinfall           (10953) «Ten FILM to była kompletna klapa»
    campen             (12273) «LATEM biwakujemy NAD JEZIOREM»
    einfrieren         (11840) «Musimy zamrozić RESZTĘ MIĘSA»
    gnadenlos          (10960) «SZEF BYŁ DLA NAS bezlitosny»

У всех четырнадцати одно устройство: польская фраза безупречна и
содержит слово ряда, но говорит о другом. Ни одна примета такого не
видит.

ВТОРОЙ ЗА ПРОХОД СЛУЧАЙ ПОДМЕНЫ В ЧЕТЫРЁХ ЯЗЫКАХ ИЗ ПЯТИ, и он хуже
первого (`erstmals`, блок 29) тем, что четыре языка не согласны даже
между собой:

    verhelfen (7710)  de «Das soll ihm zum Erfolg verhelfen»
        ru «Это должно помочь ему добиться успеха» — ВЕРНО
        en «They helped him start a new career in Hollywood»
        uk «Вони допомогли йому розпочати нову кар'єру в Голлівуді»
        tr «Ona Hollywoodda yeni bir kariyer başlamaya yardım ettiler»
        pl «TEN FILM pomógł mu zdobyć SŁAWĘ»

Три языка выдумали Голливуд, а польский — фильм и славу. То есть
источник у трёх общий, а польский шёл сам. Это объясняет, почему
польская полоса в этом блоке такая длинная: польский, похоже, местами
переводился отдельным прогоном.

ТРИНАДЦАТАЯ ТРОЙКА en+uk+tr:

    Bohrer (9036)  de «Gib mir mal den kleinen Bohrer» — ДАЙ МНЕ
        en «With the drill he DRILLS A HOLE IN THE WALL»
        uk «З допомогою дрелі він ПРОСВЕРДЛЮЄ ОТВІР У СТІНІ»
        tr «Matkap ile DUVARA BIR DELIK AÇIYOR»
        ru «Дай-ка мне маленькое сверло», pl «Podaj mi to małe wiertło»

ЕЩЁ ОДИН РЯД, ГДЕ РАСХОДИТСЯ ЧИСЛО ПОДЛЕЖАЩЕГО. `lauschen` (14153):
эталон «SIE LAUSCHEN der Musik» — множественное, и верен только русский
(«Они слушают»). Английский, украинский и турецкий поставили
единственное, а польский подменил фразу целиком.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ подмена в четырёх языках из пяти ════════════════════════
    (7710, "example_en",
     "They helped him start a new career in Hollywood",
     "That should help him achieve success",
     "подмена: эталон «Das soll ihm zum Erfolg verhelfen»; верен только ru"),
    (7710, "example_uk",
     "Вони допомогли йому розпочати нову кар'єру в Голлівуді",
     "Це має допомогти йому досягти успіху",
     "то же"),
    (7710, "example_tr",
     "Ona Hollywoodda yeni bir kariyer başlamaya yardım ettiler",
     "Bu, onun başarıya ulaşmasını sağlayacak",
     "то же"),
    (7710, "example_pl",
     "Ten film pomógł mu zdobyć sławę",
     "To ma mu pomóc osiągnąć sukces",
     "то же, и польский выдумал своё, а не то же, что три других"),

    # ══ КЛАСС: тройка en+uk+tr, тринадцатая ═════════════════════
    (9036, "example_en",
     "With the drill he drills a hole in the wall",
     "Give me the small drill bit",
     "подмена: эталон «Gib mir mal den kleinen Bohrer»"),
    (9036, "example_uk",
     "З допомогою дрелі він просвердлює отвір у стіні",
     "Дай-но мені маленьке сверло",
     "то же; ru и pl верны"),
    (9036, "example_tr",
     "Matkap ile duvara bir delik açıyor",
     "Küçük matkap ucunu bana ver",
     "то же"),

    # ══ число подлежащего ═══════════════════════════════════════
    (14153, "example_en",
     "She listens to the music with her eyes closed",
     "They listen to the music with their eyes closed",
     "эталон «Sie lauschen» множественное; верен только ru"),
    (14153, "example_uk",
     "Вона слухає музику з закритими очима",
     "Вони слухають музику із закритими очима",
     "то же"),
    (14153, "example_tr",
     "Gözleri kapalı olarak müzik dinliyor",
     "Gözleri kapalı olarak müzik dinliyorlar",
     "то же"),
    (14153, "example_pl",
     "Dzieci nasłuchiwały kroków na schodach",
     "Słuchają muzyki z zamkniętymi oczami",
     "подмена целиком: дети и шаги на лестнице вместо музыки"),

    # ══ КЛАСС: польская полоса подмен ═══════════════════════════
    (11835, "example_pl",
     "Na stole zostały okruszki po śniadaniu",
     "Na stole są wszędzie okruszki, dzieci nabrudziły podczas jedzenia",
     "подмена: завтрак вместо детей, насоривших за едой"),
    (14151, "example_pl",
     "Ryk kibiców było słychać na całej ulicy",
     "Ryk kibiców był ogłuszający",
     "подмена: «слышно на всю улицу» вместо «ohrenbetäubend»"),
    (15154, "example_pl",
     "W domu rozmawiamy otwarcie o seksualności",
     "Seksualność to normalna część ludzkiego życia",
     "подмена: разговоры дома вместо «ein normaler Teil des Lebens»"),
    (14622, "example_pl",
     "Był gościem honorowym na naszym weselu",
     "Prezydent był gościem honorowym na gali",
     "подмена: свадьба вместо гала, и потерян президент"),
    (13718, "example_pl",
     "Założyła fartuch przed gotowaniem",
     "Nosi w kuchni czerwony fartuch",
     "подмена: надела перед готовкой вместо «trägt ... in der Küche»"),
    (11839, "example_pl",
     "Bankiet weselny trwał do rana",
     "Bankiet był elegancki i bardzo luksusowy",
     "подмена: свадебный банкет до утра вместо «elegant und luxuriös»"),
    (13719, "example_pl",
     "Dzieci są już w piżamach",
     "Moja nowa piżama jest bardzo wygodna",
     "подмена: дети вместо «Mein neuer Schlafanzug»"),
    (17238, "example_pl",
     "Szukam wspólnego przejazdu do Krakowa",
     "Szukam wspólnego przejazdu do Monachium",
     "подменён город: Краков вместо Мюнхена"),
    (17239, "example_pl",
     "Latem jest tu dużo turystów",
     "Turyści zwiedzają miasto",
     "подмена: «летом тут много туристов» вместо «besichtigen die Stadt»"),
    (10953, "example_pl",
     "Ten film to była kompletna klapa",
     "Nowy serial to była kompletna klapa",
     "подменено слово: фильм вместо сериала"),
    (12273, "example_pl",
     "Latem biwakujemy nad jeziorem",
     "Tego lata biwakujemy w górach",
     "подмена: у озера вместо «in den Bergen»"),
    (11840, "example_pl",
     "Musimy zamrozić resztę mięsa",
     "Powinniśmy zamrozić te produkty",
     "подмена: остатки мяса вместо «die Lebensmittel»"),
    (10960, "example_pl",
     "Szef był dla nas bezlitosny",
     "Rywalizacja była bezlitośnie trudna",
     "подмена: начальник вместо «Der Wettbewerb»"),

    # ══ формы, которых в языке нет ══════════════════════════════
    (15653, "example_uk",
     "Таргань розбігалась по кухні",
     "Тарган бігав по кухні",
     "«таргань» не слово, и «розбігалась» множественное при одном подлежащем"),
    (14622, "example_uk",
     "Президент був почесним гістю на гала-вечері",
     "Президент був почесним гостем на гала-вечері",
     "«гістю» не форма: нужно «гостем»"),
    (15650, "example_pl",
     "Liście szeleszczą na wiatrze",
     "Liście szeleszczą na wietrze",
     "«na wiatrze» не форма: нужно «na wietrze»"),
    (16465, "example_tr",
     "Müvekkile avukatının işinden çok memnundu",
     "Kadın müvekkil avukatının işinden çok memnundu",
     "«müvekkile» дательный падеж вместо подлежащего"),
    (11840, "translation_uk",
     "заморозити, замерзнути, приостановити",
     "заморозити, замерзнути, призупинити",
     "«приостановити» русизм; по-украински «призупинити»"),

    # ══ слово не из своего списка и не то слово ═════════════════
    (7700, "example_en",
     "The sword gleamed brightly in the sun",
     "The polished sword gleamed in the sun",
     "«brightly» нет в списке; `blank` это «polished»"),
    (7694, "example_tr",
     "Yağmur bütün planlarımızı boşa çıkardı",
     "Fırtına bütün planlarımızı boşa çıkardı",
     "«yağmur» это дождь; `Unwetter` — буря, и в ru, uk, pl и en буря"),
    (12793, "example_tr",
     "Yaralı asker savaş alanında yavaşça kan kaybetti",
     "Yaralı asker savaş alanında yavaşça kan kaybından öldü",
     "«kan kaybetti» это потерял кровь; `verbluten` — умер от потери крови"),
    (10954, "example_tr",
     "Haberi duyunca tamamen patladı",
     "Haberi duyunca tamamen çılgına döndü",
     "«patlamak» это взорваться; в списке «çılgına dönmek» первым"),
    (10948, "example_pl",
     "Po bójce obaj mężczyźni byli poobijani",
     "Po bójce obaj mężczyźni byli ranni",
     "«poobijani» это в ссадинах; `verletzt` — ранены"),
    (15152, "example_uk",
     "Ми повинні ставитися до інших з повагою",
     "Ми повинні ставитися до близьких з повагою",
     "«інші» нет в списке; `Mitmensch` — «близький», и оно первое"),
    (17240, "example_ru",
     "Самолёт потерпел крушение в море",
     "Самолёт разбился в море",
     "«потерпеть крушение» нет в списке, а «разбиться» стоит первым"),
    (2732, "example_uk",
     "Це відбувається без проблем",
     "Це працює без проблем",
     "`funktionieren` это работать; в ru, en, tr и pl работает"),
    (7714, "example_pl",
     "To coś pożytecznego do codziennego życia",
     "To coś pożytecznego w codziennym życiu",
     "«do codziennego życia» не управление: нужно «w codziennym życiu»"),

    # ══ потерянное и добавленное слово ══════════════════════════
    (7702, "example_tr",
     "Eski aşkını geri kazanma girişimi başarısız oldu",
     "Eski aşkını geri kazanma girişimi başarısızdı ve baştan mahkûmdu",
     "потеряно «zum Scheitern verurteilt»"),
    (12272, "example_pl",
     "Jego serwis był bardzo mocny",
     "Serwis w tenisie był bardzo mocny",
     "потеряно «beim Tennis»"),
    (7712, "example_pl",
     "To wymaga dużo cierpliwości",
     "To wymaga dużo cierpliwości i czasu",
     "потеряно «und Zeit»"),
    (14625, "example_pl",
     "Na ścianie wisi duży plakat",
     "Plakat na ścianie jest bardzo duży",
     "перестроено, и потеряно «sehr»"),
    (14623, "example_uk",
     "На біс гурт зіграв стару пісню",
     "На біс гурт зіграв ще одну стару пісню",
     "потеряно «noch»"),
    (7721, "example_pl",
     "Ogień przyjemnie trzaska w kominku",
     "Ogień przyjemnie trzaska",
     "«w kominku» в эталоне нет"),
    (14154, "example_pl",
     "Muszę jeszcze dopytać w biurze",
     "Jeszcze dopytam",
     "«w biurze» в эталоне нет, и «muszę» вместо «werde»"),
    (7711, "example_uk",
     "Ти мав би внести своє ім'я в список",
     "Ти мусиш внести своє ім'я",
     "условное вместо «Du musst», и «в список» в эталоне нет"),
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
