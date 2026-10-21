"""B1, блок 31: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    16042: ("«Das Erbe ist sehr wertvoll» — пусто", {"t_tr": "miras", **all_x(
        "Er hat sein ganzes Erbe verspielt", "Он проиграл всё наследство", "Він програв увесь спадок",
        "He gambled away his whole inheritance", "Bütün mirasını kumarda kaybetti", "Przegrał cały spadek",
        "Si è giocato tutta l'eredità", "Se jugó toda la herencia", "Il a perdu tout son héritage au jeu",
        "Prohrál celé dědictví")}),
    11673: (LIST, {"t_ru": "пища, корм", "t_uk": "їжа, корм", "t_en": "food, nourishment", "t_tr": "besin, yem",
                   "t_pl": "pożywienie, pokarm", "t_it": "il cibo, il nutrimento"}),
    6809: ("«Er steht an der Front der Gruppe» — так не говорят; " + LIST, {
        "t_ru": "фронт, фасад", "t_uk": "фронт, фасад", "t_en": "front, facade", "t_tr": "cephe, ön yüz",
        "t_pl": "front, fasada", "t_it": "il fronte, la facciata", "t_es": "el frente, la fachada",
        "t_fr": "le front, la façade", "t_cs": "fronta, průčelí",
        **all_x("Mein Opa war im Krieg an der Front", "Мой дед в войну был на фронте", "Мій дід у війну був на фронті",
                "My grandad was at the front in the war", "Dedem savaşta cephedeydi",
                "Mój dziadek był na froncie w czasie wojny", "Mio nonno in guerra era al fronte",
                "Mi abuelo estuvo en el frente durante la guerra", "Mon grand-père était au front pendant la guerre",
                "Děda byl za války na frontě")}),
    6810: ("«Das Essen wird bald verderben» — пусто; " + LIST, {
        "t_ru": "портиться, портить", "t_uk": "псуватися, псувати", "t_en": "to spoil, to go bad",
        "t_tr": "bozulmak, keyfini kaçırmak", "t_pl": "psuć się, psuć", "t_it": "andare a male, rovinare",
        "t_es": "echarse a perder, arruinar", "t_fr": "se gâter, gâcher", "t_cs": "zkazit se, kazit",
        **all_x("Du verdirbst mir den ganzen Spaß!", "Ты мне весь кайф портишь!", "Ти мені всю забаву псуєш!",
                "You're spoiling all my fun!", "Bütün keyfimi kaçırıyorsun!", "Psujesz mi całą zabawę!",
                "Mi stai rovinando tutto il divertimento!", "¡Me estás arruinando toda la diversión!",
                "Tu gâches tout le plaisir!", "Kazíš mi celou zábavu!")}),
    14429: (LIST, {"t_ru": "сезон, эстафета", "t_uk": "сезон, естафета", "t_en": "season, relay",
                   "t_tr": "sezon, bayrak yarışı", "t_pl": "sezon, sztafeta", "t_it": "la stagione, la staffetta",
                   "t_cs": "řada, štafeta"}),
    6812: (LIST, {"t_ru": "заменять, представлять", "t_uk": "заміняти, представляти",
                  "t_en": "to stand in for, to represent", "t_tr": "yerine bakmak, temsil etmek",
                  "t_pl": "zastępować, reprezentować", "t_it": "sostituire, rappresentare", "t_es": "sustituir, representar",
                  "t_fr": "remplacer, représenter", "t_cs": "zastoupit, zastupovat"}),
    6813: (LIST + "; ru «Игра передаётся» — калька", {
        "t_ru": "транслировать, передавать", "t_uk": "транслювати, передавати", "t_en": "to broadcast, to transfer",
        "t_tr": "yayınlamak, aktarmak", "t_pl": "transmitować, przenosić", "t_es": "transmitir, contagiar",
        "t_fr": "retransmettre, transmettre", "t_cs": "vysílat, přenášet",
        "x_ru": "Матч транслируют в прямом эфире", "x_en": "The match is being broadcast live"}),
    8807: ("убрать пометки (fam.)/(hovor.); " + LIST, {
        "t_ru": "профи, профессионал", "t_uk": "профі, професіонал", "t_en": "pro, professional",
        "t_pl": "zawodowiec, fachowiec", "t_fr": "le pro, le professionnel", "t_cs": "profík, profesionál"}),
    15451: ("«Der Fisch beißt nicht am Köder» — так не говорят (beißt nicht an); " + LIST, {
        "t_ru": "наживка, приманка", "t_uk": "наживка, приманка", "t_tr": "yem, tuzak", "t_pl": "przynęta",
        **all_x("Welchen Köder nimmst du für Forellen?", "Какую наживку ты берёшь на форель?", "Яку наживку ти береш на форель?",
                "What bait do you use for trout?", "Alabalık için hangi yemi kullanıyorsun?",
                "Jakiej przynęty używasz na pstrągi?", "Che esca usi per le trote?", "¿Qué cebo usas para las truchas?",
                "Tu prends quel appât pour les truites?", "Jakou návnadu bereš na pstruhy?")}),
    2232: ("«Ich schalte das Licht aus» — пусто; " + LIST, {
        "t_ru": "выключать, устранять", "t_uk": "вимикати, усувати", "t_en": "to switch off, to eliminate",
        "t_tr": "kapatmak, devre dışı bırakmak", "t_pl": "wyłączać, eliminować", "t_es": "apagar, eliminar",
        "t_fr": "éteindre, éliminer", "t_cs": "vypnout, vyřadit",
        **all_x("Schalt bitte dein Handy aus", "Выключи, пожалуйста, телефон", "Вимкни, будь ласка, телефон",
                "Please switch your phone off", "Lütfen telefonunu kapat", "Wyłącz, proszę, telefon",
                "Spegni il telefono, per favore", "Apaga el móvil, por favor", "Éteins ton téléphone, s'il te plaît",
                "Vypni si prosím mobil")}),
    11675: ("«Das Hühnchen schmeckt gut» — пусто; " + LIST, {
        "t_ru": "курица, цыплёнок", "t_uk": "курка, курча", "t_en": "chicken", "t_tr": "tavuk, piliç", "t_pl": "kurczak",
        **all_x("Heute gibt es Hühnchen mit Reis", "Сегодня курица с рисом", "Сьогодні курка з рисом",
                "It's chicken and rice today", "Bugün pilavlı tavuk var", "Dziś jest kurczak z ryżem",
                "Oggi c'è pollo con riso", "Hoy hay pollo con arroz", "Aujourd'hui, c'est poulet-riz",
                "Dneska je kuře s rýží")}),
    6815: ("en «the highest step» — так не говорят; " + LIST, {
        "t_ru": "ступенька, уровень", "t_uk": "сходинка, рівень", "t_en": "step, level", "t_tr": "basamak, seviye",
        "t_pl": "stopień, poziom", "t_it": "il gradino, il livello", "t_es": "el escalón, el nivel",
        "t_fr": "la marche, le niveau", "t_cs": "schod, stupeň",
        **all_x("Er nimmt immer zwei Stufen auf einmal", "Он всегда перепрыгивает через две ступеньки",
                "Він завжди переступає через дві сходинки", "He always takes the stairs two steps at a time",
                "Merdivenleri hep ikişer basamak çıkıyor", "Zawsze wchodzi po dwa stopnie naraz",
                "Fa sempre due gradini alla volta", "Siempre sube los escalones de dos en dos",
                "Il monte toujours les marches deux par deux", "Vždycky bere dva schody najednou")}),
    14431: ("«Der Unfall war eine echte Tragödie …» — хроника; " + LIST, {
        "t_ru": "трагедия", "t_uk": "трагедія", "t_en": "tragedy", "t_tr": "trajedi, felaket", "t_pl": "tragedia",
        **all_x("Mach doch keine Tragödie daraus!", "Не делай из этого трагедию!", "Не роби з цього трагедію!",
                "Don't turn it into a tragedy!", "Bunu trajediye çevirme!", "Nie rób z tego tragedii!",
                "Non farne una tragedia!", "¡No hagas de esto una tragedia!", "N'en fais pas une tragédie!",
                "Nedělej z toho tragédii!")}),
    16043: ("пример про Geiselnehmer, а не про Geisel; хроника", {
        "t_ru": "заложник", "t_uk": "заручник", "t_tr": "rehine", "t_pl": "zakładnik",
        **all_x("Im Film nehmen die Räuber zwei Geiseln", "В фильме грабители берут двух заложников",
                "У фільмі грабіжники беруть двох заручників", "In the film the robbers take two hostages",
                "Filmde soyguncular iki rehine alıyor", "W filmie złodzieje biorą dwóch zakładników",
                "Nel film i rapinatori prendono due ostaggi", "En la película los atracadores toman dos rehenes",
                "Dans le film, les braqueurs prennent deux otages", "Ve filmu lupiči berou dvě rukojmí")}),
    17511: (LIST, {"t_ru": "кабель, провод", "t_uk": "кабель, провід", "t_en": "cable, wire", "t_pl": "kabel, przewód",
                   "t_cs": "kabel, šňůra"}),
    16044: (LIST, {"t_ru": "переговоры, разбирательство", "t_uk": "переговори, розгляд справи",
                   "t_en": "negotiation, hearing", "t_tr": "müzakere, duruşma", "t_pl": "negocjacje, rozprawa",
                   "t_it": "la trattativa, l'udienza", "t_cs": "jednání, přelíčení",
                   "x_en": "The negotiations on the contract have been going on for three hours"}),
    10324: ("пример книжный, en не совпадает с de; " + LIST, {
        "t_ru": "горе, огорчение", "t_uk": "горе, журба", "t_en": "sorrow, trouble", "t_tr": "keder, dert",
        "t_pl": "smutek, zmartwienie", "t_it": "il dispiacere, il dolore", "t_es": "la pena, la preocupación",
        "t_fr": "le chagrin, la peine", "t_cs": "žal, starost",
        **all_x("Was hast du denn für Kummer?", "Что у тебя за горе?", "Що в тебе за горе?", "What's your trouble?",
                "Derdin ne?", "Jakie masz zmartwienie?", "Qual è il tuo dispiacere?", "¿Qué pena tienes?",
                "Qu'est-ce qui te fait de la peine?", "Jakou máš starost?")}),
    14995: ("«Papi kommt gleich nach Hause von der Arbeit» — порядок слов; убрать пометку (hovor.)", {
        "t_cs": "tatínek, taťka", "t_ru": "папочка, папа",
        **all_x("Papi ist noch auf der Arbeit", "Папочка ещё на работе", "Татко ще на роботі",
                "Daddy's still at work", "Babacığım hâlâ işte", "Tatuś jest jeszcze w pracy",
                "Papino è ancora al lavoro", "Papi todavía está en el trabajo", "Papa est encore au travail",
                "Tatínek je ještě v práci")}),
    13651: (LIST, {"t_ru": "костюм, женский костюм", "t_en": "costume, women's suit",
                   "t_tr": "kostüm, kadın takım elbisesi", "t_pl": "kostium, przebranie", "t_it": "il costume, il tailleur"}),
    14432: (LIST + "; en «movie» — американское", {
        "t_ru": "существо, тварь", "t_uk": "істота, створіння", "t_tr": "yaratık, canlı", "t_pl": "stworzenie, istota",
        "t_cs": "stvoření, tvor", "x_en": "In this horror film he fights strange creatures"}),
    6816: (LIST + "; ru «Нам нужно сейчас возвращаться» — калька", {
        "t_ru": "возвращаться, снижаться", "t_uk": "повертатися, спадати", "t_en": "to go back, to decline",
        "t_tr": "geri dönmek, azalmak", "t_pl": "wracać, spadać", "t_it": "tornare indietro, diminuire",
        "t_es": "volver, disminuir", "t_fr": "rentrer, diminuer", "t_cs": "vrátit se, klesat",
        "x_ru": "Пора возвращаться, уже темнеет", "x_en": "We need to head back now, it's getting dark"}),
    6817: (LIST, {"t_ru": "начинаться, отправляться", "t_uk": "починатися, вирушати", "t_en": "to start, to set off",
                  "t_tr": "başlamak, yola çıkmak", "t_pl": "zaczynać się, ruszać", "t_it": "cominciare, partire",
                  "t_es": "empezar, ponerse en marcha", "t_fr": "commencer, partir", "t_cs": "začít, vyrazit"}),
    10325: ("убрать пометки (fam.)/(hovor.); " + LIST, {
        "t_ru": "придурок, идиот", "t_uk": "дурень, придурок", "t_en": "idiot, jerk", "t_tr": "ahmak, aptal",
        "t_pl": "dureń, głupek", "t_it": "lo scemo, il cretino", "t_fr": "l'imbécile, le crétin", "t_cs": "hlupák, blbec"}),
    10326: ("«Sei anständig und entschuldige dich» — учебник; " + LIST, {
        "t_ru": "порядочный, нормальный", "t_uk": "порядний, нормальний", "t_en": "decent, proper",
        "t_tr": "dürüst, doğru dürüst", "t_pl": "porządny, przyzwoity", "t_it": "perbene, decente",
        "t_es": "decente, correcto", "t_fr": "correct, honnête",
        **all_x("Iss mal was Anständiges!", "Поешь нормально!", "Поїж нормально!", "Eat something decent!",
                "Doğru dürüst bir şey ye!", "Zjedz coś porządnego!", "Mangia qualcosa di decente!", "¡Come algo decente!",
                "Mange quelque chose de correct!", "Najez se pořádně!")}),
    8808: (LIST, {"t_ru": "зарплата, награда", "t_uk": "зарплата, винагорода", "t_en": "pay, reward",
                  "t_tr": "maaş, ücret", "t_pl": "pensja, wynagrodzenie", "t_it": "lo stipendio, la ricompensa",
                  "t_es": "el sueldo, la recompensa", "t_fr": "le salaire, la récompense", "t_cs": "výplata, odměna",
                  "x_en": "My pay always comes in at the end of the month"}),
    6819: (LIST + "; en «elevator» — американское", {
        "t_ru": "запертый, включённый", "t_uk": "замкнений, включений", "t_en": "locked in, included",
        "t_tr": "mahsur, dahil", "t_pl": "zamknięty, włącznie", "t_it": "chiuso dentro, incluso",
        "t_es": "encerrado, incluido", "t_fr": "enfermé, inclus", "t_cs": "zavřený, zahrnutý",
        "x_en": "We're trapped in the lift"}),
    6820: (LIST, {"t_ru": "в конце концов, в итоге", "t_uk": "зрештою, у підсумку", "t_en": "in the end, ultimately",
                  "t_tr": "sonuçta, en sonunda", "t_pl": "ostatecznie, w końcu"}),
    6821: ("ru «монеты происходят из восемнадцатого века» — калька; " + LIST, {
        "t_ru": "происходить, быть родом", "t_uk": "походити, бути родом", "t_en": "to come from, to date from",
        "t_tr": "gelmek, kökeni olmak", "t_pl": "pochodzić, wywodzić się", "t_it": "provenire, essere originario",
        "t_es": "proceder, datar de", "t_fr": "venir de, dater de",
        **all_x("Woher stammst du eigentlich?", "Ты, вообще, откуда родом?", "Ти взагалі звідки родом?",
                "Where do you actually come from?", "Aslen nereden geliyorsun?", "Skąd właściwie pochodzisz?",
                "Di dove sei originario, in realtà?", "¿De dónde procedes, en realidad?", "Tu viens d'où, au fait?",
                "Odkud vlastně pocházíš?")}),
    10327: (LIST, {"t_ru": "прощение", "t_uk": "прощення, пробачення", "t_en": "forgiveness", "t_tr": "af, bağışlama",
                   "t_pl": "przebaczenie, wybaczenie"}),
    12542: ("ru «даёт мне моё лекарство» — калька; «female nurse» — лишнее", {
        "t_en": "nurse", "t_tr": "hemşire", "t_pl": "pielęgniarka",
        "x_ru": "Медсестра каждый день даёт мне лекарство"}),
    2066: ("«Bitte füll das Formular vollständig aus» — анкета; " + LIST, {
        "t_ru": "полный, полностью", "t_uk": "повний, повністю", "t_en": "complete, full", "t_tr": "eksiksiz, tam",
        "t_pl": "kompletny, pełny", "t_cs": "úplný, kompletní",
        **all_x("Ist die Liste vollständig?", "Список полный?", "Список повний?", "Is the list complete?",
                "Liste eksiksiz mi?", "Czy lista jest kompletna?", "La lista è completa?", "¿Está completa la lista?",
                "La liste est complète?", "Je ten seznam úplný?")}),
    14433: (LIST + "; en «movie» — американское", {
        "t_ru": "экшн, движуха", "t_uk": "екшн, рух", "t_en": "action, thrills", "t_tr": "aksiyon, heyecan",
        "t_pl": "akcja, emocje", "x_en": "This film has a lot of action"}),
    18166: ("«Der Turm ist hoch» — пусто", {**all_x(
        "Vom Turm hat man einen tollen Blick", "С башни открывается отличный вид", "З вежі відкривається чудовий вид",
        "You get a great view from the tower", "Kuleden harika bir manzara var", "Z wieży jest świetny widok",
        "Dalla torre si gode una vista fantastica", "Desde la torre hay unas vistas geniales",
        "Du haut de la tour, on a une vue géniale", "Z věže je skvělý výhled")}),
    2655: ("«Der Hund ist an der Leine» — пусто; " + LIST, {
        "t_ru": "поводок, верёвка", "t_uk": "повідець, мотузка", "t_en": "lead, leash", "t_tr": "tasma, ip",
        "t_pl": "smycz, linka", "t_it": "il guinzaglio, la corda", "t_es": "la correa, la cuerda",
        "t_fr": "la laisse, la corde",
        **all_x("Nimm den Hund bitte an die Leine", "Возьми, пожалуйста, собаку на поводок",
                "Візьми, будь ласка, собаку на повідець", "Please put the dog on the lead", "Lütfen köpeğe tasma tak",
                "Weź, proszę, psa na smycz", "Metti il guinzaglio al cane, per favore",
                "Ponle la correa al perro, por favor", "Mets le chien en laisse, s'il te plaît",
                "Vezmi prosím psa na vodítko")}),
    12147: ("«Mit einem großen Sprung ist er … gesprungen» — масло масляное; " + LIST, {
        "t_ru": "прыжок, трещина", "t_uk": "стрибок, тріщина", "t_en": "jump, crack", "t_tr": "sıçrama, çatlak",
        "t_pl": "skok, pęknięcie", "t_fr": "le saut, la fissure",
        **all_x("Das Glas hat einen Sprung", "В стакане трещина", "У склянці тріщина", "The glass has a crack in it",
                "Bardakta çatlak var", "Szklanka ma pęknięcie", "Il bicchiere ha una crepa", "El vaso tiene una grieta",
                "Le verre a une fissure", "Ta sklenice má prasklinu")}),
}

SPLIT_LATER = {
    11675: ["mit jemandem ein Hühnchen rupfen = свести счёты"],
    13494: ["jene — письменное слово; проверить уровень (C1?)"],
}
