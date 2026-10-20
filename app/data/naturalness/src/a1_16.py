"""A1, блок 16: слова 601–640 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
TWO = "в строке два разных слова — оставлено главное, второе — отдельной строкой (блок деления)"
EN = "английский пример: так не говорят"
DULL = "пример ни о чём («X ist Y») → фраза из жизни"
NEAR = "пример почти повторял пример другого слова — у каждого свой"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    18185: (LIST, {"t_ru": "зал, павильон", "t_uk": "зал, павільйон", "t_en": "hall", "t_tr": "salon",
                   "t_pl": "hala, sala", "t_it": "la sala, il padiglione", "t_es": "la sala, el pabellón",
                   "t_fr": "la salle, le hall", "t_cs": "hala, sál"}),
    398: (NEAR + " (November: «Im November ist es kühl»)", {**all_x(
        "Im Herbst fallen die Blätter", "Осенью опадают листья", "Восени опадає листя", "In autumn the leaves fall",
        "Sonbaharda yapraklar dökülür", "Jesienią spadają liście", "In autunno cadono le foglie",
        "En otoño caen las hojas", "En automne, les feuilles tombent", "Na podzim padá listí")}),
    447: (NEAR + " (Februar, Winter — «… ist es kalt»)", {**all_x(
        "Im Januar fängt das neue Jahr an", "В январе начинается новый год", "У січні починається новий рік",
        "The new year starts in January", "Yeni yıl ocakta başlar", "W styczniu zaczyna się nowy rok",
        "A gennaio comincia l'anno nuovo", "En enero empieza el año nuevo", "En janvier, la nouvelle année commence",
        "V lednu začíná nový rok")}),
    12167: ("пять значений → главные два", {"t_ru": "лук, дуга", "t_uk": "лук, дуга", "t_en": "bow, arch",
                                            "t_tr": "yay, kemer", "t_pl": "łuk", "t_it": "l'arco", "t_es": "el arco",
                                            "t_fr": "l'arc", "t_cs": "luk, oblouk"}),
    16112: (LIST, {"t_ru": "судить, оценивать", "t_uk": "судити, оцінювати", "t_en": "to judge", "t_tr": "yargılamak",
                   "t_pl": "oceniać, sądzić"}),
    894: (LIST + "; «учёба очень требовательна» — калька", {
        "t_ru": "учёба, высшее образование", "t_uk": "навчання, вища освіта", "t_en": "studies, degree",
        "t_tr": "üniversite eğitimi", "t_pl": "studia", "t_it": "gli studi", "t_es": "los estudios, la carrera",
        "x_ru": "Учёба в университете у меня очень сложная", "x_uk": "Моє навчання дуже складне"}),
    2793: (LIST + "; «окошко в банке или на почте» — описание; пример неживой", {
        "t_ru": "выключатель, окошко", "t_uk": "вимикач, віконце", "t_en": "switch, counter", "t_tr": "anahtar, gişe",
        "t_pl": "włącznik, okienko", "t_it": "l'interruttore, lo sportello", "t_es": "el interruptor, la ventanilla",
        "t_fr": "l'interrupteur, le guichet", "t_cs": "vypínač, přepážka",
        **all_x("Der Schalter ist neben der Tür", "Выключатель возле двери", "Вимикач біля дверей",
                "The switch is next to the door", "Anahtar kapının yanında", "Włącznik jest obok drzwi",
                "L'interruttore è accanto alla porta", "El interruptor está al lado de la puerta",
                "L'interrupteur est à côté de la porte", "Vypínač je vedle dveří")}),
    11696: (EN, {"x_en": "I like ham for breakfast"}),
    15019: (LIST, {"t_ru": "родственник, родня", "t_uk": "родич, родина", "t_en": "relative", "t_tr": "akraba",
                   "t_pl": "krewny", "t_it": "il parente", "t_es": "el pariente", "t_fr": "le parent",
                   "t_cs": "příbuzný"}),
    10420: (LIST, {"t_ru": "чужой, незнакомый", "t_uk": "чужий, незнайомий", "t_en": "strange, foreign",
                   "t_tr": "yabancı", "t_pl": "obcy, cudzy", "t_it": "estraneo, straniero", "t_es": "ajeno, extraño",
                   "t_fr": "étranger, inconnu", "t_cs": "cizí", "x_en": "That's unfamiliar to me"}),
    2084: (LIST + "; «кочевать» — другое значение", {
        "t_ru": "ходить в походы, гулять", "t_uk": "ходити в походи, мандрувати", "t_en": "to hike",
        "t_tr": "doğa yürüyüşü yapmak", "t_pl": "wędrować, chodzić po górach", "t_it": "fare escursioni",
        "t_es": "hacer senderismo", "t_fr": "faire de la randonnée", "t_cs": "chodit na túry",
        "x_en": "We go hiking at the weekend"}),
    408: (LIST, {"t_ru": "хобби", "t_uk": "хобі"}),
    298: ("uk «о восьмій годині» — лишнее", {"x_uk": "Ми снідаємо о восьмій"}),
    11702: (LIST + "; «в нашем любимом заведении» — канцелярски", {
        "t_ru": "кафе, заведение", "t_uk": "кафе, заклад", "t_en": "pub, restaurant", "t_tr": "mekan",
        "t_pl": "lokal, knajpa", "t_it": "il locale", "t_es": "el bar, el local", "t_fr": "le café, le bistrot",
        "t_cs": "podnik, hospoda",
        "x_ru": "Встретимся в нашем любимом кафе", "x_uk": "Зустрінемося в нашому улюбленому кафе",
        "x_en": "Let's meet at our favourite place"}),
    10438: ("«Поздравляю тебя с твоим успехом» — калька", {
        "t_it": "congratularsi, fare gli auguri",
        "x_ru": "Поздравляю с успехом!", "x_uk": "Вітаю з успіхом!", "x_en": "Congratulations on your success!"}),
    8855: (LIST, {"t_ru": "чиновник, госслужащий", "t_uk": "чиновник, держслужбовець", "t_en": "official, civil servant",
                  "t_tr": "memur", "t_pl": "urzędnik", "t_it": "il funzionario", "t_cs": "úředník"}),
    15029: (LIST + "; «спутница» — книжно", {"t_ru": "партнёрша", "t_uk": "партнерка", "t_en": "partner",
                                            "t_tr": "partner, eş", "t_pl": "partnerka", "t_it": "la compagna",
                                            "t_es": "la pareja, la compañera", "t_fr": "la compagne, la partenaire",
                                            "t_cs": "partnerka, přítelkyně"}),
    18198: (NEAR + " (Apartment: «…ein kleines Apartment gemietet»); " + LIST, {
        "t_ru": "снимать, арендовать", "t_uk": "орендувати, знімати", "t_en": "to rent", "t_tr": "kiralamak",
        "t_pl": "wynajmować", "t_it": "affittare, noleggiare", "t_es": "alquilar", "t_fr": "louer",
        "t_cs": "pronajmout si",
        **all_x("Wir mieten im Urlaub ein Auto", "В отпуске мы арендуем машину", "У відпустці ми орендуємо машину",
                "We're renting a car on holiday", "Tatilde araba kiralıyoruz", "Na urlopie wynajmujemy samochód",
                "In vacanza noleggiamo una macchina", "En vacaciones alquilamos un coche",
                "En vacances, on loue une voiture", "Na dovolené si pronajímáme auto")}),
    15037: ("«родом откуда-то» — пояснение; «Er ist unbekannter Herkunft» — книжно", {
        "t_ru": "происхождение", "t_uk": "походження", "t_en": "origin", "t_tr": "köken", "t_pl": "pochodzenie",
        **all_x("Die Herkunft spielt keine Rolle", "Происхождение не имеет значения", "Походження не має значення",
                "Origin doesn't matter", "Kökenin önemi yok", "Pochodzenie nie ma znaczenia",
                "L'origine non ha importanza", "El origen no importa", "L'origine n'a pas d'importance",
                "Na původu nezáleží")}),
    981: (LIST, {"t_ru": "разный, различный", "t_uk": "різний", "t_en": "different, various", "t_tr": "farklı, çeşitli",
                 "t_pl": "różny", "t_it": "diverso, vario", "t_es": "diferente, distinto", "t_fr": "différent, divers",
                 "t_cs": "různý, odlišný"}),
    1360: (LIST, {"t_ru": "вход, входная плата", "t_uk": "вхід, плата за вхід", "t_en": "admission, entry",
                  "t_tr": "giriş, giriş ücreti", "t_pl": "wstęp", "t_it": "l'ingresso", "t_es": "la entrada",
                  "t_fr": "l'entrée", "t_cs": "vstup, vstupné"}),
    75: (DULL, {**all_x("Im Sommer frühstücken wir auf dem Balkon", "Летом мы завтракаем на балконе",
                        "Улітку ми снідаємо на балконі", "In summer we have breakfast on the balcony",
                        "Yazın balkonda kahvaltı yaparız", "Latem jemy śniadanie na balkonie",
                        "D'estate facciamo colazione sul balcone", "En verano desayunamos en el balcón",
                        "L'été, on prend le petit-déjeuner sur le balcon", "V létě snídáme na balkoně")}),
    8870: (LIST, {"t_ru": "безработный", "t_uk": "безробітний", "t_en": "unemployed", "t_tr": "işsiz",
                  "t_pl": "bezrobotny"}),
    3051: (TWO + " («дюйм» — омоним, своя строка)", {
        "t_ru": "таможня, пошлина", "t_uk": "митниця, мито", "t_en": "customs, duty", "t_tr": "gümrük",
        "t_pl": "cło, odprawa celna", "t_it": "la dogana, il dazio", "t_es": "la aduana, el arancel",
        "t_fr": "la douane", "t_cs": "celnice, clo"}),
    16165: (LIST, {"t_ru": "иностранец", "t_uk": "іноземець", "t_en": "foreigner", "t_tr": "yabancı",
                   "t_pl": "cudzoziemiec, obcokrajowiec"}),
    17535: (LIST, {"t_ru": "автоматический, автоматически", "t_uk": "автоматичний, автоматично"}),
    753: (NEAR + " (draußen: «Draußen regnet es…»)", {
        "t_ru": "идёт дождь", "t_uk": "іде дощ", "t_tr": "yağmur yağmak", "t_pl": "padać",
        **all_x("Es regnet schon den ganzen Tag", "Дождь идёт уже весь день", "Дощ іде вже цілий день",
                "It's been raining all day", "Bütün gün yağmur yağıyor", "Pada już cały dzień",
                "Piove da tutto il giorno", "Lleva lloviendo todo el día", "Il pleut depuis toute la journée",
                "Prší už celý den")}),
    1673: (LIST, {"t_ru": "мужской", "t_uk": "чоловічий", "t_en": "male", "t_tr": "erkek", "t_pl": "męski"}),
    399: (LIST + "; «источник, очаг» — другие значения; " + EN, {
        "t_ru": "плита", "t_uk": "плита", "t_en": "stove, cooker", "t_tr": "ocak", "t_pl": "kuchenka",
        "t_it": "il fornello", "t_es": "la cocina, el fogón", "t_fr": "la cuisinière", "t_cs": "sporák",
        "x_en": "She's cooking at the stove"}),
    117: (TWO + " («лампочка» — разговорное значение, своя строка)", {
        "t_ru": "груша", "t_uk": "груша", "t_en": "pear", "t_tr": "armut", "t_pl": "gruszka", "t_it": "la pera",
        "t_es": "la pera", "t_fr": "la poire", "t_cs": "hruška"}),
    14032: (LIST, {"t_ru": "объявление", "t_uk": "оголошення", "t_en": "announcement", "t_tr": "anons",
                   "t_pl": "komunikat"}),
    1339: ("порча знаний: uk «розпечатувати» — это «вскрывать конверт», печатать на принтере — «роздрукувати»", {
        "t_ru": "печатать, распечатать", "t_uk": "друкувати, роздрукувати", "x_uk": "Мені треба роздрукувати документ"}),
    141: (EN, {"t_en": "bread roll"}),
    358: (LIST + "; «Greetings to your family» — так не говорят", {
        "t_ru": "привет, приветствие", "t_uk": "привіт, вітання", "t_en": "greeting, regards", "t_tr": "selam",
        "t_pl": "pozdrowienie", "t_es": "el saludo, los recuerdos", "t_fr": "le salut, les amitiés",
        "x_en": "Give my regards to your family"}),
}

SPLIT_LATER = {
    3051: ["der Zoll = дюйм"],
    117: ["die Birne = лампочка (разг.)"],
}
