"""A2, блок 4: слова 121–160 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
TWO = "в строке два разных слова — оставлено главное, второе — отдельной строкой (блок деления)"
EN = "английский пример: так не говорят"
NEAR = "пример почти повторял пример другого слова — у каждого свой"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    15373: (LIST, {"t_ru": "небо", "t_uk": "небо", "t_tr": "gökyüzü", "t_pl": "niebo", "t_it": "il cielo",
                   "t_fr": "le ciel", "t_cs": "nebe, obloha"}),
    899: (TWO + " («пьеса», «произведение» — свои строки); пример — обрывок", {
        "t_ru": "кусок, штука", "t_uk": "шматок, штука", "t_en": "piece", "t_tr": "parça", "t_pl": "kawałek",
        "t_it": "il pezzo, la fetta", "t_es": "el trozo, la pieza", "t_fr": "le morceau", "t_cs": "kus, kousek",
        **all_x("Möchtest du noch ein Stück Kuchen?", "Хочешь ещё кусок пирога?", "Хочеш ще шматок пирога?",
                "Would you like another piece of cake?", "Bir parça daha pasta ister misin?",
                "Chcesz jeszcze kawałek ciasta?", "Vuoi un'altra fetta di torta?", "¿Quieres otro trozo de pastel?",
                "Tu veux encore un morceau de gâteau?", "Dáš si ještě kousek koláče?")}),
    18592: ("«будущее время» — грамматический термин; «Die Zukunft wird schön» — пример ни о чём", {
        "t_ru": "будущее", "t_uk": "майбутнє",
        **all_x("Was willst du in Zukunft machen?", "Чем ты хочешь заниматься в будущем?",
                "Чим ти хочеш займатися в майбутньому?", "What do you want to do in the future?",
                "Gelecekte ne yapmak istiyorsun?", "Co chcesz robić w przyszłości?", "Cosa vuoi fare in futuro?",
                "¿Qué quieres hacer en el futuro?", "Qu'est-ce que tu veux faire à l'avenir?",
                "Co chceš v budoucnu dělat?")}),
    1338: (LIST, {"t_ru": "вон там, напротив", "t_uk": "он там, навпроти", "t_en": "over there", "t_tr": "karşıda",
                  "t_pl": "tam, naprzeciwko"}),
    1314: (LIST, {"t_ru": "тогда, в то время", "t_uk": "тоді", "t_en": "back then", "t_tr": "o zamanlar",
                  "t_pl": "wtedy"}),
    2505: (LIST, {"t_ru": "чувство, предчувствие", "t_uk": "почуття, відчуття", "t_en": "feeling",
                  "t_tr": "duygu, his", "t_pl": "uczucie, przeczucie"}),
    879: (LIST, {"t_ru": "сильный, крепкий", "t_uk": "сильний, міцний", "t_en": "strong", "t_tr": "güçlü",
                 "t_pl": "silny, mocny", "x_en": "He's very strong"}),
    1714: (EN, {"x_en": "I got a message"}),
    6302: (LIST + "; «сдача» — отдельное употребление", {
        "t_ru": "остаток, остальное", "t_uk": "решта, залишок", "t_en": "rest", "t_tr": "kalan", "t_pl": "reszta",
        "t_it": "il resto", "t_es": "el resto", "x_ru": "Остальное — тебе"}),
    2668: ("«После того как я поел, я выхожу» — калька и не то время", {
        "x_ru": "После того как поем, выйду на улицу", "x_uk": "Після того як поїм, вийду надвір",
        "x_en": "After I've eaten, I'll go out"}),
    901: (NEAR + " (toll: «Das war toll»)", {
        "t_ru": "супер, отлично", "t_uk": "супер, чудово",
        **all_x("Super, dann sehen wir uns morgen!", "Супер, тогда увидимся завтра!", "Супер, тоді побачимося завтра!",
                "Great, see you tomorrow then!", "Süper, o zaman yarın görüşürüz!", "Super, to do zobaczenia jutro!",
                "Fantastico, allora ci vediamo domani!", "¡Genial, entonces nos vemos mañana!",
                "Super, alors on se voit demain!", "Super, tak se uvidíme zítra!")}),
    528: (LIST, {"t_ru": "тело", "t_uk": "тіло", "t_en": "body", "t_tr": "vücut", "t_pl": "ciało"}),
    2636: (LIST, {"t_ru": "заботиться, заниматься", "t_uk": "піклуватися, займатися", "t_en": "to take care of",
                  "t_tr": "ilgilenmek", "t_pl": "zajmować się, opiekować się"}),
    1749: (LIST, {"t_ru": "случаться, происходить", "t_uk": "ставатися", "t_en": "to happen", "t_tr": "olmak",
                  "t_pl": "zdarzyć się"}),
    2802: (LIST + "; " + NEAR + " (Brief: «Ich habe einen Brief … bekommen»)", {
        "t_ru": "письмо, уведомление", "t_uk": "лист, повідомлення", "t_en": "letter", "t_tr": "yazı", "t_pl": "pismo",
        **all_x("Das Schreiben vom Finanzamt verstehe ich nicht", "Письмо из налоговой я не понимаю",
                "Листа з податкової я не розумію", "I don't understand the letter from the tax office",
                "Vergi dairesinden gelen yazıyı anlamıyorum", "Nie rozumiem pisma z urzędu skarbowego",
                "Non capisco la lettera dell'ufficio delle imposte", "No entiendo la carta de Hacienda",
                "Je ne comprends pas le courrier des impôts", "Nerozumím dopisu z finančního úřadu")}),
    2366: (LIST, {"t_ru": "скорее, раньше", "t_uk": "радше, раніше", "t_en": "rather, earlier",
                  "t_tr": "daha çok, daha erken", "t_pl": "raczej, wcześniej", "t_it": "prima, piuttosto",
                  "t_es": "antes, más bien", "t_fr": "plus tôt, plutôt", "t_cs": "dřív, spíš"}),
    937: (NEAR + " (Hose: «Sie trägt eine blaue Hose»); шесть значений", {
        "t_ru": "носить, нести", "t_uk": "носити, нести", "t_en": "to wear, to carry", "t_tr": "giymek, taşımak",
        "t_pl": "nosić, nieść", "t_it": "portare, indossare", "t_es": "llevar", "t_fr": "porter", "t_cs": "nosit, nést",
        **all_x("Kannst du mir helfen, den Koffer zu tragen?", "Поможешь мне донести чемодан?",
                "Допоможеш мені донести валізу?", "Can you help me carry the suitcase?",
                "Bavulu taşımama yardım eder misin?", "Pomożesz mi nieść walizkę?", "Mi aiuti a portare la valigia?",
                "¿Me ayudas a llevar la maleta?", "Tu peux m'aider à porter la valise?", "Pomůžeš mi nést kufr?")}),
    657: (LIST, {"t_ru": "ещё раз", "t_uk": "ще раз", "t_en": "again", "t_tr": "tekrar", "t_pl": "jeszcze raz"}),
    13384: ("en пример переводил другую фразу («That» вместо «работа»)", {"x_en": "The work has been done"}),
    1000: (LIST + "; «Я представлюсь» — неживо", {
        "t_ru": "представлять, представлять себе", "t_uk": "представляти, уявляти собі", "t_en": "to introduce, to imagine",
        "t_tr": "tanıtmak, hayal etmek", "t_pl": "przedstawiać, wyobrażać sobie", "t_it": "presentare, immaginare",
        "t_es": "presentar, imaginar", "t_fr": "présenter, imaginer", "t_cs": "představit",
        "x_ru": "Позвольте представиться", "x_uk": "Дозвольте представитися"}),
    10064: (LIST, {"t_ru": "осторожный, аккуратный", "t_uk": "обережний", "t_en": "careful", "t_tr": "dikkatli",
                   "t_pl": "ostrożny"}),
    2817: (LIST, {"t_ru": "смысл", "t_uk": "сенс", "t_en": "sense, meaning", "t_tr": "anlam", "t_pl": "sens"}),
    18109: (NEAR + " (nass: «… der Boden ist nass» — внесено мной в блоке 15); пять значений", {
        "t_ru": "пол, земля", "t_uk": "підлога, земля", "t_en": "floor, ground", "t_tr": "zemin, yer",
        "t_pl": "podłoga, ziemia", "t_it": "il pavimento, il terreno", "t_es": "el suelo", "t_fr": "le sol",
        "t_cs": "podlaha, země",
        **all_x("Die Kinder sitzen auf dem Boden", "Дети сидят на полу", "Діти сидять на підлозі",
                "The children are sitting on the floor", "Çocuklar yerde oturuyor", "Dzieci siedzą na podłodze",
                "I bambini sono seduti per terra", "Los niños están sentados en el suelo",
                "Les enfants sont assis par terre", "Děti sedí na zemi")}),
    1129: (LIST + "; «изменить дату встречи» — канцелярски", {
        "t_ru": "менять, изменять", "t_uk": "змінювати", "t_en": "to change", "t_tr": "değiştirmek", "t_pl": "zmieniać",
        "t_it": "cambiare", "t_es": "cambiar", "t_fr": "changer", "t_cs": "změnit",
        "x_ru": "Ты можешь поменять время встречи?", "x_uk": "Ти можеш змінити час зустрічі?"}),
    15929: (LIST, {"t_ru": "жертва, пострадавший", "t_uk": "жертва, потерпілий", "t_en": "victim, sacrifice",
                   "t_tr": "kurban", "t_pl": "ofiara"}),
    13843: (LIST, {"t_ru": "голос", "t_uk": "голос", "t_en": "voice, vote", "t_tr": "ses, oy", "t_pl": "głos"}),
    6309: (LIST, {"t_ru": "хотя бы, по крайней мере", "t_uk": "хоча б, принаймні", "t_en": "at least",
                  "t_tr": "en azından", "t_pl": "przynajmniej, chociaż", "x_en": "At least give me a call"}),
    1262: (LIST, {"t_ru": "особенно", "t_uk": "особливо", "t_en": "especially", "t_tr": "özellikle",
                  "t_pl": "szczególnie, zwłaszcza", "t_it": "particolarmente", "t_es": "especialmente",
                  "t_fr": "particulièrement", "t_cs": "obzvlášť"}),
    1867: (LIST, {"t_ru": "безопасность, уверенность", "t_uk": "безпека, упевненість", "t_en": "safety, security",
                  "t_tr": "güvenlik", "t_pl": "bezpieczeństwo, pewność"}),
    302: (LIST + "; uk «Як ти себе почуваєш?» — калька", {
        "t_ru": "чувствовать", "t_uk": "відчувати, почуватися", "t_en": "to feel", "t_tr": "hissetmek", "t_pl": "czuć",
        "x_uk": "Як ти почуваєшся?"}),
    2492: ("пять значений; «Ich führe das Gespräch» — пример ни о чём", {
        "t_ru": "вести, руководить", "t_uk": "вести, керувати", "t_en": "to lead, to run", "t_tr": "yönetmek, götürmek",
        "t_pl": "prowadzić, kierować", "t_it": "condurre, guidare", "t_es": "llevar, dirigir", "t_fr": "mener, diriger",
        "t_cs": "vést, řídit",
        **all_x("Diese Straße führt zum Bahnhof", "Эта улица ведёт к вокзалу", "Ця вулиця веде до вокзалу",
                "This street leads to the station", "Bu cadde istasyona çıkıyor", "Ta ulica prowadzi na dworzec",
                "Questa strada porta alla stazione", "Esta calle lleva a la estación", "Cette rue mène à la gare",
                "Tahle ulice vede k nádraží")}),
    1682: (EN, {"x_en": "What's your opinion?"}),
    249: (NEAR + " (Herbst: «Im Herbst fallen die Blätter» — внесено мной в блоке 19)", {
        "t_ru": "падать, упасть", "t_uk": "падати, упасти", "t_en": "to fall", "t_tr": "düşmek", "t_pl": "spadać, upaść",
        **all_x("Pass auf, dass du nicht fällst!", "Смотри не упади!", "Дивись не впади!", "Careful you don't fall!",
                "Dikkat et, düşme!", "Uważaj, żebyś nie upadł!", "Attento a non cadere!", "¡Cuidado, no te caigas!",
                "Fais attention à ne pas tomber!", "Dávej pozor, ať nespadneš!")}),
    1433: (LIST, {"t_ru": "следовать, идти за", "t_uk": "йти за, слідувати", "t_en": "to follow", "t_tr": "takip etmek",
                  "t_pl": "iść za, podążać"}),
    18596: (LIST + "; «До этого было всё иначе» — калька", {
        "t_ru": "раньше, до этого", "t_uk": "раніше, до цього", "t_en": "before, beforehand", "t_tr": "önceden",
        "t_pl": "wcześniej, przedtem", "x_ru": "Раньше всё было иначе"}),
    6324: (LIST, {"t_ru": "наружу, оттуда", "t_uk": "назовні, звідти", "t_en": "out", "t_tr": "dışarı",
                  "t_pl": "na zewnątrz"}),
}

SPLIT_LATER = {899: ["das Stück = пьеса (Theaterstück)"]}
