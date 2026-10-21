"""A2, блок 2: слова 41–80 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
TWO = "в строке два разных слова — оставлено главное, второе — отдельной строкой (блок деления)"
EN = "английский пример: так не говорят"
NEAR = "пример повторял шаблон соседних слов — у каждого свой"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    1248: (EN, {"x_en": "I'm ready"}),
    933: (LIST, {"t_ru": "классный, отличный", "t_uk": "чудовий, класний", "t_en": "great, awesome",
                 "t_tr": "harika, süper", "t_pl": "świetny, super", "t_it": "fantastico", "t_es": "genial, estupendo",
                 "t_fr": "génial, super", "t_cs": "skvělý, super"}),
    9: (LIST, {"t_ru": "понятие, представление", "t_uk": "уявлення, поняття", "t_en": "idea, clue", "t_tr": "fikir",
               "t_pl": "pojęcie", "t_it": "l'idea", "t_es": "la idea", "t_fr": "l'idée", "t_cs": "tušení, představa"}),
    257: ("uk «майже готовий» — fertig здесь «закінчив»", {"x_uk": "Я майже закінчив", "x_en": "I'm almost done"}),
    993: (LIST, {"t_ru": "мимо, прошло", "t_uk": "повз, минуло", "t_en": "past, over", "t_tr": "yanından, bitti",
                 "t_pl": "obok, minęło", "t_it": "accanto, finito", "t_es": "de largo, terminado",
                 "t_fr": "à côté, passé", "t_cs": "kolem, pryč"}),
    407: (LIST, {"t_ru": "за, позади", "t_uk": "за, позаду", "t_en": "behind", "t_tr": "arkasında", "t_pl": "za"}),
    2206: (LIST, {"t_ru": "вид, способ", "t_uk": "вид, спосіб", "t_en": "kind, way", "t_tr": "tür, biçim",
                  "t_pl": "rodzaj, sposób", "t_it": "il modo, il tipo", "t_es": "la manera, el tipo",
                  "t_fr": "la façon, le genre", "t_cs": "způsob, druh"}),
    941: (TWO + " («попадать в цель», «принимать решение» — свои строки); " + EN, {
        "t_ru": "встречать, встречаться", "t_uk": "зустрічати, зустрічатися", "t_en": "to meet",
        "t_tr": "buluşmak, karşılaşmak", "t_pl": "spotkać, spotykać się", "t_it": "incontrare",
        "t_es": "quedar, encontrarse", "t_fr": "rencontrer, se retrouver", "t_cs": "sejít se, potkat",
        "x_en": "We're meeting at three"}),
    10036: (LIST + "; «Я охотно тебе помогу» — калька", {
        "t_ru": "с удовольствием, охотно", "t_uk": "із задоволенням, охоче", "t_en": "gladly", "t_tr": "memnuniyetle",
        "t_pl": "chętnie", "t_it": "volentieri", "t_es": "con mucho gusto", "t_fr": "volontiers", "t_cs": "rád",
        "x_ru": "Я с удовольствием тебе помогу"}),
    13343: (LIST, {"t_ru": "когда-нибудь, по", "t_uk": "коли-небудь", "t_en": "ever", "t_tr": "hiç",
                   "t_pl": "kiedykolwiek"}),
    1319: (LIST, {"t_ru": "поэтому, вот почему", "t_uk": "тому, ось чому", "t_en": "that's why", "t_tr": "bu yüzden",
                  "t_pl": "dlatego"}),
    1876: (LIST, {"t_ru": "заботиться, беспокоиться", "t_uk": "піклуватися, хвилюватися",
                  "t_en": "to take care, to worry", "t_tr": "ilgilenmek, endişelenmek",
                  "t_pl": "troszczyć się, martwić się", "t_it": "occuparsi, preoccuparsi", "t_es": "cuidar, preocuparse",
                  "t_fr": "s'occuper de, s'inquiéter", "t_cs": "starat se, dělat si starosti"}),
    1874: (LIST + "; «мобильный телефон» — книжно", {
        "t_ru": "даже", "t_uk": "навіть", "t_en": "even", "t_tr": "bile, hatta", "t_pl": "nawet", "t_it": "persino",
        "t_es": "incluso", "t_fr": "même", "t_cs": "dokonce",
        "x_ru": "Даже у моей бабушки есть мобильник", "x_uk": "Навіть моя бабуся має мобільний"}),
    13346: (LIST + "; «Здесь никого нет дома» — калька", {
        "t_en": "nobody, no one", "t_tr": "kimse", "x_ru": "Никого нет дома", "x_uk": "Нікого немає вдома",
        "x_en": "There's nobody at home"}),
    423: (LIST, {"t_ru": "идея, мысль", "t_uk": "ідея, думка", "t_en": "idea", "t_tr": "fikir", "t_pl": "pomysł"}),
    6241: (LIST + "; " + EN, {"t_ru": "довольно, достаточно", "t_uk": "досить, доволі", "t_en": "quite, pretty",
                              "t_tr": "oldukça", "t_pl": "dość, całkiem", "x_en": "That's pretty good"}),
    769: (LIST + "; «Hier herrscht Ruhe» — книжно", {
        "t_ru": "тишина, покой", "t_uk": "тиша, спокій", "t_en": "quiet, peace", "t_tr": "sessizlik, huzur",
        "t_pl": "spokój, cisza", "t_it": "la calma, il silenzio", "t_es": "la calma, la tranquilidad",
        "t_fr": "le calme, le silence", "t_cs": "klid, ticho",
        **all_x("Ich brauche ein bisschen Ruhe", "Мне нужно немного покоя", "Мені потрібно трохи спокою",
                "I need some peace and quiet", "Biraz huzura ihtiyacım var", "Potrzebuję trochę spokoju",
                "Ho bisogno di un po' di calma", "Necesito un poco de tranquilidad", "J'ai besoin d'un peu de calme",
                "Potřebuju trochu klidu")}),
    1093: (LIST, {"t_ru": "вообще", "t_uk": "взагалі", "t_en": "at all, anyway", "t_tr": "hiç, aslında",
                  "t_pl": "w ogóle", "t_it": "affatto, in realtà", "t_es": "en absoluto, en realidad",
                  "t_fr": "du tout, au fond", "t_cs": "vůbec"}),
    1505: (TWO + " («дно», «земля, участок» — свои строки)", {
        "t_ru": "причина, основание", "t_uk": "причина, підстава", "t_en": "reason", "t_tr": "neden, sebep",
        "t_pl": "powód", "t_it": "il motivo", "t_es": "el motivo", "t_fr": "la raison", "t_cs": "důvod"}),
    1402: (LIST, {"t_ru": "примерно, около", "t_uk": "приблизно", "t_en": "about, approximately", "t_tr": "yaklaşık",
                  "t_pl": "około", "t_it": "circa", "t_es": "más o menos", "t_fr": "environ", "t_cs": "asi, přibližně"}),
    6247: (LIST, {"t_ru": "пробовать, попытаться", "t_uk": "пробувати, спробувати", "t_en": "to try",
                  "t_tr": "denemek", "t_pl": "próbować"}),
    1130: ("tr — настоящее вместо будущего", {"x_tr": "Bunu farklı yapacağız"}),
    1478: ("«Geschichte ist interessant» — пример ни о чём; для A2 главное — «рассказ, история»", {
        "t_ru": "история, рассказ", "t_uk": "історія, розповідь", "t_en": "story, history", "t_tr": "hikâye, tarih",
        "t_pl": "historia, opowieść", "t_it": "la storia, il racconto", "t_es": "la historia, el cuento",
        "t_fr": "l'histoire", "t_cs": "příběh, historie",
        **all_x("Erzähl mir eine Geschichte!", "Расскажи мне историю!", "Розкажи мені історію!", "Tell me a story!",
                "Bana bir hikâye anlat!", "Opowiedz mi historię!", "Raccontami una storia!", "¡Cuéntame una historia!",
                "Raconte-moi une histoire!", "Vyprávěj mi příběh!")}),
    234: (NEAR + " (dritte: «… die … Lektion»)", {**all_x(
        "Das ist mein erstes Mal in Berlin", "Это мой первый раз в Берлине", "Це мій перший раз у Берліні",
        "It's my first time in Berlin", "Berlin'e ilk gelişim", "Jestem w Berlinie pierwszy raz",
        "È la mia prima volta a Berlino", "Es mi primera vez en Berlín", "C'est ma première fois à Berlin",
        "Jsem v Berlíně poprvé")}),
    651: ("пометка «(fam.)»; «Sie ist nett» — пример ни о чём", {
        "t_tr": "iyi, kibar", "t_fr": "gentil, sympa",
        **all_x("Deine Freunde sind echt nett", "Твои друзья очень милые", "Твої друзі дуже милі",
                "Your friends are really nice", "Arkadaşların gerçekten çok iyi", "Twoi przyjaciele są naprawdę mili",
                "I tuoi amici sono davvero simpatici", "Tus amigos son muy simpáticos", "Tes amis sont vraiment sympas",
                "Tvoji kamarádi jsou fakt milí")}),
    1326: (LIST, {"t_ru": "поэтому", "t_uk": "тому", "t_en": "that's why, therefore", "t_tr": "bu yüzden",
                  "t_pl": "dlatego", "t_it": "per questo", "t_es": "por eso", "t_fr": "c'est pourquoi", "t_cs": "proto"}),
    1070: (LIST, {"t_ru": "показывать, показать", "t_uk": "показувати, показати", "t_en": "to show",
                  "t_tr": "göstermek", "t_pl": "pokazywać", "t_it": "mostrare", "t_es": "mostrar, enseñar",
                  "t_fr": "montrer", "t_cs": "ukázat"}),
    860: (NEAR + " (toll: «Das war toll»)", {**all_x(
        "Wer hat das Spiel gewonnen?", "Кто выиграл матч?", "Хто виграв матч?", "Who won the match?",
        "Maçı kim kazandı?", "Kto wygrał mecz?", "Chi ha vinto la partita?", "¿Quién ganó el partido?",
        "Qui a gagné le match?", "Kdo vyhrál zápas?")}),
    858: ("немецкий пример с ошибкой: «Das war viel Spaß» — нужно «Das hat viel Spaß gemacht»", {
        "t_ru": "веселье, удовольствие", "t_uk": "веселощі, задоволення", "t_en": "fun", "t_tr": "eğlence",
        "t_pl": "zabawa, przyjemność", "t_it": "il divertimento", "t_es": "la diversión", "t_fr": "le plaisir, l'amusement",
        "t_cs": "zábava, legrace",
        **all_x("Das hat viel Spaß gemacht", "Было очень весело", "Було дуже весело", "That was a lot of fun",
                "Çok eğlenceliydi", "To była świetna zabawa", "È stato molto divertente", "Fue muy divertido",
                "C'était très amusant", "Byla to velká zábava")}),
    202: (TWO + " («ровный» — прилагательное eben, своя строка); «сделаем это просто завтра» — калька", {
        "t_ru": "как раз, просто", "t_uk": "якраз, просто", "t_en": "just", "t_tr": "az önce, tam", "t_pl": "właśnie",
        "t_it": "semplicemente, appunto", "t_es": "simplemente, justo", "t_fr": "simplement, justement",
        "t_cs": "prostě, právě",
        "x_ru": "Ну тогда сделаем это завтра", "x_uk": "Ну тоді зробимо це завтра", "x_pl": "No to zrobimy to jutro"}),
    2083: (LIST, {"t_ru": "во время, пока", "t_uk": "під час, поки", "t_en": "during, while", "t_tr": "sırasında",
                  "t_pl": "podczas", "t_cs": "během, zatímco"}),
}

SPLIT_LATER = {
    941: ["treffen = попасть (в цель)", "eine Entscheidung treffen = принять решение"],
    1505: ["der Grund = дно", "der Grund = земля, участок (Grund und Boden)"],
    202: ["eben = ровный, плоский"],
}
