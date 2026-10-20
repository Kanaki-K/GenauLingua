"""A1, блок 9: слова 321–360 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
TWO = "в строке два разных слова — оставлено главное, второе — отдельной строкой (блок деления)"
EN = "английский пример: так не говорят о том, что происходит сейчас"
DULL = "пример ни о чём («X ist Y») → фраза из жизни"
MARK = "пометка «(hovor.)/(coloq.)/(fam.)» в переводе"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    1646: (LIST, {"t_ru": "класть, положить", "t_uk": "класти, покласти", "t_en": "to put, to lay", "t_tr": "koymak",
                  "t_pl": "kłaść, położyć"}),
    2176: (LIST, {"t_ru": "начало", "t_uk": "початок", "t_tr": "başlangıç", "t_pl": "początek"}),
    6339: (LIST + "; «Это абсолютно правильно» — калька", {
        "t_ru": "абсолютно, совершенно", "t_uk": "абсолютно, цілком", "t_en": "absolutely", "t_tr": "kesinlikle",
        "t_pl": "absolutnie", "t_es": "absolutamente", "t_fr": "absolument", "t_cs": "naprosto, absolutně",
        "x_ru": "Абсолютно верно", "x_uk": "Абсолютно правильно"}),
    1082: ("пять значений (поезд, затяжка, ход, сквозняк, черта) — для A1 одно: «поезд»", {
        "t_ru": "поезд", "t_uk": "потяг", "t_en": "train", "t_tr": "tren", "t_pl": "pociąg", "t_it": "il treno",
        "t_es": "el tren", "t_fr": "le train", "t_cs": "vlak", "x_en": "The train arrives at eight"}),
    45: ("пояснение «от плеча до кисти» и «подлокотник» — не перевод; немецкий пример в настоящем, перевод — в прошлом", {
        "t_ru": "рука", "t_uk": "рука", "t_pl": "ręka, ramię",
        **all_x("Er hat sich am Arm verletzt", "Он поранил руку", "Він поранив руку", "He hurt his arm",
                "Kolunu yaraladı", "Zranił się w ramię", "Si è fatto male al braccio",
                "Se ha hecho daño en el brazo", "Il s'est blessé au bras", "Poranil si ruku")}),
    2109: (LIST, {"t_ru": "чудесный, замечательный", "t_uk": "чудовий", "t_en": "wonderful", "t_tr": "harika",
                  "t_pl": "wspaniały, cudowny"}),
    14913: (LIST, {"t_ru": "партнёр", "t_uk": "партнер", "t_en": "partner", "t_tr": "partner, eş", "t_pl": "partner",
                   "t_it": "il partner, il compagno", "t_es": "la pareja, el socio",
                   "t_fr": "le compagnon, le partenaire", "t_cs": "partner"}),
    13392: (LIST, {"t_ru": "кто-то, кто-нибудь", "t_uk": "хтось", "t_en": "someone, somebody", "t_tr": "biri"}),
    113: (EN, {"x_en": "He's having a beer"}),
    492: (LIST + "; tr «Oda küçük» — «моя» потеряна", {
        "t_ru": "маленький, небольшой", "t_uk": "маленький, невеликий", "t_en": "small, little", "t_tr": "küçük",
        "t_pl": "mały", "x_tr": "Odam küçük"}),
    1315: (LIST, {"t_ru": "дама", "t_uk": "пані, дама", "t_en": "lady", "t_tr": "hanım, bayan", "t_pl": "pani"}),
    8742: (LIST, {"t_ru": "начальник, шеф", "t_uk": "начальник, шеф", "t_en": "boss", "t_tr": "patron, şef",
                  "t_pl": "szef"}),
    346: (TWO + " (gleich — «одинаковый»; «сейчас, сразу» — своя строка); «У нас одинаковая идея» — калька", {
        "t_ru": "одинаковый, такой же", "t_uk": "однаковий, такий самий", "t_en": "same, equal", "t_tr": "aynı",
        "t_pl": "taki sam, jednakowy", "t_it": "stesso, uguale", "t_es": "mismo, igual", "t_fr": "même, pareil",
        "t_cs": "stejný",
        **all_x("Wir haben die gleichen Schuhe!", "У нас одинаковая обувь!", "У нас однакове взуття!",
                "We have the same shoes!", "Ayakkabılarımız aynı!", "Mamy takie same buty!",
                "Abbiamo le stesse scarpe!", "¡Tenemos los mismos zapatos!", "On a les mêmes chaussures!",
                "Máme stejné boty!")}),
    912: (EN, {"x_en": "We're dancing together"}),
    93: (LIST + "; «Ich benutze das Telefon» — пример ни о чём", {
        "t_ru": "использовать, пользоваться", "t_uk": "використовувати, користуватися",
        **all_x("Darf ich kurz dein Handy benutzen?", "Можно воспользоваться твоим телефоном?",
                "Можна скористатися твоїм телефоном?", "Can I use your phone for a moment?",
                "Telefonunu kısa bir süre kullanabilir miyim?", "Mogę na chwilę skorzystać z twojego telefonu?",
                "Posso usare un attimo il tuo cellulare?", "¿Puedo usar un momento tu móvil?",
                "Je peux utiliser ton portable une seconde?", "Můžu na chvilku použít tvůj mobil?")}),
    410: (LIST, {"t_ru": "свадьба", "t_uk": "весілля", "t_en": "wedding", "t_tr": "düğün", "t_pl": "ślub, wesele"}),
    746: (LIST + "; " + DULL, {
        "t_ru": "помещение, пространство", "t_uk": "приміщення, простір", "t_en": "room, space", "t_tr": "oda, alan",
        "t_pl": "pomieszczenie, przestrzeń", "t_it": "la stanza, lo spazio", "t_es": "la sala, el espacio",
        "t_fr": "la pièce, l'espace", "t_cs": "místnost, prostor",
        **all_x("In diesem Raum darf man nicht rauchen", "В этом помещении нельзя курить",
                "У цьому приміщенні не можна курити", "You can't smoke in this room", "Bu odada sigara içilmez",
                "W tym pomieszczeniu nie wolno palić", "In questa stanza non si può fumare",
                "En esta sala no se puede fumar", "On ne peut pas fumer dans cette pièce",
                "V této místnosti se nesmí kouřit")}),
    627: (LIST, {"t_ru": "усталый, уставший", "t_uk": "втомлений", "t_en": "tired", "t_tr": "yorgun",
                 "t_pl": "zmęczony", "x_en": "I'm really tired"}),
    135: (EN, {"x_en": "I'm writing a letter"}),
    282: (LIST + "; " + MARK, {"t_ru": "фото, фотография", "t_uk": "фото", "t_en": "photo", "t_tr": "fotoğraf",
                               "t_pl": "zdjęcie", "t_cs": "fotka, fotografie", "x_cs": "Ta fotka je roztomilá"}),
    6347: (LIST, {"t_ru": "известный, знакомый", "t_uk": "відомий, знайомий", "t_en": "well-known, famous",
                  "t_tr": "ünlü, tanıdık", "t_pl": "znany", "t_it": "noto, famoso", "t_es": "conocido, famoso",
                  "t_fr": "connu, célèbre", "t_cs": "známý"}),
    91: (LIST, {"t_ru": "пример", "t_uk": "приклад", "t_en": "example", "t_tr": "örnek", "t_pl": "przykład"}),
    913: (LIST, {"t_ru": "сумка, карман", "t_uk": "сумка, кишеня", "t_en": "bag, pocket", "t_tr": "çanta, cep",
                 "t_pl": "torba, kieszeń", "t_es": "el bolso, el bolsillo"}),
    558: (LIST, {"t_ru": "налево, слева", "t_uk": "ліворуч, зліва", "t_en": "left, on the left", "t_tr": "sola, solda",
                 "t_pl": "w lewo, po lewej"}),
    945: (LIST + "; " + MARK, {"t_ru": "пока", "t_uk": "бувай", "t_en": "bye", "t_tr": "hoşça kal, görüşürüz",
                               "t_pl": "cześć, pa", "t_es": "adiós, chao", "t_fr": "salut", "t_cs": "ahoj, čau"}),
    332: (LIST, {"t_ru": "подарок", "t_uk": "подарунок", "t_en": "present, gift", "t_tr": "hediye",
                 "t_pl": "prezent"}),
    416: (LIST + "; pl «Czuję głód» — книжно", {"t_ru": "голод", "t_uk": "голод", "t_en": "hunger",
                                               "x_pl": "Jestem głodny"}),
    729: (LIST, {"t_ru": "цена, приз", "t_uk": "ціна, приз", "t_en": "price, prize", "t_tr": "fiyat, ödül",
                 "t_pl": "cena, nagroda"}),
    1217: ("«Я могу заплатить наличными?» — калька", {"x_ru": "Можно заплатить наличными?",
                                                      "x_uk": "Можна заплатити готівкою?"}),
    6355: (LIST, {"t_ru": "открывать", "t_uk": "відкривати, відчиняти", "t_en": "to open", "t_tr": "açmak",
                  "t_pl": "otwierać"}),
    273: (LIST, {"t_ru": "фирма, компания", "t_en": "company", "t_tr": "şirket, firma", "t_pl": "firma"}),
    1730: (LIST, {"t_ru": "нормальный, обычный", "t_uk": "нормальний, звичайний", "t_en": "normal, usual",
                  "t_tr": "normal", "t_pl": "normalny, zwykły"}),
    14917: (LIST, {"t_ru": "родился, рождённый", "t_uk": "народився, народжений"}),
    78: ("порча знаний: «банк» и «скамейка» — два разных слова (Banken и Bänke); оставлен «банк», скамейка — своя строка", {
        "t_ru": "банк", "t_uk": "банк", "t_en": "bank", "t_tr": "banka", "t_pl": "bank", "t_it": "la banca",
        "t_es": "el banco", "t_fr": "la banque", "t_cs": "banka"}),
    462: ("шесть значений → главные два", {
        "t_ru": "карта, билет", "t_uk": "карта, квиток", "t_en": "card, map", "t_tr": "kart, harita",
        "t_pl": "karta, mapa", "t_it": "la mappa, la carta", "t_es": "el mapa, la tarjeta", "t_fr": "la carte",
        "t_cs": "mapa, karta"}),
    1194: (LIST + "; пример про кухню — неживой", {
        "t_ru": "выглядеть", "t_uk": "виглядати", "t_en": "to look", "t_tr": "görünmek", "t_pl": "wyglądać",
        "t_it": "sembrare", "t_es": "parecer", "t_fr": "avoir l'air",
        **all_x("Du siehst müde aus", "Ты выглядишь усталым", "Ти виглядаєш втомленим", "You look tired",
                "Yorgun görünüyorsun", "Wyglądasz na zmęczonego", "Sembri stanco", "Pareces cansado",
                "Tu as l'air fatigué", "Vypadáš unaveně")}),
    1142: (LIST + "; " + MARK, {"t_ru": "звонок", "t_uk": "дзвінок", "t_en": "call, phone call",
                                "t_tr": "arama, telefon", "t_pl": "telefon, rozmowa", "t_fr": "l'appel, le coup de fil"}),
}

SPLIT_LATER = {
    346: ["gleich = сейчас, сразу (Ich komme gleich!)"],
    78: ["die Bank (Bänke) = скамейка"],
}
