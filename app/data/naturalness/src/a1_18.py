"""A1, блок 18: слова 681–720 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
TWO = "в строке два разных слова — оставлено главное, второе — отдельной строкой (блок деления)"
EN = "английский пример: так не говорят"
NEAR = "пример повторял шаблон соседних слов — у каждого свой"
MARK = "пометки «(coloq.)/(fam.)» в переводе"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    12253: (MARK + "; «сегодня ночью» — heute Nacht здесь «сегодня вечером»", {
        "t_es": "la discoteca", "t_fr": "la boîte de nuit, la discothèque",
        "x_ru": "Сегодня вечером мы идём на дискотеку", "x_uk": "Сьогодні ввечері ми йдемо на дискотеку"}),
    1986: (TWO + " («направлять к врачу» — своя строка); " + MARK, {
        "t_ru": "переводить, перечислять", "t_uk": "переказувати", "t_en": "to transfer", "t_tr": "havale yapmak",
        "t_pl": "przelać, przelewać", "t_it": "fare un bonifico", "t_es": "transferir, hacer una transferencia",
        "t_fr": "faire un virement", "t_cs": "převést"}),
    463: (MARK + "; «люблю есть картошку» — калька", {
        "t_fr": "la pomme de terre", "x_ru": "Я люблю варёную картошку с маслом",
        "x_uk": "Я люблю варену картоплю з маслом", "x_en": "I like boiled potatoes with butter"}),
    820: (EN, {"x_en": "We're going to the pool"}),
    9043: (TWO + " («работать на себя» — Ich bin selbstständig, своя строка)", {
        "t_ru": "самостоятельный", "t_uk": "самостійний", "t_en": "independent", "t_tr": "bağımsız",
        "t_pl": "samodzielny"}),
    934: (NEAR + " (Obst: «Ich kaufe … auf dem Markt»)", {**all_x(
        "Ich mache einen Salat mit Tomaten und Gurken", "Я делаю салат из помидоров и огурцов",
        "Я роблю салат із помідорів і огірків", "I'm making a salad with tomatoes and cucumbers",
        "Domates ve salatalıklı salata yapıyorum", "Robię sałatkę z pomidorów i ogórków",
        "Faccio un'insalata con pomodori e cetrioli", "Hago una ensalada con tomates y pepinos",
        "Je fais une salade avec des tomates et des concombres", "Dělám salát z rajčat a okurek")}),
    363: (LIST + "; пример ни о чём", {
        "t_ru": "действительный", "t_uk": "дійсний, чинний",
        **all_x("Ist dieses Ticket noch gültig?", "Этот билет ещё действителен?", "Цей квиток ще дійсний?",
                "Is this ticket still valid?", "Bu bilet hâlâ geçerli mi?", "Czy ten bilet jest jeszcze ważny?",
                "Questo biglietto è ancora valido?", "¿Este billete sigue siendo válido?",
                "Ce billet est encore valable?", "Platí ještě tahle jízdenka?")}),
    17250: (LIST, {"t_ru": "осматривать", "t_uk": "оглядати", "t_en": "to visit, to view", "t_tr": "gezmek",
                   "t_pl": "zwiedzać, oglądać", "t_it": "visitare", "t_es": "visitar", "t_cs": "prohlédnout si",
                   "x_en": "We're viewing the new flat"}),
    15183: (LIST, {"t_ru": "холостой, незамужняя", "t_uk": "неодружений, незаміжня", "t_tr": "bekâr",
                   "t_pl": "nieżonaty, niezamężna"}),
    375: (LIST, {"t_ru": "остановка", "t_uk": "зупинка", "t_en": "stop"}),
    518: (MARK + "; «шариковую ручку» — так не говорят", {
        "t_es": "el bolígrafo, el boli", "x_ru": "Можно твою ручку?"}),
    27: (LIST + "; пять значений", {
        "t_ru": "регистрация, запись", "t_uk": "реєстрація, запис", "t_en": "registration, sign-up", "t_tr": "kayıt",
        "t_pl": "rejestracja, zapisy", "t_it": "l'iscrizione", "t_es": "la inscripción", "t_fr": "l'inscription",
        "t_cs": "přihláška, registrace"}),
    11890: (LIST + "; «Еда была правда вкусной» — калька", {
        "t_ru": "еда", "t_uk": "їжа", "t_en": "food, meal", "t_tr": "yemek", "t_pl": "jedzenie",
        "x_ru": "Еда была очень вкусная"}),
    886: (NEAR + " (Bahn: «Ich fahre mit … zur Arbeit»)", {**all_x(
        "Die Straßenbahn kommt alle zehn Minuten", "Трамвай ходит каждые десять минут", "Трамвай ходить кожні десять хвилин",
        "The tram comes every ten minutes", "Tramvay her on dakikada bir geliyor", "Tramwaj jeździ co dziesięć minut",
        "Il tram passa ogni dieci minuti", "El tranvía pasa cada diez minutos", "Le tram passe toutes les dix minutes",
        "Tramvaj jezdí každých deset minut")}),
    2757: ("«забронировать путешествие» — калька", {"x_ru": "Я иду в турагентство, чтобы забронировать поездку"}),
    14241: ("tr: грамматическая ошибка — «прежде чем быть отправленным»", {
        "x_tr": "Göndermeden önce mektuba pul yapıştırmam gerekiyor"}),
    14245: (TWO + " («предварительные выборы» — омоним, своя строка)", {
        "t_ru": "телефонный код", "t_uk": "телефонний код", "t_en": "area code", "t_tr": "alan kodu",
        "t_pl": "numer kierunkowy", "t_it": "il prefisso", "t_es": "el prefijo", "t_fr": "l'indicatif",
        "t_cs": "předvolba"}),
    9911: (LIST, {"t_ru": "киоск", "t_uk": "кіоск", "t_en": "kiosk", "t_tr": "büfe", "t_pl": "kiosk"}),
    2395: (NEAR + " (Doppelzimmer: «Ich buche ein …zimmer»)", {**all_x(
        "Ein Einzelzimmer kostet 80 Euro pro Nacht", "Одноместный номер стоит 80 евро за ночь",
        "Одномісний номер коштує 80 євро за ніч", "A single room costs 80 euros a night",
        "Tek kişilik oda gecelik 80 euro", "Pokój jednoosobowy kosztuje 80 euro za noc",
        "Una camera singola costa 80 euro a notte", "Una habitación individual cuesta 80 euros la noche",
        "Une chambre simple coûte 80 euros la nuit", "Jednolůžkový pokoj stojí 80 eur za noc")}),
    13600: (NEAR + " («… wird nächste Woche X Jahre alt»)", {**all_x(
        "Der Bus Nummer neunzehn fährt zum Bahnhof", "Автобус номер девятнадцать идёт до вокзала",
        "Автобус номер дев'ятнадцять їде до вокзалу", "Bus number nineteen goes to the station",
        "On dokuz numaralı otobüs istasyona gidiyor", "Autobus numer dziewiętnaście jedzie na dworzec",
        "L'autobus numero diciannove va alla stazione", "El autobús número diecinueve va a la estación",
        "Le bus numéro dix-neuf va à la gare", "Autobus číslo devatenáct jede na nádraží")}),
    18924: ("en «to have been there» — прошедшее время, не значение слова", {
        "t_en": "to be there, to be present", "x_en": "I was there the whole time and watched"}),
    11492: ("порча знаний: приставка Lieblings- переведена «любимый ресторан» — ресторан из примера", {
        "t_ru": "любимый", "t_uk": "улюблений", "t_en": "favourite", "t_tr": "en sevdiğim, favori",
        "t_pl": "ulubiony"}),
    11: (NEAR + " (Ordnung: «Alles in Ordnung?»)", {**all_x(
        "Ich habe alles vergessen", "Я всё забыл", "Я все забув", "I forgot everything", "Her şeyi unuttum",
        "Wszystko zapomniałem", "Ho dimenticato tutto", "Lo he olvidado todo", "J'ai tout oublié",
        "Všechno jsem zapomněl")}),
}

SPLIT_LATER = {
    1986: ["überweisen = направить к врачу (Überweisung)"],
    9043: ["selbstständig sein = работать на себя"],
    14245: ["die Vorwahl = предварительные выборы"],
}
