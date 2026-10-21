"""B1, блок 51: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    379: ("«Der Hase läuft schnell» — пусто", {"t_en": "hare, bunny", **all_x(
        "Zu Ostern versteckt der Hase die Eier", "На Пасху заяц прячет яйца", "На Великдень заєць ховає яйця",
        "At Easter the Easter bunny hides the eggs", "Paskalya'da tavşan yumurtaları saklar",
        "Na Wielkanoc zajączek chowa jajka", "A Pasqua il coniglio nasconde le uova", "En Pascua el conejo esconde los huevos",
        "À Pâques, le lapin cache les œufs", "O Velikonocích zajíček schovává vajíčka")}),
    18708: ("ru «Из-за твоего отсутствия ты пропустил» — бессмыслица", {**all_x(
        "In meiner Abwesenheit kümmert sich mein Kollege um alles", "В моё отсутствие всем занимается коллега",
        "За моєї відсутності всім займається колега", "In my absence my colleague takes care of everything",
        "Yokluğumda her şeyle iş arkadaşım ilgileniyor", "Pod moją nieobecność wszystkim zajmuje się kolega",
        "In mia assenza se ne occupa il mio collega", "En mi ausencia, mi compañero se encarga de todo",
        "En mon absence, mon collègue s'occupe de tout", "V mé nepřítomnosti se o všechno stará kolega")}),
    1169: (LIST, {"t_ru": "пребывание, остановка", "t_uk": "перебування, зупинка", "t_en": "stay, stopover",
                  "t_tr": "kalış, mola", "t_pl": "pobyt, postój"}),
    7052: ("«Die gefüllte Tasche war sehr schwer …» — претерит", {**all_x(
        "Gefüllte Paprika esse ich am liebsten", "Больше всего я люблю перец с начинкой", "Найбільше я люблю перець з начинкою",
        "Stuffed peppers are my favourite", "En çok içi dolu biber severim", "Najbardziej lubię nadziewane papryki",
        "I peperoni ripieni sono i miei preferiti", "Los pimientos rellenos son mis favoritos",
        "Les poivrons farcis, c'est ce que je préfère", "Nejradši mám plněné papriky")}),
    14456: ("«Die Heiligkeit des Ortes wurde … respektiert» — претерит; в речи — титул", {
        "t_tr": "kutsallık, Hazretleri", "t_pl": "świętość, Świątobliwość",
        **all_x("Seine Heiligkeit, der Papst, besucht Berlin", "Его Святейшество Папа посещает Берлин",
                "Його Святійшество Папа відвідує Берлін", "His Holiness the Pope is visiting Berlin",
                "Papa Hazretleri Berlin'i ziyaret ediyor", "Jego Świątobliwość papież odwiedza Berlin",
                "Sua Santità il Papa visita Berlino", "Su Santidad el Papa visita Berlín",
                "Sa Sainteté le pape visite Berlin", "Jeho Svatost papež navštíví Berlín")}),
    833: ("«Die Kellnerin serviert das Essen» — шаблон Kellnerin", {**all_x(
        "Das Gericht wird warm serviert", "Блюдо подают горячим", "Страву подають гарячою", "The dish is served hot",
        "Yemek sıcak servis edilir", "Danie podaje się na ciepło", "Il piatto si serve caldo", "El plato se sirve caliente",
        "Le plat se sert chaud", "Jídlo se podává teplé")}),
    7054: ("убрать пометки (colloq.)/(fam.)/(hovor.)", {"t_it": "picchiare, pestare", "t_fr": "rouer de coups, tabasser",
                                                      "t_cs": "zbít, zmlátit"}),
    13660: ("«Er kam verkleidet …» — претерит", {**all_x(
        "Zu Fasching gehe ich verkleidet als Pirat", "На карнавал я пойду переодетым в пирата",
        "На карнавал я піду переодягнений на пірата", "I'm going to carnival dressed up as a pirate",
        "Karnavala korsan kılığında gideceğim", "Na karnawał idę przebrany za pirata", "A Carnevale vado travestito da pirata",
        "En Carnaval voy disfrazado de pirata", "Pour le carnaval, je vais déguisé en pirate",
        "Na masopust jdu převlečený za piráta")}),
    12584: (EN + " («tumor» — американское)", {"t_en": "tumour, growth", "x_en": "The tumour has to be removed surgically"}),
    17130: ("«Das Kennzeichen … ist abgelaufen» — так не бывает; " + LIST, {
        "t_ru": "номерной знак, признак", "t_uk": "номерний знак, ознака", "t_en": "number plate, sign", "t_tr": "plaka, özellik",
        "t_pl": "tablica rejestracyjna, cecha", "t_it": "la targa, il segno distintivo", "t_es": "la matrícula, el rasgo distintivo",
        "t_fr": "la plaque d'immatriculation, le signe distinctif", "t_cs": "poznávací značka, znak",
        **all_x("Hast du dir das Kennzeichen gemerkt?", "Ты запомнил номерной знак?", "Ти запам'ятав номерний знак?",
                "Did you remember the number plate?", "Plakayı aklında tuttun mu?", "Zapamiętałeś tablicę rejestracyjną?",
                "Ti sei ricordato la targa?", "¿Te has quedado con la matrícula?", "Tu as retenu la plaque d'immatriculation?",
                "Zapamatoval sis poznávací značku?")}),
    10450: ("убрать пометки (colloq.)/(coloq.)/(hovor.)", {"t_it": "innamorato, cotto", "t_es": "enamorado, colado",
                                                          "t_cs": "zamilovaný, zabouchnutý"}),
    10452: ("«Aus reiner Neugier öffnete sie die Tür» — претерит", {**all_x(
        "Ich frage nur aus Neugier", "Я спрашиваю просто из любопытства", "Я питаю лише з цікавості",
        "I'm just asking out of curiosity", "Sadece meraktan soruyorum", "Pytam tylko z ciekawości",
        "Chiedo solo per curiosità", "Pregunto solo por curiosidad", "Je demande juste par curiosité",
        "Ptám se jen ze zvědavosti")}),
}

SPLIT_LATER = {}
