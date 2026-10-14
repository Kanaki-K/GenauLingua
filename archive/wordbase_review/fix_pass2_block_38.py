"""ВТОРОЙ ПРОХОД, блок 38 (ряды 7401–7600): 44 правки.

ГЛАВНОЕ В БЛОКЕ — ЗАМЕР, КОТОРЫЙ ЗАКРЫЛ КЛАСС ЦЕЛИКОМ. Ряд 7464
`Franken` (9871) дал четвёртый случай «число словами против цифры» —
pl «pięćdziesiąt franków» против «50 Franken». В блоке 36 я записал: при
четвёртом случае замерить узко, без списка числительных. Замерено, и
правило оказалось чисто структурным — «в немецком цифра есть, в переводе
цифры нет вообще»:

    168 рядов с цифрой в немецком, 106 с языком без цифры
    pl 105, uk 21, ru 18, en 4, tr 2;  только pl — 80

Класс ПОЛЬСКИЙ. Разделение на норму и дефект взято из самого немецкого:
порядковые («5. Klasse») и время («um 10 Uhr») — норма во всех
славянских, 60 рядов; измерения («50 Euro», «38 Grad», «100 PS») — 46
рядов, и вот это дефект. **44 ячейки исправлены сквозной правкой
`fix_pl_numbers_as_words.py`**, примета — `scan_number_as_word.py`.

Примета нашла и то, чего я не искал: `Anschlusszug` (1145), двойник
`Bahnsteig` — «von Gleis 5» против «с пятой платформы». Тот же вердикт
«это порядковый номер, а не измерение», вынесенный независимо от моего
решения в блоке 37. Оба оставлены и названы в примете.

САМОКРИТИКА: четыре блока я правил этот класс по одной ячейке. Второй
такой случай за проход после заголовков-повторов.

ЧЕТВЁРТАЯ ПОЛЬСКАЯ ПОЛОСА ПОДРЯД — и в ней ПОДМЕНА ЦЕЛИКОМ:

    üblicherweise (7840) de «Das Restaurant ist üblicherweise um zehn
                             Uhr geschlossen»
                         pl «ZWYKLE WRACAM DO DOMU o szóstej»

От эталона не осталось ничего, кроме наречия. Плюс первое лицо в
`verblüfft` (11017) против «Er war verblüfft», и «pyszny» вместо «den
besten» в `Apfelkuchen` (11859) — ровно то же, что в `Hackbraten` блока
37, то есть уже дважды.

ТУРЕЦКАЯ ПОЛОСА ТОЖЕ ВТОРАЯ ПОДРЯД, 10 ячеек. Две полосы разных языков
в одном блоке были новостью в блоке 37; здесь это повторилось, значит
приём надо считать правилом, а не случайностью.

ВИД КАРТОЧКИ СЛОМАН ПЯТЬ РАЗ, И ВСЕ ПЯТЬ — ОДИН МЕХАНИЗМ: в примере
слово не из своего списка, матчер молчит, карточка показывает ПЕРВЫЙ
вариант.

    beschatten (16525) ru «под наблюдением» → показывалось «вести слежку»
    touren     (17261) uk «подорожуємо»     → показывалось «гастролювати»
    Schub       (7839) pl «zastrzyk»        → показывалось «impuls»
    anspruchsvoll (7844) tr «titiz»         → показывалось «talepkâr»
    handhaben   (7874) tr «tutmak»          → показывалось «kullanmak»

Третий блок подряд с этим классом. В блоке 37 его было три случая, здесь
пять — и он держится ровно потому, что `scan_word_in_example` смотрит
обратное направление (слово ряда внутри примера), а не «слово примера
внутри списка».

ОДИН РЯД ПРАВЛЕН СО СТОРОНЫ СПИСКА, А НЕ ПРИМЕРА: `belehren` (9554).
Эталон «Der Lehrer belehrte die Schüler über die wichtigsten historischen
Ereignisse» — это нейтральное «рассказывал/разъяснял», а список ru давал
только «поучать, наставлять, инструктировать», то есть назидательные
значения. Самый человеческий русский здесь — «рассказывал», и ломать его
ради §8 значило бы сделать фразу канцелярской. Поэтому добавлено
значение, которое у `belehren` есть по Дудену («jemanden über etwas
unterrichten»), а фраза оставлена живой.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ КЛАСС: вид карточки — слово не из своего списка ══════════
    (16525, "example_ru",
     "Подозреваемый был под наблюдением полиции",
     "За подозреваемым следила полиция",
     "«под наблюдением» не из списка: показывалось «вести слежку»"),
    (16525, "example_uk",
     "Підозрюваний був під наглядом поліції",
     "За підозрюваним стежила поліція",
     "то же"),
    (17261, "example_uk",
     "Ми подорожуємо Європою цього літа",
     "Ми мандруємо Європою цього літа",
     "«подорожувати» не из списка; в нём «мандрувати»"),
    (7839, "example_pl",
     "Nowy trener dał drużynie zastrzyk nowej energii",
     "Nowy trener dał drużynie impuls nowej energii",
     "«zastrzyk» не из списка; «impuls» стоит в нём первым"),
    (7844, "example_tr",
     "Seyirciler çok titizdi ve filmi eleştirdi",
     "Seyirciler çok seçiciydi ve filmi eleştirdi",
     "«titiz» не из списка; «seçici» в нём есть"),
    (7874, "example_tr",
     "Bu aletleri dikkatli tutmalısınız",
     "Bu aletleri dikkatli kullanmalısınız",
     "«tutmak» это держать; в списке «kullanmak» первым"),
    (7855, "example_uk",
     "Ти розгортаєш газету і читаєш її",
     "Ти відкриваєш газету і читаєш її",
     "«розгортати» не из списка; в нём «відкривати»"),
    (7849, "example_uk",
     "Лікар нарешті його відпустив і сказав, що він може йти додому",
     "Лікар нарешті його виписав і сказав, що він може йти додому",
     "«відпустив» не из списка; в ru «выписал», и оно в списке uk есть"),

    # ══ правка со стороны СПИСКА, а не примера ══════════════════
    (9554, "translation_ru",
     "поучать, наставлять, инструктировать",
     "поучать, наставлять, инструктировать, рассказывать о чём-то",
     "у `belehren` есть нейтральное «unterrichten»; фраза живая, список был узкий"),
    (9554, "translation_uk",
     "повчати, наставляти, інструктувати",
     "повчати, наставляти, інструктувати, розповідати про щось",
     "то же"),

    # ══ четвёртая польская полоса подряд ════════════════════════
    (7840, "example_pl",
     "Zwykle wracam do domu o szóstej",
     "Restauracja jest zwykle zamknięta o dziesiątej",
     "подмена целиком: от эталона о ресторане не осталось ничего"),
    (11017, "example_pl",
     "Byłem zdumiony tą wiadomością",
     "Był zdumiony tą wiadomością",
     "первое лицо против «Er war verblüfft»"),
    (11859, "example_pl",
     "Babcia upiekła pyszną szarlotkę",
     "Moja babcia piecze najlepszą szarlotkę",
     "«pyszny» вместо «den besten» и прошедшее время; как в `Hackbraten`"),
    (11856, "example_pl",
     "Babcia uprawia w ogrodzie rzepę i kartofle",
     "Moja babcia uprawia w ogrodzie rzepę i ziemniaki",
     "потеряно «Meine», и «kartofle» разговорнее нейтрального эталона"),
    (12291, "example_pl",
     "Maskotką naszej drużyny jest wesoły lew",
     "Maskotką szkolnej drużyny jest wesoły lew",
     "«naszej» вместо «der Schulmannschaft»"),
    (18338, "example_pl",
     "To mieszkanie było całe zapluskwione",
     "Ten dom był całkowicie zapluskwiony",
     "«mieszkanie» вместо «Das Haus»"),
    (11028, "example_pl",
     "Z takim zmęczonym życiem nastawieniem nic z tego nie będzie",
     "Przy takim zmęczeniu życiem nic z tego nie będzie",
     "«zmęczonym życiem nastawieniem» не согласовано по-польски"),
    (12844, "example_pl",
     "Po sporcie miałem skurcz w łydce",
     "Po treningu miałem skurcz w łydce",
     "«po sporcie» калька с «nach dem Sport»; в ru «после тренировки»"),
    (7830, "example_pl",
     "Rozkłada kocyk na dziecku",
     "Rozpościera koc nad dzieckiem",
     "«kocyk na dziecku» не оборот; «rozpostrzeć» стоит в списке"),

    # ══ турецкая полоса, вторая подряд ══════════════════════════
    (14174, "example_tr",
     "O, onay olarak başını sallıyor",
     "Onaylarcasına başını sallıyor",
     "«onay olarak» не оборот; в списке «onaylarcasına»"),
    (12839, "example_tr",
     "Yaşlı adamın yıllardan hafif bir kamburu vardı",
     "Yaşlı adamın yıllardan dolayı hafif bir kamburu vardı",
     "«yıllardan» без «dolayı» фраза не согласована"),
    (7827, "example_tr",
     "Kıskançlıktan çıldırmış durumda ve doğru düşünemiyor",
     "Kıskançlıktan çılgına dönmüş ve doğru düşünemiyor",
     "«çıldırmış» не из списка; «çılgına dönmek» держит «çılgın»"),
    (12289, "example_tr",
     "Çocuk salıncakta oturuyor ve sallanıyor",
     "Çocuk salıncakta oturuyor ve ileri geri sallanıyor",
     "потеряно «hin und her»"),
    (2874, "example_tr",
     "Ajandam dolu",
     "Ajandam çok dolu",
     "потеряно «sehr»"),
    (7830, "example_tr",
     "Çocuğun üzerine bir battaniye örtüyor",
     "Çocuğun üzerine bir battaniye seriyor",
     "«örtmek» не из списка; в нём «sermek»"),
    (15178, "example_tr",
     "Ayaktakımı sokaklarda bağırıp azgınlık etti",
     "Ayaktakımı sokaklarda bağırdı ve taşkınlık yaptı",
     "«azgınlık» не тот регистр; `toben` — «taşkınlık yapmak»"),
    (11858, "example_tr",
     "Mandalina lezzetli bir turunçgil meyvesidir",
     "Mandalina en sevdiğim turunçgil meyvesi",
     "подмена: «вкусный» вместо «meine Lieblingszitrusfrucht»"),
    (14176, "example_tr",
     "Bir paketi göndermek için postaya gitmem gerekiyor",
     "Bir paketi vermek için postaneye gitmem gerekiyor",
     "«postaya» это на почту как к почте; `Postamt` — «postane»"),
    (535, "example_tr",
     "Lütfen bana bir harita verin",
     "Lütfen bana bir harita ver",
     "вы-форма против «Gib mir»; в ru и pl ты-форма"),

    # ══ обращение, лицо и время ═════════════════════════════════
    (535, "example_uk",
     "Будь ласка, дайте мені карту",
     "Дай мені, будь ласка, карту",
     "то же: вы-форма против «Gib mir»"),
    (13726, "example_en",
     "He put on his blue tie before going to work",
     "He puts on his blue tie before going to work",
     "прошедшее против «Er zieht … an»"),
    (11858, "example_en",
     "Mandarins are my favorite citrus fruits",
     "The mandarin is my favorite citrus fruit",
     "множественное против «Die Mandarine ist»"),
    (14180, "example_en",
     "He's got such a big mouth",
     "I don't like his big cheeky mouth",
     "потеряно «gefällt mir nicht» целиком"),
    (18338, "example_ru",
     "Этот дом просто кишит клопами",
     "Дом весь кишел клопами",
     "настоящее против «war», и «просто» вместо «völlig»"),

    # ══ слово не то, и калька ═══════════════════════════════════
    (14180, "example_uk",
     "Його дерзкий язик мені не подобається",
     "Його зухвалий язик мені не подобається",
     "«дерзкий» русское; по-украински «зухвалий»"),
    (15686, "example_uk",
     "Бурна ніч була небезпечною",
     "Бурхлива ніч була небезпечною",
     "«бурна» русская краткая форма; в списке «бурхливий»"),
    (12849, "example_uk",
     "Моя спина свербить",
     "У мене свербить спина",
     "калька притяжательного; по-людски «у мене свербить»"),
    (7862, "example_uk",
     "Його особистість позначена складними досвідами",
     "Його особистість позначена складним досвідом",
     "«досвід» не считается, множественного у него нет"),
    (12844, "example_uk",
     "Після спорту в мене була судома в литці",
     "Після тренування в мене була судома в литці",
     "«після спорту» калька; в ru «после тренировки»"),
    (7836, "example_uk",
     "Презентація справді вражала",
     "Презентація була справді вражаючою",
     "потеряно «sehr» и само прилагательное из списка"),
    (11033, "example_ru",
     "Бессовестный делец поступил бы именно так",
     "Бессовестный бизнесмен поступил бы так",
     "«делец» вместо «Geschäftsmann», и «именно» в эталоне нет"),
    (17839, "example_ru",
     "Концерн нанимает более десяти тысяч сотрудников по всему миру",
     "В концерне работает более десяти тысяч сотрудников по всему миру",
     "`beschäftigen` это занимать работой, а не «нанимать»; в uk верно"),
    (11028, "example_ru",
     "С таким самоубийственно безрассудным настроем ничего не выйдет",
     "С таким уставшим от жизни настроем ничего не выйдет",
     "взято третье значение; остальные пять языков про усталость от жизни"),
    (9080, "example_ru",
     "Командировочные расходы на деловую поездку будут возмещены",
     "Командировочные расходы будут возмещены",
     "«командировочные» и значит «на деловую поездку» — тавтология"),
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
