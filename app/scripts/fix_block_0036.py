"""
Сплошная вычитка, блок 36: ряды 5501–5700 по рангу частотности
(id первого 16350, id последнего 17207).

Главное за блок:

* `faulen` — ряд, где немецкий пример не про слово ряда. `faulen` это
  «гнить», а пример `Wir faulen den ganzen Tag im Park rum` — про
  `rumfaulen`, «валяться без дела». Русский и польский перевели
  буквально и получили «Мы весь день гниём в парке». Пример приведён к
  слову ряда, за ним все пять переводов.
* `The kings coronation` — притяжательное без апострофа.
* `draufgehen`, `entsprechen`, `gebühren`, `rausschmeißen`, `frieren`,
  `schmelzen`, `Kutscher`, `Wähler` — немецкий говорит одно, часть
  языков другое.
* Украинские небывальщины: `розхиталаний`, `розорюючим`, `умирущий`,
  `піднносу`, `чотири разів`, и `радуга` в значениях к `Regenbogen`.
* Польский `guzik na głowie` в значениях к `Beule` — это пуговица.
* Турецкие небывальщины: `zırzıp`, `penthasta`, `tökmeyesin`,
  `incinettim`, `dansetti`.

    python -m app.scripts.fix_block_0036            # показать
    python -m app.scripts.fix_block_0036 --apply    # применить
"""

from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.config import settings  # noqa: E402

