"""B1, блок 72: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    9542: ("«Der Lehrer schreibt mit Kreide …» — учебник", {
        "t_es": "la tiza",
        **all_x("Die Kinder malen mit Kreide auf den Gehweg", "Дети рисуют мелом на тротуаре", "Діти малюють крейдою на тротуарі",
                "The kids are drawing on the pavement with chalk", "Çocuklar kaldırıma tebeşirle resim çiziyor",
                "Dzieci rysują kredą po chodniku", "I bambini disegnano col gesso sul marciapiede",
                "Los niños pintan con tiza en la acera", "Les enfants dessinent à la craie sur le trottoir",
                "Děti kreslí křídou na chodník")}),
    15152: ("ru «Мы должны» — калька; " + LIST, {
        "t_ru": "ближний, окружающие", "t_uk": "ближній, інші люди", "t_en": "fellow human being",
        "t_tr": "etrafımızdaki insan", "t_pl": "bliźni", "t_it": "il prossimo", "t_es": "el prójimo",
        "t_fr": "le semblable, le prochain",
        "x_ru": "Нужно с уважением относиться к окружающим", "x_uk": "Треба з повагою ставитися до ближніх"}),
    13563: ("«Wir gehen aufm Fest tanzen» — неверно (aufm = auf dem, тут нужно aufs)", {
        "t_en": "on the", "t_tr": "üstünde", "t_it": "sul, sulla", "t_es": "en el, en la", "t_fr": "sur le, sur la",
        **all_x("Das Handy liegt aufm Tisch", "Телефон лежит на столе", "Телефон лежить на столі", "The phone's on the table",
                "Telefon masanın üstünde", "Telefon leży na stole", "Il telefono è sul tavolo", "El móvil está en la mesa",
                "Le portable est sur la table", "Mobil leží na stole")}),
    2017: ("«Ich habe eine Urkunde bekommen» — пусто; " + LIST, {
        "t_ru": "документ, грамота", "t_uk": "документ, грамота", "t_en": "certificate, document", "t_tr": "belge, sertifika",
        "t_pl": "dokument, dyplom", "t_it": "il certificato, l'attestato", "t_es": "el certificado, el diploma",
        "t_fr": "le certificat, le diplôme", "t_cs": "listina, diplom",
        **all_x("Nach dem Lauf hat jedes Kind eine Urkunde bekommen", "После забега каждый ребёнок получил грамоту",
                "Після забігу кожна дитина отримала грамоту", "After the race every child got a certificate",
                "Koşudan sonra her çocuk bir sertifika aldı", "Po biegu każde dziecko dostało dyplom",
                "Dopo la corsa ogni bambino ha ricevuto un attestato", "Después de la carrera cada niño recibió un diploma",
                "Après la course, chaque enfant a reçu un diplôme", "Po závodě dostalo každé dítě diplom")}),
    11837: ("«Er saß an der Theke und bestellte ein Bier» — претерит, повтор примера Tresen; " + LIST, {
        "t_ru": "стойка, прилавок", "t_uk": "стійка, прилавок", "t_en": "counter, bar", "t_tr": "tezgah", "t_pl": "lada, bar",
        "t_es": "el mostrador, la barra", "t_cs": "pult, bar",
        **all_x("An der Theke kann man auch Kuchen zum Mitnehmen kaufen", "За стойкой можно купить и пирог навынос",
                "Біля стійки можна купити й пиріг із собою", "You can also buy cake to take away at the counter",
                "Tezgahtan paket kek de alabilirsiniz", "Przy ladzie można też kupić ciasto na wynos",
                "Al bancone si può comprare anche la torta da portare via",
                "En el mostrador también se puede comprar tarta para llevar",
                "Au comptoir, on peut aussi acheter du gâteau à emporter", "U pultu si můžete koupit i dort s sebou")}),
    13717: ("«Sie trägt einen blauen Bikini am Strand» — каталог одежды", {
        "t_ru": "бикини", "t_uk": "бікіні", "t_fr": "le bikini", "t_cs": "bikiny",
        **all_x("Pack deinen Bikini ein, wir gehen schwimmen!", "Возьми бикини, мы идём купаться!", "Візьми бікіні, ми йдемо купатися!",
                "Pack your bikini, we're going swimming!", "Bikinini al, yüzmeye gidiyoruz!", "Spakuj bikini, idziemy pływać!",
                "Prendi il bikini, andiamo a nuotare!", "¡Coge el bikini, que vamos a nadar!", "Prends ton bikini, on va se baigner!",
                "Vezmi si bikiny, jdeme se koupat!")}),
    2855: ("«Das Auto steht am Straßenrand» — пусто; en «curb» — американское", {
        "t_en": "roadside, side of the road",
        **all_x("Fahr mal kurz an den Straßenrand, mir ist schlecht", "Прижмись к обочине, меня тошнит",
                "Зупинись на узбіччі, мене нудить", "Pull over to the side of the road, I feel sick",
                "Yol kenarına çek, midem bulanıyor", "Zjedź na pobocze, niedobrze mi",
                "Accosta sul ciglio della strada, mi viene da vomitare", "Para en el arcén, que me mareo",
                "Arrête-toi au bord de la route, j'ai mal au cœur", "Zastav na kraji silnice, je mi špatně")}),
    11838: ("пример длинный; en «ground meat» — американское", {
        "t_en": "mince, minced meat", "t_es": "la carne picada", "t_fr": "la viande hachée",
        **all_x("Für die Bolognese brauche ich noch ein Pfund Hackfleisch", "Для болоньезе мне нужно ещё полкило фарша",
                "Для болоньєзе мені ще треба пів кіло фаршу", "I need another half a kilo of mince for the bolognese",
                "Bolonez sos için yarım kilo kıyma daha lazım", "Do bolognese potrzebuję jeszcze pół kilo mięsa mielonego",
                "Per il ragù mi serve ancora mezzo chilo di macinato", "Para la boloñesa necesito medio kilo de carne picada",
                "Pour la bolognaise, il me faut encore une livre de viande hachée",
                "Na boloňskou omáčku potřebuju ještě půl kila mletého masa")}),
    17619: ("ru «номер телефона» — не тот; en «cell phone» — американское; " + LIST, {
        "t_ru": "номер мобильного", "t_uk": "номер мобільного", "t_en": "mobile number", "t_tr": "cep telefonu numarası",
        "t_pl": "numer komórki", "t_es": "el número de móvil", "t_cs": "číslo mobilu",
        **all_x("Gibst du mir deine Handynummer?", "Дашь мне свой номер мобильного?", "Даси мені свій номер мобільного?",
                "Will you give me your mobile number?", "Bana cep telefonu numaranı verir misin?", "Dasz mi swój numer komórki?",
                "Mi dai il tuo numero di cellulare?", "¿Me das tu número de móvil?", "Tu me donnes ton numéro de portable?",
                "Dáš mi svoje číslo mobilu?")}),
    13718: ("«Sie trägt eine rote Schürze in der Küche» — каталог", {
        "t_ru": "фартук", "t_uk": "фартух", "t_en": "apron", "t_tr": "önlük", "t_pl": "fartuch",
        **all_x("Zieh dir eine Schürze an, sonst machst du dich schmutzig", "Надень фартук, а то испачкаешься",
                "Вдягни фартух, а то забрудишся", "Put an apron on or you'll get dirty", "Önlük tak, yoksa kirleneceksin",
                "Załóż fartuch, bo się pobrudzisz", "Mettiti il grembiule, se no ti sporchi", "Ponte el delantal, que te vas a manchar",
                "Mets un tablier, sinon tu vas te salir", "Vezmi si zástěru, jinak se ušpiníš")}),
    13719: ("«Mein neuer Schlafanzug ist sehr bequem» — каталог; en «pajamas» — американское", {
        "t_en": "pyjamas", "t_es": "el pijama",
        **all_x("Er läuft den ganzen Sonntag im Schlafanzug herum", "Он всё воскресенье ходит в пижаме",
                "Він цілу неділю ходить у піжамі", "He wanders around in his pyjamas all Sunday",
                "Bütün pazar pijamayla dolaşıyor", "Całą niedzielę chodzi w piżamie", "Gira tutta la domenica in pigiama",
                "Se pasa todo el domingo en pijama", "Il traîne en pyjama tout le dimanche", "Celou neděli chodí v pyžamu")}),
    12269: ("en «on weekends» — американское; " + LIST, {
        "t_ru": "играть в покер, блефовать", "t_uk": "грати в покер, блефувати", "t_en": "to play poker, to bluff",
        "t_tr": "poker oynamak", "t_es": "jugar al póquer, arriesgar", "x_en": "We sometimes play poker at the weekend"}),
    12271: (LIST, {"t_ru": "видеоигра", "t_uk": "відеогра", "t_en": "video game"}),
    15653: (LIST, {"t_en": "cockroach"}),
    15654: ("пометка (coloq.)", {"t_es": "el insecto, el bicho", "t_pl": "owad"}),
    12273: ("«Wir campen diesen Sommer in den Bergen» — повтор примера zelten; " + LIST, {
        "t_ru": "отдыхать в кемпинге, жить в палатке", "t_pl": "biwakować, spać pod namiotem",
        **all_x("Campen mit Kindern ist günstiger als ein Hotel", "Отдыхать с детьми в кемпинге дешевле, чем в гостинице",
                "Відпочивати з дітьми в кемпінгу дешевше, ніж у готелі", "Camping with kids is cheaper than a hotel",
                "Çocuklarla kamp yapmak otelden daha ucuz", "Biwakowanie z dziećmi jest tańsze niż hotel",
                "Campeggiare con i bambini costa meno dell'albergo", "Ir de camping con niños sale más barato que un hotel",
                "Faire du camping avec des enfants, c'est moins cher que l'hôtel", "Kempovat s dětmi je levnější než hotel")}),
    9037: ("en «favorite» — американское; " + LIST, {
        "t_ru": "занятие, работа", "t_uk": "заняття, робота", "t_en": "activity, employment", "t_tr": "uğraş, iş",
        "t_pl": "zajęcie, zatrudnienie", "t_it": "l'occupazione, il passatempo", "t_es": "la ocupación, el empleo",
        "t_fr": "l'occupation, l'emploi", "t_cs": "činnost, zaměstnání",
        **all_x("Die Kinder brauchen im Urlaub eine Beschäftigung", "Детям на отдыхе нужно какое-то занятие",
                "Дітям на відпочинку потрібне якесь заняття", "The kids need some kind of activity on holiday",
                "Çocukların tatilde bir uğraşa ihtiyacı var", "Dzieci na wakacjach potrzebują jakiegoś zajęcia",
                "In vacanza i bambini hanno bisogno di un'occupazione", "En vacaciones los niños necesitan alguna ocupación",
                "En vacances, les enfants ont besoin d'une occupation", "Děti potřebují o prázdninách nějakou činnost")}),
    1985: ("«Hier ist eine Überwachungskamera» — табличка; " + LIST, {
        "t_ru": "камера наблюдения", "t_uk": "камера спостереження", "t_en": "security camera, CCTV camera",
        "t_pl": "kamera monitoringu", "t_es": "la cámara de vigilancia",
        **all_x("Die Überwachungskamera hat den Dieb gefilmt", "Камера наблюдения сняла вора", "Камера спостереження зняла злодія",
                "The security camera filmed the thief", "Güvenlik kamerası hırsızı kaydetti", "Kamera monitoringu nagrała złodzieja",
                "La telecamera di sorveglianza ha ripreso il ladro", "La cámara de vigilancia grabó al ladrón",
                "La caméra de surveillance a filmé le voleur", "Bezpečnostní kamera natočila zloděje")}),
    11840: ("en «groceries» — не то; " + LIST, {
        "t_ru": "замораживать, замёрзнуть", "t_uk": "заморозити, замерзнути", "t_en": "to freeze", "t_tr": "dondurmak, donmak",
        "t_pl": "zamrozić, zamarznąć", "t_fr": "congeler, geler", "t_cs": "zamrazit, zamrznout",
        **all_x("Den Rest vom Eintopf kann man gut einfrieren", "Остаток рагу можно спокойно заморозить",
                "Залишок рагу можна спокійно заморозити", "You can easily freeze the rest of the stew",
                "Güvecin kalanını rahatça dondurabilirsin", "Resztę gulaszu można spokojnie zamrozić",
                "Il resto dello stufato si può congelare tranquillamente", "El resto del guiso se puede congelar sin problema",
                "Le reste du ragoût se congèle très bien", "Zbytek polévky se dá klidně zamrazit")}),
    7712: (LIST, {"t_en": "to require, to call for", "t_tr": "gerektirmek", "t_pl": "wymagać", "t_fr": "demander, exiger"}),
    2732: ("«Das funktioniert problemlos» — пусто; " + LIST, {
        "t_ru": "без проблем, легко", "t_uk": "без проблем, легко", "t_en": "without any problems, easily",
        "t_tr": "sorunsuz, kolayca", "t_pl": "bez problemu, łatwo",
        **all_x("Mit dem Zug kommst du problemlos hin", "На поезде ты без проблем доберёшься", "Поїздом ти без проблем доберешся",
                "You can get there by train without any problems", "Trenle sorunsuz gidersin", "Pociągiem dojedziesz bez problemu",
                "Col treno ci arrivi senza problemi", "En tren llegas sin problemas", "En train, tu y arrives sans problème",
                "Vlakem se tam dostaneš bez problémů")}),
    9038: ("en «jeweler» — американское", {
        "t_en": "jeweller, jeweller's",
        **all_x("Ich bringe die Uhr zum Juwelier, die Batterie ist leer", "Я отнесу часы к ювелиру, батарейка села",
                "Я віднесу годинник до ювеліра, батарейка сіла", "I'm taking the watch to the jeweller's, the battery's dead",
                "Saati kuyumcuya götürüyorum, pili bitti", "Zaniosę zegarek do jubilera, padła bateria",
                "Porto l'orologio dal gioielliere, la pila è scarica", "Llevo el reloj a la joyería, se le ha acabado la pila",
                "J'apporte la montre chez le bijoutier, la pile est morte", "Nesu hodinky ke klenotníkovi, došla baterie")}),
    12274: ("«… unterhaltsam und lustig» — тавтология; en «movie» — американское; " + LIST, {
        "t_ru": "занимательный, развлекательный", "t_uk": "цікавий, розважальний", "t_en": "entertaining", "t_tr": "eğlenceli",
        "t_pl": "zabawny, rozrywkowy",
        **all_x("Das Buch ist leicht und unterhaltsam, genau richtig für den Urlaub", "Книга лёгкая и занимательная — как раз для отпуска",
                "Книжка легка й цікава — саме для відпустки", "The book is light and entertaining, perfect for a holiday",
                "Kitap hafif ve eğlenceli, tam tatillik", "Książka jest lekka i zabawna, w sam raz na urlop",
                "Il libro è leggero e divertente, perfetto per le vacanze",
                "El libro es ligero y entretenido, perfecto para las vacaciones",
                "Le livre est léger et divertissant, parfait pour les vacances", "Ta knížka je lehká a zábavná, akorát na dovolenou")}),
    7715: (LIST, {"t_ru": "вместе, рядом", "t_uk": "разом, поряд", "t_en": "together, side by side",
                  "t_tr": "bir arada, yan yana", "t_pl": "razem, obok siebie", "t_fr": "ensemble"}),
    15156: ("«Die Schwiegertochter meiner Mutter» — загадка, а не пример", {
        "t_ru": "невестка", "t_uk": "невістка", "t_tr": "gelin",
        **all_x("Unsere Schwiegertochter kommt aus Polen", "Наша невестка из Польши", "Наша невістка з Польщі",
                "Our daughter-in-law is from Poland", "Gelinimiz Polonyalı", "Nasza synowa pochodzi z Polski",
                "Nostra nuora è polacca", "Nuestra nuera es polaca", "Notre belle-fille vient de Pologne", "Naše snacha je z Polska")}),
    17241: ("en «sidewalk» — американское", {
        "t_en": "pavement", "t_es": "la acera", "x_en": "Don't walk in the road, stay on the pavement"}),
    9041: ("«Die Stewardess brachte mir einen Kaffee» — претерит", {
        "t_es": "la azafata",
        **all_x("Die Stewardess bringt gleich die Getränke", "Стюардесса сейчас принесёт напитки", "Стюардеса зараз принесе напої",
                "The flight attendant will bring the drinks in a minute", "Hostes birazdan içecekleri getirecek",
                "Stewardesa zaraz przyniesie napoje", "La hostess porta subito le bevande", "La azafata ahora trae las bebidas",
                "L'hôtesse de l'air va apporter les boissons", "Letuška hned přinese pití")}),
    9545: ("«Ein normaler Schultag beginnt um 8 Uhr» — справка", {
        "t_es": "el día de clase", "t_fr": "le jour d'école, la journée d'école",
        **all_x("Morgen ist der erste Schultag nach den Ferien", "Завтра первый школьный день после каникул",
                "Завтра перший шкільний день після канікул", "Tomorrow is the first school day after the holidays",
                "Yarın tatilden sonraki ilk okul günü", "Jutro pierwszy dzień szkolny po wakacjach",
                "Domani è il primo giorno di scuola dopo le vacanze",
                "Mañana es el primer día de clase después de las vacaciones",
                "Demain, c'est le premier jour d'école après les vacances", "Zítra je první školní den po prázdninách")}),
    14154: ("«Ich werde noch nachfragen» — пусто; " + LIST, {
        "t_ru": "уточнить, переспросить", "t_uk": "уточнити, перепитати", "t_en": "to ask, to check",
        "t_tr": "sormak, tekrar sormak", "t_pl": "dopytać, zapytać", "t_it": "informarsi, chiedere",
        "t_es": "preguntar, volver a preguntar", "t_fr": "demander, redemander", "t_cs": "zeptat se, doptat se",
        **all_x("Wenn du etwas nicht verstehst, frag einfach nach", "Если что-то непонятно, просто переспроси",
                "Якщо щось незрозуміло, просто перепитай", "If you don't understand something, just ask",
                "Bir şey anlamazsan tekrar sor", "Jak czegoś nie rozumiesz, po prostu dopytaj",
                "Se non capisci qualcosa, chiedi pure", "Si no entiendes algo, vuelve a preguntar",
                "Si tu ne comprends pas quelque chose, redemande", "Když něčemu nerozumíš, prostě se zeptej")}),
    2215: ("«Es kommen hohe Kosten auf uns zu» — это zukommen, не aufkommen; " + LIST, {
        "t_ru": "возникать, покрывать (расходы)", "t_uk": "виникати, покривати (витрати)", "t_en": "to arise, to cover (costs)",
        "t_tr": "ortaya çıkmak, karşılamak", "t_pl": "pojawiać się, pokrywać (koszty)", "t_it": "sorgere, farsi carico di",
        "t_es": "surgir, hacerse cargo de", "t_fr": "survenir, prendre en charge", "t_cs": "vzniknout, uhradit",
        **all_x("Für die Kosten kommen die Eltern auf", "Расходы покрывают родители", "Витрати покривають батьки",
                "The parents cover the costs", "Masrafları anne babası karşılıyor", "Koszty pokrywają rodzice",
                "Delle spese si fanno carico i genitori", "Los padres se hacen cargo de los gastos",
                "Ce sont les parents qui prennent en charge les frais", "Náklady uhradí rodiče")}),
    12275: ("pl «idę do sauny» — не то; шаблон «gerne»", {
        "t_ru": "сауна", "t_uk": "сауна",
        **all_x("Im Winter gehen wir jeden Freitag in die Sauna", "Зимой мы каждую пятницу ходим в сауну",
                "Узимку ми щоп'ятниці ходимо в сауну", "In winter we go to the sauna every Friday",
                "Kışın her cuma saunaya gidiyoruz", "Zimą w każdy piątek chodzimy do sauny",
                "D'inverno andiamo in sauna ogni venerdì", "En invierno vamos a la sauna todos los viernes",
                "En hiver, on va au sauna tous les vendredis", "V zimě chodíme každý pátek do sauny")}),
    15659: ("«Der Skorpion ist ein gefährliches Tier» — энциклопедия; в речи — знак зодиака", {
        "t_ru": "скорпион, Скорпион (знак)", "t_uk": "скорпіон, Скорпіон (знак)", "t_en": "scorpion, Scorpio",
        "t_pl": "skorpion, Skorpion (znak)", "t_it": "lo scorpione, Scorpione", "t_es": "el escorpión, Escorpio",
        "t_fr": "le scorpion, Scorpion", "t_cs": "štír, Štír",
        **all_x("Ich bin Skorpion", "Я Скорпион", "Я Скорпіон", "I'm a Scorpio", "Ben Akrep burcuyum", "Jestem Skorpionem",
                "Sono dello Scorpione", "Soy Escorpio", "Je suis Scorpion", "Jsem Štír")}),
    12276: ("pl — другое предложение; «echt rasant» — реклама", {**all_x(
        "Auf der Achterbahn wird mir immer schlecht", "На американских горках меня всегда тошнит",
        "На американських гірках мене завжди нудить", "I always feel sick on roller coasters",
        "Hız treninde hep midem bulanıyor", "Na kolejce górskiej zawsze robi mi się niedobrze",
        "Sulle montagne russe mi viene sempre la nausea", "En la montaña rusa siempre me mareo",
        "Dans les montagnes russes, j'ai toujours mal au cœur", "Na horské dráze je mi vždycky špatně")}),
    7725: ("pl — другое предложение; " + LIST, {
        "t_ru": "быстрый, шикарный", "t_uk": "швидкий, елегантний", "t_en": "quick, snazzy", "t_tr": "hızlı, şık",
        "t_pl": "szybki, elegancki", "t_it": "svelto, elegante", "t_es": "rápido, elegante", "t_fr": "rapide, chic",
        "t_cs": "rychlý, elegantní",
        **all_x("Das hast du aber flott gemacht!", "Ну ты быстро управился!", "Ну ти швидко впорався!", "That was quick of you!",
                "Ne kadar hızlı yaptın!", "Ale szybko to zrobiłeś!", "Sei stato proprio svelto!", "¡Qué rápido lo has hecho!",
                "Tu as été rapide!", "To jsi udělal rychle!")}),
    15158: ("ru «венчание» — только церковное; Trauung — и в загсе", {
        "t_ru": "бракосочетание, венчание", "x_ru": "Бракосочетание состоится через две недели",
        "x_en": "The wedding ceremony is in two weeks"}),
    12798: ("«Sie hat Bauchschmerzen» — пусто", {
        "t_ru": "боль в животе", "t_en": "stomach ache", "t_tr": "karın ağrısı", "t_es": "el dolor de barriga, el dolor de estómago",
        **all_x("Vom vielen Kuchen habe ich jetzt Bauchschmerzen", "От всего этого торта у меня теперь боль в животе",
                "Від усього цього торта в мене тепер біль у животі", "I've got a stomach ache from all that cake",
                "O kadar pastadan sonra karın ağrım var", "Od tego ciasta mam teraz ból brzucha",
                "Con tutta quella torta ora ho mal di pancia", "De tanta tarta ahora tengo dolor de barriga",
                "Avec tout ce gâteau, j'ai mal au ventre", "Z toho dortu mám teď bolest břicha")}),
    13720: ("en «vacation» — американское; " + LIST, {
        "t_ru": "купальник", "t_uk": "купальник", "t_en": "swimsuit", "t_tr": "mayo",
        "x_en": "I need a new swimsuit for the holiday"}),
    14157: ("«Der Zuhörer war ganz gefesselt …» — претерит, книжно; " + LIST, {
        "t_ru": "слушатель", "t_uk": "слухач", "t_en": "listener", "t_tr": "dinleyici",
        **all_x("Du bist ein guter Zuhörer", "Ты хороший слушатель", "Ти хороший слухач", "You're a good listener",
                "İyi bir dinleyicisin", "Jesteś dobrym słuchaczem", "Sei un buon ascoltatore", "Eres un buen oyente",
                "Tu es un bon auditeur", "Jsi dobrý posluchač")}),
}

SPLIT_LATER = {
    13563: ["aufm — разговорное слияние auf dem, а не слово; убрать из базы или вынести на C1 с пометкой «разг.»"],
}
