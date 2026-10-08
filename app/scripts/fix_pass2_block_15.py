"""ВТОРОЙ ПРОХОД, блок 15 (ряды 2801–3000) + СМЕТЁННЫЙ КЛАСС ПО ВСЕЙ БАЗЕ.

Блок дал ещё четыре подменённых предложения — класс, открытый в блоке
14, оказался крупнее, чем казался, и в нём обнаружилась закономерность:

    Zutritt    (3078)  en, uk, tr подменены — ru и pl верны
    abschalten (1110)  en, uk, tr подменены — ru и pl верны
    Notruf     (12561) en, uk, tr подменены — ru и pl верны
    einnehmen  (12559) en, uk, tr: «пациент» вместо «ты» — ru и pl верны

Четыре ряда, и каждый раз ТЕ ЖЕ ТРИ ЯЗЫКА. Это не случайные ошибки
перевода, а один источник: английский, украинский и турецкий писались
вместе, и вместе же ушли от эталона. В блоке 14 было то же самое у
`auftreten` (14438).

ПОЭТОМУ НАПИСАНА ПРИМЕТА. `scan_length_outlier`: перевод вдвое короче
нормы своего языка. Норма — медиана отношения длин по базе для каждого
языка отдельно (en 1.00, ru/uk/pl 0.80, tr 0.71), потому что прямое
сравнение с немецким дало 222 попадания, из них ~200 турецких — это
агглютинация, а не дефект.

Порог выбран замером, а не на глаз, и первая самопроверка его
забраковала: законное «Пастух доглядав овець» (0.54) и потерянный
оборот в `Knüppel` (0.42) стояли по одну сторону. При 0.50 улов 52
вместо 142, доля настоящих — две пятых вместо одной седьмой.

Примета нашла по всей базе 17 рядов, которых глазами в этих блоках не
было. Из них стоит назвать два:

    ausstehen (7070)  de «DER Zahlung steht noch aus»
        Род в эталоне: «die Zahlung». Нашлось потому, что украинский и
        турецкий в этом ряду потеряли вторую половину фразы, и я полез
        смотреть ряд целиком.

    Begleiterin (15291)  en «She's the artistS companion on tour»
        Пропущен апостроф. `scan_en_apostrophe` этого не видит: она
        ищет лишние и битые апострофы, а не отсутствующие.

Остальное в блоке — потерянное слово и слово не из своего списка:

    Bude (18183)  uk «Його КІМНАТА — повний безлад»
        «кімната» это Zimmer; карточка показывает «кімнатка».

    anwesend (6934)  tr «Tüm öğrenciler derste miydi?»
        Слова ряда в примере нет вообще: «были ли все студенты на
        лекции» без «присутствовали». Рядом ряд 13586 пишет
        «Hazır bulunan» правильно.

    Hochzeitstag (15014)  tr «Bugün bizim evlilik yıldönümü»
        При «bizim» турецкий требует притяжательного окончания:
        «yıldönümümüz».
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ КЛАСС: подменённое предложение, en+uk+tr одной рукой ══════
    (3078, "example_en",
     "No entry",
     "Access to the gym costs extra",
     "подмена: эталон «Der Zutritt zum Fitnessstudio kostet extra»; ru и pl верны"),
    (3078, "example_uk",
     "Вхід заборонено",
     "Вхід до тренажерного залу оплачується окремо",
     "то же"),
    (3078, "example_tr",
     "Giriş yasak",
     "Spor salonuna giriş ayrıca ücretlidir",
     "то же"),
    (1110, "example_en",
     "Don't forget to switch off the light",
     "On vacation I can finally unwind",
     "подмена: эталон «Im Urlaub kann ich endlich abschalten»; ru и pl верны"),
    (1110, "example_uk",
     "Не забудь вимкнути світло",
     "У відпустці я нарешті можу розслабитися",
     "то же"),
    (1110, "example_tr",
     "Işığı kapatmayı unutma",
     "Tatilde sonunda kafamı dinleyebiliyorum",
     "то же"),
    (12561, "example_en",
     "Call emergency services right now",
     "I have to make an emergency call",
     "подмена: эталон «Ich muss einen Notruf absetzen»; ru и pl верны"),
    (12561, "example_uk",
     "Викличте службу порятунку, сталася аварія",
     "Мені потрібно зробити екстрений виклик",
     "то же"),
    (12561, "example_tr",
     "Hemen acil servisleri ara",
     "Acil bir çağrı yapmam gerekiyor",
     "то же"),
    (12559, "example_en",
     "The patient must take the medicine",
     "You have to take the medicine",
     "подменено лицо: эталон «Du musst das Medikament einnehmen»"),
    (12559, "example_uk",
     "Пацієнт повинен прийняти ліки",
     "Ти повинен прийняти ліки",
     "то же"),
    (12559, "example_tr",
     "Hasta ilacı almalıdır",
     "İlacı almalısın",
     "то же"),

    # ══ КЛАСС по примете: потерянный оборот и подмена, вся база ══
    (2734, "example_en",
     "There is a protest",
     "There is a big protest against the new rule",
     "потеряно «großen ... gegen die neue Regel»; ru и pl целы"),
    (2734, "example_uk",
     "Відбувається протест",
     "Проти нового правила відбувається великий протест",
     "то же"),
    (2734, "example_tr",
     "Protesto var",
     "Yeni kurala karşı büyük bir protesto var",
     "то же"),
    (7070, "example_de",
     "Der Zahlung steht noch aus, wir warten auf das Geld",
     "Die Zahlung steht noch aus, wir warten auf das Geld",
     "род в эталоне: «die Zahlung»"),
    (7070, "example_uk",
     "Рахунок досі залишається непокритим",
     "Платіж досі залишається несплаченим, ми чекаємо на гроші",
     "потеряна вторая половина фразы; «рахунок» это Rechnung, а не Zahlung"),
    (7070, "example_tr",
     "Fatura hâlâ ödenmemiş kaldı",
     "Fatura hâlâ ödenmemiş, parayı bekliyoruz",
     "потеряно «wir warten auf das Geld»"),
    (7170, "example_pl",
     "Babcia wychowała mnie sama",
     "Babcia wychowała mnie, bo moi rodzice musieli pracować",
     "потеряна причина, и добавлено «sama», которого в эталоне нет"),
    (7698, "example_pl",
     "Uderzył pałką w stół",
     "Uderzył pałką w stół, żeby zwrócić uwagę",
     "потеряно «um Aufmerksamkeit zu bekommen»"),
    (10473, "example_pl",
     "Ale ty jesteś szczęściarz",
     "Jesteś prawdziwym szczęściarzem, że wygrałeś na loterii",
     "потеряно «dass du die Lotterie gewonnen hast»"),
    (10959, "example_pl",
     "Nie bądź takim słabeuszem",
     "On jest słabeuszem i potrzebuje pomocy przy trudnych zadaniach",
     "подмена: эталон описывает его, а не велит не быть таким"),
    (12640, "example_pl",
     "Lekarz pobrał próbkę tkanki",
     "Rana dobrze się goi, tkanka jest już prawie zagojona",
     "подмена: эталон про заживление раны, а не про взятие пробы"),
    (12640, "example_tr",
     "Yaranın dokusu iki hafta sonra neredeyse tamamen iyileşti",
     "Yara iyi iyileşiyor, doku neredeyse tamamen düzeldi",
     "«iki hafta sonra» в эталоне нет"),
    (13555, "example_uk",
     "Я задоволений обома варіантами",
     "Їжа була смачна, і обслуговування теж, я задоволений обома",
     "потеряна первая половина фразы"),
    (13555, "example_pl",
     "Jestem zadowolony z obu rzeczy",
     "Jedzenie było dobre i obsługa też, jestem zadowolony z obu",
     "то же"),
    (13975, "example_en",
     "Your explanation was very clear",
     "Your explanation was very clear and I understood everything",
     "потеряно «und ich habe alles verstanden»"),
    (13997, "example_uk",
     "Усі згідно закивали головами",
     "Ми згодні в тому, що це гарна ідея",
     "подмена: эталон «Wir stimmen darin überein, dass das eine gute Idee ist»"),
    (14155, "example_en",
     "I couldn't persuade him otherwise",
     "I couldn't change his mind, he's sticking to his opinion",
     "потеряно «er bleibt bei seiner Meinung»"),
    (14155, "example_pl",
     "Nie udało mi się go przekonać",
     "Nie udało mi się go przekonać, zostaje przy swoim zdaniu",
     "то же"),
    (15127, "example_tr",
     "Soğukta uzuvlarım uyuştu",
     "Kol, insan vücudunun önemli bir uzvudur",
     "подмена: эталон «Der Arm ist ein wichtiges Glied des menschlichen Körpers»"),
    (15291, "example_pl",
     "Przyszedł na przyjęcie ze swoją towarzyszką",
     "Ona jest towarzyszką artysty w trasie",
     "подмена: эталон «Sie ist die Begleiterin des Künstlers auf der Tournee»"),
    (15291, "example_tr",
     "Sanatçının turne eşlikçisidir",
     "Turnede sanatçının refakatçisidir",
     "«eşlikçi» не из своего списка: там «refakatçi»"),
    (15291, "example_en",
     "She's the artists companion on tour",
     "She's the artist's companion on tour",
     "пропущен апостроф: «artists» вместо «artist's»"),
    (16609, "example_ru",
     "Музей охраняется круглосуточно",
     "Охрана музея осуществляется круглосуточно",
     "слова ряда в примере не было: карточка показывает «охрана»"),
    (16905, "example_uk",
     "Трибунал його засудив",
     "Трибунал засудив його до п'яти років позбавлення волі",
     "потеряно «zu fünf Jahren Haft»"),
    (16905, "example_tr",
     "Mahkeme onu mahkum etti",
     "Özel mahkeme onu beş yıl hapse mahkûm etti",
     "потеряно «zu fünf Jahren Haft»; и «mahkum» без циркумфлекса"),
    (18322, "example_pl",
     "Wyrzuć to do śmietnika",
     "Śmieci należą do śmietnika, a nie na ulicę",
     "подмена: эталон не велит, а констатирует"),
    (18322, "example_tr",
     "Çöp çöp kutusunda olmalı, sokakta değil",
     "Çöp, sokağa değil çöp kutusuna atılmalı",
     "«Çöp çöp» подряд — запинка при чтении вслух"),

    # ══ эталон: опечатка и не то слово ════════════════════════════
    (10370, "example_de",
     "Mir gehts heute richtig elend",
     "Mir geht's heute richtig elend",
     "пропущен апостроф; по базе 13 рядов с апострофом против этого одного"),
    (10372, "example_de",
     "Lass dich nicht von ihm erschrecken",
     "Lass dich nicht von ihm schrecken",
     "слово ряда — «schrecken», а «erschrecken» это отдельный ряд 10321"),

    # ══ подмена и выдумка в одном языке ══════════════════════════
    (10379, "example_uk",
     "Я дивуюся твоєму терпінню",
     "Я дивуюся твоїй реакції",
     "эталон «über deine Reaktion»; «терпіння» приехало из ряда bewundern"),
    (6920, "example_uk",
     "Книга переплетена красивою шкірою",
     "Книга переплетена",
     "«красивою шкірою» в эталоне «Das Buch ist gebunden» нет"),
    (13656, "example_pl",
     "Na rowerze zawsze zakładaj kask",
     "Nie zapomnij założyć kasku podczas jazdy na rowerze",
     "эталон «Vergiss nicht»: не «всегда надевай», а «не забудь»"),
    (17115, "example_ru",
     "Произошла тяжёлая авария",
     "Произошла тяжёлая автомобильная авария",
     "карточка показывает «автомобильная авария»; в uk так и написано"),

    # ══ потерянное слово ═════════════════════════════════════════
    (16086, "example_en",
     "That was royal treatment",
     "That was royal treatment for us",
     "потеряно «für uns»: в польском оно есть"),
    (16086, "example_ru",
     "Это было королевское обращение",
     "Это было королевское обращение с нами",
     "то же"),
    (16086, "example_uk",
     "Це було королівське ставлення",
     "Це було королівське ставлення до нас",
     "то же"),
    (16086, "example_tr",
     "Bu kraliyet muamelesiydi",
     "Bu bize kraliyet muamelesiydi",
     "то же"),
    (6929, "example_tr",
     "Burada olanlar inanılmaz",
     "Burada olanlar gerçekten inanılmaz",
     "потеряно «einfach»: в остальных четырёх языках усиление есть"),

    # ══ слово не из своего списка и грамматика ═══════════════════
    (18183, "example_uk",
     "Його кімната — повний безлад",
     "Його кімнатка — повний безлад",
     "«кімната» это Zimmer; карточка показывает «кімнатка»"),
    (6934, "example_tr",
     "Tüm öğrenciler derste miydi?",
     "Tüm öğrenciler derste mevcut muydu?",
     "слова ряда в примере не было; «mevcut» есть в списке"),
    (15014, "example_tr",
     "Bugün bizim evlilik yıldönümü",
     "Bugün bizim evlilik yıldönümümüz",
     "при «bizim» нужно притяжательное окончание"),
    (16078, "example_uk",
     "Журі прийняло складне рішення",
     "Жюрі прийняло складне рішення",
     "ряд сам себе противоречил: в списке «жюрі», в примере «Журі»"),
    (6946, "example_uk",
     "Незнайомка дзвонила мені сьогодні",
     "Незнайомка подзвонила мені сьогодні",
     "«rief an» однократное; в ru «позвонила»"),
    (6924, "example_tr",
     "Bu tamamen olası olmayan",
     "Bu tamamen olasılıksız",
     "«olası olmayan» без сказуемого — не фраза"),

    # ══ генитив без апострофа: новое правило в scan_en_apostrophe ══
    (8625, "example_en",
     "The little boy sat piggyback on his fathers shoulders",
     "The little boy sat piggyback on his father's shoulders",
     "пропущен притяжательный апостроф; перечисление форм этого не видело"),
    (16103, "example_en",
     "The hearing of the witness was very important for the case",
     "The hearing of the witness was important for the case",
     "«very» добавлено: эталон «war wichtig», без «sehr»"),
]


def main() -> None:
    apply_mode = "--apply" in sys.argv
    engine = create_engine(settings.DATABASE_URL_SYNC)
    ok: list[tuple[int, str, str, str, str]] = []
    skipped: list[tuple[int, str, str | None]] = []
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
