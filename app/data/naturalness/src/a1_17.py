"""A1, блок 17: слова 641–680 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
TWO = "в строке два разных слова — оставлено главное, второе — отдельной строкой (блок деления)"
EN = "английский пример: так не говорят"
NEAR = "пример повторял шаблон соседних слов — у каждого свой"
MARK = "пометки «(colloq.)/(coloq.)/(fam.)/(hovor.)» в переводе"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    17163: (TWO + " («перевал», «пас» — свои строки); «нужны наши паспорта для поездки» — калька", {
        "t_ru": "паспорт", "t_uk": "паспорт", "t_en": "passport", "t_tr": "pasaport", "t_pl": "paszport",
        "t_it": "il passaporto", "t_es": "el pasaporte", "t_fr": "le passeport", "t_cs": "pas",
        "x_ru": "Для поездки нам нужны паспорта", "x_uk": "Для подорожі нам потрібні паспорти"}),
    1562: (EN, {"x_en": "That's an international company"}),
    354: (LIST + "; «любим жарить на гриле» — так не говорят", {
        "t_ru": "жарить на гриле, делать барбекю", "t_uk": "смажити на грилі, смажити шашлики",
        "t_en": "to barbecue, to grill", "t_tr": "mangal yapmak", "t_pl": "grillować", "t_it": "fare la grigliata",
        "t_es": "hacer una barbacoa", "t_fr": "faire un barbecue",
        "x_ru": "Летом мы любим делать барбекю", "x_uk": "Влітку ми любимо смажити шашлики"}),
    1160: (LIST + "; пример ни о чём", {
        "t_ru": "рабочее место", "t_uk": "робоче місце", "t_en": "workplace, job", "t_tr": "iş yeri",
        "t_pl": "miejsce pracy", "t_fr": "le lieu de travail, le poste de travail",
        **all_x("Ich habe meinen Arbeitsplatz am Fenster", "Моё рабочее место у окна", "Моє робоче місце біля вікна",
                "My desk is by the window", "Çalışma yerim pencerenin yanında", "Moje miejsce pracy jest przy oknie",
                "La mia postazione è vicino alla finestra", "Mi puesto de trabajo está junto a la ventana",
                "Mon poste de travail est près de la fenêtre", "Moje pracovní místo je u okna")}),
    364: (LIST + "; «The price is cheap» — так не говорят", {
        "t_ru": "недорогой, выгодный", "t_en": "cheap, good value", "t_tr": "uygun fiyatlı", "t_pl": "tani, korzystny",
        "t_it": "conveniente", "t_es": "económico, barato", "t_fr": "avantageux, bon marché", "t_cs": "výhodný, levný",
        "x_en": "The price is good"}),
    11744: (LIST, {"t_ru": "горький", "t_uk": "гіркий", "t_en": "bitter", "t_tr": "acı", "t_pl": "gorzki",
                   "t_it": "amaro", "t_es": "amargo", "t_fr": "amer", "t_cs": "hořký"}),
    17166: (LIST, {"t_ru": "пересадка, подключение", "t_uk": "пересадка, підключення", "t_en": "connection",
                   "t_tr": "aktarma, bağlantı", "t_pl": "przesiadka, połączenie", "t_it": "la coincidenza",
                   "t_es": "el enlace, la conexión", "t_fr": "la correspondance", "t_cs": "přípoj, připojení"}),
    341: ("«Хочешь напиток?» — так по-русски не говорят", {**all_x(
        "Getränke gibt es in der Küche", "Напитки на кухне", "Напої на кухні", "The drinks are in the kitchen",
        "İçecekler mutfakta", "Napoje są w kuchni", "Le bevande sono in cucina", "Las bebidas están en la cocina",
        "Les boissons sont dans la cuisine", "Pití je v kuchyni")}),
    1099: (NEAR + " («… ist um X Uhr» — Abflug, abfahren); «спуск на лыжах» — другое значение", {
        "t_ru": "отправление, отъезд", "t_uk": "відправлення, від'їзд", "t_en": "departure", "t_tr": "kalkış",
        "t_pl": "odjazd", "t_it": "la partenza", "t_es": "la salida", "t_fr": "le départ", "t_cs": "odjezd",
        **all_x("Wann ist die Abfahrt?", "Когда отправление?", "Коли відправлення?", "What time is the departure?",
                "Kalkış ne zaman?", "Kiedy jest odjazd?", "A che ora è la partenza?", "¿A qué hora es la salida?",
                "Le départ est à quelle heure?", "Kdy je odjezd?")}),
    2140: (NEAR + " («… ist um X Uhr»)", {**all_x(
        "Wir müssen zwei Stunden vor dem Abflug am Flughafen sein",
        "Нам нужно быть в аэропорту за два часа до вылета", "Нам треба бути в аеропорту за дві години до вильоту",
        "We need to be at the airport two hours before departure", "Kalkıştan iki saat önce havalimanında olmalıyız",
        "Musimy być na lotnisku dwie godziny przed odlotem", "Dobbiamo essere in aeroporto due ore prima della partenza",
        "Tenemos que estar en el aeropuerto dos horas antes del despegue",
        "Nous devons être à l'aéroport deux heures avant le décollage", "Musíme být na letišti dvě hodiny před odletem")}),
    2184: (TWO + " («приставать», «заправлять салат» — свои строки); " + MARK, {
        "t_ru": "включать", "t_uk": "вмикати", "t_en": "to turn on", "t_tr": "açmak", "t_pl": "włączać",
        "t_it": "accendere", "t_es": "encender", "t_fr": "allumer", "t_cs": "rozsvítit, zapnout"}),
    13530: (NEAR + " («… wird nächsten Monat X Jahre alt» — у трёх числительных)", {**all_x(
        "Das Buch kostet fünfzig Euro", "Книга стоит пятьдесят евро", "Книжка коштує п'ятдесят євро",
        "The book costs fifty euros", "Kitap elli euro", "Książka kosztuje pięćdziesiąt euro",
        "Il libro costa cinquanta euro", "El libro cuesta cincuenta euros", "Le livre coûte cinquante euros",
        "Kniha stojí padesát eur")}),
    13559: (NEAR + " («… wird nächsten Monat X Jahre alt»)", {**all_x(
        "Der Kurs dauert vierzehn Tage", "Курс длится четырнадцать дней", "Курс триває чотирнадцять днів",
        "The course lasts fourteen days", "Kurs on dört gün sürüyor", "Kurs trwa czternaście dni",
        "Il corso dura quattordici giorni", "El curso dura catorce días", "Le cours dure quatorze jours",
        "Kurz trvá čtrnáct dní")}),
    281: (NEAR + " (ausfüllen: «Formular ausfüllen»); " + LIST, {
        "t_ru": "бланк, анкета", "t_uk": "бланк, анкета", "t_en": "form", "t_tr": "form", "t_pl": "formularz",
        "t_it": "il modulo", "t_es": "el formulario", "t_fr": "le formulaire", "t_cs": "formulář",
        **all_x("Wo bekomme ich das Formular?", "Где взять этот бланк?", "Де взяти цей бланк?",
                "Where can I get the form?", "Formu nereden alabilirim?", "Gdzie dostanę ten formularz?",
                "Dove trovo il modulo?", "¿Dónde consigo el formulario?",
                "Où est-ce que je peux trouver le formulaire?", "Kde dostanu ten formulář?")}),
    7325: (LIST + "; uk «формуляр» — канцелярски", {
        "t_ru": "заполнять", "t_uk": "заповнювати", "t_en": "to fill out, to fill in", "t_tr": "doldurmak",
        "t_pl": "wypełniać", "t_it": "compilare", "t_es": "rellenar", "t_fr": "remplir", "t_cs": "vyplnit",
        "x_uk": "Будь ласка, заповни бланк"}),
    15084: (LIST, {"t_ru": "домохозяйка", "t_uk": "домогосподарка", "t_en": "housewife", "t_tr": "ev hanımı",
                   "t_pl": "gospodyni domowa"}),
    16293: ("исторический пример про «европейские державы» на A1; «держава» — другое значение", {
        "t_ru": "власть, сила", "t_uk": "влада, сила", "t_en": "power", "t_tr": "güç, iktidar", "t_pl": "władza, potęga",
        "t_it": "il potere", "t_es": "el poder", "t_fr": "le pouvoir", "t_cs": "moc",
        **all_x("Er hat viel Macht in der Firma", "У него большая власть в компании", "У нього велика влада в компанії",
                "He has a lot of power in the company", "Şirkette çok gücü var", "Ma dużo władzy w firmie",
                "Ha molto potere nell'azienda", "Tiene mucho poder en la empresa",
                "Il a beaucoup de pouvoir dans l'entreprise", "Ve firmě má velkou moc")}),
    247: (NEAR + " («Ich kaufe …» — kaufen, Brot)", {**all_x(
        "Wo kann ich eine Fahrkarte kaufen?", "Где можно купить билет?", "Де можна купити квиток?",
        "Where can I buy a ticket?", "Nereden bilet alabilirim?", "Gdzie mogę kupić bilet?",
        "Dove posso comprare il biglietto?", "¿Dónde puedo comprar un billete?",
        "Où est-ce que je peux acheter un billet?", "Kde si můžu koupit jízdenku?")}),
    2092: ("«Das Baby ist weiblich» — так не говорят (говорят Mädchen); слово живёт в анкетах", {
        "t_ru": "женский", "t_uk": "жіночий", "t_en": "female, feminine", "t_tr": "kadın, dişi",
        "t_pl": "żeński, kobiecy",
        **all_x("Bitte kreuzen Sie an: männlich oder weiblich", "Отметьте, пожалуйста: мужской или женский пол",
                "Позначте, будь ласка: чоловіча чи жіноча стать", "Please tick: male or female",
                "Lütfen işaretleyin: erkek mi, kadın mı", "Proszę zaznaczyć: płeć męska czy żeńska",
                "Barrare: maschile o femminile", "Marque, por favor: masculino o femenino",
                "Cochez, s'il vous plaît: masculin ou féminin", "Zaškrtněte prosím: mužské, nebo ženské pohlaví")}),
    17188: (LIST + "; «восприятие» — другое значение", {
        "t_ru": "ресепшен, стойка регистрации", "t_uk": "рецепція", "t_en": "reception, front desk",
        "t_tr": "resepsiyon", "t_pl": "recepcja"}),
    14072: (LIST, {"t_ru": "справка, информация", "t_uk": "довідка, інформація", "t_en": "information",
                   "t_tr": "bilgi", "t_pl": "informacja"}),
    995: (NEAR + " (Samstag: «Am … bin ich frei»); три описания вместо слова", {
        "t_ru": "первая половина дня, утро", "t_uk": "перша половина дня", "t_en": "morning",
        "t_tr": "öğleden önce", "t_pl": "przedpołudnie",
        **all_x("Am Vormittag arbeite ich", "В первой половине дня я работаю", "У першій половині дня я працюю",
                "I work in the mornings", "Öğleden önce çalışıyorum", "Przed południem pracuję", "La mattina lavoro",
                "Por la mañana trabajo", "Le matin, je travaille", "Dopoledne pracuji")}),
    2044: (LIST, {"t_ru": "сдавать", "t_uk": "здавати в оренду", "t_en": "to rent out, to let", "t_tr": "kiraya vermek",
                  "t_pl": "wynajmować", "t_it": "dare in affitto", "t_es": "alquilar", "t_fr": "louer",
                  "t_cs": "pronajímat"}),
    31: (NEAR + " (Durchsage: «… im Zug»); " + LIST, {
        "t_ru": "объявление", "t_uk": "оголошення", "t_en": "announcement", "t_tr": "anons", "t_pl": "komunikat",
        "t_it": "l'annuncio", "t_es": "el aviso", "t_fr": "l'annonce", "t_cs": "hlášení",
        **all_x("Hast du die Ansage verstanden?", "Ты понял объявление?", "Ти зрозумів оголошення?",
                "Did you understand the announcement?", "Anonsu anladın mı?", "Zrozumiałeś komunikat?",
                "Hai capito l'annuncio?", "¿Has entendido el aviso?", "Tu as compris l'annonce?",
                "Rozuměl jsi tomu hlášení?")}),
    17202: (LIST, {"t_ru": "путь, платформа", "t_uk": "колія, платформа", "t_en": "platform, track", "t_tr": "peron",
                   "t_pl": "tor, peron", "t_it": "il binario", "t_es": "la vía, el andén", "t_fr": "la voie, le quai",
                   "t_cs": "kolej, nástupiště"}),
    14102: (LIST + "; «приёмник» — другое значение", {
        "t_ru": "получатель, адресат", "t_uk": "отримувач, адресат", "t_en": "recipient", "t_tr": "alıcı",
        "t_pl": "odbiorca"}),
    9522: (EN, {"x_en": "He's doing an internship"}),
    1098: (LIST + "; uk «від'їжджає о 10-й годині» — неживо", {
        "t_ru": "отправляться, уезжать", "t_uk": "від'їжджати, вирушати", "t_en": "to depart, to leave",
        "t_tr": "hareket etmek, kalkmak", "t_pl": "odjeżdżać", "t_es": "salir", "t_cs": "odjíždět",
        "x_uk": "Поїзд відправляється о десятій"}),
}

SPLIT_LATER = {
    17163: ["der Pass = перевал", "der Pass = пас (спорт)"],
    2184: ["anmachen = приставать, заигрывать (разг.)", "anmachen = заправить (салат)"],
}
