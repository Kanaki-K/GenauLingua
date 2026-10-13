"""ВТОРОЙ ПРОХОД, блок 18 (ряды 3401–3600): 65 правок.

ПЯТЫЙ БЛОК ПОДРЯД С ПОДМЕНОЙ, И ТРИ РАЗА ОДНИ И ТЕ ЖЕ ТРИ ЯЗЫКА:

    wegwerfen (3006)    de «Das kannst du ruhig wegwerfen»
        en «Don't throw that away»
        uk «Не викидай це»
        tr «Bunu atma»
        **Отрицание наоборот.** Эталон разрешает выбросить, а три
        языка запрещают. Хуже подмены: ученик выучит обратное.

    auslösen (7066)     de «Das kann bei ihm Panik auslösen»
        en, uk, tr все три про шум и сигнализацию

    zurücktreten (3064) de «Er ist als Chef zurückgetreten»
        en, uk, tr все три про «после двадцати лет»

Русский и польский в этих трёх рядах верны. Это та же закономерность,
что в блоках 14–17: en, uk и tr писались вместе.

ЗАМЕР, КОТОРЫЙ ЗАКРЫЛ ВОПРОС О ГИБРИДАХ. В блоке 17 нашлось
«ускользнути» — русская основа с украинским окончанием, которой нет ни
в одном корпусе. Здесь нашлось второе: `keineswegs` (13512) писал
«Це зовсім не **конець** історії». По-русски «конец», по-украински
«кінець», а «конець» — ни то ни другое.

Орфографический гейт `scan_soft_sign` это не ловит: «ць» законно.
Напрашивался другой формальный признак: слово, встречающееся в своём
корпусе РОВНО ОДИН РАЗ и отличающееся одной буквой от частотного слова
того же языка. Проверено по всем пяти языкам:

    en 792   ru 1262   uk 1158   tr 1301   pl 1047

**Признак мёртв, и причина в самом устройстве языков.** В языке со
словоизменением каждая форма отличается одной буквой от соседней:
«банка» → «банках», «bogaty» → «bogata», «anladı» → «anladım». Улов
состоит из законных форм целиком, и порог тут не поможет: дефект и
норма различаются не частотой, а тем, есть ли слово в языке, а этого
без словаря не узнать.

Вывод записан: у класса «гибрид двух языков» формального признака нет,
кроме орфографической невозможности. Ловится глазами.
"""

from __future__ import annotations

import sys

from sqlalchemy import create_engine, text

from app.config import settings

