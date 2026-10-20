"""A1, блок 7: слова 241–280 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
TWO = "в строке два разных слова — оставлено главное, второе — отдельной строкой (блок деления)"
EN = "английский пример: так не говорят о том, что происходит сейчас"
DULL = "пример ни о чём («X ist Y») → фраза из жизни"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    1736: (LIST, {"t_ru": "номер", "t_uk": "номер", "t_en": "number", "t_tr": "numara", "t_pl": "numer"}),
    250: (LIST, {"t_ru": "неправильный, не тот", "t_uk": "неправильний, не той", "t_en": "wrong, false",
                 "t_tr": "yanlış", "t_pl": "błędny, zły", "t_it": "sbagliato", "t_es": "incorrecto, equivocado",
                 "t_fr": "faux", "t_cs": "špatný, chybný", "x_en": "Unfortunately, that's wrong"}),
    295: (LIST + "; «He lived in Berlin earlier» — так не говорят", {
        "t_ru": "раньше", "t_uk": "раніше", "t_en": "in the past, earlier", "t_tr": "eskiden",
        "t_pl": "wcześniej, kiedyś", "t_it": "prima, una volta", "t_es": "antes", "t_fr": "avant, autrefois",
        "t_cs": "dříve, kdysi", "x_en": "He used to live in Berlin"}),
    1041: ("«Willkommen hier» — так не говорят; «к нам» — лишнее", {
        "t_ru": "добро пожаловать", "t_uk": "ласкаво просимо", "t_tr": "hoş geldiniz", "t_pl": "witamy",
        "t_cs": "vítejte",
        **all_x("Herzlich willkommen!", "Добро пожаловать!", "Ласкаво просимо!", "Welcome!", "Hoş geldiniz!",
                "Serdecznie witamy!", "Benvenuti!", "¡Bienvenidos!", "Bienvenue!", "Srdečně vítáme!")}),
    200: (LIST + "; uk «нам дозволено» — канцелярски", {
        "t_ru": "можно, иметь право", "t_uk": "можна, мати право", "t_en": "may, to be allowed",
        "t_tr": "izni olmak", "t_pl": "móc, wolno", "t_it": "potere", "t_es": "poder", "t_cs": "smět",
        "x_uk": "Сьогодні нам можна залишитися довше"}),
    715: (LIST, {"t_ru": "план", "t_uk": "план", "t_en": "plan", "t_tr": "plan", "t_pl": "plan",
                 "t_it": "il piano, il progetto", "t_es": "el plan", "t_fr": "le plan, le projet",
                 "x_en": "What's the plan?"}),
    6277: (LIST, {"t_ru": "ошибка", "t_uk": "помилка", "t_en": "mistake, error", "t_tr": "hata", "t_pl": "błąd",
                  "t_it": "l'errore, lo sbaglio", "t_es": "el error, el fallo", "t_fr": "l'erreur, la faute",
                  "t_cs": "chyba"}),
    13375: (EN, {"x_en": "I'm ten years old"}),
    537: (LIST, {"t_pl": "powoli, wolno", "t_it": "lentamente, piano", "t_es": "despacio, lento",
                 "t_fr": "lentement, lent"}),
    896: (LIST, {"t_ru": "час, урок", "t_uk": "година, урок", "t_en": "hour, lesson", "t_tr": "saat, ders",
                 "t_pl": "godzina, lekcja", "t_it": "l'ora, la lezione", "t_es": "la hora, la clase",
                 "t_fr": "l'heure, le cours"}),
    270: (LIST + "; " + EN, {"t_ru": "фильм", "t_uk": "фільм", "t_en": "film, movie", "t_tr": "film",
                             "t_pl": "film", "x_en": "We're watching a film"}),
    551: (LIST, {"t_ru": "любить", "t_en": "to love", "t_tr": "sevmek", "t_pl": "kochać", "t_it": "amare",
                 "t_es": "amar, querer", "t_fr": "aimer"}),
    15370: (LIST + "; " + DULL, {
        "t_ru": "огонь, пожар", "t_uk": "вогонь, пожежа", "t_en": "fire", "t_tr": "ateş, yangın",
        "t_pl": "ogień, pożar",
        **all_x("Lass uns ein Feuer machen", "Давай разведём огонь", "Давай розпалимо вогонь", "Let's make a fire",
                "Hadi ateş yakalım", "Rozpalmy ogień", "Accendiamo un fuoco", "Hagamos un fuego", "Faisons un feu",
                "Rozdělejme oheň")}),
    546: (LIST, {"t_es": "por desgracia, lamentablemente"}),
    547: (LIST + "; " + EN, {"t_ru": "учить, учиться", "t_uk": "вчити, вчитися", "t_tr": "öğrenmek",
                             "x_en": "I'm learning German"}),
    1642: (TWO + " («работать» о машине, «идти» о фильме — свои строки)", {
        "t_ru": "бегать, ходить", "t_uk": "бігати, ходити", "t_en": "to run, to walk", "t_tr": "koşmak, yürümek",
        "t_pl": "biegać, chodzić", "t_it": "correre, camminare", "t_es": "correr, caminar",
        "t_fr": "courir, marcher", "t_cs": "běhat, chodit"}),
    1909: (LIST + "; «Я ищу должность» — канцелярски", {
        "t_ru": "место, должность", "t_uk": "місце, посада", "t_en": "place, job", "t_tr": "yer, iş",
        "t_pl": "miejsce, posada", "t_it": "il posto, il punto", "t_es": "el puesto, el lugar",
        "t_fr": "le poste, l'endroit", "t_cs": "místo",
        **all_x("Ich suche eine neue Stelle", "Я ищу новое место работы", "Я шукаю нове місце роботи",
                "I'm looking for a new job", "Yeni bir iş arıyorum", "Szukam nowej pracy",
                "Cerco un nuovo posto di lavoro", "Busco un nuevo puesto de trabajo", "Je cherche un nouveau poste",
                "Hledám nové místo")}),
    6287: (LIST, {"t_uk": "приносити, забирати", "t_en": "to fetch, to get", "t_tr": "getirmek, almak",
                  "t_pl": "przynieść, iść po coś", "t_it": "andare a prendere", "t_es": "ir a buscar, traer",
                  "t_fr": "aller chercher", "t_cs": "přinést, dojít pro"}),
    885: (LIST + "; «What is the name of this street?» — книжно", {
        "t_ru": "улица, дорога", "t_uk": "вулиця, дорога", "t_en": "street, road", "t_tr": "sokak, cadde",
        "t_pl": "ulica, droga", "t_it": "la strada, la via", "t_es": "la calle, la carretera",
        "t_fr": "la rue, la route", "x_en": "What's this street called?"}),
    356: ("пять значений → главные два", {
        "t_ru": "большой, высокий", "t_uk": "великий, високий", "t_en": "big, tall", "t_tr": "büyük, uzun boylu",
        "t_pl": "duży, wysoki", "t_it": "grande, alto", "t_es": "grande, alto", "t_fr": "grand, gros",
        "t_cs": "velký, vysoký"}),
    142: (EN, {"x_en": "I'm reading an interesting book"}),
    1172: (LIST + "; «прекратить это» — калька", {
        "t_ru": "переставать, прекращать", "t_uk": "переставати, припиняти", "t_en": "to stop, to quit",
        "t_tr": "bırakmak, durmak", "t_pl": "przestawać, kończyć się", "t_it": "smettere, finire",
        "t_es": "dejar de, parar", "t_fr": "arrêter, cesser", "t_cs": "přestat, skončit",
        "x_ru": "Ты можешь, пожалуйста, перестать?", "x_pl": "Możesz przestać, proszę?"}),
    763: (TWO + " («по-настоящему» — наречие richtig, своя строка)", {
        "t_ru": "правильный, настоящий", "t_uk": "правильний, справжній", "t_en": "right, correct",
        "t_tr": "doğru", "t_pl": "poprawny, właściwy", "t_it": "giusto, corretto", "t_es": "correcto",
        "t_fr": "juste, bon", "t_cs": "správný", "x_en": "That's the right answer"}),
    509: (LIST, {"t_ru": "больной"}),
    12469: ("у Arzt и zum был один пример «Ich gehe zum Arzt» — у каждого свой", {
        **all_x("Der Arzt sagt, ich soll im Bett bleiben", "Врач говорит, что мне нужно лежать в постели",
                "Лікар каже, що мені треба лежати в ліжку", "The doctor says I should stay in bed",
                "Doktor yatakta kalmam gerektiğini söylüyor", "Lekarz mówi, że mam leżeć w łóżku",
                "Il medico dice che devo stare a letto", "El médico dice que tengo que quedarme en la cama",
                "Le médecin dit que je dois rester au lit", "Lékař říká, že mám zůstat v posteli")}),
    391: (LIST + "; " + EN, {"t_ru": "жениться, выходить замуж", "t_uk": "одружуватися, виходити заміж",
                             "t_pl": "brać ślub, żenić się", "x_en": "They're getting married in June"}),
    6292: (LIST, {"t_ru": "лёгкий, простой", "t_uk": "легкий, простий", "t_en": "light, easy", "t_tr": "hafif, kolay",
                  "t_pl": "lekki, łatwy", "t_it": "leggero, facile", "t_es": "ligero, fácil",
                  "t_fr": "léger, facile"}),
    293: (LIST + "; «Ich bin froh» без продолжения — так не говорят", {
        "t_ru": "рад, довольный", "t_uk": "радий, задоволений", "t_en": "glad, happy", "t_tr": "memnun, mutlu",
        "t_pl": "zadowolony, rad", "t_it": "contento, felice", "t_es": "contento", "t_fr": "content, heureux",
        "t_cs": "rád",
        **all_x("Ich bin froh, dass du da bist", "Я рад, что ты здесь", "Я радий, що ти тут", "I'm glad you're here",
                "Burada olduğun için mutluyum", "Cieszę się, że tu jesteś", "Sono contento che tu sia qui",
                "Estoy contento de que estés aquí", "Je suis content que tu sois là", "Jsem rád, že jsi tady")}),
    624: (LIST + "; «Я хотел бы кофе» — калька", {
        "t_ru": "хотел бы, хотеть", "t_en": "would like", "t_tr": "istemek", "t_pl": "chciałbym, chcieć",
        "t_es": "querer", "t_fr": "vouloir", "x_ru": "Я бы хотел кофе", "x_uk": "Я б хотів каву",
        "x_en": "I'd like a coffee"}),
    467: (LIST + "; " + EN, {"t_en": "to buy", "t_tr": "satın almak, almak", "x_en": "I'm buying bread",
                             "x_tr": "Ekmek alıyorum"}),
    6296: (LIST + "; " + DULL, {
        "t_ru": "свет", "t_uk": "світло", "t_en": "light", "t_tr": "ışık", "t_pl": "światło", "t_it": "la luce",
        "t_es": "la luz", "t_fr": "la lumière", "t_cs": "světlo",
        **all_x("Mach bitte das Licht an", "Включи, пожалуйста, свет", "Увімкни, будь ласка, світло",
                "Turn on the light, please", "Işığı açar mısın lütfen?", "Włącz, proszę, światło",
                "Accendi la luce, per favore", "Enciende la luz, por favor", "Allume la lumière, s'il te plaît",
                "Rozsviť prosím světlo")}),
    229: (TWO + " («заявлять» — своя строка)", {
        "t_ru": "объяснять, объяснить", "t_uk": "пояснювати, пояснити", "t_en": "to explain",
        "t_tr": "açıklamak, anlatmak", "t_pl": "wyjaśniać, tłumaczyć", "t_it": "spiegare", "t_es": "explicar",
        "t_fr": "expliquer", "t_cs": "vysvětlit"}),
    798: (LIST + "; " + EN, {"t_ru": "ключ", "t_uk": "ключ", "t_es": "la llave", "x_en": "I'm looking for my key"}),
}

SPLIT_LATER = {
    1642: ["laufen = работать (Die Maschine läuft)", "laufen = идти (Was läuft im Kino?)"],
    763: ["richtig = по-настоящему (richtig gut)"],
    229: ["erklären = заявлять"],
}
