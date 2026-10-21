"""A2, блок 3: слова 81–120 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
TWO = "в строке два разных слова — оставлено главное, второе — отдельной строкой (блок деления)"
EN = "английский пример: так не говорят"
NEAR = "пример повторял пример соседнего слова — у каждого свой"
MARK = "пометки «(colloq.)/(coloq.)/(fam.)/(hovor.)» в переводе"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    6256: (LIST + "; «хочу есть что-то другое» — калька", {
        "t_ru": "другое, что-то другое", "t_uk": "інше, щось інше", "t_en": "something else, other", "t_tr": "başka",
        "t_pl": "inne", "x_ru": "Я хочу съесть что-нибудь другое"}),
    14898: ("в переводе примера ru/uk «подруга», в остальных языках «девушка» — одна строка, один смысл", {
        "x_ru": "Моя девушка сегодня придёт", "x_uk": "Моя дівчина прийде сьогодні"}),
    14899: (LIST + "; " + MARK, {"t_ru": "парень, тип", "t_uk": "хлопець, тип", "t_en": "guy", "t_tr": "adam, tip",
                                 "t_pl": "facet, typ", "t_it": "il tipo, il ragazzo", "t_es": "el tipo, el chico",
                                 "t_fr": "le type, le gars", "t_cs": "chlápek, typ",
                                 "x_fr": "Ce type est très sympa"}),
    1332: (MARK + "; " + NEAR + " (Sache: «Das ist eine … Sache»)", {
        "t_ru": "вещь, штука", "t_uk": "річ, штука", "t_en": "thing", "t_tr": "şey", "t_pl": "rzecz",
        "t_it": "la cosa", "t_fr": "la chose, le truc",
        **all_x("Was ist das für ein Ding?", "Что это за штука?", "Що це за штука?", "What is that thing?",
                "Bu ne biçim bir şey?", "Co to za rzecz?", "Cos'è questa cosa?", "¿Qué es esa cosa?",
                "C'est quoi, ce truc?", "Co je to za věc?")}),
    12465: (NEAR + " (schlagen: «Mein Herz schlägt schnell»)", {
        "t_ru": "сердце", "t_uk": "серце", "t_tr": "kalp, yürek",
        **all_x("Ich danke dir von Herzen", "Благодарю тебя от всего сердца", "Дякую тобі від щирого серця",
                "Thank you from the bottom of my heart", "Sana yürekten teşekkür ederim", "Dziękuję ci z całego serca",
                "Ti ringrazio di cuore", "Te lo agradezco de corazón", "Je te remercie du fond du cœur",
                "Děkuju ti z celého srdce")}),
    268: (LIST + "; «festival» — не то", {"t_ru": "праздник", "t_uk": "свято", "t_en": "party, celebration",
                                         "t_tr": "kutlama, şenlik", "t_pl": "święto, impreza", "t_es": "la fiesta",
                                         "t_cs": "oslava, slavnost", "x_en": "The party was wonderful"}),
    207: (LIST, {"t_ru": "несколько, некоторые", "t_uk": "кілька, деякі", "t_en": "some, a few",
                 "t_tr": "bazı, birkaç", "t_pl": "kilka, niektórzy"}),
    1875: (LIST, {"t_ru": "а", "t_uk": "а", "t_en": "but rather", "t_tr": "aksine", "t_pl": "lecz, tylko"}),
    2603: (LIST + "; «Я едва могу дождаться» — калька, по-русски «жду не дождусь»", {
        "t_ru": "едва, почти не", "t_uk": "ледве, майже не", "t_en": "hardly, barely", "t_tr": "neredeyse hiç",
        "t_pl": "ledwie, prawie nie", "x_ru": "Жду не дождусь", "x_uk": "Не можу дочекатися"}),
    1865: (LIST, {"t_ru": "ставить, сажать", "t_uk": "ставити, садити", "t_en": "to put, to seat",
                  "t_tr": "koymak, oturtmak", "t_pl": "stawiać, sadzać", "t_it": "mettere, posare",
                  "t_es": "poner, sentar", "t_fr": "mettre, poser", "t_cs": "posadit, dát"}),
    1788: (LIST, {"t_ru": "речь, выступление", "t_uk": "промова, виступ", "t_en": "speech", "t_tr": "konuşma",
                  "t_pl": "przemówienie, mowa"}),
    1196: (LIST, {"t_ru": "кроме", "t_uk": "крім", "t_en": "except, apart from", "t_tr": "hariç",
                  "t_pl": "oprócz, poza"}),
    1081: (LIST, {"t_ru": "сначала, сперва", "t_uk": "спочатку", "t_en": "first, at first", "t_tr": "önce",
                  "t_pl": "najpierw"}),
    294: (NEAR + " (aufstehen, acht: «Ich stehe … auf»)", {**all_x(
        "Morgen muss ich früh los", "Завтра мне рано выходить", "Завтра мені рано виходити",
        "I have to leave early tomorrow", "Yarın erken çıkmam lazım", "Jutro muszę wcześnie wyjść",
        "Domani devo uscire presto", "Mañana tengo que salir temprano", "Demain, je dois partir tôt",
        "Zítra musím brzy vyrazit")}),
    2994: (NEAR + " (wohl: «Das ist wohl richtig»)", {
        "t_ru": "вероятно, наверное", "t_uk": "ймовірно, мабуть", "t_en": "probably", "t_tr": "muhtemelen",
        "t_pl": "prawdopodobnie",
        **all_x("Er kommt wahrscheinlich später", "Он, наверное, придёт позже", "Він, мабуть, прийде пізніше",
                "He'll probably come later", "Muhtemelen daha sonra gelir", "Prawdopodobnie przyjdzie później",
                "Probabilmente arriva più tardi", "Probablemente venga más tarde", "Il viendra probablement plus tard",
                "Pravděpodobně přijde později")}),
    1685: (LIST, {"t_ru": "количество, множество", "t_uk": "кількість, безліч", "t_en": "amount, crowd",
                  "t_tr": "miktar, kalabalık", "t_pl": "ilość, tłum", "t_it": "la quantità, la folla",
                  "t_es": "la cantidad, la multitud", "t_fr": "la quantité, la foule", "t_cs": "množství, dav"}),
    18590: (NEAR + " (schon: «Ich bin schon fertig»)", {
        "t_ru": "уже", "t_uk": "вже",
        **all_x("Der Film hat bereits angefangen", "Фильм уже начался", "Фільм уже почався",
                "The film has already started", "Film çoktan başladı", "Film już się zaczął",
                "Il film è già cominciato", "La película ya ha empezado", "Le film a déjà commencé", "Film už začal")}),
    1819: (TWO + " («создавать» — сильное schaffen, своя строка)", {
        "t_ru": "справиться, успеть", "t_uk": "впоратися, встигнути", "t_en": "to manage, to make it",
        "t_tr": "başarmak", "t_pl": "poradzić sobie, zdążyć", "t_it": "farcela", "t_es": "lograr, conseguir",
        "t_fr": "y arriver, réussir", "t_cs": "zvládnout, stihnout"}),
    148: (NEAR + " (Vater: «… arbeitet im Büro»)", {
        "t_ru": "офис", "t_uk": "офіс", "t_tr": "ofis",
        **all_x("Ich bin heute bis sechs im Büro", "Сегодня я до шести в офисе", "Сьогодні я до шостої в офісі",
                "I'm at the office until six today", "Bugün altıya kadar ofisteyim", "Dziś jestem w biurze do szóstej",
                "Oggi sono in ufficio fino alle sei", "Hoy estoy en la oficina hasta las seis",
                "Aujourd'hui, je suis au bureau jusqu'à six heures", "Dnes jsem v kanceláři do šesti")}),
    990: (LIST, {"t_ru": "полный", "t_uk": "повний", "t_en": "full", "t_tr": "dolu", "t_pl": "pełny"}),
    1972: (LIST, {"t_ru": "всё равно, тем не менее", "t_uk": "все одно, проте", "t_en": "anyway, still",
                  "t_tr": "yine de", "t_pl": "mimo to"}),
    1725: (LIST, {"t_ru": "называть", "t_uk": "називати", "t_en": "to call, to name", "t_tr": "adlandırmak, demek",
                  "t_pl": "nazywać", "t_it": "chiamare", "t_es": "llamar", "t_fr": "appeler", "t_cs": "nazývat"}),
    2665: ("«Die Luft ist frisch» — пример ни о чём", {**all_x(
        "Mach mal das Fenster auf, ich brauche frische Luft", "Открой окно, мне нужен свежий воздух",
        "Відчини вікно, мені потрібне свіже повітря", "Open the window, I need some fresh air",
        "Pencereyi aç, temiz havaya ihtiyacım var", "Otwórz okno, potrzebuję świeżego powietrza",
        "Apri la finestra, ho bisogno di aria fresca", "Abre la ventana, necesito aire fresco",
        "Ouvre la fenêtre, j'ai besoin d'air frais", "Otevři okno, potřebuju čerstvý vzduch")}),
    186: (LIST, {"t_ru": "прямо, сразу", "t_uk": "прямо, одразу", "t_en": "directly, straight", "t_tr": "doğrudan",
                 "t_pl": "bezpośrednio, prosto", "t_it": "direttamente", "t_es": "directamente", "t_fr": "directement",
                 "t_cs": "přímo, rovnou"}),
    162: (LIST + "; " + EN, {"t_ru": "потом, после этого", "t_uk": "потім, після цього", "t_en": "after that, afterwards",
                             "t_tr": "sonra", "t_pl": "potem", "x_uk": "Потім ми підемо додому",
                             "x_en": "After that we're going home"}),
    6284: (NEAR + " (absolut, genau: «Das ist … richtig»)", {
        "t_ru": "совершенно, полностью", "t_uk": "цілком, повністю", "t_en": "completely, totally", "t_tr": "tamamen",
        "t_pl": "całkowicie, zupełnie",
        **all_x("Das habe ich völlig vergessen", "Я совершенно об этом забыл", "Я зовсім про це забув",
                "I completely forgot about it", "Bunu tamamen unuttum", "Zupełnie o tym zapomniałem",
                "Me ne sono completamente dimenticato", "Se me ha olvidado por completo", "J'ai complètement oublié",
                "Úplně jsem na to zapomněl")}),
    6285: (TWO + " («переезжать» — umziehen, своя строка)", {
        "t_ru": "тянуть, тащить", "t_uk": "тягнути", "t_en": "to pull", "t_tr": "çekmek", "t_pl": "ciągnąć",
        "t_it": "tirare", "t_es": "tirar", "t_fr": "tirer", "t_cs": "táhnout"}),
    2041: (LIST, {"t_ru": "терять, проигрывать", "t_uk": "губити, програвати", "t_en": "to lose", "t_tr": "kaybetmek",
                  "t_pl": "gubić, tracić"}),
    3015: (LIST, {"t_ru": "ценность, стоимость", "t_uk": "цінність, вартість", "t_en": "value", "t_tr": "değer",
                  "t_pl": "wartość"}),
    13379: (LIST, {"t_ru": "хотя, правда", "t_uk": "хоча, щоправда", "t_en": "admittedly", "t_tr": "gerçi",
                   "t_pl": "wprawdzie", "t_it": "certo", "t_es": "es cierto que", "t_fr": "certes", "t_cs": "sice"}),
    13836: (LIST + "; " + NEAR + " (Polizei: «Sie ruft die Polizei an»)", {
        "t_ru": "звать, вызывать", "t_uk": "кликати, викликати", "t_en": "to call, to shout",
        "t_tr": "çağırmak, seslenmek", "t_pl": "wołać, wzywać", "t_it": "chiamare", "t_es": "llamar",
        "t_fr": "appeler", "t_cs": "volat",
        **all_x("Mama ruft, wir müssen nach Hause", "Мама зовёт, нам пора домой", "Мама кличе, нам пора додому",
                "Mum's calling, we have to go home", "Annem çağırıyor, eve gitmemiz lazım", "Mama woła, musimy iść do domu",
                "La mamma chiama, dobbiamo andare a casa", "Mamá nos llama, tenemos que ir a casa",
                "Maman nous appelle, on doit rentrer", "Máma volá, musíme domů")}),
}

SPLIT_LATER = {
    1819: ["schaffen (schuf, geschaffen) = создавать"],
    6285: ["ziehen = переезжать (nach Berlin ziehen)"],
}
