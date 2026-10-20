"""A1, блок 6: слова 201–240 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
TWO = "в строке два разных слова — оставлено главное, второе — отдельной строкой (блок деления)"
EN = "английский пример: так не говорят"
SAME = "у Wasser и trinken был один и тот же пример «Ich trinke Wasser» — у каждого свой, живой"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    1739: (LIST, {"t_ru": "наверху, сверху", "t_uk": "вгорі, нагорі", "t_en": "up, upstairs", "t_tr": "yukarıda",
                  "t_pl": "na górze", "t_it": "in alto, sopra", "t_es": "arriba", "t_fr": "en haut",
                  "t_cs": "nahoře"}),
    1010: (SAME, {**all_x("Kann ich ein Glas Wasser haben?", "Можно стакан воды?", "Можна склянку води?",
                          "Can I have a glass of water?", "Bir bardak su alabilir miyim?",
                          "Mogę prosić szklankę wody?", "Posso avere un bicchiere d'acqua?",
                          "¿Me da un vaso de agua?", "Je peux avoir un verre d'eau?",
                          "Můžu dostat sklenici vody?")}),
    942: (SAME + "; " + LIST, {
        "t_ru": "пить", "t_uk": "пити", "t_pl": "pić",
        **all_x("Was möchtest du trinken?", "Что ты будешь пить?", "Що ти питимеш?",
                "What would you like to drink?", "Ne içmek istersin?", "Czego się napijesz?",
                "Cosa vuoi bere?", "¿Qué quieres beber?", "Qu'est-ce que tu veux boire?", "Co chceš pít?")}),
    1542: (LIST + "; «большой» — не hoch", {"t_ru": "высокий, высоко", "t_uk": "високий, високо", "t_en": "high",
                                           "t_tr": "yüksek", "t_pl": "wysoki, wysoko", "t_fr": "haut, élevé"}),
    13351: ("«У меня есть пять яблок» — по-русски «есть» тут лишнее", {
        "x_ru": "У меня пять яблок", "x_uk": "У мене п'ять яблук"}),
    534: ("пять значений → главные два («страна», «за городом»)", {
        "t_ru": "страна, деревня", "t_uk": "країна, село", "t_en": "country, countryside", "t_tr": "ülke, kır",
        "t_pl": "kraj, wieś", "t_it": "il paese, la campagna", "t_es": "el país, el campo",
        "t_fr": "le pays, la campagne", "t_cs": "země, venkov"}),
    6250: (LIST, {"t_ru": "тяжёлый, трудный", "t_uk": "важкий, складний", "t_en": "heavy, difficult",
                  "t_tr": "ağır, zor", "t_pl": "ciężki, trudny", "t_it": "pesante, difficile",
                  "t_es": "pesado, difícil", "t_fr": "lourd, difficile"}),
    1048: (EN, {"x_en": "The week is going by fast"}),
    13354: ("«We are four people / Siamo quattro persone» — так не говорят; uk «четверо» — другое слово", {
        "t_uk": "чотири", "x_en": "There are four of us", "x_it": "Siamo in quattro", "x_es": "Somos cuatro",
        "x_fr": "Nous sommes quatre"}),
    1075: (LIST, {"t_ru": "комната, номер", "t_uk": "кімната, номер", "t_en": "room", "t_tr": "oda"}),
    316: (LIST, {"t_ru": "нравиться", "t_tr": "hoşuna gitmek, beğenmek"}),
    6252: (LIST + "; пометка «(hovor.)» в переводе", {
        "t_ru": "смотреть, глядеть", "t_en": "to look, to watch", "t_tr": "bakmak", "t_pl": "patrzeć, oglądać",
        "t_cs": "dívat se, koukat"}),
    684: (LIST + "; " + EN, {
        "t_ru": "место, городок", "t_uk": "місце, містечко", "t_en": "place", "t_tr": "yer",
        "t_pl": "miejsce, miejscowość", "t_it": "il posto, il luogo", "t_es": "el lugar, el pueblo",
        "t_fr": "l'endroit, le lieu", "t_cs": "místo, obec", "x_en": "What place is this?"}),
    13358: (LIST, {"t_en": "your", "t_es": "vuestro"}),
    1089: (LIST, {"t_ru": "между", "t_uk": "між", "t_en": "between"}),
    107: ("«ложусь в кровать» — калька; по-русски «в постель»", {"x_ru": "Я рано ложусь в постель",
                                                              "x_fr": "Je vais au lit tôt"}),
    1060: (LIST + "; «What is this word called» — так не говорят", {
        "t_ru": "слово", "t_uk": "слово", "t_en": "word", "t_tr": "kelime, söz", "t_pl": "słowo",
        "x_en": "How do you say this word in German?", "x_uk": "Як буде це слово німецькою?"}),
    236: (LIST, {"t_ru": "рассказывать, рассказать", "t_uk": "розповідати", "t_en": "to tell", "t_tr": "anlatmak",
                 "t_pl": "opowiadać, opowiedzieć", "t_es": "contar", "t_cs": "vyprávět"}),
    1385: (LIST, {"t_ru": "извинить, извиняться", "t_uk": "вибачити, вибачатися", "t_en": "to excuse, to apologize",
                  "t_tr": "affetmek, özür dilemek", "t_pl": "przepraszać, wybaczać", "t_es": "disculpar, perdonar",
                  "t_cs": "prominout, omluvit se"}),
    2007: (LIST + "; «The book is lying downstairs» — неверно и неживо", {
        "t_ru": "внизу", "t_uk": "внизу", "t_en": "below, downstairs", "t_tr": "aşağıda", "t_pl": "na dole",
        "t_it": "giù, sotto", "t_es": "abajo", "t_fr": "en bas", "t_cs": "dole",
        **all_x("Ich warte unten", "Я подожду внизу", "Я почекаю внизу", "I'll wait downstairs", "Aşağıda beklerim",
                "Poczekam na dole", "Aspetto giù", "Espero abajo", "J'attends en bas", "Počkám dole")}),
    223: (LIST, {"t_ru": "извините, извинение", "t_uk": "вибачте, вибачення", "t_en": "excuse me, sorry",
                 "t_tr": "affedersiniz, özür", "t_pl": "przepraszam, przeprosiny"}),
    1034: (LIST, {"t_ru": "важный, важно", "t_uk": "важливий, важливо", "t_en": "important", "t_tr": "önemli",
                  "t_pl": "ważny", "x_en": "That's important"}),
    795: (LIST, {"t_ru": "плохой, плохо", "t_uk": "поганий, погано", "t_en": "bad, badly", "t_tr": "kötü",
                 "t_pl": "zły, źle", "t_it": "cattivo, male", "t_es": "malo, mal", "t_fr": "mauvais, mal",
                 "x_en": "That's bad"}),
    587: (LIST, {"t_it": "la persona, l'essere umano", "t_fr": "la personne, l'être humain"}),
    6261: ("в примере слово не видно («Я проголодался»); «заболеть» — другое употребление", {
        "t_ru": "получать, достать", "t_uk": "отримувати, дістати", "t_en": "to get", "t_tr": "almak",
        "t_pl": "dostawać", "t_it": "ricevere, prendere", "t_es": "recibir, conseguir", "t_fr": "recevoir, avoir",
        **all_x("Ich habe ein Geschenk gekriegt", "Я получил подарок", "Я отримав подарунок", "I got a present",
                "Bir hediye aldım", "Dostałem prezent", "Ho ricevuto un regalo", "He recibido un regalo",
                "J'ai eu un cadeau", "Dostal jsem dárek")}),
    882: (TWO + " («задавать вопрос» — eine Frage stellen, своя строка)", {
        "t_ru": "ставить, поставить", "t_uk": "ставити, поставити", "t_en": "to put, to place", "t_tr": "koymak",
        "t_pl": "stawiać, postawić", "t_it": "mettere, posare", "t_es": "poner, colocar", "t_fr": "mettre, poser",
        "t_cs": "postavit, dát"}),
    812: (LIST, {"t_ru": "школа", "t_uk": "школа"}),
    1937: (LIST, {"t_ru": "часть, деталь", "t_uk": "частина, деталь", "t_en": "part, piece",
                  "t_tr": "parça, bölüm", "t_pl": "część", "t_fr": "la partie, la pièce",
                  "x_en": "That's an important part"}),
    670: (LIST, {"t_es": "a menudo"}),
    287: (LIST + "; «бесплатный» — это kostenlos; «The room is free» — по-английски «бесплатна»", {
        "t_ru": "свободный", "t_uk": "вільний", "t_en": "free, vacant", "t_tr": "boş, serbest", "t_pl": "wolny",
        "t_it": "libero", "t_es": "libre", "t_fr": "libre", "t_cs": "volný", "x_en": "The room is available"}),
    15: (LIST + "; «старший» — это älter, «прежний» — ehemalig", {
        "t_ru": "старый", "t_uk": "старий", "t_en": "old", "t_tr": "eski, yaşlı", "t_pl": "stary",
        "t_it": "vecchio, anziano", "t_es": "viejo, mayor", "t_fr": "vieux, âgé"}),
    1052: ("«gdzie» — это wo", {"t_en": "where to", "t_pl": "dokąd"}),
    1039: ("пример переводит другую фразу: «до завтра» в «Auf Wiedersehen» нет; «новая встреча» — другое значение", {
        "t_ru": "до свидания", "t_uk": "до побачення", "t_en": "goodbye", "t_tr": "görüşmek üzere, hoşça kal",
        "t_pl": "do widzenia", "t_it": "arrivederci", "t_es": "adiós", "t_fr": "au revoir", "t_cs": "na shledanou",
        "x_ru": "До свидания", "x_uk": "До побачення", "x_en": "Goodbye", "x_tr": "Hoşça kalın",
        "x_pl": "Do widzenia"}),
    717: (LIST + "; первым — значение из примера", {
        "t_ru": "место, площадь", "t_uk": "місце, площа", "t_en": "seat, square", "t_tr": "yer, meydan",
        "t_pl": "miejsce, plac", "t_it": "il posto, la piazza", "t_es": "el sitio, la plaza", "t_fr": "la place",
        "t_cs": "místo, náměstí"}),
    6268: (LIST, {"t_pl": "możliwy"}),
    348: (LIST, {"t_ru": "счастливый", "t_uk": "щасливий", "t_en": "happy", "t_tr": "mutlu", "t_pl": "szczęśliwy",
                 "t_it": "felice", "t_es": "feliz", "t_fr": "heureux"}),
}

SPLIT_LATER = {882: ["eine Frage stellen = задать вопрос"]}
