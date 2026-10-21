"""B1, блок 21: следующие 40 по частоте. Вычитано вручную 21.10."""

EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    958: ("«Sie ist unglücklich» — пусто", {**all_x(
        "Das war ein unglücklicher Zufall", "Это было неудачное совпадение", "Це був невдалий збіг",
        "That was an unfortunate coincidence", "Talihsiz bir tesadüftü", "To był niefortunny zbieg okoliczności",
        "È stata una sfortunata coincidenza", "Fue una desafortunada coincidencia", "C'était une malheureuse coïncidence",
        "Byla to nešťastná náhoda")}),
    15432: ("«Wir fanden eine große Höhle» — претерит, приключенческий роман", {**all_x(
        "Im Urlaub haben wir eine Höhle besichtigt", "В отпуске мы ходили смотреть пещеру",
        "У відпустці ми ходили дивитися печеру", "On holiday we visited a cave", "Tatilde bir mağarayı gezdik",
        "Na urlopie zwiedzaliśmy jaskinię", "In vacanza abbiamo visitato una grotta", "En vacaciones visitamos una cueva",
        "En vacances, on a visité une grotte", "Na dovolené jsme navštívili jeskyni")}),
    1313: ("«Ich bin daheim» — шаблон zu Hause", {**all_x(
        "Bei uns daheim isst man viel Fleisch", "У нас дома едят много мяса", "У нас удома їдять багато м'яса",
        "At home we eat a lot of meat", "Bizim evde çok et yenir", "U nas w domu je się dużo mięsa",
        "A casa nostra si mangia molta carne", "En mi casa se come mucha carne", "Chez nous, on mange beaucoup de viande",
        "U nás doma se jí hodně masa")}),
    14404: ("«… hält jeden Sonntag eine Messe» — шаблон Priester, Pater", {**all_x(
        "Der Pfarrer hat uns getraut", "Священник нас обвенчал", "Священик нас обвінчав", "The vicar married us",
        "Papaz bizi evlendirdi", "Ksiądz udzielił nam ślubu", "Il parroco ci ha sposati", "El párroco nos casó",
        "C'est le curé qui nous a mariés", "Farář nás oddal")}),
    2042: ("«Vermeide Fehler» — команда из учебника", {**all_x(
        "Ich versuche, Zucker zu vermeiden", "Я стараюсь избегать сахара", "Я намагаюся уникати цукру",
        "I try to avoid sugar", "Şekerden kaçınmaya çalışıyorum", "Staram się unikać cukru", "Cerco di evitare lo zucchero",
        "Intento evitar el azúcar", "J'essaie d'éviter le sucre", "Snažím se vyhýbat cukru")}),
    6680: (EN + " («could rescue all people»)", {"x_en": "The fire brigade managed to rescue everyone"}),
    9452: ("«Meine Lehrerin ist sehr nett» — шаблон streng («Unsere Lehrerin ist sehr streng»)", {**all_x(
        "Die Lehrerin hat uns viele Hausaufgaben gegeben", "Учительница задала нам много домашнего задания",
        "Учителька задала нам багато домашнього завдання", "The teacher gave us lots of homework",
        "Öğretmen bize çok ödev verdi", "Nauczycielka zadała nam dużo pracy domowej",
        "La maestra ci ha dato tanti compiti", "La profesora nos ha puesto muchos deberes",
        "La maîtresse nous a donné beaucoup de devoirs", "Učitelka nám dala hodně úkolů")}),
    14978: ("«Der Graf wohnt in einem großen Schloss» — шаблон Palast, Prinz", {**all_x(
        "Graf Dracula ist eine berühmte Figur", "Граф Дракула — известный персонаж", "Граф Дракула — відомий персонаж",
        "Count Dracula is a famous character", "Kont Drakula ünlü bir karakter", "Hrabia Drakula to słynna postać",
        "Il conte Dracula è un personaggio famoso", "El conde Drácula es un personaje famoso",
        "Le comte Dracula est un personnage célèbre", "Hrabě Drákula je slavná postava")}),
    15433: ("«Im Zoo haben wir einen großen Bären gesehen» — шаблон Tiger", {**all_x(
        "Pass auf, hier gibt es Bären!", "Осторожно, здесь водятся медведи!", "Обережно, тут водяться ведмеді!",
        "Careful, there are bears around here!", "Dikkat, burada ayılar var!", "Uważaj, tu są niedźwiedzie!",
        "Attento, qui ci sono gli orsi!", "¡Cuidado, aquí hay osos!", "Attention, il y a des ours ici!",
        "Pozor, tady jsou medvědi!")}),
    6684: (EN + " («I want to own a car»)", {"x_en": "One day I'd like to own a car"}),
    16013: ("«Mein Bruder arbeitet im Militär» — шаблон Armee, Soldat", {**all_x(
        "Nach dem Hochwasser hilft das Militär", "После наводнения помогают военные", "Після повені допомагають військові",
        "The military is helping after the flood", "Selden sonra ordu yardım ediyor", "Po powodzi pomaga wojsko",
        "Dopo l'alluvione aiutano i militari", "Tras la inundación ayuda el ejército", "Après l'inondation, l'armée aide",
        "Po povodni pomáhá armáda")}),
    6686: ("«Häng deinen Mantel an den Haken!» — шаблон hängen; живое значение — «подвох»", {**all_x(
        "Das Angebot ist zu gut, wo ist der Haken?", "Слишком хорошее предложение, в чём подвох?",
        "Занадто гарна пропозиція, де підступ?", "The offer's too good — what's the catch?",
        "Teklif çok iyi, işin pürüzü nerede?", "Oferta jest za dobra, gdzie jest haczyk?",
        "L'offerta è troppo bella, dov'è l'inghippo?", "La oferta es demasiado buena, ¿dónde está la pega?",
        "L'offre est trop belle, où est le hic?", "Ta nabídka je moc dobrá, kde je háček?")}),
    8789: ("«Wir stellen neue Mitarbeiter ein» — шаблон Mitarbeiter", {**all_x(
        "Kannst du mir den Wecker auf sieben einstellen?", "Можешь настроить мне будильник на семь?",
        "Можеш налаштувати мені будильник на сьому?", "Can you set my alarm for seven?", "Alarmımı yediye ayarlar mısın?",
        "Możesz mi nastawić budzik na siódmą?", "Mi imposti la sveglia alle sette?",
        "¿Me ajustas el despertador para las siete?", "Tu peux régler mon réveil sur sept heures?",
        "Můžeš mi nastavit budík na sedm?")}),
    12522: ("«Mein Opa ist fast taub» — шаблон blind («Mein Opa ist blind»)", {**all_x(
        "Mir sind die Finger vor Kälte ganz taub", "У меня пальцы онемели от холода", "У мене пальці затерпли від холоду",
        "My fingers have gone numb with cold", "Soğuktan parmaklarım uyuştu", "Zdrętwiały mi palce z zimna",
        "Ho le dita intorpidite dal freddo", "Tengo los dedos entumecidos de frío", "J'ai les doigts engourdis par le froid",
        "Prsty mám od zimy úplně necitlivé")}),
    6687: ("«Er ist scheinbar nicht zu Hause» — шаблон anscheinend, offenbar; и смысл scheinbar — «мнимо»", {**all_x(
        "Die Aufgabe ist nur scheinbar leicht", "Задание только на первый взгляд лёгкое",
        "Завдання лише на перший погляд легке", "The task only looks easy on the face of it",
        "Görev sadece görünürde kolay", "Zadanie jest tylko pozornie łatwe", "Il compito è solo apparentemente facile",
        "La tarea es solo aparentemente fácil", "L'exercice n'est facile qu'en apparence", "Úkol je jen zdánlivě snadný")}),
}

SPLIT_LATER = {}
