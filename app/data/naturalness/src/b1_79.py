"""B1, блок 79: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    11884: ("«Ich habe mir gestern eine Dose Sardinen gekauft» — пусто; en «can» — американское", {**all_x(
        "Im Urlaub haben wir frische Sardinen gegrillt", "В отпуске мы жарили на гриле свежие сардины",
        "У відпустці ми смажили на грилі свіжі сардини", "On holiday we grilled fresh sardines",
        "Tatilde taze sardalya ızgara yaptık", "Na wakacjach grillowaliśmy świeże sardynki",
        "In vacanza abbiamo grigliato sardine fresche", "En vacaciones hicimos sardinas frescas a la plancha",
        "En vacances, on a grillé des sardines fraîches", "Na dovolené jsme grilovali čerstvé sardinky")}),
    7969: ("«Das alte Fahrrad …» — шаблон «altes Fahrrad»; " + LIST, {
        "t_ru": "непригодный, бесполезный", "t_uk": "непридатний, непотрібний", "t_pl": "bezużyteczny, nieprzydatny",
        "t_cs": "nepoužitelný, k ničemu",
        **all_x("Ohne Akku ist das Handy völlig unbrauchbar", "Без аккумулятора телефон совершенно бесполезен",
                "Без акумулятора телефон зовсім непотрібний", "Without a battery the phone is completely useless",
                "Bataryasız telefon tamamen işe yaramaz", "Bez baterii telefon jest zupełnie bezużyteczny",
                "Senza batteria il telefono è del tutto inutilizzabile", "Sin batería el móvil es totalmente inútil",
                "Sans batterie, le portable est complètement inutilisable", "Bez baterie je mobil úplně k ničemu")}),
    11134: ("«Das mysteriöse Buch hat mich fasziniert» — аннотация", {**all_x(
        "Mein Schlüssel ist auf mysteriöse Weise verschwunden", "Мой ключ таинственным образом исчез",
        "Мій ключ таємничим чином зник", "My key has disappeared in a mysterious way",
        "Anahtarım gizemli bir şekilde kayboldu", "Mój klucz zniknął w tajemniczy sposób",
        "La mia chiave è sparita in modo misterioso", "Mi llave ha desaparecido de forma misteriosa",
        "Ma clé a disparu de façon mystérieuse", "Můj klíč záhadně zmizel")}),
    7970: ("«Das war ein Schnäppchen» — пусто; " + LIST, {
        "t_ru": "выгодная покупка, удачная сделка", "t_en": "bargain", "t_tr": "kelepir, fırsat", "t_pl": "okazja",
        "t_it": "l'affare", "t_es": "la ganga", "t_fr": "la bonne affaire", "t_cs": "výhodná koupě",
        **all_x("Die Jacke war ein echtes Schnäppchen, nur 20 Euro!", "Куртка была настоящей выгодной покупкой, всего 20 евро!",
                "Куртка була справжньою вигідною покупкою, лише 20 євро!", "The jacket was a real bargain, only 20 euros!",
                "Ceket tam bir kelepirdi, sadece 20 euro!", "Kurtka to była prawdziwa okazja, tylko 20 euro!",
                "La giacca è stata un vero affare, solo 20 euro!", "La chaqueta fue una ganga, ¡solo 20 euros!",
                "La veste était une vraie bonne affaire, seulement 20 euros!", "Ta bunda byla opravdu výhodná koupě, jen 20 eur!")}),
    9110: ("пометка (hovor.); en «mail carrier» — американское; пример — справка", {
        "t_en": "postman", "t_cs": "listonoš, pošťák",
        **all_x("War der Briefträger heute schon da?", "Почтальон сегодня уже приходил?", "Листоноша сьогодні вже приходив?",
                "Has the postman been yet today?", "Postacı bugün geldi mi?", "Listonosz już dziś był?",
                "Il postino è già passato oggi?", "¿Ha pasado ya hoy el cartero?", "Le facteur est déjà passé aujourd'hui?",
                "Byl už dneska listonoš?")}),
    9111: ("«… ein neues Buch über die Antike geschrieben» — аннотация", {**all_x(
        "Historiker streiten sich bis heute darüber", "Историки спорят об этом до сих пор", "Історики сперечаються про це досі",
        "Historians are still arguing about it today", "Tarihçiler bugün hâlâ bunu tartışıyor", "Historycy do dziś się o to spierają",
        "Gli storici ne discutono ancora oggi", "Los historiadores todavía discuten sobre eso",
        "Les historiens en débattent encore aujourd'hui", "Historici se o tom přou dodnes")}),
    18361: ("пример повторяет Klopapier", {
        "t_en": "toilet paper, toilet roll",
        **all_x("Es ist kein Toilettenpapier mehr da!", "Туалетная бумага закончилась!", "Туалетний папір закінчився!",
                "There's no toilet paper left!", "Tuvalet kağıdı kalmamış!", "Nie ma już papieru toaletowego!",
                "Non c'è più carta igienica!", "¡No queda papel higiénico!", "Il n'y a plus de papier toilette!",
                "Došel toaletní papír!")}),
    9886: (EN + "; " + LIST, {
        "t_ru": "рыночная площадь", "t_uk": "ринкова площа", "t_en": "market square", "t_tr": "pazar yeri", "t_pl": "rynek",
        "t_it": "la piazza del mercato", "t_es": "la plaza del mercado", "t_fr": "la place du marché",
        "t_cs": "tržiště, tržní náměstí", "x_en": "In the market square, farmers sell their fresh vegetables"}),
    11136: (LIST, {"t_ru": "суматошный, нервный", "t_uk": "гарячковий, напружений", "t_en": "hectic", "t_tr": "telaşlı",
                   "t_pl": "gorączkowy, nerwowy", "t_it": "frenetico, agitato", "t_es": "ajetreado, frenético",
                   "t_fr": "agité, trépidant", "t_cs": "hektický, uspěchaný"}),
    7976: ("«Die Grenzen zwischen Traum und Wirklichkeit …» — книжно; " + LIST, {
        "t_ru": "размытый, смазанный", "t_uk": "розмитий, змазаний", "t_en": "smudged, blurred", "t_tr": "silinmiş, bulanık",
        "t_pl": "zamazany, rozmyty", "t_it": "sbavato, sfumato", "t_es": "corrido, borroso", "t_fr": "brouillé, flou",
        "t_cs": "rozmazaný, setřený",
        **all_x("Die Schrift ist ganz verwischt, ich kann nichts lesen", "Надпись совсем размыта, ничего не прочитать",
                "Напис зовсім розмитий, нічого не прочитати", "The writing is all smudged, I can't read anything",
                "Yazı tamamen silinmiş, hiçbir şey okuyamıyorum", "Pismo jest całe zamazane, nic nie mogę przeczytać",
                "La scritta è tutta sbavata, non riesco a leggere niente", "La letra está toda corrida, no puedo leer nada",
                "L'écriture est toute brouillée, je n'arrive à rien lire", "Písmo je celé rozmazané, nic nepřečtu")}),
    3026: ("«… muss gereinigt werden» — инструкция; en «windshield» — американское", {
        "t_en": "windscreen", "t_pl": "przednia szyba",
        **all_x("Ein Stein hat die Windschutzscheibe getroffen", "Камень попал в лобовое стекло", "Камінь влучив у лобове скло",
                "A stone has hit the windscreen", "Ön cama bir taş çarptı", "Kamień uderzył w przednią szybę",
                "Un sasso ha colpito il parabrezza", "Una piedra ha golpeado el parabrisas", "Un caillou a touché le pare-brise",
                "Do čelního skla narazil kámen")}),
    14207: (LIST, {"t_ru": "привет, здравствуйте", "t_uk": "привіт, вітаю", "t_en": "hi, morning", "t_tr": "merhaba, selam",
                   "t_pl": "cześć, dzień dobry", "t_it": "ciao, salve", "t_es": "hola, buenas", "t_fr": "salut, bonjour",
                   "t_cs": "ahoj, dobrý den"}),
    1370: ("«Ich kaufe Elektronik online» — пусто; " + LIST, {
        "t_ru": "электроника", "t_uk": "електроніка", "t_tr": "elektronik", "t_pl": "elektronika",
        **all_x("Mit Elektronik kenne ich mich leider nicht aus", "В электронике я, к сожалению, не разбираюсь",
                "В електроніці я, на жаль, не розбираюся", "I'm afraid I don't know anything about electronics",
                "Maalesef elektronikten anlamam", "Niestety nie znam się na elektronice",
                "Purtroppo di elettronica non me ne intendo", "Por desgracia no entiendo de electrónica",
                "Malheureusement, je n'y connais rien en électronique", "Bohužel se v elektronice nevyznám")}),
    11885: ("«… ist sehr nahrhaft und schmeckt dem Hund» — реклама; " + LIST, {
        "t_ru": "корм для собак", "t_uk": "корм для собак", "t_en": "dog food", "t_tr": "köpek maması", "t_pl": "karma dla psa",
        "t_es": "la comida para perros", "t_fr": "la nourriture pour chiens", "t_cs": "krmivo pro psy",
        **all_x("Kannst du auf dem Heimweg Hundefutter mitbringen?", "Можешь по дороге домой купить корм для собак?",
                "Можеш дорогою додому купити корм для собак?", "Could you pick up some dog food on your way home?",
                "Eve gelirken köpek maması alabilir misin?", "Możesz w drodze do domu kupić karmę dla psa?",
                "Puoi prendere il cibo per cani tornando a casa?", "¿Puedes traer comida para perros de camino a casa?",
                "Tu peux ramener de la nourriture pour chiens en rentrant?", "Můžeš cestou domů koupit krmivo pro psy?")}),
    11886: ("«… mega süß und saftig» — шаблон", {
        "t_es": "el melocotón",
        **all_x("Die Pfirsiche sind noch hart, die müssen noch reifen", "Персики ещё твёрдые, им надо дозреть",
                "Персики ще тверді, їм треба дозріти", "The peaches are still hard, they need to ripen",
                "Şeftaliler hâlâ sert, olgunlaşmaları lazım", "Brzoskwinie są jeszcze twarde, muszą dojrzeć",
                "Le pesche sono ancora dure, devono maturare", "Los melocotones todavía están duros, tienen que madurar",
                "Les pêches sont encore dures, elles doivent mûrir", "Broskve jsou ještě tvrdé, musí dozrát")}),
    12312: ("«… groß und sehr erfrischend» — реклама отеля; " + LIST, {
        "t_es": "la piscina",
        **all_x("Unsere Nachbarn haben einen Swimmingpool im Garten", "У наших соседей в саду бассейн", "У наших сусідів у саду басейн",
                "Our neighbours have a swimming pool in the garden", "Komşularımızın bahçesinde yüzme havuzu var",
                "Nasi sąsiedzi mają basen w ogrodzie", "I nostri vicini hanno una piscina in giardino",
                "Nuestros vecinos tienen piscina en el jardín", "Nos voisins ont une piscine dans le jardin",
                "Naši sousedé mají na zahradě bazén")}),
    2452: ("«Ich färbe mir die Haare» — пусто; " + LIST, {
        "t_ru": "красить, окрашивать", "t_uk": "фарбувати, забарвлювати", "t_en": "to dye, to colour", "t_tr": "boyamak",
        "t_pl": "farbować, barwić", "t_it": "tingere, colorare", "t_es": "teñir, colorear", "t_fr": "teindre, colorer",
        "t_cs": "barvit, obarvit",
        **all_x("Die rote Socke hat die ganze Wäsche rosa gefärbt", "Красный носок окрасил всё бельё в розовый",
                "Червона шкарпетка пофарбувала всю білизну в рожевий", "The red sock has dyed all the washing pink",
                "Kırmızı çorap bütün çamaşırları pembeye boyadı", "Czerwona skarpetka zafarbowała całe pranie na różowo",
                "Il calzino rosso ha tinto di rosa tutto il bucato", "El calcetín rojo ha teñido de rosa toda la ropa",
                "La chaussette rouge a teint tout le linge en rose", "Červená ponožka obarvila celé prádlo na růžovo")}),
    1762: ("«Gib deine PIN ein» — повтор примера eingeben; " + LIST, {
        "t_ru": "ПИН-код", "t_uk": "ПІН-код", "t_en": "PIN", "t_tr": "PIN, şifre", "t_pl": "PIN", "t_it": "il PIN",
        "t_es": "el PIN", "t_fr": "le code PIN", "t_cs": "PIN",
        **all_x("Die PIN steht im Brief von der Bank", "ПИН-код указан в письме из банка", "ПІН-код вказаний у листі з банку",
                "The PIN is in the letter from the bank", "PIN, bankadan gelen mektupta yazıyor", "PIN jest w liście z banku",
                "Il PIN è nella lettera della banca", "El PIN viene en la carta del banco", "Le code PIN est dans la lettre de la banque",
                "PIN je v dopise z banky")}),
    7984: ("en «realize» — американское написание; pl — не то время; " + LIST, {
        "t_ru": "осознавать, осуществлять", "t_uk": "усвідомлювати, здійснювати", "t_en": "to realise, to carry out",
        "t_tr": "fark etmek, gerçekleştirmek", "t_pl": "uświadomić sobie, zrealizować", "t_it": "rendersi conto, realizzare",
        "t_es": "darse cuenta, realizar", "t_fr": "réaliser, se rendre compte", "t_cs": "uvědomit si, uskutečnit",
        "x_en": "Only now do I realise how important that was", "x_pl": "Dopiero teraz sobie uświadamiam, jakie to było ważne"}),
    13577: ("«Die Stadt hat zehntausend Einwohner» — справка", {**all_x(
        "Das Auto hat zehntausend Euro gekostet", "Машина стоила десять тысяч евро", "Машина коштувала десять тисяч євро",
        "The car cost ten thousand euros", "Araba on bin euro tuttu", "Samochód kosztował dziesięć tysięcy euro",
        "La macchina è costata diecimila euro", "El coche costó diez mil euros", "La voiture a coûté dix mille euros",
        "Auto stálo deset tisíc eur")}),
    9116: ("«Der Übersetzer half uns …» — претерит", {**all_x(
        "Für die Dokumente brauche ich einen vereidigten Übersetzer", "Для документов мне нужен присяжный переводчик",
        "Для документів мені потрібен присяжний перекладач", "I need a sworn translator for the documents",
        "Belgeler için yeminli bir tercüman lazım", "Do dokumentów potrzebuję tłumacza przysięgłego",
        "Per i documenti mi serve un traduttore giurato", "Para los documentos necesito un traductor jurado",
        "Pour les documents, il me faut un traducteur assermenté", "Na dokumenty potřebuju soudního překladatele")}),
    12896: (LIST, {"t_ru": "прописывать, выписывать", "t_uk": "прописувати, виписувати", "t_en": "to prescribe",
                   "t_tr": "reçete yazmak", "t_pl": "przepisać", "t_cs": "předepsat", "x_tr": "Doktor ona antibiyotik yazıyor"}),
    1368: ("«Ich möchte Eiswürfel in mein Getränk» — так не говорят", {**all_x(
        "Möchtest du Eiswürfel in die Cola?", "Положить тебе кубики льда в колу?", "Покласти тобі кубики льоду в колу?",
        "Do you want ice cubes in your cola?", "Kolana buz küpü ister misin?", "Chcesz kostki lodu do coli?",
        "Vuoi dei cubetti di ghiaccio nella coca?", "¿Quieres cubitos de hielo en la cola?", "Tu veux des glaçons dans ton coca?",
        "Chceš do coly kostky ledu?")}),
    14211: (EN, {"t_en": "woman's voice", "x_en": "I can hear a woman's voice in the hallway"}),
    9118: ("«Der Diplomat verhandelt mit der Regierung» — новости", {**all_x(
        "Er ist kein Diplomat, er sagt immer direkt, was er denkt", "Он не дипломат, всегда говорит прямо, что думает",
        "Він не дипломат, завжди каже прямо, що думає", "He's no diplomat, he always says exactly what he thinks",
        "O diplomat değil, her zaman ne düşünüyorsa açıkça söylüyor", "On nie jest dyplomatą, zawsze mówi wprost, co myśli",
        "Non è un diplomatico, dice sempre chiaramente quello che pensa", "No es ningún diplomático, siempre dice lo que piensa",
        "Ce n'est pas un diplomate, il dit toujours franchement ce qu'il pense", "Není žádný diplomat, vždycky řekne rovnou, co si myslí")}),
    7996: ("«Sie zeigte keine Emotion …» — претерит", {**all_x(
        "Bei Filmen zeigt er nie Emotionen", "Во время фильмов он никогда не показывает эмоций",
        "Під час фільмів він ніколи не показує емоцій", "He never shows any emotion during films",
        "Filmlerde hiç duygu göstermiyor", "Na filmach nigdy nie okazuje emocji", "Nei film non mostra mai emozioni",
        "Con las películas nunca muestra emociones", "Devant un film, il ne montre jamais d'émotion",
        "U filmů nikdy nedává najevo emoce")}),
    11891: ("en «I need a refreshment» — так не говорят; " + LIST, {
        "t_ru": "освежение, прохладительный напиток", "t_uk": "освіження, прохолодний напій", "t_en": "refreshment",
        "t_tr": "serinleme, serinletici içecek", "t_pl": "orzeźwienie", "t_it": "il rinfresco, la bevanda fresca",
        "t_es": "el refresco, el refrigerio", "t_fr": "le rafraîchissement", "t_cs": "osvěžení, občerstvení",
        **all_x("Zur Erfrischung springen wir in den See", "Чтобы освежиться, мы прыгаем в озеро", "Для освіження ми стрибаємо в озеро",
                "We jump in the lake for some refreshment", "Serinlemek için göle atlıyoruz", "Dla orzeźwienia skaczemy do jeziora",
                "Per rinfrescarci ci tuffiamo nel lago", "Para refrescarnos nos tiramos al lago",
                "Pour se rafraîchir, on saute dans le lac", "Pro osvěžení skočíme do jezera")}),
    2563: ("«… und unterstützt seine Freunde» — тавтология; " + LIST, {
        "t_ru": "отзывчивый, готовый помочь", "t_uk": "чуйний, готовий допомогти", "t_en": "helpful", "t_tr": "yardımsever",
        "t_pl": "pomocny, uczynny", "t_it": "disponibile", "t_es": "servicial, atento", "t_fr": "serviable", "t_cs": "ochotný, vstřícný",
        **all_x("Die Nachbarn hier sind alle sehr hilfsbereit", "Соседи здесь все очень отзывчивые", "Сусіди тут усі дуже чуйні",
                "The neighbours here are all very helpful", "Buradaki komşular hep çok yardımsever", "Sąsiedzi tutaj są bardzo pomocni",
                "I vicini qui sono tutti molto disponibili", "Los vecinos aquí son todos muy serviciales",
                "Ici, les voisins sont tous très serviables", "Sousedé jsou tady všichni velmi ochotní")}),
    13738: ("en «sneakers» — американское; " + LIST, {
        "t_ru": "кроссовок, кеды", "t_uk": "кросівок, кеди", "t_en": "trainer", "t_tr": "spor ayakkabı",
        "t_pl": "but sportowy, adidas", "t_it": "la scarpa da ginnastica", "t_es": "la zapatilla", "t_fr": "la basket, la chaussure de sport",
        "t_cs": "teniska, sportovní bota", "x_en": "I need new trainers for running"}),
    1680: ("«Meditation hilft mir beim Entspannen und Stressabbau» — реклама", {**all_x(
        "Jeden Morgen mache ich zehn Minuten Meditation", "Каждое утро я десять минут занимаюсь медитацией",
        "Щоранку я десять хвилин займаюся медитацією", "Every morning I do ten minutes of meditation",
        "Her sabah on dakika meditasyon yapıyorum", "Każdego ranka robię dziesięć minut medytacji",
        "Ogni mattina faccio dieci minuti di meditazione", "Cada mañana hago diez minutos de meditación",
        "Chaque matin, je fais dix minutes de méditation", "Každé ráno dělám deset minut meditace")}),
    3001: ("«Die Jacke ist wasserdicht» — этикетка; " + LIST, {
        "t_ru": "водонепроницаемый, непромокаемый", "t_uk": "водонепроникний, непромокальний", "t_en": "waterproof, watertight",
        "t_tr": "su geçirmez", "t_pl": "wodoodporny, nieprzemakalny", "t_it": "impermeabile", "t_es": "impermeable",
        "t_fr": "étanche, imperméable", "t_cs": "vodotěsný, nepromokavý",
        **all_x("Ist die Uhr wirklich wasserdicht?", "Эти часы действительно водонепроницаемые?", "Цей годинник справді водонепроникний?",
                "Is the watch really waterproof?", "Saat gerçekten su geçirmez mi?", "Czy ten zegarek jest naprawdę wodoodporny?",
                "L'orologio è davvero impermeabile?", "¿El reloj es realmente impermeable?", "La montre est vraiment étanche?",
                "Jsou ty hodinky opravdu vodotěsné?")}),
    17290: ("шаблон «… macht mir Spaß»", {**all_x(
        "Beim Autofahren telefoniert man nicht!", "Во время вождения по телефону не разговаривают!",
        "Під час водіння по телефону не розмовляють!", "You don't talk on the phone while driving!",
        "Araba kullanırken telefonla konuşulmaz!", "Podczas jazdy samochodem nie rozmawia się przez telefon!",
        "Durante la guida non si telefona!", "¡Durante la conducción no se habla por teléfono!",
        "Pendant la conduite, on ne téléphone pas!", "Při řízení auta se netelefonuje!")}),
    13740: ("«Sie schminkt sich jeden Morgen» — пусто; en «makeup» — американское; " + LIST, {
        "t_ru": "краситься, делать макияж", "t_uk": "фарбуватися, робити макіяж", "t_en": "to put on make-up, to make up",
        "t_tr": "makyaj yapmak", "t_pl": "malować się, umalować", "t_cs": "líčit se, nalíčit",
        **all_x("Für die Hochzeit lasse ich mich schminken", "На свадьбу мне сделают макияж", "На весілля мені зроблять макіяж",
                "I'm having my make-up done for the wedding", "Düğün için makyaj yaptıracağım", "Na wesele dam się umalować",
                "Per il matrimonio mi faccio truccare", "Para la boda me van a maquillar", "Pour le mariage, je me fais maquiller",
                "Na svatbu se nechám nalíčit")}),
    3002: ("«Der Wasserhahn … tropft» — повтор примера tropfen; en «faucet» — американское", {
        "t_en": "tap",
        **all_x("Mach den Wasserhahn zu, während du Zähne putzt", "Закрывай кран, пока чистишь зубы", "Закривай кран, поки чистиш зуби",
                "Turn the tap off while you brush your teeth", "Dişlerini fırçalarken musluğu kapat", "Zakręcaj kran, kiedy myjesz zęby",
                "Chiudi il rubinetto mentre ti lavi i denti", "Cierra el grifo mientras te lavas los dientes",
                "Ferme le robinet quand tu te brosses les dents", "Zavírej kohoutek, když si čistíš zuby")}),
    1296: ("«… eine Broschüre über die Reisen» — так не говорят; " + LIST, {
        "t_it": "l'opuscolo, la brochure", "t_fr": "la brochure, le dépliant", "t_cs": "brožura, prospekt",
        **all_x("Im Hotel liegt eine Broschüre mit allen Ausflügen", "В отеле лежит брошюра со всеми экскурсиями",
                "У готелі лежить брошура з усіма екскурсіями", "There's a brochure with all the excursions at the hotel",
                "Otelde tüm geziler hakkında bir broşür var", "W hotelu leży broszura ze wszystkimi wycieczkami",
                "In albergo c'è un opuscolo con tutte le escursioni", "En el hotel hay un folleto con todas las excursiones",
                "À l'hôtel, il y a une brochure avec toutes les excursions", "V hotelu leží brožura se všemi výlety")}),
    2047: ("«Die Verpackung ist recyclebar» — надпись на упаковке; " + LIST, {
        "t_ru": "упаковка", "t_uk": "упаковка", "t_en": "packaging", "t_tr": "ambalaj", "t_pl": "opakowanie",
        "t_it": "la confezione, l'imballaggio", "t_es": "el envase, el embalaje", "t_fr": "l'emballage", "t_cs": "obal, balení",
        **all_x("Die Verpackung ist größer als das Produkt!", "Упаковка больше, чем сам товар!", "Упаковка більша, ніж сам товар!",
                "The packaging is bigger than the product!", "Ambalaj üründen büyük!", "Opakowanie jest większe niż produkt!",
                "La confezione è più grande del prodotto!", "¡El envase es más grande que el producto!",
                "L'emballage est plus grand que le produit!", "Obal je větší než výrobek!")}),
    14213: (EN + " («use informal you»); " + LIST, {
        "t_ru": "обращаться на ты", "t_uk": "звертатися на ти", "t_en": "to be on first-name terms", "t_tr": "sen diye hitap etmek",
        "t_pl": "mówić sobie na ty", "t_it": "dare del tu, darsi del tu", "t_es": "tutear, tutearse", "t_fr": "tutoyer, se tutoyer",
        "t_cs": "tykat, tykat si",
        "x_en": "Shall we be on first-name terms, or would you rather keep it formal?",
        "x_tr": "Birbirimize sen diye hitap edebilir miyiz, yoksa resmi mi kalalım?"}),
    11894: ("«Mein Spinat wächst schnell im Garten» — так не говорят", {**all_x(
        "Kinder mögen oft keinen Spinat", "Дети часто не любят шпинат", "Діти часто не люблять шпинат",
        "Kids often don't like spinach", "Çocuklar genelde ıspanak sevmez", "Dzieci często nie lubią szpinaku",
        "Spesso ai bambini non piacciono gli spinaci", "A los niños muchas veces no les gustan las espinacas",
        "Souvent, les enfants n'aiment pas les épinards", "Děti často nemají rády špenát")}),
}

SPLIT_LATER = {}
