"""B1, блок 14: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    15974: ("«Я должен защищать» — калька с muss", {"x_ru": "Мне приходится отстаивать своё мнение",
                                                 "x_uk": "Мені доводиться відстоювати свою думку"}),
    1949: ("«Das ist nur Theorie» — обрывок; в речи — «in der Theorie»", {**all_x(
        "In der Theorie klingt das gut", "В теории это звучит хорошо", "Теоретично це звучить добре",
        "In theory that sounds good", "Teoride kulağa iyi geliyor", "W teorii brzmi to dobrze", "In teoria suona bene",
        "En teoría suena bien", "En théorie, ça a l'air bien", "Teoreticky to zní dobře")}),
    15415: ("в жизни Schlange — прежде всего очередь; змея в траве — из учебника биологии", {
        "t_ru": "очередь, змея", "t_uk": "черга, змія", "t_en": "queue, snake", "t_tr": "kuyruk, yılan",
        "t_pl": "kolejka, wąż", "t_it": "la fila, il serpente", "t_es": "la cola, la serpiente",
        "t_fr": "la file d'attente, le serpent", "t_cs": "fronta, had",
        **all_x("An der Kasse ist eine lange Schlange", "На кассе длинная очередь", "На касі довга черга",
                "There's a long queue at the checkout", "Kasada uzun bir kuyruk var", "Przy kasie jest długa kolejka",
                "Alla cassa c'è una lunga fila", "En la caja hay una cola larga",
                "Il y a une longue file d'attente à la caisse", "U pokladny je dlouhá fronta")}),
    1750: ("«Ich habe Pech gehabt» — пусто; «смола» — другое значение", {
        "t_ru": "невезение, неудача", "t_uk": "невезіння, невдача", "t_en": "bad luck", "t_tr": "şanssızlık",
        "t_pl": "pech", "t_it": "la sfortuna", "t_es": "la mala suerte", "t_fr": "la malchance", "t_cs": "smůla",
        **all_x("So ein Pech!", "Вот невезение!", "Яке невезіння!", "What bad luck!", "Ne şanssızlık!",
                "Co za pech!", "Che sfortuna!", "¡Qué mala suerte!", "Quelle malchance!", "To je smůla!")}),
    2520: ("«Der Geschmack ist gut» — пусто; " + LIST, {
        "t_ru": "вкус", "t_uk": "смак", "t_en": "taste, flavour", "t_tr": "tat, zevk", "t_pl": "smak, gust",
        "t_it": "il sapore, il gusto", "t_es": "el sabor, el gusto", "t_fr": "le goût", "t_cs": "chuť, vkus",
        **all_x("Über Geschmack lässt sich nicht streiten", "О вкусах не спорят", "Про смаки не сперечаються",
                "There's no accounting for taste", "Zevkler tartışılmaz", "O gustach się nie dyskutuje",
                "Sui gusti non si discute", "Sobre gustos no hay nada escrito",
                "Les goûts, ça ne se discute pas", "O chutích se nediskutuje")}),
    1115: ("«Marketingabteilung» прячет слово; шаблон Bereich (Marketing)", {**all_x(
        "In welcher Abteilung arbeitest du?", "В каком отделе ты работаешь?", "У якому відділі ти працюєш?",
        "Which department do you work in?", "Hangi bölümde çalışıyorsun?", "W jakim dziale pracujesz?",
        "In quale reparto lavori?", "¿En qué departamento trabajas?", "Tu travailles dans quel service?",
        "Ve kterém oddělení pracuješ?")}),
    8773: ("перевод — список из пяти; «берёт на себя руководство» — канцелярски", {
        "t_ru": "руководство, линия (связи)", "t_uk": "керівництво, лінія", "t_en": "management, line",
        "t_tr": "yönetim, hat", "t_pl": "kierownictwo, linia", "t_it": "la direzione, la linea",
        "t_es": "la dirección, la línea", "t_fr": "la direction, la ligne", "t_cs": "vedení, linka",
        **all_x("Die Leitung ist besetzt", "Линия занята", "Лінія зайнята", "The line is busy", "Hat meşgul",
                "Linia jest zajęta", "La linea è occupata", "La línea está ocupada", "La ligne est occupée",
                "Linka je obsazená")}),
    6581: ("«Das ist geheim» — пусто", {**all_x(
        "Das bleibt aber geheim, okay?", "Но это останется в секрете, ладно?", "Але це залишиться в секреті, добре?",
        "But that stays secret, okay?", "Ama bu gizli kalacak, tamam mı?", "Ale to ma pozostać tajne, dobrze?",
        "Ma resta segreto, va bene?", "Pero esto queda en secreto, ¿vale?", "Mais ça reste secret, d'accord?",
        "Ale zůstane to tajné, jo?")}),
    6583: ("«Wir haben gegenseitige Gefühle» — так не говорят", {
        "t_it": "reciproco, a vicenda",
        **all_x("Die Nachbarn besuchen sich gegenseitig", "Соседи ходят друг к другу в гости",
                "Сусіди ходять одне до одного в гості", "The neighbours visit each other",
                "Komşular birbirini ziyaret ediyor", "Sąsiedzi nawzajem się odwiedzają",
                "I vicini si fanno visita a vicenda", "Los vecinos se visitan mutuamente",
                "Les voisins se rendent visite mutuellement", "Sousedé se vzájemně navštěvují")}),
    2780: ("«Der Sack ist schwer» — скелет", {**all_x(
        "Ich brauche einen Sack für die Kartoffeln", "Мне нужен мешок для картошки", "Мені потрібен мішок для картоплі",
        "I need a sack for the potatoes", "Patatesler için bir çuvala ihtiyacım var", "Potrzebuję worka na ziemniaki",
        "Mi serve un sacco per le patate", "Necesito un saco para las patatas",
        "J'ai besoin d'un sac pour les pommes de terre", "Potřebuju pytel na brambory")}),
    857: (EN + " («I go for a walk»)", {"x_en": "I'm going for a walk"}),
    13637: ("«Der Stoff ist sehr weich» — шаблон weich («Das Bett ist sehr weich»); " + LIST, {
        "t_ru": "ткань, материал", "t_uk": "тканина, матеріал", "t_en": "fabric, material", "t_tr": "kumaş, konu",
        "t_pl": "materiał, tkanina", "t_it": "il tessuto, la materia", "t_es": "la tela, la materia",
        "t_fr": "le tissu, la matière", "t_cs": "látka, učivo",
        **all_x("Der Lehrer hat zu viel Stoff für eine Stunde", "У учителя слишком много материала на один урок",
                "У вчителя забагато матеріалу на один урок", "The teacher has too much material for one lesson",
                "Öğretmenin bir ders için çok fazla konusu var", "Nauczyciel ma za dużo materiału na jedną lekcję",
                "L'insegnante ha troppa materia per una lezione", "El profesor tiene demasiada materia para una clase",
                "Le prof a trop de matière pour un seul cours", "Učitel má na jednu hodinu moc učiva")}),
}

SPLIT_LATER = {}
