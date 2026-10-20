"""A1, блок 5: слова 161–200 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
TWO = "в строке два разных слова — оставлено главное, второе — отдельной строкой (блок деления)"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    88: (LIST, {"t_ru": "оба, обе", "t_uk": "обидва, обидві", "t_tr": "ikisi de, her iki", "t_pl": "oba, obie",
                "t_fr": "les deux"}),
    330: ("«любить делать» — пояснение; «Я охотно пью чай» — калька", {
        "t_ru": "охотно, с удовольствием", "t_uk": "охоче, із задоволенням", "t_en": "gladly",
        "t_tr": "severek, seve seve", "t_pl": "chętnie", "t_fr": "volontiers",
        "x_ru": "Чай я пью с удовольствием", "x_uk": "Чай я п'ю із задоволенням"}),
    6222: (LIST, {"t_ru": "правда, правдивый", "t_uk": "правда, правдивий", "x_en": "That's true"}),
    478: (LIST + "; «сын или дочь» — пояснение; «Das Kind spielt» — пример ни о чём", {
        "t_ru": "ребёнок", "t_uk": "дитина", "t_tr": "çocuk",
        **all_x("Das Kind schläft schon", "Ребёнок уже спит", "Дитина вже спить", "The child is already asleep",
                "Çocuk çoktan uyudu", "Dziecko już śpi", "Il bambino dorme già", "El niño ya está dormido",
                "L'enfant dort déjà", "Dítě už spí")}),
    166: (LIST + "; «Wir reden darüber» — «поговорим об этом»", {
        "t_ru": "об этом, над этим", "t_uk": "про це, над цим", "t_en": "about it, over it",
        "t_tr": "bunun hakkında", "t_pl": "o tym, nad tym", "t_it": "ne, di questo", "t_es": "de eso, sobre eso",
        "t_fr": "en, de cela", "t_cs": "o tom, nad tím",
        "x_ru": "Мы поговорим об этом", "x_uk": "Ми поговоримо про це", "x_en": "We'll talk about it",
        "x_tr": "Bunu konuşuruz", "x_pl": "Porozmawiamy o tym", "x_fr": "On en parle",
        "x_cs": "Promluvíme si o tom"}),
    10027: (LIST + "; «Я лучше буду пить чай» — калька", {
        "t_ru": "лучше, охотнее", "t_uk": "краще, охочіше", "t_en": "rather", "t_tr": "tercihen, daha çok",
        "t_pl": "raczej, chętniej", "t_it": "piuttosto", "t_es": "mejor, más bien", "t_fr": "plutôt",
        "t_cs": "raději",
        "x_ru": "Я лучше выпью чаю, чем кофе", "x_uk": "Я краще вип'ю чаю, ніж кави"}),
    475: (LIST + "; «узнавать» — это erkennen", {"t_ru": "знать, быть знакомым", "t_uk": "знати",
                                                "t_en": "to know", "t_tr": "tanımak", "t_pl": "znać"}),
    163: ("порча знаний: «Dank dir» — это предлог dank, «благодаря тебе», а перевод учил «спасибо тебе»", {
        "t_ru": "спасибо, благодарность", "t_uk": "подяка, спасибі", "t_en": "thanks", "t_tr": "teşekkür",
        "t_pl": "podziękowanie",
        **all_x("Vielen Dank!", "Большое спасибо!", "Велике спасибі!", "Thanks a lot!", "Çok teşekkürler!",
                "Wielkie dzięki!", "Grazie mille!", "¡Muchas gracias!", "Merci beaucoup!", "Moc děkuju!")}),
    875: (LIST, {"t_ru": "город", "t_uk": "місто"}),
    284: (LIST, {"t_ru": "вопрос", "t_uk": "питання", "t_en": "question", "t_tr": "soru", "t_pl": "pytanie",
                 "t_it": "la domanda", "t_es": "la pregunta"}),
    949: ("пояснение «при указании времени» — не перевод", {
        "t_ru": "часы, час", "t_uk": "годинник, година", "t_en": "clock, o'clock", "t_tr": "saat",
        "t_pl": "zegar, godzina", "t_it": "l'orologio, l'ora", "t_es": "el reloj, la hora",
        "t_fr": "l'heure, la montre", "x_en": "It's three o'clock", "x_pl": "Jest godzina trzecia"}),
    504: (LIST, {"t_ru": "голова", "t_uk": "голова", "t_en": "head", "t_pl": "głowa"}),
    244: (LIST + "; uk «керувати автом» — не по-украински", {
        "t_ru": "ехать, водить", "t_uk": "їхати, їздити", "t_en": "to drive, to go", "t_tr": "gitmek, araba sürmek",
        "t_pl": "jechać, jeździć", "t_it": "andare, guidare", "t_es": "ir, conducir", "t_fr": "aller, conduire",
        "t_cs": "jet, jezdit"}),
    1376: (LIST, {"t_ru": "конец", "t_uk": "кінець", "t_en": "end", "t_tr": "son", "t_pl": "koniec",
                  "t_es": "el final, el fin"}),
    1493: (LIST, {"t_ru": "счастье, удача", "t_uk": "щастя, удача", "t_en": "luck, happiness",
                  "t_tr": "şans, mutluluk", "t_pl": "szczęście"}),
    872: (LIST + "; пример — будущее, как в украинском", {
        "t_ru": "позже, потом", "t_uk": "пізніше, потім", "t_en": "later", "t_tr": "daha sonra", "t_pl": "później",
        "x_ru": "Мы поедим позже", "x_en": "We'll eat later", "x_cs": "Najíme se později"}),
    92: (LIST + "; «заболевать» — другое употребление; «по электронной почте» — канцелярски", {
        "t_ru": "получать, получить", "t_uk": "отримувати, отримати", "t_en": "to get, to receive",
        "t_tr": "almak", "t_pl": "dostawać, dostać", "t_it": "ricevere", "t_es": "recibir", "t_fr": "recevoir",
        "t_cs": "dostat", "x_ru": "Я получил письмо", "x_uk": "Я отримав листа"}),
    74: (LIST + "; «почти» — не перевод bald", {"t_ru": "скоро", "t_uk": "скоро, невдовзі", "t_en": "soon",
                                               "t_tr": "yakında", "t_pl": "wkrótce, niedługo"}),
    6228: (TWO + " («широкий» — об одежде, своя строка)", {
        "t_ru": "далеко, далёкий", "t_uk": "далеко, далекий", "t_en": "far", "t_tr": "uzak",
        "t_pl": "daleko, daleki", "t_it": "lontano", "t_es": "lejos, lejano", "t_fr": "loin, lointain",
        "t_cs": "daleko, daleký"}),
    14891: (LIST + "; пометка «(hovor.)» в переводе; «The guys» — это не Jungs", {
        "t_ru": "мальчик, парень", "t_uk": "хлопчик, хлопець", "t_en": "boy", "t_tr": "erkek çocuk, oğlan",
        "t_pl": "chłopiec, chłopak", "t_it": "il ragazzo, il bambino", "t_es": "el chico, el niño",
        "t_cs": "chlapec, kluk", "x_en": "The boys are playing football"}),
    880: (TWO + " («идти к лицу», «быть написанным» — свои строки); «Ich stehe hier» — пример ни о чём", {
        "t_ru": "стоять, находиться", "t_uk": "стояти", "t_en": "to stand", "t_tr": "ayakta durmak, bulunmak",
        "t_pl": "stać", "t_it": "stare in piedi, trovarsi", "t_es": "estar de pie", "t_fr": "être debout",
        "t_cs": "stát",
        **all_x("Wir stehen an der Haltestelle", "Мы стоим на остановке", "Ми стоїмо на зупинці",
                "We're standing at the bus stop", "Durakta duruyoruz", "Stoimy na przystanku",
                "Siamo alla fermata", "Estamos en la parada", "Nous sommes à l'arrêt", "Stojíme na zastávce")}),
    119: (LIST, {"t_ru": "немного, чуть-чуть", "t_en": "a little, a bit", "t_tr": "biraz", "t_pl": "trochę",
                 "t_it": "un po'", "t_es": "un poco", "t_cs": "trochu", "x_en": "I'd like a little sugar"}),
    62: ("uk «автомобілем» — книжно, говорят «машиною»", {"x_uk": "Вона їздить на роботу машиною"}),
    191: (LIST + "; «мы лучше остаёмся дома» — калька", {
        "t_ru": "на улице, снаружи", "t_uk": "надворі, на вулиці", "t_en": "outside", "t_tr": "dışarıda",
        "t_pl": "na zewnątrz, na dworze", "t_it": "fuori", "t_es": "fuera, afuera",
        "x_ru": "На улице идёт дождь, поэтому лучше останемся дома",
        "x_uk": "Надворі йде дощ, тому краще залишимося вдома"}),
    770: (TWO + " («смело» — частица ruhig, своя строка)", {
        "t_ru": "спокойный, тихий", "t_uk": "спокійний, тихий", "t_en": "quiet, calm", "t_tr": "sakin, sessiz"}),
    42: (LIST, {"t_ru": "работать", "t_uk": "працювати", "t_tr": "çalışmak"}),
    641: (LIST + "; «фамилия» — это Nachname", {
        "t_ru": "имя, название", "t_uk": "ім'я, назва", "t_en": "name", "t_tr": "ad, isim", "t_pl": "imię, nazwa",
        "t_cs": "jméno, název"}),
    536: (LIST, {"t_ru": "длинный, долгий", "t_uk": "довгий, тривалий", "t_en": "long", "t_tr": "uzun",
                 "t_pl": "długi"}),
    871: (LIST, {"t_ru": "поздно, поздний", "t_uk": "пізно, пізній", "t_en": "late", "t_tr": "geç",
                 "t_pl": "późno, późny", "x_en": "It's too late"}),
    376: (LIST + "; «gives me her hand» — по-английски жмут руку", {
        "t_ru": "рука", "t_uk": "рука", "t_pl": "ręka, dłoń", "x_en": "She shakes my hand"}),
    1051: (EN, {"t_en": "where from", "x_en": "Where are you from?"}),
    900: (LIST, {"t_ru": "искать", "t_uk": "шукати", "t_en": "to look for", "t_tr": "aramak", "t_pl": "szukać"}),
    524: (LIST, {"t_ru": "короткий", "t_uk": "короткий", "t_en": "short", "t_tr": "kısa", "t_pl": "krótki",
                 "t_fr": "court"}),
    8735: (LIST + "; пометка «(fam.)» в переводе", {
        "t_ru": "работа, подработка", "t_uk": "робота, підробіток", "t_en": "job", "t_tr": "iş", "t_pl": "praca",
        "t_it": "il lavoro", "t_es": "el trabajo", "t_fr": "le boulot, le travail", "t_cs": "práce, brigáda"}),
    861: (LIST, {"t_ru": "играть", "t_uk": "грати", "t_en": "to play", "t_tr": "oynamak, çalmak",
                 "t_pl": "grać, bawić się", "t_it": "giocare, suonare", "t_es": "jugar, tocar"}),
    983: (LIST + "; «расслышать» — другое употребление", {
        "t_ru": "понимать", "t_uk": "розуміти", "t_en": "to understand", "t_tr": "anlamak", "t_pl": "rozumieć",
        "t_es": "entender", "t_cs": "rozumět", "x_en": "I don't understand"}),
}

SPLIT_LATER = {
    6228: ["weit = широкий, свободный (об одежде)"],
    880: ["stehen = идти к лицу (Das steht dir)", "stehen = быть написанным (Was steht da?)"],
    770: ["ruhig = смело (Du kannst ruhig fragen)"],
}
