"""A1, блок 2: слова 41–80 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
TWO = "в строке два разных слова — оставлено главное, второе — отдельной строкой (блок деления)"
EN = "английский пример: так не говорят о том, что делаешь сейчас / собираешься сделать"
GLOSS = "пояснение в скобках и пометки — не перевод"

FIXES = {
    450: (LIST, {"t_en": "now", "t_tr": "şimdi", "t_pl": "teraz", "t_cs": "teď"}),
    13262: (LIST, {"t_ru": "-ка, разок", "t_uk": "-но, разок", "t_en": "just, once", "t_tr": "bir, hele",
                   "t_pl": "no, raz", "t_it": "un attimo", "t_es": "un momento", "t_fr": "un peu",
                   "t_cs": "na chvilku"}),
    56: (TWO + " (aus — «из»; «выключено, кончилось» — своя строка)", {
        "t_ru": "из", "t_uk": "з, із", "t_en": "from, out of", "t_tr": "-den, -dan", "t_pl": "z, ze",
        "t_it": "da, di", "t_es": "de", "t_fr": "de, hors de", "t_cs": "z, ze"}),
    165: (LIST, {"t_ru": "тогда, потом", "t_uk": "тоді, потім", "t_en": "then", "t_tr": "sonra, o zaman",
                 "t_pl": "wtedy, potem", "t_it": "allora, poi", "t_es": "entonces, luego", "t_fr": "alors, puis",
                 "t_cs": "pak, potom"}),
    951: (TWO + " (um — «в, вокруг»; um … zu «чтобы» — своя строка)", {
        "t_ru": "в, вокруг", "t_uk": "о, навколо", "t_en": "at, around", "t_tr": "saat, etrafında",
        "t_pl": "o, wokół", "t_it": "a, intorno a", "t_es": "a, alrededor de", "t_fr": "à, autour de",
        "t_cs": "v, kolem", "x_en": "The course starts at nine"}),
    13265: (LIST, {"t_ru": "в", "t_uk": "в, у", "t_en": "in the", "t_tr": "-de, -da", "t_pl": "w",
                   "t_it": "in, nel", "t_es": "en el", "t_fr": "dans le, au", "t_cs": "v, ve"}),
    13267: (LIST, {"t_en": "my", "t_tr": "benim", "t_es": "mi"}),
    187: (LIST + "; «да нет же» — ответ «Doch!», другое употребление", {
        "t_ru": "же, всё-таки", "t_uk": "ж, все ж таки", "t_en": "after all", "t_tr": "yine de",
        "t_pl": "przecież, jednak", "t_it": "eppure, mica", "t_es": "sin embargo, pues",
        "t_fr": "quand même", "t_cs": "přece, vždyť"}),
    669: (TWO + " («не так ли» — «…, oder?», своя строка)", {
        "t_ru": "или, либо", "t_uk": "або, чи", "t_en": "or", "t_tr": "veya, ya da", "t_pl": "albo, lub",
        "t_cs": "nebo"}),
    631: (LIST + "; «согласно» — B1-употребление (meiner Meinung nach)", {
        "t_ru": "после, в", "t_uk": "після, до", "t_en": "after, to", "t_tr": "sonra, -e", "t_pl": "po, do",
        "t_it": "dopo, a", "t_es": "después de, a", "t_fr": "après, à", "t_cs": "po, do",
        "x_en": "After the meal we're going out"}),
    654: (LIST + "; «I want nothing» — так не говорят", {
        "t_ru": "ничего", "t_uk": "нічого", "t_en": "nothing", "t_tr": "hiçbir şey", "t_pl": "nic",
        "t_it": "niente", "t_cs": "nic", "x_en": "I don't want anything"}),
    567: (GLOSS, {"t_ru": "люди, можно", "t_uk": "люди, можна", "t_en": "one, you", "t_tr": "insan, kişi",
                  "t_pl": "się, człowiek", "t_cs": "se, člověk"}),
    1028: (LIST + "; «will» — будущее время, функция, не значение", {
        "t_ru": "становиться, стать", "t_uk": "ставати, стати", "t_en": "to become, to get", "t_tr": "olmak",
        "t_pl": "zostać, stawać się", "t_es": "volverse, hacerse", "t_cs": "stát se",
        "x_en": "I'm going to be a father soon"}),
    1047: ("порча знаний: «куда» — это wohin, другое слово", {"t_ru": "где", "t_tr": "nerede"}),
    239: (LIST, {"t_ru": "что-то, немного", "t_uk": "щось, трохи", "t_en": "something, a little"}),
    580: (LIST + "; «уже не» — это nicht mehr", {
        "t_ru": "больше", "t_uk": "більше", "t_en": "more", "t_tr": "daha fazla", "t_pl": "więcej",
        "t_it": "più", "t_es": "más", "t_fr": "plus", "t_cs": "více", "x_en": "I'd like more water"}),
    87: (LIST + "; Freundin здесь — подруга, не «girlfriend»", {
        "t_ru": "у, при", "t_uk": "у, біля", "t_en": "at, with", "t_tr": "yanında", "t_pl": "u, przy",
        "t_it": "da, presso", "t_es": "en casa de, con", "t_fr": "chez, près de", "t_cs": "u, při",
        "x_en": "I'm at my friend's place"}),
    14: (LIST, {"t_ru": "значит, итак", "t_uk": "отже", "t_en": "so, well", "t_tr": "yani, peki",
                "t_pl": "więc, czyli", "t_it": "allora, quindi", "t_es": "entonces, o sea", "t_fr": "alors, donc",
                "t_cs": "takže, tedy"}),
    121: ("по-русски «пожалуйста» покрывает и «прошу», и «не за что», и «вот, держите» — одно слово", {
        "t_ru": "пожалуйста", "t_uk": "будь ласка, прошу", "t_en": "please, you're welcome",
        "t_tr": "lütfen, rica ederim", "t_pl": "proszę", "t_fr": "s'il te plaît, s'il vous plaît",
        "t_cs": "prosím"}),
    429: (LIST + "; uk «з ранку» — неверная форма, правильно «зранку»", {
        "t_ru": "всегда, постоянно", "t_uk": "завжди, постійно", "t_en": "always", "t_tr": "her zaman, hep",
        "t_pl": "zawsze, ciągle", "t_cs": "vždy, vždycky", "x_uk": "Я завжди п'ю каву зранку"}),
    1006: (LIST, {"t_tr": "neden, niye", "t_pl": "dlaczego, czemu"}),
    992: (LIST + "; «от» — не перевод vor", {
        "t_ru": "перед, назад", "t_uk": "перед, тому", "t_en": "in front of, ago", "t_tr": "önünde, önce",
        "t_it": "davanti a, fa", "t_es": "delante de, hace", "t_fr": "devant, il y a",
        "x_en": "He's waiting in front of the house"}),
    1036: (LIST + "; «I come again» — так не говорят", {
        "t_ru": "снова, опять", "t_uk": "знову", "t_en": "again", "t_tr": "tekrar, yine", "t_pl": "znowu",
        "t_it": "di nuovo", "t_es": "otra vez", "t_fr": "de nouveau, encore", "t_cs": "znovu, zase",
        "x_ru": "Я снова приду", "x_uk": "Я прийду знову", "x_en": "I'll come again",
        "x_tr": "Tekrar geleceğim"}),
    527: (LIST, {"t_ru": "мочь, уметь", "t_uk": "могти, уміти", "t_en": "can, to be able to",
                 "t_tr": "yapabilmek", "t_pl": "móc, umieć", "t_cs": "moct, umět"}),
    571: ("uk «муж» — устаревшее, по-украински «чоловік» и есть муж", {
        "t_uk": "чоловік", "t_tr": "adam, koca"}),
    1123: (TWO + " («закончиться» — Die Milch ist alle, своя строка)", {
        "t_ru": "все", "t_uk": "усі, всі", "t_en": "everyone, all", "t_tr": "herkes, hepsi",
        "t_pl": "wszyscy", "t_it": "tutti", "t_es": "todos", "t_fr": "tous", "t_cs": "všichni"}),
    564: (LIST + "; «Я это делаю / I do that» — калька, говорят «Я это сделаю»", {
        "t_ru": "делать, сделать", "x_ru": "Я это сделаю", "x_uk": "Я це зроблю", "x_en": "I'll do it",
        "x_tr": "Bunu ben yaparım", "x_pl": "Zrobię to", "x_fr": "Je le fais"}),
    173: (LIST + "; " + EN, {
        "t_ru": "потому что, ведь", "t_uk": "бо, тому що", "t_en": "because", "t_tr": "çünkü",
        "t_pl": "bo, ponieważ", "t_it": "perché", "t_es": "porque, pues", "t_fr": "car", "t_cs": "protože",
        "x_en": "I'm staying at home because it's raining"}),
    13282: (LIST + "; " + EN, {
        "t_ru": "к, на", "t_uk": "до, на", "t_en": "to the", "t_tr": "-e, -a", "t_pl": "do, na",
        "t_it": "al, dal", "t_es": "al", "t_fr": "au, chez le", "t_cs": "k, do",
        "x_en": "I'm going to the doctor"}),
    946: (EN, {"x_en": "What are we doing here?"}),
    825: (LIST + "; «смотреть» — это schauen, другое слово", {
        "t_ru": "видеть, увидеть", "t_uk": "бачити, побачити", "t_en": "to see", "t_tr": "görmek",
        "t_pl": "widzieć, zobaczyć", "t_it": "vedere", "t_es": "ver", "t_fr": "voir", "t_cs": "vidět"}),
    319: (LIST + "; " + EN, {
        "t_ru": "идти, ходить", "t_uk": "йти, ходити", "t_en": "to go, to walk", "t_tr": "gitmek",
        "t_pl": "iść, chodzić", "t_it": "andare", "t_es": "ir", "t_fr": "aller", "t_cs": "jít, chodit",
        "x_en": "I'm going for a walk"}),
    1027: (LIST + "; «тот» — не перевод wer", {"t_ru": "кто", "t_uk": "хто", "t_en": "who", "t_tr": "kim"}),
    987: (LIST, {"t_ru": "может быть, возможно", "t_en": "maybe, perhaps", "t_es": "quizás, tal vez",
                 "x_en": "Maybe we'll come tomorrow"}),
    1091: ("семь значений в строке → главные два; " + EN, {
        "t_ru": "о, над", "t_uk": "про, над", "t_en": "about, over", "t_tr": "hakkında, üstünde",
        "t_pl": "o, nad", "t_it": "su, sopra", "t_es": "sobre, de", "t_fr": "sur, au-dessus de",
        "t_cs": "o, nad", "x_en": "We're talking about the problem"}),
    1046: (LIST + "; «You must know that» — это не «Das musst du doch wissen»", {
        "t_ru": "знать", "t_uk": "знати", "t_en": "to know", "t_tr": "bilmek", "t_pl": "wiedzieć",
        "x_en": "Surely you know that"}),
    629: ("пять вариантов, «быть должным» — канцелярски; «I must work» — так не говорят", {
        "t_ru": "должен, надо", "t_uk": "мусити, треба", "t_en": "must, to have to", "t_tr": "zorunda olmak",
        "t_pl": "musieć", "t_es": "tener que, deber", "t_fr": "devoir", "x_en": "I have to work"}),
}

SPLIT_LATER = {
    56: ["aus = выключено, кончилось (Das Licht ist aus; Die Schule ist aus)"],
    951: ["um … zu = чтобы (Ich lerne, um zu arbeiten)"],
    669: ["…, oder? = не так ли"],
    1123: ["alle sein = закончиться (Die Milch ist alle)"],
    187: ["Doch! = да нет же (ответ на отрицание)"],
}
