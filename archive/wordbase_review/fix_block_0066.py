"""
Правки блока 66 (ряды 11501–11700, ранги 23863–24280).

Находка блока — продолжение того, что началось в блоке 65:

    ряд  riegeln
    de   Er riegelte die Tür von innen ab

Заголовок — глагол без приставки, а пример показывает приставочный:
`abriegeln`. Блоком раньше то же было с `hecken`/`aushecken`. Под это
сделана примета `scan_de_verb_prefix`, и важно, чем она отличается от
`scan_de_headword_swap` из блока 64: у существительных подмена прилипает
хвостом и видна в самом слове, а у глаголов приставка ОТДЕЛЯЕТСЯ и
уезжает в конец фразы. Та примета такие ряды не видит в принципе.

По базе примета дала 29 рядов. Сломаны из них два, и оба нашлись вне
этого блока:

    2966  Ich versende das Paket heute ab      → `versenden` и
                                                 `absenden` сразу
    9945  Ich tilge meine Schulden langsam ab  → `ab` лишнее

Остальные 27 не сломаны: `Ich presse die Zitrone aus`, `Ich zünde eine
Kerze an` — фразы верные, но учат `auspressen` и `anzünden`, а ряды
названы `pressen` и `zünden`. Отдано владельцу отдельным списком.

Второй дефект блока, который стоит записать: в ряду `Heldentat` (11577)
польский перевод ПОТЕРЯЛ ОТРИЦАНИЕ.

    de  Das war wirklich keine Heldentat
    pl  To był prawdziwy bohaterski czyn

Немецкий говорит «это вовсе не подвиг», польский — «это был настоящий
подвиг». Смысл перевёрнут на противоположный, и ни по форме, ни по
согласию с другими переводами это не видно: en, uk и tr переводят
совсем другую фразу, а русский один держит отрицание.

    python -m app.scripts.fix_block_0066            # показать
    python -m app.scripts.fix_block_0066 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

FIXES: list[tuple[int, str, str, str, str]] = [
    # 11501 versetzen
    (8630, "example_uk", "Він завдає удар противнику",
     "Він завдає удару противнику",
     "«завдавати» требует родительного"),
    # 11504 einwerfen
    (8632, "example_uk", "Чи можу я коротко щось додати?",
     "Чи можу я коротко щось вставити?",
     "«додати» это добавить, а в статье «вставити зауваження»"),
    # 11505 Kontostand
    (9948, "example_uk", "Залишок коштів низький",
     "Залишок на рахунку низький",
     "потеряно слово ряда"),
    # 11506 Gemeinsamkeit
    (2511, "example_en", "We found some commonality in our views",
     "We have a lot in common",
     "перевод другого предложения"),
    # 11511 durchtrennen
    (8634, "example_uk", "Ніж перерізує мотузку легко",
     "Ніж легко перерізає мотузку",
     "«перерізує» — не та форма, и порядок слов"),
    # 11513 Rute
    (8635, "example_uk", "Рибалка забросив вудилище",
     "Рибалка закинув вудку",
     "«забросив» — русское слово, и в статье «вудка»"),
    # 11515 Gottseidank
    (11554, "example_uk", "Дякую Богу, травма не серйозна",
     "Слава Богу, травма несерйозна",
     "перевод слова первым значением"),
    (11554, "example_tr", "Allaha şükür, yaralanma ciddi değil",
     "Allah'a şükür, yaralanma ciddi değil",
     "потерян апостроф, в статье он есть"),
    (11554, "example_pl", "Dzięki Bogu nikomu nic się nie stało",
     "Dzięki Bogu obrażenia nie są poważne",
     "перевод другого предложения"),
    # 11517 bildlich
    (8637, "example_uk", "Це було образно кажучи, звичайно, неправда",
     "Це було, образно кажучи, звичайно, неправда",
     "вводный оборот не выделен запятой"),
    # 11518 Untier
    (8638, "example_uk", "У фільмі герой боровся з чудовиськом",
     "У фільмі герой боровся з жахливим чудовиськом",
     "потеряно «monströs»"),
    (8638, "example_pl", "W filmie bohater walczył z potwornym monstrum",
     "W filmie bohater walczył z potworną bestią",
     "«potworne monstrum» — одно и то же дважды"),
    # 11519 passiv
    (8639, "example_tr",
     "Onun projeye karşı pasif tutumu beni rahatsız etti",
     "Onun projeye karşı pasif tutumu hoşuma gitmedi",
     "в эталоне «gefiel mir nicht», а не «беспокоило»"),
    # 11520 verantwortungsvoll
    (11555, "example_pl", "To bardzo odpowiedzialna praca",
     "Jest bardzo odpowiedzialną osobą",
     "перевод другого предложения"),
    # 11521 ausbeuten
    (9271, "example_pl", "Szef wyzyskuje swoich pracowników",
     "Bogaty fabrykant chciał wyzyskiwać swoich robotników",
     "перевод другого предложения"),
    # 11522 zweitausend
    (13607, "example_uk", "Квиток коштував дві тисячі гривень",
     "Це було у двохтисячному році",
     "перевод другого предложения"),
    # 11524 Beisein
    (8640, "example_tr", "Törende hazır bulunmanız bizi çok mutlu eder",
     "Tanıkların huzurunda sözleşmeyi imzaladı",
     "перевод другого предложения"),
    # 11525 Stromnetz
    (17735, "example_tr",
     "Elektrik şebekesi kesintisi sırasında aşırı yüklendi",
     "Elektrik kesintisi sırasında şebeke aşırı yüklendi",
     "цепочка изафетов склеилась и подлежащее потерялось"),
    # 11526 Lösegeldforderung
    (16934, "example_uk", "Викрадачі висунули високу вимогу викупу",
     "Викрадачі висунули вимогу великого викупу",
     "«висока вимога» — не по-украински"),
    # 11527 rational
    (8641, "example_pl", "Musimy podjąć racjonalną decyzję",
     "Próbował znaleźć racjonalne wyjaśnienie",
     "перевод другого предложения"),
    # 11529 Brauerei
    (12015, "translation_tr", "bira fabrikası, birahane üretim tesisi",
     "bira fabrikası, bira üretim tesisi",
     "«birahane» это пивная, а не завод"),
    (12015, "example_pl", "W naszym mieście jest stary browar",
     "Stary browar wciąż produkował piwo tradycyjnymi metodami",
     "перевод другого предложения"),
    # 11530 fahnden
    (16935, "example_ru", "Этого человека разыскивает полиция",
     "Полиция разыскивала беглого преступника",
     "перевод другого предложения"),
    # 11531 Wutanfall
    (11556, "translation_uk", "напад гніву, вибух лютості, істерика",
     "напад гніву, вибух люті, істерика",
     "«лютості» — не та форма"),
    (11556, "example_uk",
     "Коли він почув новину, у нього була припадок гніву",
     "Коли він почув новину, у нього був напад гніву",
     "рассогласование рода, и в статье «напад»"),
    (11556, "example_pl",
     "Dziecko dostało napadu wściekłości w sklepie",
     "Dostał napadu wściekłości, kiedy usłyszał tę wiadomość",
     "перевод другого предложения"),
    # 11532 Zwirn
    (13776, "example_tr", "Düğmeyi güçlü iplikle dikiş attı",
     "Düğmeyi güçlü iplikle dikti",
     "«dikiş atmak» — не то выражение"),
    # 11533 Auflauf — лишний дефис в эталоне
    (12016, "example_de",
     "Zum Mittagessen kochte sie einen Kartoffel-Auflauf",
     "Zum Mittagessen kochte sie einen Kartoffelauflauf",
     "составное слово пишется слитно"),
    (12016, "example_uk",
     "На обід вона готувала картопляну запіканку",
     "На обід вона приготувала картопляну запіканку",
     "«kochte» это однократно"),
    (12016, "example_tr",
     "Öğle yemeği için patates fırında pişirilen yemeğini yaptı",
     "Öğle yemeği için patates gratini yaptı",
     "описание вместо слова, и лишний притяжательный"),
    # 11534 Pieper
    (17736, "example_en",
     "The beeper in my bag always beeped at the wrong time",
     "The beeper in my bag always beeps at the wrong time",
     "эталон в настоящем времени"),
    (17736, "example_ru",
     "Пищащий прибор в сумке звонит не в то время",
     "Пейджер в сумке всегда пищит не в то время",
     "перевод слова первым значением, и потеряно «immer»"),
    (17736, "example_uk",
     "Писклявий прилад у сумці завжди пищить не в той час",
     "Пейджер у сумці завжди пищить не в той час",
     "перевод слова первым значением"),
    (17736, "example_tr", "Doktorun çağrı cihazı yine çaldı",
     "Çantamdaki çağrı cihazı her zaman yanlış zamanda çalıyor",
     "перевод другого предложения"),
    # 11535 sitzend
    (8642, "example_uk", "У мене сидяча робота в офісі",
     "Сидячий спосіб життя не є здоровим",
     "перевод другого предложения"),
    # 11536 Dissertation
    (9633, "example_uk",
     "Після чотирьох років вона нарешті захистила свою дисертацію",
     "Після чотирьох років вона нарешті подала свою дисертацію",
     "«einreichen» это подати, а не захистити"),
    # 11537 Stammkunde
    (17889, "example_uk",
     "Постійні клієнти ресторану завжди мали перевагу",
     "Постійних клієнтів ресторану завжди обслуговували краще",
     "«bevorzugt behandelt» это обслуживали лучше"),
    (17889, "example_tr",
     "Restoranın daimi müşterileri her zaman tercih görmüştür",
     "Restoranın daimi müşterileri her zaman ayrıcalıklı muamele görürdü",
     "«tercih görmek» — не выражение"),
    # 11539 Sicherheitsteam
    (9272, "example_uk",
     "Команда безпеки перевіряла всіх гостей при вході",
     "Служба безпеки перевіряла всіх гостей на вході",
     "перевод слова первым значением, и «при вході» — калька"),
    # 11541 Wasserversorgung
    (18477, "example_uk",
     "У цьому регіоні водопостачання під час посухи повністю припинилась",
     "У цьому регіоні водопостачання під час посухи повністю припинилося",
     "рассогласование рода"),
    # 11542 Prestige
    (11557, "example_pl", "Ta praca daje duży prestiż",
     "Był gotów zaryzykować cały swój prestiż, by powiedzieć prawdę",
     "перевод другого предложения"),
    # 11543 Kaufmann
    (9273, "example_pl", "Kupcy sprzedawali towary na rynku",
     "Kupcy godzinami negocjowali warunki umowy handlowej",
     "перевод другого предложения"),
    # 11545 Delikatesse
    (12017, "example_uk",
     "Цей ікряний делікатес був неймовірно дорогим, але дуже смачний",
     "Цей ікряний делікатес був неймовірно дорогим, але дуже смачним",
     "рассогласование падежа во второй половине"),
    (12017, "example_tr",
     "Bu havyar lezzeti inanılmaz pahalı ama çok lezzetliydi",
     "Bu havyarlı lezzet inanılmaz pahalıydı ama çok lezzetliydi",
     "«havyar lezzeti» — перевёрнутый изафет, и время рассогласовано"),
    (12017, "example_pl", "Ten ser to prawdziwy przysmak",
     "Ten kawiorowy przysmak był niewiarygodnie drogi, ale bardzo smaczny",
     "перевод другого предложения"),
    # 11546 taktvoll
    (11558, "example_tr",
     "Onun hatalarından nazikçe bahsetti onu incitmeden",
     "Onu incitmeden hatalarından nazikçe bahsetti",
     "деепричастный оборот оторван в конец"),
    (11558, "example_pl", "Był bardzo taktowny i nikogo nie obraził",
     "Mówiła taktownie o jego błędach, nie obrażając go",
     "перевод другого предложения"),
    # 11547 Produzentin
    (9274, "example_pl", "Producentka filmu odebrała nagrodę",
     "Producentka filmu zdobyła trzy Oscary",
     "потеряно «drei Oscars»"),
    # 11548 Selbsthilfegruppe
    (13145, "example_uk",
     "Група взаємодопомоги зустрічалась кожного вівторка, щоб обговорити "
     "свої проблеми",
     "Група взаємодопомоги зустрічалася щовівторка, щоб обговорити "
     "свої проблеми",
     "«кожного вівторка» — калька"),
    # 11550 lehrreich — эталон заменили после перевода
    (9635, "example_en",
     "That was an instructive experience for everyone involved",
     "That was a very instructive experience for me",
     "перевод остался от прежнего эталона"),
    (9635, "example_uk",
     "Це був повчальний досвід для всіх залучених осіб",
     "Це був дуже повчальний досвід для мене",
     "перевод остался от прежнего эталона"),
    (9635, "example_tr",
     "Bu, tüm katılanlar için öğretici bir deneyimdi",
     "Bu benim için çok öğretici bir deneyimdi",
     "перевод остался от прежнего эталона"),
    # 11552 riegeln — заголовок без приставки, пример с приставкой
    (8643, "example_uk",
     "Він запер двері на засув зсередини перед сном",
     "Він замкнув двері на засув зсередини перед сном",
     "«запер» — русская форма"),
    (8643, "example_tr",
     "Uyumaya gitmeden önce kapıyı içeriden kilitledi",
     "Uyumaya gitmeden önce kapıyı içeriden sürgüledi",
     "«kilitlemek» это запереть на ключ, а в статье «sürgülemek»"),
    (8643, "example_pl", "Zarygluj drzwi, zanim pójdziesz spać",
     "Zaryglował drzwi od wewnątrz, zanim poszedł spać",
     "эталон не в повелительном, и потеряно «von innen»"),
    # 11554 Beschwörung
    (14821, "example_pl", "Wypowiedział dziwne zaklęcie nad ogniem",
     "Przywoływanie duchów było dawnym zwyczajem w wielu kulturach",
     "перевод другого предложения"),
    # 11555 zusammenpacken
    (17398, "example_pl", "Muszę spakować rzeczy przed wyjazdem",
     "Przed wyjazdem musimy spakować wszystkie rzeczy",
     "в эталоне «wir», и потеряно «alle»"),
    # 11556 bewerkstelligen
    (8645, "example_pl", "Nie wiem jak udało mu się tego dokonać",
     "Trudno dokonać tak skomplikowanego zadania",
     "перевод другого предложения"),
    # 11557 auftauen
    (12018, "example_tr",
     "Eti pişirmeden önce et en az 24 saat çözdürülmelidir",
     "Et, pişirmeden önce en az 24 saat çözdürülmelidir",
     "«eti … et» — подлежащее названо дважды"),
    (12018, "example_pl", "Musisz rozmrozić mięso przed obiadem",
     "Mięso musi się rozmrażać co najmniej 24 godziny, zanim je ugotujesz",
     "перевод другого предложения"),
    # 11558 Parkuhr
    (17399, "translation_uk", "паркомат, парковочний счетчик",
     "паркомат, парковий лічильник",
     "«счетчик» — русское слово"),
    (17399, "example_ru",
     "Мне нужно внести деньги в паркомат перед кафе",
     "Мне нужно внести деньги в паркомат, прежде чем идти в кафе",
     "«перед кафе» значит «рядом с кафе»"),
    (17399, "example_uk",
     "Мені потрібно кинути монету в паркомат перед кав'ярнею",
     "Мені потрібно кинути монету в паркомат, перш ніж іти до кав'ярні",
     "«перед кав'ярнею» значит «рядом с кафе»"),
    (17399, "example_pl", "Wrzuć monetę do parkometru",
     "Muszę wrzucić monetę do parkometru, zanim pójdę do kawiarni",
     "перевод другого предложения"),
    # 11559 produktiv
    (9275, "example_pl", "Dzisiaj byłem bardzo produktywny w pracy",
     "Dzisiaj byłem bardzo produktywny i wiele zrobiłem",
     "«w pracy» в эталоне нет, зато потеряно «viel geschafft»"),
    # 11560 zuhalten
    (8646, "example_en", "Close the door, there's a draft",
     "Hold the door shut, there's a draft",
     "«close» теряет слово ряда — держать закрытым"),
    (8646, "example_uk", "Закрий двері, тягне від вікна",
     "Тримай двері закритими, тягне",
     "«закрий» теряет слово ряда, и «від вікна» в эталоне нет"),
    (8646, "example_tr", "Kapıyı kapat, rüzgâr geliyor",
     "Kapıyı kapalı tut, cereyan var",
     "«kapat» теряет слово ряда"),
    (8646, "example_pl", "Zatkał nos, bo strasznie śmierdziało",
     "Trzymaj drzwi zamknięte, bo ciągnie",
     "перевод совсем другого предложения"),
    # 11561 unpässlich
    (13146, "example_uk", "Мені сьогодні щось нездоровиться",
     "Мені сьогодні нездоровиться, здається, я не зовсім у формі",
     "потеряна вторая половина"),
    (13146, "example_tr",
     "Bugün kendimi rahatsız hissediyorum, sanırım grip oldum",
     "Bugün kendimi rahatsız hissediyorum, sanırım tam formda değilim",
     "«grip oldum» это «подхватил грипп», чего в эталоне нет"),
    (13146, "example_pl", "Dzisiaj jestem trochę niedysponowana",
     "Dzisiaj jestem niedysponowany, chyba nie jestem w pełni formy",
     "потеряна вторая половина"),
    # 11564 bezwecken
    (8647, "example_en",
     "With this measure we aim at better efficiency",
     "With this we aim at better efficiency",
     "«measure» в эталоне нет"),
    (8647, "example_uk",
     "Цією мірою ми переслідуємо мету підвищення ефективності",
     "Цим ми маємо на меті кращу ефективність",
     "«мірою» — не то слово, и оборот раздут"),
    (8647, "example_tr",
     "Bu ölçüyle daha iyi verimliliği amaçlıyoruz",
     "Bununla daha iyi bir verimlilik amaçlıyoruz",
     "«ölçü» это мера измерения"),
    (8647, "example_pl", "Co ty właściwie masz na celu",
     "Tym mamy na celu lepszą efektywność",
     "перевод другого предложения, да ещё и вопрос без знака"),
    # 11566 Halbinsel
    (15867, "example_tr", "İtalya, Akdenizdeki ünlü bir yarımadadır",
     "İtalya, Akdeniz'deki ünlü bir yarımadadır",
     "потерян апостроф в названии"),
    # 11567 hypnotisieren
    (13147, "example_pl", "Magik potrafi hipnotyzować ludzi na scenie",
     "Hipnotyzer potrafi hipnotyzować ludzi",
     "перевод другого предложения"),
    # 11568 Gesandte
    (16936, "example_ru", "Послы двух стран встретились на переговоры",
     "Посланники двух стран встретились на переговорах",
     "перевод слова первым значением, и не тот падеж"),
    (16936, "example_uk", "Емісари двох країн зустрілися на переговорах",
     "Посланці двох країн зустрілися на переговорах",
     "перевод слова первым значением"),
    (16936, "example_tr", "İki ülkenin elçileri müzakerelere katıldı",
     "İki ülkenin elçileri müzakereler için buluştu",
     "«katıldı» это участвовали, а в эталоне встретились"),
    # 11569 Müllabfuhr
    (18479, "example_uk", "Вивіз сміття відбувається по понеділках",
     "Вивіз сміття відбувається щопонеділка",
     "«по понеділках» — калька"),
    # 11570 Armenhaus
    (16937, "example_tr", "Yaşlı adam düşkünler evinde kalıyor",
     "19. yüzyılda düşkünler evleri yoksullar için sığınaktı",
     "перевод другого предложения"),
    # 11571 Konservatorium
    (9636, "example_uk", "Вона навчається піаніно в консерваторії",
     "Вона вчиться грати на фортепіано в консерваторії",
     "«навчатися піаніно» — не то управление"),
    (9636, "example_tr", "Konservatuarda piyano öğreniyor",
     "Konservatuvarda piyano öğreniyor",
     "в статье «konservatuvar»"),
    # 11573 tagaus
    (18942, "example_tr", "Gün gün bahçede çalışıyor",
     "Her gün bahçede çalışıyor",
     "«gün gün» — не выражение"),
    # 11574 Eiszeit
    (15868, "example_tr",
     "Buzul çağında Dünyanın büyük kısımları buzla kaplıydı",
     "Buzul çağında Dünya'nın büyük kısımları buzla kaplıydı",
     "потерян апостроф в названии"),
    # 11576 Raststätte
    (17400, "example_ru",
     "На автостраде мы остановились на зоне отдыха",
     "На автостраде мы остановились в зоне отдыха",
     "«на зоне» — не то управление"),
    (17400, "example_uk",
     "На автостраді ми зупинились на зоні відпочинку",
     "На автостраді ми зупинилися в зоні відпочинку",
     "«на зоні» — не то управление"),
    # 11577 abraten — эталон заменили после перевода
    (14321, "example_en",
     "The doctor advised me against lifting heavy loads",
     "I can only advise you against it",
     "перевод остался от прежнего эталона"),
    (14321, "example_uk", "Лікар порадив відмовитись від солодкого",
     "Від цього я можу тільки тебе відраджувати",
     "перевод остался от прежнего эталона"),
    (14321, "example_tr",
     "Doktor bana ağır yükleri kaldırmamaktan caydırdı",
     "Bundan seni ancak caydırabilirim",
     "перевод остался от прежнего эталона"),
    # 11578 tugendhaft
    (11559, "example_uk", "Він веде чесне життя",
     "Він веде добродійне життя",
     "перевод слова первым значением"),
    (11559, "example_pl", "Prowadzi cnotliwe i spokojne życie",
     "Prowadzi cnotliwe życie",
     "«i spokojne» в эталоне нет"),
    # 11579 Clip — эталон заменили после перевода
    (17737, "example_en",
     "The video clip shows breathtaking footage",
     "Take a look at this clip!",
     "перевод остался от прежнего эталона"),
    (17737, "example_ru", "Видеоклип показывает захватывающие кадры",
     "Посмотри-ка на этот клип!",
     "перевод остался от прежнего эталона"),
    (17737, "example_uk", "Відеокліп показує захопливі кадри",
     "Подивись на цей кліп!",
     "перевод остался от прежнего эталона"),
    (17737, "example_tr",
     "Müzik klibı nefes kesici görüntüler gösteriyor",
     "Şu klibe bir bak!",
     "перевод остался от прежнего эталона, и «klibı» — не та форма"),
    # 11580 Lyrik
    (14823, "example_tr", "Bu şairin lirikliği çok duygusal",
     "Bu şairin lirik şiiri çok duygusal",
     "«liriklik» — нет такого слова"),
    # 11583 Bazillus
    (13148, "example_ru", "Бациллы в старой воде заразили бы нас всех",
     "Бациллы в старой воде сделали бы нас всех больными",
     "«hätten krank gemacht» это сделали бы больными"),
    (13148, "example_pl", "Umyj ręce żeby nie roznosić zarazków",
     "Zarazki w tej starej wodzie mogłyby nas wszystkich rozchorować",
     "перевод другого предложения"),
    # 11584 Auftragsmörder
    (16938, "example_ru", "Убийцу на заказ наконец поймала полиция",
     "Наёмного убийцу наконец поймала полиция",
     "перевод слова первым значением"),
    (16938, "example_tr", "Kira katil sonunda polis tarafından yakalandı",
     "Kiralık katil sonunda polis tarafından yakalandı",
     "«kira katil» — разваленное выражение"),
    # 11585 Kartoffelsalat
    (12019, "example_tr",
     "Patates salatası bugün çok lezzetli, çok mayonez ile hazırlanmış",
     "Patates salatası bugün bol mayonezle özellikle lezzetli",
     "«çok … çok» дважды, и «besonders» потеряно"),
    (12019, "example_pl", "Na grilla zrobię sałatkę ziemniaczaną",
     "Sałatka ziemniaczana jest dziś szczególnie dobra, z dużą ilością "
     "majonezu",
     "перевод другого предложения"),
    # 11586 unerkannt — падеж в эталоне
    (8648, "example_de",
     "Er verließ unerkannt die Stadt, damit ihn niemand folgen konnte",
     "Er verließ unerkannt die Stadt, damit ihm niemand folgen konnte",
     "«folgen» требует датива"),
    (8648, "example_tr",
     "Kimse onu takip edemeyecek şekilde şehri tanınmamış olarak terk etti",
     "Kimse onu takip edemesin diye şehri tanınmadan terk etti",
     "оборот раздут до неузнаваемости"),
    (8648, "example_pl",
     "Wyszedł z budynku nierozpoznany przez nikogo",
     "Opuścił miasto nierozpoznany, żeby nikt nie mógł go śledzić",
     "перевод другого предложения"),
    # 11587 befreiend
    (11560, "example_tr",
     "Sonunda gerçeği söylemek çok özgürleştiriciydi",
     "Sonunda gerçeği söylemek ve artık yalan söylememek çok "
     "özgürleştiriciydi",
     "потеряно «nicht mehr zu lügen»"),
    (11560, "example_pl", "To było wyzwalające uczucie",
     "To było wyzwalające, w końcu powiedzieć prawdę i przestać kłamać",
     "перевод другого предложения"),
    # 11589 Kriegsgefangener — сильное окончание в эталоне
    (16940, "example_de",
     "Der Kriegsgefangener wurde schließlich nach Hause entlassen",
     "Der Kriegsgefangene wurde schließlich nach Hause entlassen",
     "прилагательное-существительное после «der» берёт слабое окончание"),
    (16940, "example_pl", "Jeniec wojenny w końcu wrócił do domu",
     "Jeniec wojenny został w końcu zwolniony i odesłany do domu",
     "«wrócił» вместо «entlassen» — отпустили, а не вернулся сам"),
    # 11590 Schulbehörde
    (9637, "example_uk",
     "Шкільна адміністрація прийняла нові правила для всіх шкіл",
     "Управління освіти ухвалило нові правила для всіх шкіл",
     "перевод слова первым значением"),
    (9637, "example_tr",
     "Okul otoritesi tüm okullar için yeni kurallar koydu",
     "Eğitim müdürlüğü tüm okullar için yeni kurallar koydu",
     "«okul otoritesi» — калька, в статье «eğitim müdürlüğü»"),
    # 11591 Kuli
    (9276, "example_uk", "Кулі носили важкі вантажі на ринку",
     "Кулі носив важкі вантажі на ринку",
     "в эталоне один человек"),
    (9276, "example_pl", "Pożycz mi długopis na chwilę",
     "Kulis nosił ciężkie ładunki na rynku",
     "перевод другого предложения"),
    # 11592 Bedienstete
    (9277, "example_uk",
     "Служачі готелю були дуже ввічливі та привітні",
     "Службовці готелю були дуже ввічливі та привітні",
     "«служачі» — нет такой формы"),
    (9277, "example_pl", "Pracownicy hotelu byli bardzo uprzejmi",
     "Pracownicy hotelu byli bardzo uprzejmi i pomocni",
     "потеряно «hilfsbereit»"),
    # 11594 veranlagt
    (11561, "example_tr",
     "Sanatsal yetenekle donanmış ve resim yapmayı seviyor",
     "Sanata yatkın ve resim yapmayı seviyor",
     "«yetenekle donanmış» — раздутый оборот"),
    # 11598 Krankenpfleger
    (13149, "example_tr", "Hemşire hastaları sevgiyle düşündü",
     "Erkek hemşire hastalarla sevgiyle ilgilendi",
     "«düşünmek» это думать, и потерян мужской род"),
    (13149, "example_pl", "Pielęgniarz zmierzył mi ciśnienie",
     "Pielęgniarz troskliwie opiekował się pacjentami",
     "перевод другого предложения"),
    # 11599 Albino
    (13150, "example_pl", "Ten biały królik to albinos",
     "Albinos miał białą skórę i czerwone oczy",
     "перевод другого предложения"),
    # 11600 kraus
    (8649, "example_uk",
     "Її кучеряві волосся було важко розчісувати",
     "Її кучеряве волосся було важко розчісувати",
     "«волосся» среднего рода и единственного числа"),
    (8649, "example_tr", "Kıvırcık saçını taraması zordu",
     "Kıvırcık saçlarını taramak zordu",
     "лишний притяжательный у отглагольного"),
    (8649, "example_pl", "Ona ma gęste kręcone włosy",
     "Jej kręcone włosy były trudne do rozczesania",
     "перевод другого предложения"),
    # 11602 Nimmerwiedersehen
    (11563, "example_en", "Farewell, I'll miss you",
     "Goodbye forever, I'll miss you",
     "потеряно «Nimmer-»"),
    (11563, "example_uk", "До побачення, буду тебе сумувати",
     "Прощавай назавжди, я буду за тобою сумувати",
     "«буду тебе сумувати» — сломанное управление"),
    (11563, "example_pl", "To było nasze pożegnanie na zawsze",
     "Pożegnanie na zawsze, będę za tobą tęsknić",
     "перевод другого предложения"),
    # 11603 zerdrückt
    (8650, "example_pl", "Ten pomidor jest całkiem zgnieciony",
     "Kwiat był zgnieciony i stracił swój kształt",
     "перевод другого предложения"),
    # 11604 einschleusen
    (16941, "example_ru", "Они провели шпиона в страну контрабандой",
     "Они тайно ввели шпиона в страну так, что никто этого не заметил",
     "потеряно «ohne dass jemand es bemerkte»"),
    (16941, "example_uk", "Вони провели шпигуна до країни контрабандою",
     "Вони таємно ввели шпигуна до країни так, що ніхто цього не помітив",
     "потеряно «ohne dass jemand es bemerkte»"),
    # 11606 verbarrikadieren
    (16942, "example_uk", "Вони забарикадувалися в будинку",
     "Вони забарикадувалися в будинку й викликали поліцію",
     "потеряна вторая половина"),
    (16942, "example_tr", "Göstericiler sokakta barikat kurdu",
     "Evde kendilerini barikatladılar ve polisi aradılar",
     "перевод другого предложения"),
    # 11607 Armada
    (16943, "example_tr", "İspanyol gemi armadası efsaneleşti",
     "İspanyol gemi armadası efsaneviydi",
     "«efsaneleşti» значит «стала легендой», а в эталоне «была»"),
    # 11611 Areal
    (8651, "example_pl", "Cały teren jest ogrodzony płotem",
     "Teren był duży i dobrze utrzymany",
     "перевод другого предложения"),
    # 11612 republikanisch
    (16947, "example_tr",
     "Cumhuriyet yanlısı idealler devrim sırasında yayıldı",
     "Cumhuriyetçi idealler devrim sırasında yayıldı",
     "в статье «cumhuriyetçi»"),
    # 11613 Blutkreislauf
    (13151, "example_pl", "Spacer poprawia krążenie krwi",
     "Krążenie krwi transportuje tlen po całym ciele",
     "перевод другого предложения"),
    # 11614 frontal
    (8652, "example_tr", "Doğrudan saldırı şaşırtıcı ve etkili oldu",
     "Cepheden saldırı şaşırtıcı ve etkiliydi",
     "«doğrudan» это прямой, а в статье «cepheden»"),
    (8652, "example_pl",
     "Doszło do czołowego zderzenia dwóch samochodów",
     "Czołowy atak był zaskakujący i skuteczny",
     "перевод другого предложения"),
    # 11616 Sondermeldung — чисто
    # 11619 blinken
    (8653, "example_uk", "Неонова вивіска мерцає вночі",
     "Неонова вивіска мерехтить уночі",
     "«мерцає» — русская форма"),
    (8653, "example_pl", "Lampka na routerze cały czas miga",
     "Neonowy szyld miga nocą",
     "перевод другого предложения"),
    # 11621 umsichtig
    (11564, "example_pl",
     "Był rozważny i nie podejmował pochopnych decyzji",
     "Działał rozważnie i długo się zastanawiał",
     "перевод другого предложения"),
    # 11622 unvergleichlich
    (8654, "example_uk", "Концерт був неповторно гарним",
     "Концерт був незрівнянно гарний",
     "перевод слова первым значением"),
    (8654, "example_pl", "Ten widok jest po prostu niezrównany",
     "Koncert był nieporównywalnie piękny",
     "перевод другого предложения"),
    # 11624 Elan
    (11565, "example_pl", "Zabrał się do pracy z wielkim zapałem",
     "Pracuje nad projektem z wielkim zapałem",
     "перевод другого предложения"),
    # 11625 unbewohnt
    (18480, "example_uk", "Дім необитаємий і повільно руйнується",
     "Будинок нежилий і повільно руйнується",
     "«необитаємий» — нет такой формы"),
    # 11626 bürgerlich
    (16948, "example_tr", "Tipik bir burjuva ailesinden geliyor",
     "Burjuva bir aileden geliyor",
     "«tipik» в эталоне нет"),
    # 11627 rätselhafte
    (8655, "example_uk", "Його загадкова посмішка мене збивала",
     "Його загадкова посмішка мене збивала з пантелику",
     "«збивала» без дополнения повисает"),
    (8655, "example_pl", "Jego zagadkowy uśmiech mnie zaniepokoił",
     "Jego zagadkowy uśmiech mnie zmieszał",
     "«zaniepokoił» это встревожил, а `verwirrte` — сбил с толку"),
    # 11630 Dämpfer
    (17402, "example_en", "The silencer on the exhaust reduces noise",
     "The news was a real blow",
     "перевод взял другое значение слова и построил свою фразу"),
    (17402, "example_ru", "Глушитель на выхлопе снижает шум",
     "Эта новость была настоящим ударом",
     "перевод взял другое значение слова и построил свою фразу"),
    (17402, "example_uk", "Глушник на виході зменшує шум",
     "Ця новина була справжнім ударом",
     "перевод взял другое значение слова и построил свою фразу"),
    # 11632 Nische
    (18481, "example_en", "We have a small niche in the wall for shelves",
     "I have a small niche in the wall for shelves",
     "в эталоне «ich», а не «мы»"),
    (18481, "example_ru", "У нас в стене есть маленькая ниша для полок",
     "У меня в стене есть маленькая ниша для полок",
     "в эталоне «ich», а не «мы»"),
    (18481, "example_uk", "У нас у стіні є маленька ніша для полиць",
     "У мене в стіні є маленька ніша для полиць",
     "в эталоне «ich», а не «ми»"),
    (18481, "example_tr", "Duvarımızda raflar için küçük bir niş var",
     "Duvarımda raflar için küçük bir niş var",
     "в эталоне «ich», а не «мы»"),
    # 11633 Plankton
    (15870, "example_ru",
     "Планктон является основой пищевой цепи в море",
     "Планктон — основа пищевой цепи в море",
     "«является» — канцелярит"),
    (15870, "example_uk",
     "Планктон є основою харчового ланцюга в морі",
     "Планктон — основа харчового ланцюга в морі",
     "лишняя связка"),
    # 11635 Modus — чисто
    # 11636 einräumen
    (11567, "example_pl", "Muszę przyznać że się pomyliłem",
     "Muszę przyznać, że się pomyliłem",
     "нет запятой перед «że»"),
    # 11637 Bohnenstange
    (15329, "example_en",
     "My sons turned into a real beanpole since he started growing so tall",
     "My son turned into a real beanpole since he started growing so fast",
     "потерян апостроф, и «tall» вместо «schnell»"),
    (15329, "example_ru", "Мой сын стал совсем высоким и худым",
     "Мой сын стал настоящей каланчой, с тех пор как так быстро растёт",
     "потеряно слово ряда и вторая половина"),
    (15329, "example_uk",
     "Мій син став схожим на палицю, як він виріс у висоту",
     "Мій син став справжньою каланчею, відколи так швидко росте",
     "перевод слова описанием, и вторая половина сломана"),
    (15329, "example_tr",
     "Oğlum bir fasulye sapı gibi uzun ve zayıf oldu",
     "Oğlum bu kadar hızlı büyüdüğünden beri tam bir sırık oldu",
     "потеряно «seit er so schnell wächst»"),
    # 11639 Greis
    (15330, "example_de",
     "Der alte Greis saß jeden Tag auf der Bank im Berliner Park",
     "Der Greis saß jeden Tag auf der Bank im Berliner Park",
     "«alte Greis» — одно и то же дважды"),
    (15330, "example_ru",
     "Старец сидел каждый день на скамейке в парке",
     "Старец сидел каждый день на скамейке в берлинском парке",
     "потеряно «Berliner»"),
    (15330, "example_uk", "Старець сидів щодня на лавці в парку",
     "Старець сидів щодня на лавці в берлінському парку",
     "потеряно «Berliner»"),
    (15330, "example_tr",
     "Yaşlı adam her gün parkta bankta oturuyordu",
     "Yaşlı adam her gün Berlin'deki parkta bir bankta oturuyordu",
     "потеряно «Berliner»"),
    (15330, "example_pl",
     "Stary starzec siedział codziennie na ławce w berlińskim parku",
     "Starzec siedział codziennie na ławce w berlińskim parku",
     "«stary starzec» — одно и то же дважды"),
    # 11640 Anarchist
    (16950, "example_ru", "Анархист громко протестовал против правительства",
     "Анархисты громко протестовали против правительства",
     "в эталоне множественное число"),
    (16950, "example_uk", "Анархіст голосно протестував проти уряду",
     "Анархісти голосно протестували проти уряду",
     "в эталоне множественное число"),
    (16950, "example_tr",
     "Anarşist hükümet aleyhine sesli protesto yaptı",
     "Anarşistler hükümete karşı yüksek sesle protesto yaptı",
     "в эталоне множественное, и «aleyhine sesli» — калька"),
    # 11641 Treibsand
    (15871, "example_tr", "Gezgin batakçıl kuma saplanıp çıkamadı",
     "Gezgin bataklık kumuna saplandı ve çıkamadı",
     "«batakçıl» — нет такого слова"),
    # 11642 wunderhübsch
    (11568, "example_tr", "Yeni saç stilin harika güzel görünüyor",
     "Yeni saç modelin gerçekten harika görünüyor",
     "«harika güzel» — два усилителя подряд"),
    (11568, "example_pl", "Masz prześliczną nową fryzurę",
     "Twoja nowa fryzura wygląda naprawdę prześlicznie",
     "перевод другого предложения"),
    # 11643 mangeln
    (8658, "example_tr", "Bana cesaret değil, zaman eksik",
     "Bende cesaret değil, zaman eksik",
     "«bana» — не то управление"),
    (8658, "example_pl", "Brakuje mi czasu na wszystko",
     "Brakuje mi nie odwagi, a czasu",
     "перевод другого предложения"),
    # 11644 Ehrenmedaille
    (16951, "example_ru", "Боец получил медаль за отвагу",
     "Солдат получил медаль почёта за свою отвагу",
     "потеряно слово ряда"),
    (16951, "example_uk", "Йому вручили медаль пошани",
     "Солдат отримав медаль пошани за свою відвагу",
     "перевод другого предложения"),
    # 11645 Abruf
    (17741, "example_ru", "Данные доступны к вызову в любое время",
     "Данные доступны по запросу в любое время",
     "«доступны к вызову» — не по-русски"),
    (17741, "example_uk", "Дані доступні до запиту в будь-який час",
     "Дані доступні на запит у будь-який час",
     "не то управление"),
    (17741, "example_tr", "Veriler istediği zaman çağrıya hazır",
     "Veriler her zaman erişime hazır",
     "«istediği zaman» без подлежащего повисает"),
    # 11646 Wangenknochen
    (15331, "example_uk", "У неї були високі, видатні скули",
     "У неї були високі, виразні вилиці",
     "«видатні» значит выдающиеся по заслугам, и в статье «вилиця»"),
    # 11647 Fahrlässigkeit
    (16952, "example_uk", "Його необережність привела до аварії",
     "Його недбалість призвела до аварії",
     "«привела до» — калька, и перевод слова первым значением"),
    # 11648 Seelenfrieden
    (11569, "example_tr", "Doğada ruh sağlığı aradı",
     "Doğada iç huzur aradı",
     "«ruh sağlığı» это психическое здоровье"),
    (11569, "example_pl", "W lesie odzyskuję spokój ducha",
     "Szukała spokoju ducha w naturze",
     "перевод другого предложения"),
    # 11649 Schnorrer
    (11570, "example_uk", "Він паразит і позичає гроші у всіх",
     "Він дармоїд і позичає гроші у всіх",
     "«паразит» в статье нет"),
    (11570, "example_tr",
     "Herkesin parasını ödünç alan bir dilenci",
     "O bir beleşçi ve herkesten borç para alıyor",
     "фраза без подлежащего и сказуемого"),
    (11570, "example_pl", "Ten naciągacz znowu prosi o pieniądze",
     "To naciągacz i od wszystkich pożycza pieniądze",
     "перевод другого предложения"),
    # 11650 Handicap
    (13153, "example_pl",
     "Jego niepełnosprawność nie przeszkodziła mu w karierze",
     "Jego niepełnosprawność nie przeszkodziła mu osiągnąć celu",
     "«w karierze» вместо «sein Ziel zu erreichen»"),
    # 11652 Faszination
    (11571, "example_uk", "Захоплення древніми культурами вічне",
     "Захоплення давніми культурами вічне",
     "«древній» — русизм"),
    (11571, "example_tr", "Eski kültürlerin büyülemesi zamansızdır",
     "Eski kültürlere duyulan hayranlık zamansızdır",
     "«büyüleme» это действие, а нужно чувство"),
    (11571, "example_pl", "Mam wielką fascynację dawnymi kulturami",
     "Fascynacja dawnymi kulturami jest ponadczasowa",
     "перевод другого предложения"),
    # 11653 adlig
    (16954, "example_tr", "Soylu bir ailenden geliyordu",
     "Soylu bir aileden geliyordu",
     "«ailenden» — лишняя согласная"),
    # 11655 stinkig
    (11572, "example_en", "The fish smelled terrible",
     "Your fish smells far too stinky to me",
     "перевод другого предложения"),
    (11572, "example_uk", "Риба страшенно смерділа",
     "Твоя риба для мене занадто смердюча",
     "перевод другого предложения"),
    (11572, "example_pl", "Wyrzuć te śmierdzące skarpetki",
     "Twoja ryba zbyt mi śmierdzi",
     "перевод совсем другого предложения"),
    # 11657 Extremist
    (16955, "example_tr",
     "Aşırıcılar radikal değişiklikleri talep ettiler",
     "Aşırılıkçılar radikal değişiklikler talep etti",
     "«aşırıcı» — не та форма, и лишний аккузатив"),
    # 11658 violett
    (8660, "example_pl", "Kupiła fioletową sukienkę na imprezę",
     "Włożyła fioletową sukienkę na imprezę",
     "«kupiła» вместо «trug»"),
    # 11659 unüberlegt
    (11573, "example_uk",
     "Це було необмислене рішення з твоєї сторони",
     "Це було необдумане рішення з твого боку",
     "«необмислений» — нет такой формы, и «з твоєї сторони» — калька"),
    (11573, "example_tr",
     "Senin tarafından düşüncesiz bir karar almıştın",
     "Bu, senin verdiğin düşüncesiz bir karardı",
     "«senin tarafından … almıştın» — двойное подлежащее"),
    # 11661 Delegierte
    (16956, "example_tr", "Delegeler çeşitli ülkelerden gelmişlerdir",
     "Delegeler çeşitli ülkelerden geldi",
     "«gelmişlerdir» — пересказ с чужих слов"),
    # 11662 Teelöffel
    (12020, "example_pl", "Dodaj łyżeczkę cukru do herbaty",
     "Potrzebuję łyżeczki do herbaty",
     "перевод другого предложения"),
    # 11664 Rechtschreibung
    (9638, "example_tr", "Mektuptaki imla hatalarını düzeltmen lazım",
     "İmlam her zaman mükemmel değil",
     "перевод другого предложения"),
    # 11665 vergänglich
    (18944, "example_uk", "Молодість швидкоплинна, цінуй її",
     "Красота недовговічна й швидкоплинна",
     "перевод другого предложения"),
    # 11666 urplötzlich
    (18945, "example_uk", "Раптово в темряві зявилася постать",
     "Раптово в темряві з'явилася постать",
     "потерян апостроф"),
    # 11668 vorweisen
    (8661, "example_tr", "Aday etkileyici başarıları gösterebilir",
     "Aday etkileyici başarılar gösterebildi",
     "эталон в прошедшем, и лишний аккузатив"),
    (8661, "example_pl", "Musisz okazać bilet przy wejściu",
     "Kandydat mógł wykazać się imponującymi osiągnięciami",
     "перевод другого предложения"),
    # 11670 Peinlichkeit
    (11575, "example_en", "The situation was simply embarrassing to me",
     "I'll never forget this embarrassment",
     "перевод другого предложения"),
    # 11671 Kralle
    (15872, "example_en", "The eagle attacked with its claws",
     "The eagle seized the prey with its claws",
     "потеряно «die Beute»"),
    (15872, "example_tr", "Kartal pençeleriyle saldırdı",
     "Kartal avı pençeleriyle yakaladı",
     "потеряно «die Beute»"),
    # 11674 Bruchlandung
    (17403, "example_uk",
     "Літак здійснив аварійне приземлення в поле",
     "Літак здійснив аварійну посадку на полі",
     "в статье «посадка», и не тот падеж"),
    (17403, "example_tr", "Uçak sahada zorunlu iniş yaptı",
     "Uçak tarlada zorunlu iniş yaptı",
     "«saha» это спортивное поле"),
    # 11675 Staatsbürgerschaft
    (16958, "example_pl", "W zeszłym roku dostał polskie obywatelstwo",
     "Złożył wniosek o niemieckie obywatelstwo",
     "перевод другого предложения"),
    # 11677 Trainerin
    (12407, "translation_pl", "trenerka, trenerka drużyny",
     "trenerka, kobieta trener",
     "одно и то же слово дважды"),
    # 11678 nörgeln
    (11576, "example_uk", "Він постійно на все скаржиться",
     "Він постійно до всього придирається",
     "перевод слова третьим значением"),
    (11576, "example_tr", "Hep her şeyden şikayet ediyor",
     "Sürekli her şeye söyleniyor",
     "в статье «söylenmek», а «şikayet etmek» это жаловаться"),
    (11576, "example_pl", "Dziadek ciągle zrzędzi na pogodę",
     "Ciągle na wszystko zrzędzi",
     "перевод другого предложения"),
    # 11679 Heldentat — польский потерял отрицание
    (11577, "example_en", "His heroic deed will never be forgotten",
     "That was really no heroic deed",
     "перевод остался от прежнего эталона"),
    (11577, "example_uk", "Його подвиг ніколи не забудуть",
     "Це був зовсім не подвиг",
     "перевод остался от прежнего эталона"),
    (11577, "example_tr", "Onun kahramanca işi asla unutulmayacak",
     "Bu gerçekten bir kahramanlık değildi",
     "перевод остался от прежнего эталона"),
    (11577, "example_pl", "To był prawdziwy bohaterski czyn",
     "To naprawdę nie był bohaterski czyn",
     "перевод потерял отрицание и сказал обратное эталону"),
    # 11680 Sicherheitskraft
    (16959, "example_ru", "Силы безопасности взяли город под контроль",
     "Силы безопасности взяли контроль в свои руки",
     "«город» в эталоне нет"),
    (16959, "example_uk", "Сили безпеки узяли місто під контроль",
     "Сили безпеки взяли контроль у свої руки",
     "«місто» в эталоне нет"),
    (16959, "example_tr", "Güvenlik güçleri kontrol aldı",
     "Güvenlik güçleri kontrolü ele aldı",
     "«kontrol almak» — не выражение"),
    (16959, "example_pl", "Siły bezpieczeństwa otoczyły cały budynek",
     "Siły bezpieczeństwa przejęły kontrolę",
     "перевод другого предложения"),
    # 11681 Baseballspieler
    (12408, "example_tr", "Beyzbol oyuncusu bir sayı attı",
     "Beyzbol oyuncusu bir home run yaptı",
     "потеряно «Home Run»"),
    # 11682 Einsatzleiter
    (9278, "example_pl", "Dowódca akcji kierował ratowaniem ludzi",
     "Dowódca akcji koordynował akcję ratunkową",
     "«kierował ratowaniem ludzi» — пересказ вместо перевода"),
    # 11683 eingehend
    (8663, "example_pl", "Potrzebne było szczegółowe badanie sprawy",
     "Potrzebne było dokładniejsze badanie",
     "потеряна сравнительная степень, и «sprawy» в эталоне нет"),
    # 11684 volltanken
    (17404, "example_ru", "Мне нужно заполнить бак перед поездкой",
     "Мне нужно заправить полный бак, прежде чем начнётся поездка",
     "«заполнить бак» — калька, и потеряно «bevor die Fahrt beginnt»"),
    (17404, "example_tr",
     "Yola çıkmadan önce tamamen yakıt almalıyız",
     "Yola çıkmadan önce depoyu doldurmalıyım",
     "в эталоне «ich», а не «мы»"),
    # 11685 entwaffnen
    (16960, "example_pl", "Policja musiała rozbroić napastnika",
     "Policja musiała rozbroić uzbrojonego mężczyznę",
     "«napastnik» вместо «bewaffneter Mann»"),
    # 11686 dreihundert
    (13608, "example_tr", "Üçyüz kişi orada toplandı",
     "Üç yüz kişi orada toplandı",
     "«üç yüz» пишется раздельно"),
    # 11687 Klapperschlange
    (15873, "example_uk", "Гремуча змія лежить на дорозі",
     "Гримуча змія лежить на дорозі",
     "«гремуча» — русская форма, в статье «гримуча»"),
    # 11689 Hämorrhoiden
    (13155, "example_uk",
     "Після довгої поїздки у нього з'явилися геморой",
     "Після довгої поїздки в нього з'явився геморой",
     "рассогласование числа"),
    # 11690 Respektlosigkeit
    (11578, "example_uk", "Його неповажність до вчителя всіх обурила",
     "Його неповага до старших була нестерпною",
     "перевод другого предложения"),
    # 11692 besudeln
    (8664, "example_uk", "Не забрудни нову сорочку соусом",
     "Його репутацію заплямували скандали",
     "перевод совсем другого предложения"),
    # 11693 gekühlt
    (12021, "example_pl", "Schłodzone piwo smakuje najlepiej w upał",
     "Schłodzone piwo smakowało wspaniale w ten upalny dzień",
     "перевод другого предложения"),
    # 11694 Sternchen
    (15874, "example_ru", "Маленькая звездочка на небе была красивой",
     "Маленькая звёздочка на небе была прекрасной",
     "«е» вместо «ё», и «wunderschön» это прекрасной"),
    # 11695 Empfindungen
    (11579, "example_pl", "Mam dziwne odczucie w nodze",
     "Z trudem mógł wyrazić swoje najgłębsze uczucia",
     "перевод другого предложения"),
    # 11696 geröstet
    (12022, "example_pl", "Świeżo palona kawa pięknie pachnie",
     "Palona kawa pięknie pachniała",
     "«świeżo» в эталоне нет, и время не то"),
    # 2966 versenden — найдено приметой, вне блока
    (2966, "example_de", "Ich versende das Paket heute ab",
     "Ich versende das Paket heute",
     "«versenden» и «absenden» в одной фразе сразу"),
    # 9945 tilgen — найдено приметой, вне блока
    (9945, "example_de", "Ich tilge meine Schulden langsam ab",
     "Ich tilge meine Schulden langsam",
     "у «tilgen» нет приставки «ab»"),
]


def main() -> None:
    apply_mode = "--apply" in sys.argv
    engine = create_engine(settings.DATABASE_URL_SYNC)

    ok, skipped = [], []
    with engine.connect() as conn:
        for wid, col, was, now, why in FIXES:
            cur = conn.execute(
                text(f"SELECT {col} FROM words WHERE id = :i"), {"i": wid}
            ).scalar()
            if (cur or "").strip() != was:
                skipped.append((wid, col, cur))
            else:
                ok.append((wid, col, was, now, why))

    print(f"=== правок {len(FIXES)}, совпало {len(ok)}, "
          f"пропущено {len(skipped)} ===\n")
    for wid, col, was, now, why in ok:
        print(f"  {wid} {col} — {why}")
        print(f"      было:  {was!r}")
        print(f"      стало: {now!r}")
    for wid, col, cur in skipped:
        print(f"  ПРОПУЩЕНО {wid} {col}: {cur!r}")

    if not apply_mode:
        print("\nэто показ. Для применения — флаг --apply")
        return

    with engine.begin() as conn:
        for wid, col, _, now, _ in ok:
            conn.execute(text(f"UPDATE words SET {col} = :v WHERE id = :i"),
                         {"v": now, "i": wid})
    print(f"\nприменено: {len(ok)}")

    with engine.connect() as conn:
        bad = 0
        for wid, col, _, now, _ in ok:
            cur = conn.execute(text(f"SELECT {col} FROM words WHERE id = :i"),
                               {"i": wid}).scalar()
            if (cur or "").strip() != now:
                print(f"  ТРЕВОГА: {wid} {col} не записалось")
                bad += 1
        print(f"самопроверка: не записалось {bad}")


if __name__ == "__main__":
    main()
