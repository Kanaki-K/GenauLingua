"""B1, блок 24: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    10273: ("ru «совершенно измучен» — книжно", {"x_ru": "После долгого похода я совсем без сил"}),
    6714: (EN + " («That's possibly too expensive»)", {"x_en": "That might be too expensive for us"}),
    9749: (LIST + "; убрать пометки (colloq.)", {
        "t_ru": "на мели, без денег", "t_uk": "на мілині, без грошей", "t_en": "broke, bankrupt",
        "t_tr": "beş parasız, iflas etmiş", "t_pl": "spłukany, zbankrutowany", "t_it": "al verde, squattrinato",
        "t_es": "sin blanca, en quiebra", "t_fr": "fauché, ruiné"}),
    14410: ("«Das Drehbuch für den Film ist fertig» — пусто", {**all_x(
        "Er schreibt Drehbücher für Serien", "Он пишет сценарии для сериалов", "Він пише сценарії для серіалів",
        "He writes scripts for TV series", "Diziler için senaryo yazıyor", "Pisze scenariusze do seriali",
        "Scrive sceneggiature per serie TV", "Escribe guiones para series", "Il écrit des scénarios pour des séries",
        "Píše scénáře k seriálům")}),
    2650: ("«Ich habe gute Laune» — пусто", {**all_x(
        "Der Chef hat heute schlechte Laune", "У шефа сегодня плохое настроение", "У шефа сьогодні поганий настрій",
        "The boss is in a bad mood today", "Patronun bugün keyfi yok", "Szef ma dziś zły humor",
        "Il capo oggi è di cattivo umore", "El jefe está hoy de mal humor", "Le chef est de mauvaise humeur aujourd'hui",
        "Šéf má dneska špatnou náladu")}),
    16023: ("«Die Polizei legte ihm Handschellen an» — претерит", {**all_x(
        "Die Polizei hat ihm Handschellen angelegt", "Полиция надела на него наручники", "Поліція наділа на нього кайданки",
        "The police put handcuffs on him", "Polis ona kelepçe taktı", "Policja założyła mu kajdanki",
        "La polizia gli ha messo le manette", "La policía le puso las esposas", "La police lui a passé les menottes",
        "Policie mu nasadila pouta")}),
    13926: ("«Das ist ein interessanter Ausdruck» — пусто", {**all_x(
        "Den Ausdruck kenne ich nicht", "Я не знаю этого выражения", "Я не знаю цього виразу",
        "I don't know that expression", "Bu ifadeyi bilmiyorum", "Nie znam tego wyrażenia",
        "Non conosco questa espressione", "No conozco esa expresión", "Je ne connais pas cette expression",
        "Ten výraz neznám")}),
    18669: ("«Die heutige Welt ist sehr schnell» — газета", {**all_x(
        "Hast du die heutige Zeitung gesehen?", "Ты видел сегодняшнюю газету?", "Ти бачив сьогоднішню газету?",
        "Have you seen today's paper?", "Bugünkü gazeteyi gördün mü?", "Widziałeś dzisiejszą gazetę?",
        "Hai visto il giornale di oggi?", "¿Has visto el periódico de hoy?", "Tu as vu le journal d'aujourd'hui?",
        "Viděl jsi dnešní noviny?")}),
    71: ("«Das Badezimmer ist klein» — пусто", {**all_x(
        "Das Badezimmer ist gerade besetzt", "Ванная сейчас занята", "Ванна кімната зараз зайнята",
        "The bathroom's busy right now", "Banyo şu an dolu", "Łazienka jest teraz zajęta", "Il bagno adesso è occupato",
        "El baño está ocupado ahora mismo", "La salle de bains est occupée", "Koupelna je teď obsazená")}),
    17500: (LIST, {
        "t_ru": "сеть, связь", "t_uk": "мережа, зв'язок", "t_en": "network, signal", "t_tr": "şebeke, ağ",
        "t_pl": "sieć, zasięg"}),
    8796: (LIST + "; нанимать — другое значение", {
        "t_ru": "натворить, включить", "t_uk": "накоїти, увімкнути", "t_en": "to get up to, to switch on",
        "t_tr": "karıştırmak, açmak", "t_pl": "narobić, włączyć", "t_it": "combinare, accendere", "t_es": "hacer, encender",
        "t_fr": "faire, allumer", "t_cs": "vyvádět, zapnout"}),
    505: ("«Sie hat Kopfschmerzen» — пусто; ru «у неё головная боль» — калька", {**all_x(
        "Von dem Lärm bekomme ich Kopfschmerzen", "От этого шума у меня болит голова", "Від цього шуму в мене болить голова",
        "That noise is giving me a headache", "Bu gürültüden başım ağrıyor", "Od tego hałasu boli mnie głowa",
        "Questo rumore mi fa venire mal di testa", "Este ruido me da dolor de cabeza", "Ce bruit me donne mal à la tête",
        "Z toho hluku mě bolí hlava")}),
    1095: ("«Die Übung ist wichtig» — пусто", {**all_x(
        "Mir fehlt noch die Übung", "Мне ещё не хватает практики", "Мені ще бракує практики",
        "I still need more practice", "Daha pratiğe ihtiyacım var", "Brakuje mi jeszcze wprawy",
        "Mi manca ancora la pratica", "Todavía me falta práctica", "Je manque encore de pratique",
        "Ještě mi chybí praxe")}),
    2818: ("«Das ist sinnlos» — пусто", {**all_x(
        "Es ist sinnlos, mit ihm zu streiten", "С ним бессмысленно спорить", "З ним безглуздо сперечатися",
        "It's pointless arguing with him", "Onunla tartışmak anlamsız", "Kłótnia z nim nie ma sensu",
        "È inutile litigare con lui", "Es inútil discutir con él", "C'est inutile de se disputer avec lui",
        "Je nesmyslné se s ním hádat")}),
    1293: ("«Das Haus brennt» — пусто; " + LIST, {
        "t_ru": "гореть, жечь", "t_uk": "горіти, пекти", "t_en": "to burn, to be on", "t_tr": "yanmak, acımak",
        "t_pl": "palić się, piec", "t_it": "bruciare, essere acceso", "t_es": "arder, estar encendido",
        "t_fr": "brûler, être allumé", "t_cs": "hořet, pálit",
        **all_x("Im Keller brennt noch Licht", "В подвале ещё горит свет", "У підвалі ще горить світло",
                "The light's still on in the cellar", "Bodrumda ışık hâlâ yanıyor", "W piwnicy jeszcze pali się światło",
                "In cantina c'è ancora la luce accesa", "En el sótano todavía hay una luz encendida",
                "Il y a encore de la lumière allumée à la cave", "Ve sklepě ještě hoří světlo")}),
    17501: ("«Welcher Sender läuft denn heute Abend?» — так не говорят; " + LIST, {
        "t_ru": "телеканал, радиостанция", "t_uk": "телеканал, радіостанція", "t_en": "channel, station",
        "t_tr": "kanal, istasyon", "t_pl": "kanał, stacja", "t_it": "il canale, l'emittente",
        **all_x("Auf welchem Sender kommt das Spiel?", "На каком канале показывают матч?", "На якому каналі показують матч?",
                "Which channel is the match on?", "Maç hangi kanalda?", "Na którym kanale jest mecz?",
                "Su che canale danno la partita?", "¿En qué canal echan el partido?", "Le match passe sur quelle chaîne?",
                "Na jakém kanálu dávají zápas?")}),
    2379: ("«Die Bewerbung ist eingegangen» — канцелярит; " + LIST, {
        "t_ru": "засыхать, садиться (о ткани)", "t_uk": "засихати, сідати (про тканину)", "t_en": "to die, to shrink",
        "t_tr": "kurumak, çekmek", "t_pl": "usychać, kurczyć się", "t_it": "morire, restringersi",
        "t_es": "morirse, encogerse", "t_fr": "dépérir, rétrécir", "t_cs": "uschnout, srazit se",
        **all_x("Ohne Wasser geht die Pflanze ein", "Без воды растение засохнет", "Без води рослина засохне",
                "Without water the plant will die", "Su olmadan bitki kurur", "Bez wody roślina uschnie",
                "Senz'acqua la pianta muore", "Sin agua la planta se muere", "Sans eau, la plante dépérit",
                "Bez vody kytka uschne")}),
    8798: ("«Das Meeting ist um drei Uhr» — пусто", {**all_x(
        "Ich muss jetzt in ein Meeting", "Мне пора на совещание", "Мені вже треба на нараду",
        "I've got to go to a meeting now", "Şimdi bir toplantıya girmem lazım", "Muszę teraz iść na spotkanie",
        "Adesso devo andare a una riunione", "Ahora tengo una reunión", "Là, je dois aller en réunion",
        "Teď musím na poradu")}),
    11667: ("«Das Essen war wirklich köstlich» — шаблон Essen; " + LIST, {
        "t_ru": "очень вкусный, восхитительный", "t_uk": "дуже смачний, чудовий", "t_en": "delicious, delightful",
        "t_tr": "nefis, çok lezzetli", "t_pl": "przepyszny, wyśmienity",
        **all_x("Das riecht ja köstlich!", "Как вкусно пахнет!", "Як смачно пахне!", "That smells delicious!",
                "Çok nefis kokuyor!", "Ale przepysznie pachnie!", "Che profumo delizioso!", "¡Qué olor tan delicioso!",
                "Ça sent délicieux!", "To voní výborně!")}),
    13488: (EN + " («some store»)", {"x_en": "I bought it in some shop"}),
    17087: (LIST, {
        "t_ru": "груз, заряд", "t_uk": "вантаж, заряд", "t_en": "load, charge", "t_tr": "yük",
        "t_pl": "ładunek, towar", "t_fr": "le chargement, la charge", "t_cs": "náklad, náboj"}),
    10280: ("ru «Ты должен стыдиться» — калька müssen/sollen", {
        "x_ru": "Постыдился бы своего поведения!", "x_uk": "Посоромився б своєї поведінки!",
        "x_en": "You should be ashamed of your behaviour"}),
    1890: ("«Das Kind spielt mit Spielzeug» — пусто", {**all_x(
        "Räum dein Spielzeug auf!", "Убери свои игрушки!", "Прибери свої іграшки!", "Tidy up your toys!",
        "Oyuncaklarını topla!", "Posprzątaj zabawki!", "Metti a posto i tuoi giocattoli!", "¡Recoge tus juguetes!",
        "Range tes jouets!", "Ukliď si hračky!")}),
}

REPLACE = [
    {"id": 10275, "by": 11969, "lang": "de", "why": "stille — форма слова still"},
    {"id": 10278, "by": 10161, "lang": "de", "why": "verfluchte — форма слова verflucht"},
    {"id": 10279, "by": 1136, "lang": "de", "why": "Furcht — книжный вариант Angst"},
]

SPLIT_LATER = {
    8796: ["anstellen = нанимать (Die Firma stellt neue Leute an)"],
    2379: ["eingehen = поступать (Die Bewerbung ist eingegangen); eingehen auf = вникать"],
    13488: ["irgendeinem — форма; нет леммы irgendein (есть только irgendeiner = кто-нибудь)"],
}
