"""A1, блок 8: слова 281–320 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
TWO = "в строке два разных слова — оставлено главное, второе — отдельной строкой (блок деления)"
EN = "английский пример: так не говорят о том, что происходит сейчас"
DULL = "пример ни о чём («X ist Y») → фраза из жизни"
SAME = "пример совпадал с примером другого слова — у каждого свой"
HOVOR = "пометка «(hovor.)» в переводе"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    6298: (LIST, {"t_ru": "мало, немного", "t_uk": "мало, небагато", "t_en": "little, few", "t_tr": "az",
                  "t_pl": "mało, niewiele", "t_cs": "málo", "x_en": "I only have a little time today"}),
    841: (TWO + " («хорошо сидеть по фигуре» — своя строка); " + EN, {
        "t_ru": "сидеть", "t_uk": "сидіти", "t_en": "to sit", "t_tr": "oturmak", "t_pl": "siedzieć",
        "t_it": "stare seduto", "t_es": "estar sentado", "t_fr": "être assis", "t_cs": "sedět",
        "x_en": "I'm sitting on the chair"}),
    540: (TWO + " («согласно» — laut + род. падеж, своя строка)", {
        "t_ru": "громкий, громко", "t_uk": "гучний, гучно", "t_en": "loud", "t_tr": "gürültülü, yüksek sesle",
        "t_pl": "głośny, głośno", "t_it": "alto, forte", "t_es": "alto, fuerte", "t_fr": "fort, bruyant",
        "t_cs": "hlasitý, nahlas"}),
    10061: ("порча знаний: «Ich bin nicht böse» — «я не сержусь», а перевод «Я не злой» — «я не злой человек»", {
        "t_ru": "злой, сердитый", "t_uk": "злий, сердитий", "t_en": "angry, evil", "t_tr": "kızgın, kötü",
        "t_pl": "zły", "t_es": "enfadado, malo", "t_fr": "fâché, méchant",
        "x_ru": "Я не сержусь", "x_uk": "Я не серджуся"}),
    394: (LIST, {"t_ru": "называться, значить", "t_uk": "називатися, означати", "t_en": "to be called, to mean",
                 "t_tr": "adı olmak, anlamına gelmek", "t_pl": "nazywać się, znaczyć", "x_en": "What's your name?"}),
    6307: (LIST, {"t_ru": "твёрдый, жёсткий", "t_uk": "твердий, жорсткий", "t_en": "hard, tough",
                  "t_tr": "sert, katı", "t_pl": "twardy", "t_cs": "tvrdý"}),
    1589: (TWO + " («Klasse!» — «отлично», своя строка)", {
        "t_ru": "класс", "t_uk": "клас", "t_en": "class, grade", "t_tr": "sınıf", "t_pl": "klasa"}),
    1055: (SAME + " (suchen: «Ich suche eine Wohnung»)", {
        "t_en": "flat, apartment", "t_tr": "daire", "t_es": "el piso, el apartamento",
        "t_fr": "l'appartement",
        **all_x("Unsere Wohnung hat drei Zimmer", "В нашей квартире три комнаты", "У нашій квартирі три кімнати",
                "Our flat has three rooms", "Dairemiz üç odalı", "Nasze mieszkanie ma trzy pokoje",
                "Il nostro appartamento ha tre stanze", "Nuestro piso tiene tres habitaciones",
                "Notre appartement a trois pièces", "Náš byt má tři pokoje")}),
    822: (LIST, {"t_ru": "красивый, приятный", "t_uk": "гарний, приємний", "t_en": "beautiful, nice",
                 "t_tr": "güzel, hoş", "t_pl": "piękny, ładny", "t_es": "bonito, hermoso", "t_fr": "beau, joli"}),
    30: (LIST, {"t_ru": "звонить, позвонить", "t_uk": "дзвонити, подзвонити", "t_en": "to call, to phone",
                "t_tr": "aramak", "t_pl": "dzwonić, zadzwonić"}),
    10066: (LIST, {"t_ru": "смеяться", "t_uk": "сміятися", "t_en": "to laugh", "t_tr": "gülmek",
                   "t_pl": "śmiać się"}),
    1426: (TWO + " («вылететь» — rausfliegen, своя строка); " + EN, {
        "t_ru": "летать, лететь", "t_uk": "летіти, літати", "t_en": "to fly", "t_tr": "uçmak",
        "t_pl": "lecieć, latać", "t_it": "volare", "t_es": "volar", "t_fr": "voler, prendre l'avion",
        "x_en": "We're flying to Spain"}),
    335: (LIST, {"t_ru": "магазин, дело", "t_uk": "магазин, справа", "t_en": "shop, business",
                 "t_tr": "dükkân, iş", "t_pl": "sklep, interes"}),
    706: (LIST + "; uk «Скільки вас осіб?» — канцелярски", {
        "t_ru": "человек, особа", "t_uk": "людина, особа", "t_en": "person", "t_tr": "kişi", "t_pl": "osoba",
        "x_uk": "На скільки осіб?", "x_en": "How many of you are there?"}),
    1639: (LIST + "; «ставня» — другое значение; " + HOVOR, {
        "t_ru": "магазин, лавка", "t_uk": "магазин, крамниця", "t_en": "shop, store", "t_tr": "dükkân",
        "t_pl": "sklep", "t_cs": "obchod, krám"}),
    625: (LIST + "; «возможно» — mag sein, другое употребление", {
        "t_ru": "нравиться, любить", "t_uk": "подобатися, любити", "t_en": "to like", "t_tr": "sevmek, hoşlanmak",
        "t_pl": "lubić", "t_it": "piacere", "t_es": "gustar", "t_fr": "aimer"}),
    406: (LIST, {"t_ru": "сзади, позади", "t_uk": "ззаду, позаду", "t_en": "at the back, behind",
                 "t_tr": "arkada", "t_pl": "z tyłu"}),
    562: (LIST, {"t_ru": "смешной, весёлый", "t_uk": "смішний, веселий", "t_en": "funny",
                 "t_tr": "komik, eğlenceli", "t_pl": "śmieszny, zabawny", "t_it": "divertente, buffo",
                 "t_cs": "legrační, vtipný"}),
    797: (LIST + "; " + DULL, {
        "t_ru": "конец, вывод", "t_uk": "кінець, висновок", "t_en": "end, conclusion", "t_tr": "son, sonuç",
        "t_pl": "koniec, wniosek", "t_es": "el final, la conclusión",
        **all_x("Am Schluss hat er gelacht", "В конце он засмеялся", "Наприкінці він засміявся",
                "In the end he laughed", "Sonunda güldü", "Na koniec się roześmiał", "Alla fine ha riso",
                "Al final se rio", "À la fin, il a ri", "Na konci se zasmál")}),
    930: (DULL, {"t_en": "table",
                 **all_x("Das Essen steht auf dem Tisch", "Еда на столе", "Їжа на столі", "The food is on the table",
                         "Yemek masada", "Jedzenie jest na stole", "Il cibo è in tavola",
                         "La comida está en la mesa", "Le repas est sur la table", "Jídlo je na stole")}),
    6325: ("«день моей жизни» — калька; der Tag meines Lebens — «лучший день в жизни»", {
        "t_ru": "жизнь", "t_uk": "життя", "t_en": "life", "t_tr": "hayat", "t_pl": "życie",
        "x_ru": "Это был лучший день в моей жизни", "x_uk": "Це був найкращий день мого життя",
        "x_en": "That was the best day of my life", "x_pl": "To był najpiękniejszy dzień w moim życiu",
        "x_cs": "To byl nejkrásnější den mého života"}),
    1283: (LIST, {"t_ru": "просить, попросить", "t_uk": "просити, попросити", "t_en": "to ask",
                  "t_tr": "rica etmek, istemek", "t_pl": "prosić, poprosić"}),
    414: ("«Мы живём в отеле» — по-русски «остановились»; " + EN, {
        "x_ru": "Мы остановились в отеле", "x_uk": "Ми зупинилися в готелі", "x_en": "We're staying in a hotel"}),
    554: (SAME + " (auf: «Das Buch liegt auf dem Tisch»); " + LIST, {
        "t_ru": "лежать, находиться", "t_uk": "лежати, знаходитися", "t_en": "to lie, to be located",
        "t_tr": "yatmak, bulunmak", "t_pl": "leżeć", "t_it": "stare, trovarsi", "t_es": "estar, encontrarse",
        "t_fr": "être posé, se trouver",
        **all_x("Ich liege im Bett und lese", "Я лежу в кровати и читаю", "Я лежу в ліжку й читаю",
                "I'm lying in bed reading", "Yatakta yatıp kitap okuyorum", "Leżę w łóżku i czytam",
                "Sto sdraiato a letto e leggo", "Estoy tumbado en la cama leyendo", "Je suis couché au lit et je lis",
                "Ležím v posteli a čtu")}),
    32: (LIST, {"t_ru": "ответ", "t_en": "answer, reply", "t_tr": "cevap, yanıt"}),
    54: ("uk «очі» — множественное, не перевод слова", {"t_ru": "глаз", "t_uk": "око"}),
    9712: (LIST, {"t_ru": "продавать, продать", "t_uk": "продавати, продати"}),
    111: (LIST, {"t_ru": "платить, заплатить", "t_uk": "платити, заплатити", "t_en": "to pay", "t_tr": "ödemek",
                 "t_pl": "płacić, zapłacić"}),
    22: (LIST, {"t_ru": "начинать, начинаться", "t_en": "to start, to begin", "t_tr": "başlamak",
                "t_pl": "zaczynać"}),
    1486: (LIST + "; Spiel здесь — матч", {
        "t_ru": "выигрывать, побеждать", "t_uk": "вигравати, перемагати", "t_en": "to win", "t_tr": "kazanmak",
        "t_pl": "wygrywać", "t_it": "vincere", "t_es": "ganar", "t_fr": "gagner", "t_cs": "vyhrát",
        "x_ru": "Мы очень хотим выиграть этот матч", "x_uk": "Ми дуже хочемо виграти цей матч"}),
    652: (LIST, {"t_ru": "новый", "t_uk": "новий", "t_en": "new", "t_pl": "nowy"}),
    114: (SAME + " (an: «Das Bild hängt an der Wand»); " + HOVOR, {
        "t_ru": "картина, фото", "t_uk": "картина, фото", "t_en": "picture, photo", "t_tr": "resim, fotoğraf",
        "t_pl": "obraz, zdjęcie", "t_it": "il quadro, la foto", "t_es": "el cuadro, la foto",
        "t_fr": "le tableau, la photo", "t_cs": "obraz, fotka",
        **all_x("Schick mir mal ein Bild vom Hund!", "Пришли мне фото собаки!", "Надішли мені фото собаки!",
                "Send me a picture of the dog!", "Bana köpeğin bir fotoğrafını gönder!", "Wyślij mi zdjęcie psa!",
                "Mandami una foto del cane!", "¡Mándame una foto del perro!", "Envoie-moi une photo du chien!",
                "Pošli mi fotku psa!")}),
    17476: (LIST + "; «Мой телефон сломан» — калька", {
        "t_ru": "мобильник, телефон", "t_uk": "мобільний, телефон", "t_en": "mobile phone", "t_tr": "cep telefonu",
        "t_pl": "komórka, telefon", "t_it": "il cellulare", "t_es": "el móvil",
        "x_ru": "У меня сломался телефон", "x_pl": "Moja komórka jest zepsuta"}),
    978: (LIST, {"t_ru": "женат, замужем", "t_uk": "одружений, заміжня", "t_pl": "żonaty, zamężna"}),
    1066: ("«Bitte zahl hier» — по-немецки так не говорят", {
        "t_ru": "платить", "t_uk": "платити", "t_en": "to pay", "t_tr": "ödemek", "t_pl": "płacić", "t_cs": "platit",
        **all_x("Kann ich mit Karte zahlen?", "Можно заплатить картой?", "Можна заплатити карткою?",
                "Can I pay by card?", "Kartla ödeyebilir miyim?", "Mogę zapłacić kartą?",
                "Posso pagare con la carta?", "¿Puedo pagar con tarjeta?", "Je peux payer par carte?",
                "Můžu platit kartou?")}),
}

SPLIT_LATER = {
    841: ["sitzen = хорошо сидеть (Die Hose sitzt gut)"],
    540: ["laut + Gen. = согласно (laut Gesetz)"],
    1589: ["Klasse! = отлично"],
    1426: ["rausfliegen = вылететь (откуда-то)"],
}
