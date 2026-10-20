"""A1, блок 13: слова 481–520 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
TWO = "в строке два разных слова — оставлено главное, второе — отдельной строкой (блок деления)"
EN = "английский пример: так не говорят о том, что происходит сейчас / будет"
DULL = "пример ни о чём («X ist Y») → фраза из жизни"
SAME = "пример совпадал с примером другого слова — у каждого свой"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    1032: (LIST, {"t_tr": "hava", "t_it": "il tempo", "t_es": "el tiempo"}),
    443: (LIST, {"t_ru": "куртка, пиджак", "t_uk": "куртка, піджак", "t_en": "jacket", "t_tr": "ceket, mont",
                 "t_pl": "kurtka, marynarka"}),
    6558: (LIST, {"t_ru": "середина, центр", "t_en": "middle, centre", "t_tr": "orta", "t_pl": "środek",
                  "t_it": "il mezzo, il centro", "t_es": "el medio, el centro", "t_fr": "le milieu", "t_cs": "střed"}),
    138: (SAME + " (kaufen: «Ich kaufe Brot»)", {
        "t_ru": "хлеб", "t_uk": "хліб", "t_en": "bread", "t_pl": "chleb",
        **all_x("Zum Frühstück esse ich Brot mit Käse", "На завтрак я ем хлеб с сыром", "На сніданок я їм хліб із сиром",
                "For breakfast I have bread and cheese", "Kahvaltıda peynirli ekmek yerim",
                "Na śniadanie jem chleb z serem", "A colazione mangio pane e formaggio",
                "Para desayunar como pan con queso", "Au petit-déjeuner, je mange du pain avec du fromage",
                "K snídani jím chléb se sýrem")}),
    14957: (LIST + "; «Младенцы спят в коляске» — книжно", {
        "t_ru": "малыш, младенец", "t_uk": "немовля, малюк", "t_en": "baby", "t_tr": "bebek",
        "t_pl": "niemowlę, maluch", "t_it": "il bebè", "t_cs": "miminko",
        **all_x("Das Baby schläft im Kinderwagen", "Малыш спит в коляске", "Малюк спить у візочку",
                "The baby is sleeping in the pram", "Bebek bebek arabasında uyuyor", "Maluch śpi w wózku",
                "Il bebè dorme nella carrozzina", "El bebé duerme en el cochecito", "Le bébé dort dans le landau",
                "Miminko spí v kočárku")}),
    695: (TWO + " («документ» — Papiere, своя строка); пример ни о чём", {
        "t_ru": "бумага", "t_uk": "папір", "t_en": "paper", "t_tr": "kağıt", "t_pl": "papier", "t_it": "la carta",
        "t_es": "el papel", "t_fr": "le papier", "t_cs": "papír",
        **all_x("Hast du ein Blatt Papier für mich?", "У тебя есть для меня лист бумаги?", "Маєш для мене аркуш паперу?",
                "Do you have a sheet of paper for me?", "Bana bir kağıt verebilir misin?",
                "Masz dla mnie kartkę papieru?", "Hai un foglio di carta per me?", "¿Tienes una hoja de papel para mí?",
                "Tu as une feuille de papier pour moi?", "Máš pro mě list papíru?")}),
    599: (LIST + "; «We eat around noon» — не то", {
        "t_ru": "полдень, обед", "t_uk": "полудень, обід", "t_en": "noon, midday", "t_tr": "öğle", "t_pl": "południe",
        "t_it": "il mezzogiorno", "t_es": "el mediodía", "t_fr": "le midi", "t_cs": "poledne",
        "x_en": "We're having lunch"}),
    2372: (LIST, {"t_ru": "срочный, спешный", "t_uk": "терміновий", "t_en": "urgent, in a hurry", "t_tr": "acil",
                  "t_pl": "pilny", "t_it": "urgente, di fretta", "t_es": "urgente, con prisa", "t_fr": "pressé, urgent"}),
    13470: (LIST, {"t_ru": "столько, так много", "t_uk": "стільки, так багато", "t_en": "so much, that much",
                   "t_tr": "bu kadar", "t_pl": "tyle", "t_it": "tanto", "t_es": "tanto", "t_fr": "autant, tant",
                   "t_cs": "tolik"}),
    2552: ("немецкий пример с ошибкой: нужно «die Ukraine»; " + LIST, {
        "t_ru": "родина, родные края", "t_uk": "батьківщина, рідний край", "t_en": "home, homeland",
        "t_tr": "memleket, vatan", "t_pl": "ojczyzna, rodzinne strony", "t_it": "la patria",
        "t_es": "la patria, la tierra natal", "t_fr": "la patrie", "t_cs": "domov, vlast",
        "x_de": "Meine Heimat ist die Ukraine", "x_ru": "Моя родина — Украина", "x_uk": "Моя батьківщина — Україна",
        "x_en": "My homeland is Ukraine", "x_tr": "Benim memleketim Ukrayna", "x_pl": "Moją ojczyzną jest Ukraina",
        "x_it": "La mia patria è l'Ucraina", "x_es": "Mi patria es Ucrania", "x_fr": "Ma patrie, c'est l'Ukraine",
        "x_cs": "Můj domov je Ukrajina"}),
    432: ("немецкий пример: «mehr Information» — по-немецки «mehr Informationen»", {
        "x_de": "Ich brauche mehr Informationen", "x_ru": "Мне нужно больше информации",
        "x_uk": "Мені потрібно більше інформації", "x_en": "I need more information",
        "x_tr": "Daha fazla bilgiye ihtiyacım var", "x_pl": "Potrzebuję więcej informacji",
        "x_it": "Ho bisogno di più informazioni", "x_es": "Necesito más información",
        "x_fr": "J'ai besoin de plus d'informations", "x_cs": "Potřebuji víc informací"}),
    809: (LIST, {"t_en": "wardrobe, cupboard", "x_en": "The wardrobe is full"}),
    212: ("«Sie bekommt eine Einladung» — пример ни о чём", {
        **all_x("Danke für die Einladung!", "Спасибо за приглашение!", "Дякую за запрошення!",
                "Thanks for the invitation!", "Davet için teşekkürler!", "Dziękuję za zaproszenie!",
                "Grazie per l'invito!", "¡Gracias por la invitación!", "Merci pour l'invitation!",
                "Díky za pozvání!")}),
    13474: (SAME + " (kosten: «Wie viel kostet das?»); «почём» — просторечие", {
        "t_ru": "сколько", "t_uk": "скільки", "t_en": "how much, how many", "t_tr": "ne kadar, kaç", "t_pl": "ile",
        **all_x("Wie viel Zucker nimmst du?", "Сколько тебе сахара?", "Скільки тобі цукру?",
                "How much sugar do you take?", "Kaç şeker alırsın?", "Ile cukru słodzisz?",
                "Quanto zucchero prendi?", "¿Cuánto azúcar quieres?", "Combien de sucre tu prends?",
                "Kolik si dáš cukru?")}),
    12505: (LIST + "; it — книжно", {
        "t_ru": "пахнуть, нюхать", "t_uk": "пахнути, нюхати", "t_en": "to smell", "t_tr": "kokmak, koklamak",
        "t_pl": "pachnieć, wąchać", "t_it": "profumare, odorare", "t_cs": "vonět, čichat",
        "x_it": "I fiori profumano tantissimo"}),
    1128: (LIST + "; пример про «условия компании» — канцелярский", {
        "t_ru": "предлагать, угощать", "t_uk": "пропонувати, частувати", "t_en": "to offer",
        "t_tr": "sunmak, ikram etmek", "t_pl": "oferować, częstować",
        **all_x("Darf ich dir einen Kaffee anbieten?", "Можно предложить тебе кофе?", "Можна запропонувати тобі каву?",
                "Can I offer you a coffee?", "Sana bir kahve ikram edebilir miyim?", "Mogę ci zaproponować kawę?",
                "Posso offrirti un caffè?", "¿Te puedo ofrecer un café?", "Je peux te proposer un café?",
                "Můžu ti nabídnout kávu?")}),
    2103: (LIST + "; «Ты можешь это повторить, пожалуйста?» — калька", {
        "t_ru": "повторять, повторить", "x_ru": "Повтори, пожалуйста"}),
    1563: ("«Ich sitze im Internet» — по-немецки так не говорят", {
        **all_x("Ich habe das im Internet gefunden", "Я нашёл это в интернете", "Я знайшов це в інтернеті",
                "I found it on the internet", "Bunu internette buldum", "Znalazłem to w internecie",
                "L'ho trovato su internet", "Lo he encontrado en internet", "Je l'ai trouvé sur internet",
                "Našel jsem to na internetu")}),
    1266: (EN + "; «Я заказываю воду» — калька", {
        "x_ru": "Я закажу воду", "x_uk": "Я замовлю воду", "x_en": "I'll order a water", "x_pl": "Zamówię wodę"}),
    211: (TWO + " («загружать» — einladen = laden, своя строка)", {
        "t_ru": "приглашать, угощать", "t_uk": "запрошувати, пригощати", "t_en": "to invite, to treat",
        "t_tr": "davet etmek, ısmarlamak", "t_pl": "zapraszać, stawiać", "t_it": "invitare, offrire",
        "t_es": "invitar", "t_fr": "inviter", "t_cs": "pozvat, zvát", "x_en": "I'm inviting you"}),
    965: (SAME + " («… beginnt um neun» — у um и Kurs); " + LIST, {
        "t_ru": "урок, занятие", "t_uk": "урок, заняття", "t_en": "lesson, class", "t_tr": "ders",
        "t_pl": "lekcja, zajęcia", "t_it": "la lezione", "t_es": "la clase", "t_fr": "le cours",
        "t_cs": "vyučování, výuka",
        **all_x("Heute fällt der Unterricht aus", "Сегодня занятия отменяются", "Сьогодні заняття скасовуються",
                "There's no class today", "Bugün ders yok", "Dziś nie ma lekcji", "Oggi la lezione è annullata",
                "Hoy no hay clase", "Aujourd'hui, le cours est annulé", "Dnes odpadá vyučování")}),
    183: (EN, {"x_en": "I have a class on Tuesday"}),
    6633: (LIST + "; «мимо» — другое употребление", {
        "t_ru": "рядом", "t_uk": "поруч", "t_en": "next to it", "t_tr": "yanında", "t_pl": "obok",
        "t_it": "accanto", "t_es": "al lado", "t_fr": "à côté", "t_cs": "vedle"}),
    12121: (SAME + " (ещё одно «… um neun»); " + LIST, {
        "t_ru": "старт, начало", "t_uk": "старт, початок", "t_en": "start", "t_tr": "başlangıç, start",
        "t_pl": "start", "t_it": "la partenza, l'inizio", "t_es": "la salida, el comienzo",
        "t_fr": "le départ, le début", "t_cs": "start, začátek",
        **all_x("Der Start war nicht leicht", "Начало было непростым", "Початок був непростим", "The start wasn't easy",
                "Başlangıç kolay değildi", "Start nie był łatwy", "L'inizio non è stato facile",
                "El comienzo no fue fácil", "Le début n'a pas été facile", "Začátek nebyl snadný")}),
    1200: (LIST + "; «удостоверение личности» — канцелярски", {
        "t_ru": "удостоверение, документ", "t_uk": "посвідчення, документ", "t_en": "ID card, ID", "t_tr": "kimlik",
        "t_pl": "dowód osobisty, legitymacja", "t_it": "la carta d'identità", "t_es": "el carné de identidad",
        "t_fr": "la carte d'identité", "t_cs": "průkaz", "x_ru": "Покажи, пожалуйста, удостоверение"}),
    269: (LIST, {"t_ru": "температура, жар", "t_uk": "температура, жар", "t_en": "fever", "t_tr": "ateş",
                 "t_pl": "gorączka", "t_cs": "horečka, teplota"}),
    188: (SAME + " (Samstag: «Am … bin ich frei»)", {
        **all_x("Am Donnerstag habe ich Geburtstag", "В четверг у меня день рождения", "У четвер у мене день народження",
                "My birthday is on Thursday", "Perşembe günü doğum günüm", "W czwartek mam urodziny",
                "Giovedì è il mio compleanno", "El jueves es mi cumpleaños", "Jeudi, c'est mon anniversaire",
                "Ve čtvrtek mám narozeniny")}),
    1829: (LIST + "; " + DULL, {
        "t_ru": "табличка, вывеска", "t_uk": "табличка, вивіска", "t_en": "sign", "t_tr": "tabela, levha",
        "t_pl": "tabliczka, znak", "t_it": "il cartello, l'insegna", "t_es": "el letrero, el cartel",
        "t_fr": "le panneau, l'enseigne", "t_cs": "cedule, značka",
        **all_x("Was steht auf dem Schild?", "Что написано на табличке?", "Що написано на табличці?",
                "What does the sign say?", "Tabelada ne yazıyor?", "Co jest napisane na tabliczce?",
                "Cosa c'è scritto sul cartello?", "¿Qué pone en el letrero?",
                "Qu'est-ce qui est écrit sur le panneau?", "Co je napsané na ceduli?")}),
    739: (LIST + "; первым — то, что говорят чаще", {
        "t_ru": "вовремя, пунктуальный", "t_uk": "вчасно, пунктуальний", "t_en": "on time, punctual",
        "t_tr": "dakik, tam zamanında", "t_pl": "punktualny, na czas"}),
    590: (LIST + "; «Аренда — триста евро» — канцелярски", {
        "t_ru": "квартплата, аренда", "t_uk": "оренда, квартплата", "t_en": "rent", "t_tr": "kira", "t_pl": "czynsz",
        "t_it": "l'affitto", "t_es": "el alquiler", "t_fr": "le loyer", "t_cs": "nájem",
        "x_ru": "Квартплата — триста евро", "x_uk": "Квартплата — триста євро"}),
    199: (LIST + "; «принимаю короткий душ» — калька", {
        "t_ru": "душ", "t_uk": "душ", "t_tr": "duş", "t_pl": "prysznic",
        "x_ru": "Я быстро приму душ", "x_uk": "Я швиденько прийму душ", "x_en": "I'm taking a quick shower"}),
    1198: (TWO + " («бросить дело» — своя строка); " + EN, {
        "t_ru": "выходить", "t_uk": "виходити", "t_en": "to get off", "t_tr": "inmek", "t_pl": "wysiadać",
        "t_it": "scendere", "t_es": "bajarse", "t_fr": "descendre", "t_cs": "vystoupit",
        "x_en": "I'm getting off at the next stop"}),
    208: (LIST + "; " + EN, {
        "t_ru": "делать покупки, ходить за покупками", "t_uk": "робити покупки", "t_en": "to go shopping, to shop",
        "t_tr": "alışveriş yapmak", "t_pl": "robić zakupy", "t_it": "fare la spesa",
        "t_es": "hacer la compra, ir de compras", "t_fr": "faire les courses", "t_cs": "nakupovat",
        "x_en": "I'm going shopping"}),
}

SPLIT_LATER = {
    695: ["die Papiere = документы"],
    211: ["einladen = загружать (Gepäck einladen)"],
    1198: ["aussteigen = выйти из дела"],
}
