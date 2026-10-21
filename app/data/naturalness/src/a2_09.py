"""A2, блок 9: слова 321–360 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
SKEL = "пример-скелет («X ist ernst/frisch») — так о вещи не говорят"
TWO = "в строке два разных слова — оставлено главное, второе — отдельной строкой (блок деления)"
EN = "английский пример: так не говорят"
RAIN = "четвёртый пример «идёт дождь, но…» (trotz, daher, trotzdem) — у каждого свой"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    291: ("«с уважением в конце письма» — не перевод, а пояснение; " + LIST, {
        "t_ru": "приветливый, дружелюбный", "t_uk": "привітний, дружелюбний", "t_en": "friendly, kind",
        "t_tr": "nazik, cana yakın", "t_pl": "miły, uprzejmy", "t_it": "gentile, cordiale", "t_es": "amable, simpático",
        "t_fr": "aimable, gentil", "t_cs": "milý, přívětivý",
        **all_x("Die Leute hier sind sehr freundlich", "Люди здесь очень приветливые", "Люди тут дуже привітні",
                "People here are really friendly", "Buradaki insanlar çok cana yakın", "Ludzie tutaj są bardzo mili",
                "La gente qui è molto gentile", "La gente aquí es muy amable", "Les gens ici sont très aimables",
                "Lidi tady jsou moc milí")}),
    17484: ("«Meine Daten sind auf meinem Computer» — неживо; " + LIST, {
        "t_ru": "данные", "t_uk": "дані", "t_en": "data", "t_tr": "veriler, bilgiler", "t_pl": "dane",
        **all_x("Ich habe alle Daten verloren", "Я потерял все данные", "Я втратив усі дані", "I've lost all my data",
                "Bütün verilerimi kaybettim", "Straciłem wszystkie dane", "Ho perso tutti i dati",
                "He perdido todos los datos", "J'ai perdu toutes mes données", "Přišel jsem o všechna data")}),
    2364: ("«Ich denke ebenso» повторял genauso («Ich denke genauso wie du»); " + LIST, {
        "t_ru": "так же, тоже", "t_uk": "так само, теж", "t_en": "just as, likewise", "t_tr": "aynı şekilde, o kadar",
        "t_pl": "tak samo, równie", "t_it": "altrettanto, allo stesso modo", "t_es": "igual de, del mismo modo",
        "t_fr": "aussi, de même", "t_cs": "stejně, rovněž",
        **all_x("Sie spricht Englisch ebenso gut wie Deutsch",
                "Она говорит по-английски так же хорошо, как по-немецки",
                "Вона говорить англійською так само добре, як німецькою", "She speaks English just as well as German",
                "İngilizceyi Almanca kadar iyi konuşuyor", "Mówi po angielsku tak samo dobrze jak po niemiecku",
                "Parla l'inglese altrettanto bene quanto il tedesco", "Habla inglés igual de bien que alemán",
                "Elle parle anglais aussi bien que l'allemand", "Mluví anglicky stejně dobře jako německy")}),
    # genauso в речи на A2 (Goethe A2: «genauso»); ebenso сливается на него
    326: ("уровень: genauso — A2, как и ebenso, который на него заменён", {"level": "A2"}),
    1947: ("«шумиха, скандал» — другое значение (Mach kein Theater); «Wir gehen ins Theater» — как Park, Wald", {
        "t_ru": "театр", "t_uk": "театр", "t_en": "theatre", "t_tr": "tiyatro", "t_pl": "teatr",
        "t_it": "il teatro", "t_es": "el teatro", "t_fr": "le théâtre", "t_cs": "divadlo",
        **all_x("Die Karten fürs Theater habe ich schon", "Билеты в театр у меня уже есть",
                "Квитки до театру в мене вже є", "I've already got the theatre tickets", "Tiyatro biletlerini aldım bile",
                "Bilety do teatru już mam", "I biglietti per il teatro li ho già", "Ya tengo las entradas para el teatro",
                "J'ai déjà les billets pour le théâtre", "Lístky do divadla už mám")}),
    513: (SKEL, {
        "t_en": "illness, disease", "t_pl": "choroba",
        **all_x("Wegen einer Krankheit war ich zwei Wochen zu Hause", "Из-за болезни я две недели сидел дома",
                "Через хворобу я два тижні сидів удома", "I was stuck at home for two weeks with an illness",
                "Hastalık yüzünden iki hafta evdeydim", "Przez chorobę siedziałem dwa tygodnie w domu",
                "Per una malattia sono rimasto a casa due settimane", "Por una enfermedad estuve dos semanas en casa",
                "À cause d'une maladie, je suis resté deux semaines à la maison",
                "Kvůli nemoci jsem byl dva týdny doma")}),
    13452: (LIST, {"t_uk": "незважаючи на, попри", "t_pl": "mimo, pomimo", "t_cs": "navzdory, přes",
                   "x_it": "Nonostante la pioggia facciamo una passeggiata"}),
    1062: ("en «We choose a new president» — неверно; пример — язык новостей; «набирать номер» — третье значение", {
        "t_ru": "выбирать, голосовать", "t_uk": "обирати, голосувати", "t_en": "to choose, to vote",
        "t_tr": "seçmek, oy vermek", "t_pl": "wybierać, głosować", "t_it": "scegliere, votare",
        "t_es": "elegir, votar", "t_fr": "choisir, voter", "t_cs": "vybrat, volit",
        **all_x("Am Sonntag gehe ich wählen", "В воскресенье я иду голосовать", "У неділю я йду голосувати",
                "I'm going to vote on Sunday", "Pazar günü oy vermeye gidiyorum", "W niedzielę idę głosować",
                "Domenica vado a votare", "El domingo voy a votar", "Dimanche, je vais voter", "V neděli jdu volit")}),
    12108: (LIST, {"t_ru": "выходить (в город), заканчиваться", "t_uk": "виходити (розважитися), закінчуватися",
                   "t_en": "to go out, to run out", "t_tr": "dışarı çıkmak, tükenmek", "t_pl": "wychodzić, kończyć się",
                   "t_it": "uscire, finire", "t_es": "salir, acabarse", "t_fr": "sortir, s'épuiser",
                   "t_cs": "jít ven, docházet"}),
    14382: ("«скворец, катаракта» — омонимы в одной строке; «Mein Lieblingsstar singt heute» — неживо", {
        "t_ru": "звезда, знаменитость", "t_uk": "зірка, знаменитість", "t_en": "star, celebrity",
        "t_tr": "yıldız, ünlü", "t_pl": "gwiazda", "t_it": "la star, la celebrità", "t_es": "la estrella, el famoso",
        "t_fr": "la star, la vedette", "t_cs": "hvězda, celebrita",
        **all_x("In Brasilien ist er ein großer Star", "В Бразилии он большая звезда", "У Бразилії він велика зірка",
                "He's a big star in Brazil", "Brezilya'da büyük bir yıldız", "W Brazylii jest wielką gwiazdą",
                "In Brasile è una grande star", "En Brasil es una gran estrella", "Au Brésil, c'est une grande star",
                "V Brazílii je velká hvězda")}),
    672: ("«У меня болит ухо» — то, что говорят врачу; " + LIST, {
        "t_ru": "ухо", "t_uk": "вухо", "t_en": "ear", "t_tr": "kulak", "t_pl": "ucho",
        **all_x("Mir tut das Ohr weh", "У меня болит ухо", "У мене болить вухо", "My ear hurts", "Kulağım ağrıyor",
                "Boli mnie ucho", "Mi fa male l'orecchio", "Me duele el oído", "J'ai mal à l'oreille", "Bolí mě ucho")}),
    1822: (SKEL + "; " + LIST, {
        "t_ru": "острый", "t_uk": "гострий", "t_en": "spicy, sharp", "t_tr": "acı, keskin", "t_pl": "ostry",
        "t_it": "piccante, affilato", "t_es": "picante, afilado", "t_fr": "épicé, tranchant", "t_cs": "pálivý, ostrý",
        **all_x("Ist die Suppe sehr scharf?", "Суп очень острый?", "Суп дуже гострий?", "Is the soup very spicy?",
                "Çorba çok acı mı?", "Czy zupa jest bardzo ostra?", "La zuppa è molto piccante?",
                "¿La sopa está muy picante?", "La soupe est très épicée?", "Je ta polévka hodně pálivá?")}),
    2095: (LIST, {"t_ru": "по-прежнему, и дальше", "t_uk": "надалі, як і раніше", "t_en": "still, from now on",
                  "t_tr": "hâlâ, bundan sonra da", "t_pl": "nadal, dalej", "t_it": "ancora, in futuro",
                  "t_es": "todavía, en adelante", "t_fr": "toujours, à l'avenir", "t_cs": "nadále, stále",
                  "x_uk": "Я й далі працюю тут"}),
    14944: (LIST, {"t_en": "grown-up, adult", "t_tr": "yetişkin", "x_en": "My brother is already grown up"}),
    1773: ("«о 20 годині», «at 8 in the evening» — так время не называют", {
        "t_ru": "программа, передача", "t_uk": "програма, передача", "t_en": "programme, schedule",
        "t_tr": "program", "t_pl": "program", "t_it": "il programma", "t_es": "el programa",
        "t_fr": "le programme, l'émission", "t_cs": "program, pořad",
        **all_x("Was steht heute auf dem Programm?", "Что у нас сегодня в программе?", "Що в нас сьогодні в програмі?",
                "What's on the programme today?", "Bugün programda ne var?", "Co mamy dziś w programie?",
                "Cosa c'è in programma oggi?", "¿Qué hay hoy en el programa?",
                "Qu'est-ce qu'il y a au programme aujourd'hui?", "Co je dnes na programu?")}),
    2578: ("пример — обрывок, не предложение; " + LIST, {
        "t_ru": "в течение, внутри", "t_uk": "протягом, усередині", "t_en": "within, inside", "t_tr": "içinde",
        "t_pl": "w ciągu, wewnątrz", "t_it": "entro, dentro", "t_es": "en el plazo de, dentro de",
        "t_fr": "en l'espace de, dans", "t_cs": "během, do",
        **all_x("Das Paket kommt innerhalb einer Woche", "Посылка придёт в течение недели", "Посилка прийде протягом тижня",
                "The parcel will arrive within a week", "Paket bir hafta içinde gelir", "Paczka przyjdzie w ciągu tygodnia",
                "Il pacco arriva entro una settimana", "El paquete llega en el plazo de una semana",
                "Le colis arrive dans la semaine", "Balík přijde do týdne")}),
    2859: (EN + " («We argue often»); " + LIST, {
        "t_ru": "ссориться, спорить", "t_uk": "сваритися, сперечатися", "t_en": "to argue, to quarrel",
        "t_tr": "tartışmak, kavga etmek", "t_pl": "kłócić się",
        **all_x("Die Kinder streiten sich ständig", "Дети постоянно ссорятся", "Діти постійно сваряться",
                "The kids are always arguing", "Çocuklar sürekli kavga ediyor", "Dzieci ciągle się kłócą",
                "I bambini litigano in continuazione", "Los niños se pelean todo el rato",
                "Les enfants se disputent tout le temps", "Děti se pořád hádají")}),
    6524: (EN + "; " + LIST, {"t_ru": "впереди, спереди", "t_uk": "попереду, спереду", "t_en": "at the front, in front",
                              "t_tr": "önde", "t_pl": "z przodu", "x_ru": "Я сижу в автобусе впереди",
                              "x_en": "I'm sitting at the front of the bus",
                              "x_it": "Sono seduto davanti sull'autobus"}),
    6528: (LIST + "; es/fr — книжно", {
        "t_ru": "в обрез, едва", "t_uk": "обмаль, ледве", "t_en": "tight, barely", "t_tr": "az, kıt",
        "t_pl": "skąpy, ledwie", "t_it": "scarso, appena", "t_es": "justo, apenas", "t_fr": "juste, à peine",
        "t_cs": "málo, sotva", "x_es": "Vamos justos de dinero", "x_fr": "On est un peu juste en ce moment"}),
    2432: (LIST + "; «Ich brauche eine Erlaubnis» — пусто", {
        "t_ru": "разрешение", "t_uk": "дозвіл", "t_en": "permission", "t_tr": "izin", "t_pl": "pozwolenie, zgoda",
        **all_x("Hast du die Erlaubnis von deinen Eltern?", "У тебя есть разрешение от родителей?",
                "У тебе є дозвіл від батьків?", "Do you have your parents' permission?", "Ailenden izin aldın mı?",
                "Masz pozwolenie od rodziców?", "Hai il permesso dei tuoi genitori?", "¿Tienes permiso de tus padres?",
                "Tu as la permission de tes parents?", "Máš od rodičů svolení?")}),
    2216: (LIST, {"t_ru": "открывать", "t_uk": "відкривати, відчиняти", "t_en": "to open", "t_tr": "açmak",
                  "t_pl": "otwierać"}),
    2130: (EN + " («most recently»); " + LIST, {
        "t_ru": "в последний раз, в конце", "t_uk": "востаннє, наостанок", "t_en": "last, in the end",
        "t_tr": "en son, sonunda", "t_pl": "ostatnio, na końcu", "t_it": "l'ultima volta, alla fine",
        "t_es": "la última vez, al final", "t_fr": "la dernière fois, en dernier", "t_cs": "naposledy, nakonec",
        "x_en": "When were you last here?"}),
    14946: (LIST, {"t_en": "cousin", "t_tr": "kuzen"}),
    15404: ("«Wir wandern auf den Berg» — у Berg десятки похожих примеров; «куча» — другое значение", {
        "t_ru": "гора", "t_uk": "гора", "t_en": "mountain", "t_tr": "dağ", "t_pl": "góra",
        **all_x("Im Urlaub fahren wir in die Berge", "В отпуск мы едем в горы", "У відпустку ми їдемо в гори",
                "We're going to the mountains on holiday", "Tatilde dağlara gidiyoruz", "Na urlop jedziemy w góry",
                "In vacanza andiamo in montagna", "En vacaciones nos vamos a la montaña",
                "En vacances, on va à la montagne", "Na dovolenou jedeme na hory")}),
    17914: (LIST, {"t_uk": "відсоток", "t_en": "percent", "t_tr": "yüzde"}),
    13459: (LIST, {"t_uk": "кілька", "t_en": "several", "t_tr": "birkaç", "t_pl": "kilka",
                   "x_en": "I've read several books"}),
    292: (SKEL + "; " + LIST, {
        "t_ru": "свежий, прохладный", "t_uk": "свіжий, прохолодний", "t_en": "fresh", "t_tr": "taze", "t_pl": "świeży",
        **all_x("Die Brötchen sind ganz frisch vom Bäcker", "Булочки совсем свежие, из пекарни",
                "Булочки зовсім свіжі, з пекарні", "The rolls are fresh from the bakery", "Ekmekler fırından taptaze geldi",
                "Bułki są świeżutkie, prosto z piekarni", "I panini sono freschissimi, appena presi dal fornaio",
                "Los panecillos están frescos, recién comprados en la panadería",
                "Les petits pains sont tout frais, de la boulangerie", "Rohlíky jsou čerstvé z pekárny")}),
    3: (EN, {"x_en": "I study German in the evenings"}),
    10182: (LIST, {"t_ru": "свободный, расслабленный", "t_uk": "вільний, розслаблений", "t_en": "loose, relaxed",
                   "t_tr": "gevşek, rahat", "t_pl": "luźny, wyluzowany", "t_it": "allentato, rilassato",
                   "t_es": "flojo, relajado", "t_fr": "desserré, détendu", "t_cs": "uvolněný, volný"}),
    2950: (LIST, {"t_ru": "поранить, обидеть", "t_uk": "поранити, образити", "t_en": "to injure, to hurt",
                  "t_tr": "yaralamak, incitmek", "t_pl": "zranić, urazić", "t_it": "ferire, offendere",
                  "t_es": "herir, lesionar", "t_fr": "blesser, vexer", "t_cs": "zranit, urazit"}),
    17915: (LIST + "; «Врач должен» — калька с muss", {
        "t_ru": "обследовать, осматривать", "t_uk": "обстежувати, оглядати", "t_en": "to examine, to investigate",
        "t_tr": "muayene etmek, incelemek", "t_pl": "badać", "t_it": "visitare, esaminare",
        "t_es": "examinar, investigar", "t_fr": "examiner, étudier", "t_cs": "vyšetřit, zkoumat",
        "x_ru": "Врачу нужно меня осмотреть", "x_uk": "Лікар має мене оглянути"}),
    6537: ("«Danke, ebenfalls!» — так слово и живёт в речи; " + LIST, {
        "t_ru": "тоже, взаимно", "t_uk": "також, взаємно", "t_en": "too, likewise", "t_tr": "de, aynı şekilde",
        "t_pl": "również, nawzajem", "t_it": "anche, altrettanto", "t_es": "también, igualmente",
        "t_fr": "également, pareillement", "t_cs": "také, nápodobně",
        **all_x("Danke, ebenfalls!", "Спасибо, взаимно!", "Дякую, взаємно!", "Thanks, you too!",
                "Teşekkürler, size de!", "Dziękuję, nawzajem!", "Grazie, altrettanto!", "¡Gracias, igualmente!",
                "Merci, pareillement!", "Děkuji, nápodobně!")}),
    17488: ("«Мотор моей машины сломан» — калька", {"x_ru": "У моей машины сломался мотор",
                                                  "x_uk": "У моїй машині зламався мотор"}),
    12110: (LIST, {"t_ru": "прыгать", "t_uk": "стрибати", "t_en": "to jump", "t_tr": "zıplamak, atlamak",
                   "t_pl": "skakać", "t_cs": "skákat, skočit"}),
    731: (LIST, {"t_ru": "пробовать, примерять", "t_uk": "пробувати, куштувати", "t_en": "to try, to taste",
                 "t_tr": "denemek, tadına bakmak", "t_pl": "próbować, kosztować"}),
    692: (LIST + "; «Я пакую чемодан» — калька", {
        "t_ru": "паковать, собирать вещи", "t_uk": "пакувати, збирати речі", "t_en": "to pack, to grab",
        "t_tr": "paketlemek, bavul hazırlamak", "t_pl": "pakować", "t_it": "fare la valigia, impacchettare",
        "t_es": "hacer la maleta, empaquetar", "t_fr": "faire sa valise, emballer", "t_cs": "balit, sbalit",
        **all_x("Hast du deinen Koffer schon gepackt?", "Ты уже собрал чемодан?", "Ти вже зібрав валізу?",
                "Have you packed your suitcase yet?", "Bavulunu hazırladın mı?", "Spakowałeś już walizkę?",
                "Hai già fatto la valigia?", "¿Ya has hecho la maleta?", "Tu as déjà fait ta valise?",
                "Už sis sbalil kufr?")}),
    13895: (TWO + " (артикль — грамматика, своя строка)", {
        "t_ru": "статья, товар", "t_uk": "стаття, товар", "t_en": "article, item", "t_tr": "makale, ürün",
        "t_pl": "artykuł, towar", "t_it": "l'articolo", "t_es": "el artículo", "t_fr": "l'article",
        "t_cs": "článek, zboží"}),
    1031: ("«Der Westen liegt 500 km von hier» — смысла нет", {**all_x(
        "Die Sonne geht im Westen unter", "Солнце садится на западе", "Сонце сідає на заході",
        "The sun sets in the west", "Güneş batıdan batar", "Słońce zachodzi na zachodzie",
        "Il sole tramonta a ovest", "El sol se pone por el oeste", "Le soleil se couche à l'ouest",
        "Slunce zapadá na západě")}),
    13461: (RAIN + "; " + LIST, {
        "t_ru": "однако, но", "t_uk": "однак, проте", "t_en": "however, but", "t_tr": "ancak, fakat",
        "t_pl": "jednak", "t_it": "però, tuttavia", "t_es": "sin embargo, pero", "t_fr": "cependant, mais",
        "t_cs": "však, ale",
        **all_x("Das Hotel war teuer, jedoch sehr schön", "Отель был дорогой, однако очень хороший",
                "Готель був дорогий, однак дуже гарний", "The hotel was expensive, but very nice",
                "Otel pahalıydı ama çok güzeldi", "Hotel był drogi, jednak bardzo ładny",
                "L'albergo era caro, però molto bello", "El hotel era caro, pero muy bonito",
                "L'hôtel était cher, mais très beau", "Hotel byl drahý, ale velmi pěkný")}),
}

# Письменное → разговорное: немцу учить то, что он услышит
REPLACE = [
    {"id": 13461, "by": 4, "lang": "de", "why": "jedoch — письменное, в речи aber"},
    {"id": 2364, "by": 326, "lang": "de", "why": "ebenso — письменное, в речи genauso"},
]

SPLIT_LATER = {
    1947: ["das Theater = шумиха (Mach kein Theater!)"],
    14382: ["der Star = скворец"],
    13895: ["der Artikel = артикль"],
}
