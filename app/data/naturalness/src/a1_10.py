"""A1, блок 10: слова 361–400 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
TWO = "в строке два разных слова — оставлено главное, второе — отдельной строкой (блок деления)"
EN = "английский пример: так не говорят о том, что происходит сейчас / будет"
SAME = "пример почти совпадал с примером другого слова — у каждого свой"
MARK = "пометка «(coloq.)/(fam.)/(hovor.)» в переводе"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    18610: (LIST, {"t_ru": "секунда", "t_uk": "секунда", "t_en": "second", "t_tr": "saniye", "t_pl": "sekunda",
                   "t_it": "il secondo"}),
    1431: (LIST, {"t_en": "plane, airplane", "x_en": "The plane lands at 3 pm"}),
    18611: (LIST + "; «Это длится вечно» — калька", {
        "t_ru": "вечно, целую вечность", "t_uk": "вічно, цілу вічність", "t_en": "forever, for ages",
        "t_tr": "sonsuza kadar", "t_pl": "wiecznie",
        "x_ru": "Это длится целую вечность", "x_uk": "Це триває цілу вічність"}),
    748: (LIST + "; «правый» в политике — другое значение", {
        "t_ru": "направо, справа", "t_uk": "праворуч, справа", "t_en": "right, on the right", "t_tr": "sağa, sağda",
        "t_pl": "w prawo, po prawej", "t_it": "a destra", "t_es": "a la derecha", "t_fr": "à droite",
        "t_cs": "doprava, vpravo"}),
    1022: (EN, {"x_en": "She's having a glass of wine"}),
    1463: (LIST, {"t_ru": "принадлежать", "t_uk": "належати", "t_en": "to belong", "t_tr": "ait olmak",
                  "t_pl": "należeć", "t_it": "appartenere", "t_es": "pertenecer", "t_fr": "appartenir, être à",
                  "x_en": "The book is mine"}),
    33: (LIST, {"t_ru": "отвечать, ответить", "t_en": "to answer, to reply", "t_tr": "cevap vermek",
                "t_pl": "odpowiadać, odpowiedzieć"}),
    1284: (LIST, {"t_ru": "взгляд, вид", "t_uk": "погляд, вид", "t_en": "look, view", "t_tr": "bakış, manzara",
                  "t_pl": "spojrzenie, widok", "t_it": "lo sguardo, la vista", "t_es": "la mirada, la vista",
                  "t_fr": "le regard, la vue"}),
    461: (SAME + " (Handy: «Mein Handy ist kaputt»); «вымотанный» — другое употребление", {
        "t_ru": "сломанный, испорченный", "t_uk": "зламаний, несправний", "t_en": "broken", "t_tr": "bozuk",
        "t_pl": "zepsuty", "t_it": "rotto, guasto", "t_es": "roto, estropeado", "t_fr": "cassé, en panne",
        "t_cs": "rozbitý",
        **all_x("Die Waschmaschine ist kaputt", "Стиральная машина сломалась", "Пральна машина зламалася",
                "The washing machine is broken", "Çamaşır makinesi bozuk", "Pralka jest zepsuta",
                "La lavatrice è rotta", "La lavadora está estropeada", "La machine à laver est en panne",
                "Pračka je rozbitá")}),
    7: (LIST, {"t_ru": "внимание, осторожно", "t_uk": "увага, обережно", "t_en": "attention, watch out",
               "t_tr": "dikkat", "t_pl": "uwaga", "t_it": "attenzione", "t_es": "atención", "t_fr": "attention",
               "t_cs": "pozor"}),
    1053: (LIST, {"t_ru": "жить", "t_en": "to live", "t_tr": "oturmak"}),
    1087: ("uk «Це другий день» — потеряно «уже»", {"x_uk": "Це вже другий день",
                                                   "x_en": "It's already the second day"}),
    105: (LIST + "; " + EN, {"t_ru": "навещать, посещать", "t_uk": "відвідувати, навідувати", "t_en": "to visit",
                             "t_tr": "ziyaret etmek", "t_pl": "odwiedzać", "t_it": "visitare, andare a trovare",
                             "t_es": "visitar", "t_fr": "rendre visite à, visiter", "t_cs": "navštívit, navštěvovat",
                             "x_en": "We're visiting our grandmother"}),
    344: (SAME + " (Wasser: стакан воды); " + LIST, {
        "t_ru": "стакан, стекло", "t_uk": "склянка, скло", "t_en": "glass", "t_tr": "bardak, cam",
        "t_pl": "szklanka, szkło", "t_it": "il bicchiere, il vetro", "t_es": "el vaso, el vidrio", "t_fr": "le verre",
        "t_cs": "sklenice, sklo",
        **all_x("Stell die Gläser bitte auf den Tisch", "Поставь, пожалуйста, стаканы на стол",
                "Постав, будь ласка, склянки на стіл", "Put the glasses on the table, please",
                "Bardakları masaya koy lütfen", "Postaw, proszę, szklanki na stół",
                "Metti i bicchieri sul tavolo, per favore", "Pon los vasos en la mesa, por favor",
                "Mets les verres sur la table, s'il te plaît", "Dej prosím sklenice na stůl")}),
    530: (LIST, {"t_en": "kitchen", "t_tr": "mutfak"}),
    50: (LIST, {"t_ru": "задание, задача", "t_uk": "завдання, задача", "t_en": "task, exercise",
                "t_tr": "görev, ödev", "t_pl": "zadanie", "t_it": "il compito, l'esercizio",
                "t_es": "la tarea, el ejercicio", "t_fr": "la tâche, l'exercice", "t_cs": "úkol, úloha",
                "x_en": "This task isn't hard"}),
    10110: ("«Congratulations on your birthday» — так не говорят", {
        "t_ru": "поздравление", "t_uk": "вітання", "t_en": "congratulations, best wishes", "t_tr": "tebrik",
        "t_pl": "gratulacje, życzenia", "t_it": "gli auguri", "t_es": "la felicitación",
        "t_fr": "les félicitations, les vœux", "x_en": "Best wishes on your birthday!"}),
    261: (LIST + "; " + EN, {"t_ru": "праздновать, отмечать", "t_uk": "святкувати, відзначати",
                             "t_en": "to celebrate, to party", "t_tr": "kutlamak", "t_pl": "świętować",
                             "t_es": "celebrar, festejar", "t_fr": "fêter, faire la fête", "t_cs": "slavit",
                             "x_ru": "Мы отмечаем в субботу", "x_en": "We're celebrating on Saturday"}),
    6389: (TWO + " (erst — «первый»; «только, лишь» — наречие erst, своя строка)", {
        "t_ru": "первый", "t_uk": "перший", "t_en": "first", "t_tr": "ilk", "t_pl": "pierwszy", "t_it": "primo",
        "t_es": "primero", "t_fr": "premier", "t_cs": "první"}),
    86: (SAME + " («…beginnt um acht» — у четырёх слов); " + LIST, {
        "t_ru": "начинать, начинаться", "t_en": "to begin, to start", "t_tr": "başlamak",
        "t_pl": "zaczynać, zaczynać się",
        **all_x("Wann beginnt die Schule?", "Когда начинается школа?", "Коли починається школа?",
                "When does school start?", "Okul ne zaman başlıyor?", "Kiedy zaczyna się szkoła?",
                "Quando comincia la scuola?", "¿Cuándo empieza el colegio?", "Quand commence l'école?",
                "Kdy začíná škola?")}),
    265: (MARK + "; «хочу сейчас только смотреть телевизор» — калька", {
        "t_es": "ver la televisión, ver la tele", "t_fr": "regarder la télévision, regarder la télé",
        "t_cs": "dívat se na televizi",
        "x_ru": "Сейчас я хочу просто посмотреть телевизор", "x_uk": "Зараз я хочу просто подивитися телевізор"}),
    1696: (TWO + " («выматывать» — своя строка)", {
        "t_ru": "брать с собой, подвозить", "t_uk": "брати з собою, підвозити", "t_en": "to take along, to give a lift",
        "t_tr": "yanına almak", "t_pl": "zabierać ze sobą", "t_it": "portare con sé, dare un passaggio",
        "t_es": "llevar, llevarse", "t_fr": "emmener, emporter"}),
    8: (EN, {"x_en": "What's your address?"}),
    6396: (LIST, {"t_ru": "напоминать, вспоминать", "t_uk": "нагадувати, згадувати", "t_pl": "przypominać, pamiętać",
                  "t_fr": "rappeler, se souvenir", "t_cs": "připomínat, vzpomínat si"}),
    1229: (LIST, {"t_ru": "означать, значить", "t_uk": "означати", "t_en": "to mean", "t_tr": "anlamına gelmek",
                  "t_pl": "znaczyć, oznaczać"}),
    357: (LIST, {"t_ru": "группа, компания", "t_uk": "група, компанія", "t_en": "group", "t_tr": "grup",
                 "t_pl": "grupa", "t_it": "il gruppo", "t_es": "el grupo", "t_fr": "le groupe", "t_cs": "skupina"}),
    14929: (LIST, {"t_ru": "муж", "t_en": "husband", "t_tr": "koca, eş"}),
    1317: ("«Благодарю тебя» — книжно; «I thank you» — так не говорят", {
        "t_ru": "благодарить",
        **all_x("Ich möchte dir für deine Hilfe danken", "Хочу поблагодарить тебя за помощь",
                "Хочу подякувати тобі за допомогу", "I'd like to thank you for your help",
                "Yardımın için sana teşekkür etmek istiyorum", "Chcę ci podziękować za pomoc",
                "Voglio ringraziarti per l'aiuto", "Quiero agradecerte tu ayuda",
                "Je veux te remercier pour ton aide", "Chci ti poděkovat za pomoc")}),
    2126: ("«Ich bin zufrieden» без продолжения — пример ни о чём", {
        "t_ru": "довольный", "t_en": "satisfied, happy with", "t_tr": "memnun", "t_pl": "zadowolony",
        **all_x("Bist du mit dem Hotel zufrieden?", "Ты доволен отелем?", "Ти задоволений готелем?",
                "Are you happy with the hotel?", "Otelden memnun musun?", "Jesteś zadowolony z hotelu?",
                "Sei contento dell'hotel?", "¿Estás contento con el hotel?", "Tu es content de l'hôtel?",
                "Jsi spokojený s hotelem?")}),
    6400: (TWO + " («реально» — наречие echt, своя строка)", {
        "t_ru": "настоящий, подлинный", "t_uk": "справжній", "t_en": "real, genuine", "t_tr": "gerçek",
        "t_pl": "prawdziwy", "t_it": "vero, autentico", "t_es": "verdadero, auténtico", "t_fr": "vrai, véritable",
        "t_cs": "opravdový, skutečný"}),
    276: (LIST + "; «плоть» — другое значение", {
        "t_ru": "мясо", "t_uk": "м'ясо", "t_en": "meat", "t_pl": "mięso", "t_fr": "la viande",
        "x_en": "He doesn't eat meat"}),
    24: (LIST + "; «The offer is only this week» — так не говорят", {
        "t_ru": "предложение, акция", "t_uk": "пропозиція, акція", "t_en": "offer, special offer",
        "t_tr": "teklif, indirim", "t_pl": "oferta, promocja", "t_fr": "l'offre, la promotion",
        "t_cs": "nabídka, akce",
        "x_ru": "Предложение действует только на этой неделе", "x_en": "The offer is only valid this week"}),
    915: (EN + "; «Я беру такси» — калька, речь о будущем", {
        "x_ru": "Я возьму такси до вокзала", "x_uk": "Я візьму таксі до вокзалу",
        "x_en": "I'll take a taxi to the station"}),
}

SPLIT_LATER = {
    6389: ["erst = только, лишь (erst morgen)"],
    6400: ["echt = реально, правда (echt gut)"],
    1696: ["mitnehmen = выматывать (Das hat mich mitgenommen)"],
}