FIXES: list[tuple[int, str, str, str, str]] = [
    # ══ КЛАСС: подмена, и один раз — отрицание наоборот ══════════
    (3006, "example_en",
     "Don't throw that away",
     "You can safely throw that away",
     "ОТРИЦАНИЕ НАОБОРОТ: эталон разрешает, перевод запрещает"),
    (3006, "example_uk",
     "Не викидай це",
     "Це можеш спокійно викинути",
     "то же"),
    (3006, "example_tr",
     "Bunu atma",
     "Bunu rahatça atabilirsin",
     "то же"),
    (7066, "example_en",
     "The noise triggered the alarm",
     "That can trigger panic in him",
     "подмена: эталон «Das kann bei ihm Panik auslösen»"),
    (7066, "example_uk",
     "Шум викликав тривогу",
     "Це може викликати у нього паніку",
     "то же"),
    (7066, "example_tr",
     "Gürültü alarmı tetikledi",
     "Bu onda panik tetikleyebilir",
     "то же"),
    (3064, "example_en",
     "He resigned after twenty years",
     "He resigned as boss",
     "подмена: эталон «Er ist als Chef zurückgetreten»"),
    (3064, "example_uk",
     "Він пішов у відставку після двадцяти років",
     "Він пішов у відставку з посади начальника",
     "то же"),
    (3064, "example_tr",
     "Yirmi yıldan sonra istifa etti",
     "Patronluktan istifa etti",
     "то же"),
    (12177, "example_pl",
     "W sylwestra puszczaliśmy fajerwerki",
     "Fajerwerki w sylwestra były bardzo piękne",
     "подмена: эталон «Das Feuerwerk an Silvester war super schön»"),
    (11710, "example_uk",
     "Пес лиже мою долоню",
     "Пес лиже руку свого господаря",
     "подмена: эталон «die Hand seines Besitzers»"),

    # ══ ГИБРИД ДВУХ ЯЗЫКОВ: второй случай после блока 17 ═════════
    (13512, "example_uk",
     "Це зовсім не конець історії",
     "Це зовсім не кінець історії",
     "«конець» ни русское, ни украинское: по-украински «кінець»"),

    # ══ эталон: не немецкая конструкция ══════════════════════════
    (13998, "example_de",
     "Aus meinem Standpunkt ist das falsch",
     "Von meinem Standpunkt aus ist das falsch",
     "«aus einem Standpunkt» по-немецки не говорят"),
    (15037, "example_de",
     "Er kommt aus unsicherer Herkunft",
     "Er ist unbekannter Herkunft",
     "«aus Herkunft kommen» не конструкция; и четыре языка говорят «неизвестного»"),
    (15037, "example_pl",
     "Jest niepewnego pochodzenia",
     "Jest nieznanego pochodzenia",
     "то же: «неизвестного», а не «неуверенного»"),

    # ══ формы, которых в языке нет ═══════════════════════════════
    (7063, "example_uk",
     "Я намагаюся тримати його подалі від мого дитини",
     "Я намагаюся тримати його подалі від моєї дитини",
     "«дитина» жіночого роду: «моєї»"),
    (16143, "example_uk",
     "Після великої битви поле бою було скрізь покрито уламками",
     "Після великої битви поле бою було скрізь покрите уламками",
     "узгодження з «поле»: «покрите»"),
    (15497, "example_tr",
     "Kurdun kürü gri",
     "Kurdun kürkü gri",
     "«kürü» не форма: нужно «kürkü»"),
    (8858, "example_tr",
     "Bu projede sizle işbirliği yapmaktan memnunuz",
     "Bu projede sizinle işbirliği yapmaktan memnunuz",
     "«sizle» не форма: нужно «sizinle»"),
    (10453, "example_tr",
     "Sen çok geç geldiğine şaşırıyorum",
     "Bu kadar geç gelmene şaşırıyorum",
     "«Sen» в именительном при «geldiğine» не согласовано"),
    (18199, "example_tr",
     "Otelde güzel manzaralı bir süit rezerv ettik",
     "Otelde güzel manzaralı bir süit rezervasyonu yaptık",
     "«rezerv etmek» не турецкий оборот"),
    (15035, "example_tr",
     "Birbirimiz için önemsiyoruz",
     "Birbirimize özen gösteriyoruz",
     "«önemsemek» требует дополнения"),
    (7068, "example_uk",
     "Боксер наносить удар та потрапляє супернику",
     "Боксер завдає удару і влучає в суперника",
     "«потрапляє супернику» не узгоджено"),
    (7068, "example_tr",
     "Boksör vurur ve rakibini vurur",
     "Boksör vuruyor ve rakibine isabet ediyor",
     "«vurur» дважды в одной фразе"),
    (18200, "example_tr",
     "Oturma odamı için yeni perdeler aldım",
     "Oturma odam için yeni perdeler aldım",
     "«için» не берёт винительный"),
    (7057, "example_tr",
     "Birlikte kiliseye ayinlere gidiyoruz",
     "Birlikte kilisedeki ayine gidiyoruz",
     "два направительных падежа подряд, и множественное вместо единственного"),

    # ══ слово не из своего списка и не то слово ══════════════════
    (2335, "example_tr",
     "Yakında yeni bir işletme açıyoruz",
     "Yakında yeni bir dükkân açıyoruz",
     "«işletme» это предприятие, а Laden — магазин"),
    (7065, "example_tr",
     "Parti için orijinal bir fikirdi",
     "Parti için sıra dışı bir fikirdi",
     "«orijinal» нет в списке, а «sıra dışı» стоит первым"),
    (7064, "example_tr",
     "Kötü haberin ardından tamamen müteessirdi",
     "Kötü haberin ardından tamamen altüst olmuştu",
     "«müteessir» книжное; в списке «altüst olmuş»"),
    (17132, "example_tr",
     "Tüfeğin nişanından bakıyorum",
     "Tüfeğin nişangâhından bakıyorum",
     "«nişan» это помолвка; прицел — «nişangâh»"),
    (7072, "example_tr",
     "Polis hırsızı takip ediyor",
     "Polis hırsızın izini sürüyor",
     "«takip etmek» это следовать, а aufspüren — выследить"),
    (10458, "example_tr",
     "Durum umut verici değil",
     "Durum umutsuz görünüyor",
     "«не обнадёживает» слабее, чем hoffnungslos; и слова ряда не было"),
    (1886, "example_tr",
     "Bu özellikle senin için",
     "Bu özel olarak senin için",
     "«özellikle» это наречие «особенно», а нужно «speziell»"),
    (10472, "example_tr",
     "Öğretmen öğrencileri ödevlerini yapmaya zorluyor",
     "Öğretmen öğrencilere ödevlerini yapmaları için ısrar ediyor",
     "«zorlamak» это принуждать, а drängen — настаивать"),
    (15032, "example_uk",
     "Слухай, дружочок, це тебе не стосується",
     "Слухай, дружок, це тебе не стосується",
     "в списке «дружок», а не «дружочок»"),
    (15033, "example_uk",
     "Моя сусідка спекла мені торт",
     "Моя сусідка спекла мені пиріг",
     "Kuchen это пирог; «торт» это Torte, отдельный ряд"),
    (1425, "example_uk",
     "Полум'я палає помаранчевим кольором",
     "Полум'я мерехтить помаранчевим",
     "«палає» это горит, а flackert — мерцает"),
    (1425, "example_tr",
     "Alev turuncu renkte yanıyor",
     "Alev turuncu renkte titreşiyor",
     "то же: «yanıyor» это горит"),
    (16134, "example_uk",
     "Грабіж у банку був спектакулярним",
     "Грабіж у банку був вражаючим",
     "«спектакулярний» не українське слово"),
    (16134, "example_tr",
     "Bankanın soygunu spektakuler oldu",
     "Bankadaki soygun çok çarpıcıydı",
     "«bankanın soygunu» это ограбление, совершённое банком"),
    (7059, "example_uk",
     "Сирена голосно виє, коли вибухає пожежа",
     "Сирена голосно виє, коли починається пожежа",
     "пожар не «вибухає»"),
    (15500, "example_uk",
     "З гарячого горщика піднімалася пара",
     "З гарячої каструлі піднімалася пара",
     "«горщик» это цветочный горшок, а Topf здесь кастрюля"),
    (7071, "example_uk",
     "Дід іде зі своєю палицею",
     "Старий чоловік іде зі своєю палицею",
     "«дід» это дедушка, а der alte Mann — старик"),
    (10467, "example_uk",
     "Це була жахлива ніч у старому замку",
     "Це була зловісна ніч у старому замку",
     "«жахлива» это ужасная, а unheimlich — жуткая, зловещая"),
    (7064, "example_uk",
     "Вона була зовсім розстроєна поганою новиною",
     "Вона була зовсім засмучена після поганої новини",
     "«розстроєна» русизм, и падеж вместо «після»"),
    (18200, "example_uk",
     "Я купив нові завіси для мого вітального залу",
     "Я купив нові штори для своєї вітальні",
     "«вітальний зал» это приветственный зал; гостиная — «вітальня»"),
    (10457, "example_uk",
     "Мене охопила туга за домом",
     "Я тужу за своєю батьківщиною",
     "эталон «nach meiner Heimat», а не по дому"),
    (10457, "example_pl",
     "Czuję ogromną tęsknotę za domem",
     "Czuję tęsknotę za moją ojczyzną",
     "то же, и «ogromną» в эталоне нет"),
    (7073, "example_pl",
     "Nie powinieneś wtrącać się w jej sprawy",
     "Nie powinieneś wtrącać się w ich sprawy",
     "эталон «ihre Angelegenheiten» — их, а не её"),
    (15498, "example_pl",
     "Jedziemy w północny region",
     "Jedziemy do północnego regionu",
     "по-польски «jechać do», а не «w»"),
    (2082, "example_pl",
     "Mam wykład",
     "Wygłaszam wykład",
     "«mam» это у меня есть, а halten — выступать с докладом"),
    (12593, "example_pl",
     "Była blada, jakby się czegoś bała",
     "Wyglądała na bladą, jakby się bała",
     "эталон «sah blass aus» — выглядела; и «czegoś» в нём нет"),

    # ══ эталон и перевод: время, число, модальность ══════════════
    (17133, "example_ru",
     "Мы развернулись, потому что начался дождь",
     "Нам пришлось развернуться, потому что начался дождь",
     "потерян модальный: эталон «mussten umkehren»"),
    (17133, "example_uk",
     "Ми розвернулися, тому що почався дощ",
     "Нам довелося розвернутися, тому що почався дощ",
     "то же"),
    (8864, "example_uk",
     "Мені потрібне чорне чорнило для принтера",
     "Мені потрібне було чорне чорнило для принтера",
     "эталон «brauchte» в прошедшем; в ru, en и pl оно есть"),
    (8864, "example_tr",
     "Yazıcım için siyah mürekkep gerekli",
     "Yazıcım için siyah mürekkep gerekiyordu",
     "то же"),
    (8865, "example_uk",
     "Мій перукар завжди робить хорошу стрижку",
     "Мій перукар завжди робить гарні стрижки",
     "эталон «gute Haarschnitte» во множественном"),
    (14003, "example_tr",
     "Lütfen abartma, sadece küçük bir şey",
     "Lütfen abartma, sadece küçük bir şeydi",
     "потеряна связка: эталон «es war»"),
    (7088, "example_tr",
     "Hırsızlar eve zorla girdi",
     "Hırsızlar eve zorla girmeyi başardı",
     "потеряно «konnten»: в остальных четырёх оно есть"),

    # ══ часы цифрой и обрубленное сокращение ═════════════════════
    (14002, "example_en",
     "The press conference starts at 2 p.m",
     "The press conference starts at 2 o'clock",
     "«p.m» без второй точки — обрубок, озвучка прочитает неверно"),
    (2904, "example_en",
     "The broadcast starts at 8 pm",
     "The broadcast starts at 8 o'clock",
     "то же, и без точек вовсе"),
    (2904, "example_ru",
     "Трансляция начинается в 20:00",
     "Трансляция начинается в 20 часов",
     "двоеточие в часах озвучка не читает"),

    # ══ потерянное и добавленное слово ═══════════════════════════
    (17130, "example_tr",
     "Arabanın plakası geçerliliğini yitirdi",
     "Senin arabanın plakası geçerliliğini yitirdi",
     "потеряно «deines»: в остальных четырёх оно есть"),
    (12177, "example_uk",
     "Феєрверк на Новий Рік був дуже гарний",
     "Феєрверк у новорічну ніч був дуже гарний",
     "Silvester это новогодняя НОЧЬ, а не Новый год"),
    (10464, "example_pl",
     "Muszę jeszcze raz przemyśleć twoją propozycję",
     "Muszę jeszcze raz przemyśleć twoją propozycję, zanim powiem tak",
     "потеряно «bevor ich ja sage»"),
    (13663, "example_pl",
     "Miała na sobie elegancką sukienkę",
     "Miała na sobie elegancką sukienkę na imprezę",
     "потеряно «zur Party»"),
    (14004, "example_uk",
     "Це була буквально найкраща їжа, яку я коли-небудь їв",
     "Це було буквально найкраще, що я коли-небудь їв",
     "«їжа» в эталоне «das Beste» нет"),
    (7080, "example_tr",
     "Haberi duyduktan sonra çok mutlu göründüler",
     "Haberden dolayı çok mutlu göründüler",
     "«услышав новость» в эталоне нет: там «über die Nachricht»"),
    (16136, "example_pl",
     "Latem panują tu wysokie temperatury",
     "Latem panują wysokie temperatury",
     "«tu» в эталоне нет"),
    (12589, "example_ru",
     "После аварии у него было сильное кровотечение из раны на голове",
     "После аварии у него было сильное кровотечение из головы",
     "«из раны» в эталоне нет"),
    (11708, "example_pl",
     "Dziecko przełyka tabletkę, popijając wodą",
     "Dziecko przełyka tabletkę z wodą",
     "деепричастие вместо простого «mit Wasser»"),
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
