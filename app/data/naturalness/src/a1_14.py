"""A1, блок 14: слова 521–560 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
TWO = "в строке два разных слова — оставлено главное, второе — отдельной строкой (блок деления)"
EN = "английский пример: так не говорят о том, что происходит сейчас / будет"
DULL = "пример ни о чём («X ist Y») → фраза из жизни"
SAME = "пример совпадал с примером другого слова — у каждого свой"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    920: (LIST + "; " + EN, {
        "t_ru": "звонить, говорить по телефону", "t_uk": "дзвонити, телефонувати", "t_en": "to phone, to be on the phone",
        "t_tr": "telefonla konuşmak", "t_pl": "dzwonić, rozmawiać przez telefon", "t_it": "telefonare",
        "t_es": "hablar por teléfono", "x_en": "I'm on the phone with my mum"}),
    2514: (LIST, {"t_ru": "багаж", "t_uk": "багаж", "t_en": "luggage", "t_tr": "bagaj", "t_pl": "bagaż"}),
    928: (LIST + "; «слова песни» — другое значение; " + DULL, {
        "t_ru": "текст", "t_uk": "текст", "t_en": "text", "t_tr": "metin", "t_pl": "tekst", "t_es": "el texto",
        "t_fr": "le texte",
        **all_x("Den Text verstehe ich nicht", "Этот текст я не понимаю", "Цей текст я не розумію",
                "I don't understand this text", "Bu metni anlamıyorum", "Nie rozumiem tego tekstu",
                "Non capisco questo testo", "No entiendo este texto", "Je ne comprends pas ce texte",
                "Tomu textu nerozumím")}),
    8788: ("для A1 Führung — это экскурсия; пример про «руководство компании» — канцелярский", {
        "t_ru": "экскурсия, руководство", "t_uk": "екскурсія, керівництво", "t_en": "guided tour, management",
        "t_tr": "rehberli tur, yönetim", "t_pl": "oprowadzanie, kierownictwo",
        "t_it": "la visita guidata, la direzione", "t_es": "la visita guiada, la dirección",
        "t_fr": "la visite guidée, la direction", "t_cs": "prohlídka s průvodcem, vedení",
        **all_x("Gibt es heute eine Führung durch das Schloss?", "Сегодня есть экскурсия по замку?",
                "Сьогодні є екскурсія замком?", "Is there a guided tour of the castle today?",
                "Bugün şatoda rehberli tur var mı?", "Czy dziś jest oprowadzanie po zamku?",
                "Oggi c'è una visita guidata del castello?", "¿Hay hoy una visita guiada al castillo?",
                "Il y a une visite guidée du château aujourd'hui?", "Je dnes prohlídka zámku s průvodcem?")}),
    643: (LIST, {"t_ru": "мокрый", "t_uk": "мокрий", "t_en": "wet", "t_tr": "ıslak", "t_pl": "mokry"}),
    73: (LIST + "; «Мы встречаемся на вокзале» — калька", {
        "t_ru": "вокзал", "t_uk": "вокзал", "t_en": "station, train station", "t_tr": "tren istasyonu, gar",
        "t_pl": "dworzec", "x_ru": "Встретимся на вокзале", "x_uk": "Зустрінемося на вокзалі",
        "x_en": "Let's meet at the station"}),
    783: (LIST + "; «сет в теннисе, набор» — другие значения; " + DULL, {
        "t_ru": "предложение, фраза", "t_uk": "речення, фраза", "t_en": "sentence", "t_tr": "cümle", "t_pl": "zdanie",
        "t_it": "la frase", "t_es": "la frase, la oración", "t_fr": "la phrase", "t_cs": "věta",
        **all_x("Bilde einen Satz mit diesem Wort", "Составь предложение с этим словом", "Склади речення з цим словом",
                "Make a sentence with this word", "Bu kelimeyle bir cümle kur", "Ułóż zdanie z tym słowem",
                "Fai una frase con questa parola", "Haz una frase con esta palabra", "Fais une phrase avec ce mot",
                "Vytvoř větu s tímto slovem")}),
    12523: ("«Mein Gewicht ist zu hoch» — по-немецки так не говорят; «гиря» — другое значение", {
        "t_ru": "вес", "t_uk": "вага", "t_en": "weight", "t_tr": "ağırlık, kilo", "t_pl": "waga",
        **all_x("Ich muss auf mein Gewicht achten", "Мне нужно следить за весом", "Мені треба стежити за вагою",
                "I have to watch my weight", "Kiloma dikkat etmem lazım", "Muszę uważać na wagę",
                "Devo stare attento al peso", "Tengo que cuidar mi peso", "Je dois faire attention à mon poids",
                "Musím si hlídat váhu")}),
    1100: (LIST, {"t_ru": "сдавать, отдавать", "t_uk": "здавати, віддавати", "t_en": "to hand in, to hand over",
                  "t_tr": "teslim etmek", "t_pl": "oddać", "t_it": "consegnare", "t_es": "entregar",
                  "t_fr": "rendre, remettre", "t_cs": "odevzdat"}),
    34: (TWO + " («заявление в полицию» — своя строка); " + SAME + " (третий пример «Ich suche eine Wohnung»)", {
        "t_ru": "объявление, реклама", "t_uk": "оголошення, реклама", "t_en": "ad", "t_tr": "ilan, reklam",
        "t_pl": "ogłoszenie", "t_it": "l'annuncio", "t_es": "el anuncio", "t_fr": "l'annonce", "t_cs": "inzerát",
        **all_x("Ich habe eine Anzeige in der Zeitung gelesen", "Я прочитал объявление в газете",
                "Я прочитав оголошення в газеті", "I read an ad in the paper", "Gazetede bir ilan okudum",
                "Przeczytałem ogłoszenie w gazecie", "Ho letto un annuncio sul giornale",
                "He leído un anuncio en el periódico", "J'ai lu une annonce dans le journal",
                "Četl jsem inzerát v novinách")}),
    1606: (EN, {"x_en": "I'm opening an account"}),
    1997: (TWO + " («переодеваться» — sich umziehen, своя строка)", {
        "t_ru": "переезжать", "t_uk": "переїжджати", "t_en": "to move house", "t_tr": "taşınmak",
        "t_pl": "przeprowadzać się", "t_it": "traslocare", "t_es": "mudarse", "t_fr": "déménager",
        "t_cs": "stěhovat se"}),
    565: (EN, {"x_en": "The trees blossom in May"}),
    14985: (LIST, {"t_ru": "жена", "t_uk": "дружина", "t_tr": "eş, karı", "t_pl": "żona"}),
    1695: (LIST + "; «Я охотно участвую» — калька", {
        "t_ru": "участвовать, присоединяться", "t_en": "to join in, to take part", "t_tr": "katılmak",
        "t_pl": "brać udział, przyłączyć się", "t_it": "partecipare", "t_es": "participar, apuntarse",
        "t_cs": "přidat se, zúčastnit se",
        "x_ru": "Я с удовольствием поучаствую", "x_uk": "Я із задоволенням долучуся", "x_en": "I'd love to join in"}),
    248: (EN, {"t_en": "bike, bicycle", "x_en": "He goes by bike"}),
    1534: (SAME + " (willkommen: «Herzlich willkommen!»); " + LIST, {
        "t_ru": "тёплый, сердечный", "t_uk": "теплий, сердечний", "t_en": "warm, cordial", "t_tr": "sıcak, içten",
        "t_pl": "serdeczny", "t_it": "caloroso, cordiale", "t_es": "cordial, caluroso", "t_fr": "chaleureux",
        **all_x("Vielen Dank für den herzlichen Empfang!", "Спасибо за тёплый приём!", "Дякую за теплий прийом!",
                "Thank you for the warm welcome!", "Sıcak karşılamanız için teşekkürler!",
                "Dziękuję za serdeczne przyjęcie!", "Grazie per la calorosa accoglienza!",
                "¡Gracias por el caluroso recibimiento!", "Merci pour l'accueil chaleureux!",
                "Děkujeme za srdečné přijetí!")}),
    8797: (LIST, {"t_ru": "коллега", "t_uk": "колега", "t_en": "colleague", "t_tr": "iş arkadaşı, meslektaş",
                  "t_pl": "kolega, współpracownik"}),
    454: (EN, {"x_en": "It's hot in July"}),
    1141: (LIST + "; " + EN, {"t_ru": "прибытие, приезд", "t_uk": "прибуття, приїзд", "t_tr": "varış",
                              "t_pl": "przyjazd, przylot", "x_en": "Arrival is at 3 pm", "x_uk": "Прибуття о 15:00"}),
    55: (EN + "; uk «до моря» — по-украински «на море»", {
        "x_en": "In August we're going to the seaside", "x_uk": "У серпні ми їдемо на море"}),
    1776: (LIST, {"t_ru": "экзамен, проверка", "t_uk": "іспит, перевірка", "t_en": "exam, test", "t_tr": "sınav",
                  "t_pl": "egzamin", "t_it": "l'esame", "t_es": "el examen", "t_fr": "l'examen", "t_cs": "zkouška"}),
    598: (LIST, {"t_ru": "принести с собой, захватить", "t_uk": "принести з собою", "t_en": "to bring along",
                 "t_tr": "yanında getirmek", "t_pl": "przynieść ze sobą", "x_ru": "Захвати, пожалуйста, хлеб"}),
    9753: (LIST, {"t_ru": "клиент, покупатель", "t_uk": "клієнт, покупець", "t_tr": "müşteri", "t_pl": "klient",
                  "x_en": "The customer is unhappy"}),
    9461: ("uk пример переводил другую фразу — пропала «информатика в Берлине»; " + LIST, {
        "t_ru": "учиться в вузе, изучать", "t_uk": "навчатися в університеті, вивчати", "t_en": "to study",
        "t_tr": "üniversitede okumak", "t_pl": "studiować", "t_fr": "étudier, faire des études",
        "x_ru": "Я учусь на информатике в Берлине", "x_uk": "Я вивчаю інформатику в Берліні",
        "x_tr": "Berlin'de bilişim okuyorum"}),
    2226: (LIST, {"t_ru": "выход", "t_uk": "вихід", "t_en": "exit, way out", "t_tr": "çıkış", "t_pl": "wyjście",
                  "t_it": "l'uscita", "t_es": "la salida", "t_fr": "la sortie", "t_cs": "východ"}),
    235: (LIST, {"t_ru": "взрослый", "t_uk": "дорослий", "t_tr": "yetişkin", "t_pl": "dorosły", "t_it": "l'adulto",
                 "t_es": "el adulto", "t_fr": "l'adulte", "t_cs": "dospělý", "x_tr": "Sadece yetişkinler için"}),
    800: (LIST, {"t_ru": "быть вкусным", "t_uk": "смакувати, бути смачним", "t_en": "to taste", "t_tr": "tadı olmak",
                 "t_pl": "smakować", "t_it": "avere un buon sapore", "t_es": "saber", "t_fr": "avoir bon goût"}),
    396: (LIST, {"t_ru": "светлый, яркий", "t_uk": "світлий, яскравий", "t_en": "bright, light",
                 "t_tr": "aydınlık, parlak", "t_pl": "jasny", "t_it": "luminoso, chiaro", "t_es": "luminoso, claro",
                 "t_fr": "clair, lumineux", "t_cs": "světlý, jasný"}),
    1359: (TWO + " («вступать в бизнес» — своя строка)", {
        "t_ru": "садиться, входить", "t_uk": "сідати, заходити", "t_en": "to get in, to get on", "t_tr": "binmek",
        "t_pl": "wsiadać"}),
    603: (SAME + " (Dienstag: «…habe ich Kurs»)", {
        **all_x("Am Mittwoch gehe ich zum Zahnarzt", "В среду я иду к зубному", "У середу я йду до стоматолога",
                "I'm going to the dentist on Wednesday", "Çarşamba günü dişçiye gidiyorum", "W środę idę do dentysty",
                "Mercoledì vado dal dentista", "El miércoles voy al dentista", "Mercredi, je vais chez le dentiste",
                "Ve středu jdu k zubaři")}),
    811: (LIST + "; " + DULL, {
        "t_ru": "ботинок, туфля", "t_uk": "черевик, туфля",
        **all_x("Die Schuhe sind zu klein", "Ботинки малы", "Черевики замалі", "The shoes are too small",
                "Ayakkabılar çok küçük", "Te buty są za małe", "Le scarpe sono troppo piccole",
                "Los zapatos me quedan pequeños", "Les chaussures sont trop petites", "Boty jsou moc malé")}),
    18160: (LIST, {"t_ru": "квартира, апартаменты", "t_uk": "квартира, апартаменти", "t_en": "apartment, flat",
                   "t_tr": "daire", "t_pl": "apartament, mieszkanie", "t_it": "l'appartamento", "t_es": "el apartamento",
                   "t_fr": "l'appartement, le studio", "t_cs": "apartmán, byt"}),
    17097: ("шесть значений, включая неуместное для A1 «половой акт» → главное: «движение»", {
        "t_ru": "движение, транспорт", "t_uk": "рух, транспорт", "t_en": "traffic", "t_tr": "trafik",
        "t_pl": "ruch, ruch drogowy", "t_it": "il traffico", "t_es": "el tráfico", "t_fr": "la circulation, le trafic",
        "t_cs": "provoz, doprava"}),
    1083: (LIST + "; «В настоящее время я работаю здесь» — книжно", {
        "t_ru": "сейчас, в настоящее время", "t_uk": "зараз", "t_en": "currently, at the moment", "t_tr": "şu anda",
        "t_pl": "obecnie", "t_it": "attualmente, al momento", "t_es": "actualmente, de momento",
        "t_fr": "actuellement, en ce moment", "t_cs": "momentálně",
        "x_ru": "Сейчас я работаю здесь", "x_en": "I'm working here at the moment"}),
    1177: (SAME + " (kaputt — «… ist kaputt»)", {
        "t_en": "lift, elevator",
        **all_x("Wir nehmen den Aufzug", "Поедем на лифте", "Поїдемо ліфтом", "Let's take the lift",
                "Asansöre binelim", "Pojedźmy windą", "Prendiamo l'ascensore", "Cojamos el ascensor",
                "Prenons l'ascenseur", "Pojedeme výtahem")}),
}

SPLIT_LATER = {
    34: ["die Anzeige = заявление в полицию (Anzeige erstatten)"],
    1997: ["sich umziehen = переодеваться"],
    1359: ["einsteigen = вступить в дело"],
}
