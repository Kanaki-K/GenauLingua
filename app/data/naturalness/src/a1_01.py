"""A1, блок 1: 40 самых частых слов (служебные). Вычитано вручную 21.10.

Ключи: t_<язык> — перевод слова, x_<язык> — пример.
"""

LIST = "список → главное слово и не больше одной альтернативы"
GLOSS = "в переводе пояснение вместо слова («определённый артикль», «вспомогательный глагол»)"
ARTICLE = ("порча знаний: артикль в примере переведён как «тот/эта» — учит, что der/die значит «тот»; "
           "строка — указательное местоимение, пример тоже")
TWO = "в строке два разных слова — оставлено главное, второе — отдельной строкой (блок деления)"

FIXES = {
    167: (LIST + "; «который» — относительное, другое употребление", {
        "t_ru": "это, то", "t_uk": "це, те", "t_en": "this, that", "t_tr": "bu, şu", "t_pl": "to",
        "t_it": "questo, quello", "t_es": "esto, eso", "t_fr": "ça, cela", "t_cs": "to"}),
    195: ("пример: местоимение — в живой форме («А ты…?»), иначе по-польски/испански/чешски калька", {
        "x_pl": "A ty idziesz z nami dziś wieczorem?",
        "x_es": "¿Y tú vienes con nosotros esta noche?",
        "x_cs": "A ty půjdeš dnes večer s námi?"}),
    653: ("«нет» — это nein, не nicht; служебные пометки («-me») — не перевод", {
        "t_ru": "не", "t_uk": "не", "t_tr": "değil", "t_fr": "ne… pas"}),
    180: (ARTICLE + "; " + GLOSS, {
        "t_ru": "эта, та", "t_uk": "ця, та", "t_en": "this one, that one", "t_tr": "bu, şu",
        "t_pl": "ta", "t_it": "questa, quella", "t_es": "esta, esa", "t_fr": "celle-ci, celle-là",
        "t_cs": "ta",
        "x_de": "Die da ist meine Schwester",
        "x_ru": "Вон та — моя сестра",
        "x_uk": "Он та — моя сестра",
        "x_en": "The one over there is my sister",
        "x_tr": "Şuradaki benim kız kardeşim",
        "x_pl": "Tamta to moja siostra",
        "x_it": "Quella lì è mia sorella",
        "x_es": "Esa de ahí es mi hermana",
        "x_fr": "Celle-là, c'est ma sœur",
        "x_cs": "Tamta je moje sestra"}),
    955: (LIST, {"t_uk": "і, та", "t_pl": "i"}),
    237: (GLOSS, {"t_ru": "оно, это", "t_fr": "il, ça"}),
    174: (ARTICLE + "; " + GLOSS, {
        "t_ru": "этот, тот", "t_uk": "цей, той", "t_en": "this one, that one", "t_tr": "bu, şu",
        "t_pl": "ten", "t_it": "questo, quello", "t_es": "este, ese", "t_fr": "celui-ci, celui-là",
        "t_cs": "ten",
        "x_de": "Der da gefällt mir",
        "x_ru": "Вот этот мне нравится",
        "x_uk": "Ось цей мені подобається",
        "x_en": "I like that one",
        "x_tr": "Şu hoşuma gidiyor",
        "x_pl": "Ten mi się podoba",
        "x_it": "Quello lì mi piace",
        "x_es": "Ese de ahí me gusta",
        "x_fr": "Celui-là me plaît",
        "x_cs": "Tenhle se mi líbí"}),
    1045: ("«We go home» — не так говорят о том, что делаешь сейчас", {"x_en": "We're going home"}),
    1077: (TWO + " (zu — «к»; «слишком» и «закрыто» — свои строки)", {
        "t_ru": "к, в", "t_uk": "до", "t_en": "to", "t_tr": "-e, -a", "t_pl": "do",
        "t_it": "a, da", "t_es": "a", "t_fr": "à, chez", "t_cs": "do, k"}),
    13223: ("порча знаний: «неопределённый артикль» в переводе, а в примере ein не виден вовсе; "
            "строка — числительное «один»", {
        "t_ru": "один", "t_uk": "один", "t_en": "one, a", "t_tr": "bir", "t_pl": "jeden",
        "t_it": "un, uno", "t_es": "un, uno", "t_fr": "un", "t_cs": "jeden",
        "x_de": "Ich habe nur ein Kind",
        "x_ru": "У меня только один ребёнок",
        "x_uk": "У мене тільки одна дитина",
        "x_en": "I have only one child",
        "x_tr": "Sadece bir çocuğum var",
        "x_pl": "Mam tylko jedno dziecko",
        "x_it": "Ho solo un figlio",
        "x_es": "Solo tengo un hijo",
        "x_fr": "Je n'ai qu'un enfant",
        "x_cs": "Mám jen jedno dítě"}),
    431: (LIST, {
        "t_ru": "в, через", "t_uk": "у, в", "t_en": "in, into", "t_tr": "-de, -da", "t_pl": "w",
        "t_it": "in, a", "t_es": "en", "t_fr": "dans, en", "t_cs": "v, ve"}),
    442: (LIST, {"t_tr": "evet"}),
    596: ("«Это принадлежит мне» — канцелярски; " + LIST, {
        "t_ru": "мне", "t_uk": "мені", "t_tr": "bana", "t_pl": "mi, mnie",
        "x_de": "Gib mir bitte das Salz",
        "x_ru": "Дай мне, пожалуйста, соль",
        "x_uk": "Дай мені, будь ласка, сіль",
        "x_en": "Pass me the salt, please",
        "x_tr": "Tuzu bana verir misin lütfen?",
        "x_pl": "Podaj mi, proszę, sól",
        "x_it": "Passami il sale, per favore",
        "x_es": "Pásame la sal, por favor",
        "x_fr": "Passe-moi le sel, s'il te plaît",
        "x_cs": "Podej mi prosím sůl"}),
    597: (LIST + "; «I go with you» — не так говорят", {
        "t_ru": "с, на", "t_uk": "з, на", "t_tr": "ile", "t_pl": "z", "t_cs": "s, se",
        "x_ru": "Я пойду с тобой", "x_uk": "Я піду з тобою", "x_en": "I'm coming with you"}),
    1035: ("«Як ти почуваєшся?» — это «как себя чувствуешь», а Wie geht's — «как дела»", {
        "t_tr": "nasıl, gibi", "x_uk": "Як у тебе справи?"}),
    49: (LIST + "; «на тему» — другое употребление", {
        "t_ru": "на, в", "t_tr": "üzerinde", "t_it": "su, sopra", "t_es": "sobre, en"}),
    4: (LIST, {
        "t_ru": "но, а", "t_uk": "але, а", "t_en": "but", "t_tr": "ama, fakat", "t_pl": "ale",
        "t_it": "ma", "t_es": "pero", "t_fr": "mais", "t_cs": "ale"}),
    843: (LIST, {
        "t_ru": "так", "t_uk": "так", "t_en": "so, like this", "t_tr": "böyle", "t_pl": "tak",
        "t_it": "così", "t_es": "así", "t_fr": "comme ça, ainsi", "t_cs": "tak"}),
    402: (LIST, {"t_ru": "здесь, тут", "t_uk": "тут", "t_tr": "burada", "t_it": "qui",
                 "t_es": "aquí", "t_fr": "ici", "t_cs": "tady, tu"}),
    366: (GLOSS, {"t_ru": "иметь", "t_uk": "мати", "t_tr": "sahip olmak"}),
    304: (LIST, {"t_ru": "для, за", "t_uk": "для, за", "t_en": "for", "t_tr": "için",
                 "t_pl": "dla", "t_es": "para, por", "t_cs": "pro"}),
    991: (LIST + "; «чей-то» — не перевод", {
        "t_ru": "от, из", "t_uk": "від, з", "t_en": "from, of", "t_tr": "-den", "t_pl": "od, z",
        "t_es": "de", "t_fr": "de", "t_cs": "od, z"}),
    1026: (LIST, {"t_ru": "если, когда", "t_en": "if, when", "t_tr": "eğer"}),
    426: (TWO + " (ihr — «её»; «вы» и «их» — свои строки)", {
        "t_ru": "её", "t_uk": "її", "t_en": "her", "t_tr": "onun", "t_pl": "jej",
        "t_it": "suo, sua", "t_es": "su", "t_fr": "son, sa", "t_cs": "její"}),
    19: (LIST, {
        "t_ru": "на, у", "t_uk": "на, біля", "t_en": "at, on", "t_tr": "-de, yanında",
        "t_pl": "na, przy", "t_it": "a, su", "t_es": "en, a", "t_fr": "à, sur", "t_cs": "na, u"}),
    656: (LIST + "; «I want more water» — грубовато, так просят иначе", {
        "t_ru": "ещё", "t_uk": "ще", "t_en": "still, more", "t_tr": "daha, hâlâ", "t_pl": "jeszcze",
        "t_it": "ancora", "t_es": "más, todavía", "t_fr": "encore", "t_cs": "ještě",
        "x_en": "I'd like some more water", "x_tr": "Biraz daha su istiyorum"}),
    160: (TWO + " (da — «тут, там»; «так как» — своя строка)", {
        "t_ru": "тут, там", "t_uk": "тут, там", "t_en": "there, here", "t_tr": "orada, burada",
        "t_pl": "tu, tam", "t_it": "qui, lì", "t_es": "aquí, ahí", "t_fr": "là", "t_cs": "tady, tam"}),
    664: (LIST, {
        "t_ru": "только, лишь", "t_uk": "тільки, лише", "t_en": "only, just", "t_tr": "sadece",
        "t_pl": "tylko", "t_it": "solo", "t_es": "solo", "t_fr": "seulement", "t_cs": "jen"}),
    185: (LIST, {"t_ru": "тебе", "t_uk": "тобі", "t_tr": "sana", "t_pl": "ci, tobie"}),
    836: (LIST, {"t_ru": "себя, себе", "t_en": "oneself", "t_tr": "kendini", "t_pl": "się",
                 "t_it": "si", "t_es": "se", "t_fr": "se", "t_cs": "se"}),
    362: (LIST + "; в примере слово не видно («Это вкусно»)", {
        "t_ru": "хороший, хорошо", "t_uk": "добрий, добре", "t_en": "good, well", "t_tr": "iyi",
        "t_pl": "dobry, dobrze", "t_it": "buono, bene", "t_es": "bueno, bien", "t_fr": "bon, bien",
        "t_cs": "dobrý, dobře",
        "x_de": "Das ist eine gute Idee",
        "x_ru": "Это хорошая идея",
        "x_uk": "Це добра ідея",
        "x_en": "That's a good idea",
        "x_tr": "Bu iyi bir fikir",
        "x_pl": "To dobry pomysł",
        "x_it": "È una buona idea",
        "x_es": "Es una buena idea",
        "x_fr": "C'est une bonne idée",
        "x_cs": "To je dobrý nápad"}),
    48: (LIST, {"t_ru": "тоже, также", "t_uk": "теж, також", "t_en": "also, too", "t_tr": "de, da",
                "t_pl": "też, także", "t_it": "anche", "t_fr": "aussi", "t_cs": "také, i"}),
    13258: (LIST, {"t_es": "lo, le", "t_cs": "ho, jeho"}),
    13259: (LIST + "; «I'm already ready» — так не говорят", {
        "t_ru": "уже", "t_uk": "вже", "t_en": "already", "t_tr": "zaten, çoktan", "t_pl": "już",
        "t_cs": "už", "x_en": "I'm done already"}),
    827: (TWO + " (sein — «быть»; «его» — своя строка); пример «быть пунктуальным» — канцелярски", {
        "t_ru": "быть", "t_uk": "бути", "t_en": "to be", "t_tr": "olmak", "t_pl": "być",
        "t_it": "essere", "t_es": "ser, estar", "t_fr": "être", "t_cs": "být",
        "x_de": "Kannst du morgen um acht hier sein?",
        "x_ru": "Ты можешь быть здесь завтра в восемь?",
        "x_uk": "Ти можеш бути тут завтра о восьмій?",
        "x_en": "Can you be here tomorrow at eight?",
        "x_tr": "Yarın sekizde burada olabilir misin?",
        "x_pl": "Możesz być tu jutro o ósmej?",
        "x_it": "Puoi essere qui domani alle otto?",
        "x_es": "¿Puedes estar aquí mañana a las ocho?",
        "x_fr": "Tu peux être là demain à huit heures?",
        "x_cs": "Můžeš tu být zítra v osm?"}),
    13: (TWO + " (als — «чем»; «когда» и «в качестве» — свои строки)", {
        "t_ru": "чем", "t_uk": "ніж", "t_en": "than", "t_tr": "-den", "t_pl": "niż",
        "t_it": "di, che", "t_es": "que", "t_fr": "que", "t_cs": "než"}),
}

# Второе значение — отдельной строкой, когда появится инструмент добавления
SPLIT_LATER = {
    1077: ["zu = слишком (Das ist zu teuer)", "zu = закрыто (Der Laden ist zu)"],
    426: ["ihr = вы (Habt ihr Zeit?)", "ihr = их (Das ist ihr Auto — их машина)"],
    160: ["da = так как (Da es regnet, bleibe ich hier)"],
    827: ["sein = его (Das ist sein Buch)"],
    13: ["als = когда, в прошлом (Als ich klein war…)", "als = в качестве (Ich arbeite als Kellner)"],
    174: ["der — артикль: грамматическая карточка, не словарная"],
    180: ["die — артикль: грамматическая карточка"],
    13223: ["ein — неопределённый артикль: грамматическая карточка"],
}
