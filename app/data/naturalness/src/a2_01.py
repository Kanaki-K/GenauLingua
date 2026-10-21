"""A2, блок 1: слова 1–40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
TWO = "в строке два разных слова — оставлено главное, второе — отдельной строкой (блок деления)"
EN = "английский пример: так не говорят"
DULL = "пример ни о чём → фраза из жизни"
SAME = "пример совпадал с примером другого слова — у каждого свой"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    2104: (TWO + " («настоящий» — прилагательное wirklich, своя строка)", {
        "t_ru": "действительно, правда", "t_uk": "справді, дійсно", "t_en": "really, truly", "t_tr": "gerçekten",
        "t_pl": "naprawdę", "t_it": "davvero", "t_es": "realmente, de verdad", "t_fr": "vraiment",
        "t_cs": "opravdu, skutečně", "x_en": "That's really great"}),
    1014: (LIST, {"t_ru": "дорога, путь", "t_uk": "дорога, шлях", "t_en": "way, path", "t_tr": "yol", "t_pl": "droga",
                  "t_it": "la strada, il sentiero", "t_es": "el camino", "t_fr": "le chemin", "t_cs": "cesta"}),
    13295: (LIST, {"t_es": "tu"}),
    837: (LIST + "; пример почти повторял Weg («Der Weg ist …»)", {
        "t_ru": "безопасный, уверенный", "t_uk": "безпечний, упевнений", "t_en": "safe, sure", "t_tr": "güvenli, emin",
        "t_pl": "bezpieczny, pewny", "t_it": "sicuro", "t_es": "seguro", "t_fr": "sûr", "t_cs": "bezpečný, jistý",
        **all_x("Bist du sicher?", "Ты уверен?", "Ти впевнений?", "Are you sure?", "Emin misin?", "Jesteś pewny?",
                "Sei sicuro?", "¿Estás seguro?", "Tu es sûr?", "Jsi si jistý?")}),
    13810: (LIST, {"t_ru": "ну", "t_uk": "ну", "t_en": "well, so", "t_tr": "ee, peki", "t_pl": "no", "t_it": "allora, beh",
                   "t_es": "bueno, eh", "t_fr": "alors, eh bien", "t_cs": "no, tak"}),
    539: (TWO + " («велеть», «перестать» — свои строки); «Lass das» — «перестань», а не «оставь это»", {
        "t_ru": "оставить, позволить", "t_uk": "залишити, дозволити", "t_en": "to leave, to let",
        "t_tr": "bırakmak, izin vermek", "t_pl": "zostawić, pozwolić", "t_it": "lasciare", "t_es": "dejar",
        "t_fr": "laisser", "t_cs": "nechat",
        **all_x("Lass mich in Ruhe!", "Оставь меня в покое!", "Залиш мене в спокої!", "Leave me alone!",
                "Beni rahat bırak!", "Zostaw mnie w spokoju!", "Lasciami in pace!", "¡Déjame en paz!",
                "Laisse-moi tranquille!", "Nech mě být!")}),
    13300: (LIST, {"t_ru": "иметь в виду, считать", "t_uk": "мати на увазі, вважати", "t_en": "to mean, to think",
                   "t_tr": "demek istemek, düşünmek", "t_pl": "mieć na myśli, uważać", "t_it": "intendere, pensare",
                   "t_es": "querer decir, opinar", "t_fr": "vouloir dire, penser", "t_cs": "myslet, mínit"}),
    325: (LIST + "; «Это точно то, что нужно» — не тот смысл", {
        "t_ru": "точно, именно", "t_uk": "точно, саме", "t_en": "exactly", "t_tr": "tam, aynen", "t_pl": "dokładnie",
        "t_it": "esattamente", "t_es": "exactamente", "t_fr": "exactement", "t_cs": "přesně",
        **all_x("Genau, so machen wir das", "Точно, так и сделаем", "Точно, так і зробимо", "Exactly, that's what we'll do",
                "Aynen, öyle yapalım", "Dokładnie, tak zrobimy", "Esatto, facciamo così", "Exacto, lo hacemos así",
                "Exactement, on fait comme ça", "Přesně, tak to uděláme")}),
    2106: (LIST, {"t_ru": "пожалуй, наверное", "t_uk": "мабуть", "t_en": "probably", "t_tr": "herhalde", "t_pl": "chyba",
                  "t_it": "probabilmente", "t_es": "probablemente", "t_fr": "sans doute", "t_cs": "asi"}),
    749: (LIST + "; " + EN, {"t_ru": "говорить, разговаривать", "t_uk": "говорити, розмовляти", "t_en": "to talk",
                             "t_tr": "konuşmak", "t_pl": "rozmawiać, mówić", "t_it": "parlare", "t_es": "hablar",
                             "t_fr": "parler", "t_cs": "mluvit", "x_en": "We're talking about the problem"}),
    6186: (LIST + "; «выйдем наружу» — неживо", {
        "t_ru": "наружу, на улицу", "t_uk": "назовні, геть", "t_en": "out", "t_tr": "dışarı", "t_pl": "na zewnątrz",
        "x_ru": "Пошли, выйдем на улицу"}),
    691: (TWO + " («несколько» — ein paar, своя строка); «Das Paar tanzt» — пример ни о чём", {
        "t_ru": "пара", "t_uk": "пара", "t_en": "couple, pair", "t_tr": "çift", "t_pl": "para",
        "t_it": "la coppia, il paio", "t_es": "la pareja, el par", "t_fr": "le couple, la paire", "t_cs": "pár",
        **all_x("Die beiden sind ein schönes Paar", "Они красивая пара", "Вони гарна пара", "They make a lovely couple",
                "Çok güzel bir çift", "Są piękną parą", "Sono una bella coppia", "Hacen buena pareja",
                "Ils forment un beau couple", "Jsou krásný pár")}),
    1040: (LIST, {"t_ru": "почему, как так", "t_uk": "чому", "t_en": "why, how come", "t_tr": "neden",
                  "t_pl": "dlaczego, czemu"}),
    645: (TWO + " («натуральный» — прилагательное, своя строка); «Natürlich, das ist gut» — неживо", {
        "t_ru": "конечно, естественно", "t_uk": "звичайно, природно", "t_en": "of course, naturally",
        "t_tr": "elbette, tabii ki", "t_pl": "oczywiście", "t_it": "naturalmente, certo", "t_es": "por supuesto, claro",
        "t_fr": "bien sûr, naturellement", "t_cs": "samozřejmě",
        **all_x("Kommst du mit? — Natürlich!", "Пойдёшь с нами? — Конечно!", "Підеш з нами? — Звичайно!",
                "Are you coming? — Of course!", "Geliyor musun? — Elbette!", "Idziesz z nami? — Oczywiście!",
                "Vieni con noi? — Naturalmente!", "¿Vienes? — ¡Por supuesto!", "Tu viens? — Bien sûr!",
                "Jdeš s námi? — Samozřejmě!")}),
    6193: (LIST, {"t_ru": "совсем, вовсе", "t_uk": "зовсім", "t_en": "at all", "t_tr": "hiç", "t_pl": "wcale",
                  "t_it": "affatto", "t_es": "en absoluto, nada", "t_fr": "du tout", "t_cs": "vůbec"}),
    13313: (SAME + " (Theater: «Wir gehen ins Theater»)", {
        "t_ru": "в", "t_uk": "в, до", "t_en": "into the", "t_tr": "-e", "t_pl": "do", "t_it": "nel", "t_es": "al, en el",
        "t_fr": "dans le, au", "t_cs": "do",
        **all_x("Komm, wir springen ins Wasser!", "Давай, прыгаем в воду!", "Давай стрибнемо у воду!",
                "Come on, let's jump into the water!", "Hadi, suya atlayalım!", "Chodź, skaczemy do wody!",
                "Dai, saltiamo in acqua!", "¡Venga, saltamos al agua!", "Allez, on saute dans l'eau!",
                "Pojď, skočíme do vody!")}),
    13815: (LIST, {"t_ru": "ах, ой", "t_uk": "ах, ой", "t_en": "oh, ah"}),
    13315: (LIST, {"t_ru": "из этого, об этом", "t_uk": "з цього, про це", "t_en": "of it, about it", "t_tr": "ondan",
                   "t_pl": "z tego, o tym", "t_it": "ne", "t_es": "de eso", "t_fr": "en", "t_cs": "z toho, o tom"}),
    161: (LIST, {"t_ru": "за это, для этого", "t_uk": "за це, для цього", "t_en": "for it", "t_tr": "bunun için",
                 "t_pl": "za to", "t_it": "per questo", "t_es": "para eso, a favor", "t_fr": "pour ça", "t_cs": "za to"}),
    1537: (LIST, {"t_ru": "туда", "t_uk": "туди", "t_en": "there", "t_tr": "oraya", "t_pl": "tam", "t_it": "là",
                  "t_es": "allá", "t_fr": "là-bas", "t_cs": "tam"}),
    1136: (LIST + "; «У меня страх перед пауками» — калька", {
        "t_ru": "страх, боязнь", "t_uk": "страх", "t_en": "fear", "t_tr": "korku", "t_pl": "strach, lęk",
        "x_ru": "Я боюсь пауков", "x_pl": "Boję się pająków"}),
    6206: (LIST, {"t_ru": "внутрь", "t_uk": "всередину", "t_en": "in", "t_tr": "içeri", "t_pl": "do środka",
                  "t_it": "dentro", "t_es": "dentro, adentro", "t_fr": "dedans", "t_cs": "dovnitř"}),
    21: (LIST + "; «Мы выбираем другой путь» — калька", {
        "t_ru": "другой, остальные", "t_uk": "інший, решта", "t_en": "other, another", "t_tr": "diğer, başka",
        "t_pl": "inny, pozostali", "t_it": "altro", "t_es": "otro", "t_fr": "autre", "t_cs": "jiný, ostatní",
        "x_ru": "Пойдём другой дорогой", "x_uk": "Підемо іншою дорогою", "x_en": "Let's take another way"}),
    18567: (LIST, {"t_ru": "только, лишь", "t_uk": "лише, тільки", "t_en": "only, not until", "t_tr": "ancak, henüz",
                   "t_pl": "dopiero", "t_it": "solo, appena", "t_es": "solo, apenas", "t_fr": "seulement, ne que",
                   "t_cs": "teprve, až"}),
    1473: (LIST, {"t_ru": "достаточно, хватит", "t_uk": "достатньо, досить", "t_en": "enough", "t_tr": "yeterince",
                  "t_pl": "wystarczająco, dość"}),
    6212: (LIST, {"t_ru": "весь, целый", "t_uk": "весь, цілий", "t_en": "whole, entire", "t_tr": "bütün, tüm",
                  "t_pl": "cały", "t_it": "intero, tutto", "t_es": "entero, todo", "t_fr": "entier, tout",
                  "x_ru": "Я ждал всё время"}),
    108: ("«Bevor ich gehe, sage ich tschüss» — неживо и в немецком; " + LIST, {
        "t_ru": "прежде чем, перед тем как", "t_uk": "перед тим як", "t_en": "before", "t_tr": "-meden önce",
        "t_pl": "zanim",
        **all_x("Wasch dir die Hände, bevor du isst", "Помой руки, прежде чем есть", "Помий руки перед тим, як їсти",
                "Wash your hands before you eat", "Yemekten önce ellerini yıka", "Umyj ręce, zanim zjesz",
                "Lavati le mani prima di mangiare", "Lávate las manos antes de comer", "Lave-toi les mains avant de manger",
                "Umyj si ruce, než budeš jíst")}),
    13330: (LIST, {"t_ru": "каждый, любой", "t_uk": "кожен, будь-який", "t_en": "every, everyone", "t_tr": "her, herkes",
                   "t_pl": "każdy", "t_it": "ognuno, ogni", "t_es": "cada, todo el mundo", "t_fr": "chaque, tout le monde"}),
    1513: (LIST, {"t_ru": "остановка, опора", "t_uk": "зупинка, опора", "t_en": "stop, support", "t_tr": "durak, destek",
                  "t_pl": "przystanek, oparcie"}),
    774: (LIST, {"t_ru": "вещь, дело", "t_uk": "річ, справа", "t_en": "thing, matter", "t_tr": "şey, mesele",
                 "t_pl": "rzecz, sprawa", "x_en": "That's a simple thing"}),
    170: (LIST + "; «Что ты хочешь к этому?» — калька", {
        "t_ru": "к этому, кроме того", "t_uk": "до цього, крім того", "t_en": "with it, in addition",
        "t_tr": "buna, ayrıca", "t_pl": "do tego, poza tym", "t_it": "con questo, inoltre", "t_es": "con eso, además",
        "t_fr": "avec ça, en plus", "t_cs": "k tomu, navíc", "x_ru": "Что будешь к этому?"}),
    172: (LIST + "; «вспоминать о чём-то» — denken an, своя строка", {
        "t_ru": "думать, считать", "t_uk": "думати, вважати", "t_en": "to think", "t_tr": "düşünmek", "t_pl": "myśleć",
        "t_it": "pensare", "t_es": "pensar", "t_fr": "penser", "t_cs": "myslet", "x_en": "I think that's good"}),
    13335: (LIST, {"t_ru": "об этом, на этом", "t_uk": "про це, на цьому", "t_en": "about it, of it", "t_tr": "onu",
                   "t_pl": "o tym", "t_it": "ne, ci", "t_es": "de eso, en eso", "t_fr": "en, y", "t_cs": "na to, o tom"}),
    1346: (LIST, {"t_ru": "всё равно", "t_uk": "байдуже, однаково", "t_en": "doesn't matter", "t_tr": "fark etmez",
                  "t_pl": "wszystko jedno, obojętny", "t_it": "indifferente", "t_es": "igual", "t_fr": "égal",
                  "t_cs": "jedno"}),
    6224: (TWO + " («падеж» — своя строка)", {"t_ru": "случай, падение", "t_uk": "випадок, падіння", "t_en": "case, fall",
                                             "t_tr": "durum, düşme", "t_pl": "przypadek, upadek"}),
    976: (LIST + "; «оставлять где-то» — другое употребление", {
        "t_ru": "забывать, забыть", "t_uk": "забувати, забути", "t_en": "to forget", "t_tr": "unutmak",
        "t_pl": "zapominać, zapomnieć", "t_cs": "zapomenout"}),
    13338: (LIST, {"t_ru": "на это, этого", "t_uk": "на це", "t_en": "on it, to it", "t_tr": "ona", "t_pl": "na to",
                   "t_it": "su questo, ci", "t_es": "en eso", "t_fr": "en, y", "t_cs": "na to"}),
}

SPLIT_LATER = {
    2104: ["wirklich = настоящий (eine wirkliche Hilfe)"],
    539: ["lassen = велеть, сделать (sich die Haare schneiden lassen)", "lassen = перестать (Lass das!)"],
    691: ["ein paar = несколько"],
    645: ["natürlich = натуральный, естественный"],
    6224: ["der Fall = падеж"],
    172: ["denken an = вспоминать о, думать о"],
}
