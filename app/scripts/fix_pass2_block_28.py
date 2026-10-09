"""ВТОРОЙ ПРОХОД, блок 28 (ряды 5401–5600): 67 правок.

ДВЕНАДЦАТАЯ ТРОЙКА en+uk+tr:

    erleiden (12708)  de «Sie hat große VERLUSTE erlitten» — потери, ОНА
        en «I suffered a serious INJURY»
        uk «Я перенес серйозну ТРАВМУ»
        tr «Ağır bir YARALANMA yaşadım»
        ru «Она претерпела большие потери», pl «Poniosła duże straty»

Здесь тройка сменила не только существительное, но и лицо: эталон про
«она», три языка написали «я». Расклад прежний — ru и pl верны.

ДВА РЯДА, ГДЕ КАРТОЧКА УЧИЛА ОДНОМУ И ТОМУ ЖЕ РАЗНЫМИ НЕМЕЦКИМИ
СЛОВАМИ. Это не дубль по строгой проверке, а хуже:

    Nachtwache  (8961)  ru «Он работает в НОЧНУЮ СМЕНУ в больнице»
    Nachtschicht (8963) ru «...работать в НОЧНУЮ СМЕНУ»

`Nachtwache` это дежурство, `Nachtschicht` — смена, и по-русски,
по-украински и по-английски обе карточки показывали одно и то же
словосочетание. Турецкий и польский различали их сами («gece nöbeti»
против «gece vardiyası», «nocny dyżur» против «nocna zmiana»), и по ним
выровнены остальные три. В строгий список дублей ряд не попадает —
немецкие слова разные, — и поиском такое не находится: нужен глаз.

ПОЛЬСКИХ ПОДМЕН ТРИ, И ОДНА ИЗ НИХ САМАЯ ДАЛЁКАЯ ЗА ПРОХОД:

    zweieinhalb (13545)  de «Das dauert zweieinhalb Stunden»
                         pl «Mój syn ma dwa i pół roku»
    plündern    (16349)  de «Die Piraten plündern Schiffe auf dem Meer»
                         pl «Żołnierze plądrowali okoliczne wioski»
    Glücksspiel (12222)  tr «Kumarbazlık onu iflasa sürükledi»

Первая держит только числительное, всё остальное придумано. Турецкая в
`Glücksspiel` того же рода: вместо «азартная игра вызывает зависимость»
— «игра довела его до банкротства».

ЧТО ПОДТВЕРДИЛО НАБЛЮДЕНИЕ ПРО УЧАСТКИ. Ряд `geheimnisvoll` (10740)
стоит в этом блоке, а `geheimnisvolle` (10551) — в блоке 19. Заголовок
второго это склонённая форма первого, и переводы у них совпадают. Пока
владелец не поправит заголовок, дублем они формально не считаются;
после правки станут. Записано в HANDOVER к списку заголовков.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ КЛАСС: тройка en+uk+tr, двенадцатая ═════════════════════
    (12708, "example_en",
     "I suffered a serious injury",
     "She suffered great losses",
     "подмена и существительного, и лица: эталон «Sie hat große Verluste»"),
    (12708, "example_uk",
     "Я перенес серйозну травму",
     "Вона зазнала великих втрат",
     "то же; ru и pl верны"),
    (12708, "example_tr",
     "Ağır bir yaralanma yaşadım",
     "Büyük kayıplara uğradı",
     "то же"),

    # ══ две карточки учили одному словосочетанию ════════════════
    (8961, "example_ru",
     "Он работает в ночную смену в больнице",
     "Он на ночном дежурстве в больнице",
     "«ночная смена» — это ряд `Nachtschicht` (8963); здесь дежурство"),
    (8961, "example_uk",
     "Він працює в нічну зміну в лікарні",
     "Він на нічному чергуванні в лікарні",
     "то же; tr и pl различали ряды сами"),
    (8961, "example_en",
     "He works the night shift at the hospital",
     "He is on night duty at the hospital",
     "то же"),

    # ══ КЛАСС: подменённое предложение ══════════════════════════
    (13545, "example_pl",
     "Mój syn ma dwa i pół roku",
     "To potrwa dwie i pół godziny",
     "подмена: от эталона осталось только числительное"),
    (16349, "example_pl",
     "Żołnierze plądrowali okoliczne wioski",
     "Piraci plądrują statki na morzu",
     "подмена: солдаты и деревни вместо пиратов и кораблей"),
    (12222, "example_tr",
     "Kumarbazlık onu iflasa sürükledi",
     "Kumar bağımlılık yaratabilir",
     "подмена: эталон «Glücksspiel kann süchtig machen»"),

    # ══ формы, которых в языке нет ══════════════════════════════
    (10751, "example_uk",
     "Його зауваження були абсолютно невмісні",
     "Його зауваження були абсолютно недоречні",
     "«невмісні» не слово; в списке «недоречний»"),
    (10762, "translation_uk",
     "удаваний, прикидуваний, награний",
     "удаваний, нещирий, награний",
     "«прикидуваний» не форма украинского языка"),
    (17197, "translation_uk",
     "перетинати, перехрещувати, скрещувати тварин або рослини, крейсерувати",
     "перетинати, перехрещувати, схрещувати тварин або рослини, крейсерувати",
     "«скрещувати» русское; по-украински «схрещувати»"),
    (7434, "example_uk",
     "Собака втекла",
     "Собака втік",
     "«собака» в украинском мужского рода"),
    (13545, "example_uk",
     "Це займе два з половиною годин",
     "Це займе дві з половиною години",
     "«година» женского рода: «дві з половиною години»"),

    # ══ слово не из своего списка ═══════════════════════════════
    (10743, "example_tr",
     "Haberler gerçekten korkunç",
     "Haberler gerçekten korkutucu",
     "«korkunç» нет в списке, а «korkutucu» стоит первым"),
    (16339, "example_tr",
     "Rapor bunun güvenli olduğunu gösteriyor",
     "Bilirkişi raporu bunun güvenli olduğunu gösteriyor",
     "в списке «bilirkişi raporu», а пример давал половину"),
    (17973, "example_tr",
     "Bu yaşam şekli bizimkinden tamamen farklı",
     "Bu yaşam biçimi bizimkinden tamamen farklı",
     "«yaşam şekli» нет в списке, а «yaşam biçimi» стоит первым"),
    (11779, "example_tr",
     "Dikkat, biber oldukça acı",
     "Dikkat, karabiber oldukça acı",
     "«biber» это овощ; чёрный перец — «karabiber», и он первый"),
    (1628, "example_tr",
     "Lütfen içkiyi soğut",
     "Lütfen içeceği soğut",
     "«içki» это спиртное; `Getränk` — любой напиток"),
    (7438, "example_tr",
     "Film başarısız oldu",
     "Film bir başarısızlıktı",
     "ряд о существительном, а пример давал прилагательное"),
    (16351, "example_tr",
     "Polis şüpheli kişiyi izliyor",
     "Polis şüpheliyi gizlice izliyor",
     "`beschatten` это слежка; в списке «gizlice izlemek»"),
    (16344, "example_pl",
     "Nadużywanie alkoholu to duży problem",
     "Nadużycie alkoholu to duży problem",
     "«nadużywanie» отглагольное; в списке существительное «nadużycie»"),
    (2236, "example_ru",
     "Я выдаю справку",
     "Я выдаю свидетельство",
     "`Zeugnis` это свидетельство; в en, uk, tr и pl оно"),
    (16341, "example_ru",
     "Эта улика доказывает его вину",
     "Улика показывает его вину",
     "добавлено «Эта», и «доказывает» вместо «zeigt»"),
    (7435, "example_ru",
     "Жужжание двигателя было громким",
     "Гудение двигателя было громким",
     "двигатель не жужжит; `Surren` здесь гудение, и оно в списке"),
    (7435, "example_uk",
     "Дзижчання двигуна було гучним",
     "Гудіння двигуна було гучним",
     "то же"),
    (18263, "example_ru",
     "Одежда сохнет на солнце",
     "Бельё сохнет на солнце",
     "`Wäsche` это бельё; в uk, tr, en и pl бельё"),
    (17586, "example_ru",
     "Одним кликом откроется сайт",
     "Одним кликом откроется страница",
     "`Seite` это страница, а не сайт; в en, tr и pl страница"),
    (17586, "example_uk",
     "Одним кліком відкриється сайт",
     "Одним кліком відкриється сторінка",
     "то же"),
    (17585, "example_ru",
     "Штепсель ослаблен, вставь его получше",
     "Вилка плохо держится, вставь её получше",
     "«штепсель ослаблен» не по-русски; «вилка» стоит в списке первой"),
    (17585, "example_uk",
     "Штепсель розхитаний, вставляй його краще",
     "Вилка погано тримається, вставляй її краще",
     "то же"),
    (10745, "example_ru",
     "Они не оценили его заслуги по достоинству",
     "Они не оценили его достижение",
     "`Leistung` в единственном числе; в en, uk и pl достижение"),

    # ══ управление и сочетаемость ═══════════════════════════════
    (16337, "example_tr",
     "Komutan askerlerine yürümelerini emretti",
     "Komutan askerlere yürüyüş emri verdi",
     "«yürümek» это идти пешком; `marschieren` — «yürüyüş»"),
    (14544, "example_tr",
     "Davul yüksek sesle çalıyor",
     "Davulun sesi çok yüksek",
     "«davul çalıyor» значит «играет на барабане», а не «звучит»"),
    (12715, "example_tr",
     "Kazadan sonra amnezi yaşadı",
     "Kazadan sonra amnezi geçirdi",
     "«amnezi yaşamak» не оборот: говорят «geçirmek»"),
    (18266, "example_tr",
     "Eşiğe dikkat et, tökezlemeyesin",
     "Tökezlememek için eşiğe dikkat et",
     "«tökezlemeyesin» не живая форма; цель передаётся через «için»"),
    (18268, "example_tr",
     "Misafirler iyi barındırılıyor",
     "Misafirler iyi yerleştirilmiş",
     "эталон о состоянии «sind untergebracht», а не о длящемся действии"),
    (7439, "example_pl",
     "On przelał łzy",
     "Wylał łzy",
     "«przelać łzy» не оборот: говорят «wylać łzy»"),
    (13547, "example_pl",
     "Postaw przecinek w tym zdaniu",
     "Nie zapomnij przecinka w tym zdaniu",
     "эталон «Vergiss das Komma nicht» — не поставь, а не забудь"),
    (18267, "example_pl",
     "Mogę zostawić swoje rzeczy w szafce w szkole",
     "Mogę włożyć swoje rzeczy do szafki w szkole",
     "«zostawić» это оставить; эталон «legen» — положить"),
    (12222, "example_pl",
     "Hazard potrafi naprawdę wciągnąć",
     "Hazard może uzależniać",
     "«wciągnąć» это увлечь; `süchtig machen` — вызывать зависимость"),
    (10754, "example_pl",
     "Pani życzliwość na zawsze pozostanie w moim sercu",
     "Jej życzliwość na zawsze pozostanie w moim sercu",
     "«Ihre» прочитано как вежливое «Ваша»; в остальных четырёх «её»"),
    (10756, "example_uk",
     "Вона честолюбива студентка і наполегливо вчиться",
     "Вона честолюбива студентка і наполегливо працює",
     "`arbeitet hart` это работает; в остальных четырёх работа"),
    (8967, "example_uk",
     "Засновник цієї компанії був геніальною людиною",
     "Засновник цієї компанії був генієм",
     "`war ein Genie` — был гением"),
    (16350, "example_uk",
     "Збройні сили країни готові до оборони",
     "Збройні сили відповідають за оборону країни",
     "потеряно «zuständig»: силы не «готовы», а отвечают"),
    (12710, "example_uk",
     "Пацієнт лежить у відділенні інтенсивної терапії",
     "Пацієнт лежить у відділенні інтенсивної терапії в лікарні",
     "потеряно «im Krankenhaus»: в остальных четырёх оно есть"),
    (9830, "example_uk",
     "Я йду до пекарні кожного ранку",
     "Я ходжу до пекарні кожного ранку",
     "«йду» однократно; «jeden Morgen» требует многократного «ходжу»"),
    (7447, "example_uk",
     "Ми не можемо перетинати кордон",
     "Нам не можна перетинати кордон",
     "«dürfen nicht» это нельзя, а не «не можем»"),
    (1922, "example_uk",
     "Я серфлю в інтернеті",
     "Я сиджу в інтернеті",
     "«серфлю» не живая форма; в списке «сидіти в інтернеті» первым"),
    (17198, "example_uk",
     "На автостраді була велика пробка",
     "На автостраді був величезний затор",
     "«riesig» это огромный, а не большой; «затор» стоит в списке первым"),

    # ══ время глагола ═══════════════════════════════════════════
    (1181, "example_tr",
     "Ders bugün iptal oldu",
     "Ders bugün iptal oluyor",
     "прошедшее против «fällt heute aus»"),
    (1181, "example_pl",
     "Zajęcia zostały dziś odwołane",
     "Zajęcia są dziś odwołane",
     "то же"),
    (17197, "example_ru",
     "Наши пути пересекаются",
     "Наши пути пересекутся",
     "настоящее против «wird sich kreuzen»; в en, tr и pl будущее"),
    (17197, "example_uk",
     "Наші дороги часто перетинаються",
     "Наші дороги перетнуться",
     "то же, и добавлено «часто»"),

    # ══ потерянное и добавленное слово ══════════════════════════
    (16340, "example_ru",
     "Эксперт обезвредил бомбу",
     "Эксперт по взрывчатке обезвредил бомбу",
     "потеряно «Sprengstoff-»: в en и tr специалист назван"),
    (16340, "example_uk",
     "Фахівець знешкодив бомбу",
     "Фахівець із вибухівки знешкодив бомбу",
     "то же"),
    (16340, "example_pl",
     "Ekspert rozbroił bombę",
     "Ekspert od materiałów wybuchowych rozbroił bombę",
     "то же"),
    (12705, "example_tr",
     "Çabuk iyileşmeler diliyorum",
     "Sana çabuk iyileşmeler diliyorum",
     "потеряно «dir»"),
    (8969, "example_tr",
     "Kalp cerrahisinde uzmanlaşmış",
     "O, kalp cerrahisinde uzmanlaşmış",
     "потеряно подлежащее «Er»"),
    (10739, "example_ru",
     "Она очень любезный человек",
     "Она любезный человек",
     "«очень» в эталоне нет"),
    (10739, "example_uk",
     "Вона дуже люб'язна людина",
     "Вона люб'язна людина",
     "то же"),
    (10739, "example_tr",
     "O çok kibar bir kişi",
     "O kibar bir kişi",
     "то же"),
    (18773, "example_tr",
     "İlkbahar aylarında çiçekler açar",
     "İlkbaharda çiçekler açar",
     "«aylarında» в эталоне нет"),
    (9829, "example_tr",
     "Mağazanın birçok sadık müşterisi var",
     "Mağazanın sadık bir müşteri kitlesi var",
     "«birçok» в эталоне нет, и `Kundschaft` — это клиентура целиком"),
    (13544, "example_pl",
     "Przyszedłem tu tylko przez niego",
     "Przyszedłem tu przez niego",
     "«tylko» в эталоне нет"),
    (12713, "example_pl",
     "Po imprezie byłem jeszcze w alkoholowym upojeniu",
     "Po imprezie byłem jeszcze w upojeniu",
     "«alkoholowym» в эталоне нет"),
    (2734, "example_pl",
     "Trwa duży protest przeciwko nowym przepisom",
     "Trwa duży protest przeciwko nowej zasadzie",
     "множественное против «die neue Regel»"),
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
