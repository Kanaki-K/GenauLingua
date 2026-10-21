"""A2, блок 16: слова 601–640 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
SKEL = "пример-скелет («Mittags essen wir», «Ich übersetze den Text») — пусто"
EN = "английский пример: так не говорят"
WEAR = "«trägt …» — шаблон одежды; у каждой вещи свой пример"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    7143: ("«популярен у туристов» — язык путеводителя; " + LIST, {
        "t_ru": "регион, область", "t_uk": "регіон, область", "t_en": "region, area", "t_tr": "bölge",
        "t_pl": "region, okolica",
        **all_x("Aus welcher Region kommst du?", "Из какого ты региона?", "З якого ти регіону?",
                "Which region are you from?", "Hangi bölgedensin?", "Z jakiego regionu jesteś?", "Di che regione sei?",
                "¿De qué región eres?", "Tu viens de quelle région?", "Z jakého jsi regionu?")}),
    18216: (LIST, {"t_ru": "кастрюля, горшок", "t_uk": "каструля, горщик", "t_en": "pot, saucepan",
                   "t_tr": "tencere, saksı", "t_pl": "garnek, doniczka", "t_es": "la olla, la maceta",
                   "t_fr": "la casserole, le pot", "t_cs": "hrnec, květináč"}),
    15518: ("шестой пример про погоду; «холодный по тону» — пояснение; " + LIST, {
        "t_ru": "прохладный, сдержанный", "t_uk": "прохолодний, стриманий", "t_en": "cool, chilly", "t_tr": "serin",
        "t_pl": "chłodny",
        **all_x("Stell das Bier bitte kühl", "Поставь, пожалуйста, пиво в прохладное место",
                "Постав, будь ласка, пиво в прохолодне місце", "Please keep the beer cool",
                "Birayı serin bir yere koy lütfen", "Postaw piwo w chłodnym miejscu", "Metti la birra al fresco, per favore",
                "Pon la cerveza en un sitio fresco, por favor", "Mets la bière au frais, s'il te plaît",
                "Dej prosím pivo na chladné místo")}),
    355: (EN, {"x_en": "He's got the flu"}),
    458: ("«Ich schaue in den Kalender» — пусто", {**all_x(
        "Moment, ich schaue kurz in meinen Kalender", "Секунду, загляну в календарь", "Секунду, зазирну в календар",
        "Hang on, let me check my calendar", "Bir saniye, ajandama bakayım", "Chwileczkę, zajrzę do kalendarza",
        "Un attimo, guardo l'agenda", "Un momento, miro la agenda", "Une seconde, je regarde mon agenda",
        "Moment, podívám se do diáře")}),
    39: ("«… ist um die Ecke» — шаблон Park, Bushaltestelle", {**all_x(
        "Die Apotheke hat heute bis acht Uhr auf", "Аптека сегодня работает до восьми", "Аптека сьогодні працює до восьмої",
        "The pharmacy is open until 8 today", "Eczane bugün saat sekize kadar açık", "Apteka jest dziś czynna do ósmej",
        "La farmacia oggi è aperta fino alle otto", "La farmacia hoy abre hasta las ocho",
        "La pharmacie est ouverte jusqu'à 20 heures aujourd'hui", "Lékárna má dnes otevřeno do osmi")}),
    12620: ("«Духи пахнут очень хорошо, мне они нравятся» — длинно и книжно", {**all_x(
        "Dein Parfüm riecht gut", "Твои духи приятно пахнут", "Твої парфуми приємно пахнуть", "Your perfume smells nice",
        "Parfümün güzel kokuyor", "Twoje perfumy ładnie pachną", "Il tuo profumo ha un buon odore", "Tu perfume huele bien",
        "Ton parfum sent bon", "Tvůj parfém hezky voní")}),
    1404: ("перевод — список из шести слов", {
        "t_ru": "предмет, полка", "t_uk": "предмет, полиця", "t_en": "subject, compartment", "t_tr": "ders, bölme",
        "t_pl": "przedmiot, przegroda", "t_it": "la materia, lo scomparto", "t_es": "la asignatura, el compartimento",
        "t_fr": "la matière, le compartiment", "t_cs": "předmět, přihrádka"}),
    575: ("«Mathematik ist mein Lieblingsfach» — шаблон Fach («Welches Fach magst du am liebsten?»)", {**all_x(
        "In Mathematik bin ich leider schlecht", "По математике я, к сожалению, слабый",
        "З математики я, на жаль, слабкий", "Unfortunately I'm bad at maths", "Maalesef matematikte kötüyüm",
        "Niestety jestem słaby z matematyki", "Purtroppo in matematica vado male",
        "Por desgracia, se me dan mal las matemáticas", "Malheureusement, je suis nul en maths",
        "Z matematiky jsem bohužel špatný")}),
    14483: ("«Der Sänger singt wunderbar» — масло масляное", {**all_x(
        "Der Sänger war gestern im Fernsehen", "Этот певец вчера был по телевизору", "Цей співак учора був на телебаченні",
        "That singer was on TV yesterday", "Bu şarkıcı dün televizyondaydı", "Ten piosenkarz był wczoraj w telewizji",
        "Quel cantante ieri era in tv", "Ese cantante salió ayer en la tele", "Ce chanteur est passé à la télé hier",
        "Ten zpěvák byl včera v televizi")}),
    1222: (LIST, {"t_ru": "баскетбол", "t_uk": "баскетбол"}),
    1307: ("«Химия — это сложно» — по-русски о предмете так не говорят", {"x_ru": "Химия — сложный предмет"}),
    16194: ("«идёт в ратушу подать заявление» — в речи «в мэрию»; " + LIST, {
        "t_ru": "ратуша, мэрия", "t_uk": "ратуша, мерія", "t_en": "town hall", "t_tr": "belediye binası",
        "t_pl": "ratusz, urząd miasta",
        "x_ru": "Она идёт в мэрию подать заявление", "x_uk": "Вона йде до мерії подати заяву",
        "x_en": "She's going to the town hall to hand in an application"}),
    1321: ("«Пожалуйста, открой файл на своём компьютере» — инструкция", {**all_x(
        "Ich schicke dir die Datei per Mail", "Я пришлю тебе файл по почте", "Я надішлю тобі файл поштою",
        "I'll send you the file by email", "Dosyayı sana e-postayla gönderirim", "Wyślę ci plik mailem",
        "Ti mando il file per email", "Te mando el archivo por correo", "Je t'envoie le fichier par mail",
        "Pošlu ti ten soubor mailem")}),
    7167: ("«Mach die Tür zu» — шаблон aufmachen («Mach die Tür auf!»)", {**all_x(
        "Mach die Augen zu, ich habe eine Überraschung!", "Закрой глаза, у меня сюрприз!", "Закрий очі, у мене сюрприз!",
        "Close your eyes, I've got a surprise!", "Gözlerini kapat, sana bir sürprizim var!", "Zamknij oczy, mam niespodziankę!",
        "Chiudi gli occhi, ho una sorpresa!", "¡Cierra los ojos, que tengo una sorpresa!", "Ferme les yeux, j'ai une surprise!",
        "Zavři oči, mám překvapení!")}),
    2117: ("снова «о моде»; " + EN + " («I read a magazine about fashion»)", {**all_x(
        "Im Wartezimmer liegen alte Zeitschriften", "В приёмной лежат старые журналы", "У приймальні лежать старі журнали",
        "There are old magazines in the waiting room", "Bekleme odasında eski dergiler var",
        "W poczekalni leżą stare czasopisma", "In sala d'attesa ci sono vecchie riviste",
        "En la sala de espera hay revistas viejas", "Il y a de vieux magazines dans la salle d'attente",
        "V čekárně leží staré časopisy")}),
    2900: (SKEL + "; «переправлять на другой берег» — устар.", {
        "t_ru": "переводить", "t_uk": "перекладати", "t_en": "to translate", "t_tr": "çevirmek", "t_pl": "tłumaczyć",
        **all_x("Kannst du mir das übersetzen?", "Можешь мне это перевести?", "Можеш мені це перекласти?",
                "Can you translate that for me?", "Bunu bana çevirebilir misin?", "Możesz mi to przetłumaczyć?",
                "Me lo puoi tradurre?", "¿Me lo puedes traducir?", "Tu peux me traduire ça?", "Můžeš mi to přeložit?")}),
    601: (SKEL + "; " + LIST, {
        "t_ru": "в обед, в полдень", "t_uk": "опівдні, в обід",
        **all_x("Mittags habe ich nur eine halbe Stunde Pause", "В обед у меня всего полчаса перерыва",
                "В обід у мене лише пів години перерви", "I only get half an hour's break at lunchtime",
                "Öğlen sadece yarım saat molam var", "W południe mam tylko pół godziny przerwy",
                "A mezzogiorno ho solo mezz'ora di pausa", "Al mediodía solo tengo media hora de descanso",
                "À midi, je n'ai qu'une demi-heure de pause", "V poledne mám jen půl hodiny pauzu")}),
    516: ("«Wir halten an der Kreuzung» — пусто; «скрещивание» — другое значение", {
        "t_ru": "перекрёсток", "t_uk": "перехрестя", "t_en": "crossroads, junction", "t_tr": "kavşak",
        "t_pl": "skrzyżowanie",
        **all_x("An dieser Kreuzung passieren oft Unfälle", "На этом перекрёстке часто бывают аварии",
                "На цьому перехресті часто трапляються аварії", "There are often accidents at this junction",
                "Bu kavşakta sık sık kaza oluyor", "Na tym skrzyżowaniu często są wypadki",
                "A questo incrocio succedono spesso incidenti", "En este cruce hay accidentes a menudo",
                "Il y a souvent des accidents à ce carrefour", "Na téhle křižovatce se často stávají nehody")}),
    2956: (EN + " («I'm traveling tomorrow»); " + LIST, {
        "t_ru": "уезжать (в поездку)", "t_uk": "їхати в подорож", "t_en": "to go away (on a trip)",
        "t_tr": "seyahate çıkmak", "t_pl": "wyjechać", "x_en": "I'm going away tomorrow", "x_cs": "Zítra odjíždím"}),
    14031: (LIST, {"t_ru": "заметка, пометка", "t_uk": "нотатка, позначка", "t_en": "note", "t_tr": "not",
                   "t_pl": "notatka"}),
    635: (EN, {"x_en": "I'm free in the afternoon"}),
    1732: (LIST, {"t_ru": "оценка, нота", "t_uk": "оцінка, нота", "t_en": "mark, note", "t_tr": "not, nota",
                  "t_pl": "ocena, nuta"}),
    9495: ("«Die Schülerin hat gute Noten» — шаблон Note", {**all_x(
        "Die neue Schülerin kommt aus Spanien", "Новая ученица из Испании", "Нова учениця з Іспанії",
        "The new student is from Spain", "Yeni kız öğrenci İspanya'dan", "Nowa uczennica jest z Hiszpanii",
        "La nuova alunna viene dalla Spagna", "La alumna nueva es de España", "La nouvelle élève vient d'Espagne",
        "Nová žákyně je ze Španělska")}),
    7187: ("ru «очень экономична» — краткая форма книжная", {"x_ru": "Машина дешёвая, к тому же очень экономичная"}),
    2551: ("«Ich führe den Haushalt» — книжно; " + LIST, {
        "t_ru": "домашнее хозяйство, бюджет", "t_uk": "домашнє господарство, бюджет", "t_en": "household, housework",
        "t_tr": "ev işleri, bütçe", "t_pl": "prace domowe, budżet", "t_it": "la casa, le faccende domestiche",
        "t_es": "la casa, las tareas domésticas", "t_fr": "le ménage, le foyer", "t_cs": "domácnost, rozpočet",
        **all_x("Wer macht bei euch den Haushalt?", "Кто у вас занимается домашним хозяйством?",
                "Хто у вас веде господарство?", "Who does the housework in your house?", "Sizde ev işlerini kim yapıyor?",
                "Kto u was zajmuje się pracami domowymi?", "Chi si occupa della casa da voi?",
                "¿Quién hace las tareas domésticas en tu casa?", "Qui fait le ménage chez vous?",
                "Kdo se u vás stará o domácnost?")}),
    14035: (LIST, {"t_tr": "buyrun"}),
    17160: (EN + " («I pack my things for vacation»)", {"x_ru": "Я собираю вещи в отпуск",
                                                       "x_en": "I'm packing my things for the holiday"}),
    1479: (LIST, {"t_ru": "посуда", "t_uk": "посуд", "t_en": "dishes", "t_tr": "bulaşık", "t_pl": "naczynia"}),
    17162: (EN + " («away traveling»)", {"x_en": "My wife is away this week"}),
    737: (WEAR, {**all_x(
        "Der Pullover ist beim Waschen eingelaufen", "Свитер сел после стирки", "Светр сів після прання",
        "The jumper shrank in the wash", "Kazak yıkanınca çekti", "Sweter skurczył się w praniu",
        "Il maglione si è ristretto in lavatrice", "El jersey ha encogido al lavarlo", "Le pull a rétréci au lavage",
        "Svetr se srazil v pračce")}),
    994: ("«Vorgestern war es warm» — седьмой пример про погоду", {**all_x(
        "Vorgestern habe ich ihn noch gesehen", "Я его ещё позавчера видел", "Я його ще позавчора бачив",
        "I saw him just the day before yesterday", "Onu daha evvelsi gün gördüm", "Jeszcze przedwczoraj go widziałem",
        "L'ho visto ancora l'altro ieri", "Lo vi anteayer", "Je l'ai encore vu avant-hier",
        "Ještě předevčírem jsem ho viděl")}),
    1998: ("«Der Umzug war anstrengend» — пусто; " + LIST, {
        "t_ru": "переезд, шествие", "t_uk": "переїзд, хода", "t_en": "move, parade", "t_tr": "taşınma, geçit töreni",
        "t_pl": "przeprowadzka, pochód",
        **all_x("Hilfst du mir beim Umzug?", "Поможешь мне с переездом?", "Допоможеш мені з переїздом?",
                "Will you help me with the move?", "Taşınırken bana yardım eder misin?", "Pomożesz mi przy przeprowadzce?",
                "Mi aiuti con il trasloco?", "¿Me ayudas con la mudanza?", "Tu m'aides pour le déménagement?",
                "Pomůžeš mi se stěhováním?")}),
    15541: ("«Das Gewitter kam plötzlich» — книжно; " + LIST, {
        "t_ru": "гроза", "t_uk": "гроза", "t_en": "thunderstorm", "t_tr": "fırtına", "t_pl": "burza",
        **all_x("Bei Gewitter gehe ich nicht schwimmen", "В грозу я не хожу купаться", "У грозу я не ходжу купатися",
                "I don't go swimming in a thunderstorm", "Fırtınada yüzmeye gitmem", "W czasie burzy nie chodzę pływać",
                "Con il temporale non vado a nuotare", "Con tormenta no voy a nadar",
                "Quand il y a de l'orage, je ne vais pas me baigner", "Za bouřky nechodím plavat")}),
}

# zudem — письменное; говорят außerdem
REPLACE = [{"id": 7187, "by": 64, "lang": "de", "why": "zudem — письменное, в речи außerdem"}]

SPLIT_LATER = {}
