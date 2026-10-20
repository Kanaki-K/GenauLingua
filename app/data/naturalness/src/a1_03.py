"""A1, блок 3: слова 81–120 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
TWO = "в строке два разных слова — оставлено главное, второе — отдельной строкой (блок деления)"
EN = "английский пример: так не говорят о том, что происходит сейчас"

FIXES = {
    655: (LIST, {"t_ru": "никогда", "t_uk": "ніколи", "t_en": "never", "t_tr": "asla, hiçbir zaman",
                 "t_pl": "nigdy"}),
    13291: (LIST, {"t_ru": "никакой, не", "t_uk": "жодний, ніякий", "t_en": "no, not any", "t_tr": "hiç",
                   "t_pl": "żaden", "t_es": "ningún", "t_fr": "aucun, pas de", "t_cs": "žádný"}),
    986: (LIST, {"t_ru": "много", "t_uk": "багато", "t_en": "a lot, much", "t_tr": "çok", "t_pl": "dużo, wiele",
                 "t_it": "molto", "t_cs": "hodně, mnoho", "x_ru": "Много дел"}),
    541: (LIST + "; «с удовольствием живём» — калька с gern", {
        "t_ru": "жить", "t_uk": "жити", "t_en": "to live", "t_tr": "yaşamak", "t_pl": "żyć, mieszkać",
        "t_it": "vivere", "t_cs": "žít, bydlet", "x_ru": "Нам нравится жить в этом городе"}),
    205: (TWO + " (einfach — «простой»; «просто» и «в один конец» — свои строки)", {
        "t_ru": "простой, лёгкий", "t_uk": "простий, легкий", "t_en": "easy, simple", "t_tr": "kolay, basit",
        "t_pl": "prosty, łatwy", "t_it": "semplice, facile", "t_es": "sencillo, fácil", "t_fr": "simple, facile",
        "t_cs": "jednoduchý, snadný"}),
    13293: (TWO + " («самый» — am besten, своя строка)", {
        "t_ru": "на, у", "t_uk": "на, біля", "t_en": "at the, on the", "t_tr": "-de, -da", "t_pl": "na, przy"}),
    1071: ("обрывок «времени по часам» и пять значений → «время»; «I have no time» — книжно", {
        "t_ru": "время", "t_uk": "час", "t_en": "time", "t_tr": "zaman, vakit", "t_pl": "czas",
        "t_it": "il tempo", "t_es": "el tiempo", "t_fr": "le temps", "t_cs": "čas", "x_en": "I don't have time"}),
    500: (LIST + "; пример — будущее время, как в русском", {
        "t_ru": "приходить, приезжать", "t_uk": "приходити, приїжджати", "t_en": "to come", "t_tr": "gelmek",
        "t_pl": "przychodzić, przyjeżdżać", "t_it": "venire", "t_es": "venir", "t_fr": "venir",
        "t_cs": "přijít, přijet",
        "x_uk": "Він прийде о третій", "x_en": "He's coming at three", "x_pl": "Przyjdzie o trzeciej"}),
    2093: (LIST + "; «потому что болен» — книжно", {
        "t_ru": "потому что, так как", "t_uk": "бо, тому що", "t_en": "because", "t_tr": "çünkü",
        "t_pl": "bo, ponieważ", "x_ru": "Я остаюсь дома, потому что заболел",
        "x_en": "I'm staying at home because I'm sick"}),
    401: (LIST, {"t_ru": "сегодня", "t_uk": "сьогодні", "t_en": "today", "t_tr": "bugün", "t_pl": "dzisiaj, dziś",
                 "t_cs": "dnes, dneska"}),
    1059: (LIST, {"t_ru": "хотеть, собираться", "t_uk": "хотіти, збиратися", "t_en": "to want", "t_tr": "istemek",
                  "t_pl": "chcieć"}),
    305: (LIST + "; «весь» — прилагательное ganz, своя строка", {
        "t_ru": "совсем, довольно", "t_uk": "цілком, досить", "t_en": "quite, completely",
        "t_tr": "tamamen, oldukça", "t_pl": "całkiem, zupełnie", "t_it": "abbastanza, del tutto",
        "t_es": "bastante, completamente", "t_fr": "assez, tout à fait", "t_cs": "docela, úplně"}),
    1316: (TWO + " («с этим» — наречие damit, своя строка)", {
        "t_ru": "чтобы", "t_uk": "щоб", "t_en": "so that", "t_tr": "diye, için", "t_pl": "żeby, aby",
        "t_it": "affinché, così da", "t_es": "para que", "t_fr": "pour que", "t_cs": "aby"}),
    286: (LIST, {"t_ru": "женщина, жена", "t_uk": "жінка, дружина", "t_en": "woman, wife", "t_tr": "kadın, eş",
                 "t_pl": "kobieta, żona", "t_it": "la donna, la moglie", "t_es": "la mujer, la esposa",
                 "t_fr": "la femme", "t_cs": "žena, manželka"}),
    118: (LIST, {"t_ru": "до", "t_uk": "до", "t_en": "until, by", "t_tr": "-e kadar", "t_pl": "do, aż do",
                 "t_it": "fino a", "t_cs": "do"}),
    663: (LIST + "; «Что мы теперь делаем?» — калька", {
        "t_ru": "теперь, ну", "t_uk": "тепер, ну", "t_en": "now, well", "t_tr": "şimdi", "t_pl": "teraz, no",
        "t_it": "ora, dunque", "t_es": "ahora, pues", "t_fr": "maintenant, alors", "t_cs": "teď, tak",
        "x_ru": "Что нам теперь делать?", "x_uk": "Що нам тепер робити?"}),
    1084: ("«Я вернусь обратно» — тавтология; пример, где слово видно", {
        "t_ru": "назад, обратно", "t_uk": "назад", "t_en": "back", "t_tr": "geri", "t_pl": "z powrotem",
        "t_it": "indietro, di ritorno", "t_es": "de vuelta, atrás", "t_fr": "de retour, en arrière",
        "t_cs": "zpět, zpátky",
        "x_de": "Wir fahren mit dem Bus zurück",
        "x_ru": "Обратно мы поедем на автобусе",
        "x_uk": "Назад ми поїдемо автобусом",
        "x_en": "We're going back by bus",
        "x_tr": "Otobüsle geri döneceğiz",
        "x_pl": "Z powrotem pojedziemy autobusem",
        "x_it": "Torniamo indietro in autobus",
        "x_es": "De vuelta vamos en autobús",
        "x_fr": "Au retour, on prend le bus",
        "x_cs": "Zpátky pojedeme autobusem"}),
    13302: (LIST, {"t_ru": "два, две", "t_uk": "два, дві", "t_pl": "dwa, dwie"}),
    486: (TWO + " («конечно» — Klar!, своя строка)", {
        "t_ru": "ясный, понятный", "t_uk": "ясний, зрозумілий", "t_en": "clear", "t_tr": "açık, net",
        "t_pl": "jasny", "t_it": "chiaro", "t_es": "claro", "t_fr": "clair", "t_cs": "jasný"}),
    550: (LIST + "; «Many people are here» — так не говорят", {
        "t_ru": "люди", "t_uk": "люди", "t_en": "people", "t_tr": "insanlar", "t_pl": "ludzie",
        "t_it": "la gente", "t_es": "la gente", "t_fr": "les gens", "t_cs": "lidé, lidi",
        "x_en": "There are a lot of people here"}),
    971: ("«Vater arbeitet im Büro» — по-немецки так не говорят, нужно «Mein Vater»", {
        "x_de": "Mein Vater arbeitet im Büro",
        "x_ru": "Мой отец работает в офисе",
        "x_uk": "Мій батько працює в офісі",
        "x_en": "My father works in an office",
        "x_tr": "Babam ofiste çalışıyor",
        "x_pl": "Mój tata pracuje w biurze",
        "x_it": "Mio padre lavora in ufficio",
        "x_es": "Mi padre trabaja en una oficina",
        "x_fr": "Mon père travaille dans un bureau",
        "x_cs": "Můj táta pracuje v kanceláři"}),
    1: (TWO + " («прочь» — ab!, своя строка)", {
        "t_ru": "с, начиная с", "t_uk": "з, від", "t_en": "from", "t_tr": "-den itibaren", "t_pl": "od",
        "t_it": "da, a partire da", "t_es": "a partir de, desde", "t_cs": "od",
        "x_en": "From Monday I'm on holiday"}),
    910: (LIST, {"t_ru": "день", "t_uk": "день", "t_pl": "dzień"}),
    328: (TWO + " («прямой, ровно» — прилагательное gerade); «Ich bin gerade hier» — так не говорят", {
        "t_ru": "как раз, сейчас", "t_uk": "саме, якраз", "t_en": "just, right now", "t_tr": "şu anda, tam",
        "t_pl": "właśnie", "t_it": "proprio ora, appena", "t_es": "justo ahora", "t_fr": "en ce moment, juste",
        "t_cs": "právě, zrovna",
        "x_de": "Ich bin gerade beschäftigt",
        "x_ru": "Я сейчас занят",
        "x_uk": "Я зараз зайнятий",
        "x_en": "I'm busy right now",
        "x_tr": "Şu anda meşgulüm",
        "x_pl": "Jestem właśnie zajęty",
        "x_it": "Sono occupato proprio ora",
        "x_es": "Ahora mismo estoy ocupado",
        "x_fr": "Je suis occupé en ce moment",
        "x_cs": "Zrovna jsem zaneprázdněný"}),
    321: ("«I have no money» — книжно", {"x_en": "I don't have any money"}),
    197: (LIST + "; " + EN, {
        "t_ru": "через, сквозь", "t_uk": "через, крізь", "t_en": "through", "t_tr": "içinden, arasından",
        "t_pl": "przez", "t_it": "attraverso, per", "t_es": "por, a través de", "t_fr": "à travers, par",
        "t_cs": "přes, skrz", "x_en": "We're walking through the park", "x_it": "Passiamo per il parco"}),
    620: ("порча знаний: «гайка» — омоним, другое слово (die Mutter, Plural Muttern); "
          "«Mutter ist zu Hause» — по-немецки нужно «Meine Mutter»", {
        "t_ru": "мама, мать", "t_uk": "мама, мати", "t_en": "mother, mom", "t_tr": "anne",
        "t_pl": "mama, matka", "t_it": "la madre, la mamma", "t_es": "la madre, la mamá",
        "t_fr": "la mère, la maman", "t_cs": "matka, máma",
        "x_de": "Meine Mutter ist zu Hause",
        "x_ru": "Моя мама дома",
        "x_uk": "Моя мама вдома",
        "x_en": "My mother is at home",
        "x_tr": "Annem evde",
        "x_pl": "Moja mama jest w domu",
        "x_it": "Mia madre è a casa",
        "x_es": "Mi madre está en casa",
        "x_fr": "Ma mère est à la maison",
        "x_cs": "Moje máma je doma"}),
    1738: ("«если» — это wenn, не ob", {"t_ru": "ли", "x_en": "I don't know whether he's coming"}),
    100: (LIST, {"t_ru": "лучше", "t_uk": "краще", "t_pl": "lepiej, lepszy", "t_it": "meglio", "t_fr": "mieux",
                 "t_cs": "lépe"}),
    1860: (LIST + "; пример — будущее время, как в других языках", {
        "t_ru": "сам", "t_uk": "сам", "t_en": "oneself", "t_tr": "kendim, kendi", "t_pl": "sam",
        "t_it": "da solo, stesso", "t_es": "mismo", "t_fr": "soi-même", "t_cs": "sám",
        "x_ru": "Я сделаю это сам", "x_uk": "Я зроблю це сам", "x_tr": "Bunu kendim yaparım"}),
    395: (LIST + "; «Я могу тебе помочь?» — калька", {
        "t_ru": "помогать, помочь", "t_uk": "допомагати, допомогти", "t_en": "to help", "t_tr": "yardım etmek",
        "t_pl": "pomagać, pomóc", "t_cs": "pomáhat, pomoct",
        "x_ru": "Тебе помочь?", "x_uk": "Тобі допомогти?"}),
    271: (TWO + " («считать» — Ich finde das gut, своя строка)", {
        "t_ru": "находить, найти", "t_uk": "знаходити, знайти", "t_en": "to find", "t_tr": "bulmak",
        "t_pl": "znaleźć", "t_it": "trovare", "t_es": "encontrar", "t_fr": "trouver", "t_cs": "najít"}),
    18564: (LIST, {"t_tr": "uzun süre", "t_es": "mucho tiempo"}),
    1023: (LIST + "; «We go further» — так не говорят", {
        "t_ru": "дальше", "t_uk": "далі", "t_en": "further, on", "t_tr": "ileri, devam", "t_pl": "dalej",
        "t_it": "avanti, oltre", "t_es": "adelante", "t_fr": "plus loin", "t_cs": "dál",
        "x_en": "We're moving on"}),
    189: ("порча знаний: «туда» — это dorthin", {"t_ru": "там", "t_uk": "там", "t_es": "allí, ahí",
                                                "t_fr": "là-bas"}),
    310: (TWO + " («существовать» — es gibt, своя строка)", {
        "t_ru": "давать, дать", "t_uk": "давати, дати", "t_en": "to give", "t_tr": "vermek",
        "t_pl": "dawać, dać", "t_cs": "dávat, dát"}),
}

SPLIT_LATER = {
    205: ["einfach = просто (Mach es einfach!)", "einfache Fahrt = в один конец"],
    13293: ["am + превосходная = самый (am besten)"],
    305: ["ganz = весь, целый (der ganze Tag)"],
    1316: ["damit = с этим (Was willst du damit?)"],
    1: ["ab! = прочь"],
    486: ["Klar! = конечно"],
    328: ["gerade = прямой, ровный"],
    620: ["die Mutter (Muttern) = гайка — B2, своя строка"],
    271: ["finden = считать (Ich finde das gut)"],
    310: ["es gibt = есть, существует"],
}
