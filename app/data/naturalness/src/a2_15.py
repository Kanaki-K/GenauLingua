"""A2, блок 15: слова 561–600 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
SKEL = "пример-скелет («Der Himmel ist grau», «Sie nimmt ein Medikament») — пусто"
TWO = "в строке два разных слова — оставлено главное, второе — отдельной строкой (блок деления)"
EN = "английский пример: так не говорят"
WEAR = "«trägt …» — шаблон одежды; у каждой вещи свой пример"
BAKE = "пятый пример «печёт пироги» (Tante, Oma, backen, Nachbarin, Torte) — у каждого свой"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    13509: ("en «thus» — книжно; ru «таким образом мы можем» — канцелярски", {
        "t_ru": "таким образом, значит", "t_uk": "таким чином, отже", "t_en": "so, thus",
        "t_tr": "böylece, dolayısıyla", "t_pl": "zatem, tym samym", "t_it": "quindi, perciò",
        "t_es": "así que, por lo tanto", "t_fr": "donc, ainsi", "t_cs": "takže, tím pádem",
        "x_ru": "Проект готов, а значит, можем начинать", "x_uk": "Проект готовий, отже, можемо починати",
        "x_en": "The project is ready, so we can start"}),
    18704: ("«Sommersaison» прячет слово в составном; " + LIST, {
        "t_ru": "сезон", "t_uk": "сезон", "t_en": "season", "t_tr": "sezon", "t_pl": "sezon",
        **all_x("Erdbeeren haben jetzt Saison", "Сейчас сезон клубники", "Зараз сезон полуниці",
                "Strawberries are in season now", "Şimdi çilek sezonu", "Teraz jest sezon na truskawki",
                "Adesso è la stagione delle fragole", "Ahora es temporada de fresas", "C'est la saison des fraises",
                "Teď je sezóna jahod")}),
    2710: ("«Ich parke mein Auto hier» — так о себе не рассказывают; " + LIST, {
        "t_ru": "парковать(ся)", "t_uk": "паркувати(ся)", "t_es": "aparcar", "t_fr": "se garer, garer",
        **all_x("Ich habe direkt vor dem Haus geparkt", "Я припарковался прямо перед домом",
                "Я припаркувався просто перед будинком", "I parked right in front of the house",
                "Evin hemen önüne park ettim", "Zaparkowałem tuż przed domem", "Ho parcheggiato proprio davanti a casa",
                "He aparcado justo delante de casa", "Je me suis garé juste devant la maison",
                "Zaparkoval jsem přímo před domem")}),
    935: (BAKE + "; en «torte» — не по-английски", {
        "t_en": "cake", "t_tr": "pasta", "t_es": "la tarta",
        **all_x("Zum Geburtstag gibt es eine große Torte mit Kerzen",
                "На день рождения будет большой торт со свечами", "На день народження буде великий торт зі свічками",
                "There'll be a big cake with candles for the birthday", "Doğum günü için mumlu büyük bir pasta olacak",
                "Na urodziny będzie duży tort ze świeczkami", "Per il compleanno ci sarà una grande torta con le candeline",
                "Para el cumpleaños habrá una tarta grande con velas",
                "Pour l'anniversaire, il y aura un grand gâteau avec des bougies", "K narozeninám bude velký dort se svíčkami")}),
    768: (WEAR, {**all_x(
        "Pack dir was zu essen in den Rucksack", "Положи себе в рюкзак что-нибудь поесть", "Поклади собі в рюкзак щось поїсти",
        "Put something to eat in your backpack", "Sırt çantana yiyecek bir şey koy", "Spakuj sobie coś do jedzenia do plecaka",
        "Mettiti qualcosa da mangiare nello zaino", "Métete algo de comer en la mochila",
        "Mets-toi quelque chose à manger dans ton sac à dos", "Dej si do batohu něco k jídlu")}),
    1634: (LIST, {"t_ru": "уволиться, расторгнуть договор", "t_uk": "звільнитися, розірвати договір",
                  "t_en": "to quit, to cancel (a contract)", "t_tr": "istifa etmek, feshetmek",
                  "t_pl": "złożyć wypowiedzenie, wypowiedzieć umowę", "t_it": "licenziarsi, disdire",
                  "t_es": "renunciar, rescindir", "t_fr": "démissionner, résilier", "t_cs": "dát výpověď, vypovědět"}),
    1366: ("«призывать в армию» — третье значение; " + LIST, {
        "t_ru": "вселяться, взимать", "t_uk": "вселятися, стягувати", "t_en": "to move in, to collect",
        "t_tr": "taşınmak, tahsil etmek", "t_pl": "wprowadzać się, pobierać", "t_it": "trasferirsi, riscuotere",
        "t_es": "mudarse, cobrar", "t_fr": "emménager, percevoir", "t_cs": "nastěhovat se, vybírat",
        "x_ru": "Мы въезжаем на следующей неделе"}),
    903: ("«Sie geht in den Supermarkt» — шаблон «gehen in den X»", {**all_x(
        "Ich geh schnell zum Supermarkt, brauchst du was?", "Я быстро сбегаю в супермаркет, тебе что-нибудь нужно?",
        "Я швиденько збігаю в супермаркет, тобі щось треба?", "I'm just popping to the supermarket, do you need anything?",
        "Hemen süpermarkete gidiyorum, bir şey lazım mı?", "Skoczę szybko do supermarketu, potrzebujesz czegoś?",
        "Faccio un salto al supermercato, ti serve qualcosa?", "Voy un momento al supermercado, ¿necesitas algo?",
        "Je fais un saut au supermarché, tu as besoin de quelque chose?", "Skočím do supermarketu, potřebuješ něco?")}),
    1940: ("«Я принимаю участие в курсе» — канцелярски; " + LIST, {
        "t_ru": "участвовать", "t_uk": "брати участь", "t_en": "to take part", "t_tr": "katılmak",
        "t_pl": "brać udział, uczestniczyć", "t_it": "partecipare", "t_es": "participar", "t_fr": "participer",
        "t_cs": "účastnit se",
        **all_x("Wie viele Leute nehmen an der Reise teil?", "Сколько человек участвует в поездке?",
                "Скільки людей бере участь у поїздці?", "How many people are taking part in the trip?",
                "Geziye kaç kişi katılıyor?", "Ile osób bierze udział w wycieczce?", "Quante persone partecipano al viaggio?",
                "¿Cuántas personas participan en el viaje?", "Combien de personnes participent au voyage?",
                "Kolik lidí se účastní výletu?")}),
    437: ("шаблон fünfzig («Das Buch kostet fünfzig Euro»); " + LIST, {
        "t_ru": "всего, в целом", "t_uk": "усього, загалом", "t_en": "in total, overall", "t_tr": "toplam",
        "t_pl": "w sumie, łącznie",
        **all_x("Wir waren insgesamt zehn Leute", "Всего нас было десять человек", "Загалом нас було десятеро",
                "There were ten of us in total", "Toplam on kişiydik", "W sumie było nas dziesięcioro",
                "In totale eravamo in dieci", "En total éramos diez", "On était dix au total", "Celkem nás bylo deset")}),
    605: ("четвёртый пример «интересуется …» (interessieren, Interesse, Kultur)", {**all_x(
        "Das ist gerade total in Mode", "Сейчас это очень в моде", "Зараз це дуже в моді",
        "That's really in fashion right now", "Bu şu an çok moda", "To jest teraz bardzo modne",
        "Adesso va molto di moda", "Ahora está muy de moda", "C'est très à la mode en ce moment",
        "Teď je to hodně v módě")}),
    13659: (LIST + "; uk — без «а тепер»", {
        "t_ru": "зонт, козырёк", "t_uk": "парасолька, козирок", "t_en": "umbrella, screen", "t_tr": "şemsiye",
        "t_pl": "parasol", "t_it": "l'ombrello", "t_es": "el paraguas", "t_fr": "le parapluie", "t_cs": "deštník",
        "x_ru": "Я забыл зонт, а теперь идёт дождь", "x_uk": "Я забув парасольку, а тепер іде дощ"}),
    2559: ("«Wir stellen Autos her» — кто «мы»? пусто; " + LIST, {
        "t_ru": "производить, изготавливать", "t_uk": "виробляти, виготовляти", "t_en": "to produce, to manufacture",
        "t_tr": "üretmek, imal etmek", "t_pl": "produkować, wytwarzać", "t_it": "produrre, fabbricare",
        "t_es": "fabricar, producir", "t_fr": "fabriquer, produire", "t_cs": "vyrábět",
        **all_x("Die Firma stellt Möbel her", "Эта фирма производит мебель", "Ця фірма виробляє меблі",
                "The company manufactures furniture", "Şirket mobilya üretiyor", "Ta firma produkuje meble",
                "L'azienda produce mobili", "La empresa fabrica muebles", "L'entreprise fabrique des meubles",
                "Ta firma vyrábí nábytek")}),
    11707: (TWO + " («житель Гамбурга» — омоним)", {
        "t_ru": "гамбургер, бургер", "x_ru": "На обед я ем гамбургер с картошкой фри",
        "x_en": "I'm having a hamburger with fries for lunch"}),
    283: ("uk «Я фотографую місто» — без «люблю», смысл потерян; " + LIST, {
        "t_ru": "фотографировать, снимать", "t_uk": "фотографувати", "t_en": "to take photos, to photograph",
        "t_tr": "fotoğraf çekmek", "t_pl": "fotografować, robić zdjęcia", "t_es": "fotografiar, sacar fotos",
        "x_uk": "Я люблю фотографувати місто", "x_en": "I like taking photos of the city",
        "x_tr": "Şehrin fotoğraflarını çekmeyi seviyorum"}),
    7055: ("«Содержимое бутылки очень ценно» — неживо; " + LIST, {
        "t_ru": "содержимое, содержание", "t_uk": "вміст, зміст", "t_en": "contents, content",
        "t_tr": "içerik, içindekiler", "t_pl": "zawartość, treść", "t_it": "il contenuto", "t_es": "el contenido",
        "t_fr": "le contenu", "t_cs": "obsah",
        **all_x("Der Inhalt der Tasche liegt auf dem Tisch", "Всё содержимое сумки лежит на столе",
                "Увесь вміст сумки лежить на столі", "The contents of the bag are on the table",
                "Çantanın içindekiler masada", "Zawartość torby leży na stole", "Il contenuto della borsa è sul tavolo",
                "El contenido del bolso está sobre la mesa", "Le contenu du sac est sur la table",
                "Obsah tašky leží na stole")}),
    8857: (LIST, {"t_ru": "начальница", "t_uk": "начальниця, керівниця", "t_en": "boss", "t_tr": "patron",
                  "t_pl": "szefowa"}),
    7057: (TWO + " (выставка и месса); «zur Messe in der Kirche» — масло масляное", {
        "t_ru": "выставка, ярмарка", "t_uk": "виставка, ярмарок", "t_en": "trade fair, exhibition", "t_tr": "fuar",
        "t_pl": "targi", "t_it": "la fiera", "t_es": "la feria", "t_fr": "le salon, la foire", "t_cs": "veletrh",
        **all_x("Mein Mann ist diese Woche auf einer Messe in Köln", "Мой муж на этой неделе на выставке в Кёльне",
                "Мій чоловік цього тижня на виставці в Кельні", "My husband is at a trade fair in Cologne this week",
                "Kocam bu hafta Köln'de bir fuarda", "Mój mąż jest w tym tygodniu na targach w Kolonii",
                "Mio marito questa settimana è a una fiera a Colonia", "Mi marido está esta semana en una feria en Colonia",
                "Mon mari est à un salon à Cologne cette semaine", "Můj manžel je tento týden na veletrhu v Kolíně")}),
    7058: (LIST, {"t_ru": "рамка, рама", "t_uk": "рамка, рама", "t_en": "frame", "t_tr": "çerçeve",
                  "t_pl": "rama, ramka", "t_it": "la cornice, il telaio", "t_cs": "rám, rámeček"}),
    707: ("«Die Pflanze braucht Wasser» — скелет", {
        "t_ru": "растение", "t_uk": "рослина", "t_pl": "roślina",
        **all_x("Kannst du im Urlaub meine Pflanzen gießen?", "Можешь поливать мои растения, пока я в отпуске?",
                "Можеш поливати мої рослини, поки я у відпустці?", "Can you water my plants while I'm on holiday?",
                "Ben tatildeyken bitkilerimi sular mısın?", "Możesz podlewać moje rośliny, kiedy będę na urlopie?",
                "Mi annaffi le piante mentre sono in vacanza?", "¿Me riegas las plantas mientras estoy de vacaciones?",
                "Tu peux arroser mes plantes pendant mes vacances?", "Můžeš mi zalévat rostliny, až budu na dovolené?")}),
    15033: (BAKE, {"t_en": "neighbour", "t_tr": "komşu", **all_x(
        "Meine Nachbarin passt manchmal auf unseren Hund auf", "Соседка иногда присматривает за нашей собакой",
        "Сусідка іноді доглядає нашого собаку", "My neighbour sometimes looks after our dog",
        "Komşum bazen köpeğimize bakıyor", "Sąsiadka czasem opiekuje się naszym psem",
        "La mia vicina a volte ci tiene il cane", "Mi vecina a veces nos cuida el perro",
        "Ma voisine garde parfois notre chien", "Sousedka nám občas hlídá psa")}),
    1285: ("uk «русяве» — это светло-русый, а не блонд", {"t_ru": "светлый, белокурый", "t_uk": "білявий, світлий",
                                                       "x_uk": "У неї біляве волосся"}),
    1069: ("«Ich zeichne ein Bild» — скелет", {"t_ru": "рисовать, чертить", **all_x(
        "Er zeichnet sehr gut", "Он очень хорошо рисует", "Він дуже добре малює", "He's really good at drawing",
        "Çok iyi resim çiziyor", "Bardzo dobrze rysuje", "Disegna molto bene", "Dibuja muy bien",
        "Il dessine très bien", "Kreslí moc hezky")}),
    67: (LIST, {"t_ru": "печь", "t_uk": "пекти", "t_tr": "fırında pişirmek", "t_pl": "piec",
                "x_en": "My gran bakes wonderful cakes"}),
    353: (SKEL + "; шаблон blau («Der Himmel ist blau»)", {**all_x(
        "Heute ist alles so grau und kalt", "Сегодня всё такое серое и холодное", "Сьогодні все таке сіре й холодне",
        "Everything's so grey and cold today", "Bugün her şey çok gri ve soğuk", "Dziś wszystko jest takie szare i zimne",
        "Oggi è tutto così grigio e freddo", "Hoy todo está tan gris y frío", "Aujourd'hui, tout est si gris et froid",
        "Dneska je všechno tak šedé a studené")}),
    14006: (LIST, {"t_ru": "консультировать, обсуждать", "t_uk": "консультувати, радитися",
                   "t_en": "to advise, to discuss", "t_tr": "danışmanlık yapmak, görüşmek",
                   "t_pl": "doradzać, obradować", "t_it": "consigliare, discutere", "t_es": "asesorar, deliberar",
                   "t_fr": "conseiller, délibérer", "t_cs": "radit, projednávat"}),
    8865: ("«делает хорошие стрижки» — калька", {**all_x(
        "Ich muss mal wieder zum Friseur", "Мне пора снова к парикмахеру", "Мені знову час до перукаря",
        "I need to go to the hairdresser's again", "Yine kuaföre gitmem lazım", "Muszę znowu iść do fryzjera",
        "Devo tornare dal parrucchiere", "Tengo que ir otra vez al peluquero",
        "Il faut que je retourne chez le coiffeur", "Musím zase ke kadeřníkovi")}),
    1292: ("uk/en потеряли «на сковороде»; " + LIST, {
        "t_ru": "жарить", "t_uk": "смажити", "t_en": "to fry, to roast", "t_tr": "kızartmak", "t_pl": "smażyć",
        "x_uk": "Я смажу м'ясо на сковороді", "x_en": "I'm frying the meat in the pan",
        "x_tr": "Eti tavada kızartıyorum"}),
    577: (SKEL, {**all_x(
        "Nehmen Sie das Medikament dreimal am Tag", "Принимайте лекарство три раза в день", "Приймайте ліки тричі на день",
        "Take the medication three times a day", "İlacı günde üç kez alın", "Proszę brać lek trzy razy dziennie",
        "Prenda il farmaco tre volte al giorno", "Tome el medicamento tres veces al día",
        "Prenez le médicament trois fois par jour", "Berte ten lék třikrát denně")}),
    8868: (LIST, {"t_en": "colleague", "t_tr": "iş arkadaşı", "t_pl": "koleżanka z pracy"}),
    448: (WEAR, {**all_x(
        "Die Jeans passt mir nicht mehr", "Эти джинсы мне уже не подходят",
        "Ці джинси мені вже не підходять", "These jeans don't fit me any more", "Bu kot artık bana olmuyor",
        "Te dżinsy już na mnie nie pasują", "Questi jeans non mi stanno più", "Estos vaqueros ya no me quedan bien",
        "Ce jean ne me va plus", "Ty džíny mi už nesedí")}),
    8874: ("«Журналист пишет статьи для газеты» — из словаря, а не из жизни", {**all_x(
        "Der Journalist hat viele Fragen gestellt", "Журналист задал много вопросов", "Журналіст поставив багато запитань",
        "The journalist asked a lot of questions", "Gazeteci çok soru sordu", "Dziennikarz zadał dużo pytań",
        "Il giornalista ha fatto tante domande", "El periodista hizo muchas preguntas",
        "Le journaliste a posé beaucoup de questions", "Novinář položil spoustu otázek")}),
    18212: ("«Die Reinigung des Hauses» — канцелярски; химчистка — то, что говорят каждый день", {
        "t_ru": "уборка, химчистка", "t_uk": "прибирання, хімчистка", "t_en": "cleaning, dry cleaner's",
        "t_tr": "temizlik, kuru temizleme", "t_pl": "sprzątanie, pralnia chemiczna", "t_it": "la pulizia, la tintoria",
        "t_es": "la limpieza, la tintorería", "t_fr": "le nettoyage, le pressing", "t_cs": "úklid, čistírna",
        **all_x("Ich bringe den Anzug in die Reinigung", "Я отнесу костюм в химчистку", "Я віднесу костюм у хімчистку",
                "I'm taking the suit to the dry cleaner's", "Takım elbiseyi kuru temizlemeciye götürüyorum",
                "Zaniosę garnitur do pralni chemicznej", "Porto il vestito in tintoria", "Llevo el traje a la tintorería",
                "J'apporte le costume au pressing", "Nesu oblek do čistírny")}),
    17140: ("ru «жилье» — без ё; пример пустой; " + LIST, {
        "t_ru": "жильё, ночлег", "t_uk": "житло, нічліг", "t_en": "accommodation, place to stay",
        "t_tr": "konaklama, kalacak yer", "t_pl": "nocleg, zakwaterowanie",
        **all_x("Ich habe eine günstige Unterkunft in der Altstadt gefunden", "Я нашёл недорогое жильё в старом городе",
                "Я знайшов недороге житло в старому місті", "I've found cheap accommodation in the old town",
                "Eski şehirde ucuz bir kalacak yer buldum", "Znalazłem tani nocleg na starym mieście",
                "Ho trovato un alloggio economico nel centro storico", "He encontrado un alojamiento barato en el casco antiguo",
                "J'ai trouvé un logement pas cher dans la vieille ville", "Našel jsem levné ubytování ve starém městě")}),
    3030: ("«Die Wolke zieht über den Himmel» — книжно", {**all_x(
        "Am Himmel ist keine einzige Wolke", "На небе ни облачка", "На небі жодної хмаринки",
        "There isn't a single cloud in the sky", "Gökyüzünde tek bir bulut yok", "Na niebie nie ma ani jednej chmurki",
        "In cielo non c'è neanche una nuvola", "No hay ni una nube en el cielo", "Il n'y a pas un seul nuage dans le ciel",
        "Na obloze není ani mráček")}),
    14475: ("пример — аннотация из каталога; «выдача документа» — другое значение", {
        "t_ru": "выставка, экспозиция", "t_uk": "виставка, експозиція", "t_en": "exhibition", "t_tr": "sergi",
        "t_pl": "wystawa", "t_it": "la mostra", "t_es": "la exposición", "t_fr": "l'exposition", "t_cs": "výstava",
        **all_x("Die Ausstellung ist noch bis Sonntag offen", "Выставка открыта ещё до воскресенья",
                "Виставка відкрита ще до неділі", "The exhibition is open until Sunday", "Sergi pazara kadar açık",
                "Wystawa jest otwarta jeszcze do niedzieli", "La mostra è aperta fino a domenica",
                "La exposición está abierta hasta el domingo", "L'exposition est ouverte jusqu'à dimanche",
                "Výstava je otevřená ještě do neděle")}),
    950: (LIST, {"t_ru": "время (на часах)", "t_uk": "час (на годиннику)", "t_en": "time (of day)", "t_tr": "saat",
                 "t_pl": "godzina"}),
}

# somit — письменное; говорят also
REPLACE = [{"id": 13509, "by": 14, "lang": "de", "why": "somit — письменное, в речи also"}]

SPLIT_LATER = {
    11707: ["der Hamburger = житель Гамбурга"],
    7057: ["die Messe = месса"],
}
