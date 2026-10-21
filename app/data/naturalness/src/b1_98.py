"""B1, блок 98: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    11991: (EN, {"x_en": "After dinner we have a liqueur"}),
    11992: ("шаблон «gerne»; en «jello» — американское", {
        "t_en": "jelly",
        **all_x("Zum Nachtisch gibt es grünen Wackelpudding mit Vanillesoße", "На десерт зелёное желе с ванильным соусом",
                "На десерт зелене желе з ванільним соусом", "For pudding there's green jelly with custard",
                "Tatlı olarak vanilya soslu yeşil jöle var", "Na deser jest zielona galaretka z sosem waniliowym",
                "Per dessert c'è la gelatina verde con la crema alla vaniglia", "De postre hay gelatina verde con salsa de vainilla",
                "En dessert, il y a de la gelée verte avec de la crème anglaise", "Jako dezert je zelené želé s vanilkovou omáčkou")}),
    13107: ("uk — порядок слов", {"x_uk": "Я сьогодні йду на педикюр"}),
    14799: (EN, {"x_en": "He plays the clarinet in the orchestra"}),
    15846: (LIST, {"t_ru": "дымка, испарения", "t_uk": "імла, випари", "t_en": "haze, mist", "t_tr": "pus, buğu",
                   "t_pl": "mgiełka, opary", "t_it": "la foschia, il vapore", "t_es": "la neblina, la bruma", "t_fr": "la brume, la vapeur",
                   "t_cs": "opar, výpary"}),
    2171: ("«… bietet mehr Platz» — реклама; " + LIST, {
        "t_ru": "пристройка, выращивание", "t_uk": "прибудова, вирощування", "t_en": "extension, cultivation",
        "t_tr": "ek bina, yetiştirme", "t_pl": "przybudówka, uprawa", "t_it": "l'ampliamento, la coltivazione",
        "t_es": "la ampliación, el cultivo", "t_fr": "l'extension, la culture",
        **all_x("Der Anbau ist im Sommer fertig, dann haben wir endlich ein Gästezimmer",
                "Пристройку закончат летом, и тогда у нас наконец будет гостевая комната",
                "Прибудову закінчать улітку, і тоді в нас нарешті буде гостьова кімната",
                "The extension will be finished in summer, then we'll finally have a guest room",
                "Ek bina yazın bitiyor, o zaman nihayet bir misafir odamız olacak",
                "Przybudówka będzie gotowa latem, wtedy wreszcie będziemy mieć pokój gościnny",
                "L'ampliamento sarà pronto in estate, e finalmente avremo una camera per gli ospiti",
                "La ampliación estará lista en verano y por fin tendremos un cuarto de invitados",
                "L'extension sera finie cet été, et on aura enfin une chambre d'amis",
                "Přístavba bude hotová v létě a pak budeme mít konečně pokoj pro hosty")}),
    15847: ("«Es gibt starken Hagel» — пусто", {**all_x(
        "Bei Hagel stellen wir das Auto in die Garage", "Когда идёт град, мы ставим машину в гараж",
        "Коли йде град, ми ставимо машину в гараж", "When there's hail we put the car in the garage",
        "Dolu yağınca arabayı garaja koyuyoruz", "Kiedy pada grad, wstawiamy samochód do garażu",
        "Quando c'è la grandine mettiamo la macchina in garage", "Cuando hay granizo metemos el coche en el garaje",
        "Quand il y a de la grêle, on met la voiture au garage", "Když padají kroupy, dáváme auto do garáže")}),
    11993: ("шаблон «gerne»; " + LIST, {
        "t_en": "pumpkin", "t_es": "la calabaza", "t_fr": "la citrouille",
        **all_x("An Halloween schnitzen die Kinder Gesichter in die Kürbisse", "На Хэллоуин дети вырезают на тыквах рожицы",
                "На Гелловін діти вирізають на гарбузах обличчя", "At Halloween the kids carve faces into the pumpkins",
                "Cadılar Bayramı'nda çocuklar balkabaklarına surat oyuyor", "Na Halloween dzieci wycinają w dyniach buzie",
                "Ad Halloween i bambini intagliano facce nelle zucche", "En Halloween los niños tallan caras en las calabazas",
                "À Halloween, les enfants sculptent des visages dans les citrouilles",
                "Na Halloween vyřezávají děti do dýní obličeje")}),
    9626: ("uk/en/tr — другой смысл; " + LIST, {
        "t_ru": "посмотреть в словаре, справиться", "t_uk": "подивитися у словнику", "t_en": "to look up", "t_tr": "sözlükte bakmak",
        "t_pl": "sprawdzić, zajrzeć", "t_cs": "vyhledat, podívat se",
        "x_uk": "Хвилинку, я швидко подивлюся це слово в словнику",
        "x_en": "Hang on, I'll just look the word up in the dictionary",
        "x_tr": "Bir dakika, kelimeye hemen sözlükte bakayım"}),
    11994: ("«… ist praktisch, aber teuer» — реклама", {**all_x(
        "Nimm bloß nichts aus der Minibar, das ist total teuer", "Только ничего не бери из мини-бара, там всё жутко дорого",
        "Тільки нічого не бери з мінібару, там усе страшенно дорого", "Don't take anything from the minibar, it's really expensive",
        "Sakın minibardan bir şey alma, çok pahalı", "Tylko nic nie bierz z minibaru, to strasznie drogie",
        "Non prendere niente dal minibar, costa un sacco", "No cojas nada del minibar, que es carísimo",
        "Ne prends surtout rien dans le minibar, c'est hyper cher", "Hlavně si nic neber z minibaru, je to strašně drahé")}),
    11995: ("«… ist ganz wichtig» — пусто; " + LIST + " (было четыре значения)", {
        "t_ru": "перекус, подкрепление", "t_uk": "перекус, підкріплення", "t_en": "snack, refreshment", "t_tr": "ara öğün, takviye",
        "t_pl": "przekąska, wzmocnienie", "t_it": "lo spuntino, il rafforzamento", "t_es": "el tentempié, el refrigerio",
        "t_fr": "l'en-cas, le renforcement", "t_cs": "posilnění, svačinka",
        **all_x("Nach der Wanderung brauchen wir erst mal eine Stärkung", "После похода нам сначала нужен перекус",
                "Після походу нам спочатку потрібен перекус", "After the hike we need a snack first",
                "Yürüyüşten sonra önce bir ara öğüne ihtiyacımız var", "Po wędrówce najpierw potrzebujemy przekąski",
                "Dopo l'escursione ci serve prima uno spuntino", "Después de la excursión primero necesitamos un tentempié",
                "Après la randonnée, il nous faut d'abord un en-cas", "Po túře potřebujeme nejdřív posilnění")}),
    8540: ("«Die Ketten rasseln in der Nacht» — из страшилки; " + LIST, {
        "t_ru": "греметь, дребезжать", "t_uk": "гриміти, деренчати", "t_en": "to rattle", "t_tr": "takırdamak", "t_pl": "grzechotać",
        "t_it": "sferragliare", "t_es": "traquetear", "t_fr": "ferrailler, cliqueter", "t_cs": "chrastit, řinčet",
        **all_x("Der alte Motor rasselt ganz schön laut", "Старый мотор гремит довольно громко", "Старий мотор гримить досить голосно",
                "The old engine rattles pretty loudly", "Eski motor epey gürültülü takırdıyor", "Stary silnik grzechocze dość głośno",
                "Il vecchio motore sferraglia parecchio", "El motor viejo traquetea bastante fuerte",
                "Le vieux moteur ferraille pas mal", "Starý motor dost hlasitě chrastí")}),
    8541: ("en «leg … goes to» — так не говорят; " + LIST, {
        "t_ru": "этап, отрезок пути", "t_uk": "етап, відрізок шляху", "t_en": "stage, leg", "t_tr": "etap, aşama",
        "t_pl": "etap, odcinek", "t_it": "la tappa", "t_es": "la etapa", "t_fr": "l'étape", "t_cs": "etapa, úsek",
        "x_en": "The next leg of our trip is Portugal"}),
    11996: ("«Ich siebe … durch ein Sieb» — повтор; " + LIST, {
        "t_ru": "сито, дуршлаг", "t_uk": "сито, друшляк", "t_en": "sieve, colander", "t_tr": "elek, süzgeç", "t_pl": "sito, durszlak",
        "t_it": "il colino, lo scolapasta", "t_es": "el colador, el tamiz", "t_fr": "la passoire, le tamis", "t_cs": "cedník, síto",
        **all_x("Gieß die Nudeln durch das Sieb ab", "Слей макароны через дуршлаг", "Злий макарони через друшляк",
                "Drain the pasta through the colander", "Makarnayı süzgeçten süz", "Odcedź makaron na durszlaku",
                "Scola la pasta nello scolapasta", "Escurre la pasta con el colador", "Égoutte les pâtes dans la passoire",
                "Sceď těstoviny přes cedník")}),
    13113: ("«Der Hautarzt entfernte …» — претерит", {
        "t_pl": "kurzajka, brodawka",
        **all_x("Gegen die Warze am Finger hilft leider keine Creme", "От бородавки на пальце, к сожалению, не помогает никакой крем",
                "Від бородавки на пальці, на жаль, не допомагає жоден крем",
                "Unfortunately no cream helps with the wart on my finger",
                "Parmağımdaki siğile maalesef hiçbir krem iyi gelmiyor", "Na kurzajkę na palcu niestety nie pomaga żaden krem",
                "Purtroppo per la verruca sul dito non serve nessuna crema",
                "Por desgracia, ninguna crema ayuda contra la verruga del dedo",
                "Malheureusement, aucune crème n'aide contre la verrue sur mon doigt",
                "Na bradavici na prstu bohužel nepomáhá žádný krém")}),
    18465: ("ru «диван имеет» — калька; " + LIST, {
        "t_ru": "обивка, подушка", "t_uk": "оббивка, подушка", "t_en": "upholstery, cushion", "t_tr": "döşeme, minder",
        "t_pl": "tapicerka, poduszka", "t_it": "l'imbottitura, il cuscino", "t_es": "el acolchado, el cojín",
        "t_fr": "le rembourrage, le coussin", "t_cs": "čalounění, polštář",
        "x_ru": "У дивана очень мягкая обивка", "x_uk": "У дивана дуже м'яка оббивка",
        "x_en": "The sofa has very soft upholstery"}),
    9254: ("uk «я повинен» — калька; en → британское «job centre»; " + LIST, {
        "t_ru": "служба занятости, биржа труда", "t_uk": "служба зайнятості, біржа праці", "t_en": "job centre",
        "t_tr": "iş kurumu", "t_pl": "urząd pracy", "t_it": "il centro per l'impiego, l'ufficio di collocamento",
        "x_uk": "Завтра мені треба піти в службу зайнятості, щоб зареєструватися",
        "x_en": "I have to go to the job centre tomorrow to register"}),
    8548: ("en «the latter I prefer» — порядок слов; " + LIST, {
        "t_ru": "последний из названных, второй", "t_uk": "останній з названих, другий", "t_en": "the latter", "t_tr": "sonuncusu",
        "t_pl": "to drugie", "t_it": "quest'ultimo", "t_es": "este último", "t_fr": "ce dernier", "t_cs": "ten druhý",
        "x_en": "I can choose between tea and coffee; I prefer the latter"}),
    12394: ("ru/uk «поддерживают» — слово не из перевода; " + LIST, {
        "t_ru": "подбадривать, разжигать", "t_uk": "підбадьорювати, розпалювати", "t_en": "to cheer on, to fire up",
        "t_tr": "tezahürat yapmak, desteklemek", "t_pl": "zagrzewać do walki, kibicować", "t_it": "incitare, fare il tifo per",
        "t_es": "animar, avivar", "t_fr": "encourager, attiser", "t_cs": "povzbuzovat, fandit",
        "x_ru": "Болельщики подбадривают свою команду во время матча",
        "x_uk": "Уболівальники підбадьорюють свою команду під час матчу"}),
    12395: ("en «on weekends» — американское; en потерял «oft»", {"x_en": "At weekends I often play golf"}),
    13117: ("«… erfolgte sofort nach der Diagnose» — канцелярит; " + LIST + " (было шесть значений)", {
        "t_ru": "инструктаж, направление в больницу", "t_uk": "інструктаж, скерування до лікарні", "t_en": "briefing, admission to hospital",
        "t_tr": "bilgilendirme, hastaneye yatırılma", "t_pl": "instruktaż, skierowanie do szpitala", "t_it": "la formazione, il ricovero",
        "t_es": "la formación, el ingreso", "t_fr": "la formation, l'admission", "t_cs": "zaškolení, přijetí",
        **all_x("Am ersten Tag bekommst du eine Einweisung an der Kasse", "В первый день тебе проведут инструктаж по работе на кассе",
                "Першого дня тобі проведуть інструктаж на касі", "On your first day you'll get a briefing on the till",
                "İlk gün kasada bir bilgilendirme alacaksın", "Pierwszego dnia dostaniesz instruktaż przy kasie",
                "Il primo giorno ti fanno una formazione alla cassa", "El primer día te dan una formación en la caja",
                "Le premier jour, tu as une formation à la caisse", "První den dostaneš zaškolení u pokladny")}),
    9256: ("en «on weekends» — американское", {
        "t_en": "to wait tables, to work as a waitress", "t_pl": "kelnerować, pracować jako kelner",
        "x_en": "She waits tables in a restaurant at the weekend"}),
    12001: ("pl — другой смысл; пометка (hovor.); " + LIST, {
        "t_ru": "постоянный посетитель, завсегдатай", "t_uk": "постійний відвідувач, завсідник", "t_en": "regular", "t_tr": "müdavim",
        "t_pl": "stały klient, bywalec", "t_it": "il cliente abituale", "t_es": "el cliente habitual", "t_fr": "l'habitué",
        "t_cs": "stálý host, štamgast", "x_pl": "Stały klient przychodzi codziennie do kawiarni na kawę"}),
    8554: ("«neue Mitarbeiter ins Team integrieren» — офисный канцелярит; " + LIST, {
        "t_ru": "интегрировать, вливаться", "t_uk": "інтегрувати, вливатися", "t_en": "to integrate, to fit in",
        "t_tr": "entegre etmek, uyum sağlamak", "t_pl": "integrować", "t_it": "integrare", "t_es": "integrar", "t_fr": "intégrer",
        "t_cs": "začlenit, integrovat",
        **all_x("Unser Sohn hat sich schnell in die neue Klasse integriert", "Наш сын быстро влился в новый класс",
                "Наш син швидко влився в новий клас", "Our son has quickly fitted in with his new class",
                "Oğlumuz yeni sınıfına çabucak uyum sağladı", "Nasz syn szybko zintegrował się z nową klasą",
                "Nostro figlio si è integrato subito nella nuova classe", "Nuestro hijo se ha integrado rápido en la nueva clase",
                "Notre fils s'est vite intégré dans sa nouvelle classe", "Náš syn se rychle začlenil do nové třídy")}),
    9943: ("«Die Smaragde … leuchteten» — претерит", {**all_x(
        "Ihre Augen sind grün wie Smaragde", "Её глаза зелёные, как изумруды", "Її очі зелені, як смарагди",
        "Her eyes are as green as emeralds", "Gözleri zümrüt gibi yeşil", "Jej oczy są zielone jak szmaragdy",
        "I suoi occhi sono verdi come smeraldi", "Sus ojos son verdes como esmeraldas",
        "Ses yeux sont verts comme des émeraudes", "Její oči jsou zelené jako smaragdy")}),
    15848: ("«Der Fisch bewegte …» — претерит; " + LIST + " (было четыре значения)", {
        "t_ru": "плавник, ласта", "t_uk": "плавець, ласта", "t_en": "fin, flipper", "t_tr": "yüzgeç, palet", "t_pl": "płetwa",
        "t_fr": "la nageoire, la palme", "t_cs": "ploutev",
        **all_x("Zum Schnorcheln brauche ich Brille und Flossen", "Для снорклинга мне нужны маска и ласты",
                "Для снорклінгу мені потрібні маска й ласти", "For snorkelling I need a mask and flippers",
                "Şnorkel için gözlük ve palet lazım", "Do snorkelingu potrzebuję maski i płetw",
                "Per lo snorkeling mi servono maschera e pinne", "Para hacer esnórquel necesito gafas y aletas",
                "Pour le snorkeling, il me faut un masque et des palmes", "Na šnorchlování potřebuju brýle a ploutve")}),
    18466: ("en «apartment» — американское; пример пустой; " + LIST, {
        "t_ru": "верхний этаж", "t_uk": "верхній поверх", "t_tr": "üst kat", "t_pl": "piętro, górne piętro",
        "t_it": "il piano di sopra", "t_es": "la planta de arriba", "t_fr": "l'étage",
        **all_x("Die Kinderzimmer sind im Obergeschoss", "Детские комнаты на верхнем этаже", "Дитячі кімнати на верхньому поверсі",
                "The children's rooms are upstairs", "Çocuk odaları üst katta", "Pokoje dzieci są na piętrze",
                "Le camerette dei bambini sono al piano di sopra", "Los cuartos de los niños están en la planta de arriba",
                "Les chambres des enfants sont à l'étage", "Dětské pokoje jsou v horním patře")}),
    15849: (LIST, {"t_ru": "источник, родник", "t_uk": "джерело", "t_en": "source, spring", "t_tr": "kaynak, pınar", "t_pl": "źródło",
                   "t_it": "la sorgente, la fonte", "t_es": "la fuente, el manantial", "t_fr": "la source", "t_cs": "pramen, zdroj"}),
    18935: ("en «ornaments» — американское; " + LIST, {
        "t_ru": "рождественский период, рождественские праздники", "t_uk": "різдвяний період, різдвяні свята",
        "t_en": "Christmas time, Christmas season", "t_pl": "okres świąteczny", "t_it": "il periodo natalizio",
        "t_es": "la época navideña", "t_fr": "la période de Noël", "t_cs": "vánoční období",
        "x_en": "At Christmas time we decorate the house with lights and decorations"}),
    9628: ("«… erklärte die komplexe Theorie» — претерит, книжно; " + LIST, {
        "t_ru": "профессор, преподавательница", "t_uk": "професорка", "t_en": "professor", "t_tr": "profesör",
        "t_pl": "pani profesor, profesorka", "t_it": "la professoressa", "t_es": "la profesora", "t_fr": "la professeure",
        **all_x("Unsere Professorin antwortet immer sofort auf E-Mails", "Наша профессор всегда сразу отвечает на письма",
                "Наша професорка завжди одразу відповідає на листи", "Our professor always answers emails straight away",
                "Profesörümüz e-postalara hep hemen cevap veriyor", "Nasza pani profesor zawsze od razu odpowiada na maile",
                "La nostra professoressa risponde sempre subito alle e-mail",
                "Nuestra profesora siempre contesta enseguida a los correos",
                "Notre professeure répond toujours tout de suite aux e-mails",
                "Naše profesorka vždycky hned odpovídá na e-maily")}),
    17724: ("«… für die Kommunikation über das Projekt» — канцелярит; " + LIST, {
        "t_ru": "чат", "t_uk": "чат", "t_en": "chat", "t_tr": "sohbet", "t_pl": "czat", "t_fr": "le chat",
        **all_x("Schreib es einfach in den Chat, dann sehen es alle", "Просто напиши это в чат, тогда все увидят",
                "Просто напиши це в чат, тоді всі побачать", "Just put it in the chat, then everyone will see it",
                "Sohbete yaz, herkes görsün", "Napisz to po prostu na czacie, wtedy wszyscy zobaczą",
                "Scrivilo nella chat, così lo vedono tutti", "Escríbelo en el chat y así lo ve todo el mundo",
                "Écris-le dans le chat, comme ça tout le monde le verra", "Napiš to do chatu, ať to vidí všichni")}),
    12398: ("пример повторяет Paddel; " + LIST + " (было три длинных значения)", {
        "t_ru": "грести", "t_uk": "гребти", "t_en": "to paddle", "t_tr": "kürek çekmek", "t_pl": "wiosłować",
        "t_it": "pagaiare, andare in canoa", "t_es": "remar", "t_fr": "pagayer", "t_cs": "pádlovat",
        **all_x("Im Urlaub paddeln wir jeden Morgen eine Runde auf dem See",
                "В отпуске мы каждое утро немного гребём по озеру", "У відпустці ми щоранку трохи гребемо по озеру",
                "On holiday we paddle around the lake every morning", "Tatilde her sabah gölde biraz kürek çekiyoruz",
                "Na urlopie co rano trochę wiosłujemy po jeziorze", "In vacanza ogni mattina andiamo in canoa sul lago",
                "En vacaciones cada mañana remamos un rato por el lago", "En vacances, on pagaie un peu sur le lac tous les matins",
                "O dovolené každé ráno chvíli pádlujeme po jezeře")}),
    89: ("«Der Mantel ist beige» — пусто", {**all_x(
        "Zu der beigen Hose passt ein weißes Hemd gut", "К бежевым брюкам хорошо подходит белая рубашка",
        "До бежевих штанів добре пасує біла сорочка", "A white shirt goes well with beige trousers",
        "Bej pantolona beyaz gömlek iyi gider", "Do beżowych spodni dobrze pasuje biała koszula",
        "Con i pantaloni beige sta bene una camicia bianca", "Con el pantalón beige queda bien una camisa blanca",
        "Une chemise blanche va bien avec un pantalon beige", "K béžovým kalhotám se hodí bílá košile")}),
    1180: ("en потерял «aus»; " + LIST, {
        "t_ru": "распечатать", "t_uk": "роздрукувати", "t_en": "to print out", "t_tr": "yazdırmak, çıktı almak", "t_pl": "wydrukować",
        "t_cs": "vytisknout", "x_en": "Can you print out the document?"}),
    15314: (LIST, {"t_ru": "горшок", "t_uk": "горщик", "t_en": "potty", "t_tr": "lazımlık", "t_pl": "nocnik"}),
    12004: ("«… ist sehr proteinreich» — этикетка; " + LIST, {
        "t_ru": "арахис", "t_uk": "арахіс", "t_pl": "orzeszek ziemny", "t_it": "l'arachide, la nocciolina", "t_es": "el cacahuete",
        "t_fr": "la cacahuète", "t_cs": "arašíd",
        **all_x("Meine Tochter ist gegen Erdnüsse allergisch", "У моей дочки аллергия на арахис", "У моєї доньки алергія на арахіс",
                "My daughter is allergic to peanuts", "Kızımın yer fıstığına alerjisi var", "Moja córka ma alergię na orzeszki ziemne",
                "Mia figlia è allergica alle arachidi", "Mi hija es alérgica a los cacahuetes",
                "Ma fille est allergique aux cacahuètes", "Moje dcera je alergická na arašídy")}),
    13127: ("«sehr süchtig machend» — неграмотно", {**all_x(
        "Nikotin macht schnell süchtig", "От никотина быстро возникает зависимость", "Від нікотину швидко виникає залежність",
        "Nicotine is highly addictive", "Nikotin çabuk bağımlılık yapar", "Nikotyna szybko uzależnia",
        "La nicotina crea dipendenza molto in fretta", "La nicotina crea adicción muy rápido",
        "La nicotine rend vite dépendant", "Nikotin rychle vytváří závislost")}),
    9630: ("«Der Bibliothekar half …» — претерит", {**all_x(
        "Frag den Bibliothekar, er weiß, wo das Buch steht", "Спроси библиотекаря, он знает, где стоит книга",
        "Спитай бібліотекаря, він знає, де стоїть книжка", "Ask the librarian, he knows where the book is",
        "Kütüphaneciye sor, kitabın nerede olduğunu biliyor", "Zapytaj bibliotekarza, on wie, gdzie stoi ta książka",
        "Chiedi al bibliotecario, sa dov'è il libro", "Pregúntale al bibliotecario, él sabe dónde está el libro",
        "Demande au bibliothécaire, il sait où est le livre", "Zeptej se knihovníka, ví, kde ta kniha stojí")}),
}

REPLACE = []

SPLIT_LATER = {}