# (id, колонка, что стоит сейчас, на что менять, зачем)
FIXES: list[tuple[int, str, str, str, str]] = [

    # --- faulen: пример был не про слово ряда --------------------------------
    (7451, "example_de", "Wir faulen den ganzen Tag im Park rum",
     "Das Obst fault in der Sonne",
     "«faulen» — гнить; пример был про «rumfaulen»"),
    (7451, "example_en", "We are lazing around in the park",
     "The fruit rots in the sun", "то же"),
    (7451, "example_ru", "Мы весь день гниём в парке",
     "Фрукты гниют на солнце", "то же"),
    (7451, "example_uk", "Я почав лінуватися останнім часом",
     "Фрукти гниють на сонці", "то же"),
    (7451, "example_tr", "Parkta tembel davranıyoruz",
     "Meyveler güneşte çürüyor", "то же"),
    (7451, "example_pl", "Cały dzień gnijemy w parku",
     "Owoce gniją na słońcu", "то же"),

    # --- английский апостроф -------------------------------------------------
    (14550, "example_en", "The kings coronation was a big celebration",
     "The king's coronation was a big celebration",
     "пропущен апостроф притяжательного"),

    # --- перевод переводит другую фразу --------------------------------------
    (7467, "example_en", "All the money goes to rent",
     "A lot of time will go into this",
     "немецкий «Dabei wird viel Zeit draufgehen»"),
    (7467, "example_uk", "Усі гроші йдуть на оренду",
     "На це піде багато часу", "то же"),
    (7467, "example_tr", "Bütün para kira için harcamaya gidiyor",
     "Buna çok zaman gidecek", "то же"),
    (2412, "example_en", "This doesn't meet my expectations",
     "This must comply with the rules",
     "немецкий «Das muss den Regeln entsprechen»"),
    (2412, "example_uk", "Це не відповідає моїм очікуванням",
     "Це повинно відповідати правилам", "то же"),
    (2412, "example_tr", "Bu gerçeğe uymuyor", "Bu kurallara uymalı",
     "то же"),
    (7476, "example_en", "You deserve more respect",
     "He deserves great thanks for that",
     "немецкий «Ihm gebührt großer Dank dafür»"),
    (7476, "example_uk", "Тобі належиться відпустка",
     "Йому належиться велика подяка за це", "то же"),
    (7476, "example_tr", "Daha fazla saygıya lâyıksın",
     "Bunun için büyük bir teşekkürü hak ediyor", "то же"),
    (7472, "example_en", "The boss kicked him out",
     "They want to kick him out next week",
     "немецкий «Sie wollen ihn nächste Woche rausschmeißen»"),
    (7472, "example_uk", "Босс його викинув",
     "Вони хочуть вигнати його наступного тижня", "то же"),
    (7472, "example_tr", "Patron onu dışarı attı",
     "Onu gelecek hafta işten atmak istiyorlar", "то же"),
    (12718, "example_en", "It is cold, we will freeze",
     "I'm cold, we will freeze", "немецкий «Mir ist kalt»"),
    (12718, "example_uk", "Холодно, ми замерзнемо",
     "Мені холодно, ми замерзнемо", "то же"),
    (12718, "example_tr", "Soğuk, donacağız", "Üşüyorum, donacağız",
     "то же"),
    (15580, "example_en", "The snow melts in the sun",
     "The ice melts in the sun", "немецкий «Das Eis schmilzt»"),
    (15580, "example_uk", "Сніг тане на сонці", "Лід тане на сонці",
     "то же"),
    (15580, "example_tr", "Kar güneşte eriyor", "Buz güneşte eriyor",
     "то же"),
    (8975, "example_en", "The coachman drives the horses through the city",
     "The coachman drives the carriage through the city",
     "немецкий «fährt die Kutsche»"),
    (8975, "example_uk", "Кучер їде на конях через місто",
     "Кучер веде карету через місто", "то же"),
    (8975, "example_tr", "Arabacı atları şehirden geçiriyor",
     "Arabacı faytonu şehirden geçiriyor", "то же"),
    (16356, "example_en", "The voter determines the outcome of the election",
     "The voter decides about politics",
     "немецкий «Der Wähler entscheidet über die Politik»"),
    (16356, "example_uk", "Виборець вирішує політику",
     "Виборець вирішує, якою буде політика", "фраза не собрана"),
    (16356, "example_pl", "Wyborcy poszli do urn w niedzielę",
     "Wyborca decyduje o polityce", "то же"),
    (1733, "example_en", "Let me note your phone number",
     "Please note down the appointment",
     "немецкий «Notier dir bitte den Termin»"),
    (1733, "example_uk", "Я занотовую все на лекціях",
     "Запиши, будь ласка, дату зустрічі", "то же"),
    (1733, "example_tr", "Adresini hemen not ettim",
     "Lütfen randevuyu not et", "то же"),

    # --- украинские небывальщины и опечатки ----------------------------------
    (17585, "example_uk", "Штепсель розхиталаний, вставляй його краще",
     "Штепсель розхитаний, вставляй його краще", "«розхиталаний» — не слово"),
    (12716, "example_uk", "Крах економіки був розорюючим",
     "Крах економіки був руйнівним", "«розорюючим» — не слово"),
    (12724, "translation_uk", "умирущий, що вмирає, вмираючий",
     "вмираючий, що вмирає, присмертний", "«умирущий» — не слово"),
    (12724, "example_uk", "Той, що вмирає, чоловік просив води",
     "Вмираючий чоловік попросив води", "порядок слов сломан"),
    (11784, "example_uk", "Їжа лежить на піднносу",
     "Їжа лежить на таці", "«піднносу» — опечатка и падеж"),
    (13549, "translation_uk", "чотири рази, чотири разів",
     "чотири рази, чотирикратно", "«чотири разів» — не форма"),
    (15578, "translation_uk", "веселка, радуга", "веселка, райдуга",
     "«радуга» — русское слово"),
    (10759, "example_uk", "Я презираю людей, які насміхаються над іншими",
     "Я зневажаю людей, які насміхаються над іншими",
     "«презирати» — русизм"),
    (15116, "example_uk", "Супруг королеви також був присутній",
     "Чоловік королеви також був присутній", "«Супруг» — русское слово"),
    (7469, "example_uk", "Мені приховали важну інформацію",
     "Від мене приховали важливу інформацію",
     "«важну» — русская форма, и конструкция"),
    (7449, "example_uk", "Ув'язнений намагається втекти з тюрми",
     "Ув'язнений намагається втекти з в'язниці", "«тюрма» — русизм"),
    (13552, "example_uk", "Мені треба півтора години для подорожі",
     "Мені треба півтори години на дорогу",
     "«півтора» при женском роде"),
    (7465, "example_uk", "Я тебе кілька разів попереджував",
     "Я тебе кілька разів попереджав", "«попереджував» — не форма"),
    (12720, "example_uk", "Сухожилля в моїй ногі болить",
     "Сухожилля в моїй нозі болить", "«ногі» — не форма"),
    (12719, "example_uk", "Я вдарився ліктем", "Я травмував лікоть",
     "«verletzt» — травмировал"),
    (15585, "example_uk", "Маленька мишеня ховається",
     "Маленька мишка ховається", "род не согласован"),
    (10774, "example_uk", "Це чиста божевільність",
     "Це чисте божевілля", "в значениях «божевілля»"),
    (7464, "example_uk", "Це на добро всіх людей",
     "Це на благо всіх людей", "«на добро» — не та форма"),
    (12717, "example_uk", "У мене є шишка на голові",
     "У мене ґуля на голові", "в значениях первое «ґуля», и лишнее «є»"),
    (12711, "example_uk", "Я застудив горло на протязі",
     "Я застуджений і залишаюся сьогодні вдома",
     "немецкий «Ich bin erkältet und bleibe heute zu Hause»"),
    (12713, "example_uk", "У сп'янінні він наговорив дурниць",
     "Після вечірки я все ще був у сп'янінні",
     "немецкий «Nach der Party war ich noch im Rausch»"),
    (12714, "example_uk", "Розрізаний кавун лежить на столі",
     "Розрізану рану довелося зашити",
     "немецкий «Die aufgeschlitzte Wunde musste genäht werden»"),
    (14551, "example_uk", "Вона прочитала вірш напам'ять",
     "Перший куплет пісні гарний",
     "немецкий «Der erste Vers des Liedes ist schön»"),
    (14549, "example_uk", "Об'явлення було для нього великим шоком",
     "Одкровення було для нього великим шоком",
     "в значениях первое «одкровення»"),
    (9828, "example_uk", "У тебе є гроші на концерт?",
     "У тебе досить грошей на концерт?", "потеряно «genug»"),
    (15107, "example_uk", "Маленький хлопчик зовсім милий",
     "Маленький хлопчина дуже милий", "в значениях «хлопчина»"),
    (10757, "example_uk", "Його занепокоєння про майбутнє обґрунтоване",
     "Його занепокоєння щодо майбутнього обґрунтоване", "предлог"),
    (14102, "example_uk", "Отримувач не забрав посилку з пошти",
     "Отримувач вказаний внизу",
     "немецкий «Der Empfänger steht unten»"),
    (15115, "example_uk", "Дідуся поховали біля старої церкви",
     "Ми поховаємо дідуся наступного тижня",
     "немецкий «Wir beerdigen meinen Großvater nächste Woche»"),
    (18779, "example_uk",
     "У Святий вечір ми даруємо один одному подарунки",
     "На Святвечір ми даруємо один одному подарунки",
     "в значениях «Святвечір»"),
    (10773, "example_uk", "Не принижуй його перед друзями",
     "Він намагався принизити мене перед усіма",
     "немецкий «Er versuchte, mich vor allen zu demütigen»"),
    (18780, "example_uk", "Нещодавно вона кожен день ходить бігти",
     "Останнім часом вона щодня ходить бігати", "фраза не собрана"),
    (10769, "example_uk", "Водій їхав безжалісно й небезпечно",
     "Водій був безцеремонний і небезпечний",
     "немецкий «Der Fahrer war rücksichtslos»"),
    (7455, "example_uk", "Помітно, що ти втомився",
     "Вона носить помітно яскравий одяг",
     "немецкий «Sie trägt auffällig bunte Kleidung»"),

    # --- русские -------------------------------------------------------------
    (17200, "example_ru", "Груженый корабль плывёт медленно",
     "Гружёный корабль медленно плывёт в Гамбург",
     "потеряна «ё» и Гамбург"),
    (16354, "example_ru", "Решено об освобождении заключенного",
     "Освобождение заключённого решено", "калька и потеряна «ё»"),
    (16358, "example_ru", "У меня нет полномочий это подписывать",
     "У тебя нет полномочий это решать",
     "немецкий «Du hast nicht die Befugnis, das zu entscheiden»"),
    (8973, "example_ru",
     "Какую профессию ты хочешь потом освоить и ею заниматься?",
     "Какой профессией ты хочешь потом заниматься?", "фраза перегружена"),
    (17204, "example_ru", "Пристёгивайся, мы уже едем",
     "Не забудь пристегнуться, прежде чем мы поедем",
     "немецкий «Vergiss nicht, dich anzuschnallen»"),

    # --- польские ------------------------------------------------------------
    (12717, "translation_pl", "guz, guzik na głowie, wgniecenie",
     "guz, guzek na głowie, wgniecenie", "«guzik» — пуговица"),
    (16350, "example_pl", "Siły zbrojne chronią granice kraju",
     "Siły zbrojne odpowiadają za obronę kraju",
     "немецкий «sind für die Verteidigung zuständig»"),
    (13546, "example_pl", "Boli mnie tuż poniżej kolana",
     "Obraz wisi poniżej okna",
     "немецкий «Das Bild hängt unterhalb des Fensters»"),
    (12224, "example_pl", "Mój brat jest zawodowym sportowcem",
     "Sportowiec trenuje codziennie",
     "немецкий «Der Sportler trainiert jeden Tag»"),
    (16351, "example_pl", "Detektyw śledził go przez cały tydzień",
     "Policja śledzi podejrzanego",
     "немецкий «Die Polizei beschattet den Verdächtigen»"),
    (11781, "example_pl", "Na kolację zrobiłem łososia z ryżem",
     "Łosoś to moja ulubiona ryba",
     "немецкий «Der Lachs ist mein Lieblingsfisch»"),
    (11782, "example_pl", "Dodaj łyżeczkę sody do ciasta",
     "Lubię pić wodę sodową z cytryną",
     "немецкий «Ich trinke gerne Soda mit Zitrone»"),
    (13549, "example_pl", "Byłem tam już cztery razy",
     "W tym tygodniu byłem cztery razy na siłowni",
     "немецкий про спортзал"),
    (13551, "example_pl", "Wyszedł przed dom na papierosa",
     "Siądź przed oknem", "немецкий «Setz dich vors Fenster»"),
    (12225, "example_pl", "Strzelał do tarczy na podwórku",
     "Tarcza wisi na ścianie",
     "немецкий «Die Zielscheibe hängt an der Wand»"),
    (13699, "example_pl", "Nosiła srebrny medalion na szyi",
     "Nosiła złoty medalion na szyi", "в немецком золотой"),
    (15581, "example_pl", "Promień słońca wpada do pokoju",
     "Promień światła wpada przez okno",
     "немецкий «Der Lichtstrahl fällt durch das Fenster»"),
    (16354, "example_pl", "Czekamy na zezwolenie szefa",
     "Zwolnienie więźnia zostało postanowione",
     "немецкий «Die Freigabe des Gefangenen ist beschlossen»"),
    (15582, "example_pl", "Nad łąką leci rój pszczół",
     "Rój pszczół przelatuje obok", "луг приписан"),
    (15583, "example_pl", "Koń je siano w stajni", "Koń je siano",
     "конюшня приписана"),
    (11785, "example_pl", "Na tym polu rośnie pszenica",
     "Pszenica dobrze rośnie na tym polu", "потеряно «gut»"),
    (13552, "example_pl", "Czekaliśmy półtorej godziny na autobus",
     "Potrzebuję półtorej godziny na podróż",
     "немецкий «Ich brauche eineinhalb Stunden für die Fahrt»"),
    (16357, "example_pl", "Jego dziadek był komunistą",
     "Komunista bronił swojej ideologii",
     "немецкий «Der Kommunist verteidigte seine Ideologie»"),
    (11786, "example_pl", "Polej makaron sosem pomidorowym",
     "Sos smakował wyśmienicie z mięsem",
     "немецкий «Die Sauce schmeckte köstlich zum Fleisch»"),
    (13700, "example_pl", "W muzeum pokazują stare klejnoty",
     "Klejnot był bardzo cenny",
     "немецкий «Das Juwel war von großem Wert»"),
    (15584, "example_pl", "W ogrodzie siedzi duża ropucha",
     "Ropucha skacze przez ulicę",
     "немецкий «Die Kröte hüpft über die Straße»"),
    (15585, "example_pl", "Mała myszka schowała się za szafą",
     "Mała myszka się chowa", "шкаф приписан"),
    (11787, "example_pl", "Posmaruj chleb masłem orzechowym",
     "Lubię masło orzechowe",
     "немецкий «Ich esse gerne Erdnussbutter»"),
    (16358, "example_pl", "Nie masz uprawnień, żeby to podpisać",
     "Nie masz uprawnień, żeby o tym decydować",
     "«podpisać» — подписать, а в немецком решать"),

    # --- турецкие небывальщины и падежи --------------------------------------
    (10770, "example_tr", "Gerçekten zırzıp biri",
     "Gerçekten huysuz bir kadın", "«zırzıp» — не слово"),
    (18270, "example_tr", "Şehirde bir penthasta yaşıyor",
     "Şehirde bir çatı katı dairesinde yaşıyor", "«penthasta» — не слово"),
    (18266, "example_tr", "Eşiğe dikkat et, tökmeyesin",
     "Eşiğe dikkat et, tökezlemeyesin", "«tökmeyesin» — не слово"),
    (12719, "example_tr", "Dirseğimi incinettim", "Dirseğimi incittim",
     "«incinettim» — опечатка"),
    (12226, "example_tr", "Kukla sahnede dansetti",
     "Kukla sahnede dans etti", "«dans etmek» пишется раздельно"),
    (12712, "example_tr", "Babamın kalp krizi geçirmişti",
     "Babam kalp krizi geçirdi", "«Babamın» — чей-то отец"),
    (17584, "example_tr", "Bu yeni arabanın ilk prototipıdir",
     "Bu yeni arabanın ilk prototipi", "«prototipıdir» — опечатка и «-dir»"),
    (11787, "example_tr", "Yer fistığı tereyağını seviyorum",
     "Fıstık ezmesini severim", "«yer fıstığı tereyağı» — калька"),
    (8969, "example_tr", "Kalp cerrahisinde uzmanlaştırılmış",
     "Kalp cerrahisinde uzmanlaşmış", "лишний страдательный залог"),
    (10759, "example_tr", "Kimseyi hor görme",
     "Başkalarıyla alay eden insanları hor görürüm",
     "немецкий «Ich verachte Menschen, die andere auslachen»"),
    (12714, "example_tr", "Kesiş yara dikişle kapatılması gerekiyordu",
     "Yarılmış yaranın dikilmesi gerekiyordu", "фраза не собрана"),
    (10760, "example_tr", "Çikolata için bir eğilimim var",
     "Çikolataya karşı bir eğilimim var", "падеж"),
    (2036, "example_tr", "Buluşma saatini yarın kararlaştıralım",
     "Bir randevu kararlaştırıyoruz", "«yarın» приписано"),
    (17974, "example_tr", "Topçuluk piyadeyi destekledi",
     "Topçu birliği piyadeyi destekledi", "«topçuluk» — ремесло"),
    (17588, "example_tr", "Okumak için bir büyüteç gerekli",
     "Okumak için bir büyütece ihtiyacım var", "«gerekli» — не форма"),
    (10765, "example_tr", "Rahatsızlıklar minimaldir",
     "Rahatsızlıklar azdı", "«minimaldir» — канцелярит"),
    (13699, "example_tr", "Boynunda altın bir madalyon taşıyordu",
     "Boynunda altın bir madalyon takıyordu", "«taşımak» — носить груз"),
    (17202, "example_tr", "Tren üçüncü rayda", "Tren üçüncü peronda",
     "«ray» — рельс"),
    (14096, "example_tr", "Sözlerimi harfiyen alma",
     "Sözlerimi harfiyen anlama", "«almak» — не то слово"),
    (10766, "example_tr", "Çocuk çok zekiydi", "Çocuk çok zeki",
     "в немецком настоящее время"),
    (15581, "example_tr", "Işın pencereden geçiyor",
     "Işık huzmesi pencereden içeri düşüyor", "«geçiyor» — проходит мимо"),
    (15582, "example_tr", "Bir sürü arı uçup geçiyor",
     "Bir arı sürüsü uçup geçiyor", "«bir sürü» — много"),
    (12721, "example_tr", "Omurga önemlidir", "Omurga çok önemli", "«-dir»"),
    (7461, "example_tr", "Filmin son sekansı çok etkileyici",
     "Olayların sırası önemli",
     "немецкий «Die Sequenz der Ereignisse ist wichtig»"),
    (15583, "example_tr", "At saman yiyor", "At kuru ot yiyor",
     "«saman» — солома"),
    (10768, "example_tr", "İki oyuncu arasındaki romansa kısa sürdü",
     "İki oyuncu arasındaki romans kısa sürdü", "«romansa» — не форма"),
    (11785, "example_tr", "Buğday bu alanda iyi büyüyor",
     "Buğday bu tarlada iyi büyüyor", "«alan» — площадь"),
    (7463, "example_tr", "Benim yeteneklerim oldukça sınırlı",
     "Yeteneklerim oldukça sınırlı", "лишнее «benim»"),
    (15584, "example_tr", "Kurbağa yolun üstüne sıçrıyor",
     "Kara kurbağası yolun karşısına zıplıyor", "«üstüne» — наверх"),
    (10771, "example_tr", "Bununla kaldıramıyorum", "Bunu kaldıramıyorum",
     "падеж"),
    (10773, "example_tr", "Herkes karşısında beni aşağılamaya çalıştı",
     "Herkesin önünde beni aşağılamaya çalıştı", "«herkes karşısında» — калька"),
    (7475, "example_tr", "Bu bilgi senin için ilgili",
     "Bu bilgi senin için önemli", "«ilgili» — связанный"),
    (15116, "example_tr", "Kraliçenin eşi de hazırda idi",
     "Kraliçenin eşi de oradaydı", "«hazırda idi» — не форма"),
    (17975, "example_tr", "İnsan organizması karmaşıktır",
     "İnsan organizması karmaşık", "«-dır»"),
    (7477, "example_tr", "Çok yorgun bir izlenim veriyorsun",
     "Bu biraz garip bir izlenim veriyor",
     "немецкий «Das kommt etwas seltsam rüber»"),
    (16358, "example_tr", "Bunu karar verme yetkin yok",
     "Buna karar verme yetkin yok", "падеж"),
    (12722, "example_tr", "Terapistim benim sorunlarımla yardım ediyor",
     "Terapistim sorunlarımda bana yardım ediyor", "падежи"),
    (11786, "example_tr", "Sos ete lezzetli geldi",
     "Sos etle çok lezzetliydi", "фраза не собрана"),
    (10762, "example_tr", "Onun taklit edilen kibarlığı şeffaf idi",
     "Onun yapmacık kibarlığı belli oluyordu", "калька и «idi»"),
    (10763, "example_tr", "Yenilen korku artık o kadar kötü değil",
     "Aşılan korku artık o kadar kötü değil", "«yenilen» — съеденный"),
    (8972, "example_tr", "Kardeşim gerçek bir icatçı",
     "İyi bir mucit sabır ve yaratıcılık ister",
     "немецкий «Ein guter Erfinder braucht Geduld und Kreativität»"),
    (12717, "example_tr", "Başımda bir çıkıntı var",
     "Başımda bir şişlik var", "«çıkıntı» — выступ"),
    (18777, "example_tr", "Cuma akşamları sinemaya gidiyoruz",
     "Cuma akşamları sık sık sinemaya gidiyoruz", "потеряно «oft»"),
    (7453, "example_tr", "Saçlarım için bir lastik gerekli",
     "Saçım için bir lastiğe ihtiyacım var", "«gerekli» — не форма"),
    (7454, "example_tr", "Hırsız izleri silinmiş kayboldu",
     "Hırsız iz bırakmadan kayboldu", "фраза не собрана"),
    (14095, "example_tr", "Bir uzlaşı buldum", "Bir uzlaşma bulduk",
     "лицо не согласовано"),
    (12225, "example_tr", "Hedef duvarda asılıdır",
     "Hedef tahtası duvarda asılı", "«-dır»"),
    (14548, "example_tr", "Bu benim için kutsal ve vazgeçmeyeceğim",
     "Bu benim için kutsal", "вторая половина приписана"),
    (7448, "example_tr", "Daha sık spor salonuna gidiyor",
     "Eskisinden daha sık spor salonuna gidiyor", "потеряно «als früher»"),
    (12711, "example_tr", "Soğuk almışım ve evde kalıyorum",
     "Üşütmüşüm ve evde kalıyorum", "«soğuk almak» — не форма"),

    # --- потерянное и приписанное --------------------------------------------
    (14550, "example_tr", "Kralın taç giyme töreni büyük bir kutlama idi",
     "Kralın taç giyme töreni büyük bir kutlamaydı", "«idi» пишут слитно"),
    (8973, "example_en", "What profession would you like to have later?",
     "What profession would you like to practice later?",
     "«have» слабее, чем «ausüben»"),
    (2553, "example_en", "Homesickness hit me after one week abroad",
     "I'm homesick for my family",
     "немецкий «Ich habe Heimweh nach meiner Familie»"),
    (2553, "example_uk", "Я сумую за домом",
     "Я сумую за своєю родиною", "то же"),
    (2553, "example_tr", "Memleketimi özlüyorum", "Ailemi özlüyorum",
     "то же"),
    (17200, "example_en", "The laden ship moves slowly",
     "The laden ship moves slowly to Hamburg", "потерян Гамбург"),
    (17200, "example_uk", "Навантажений корабель пливе повільно",
     "Навантажений корабель повільно пливе до Гамбурга", "то же"),
    (17200, "example_tr", "Yüklü gemi yavaş hareket ediyor",
     "Yüklü gemi yavaşça Hamburg'a gidiyor", "то же"),
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
