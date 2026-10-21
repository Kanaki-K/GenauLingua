"""B1, блок 13: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    11650: (EN + " («We drink champagne on the birthday»)", {**all_x(
        "Lass uns mit Champagner anstoßen!", "Давай чокнемся шампанским!", "Давай цокнемося шампанським!",
        "Let's toast with champagne!", "Şampanyayla kadeh kaldıralım!", "Wznieśmy toast szampanem!",
        "Brindiamo con lo champagne!", "¡Brindemos con champán!", "Trinquons au champagne!",
        "Připijme si šampaňským!")}),
    2926: ("«Das ist Unrecht» — пусто; в речи — «Da hast du Unrecht»", {
        "t_es": "la injusticia, no tener razón",
        **all_x("Da hast du Unrecht", "Тут ты неправ", "Тут ти неправий", "You're wrong there", "Bu konuda haksızsın",
                "Tu nie masz racji", "Qui hai torto", "En eso no tienes razón", "Là, tu as tort", "V tom se mýlíš")}),
    1968: ("«Trenn den Müll» — команда; " + LIST, {
        "t_ru": "разделять, расставаться", "t_uk": "розділяти, розходитися", "t_en": "to separate, to split up",
        "t_tr": "ayırmak, ayrılmak", "t_pl": "oddzielać, rozstawać się", "t_it": "separare, differenziare",
        "t_es": "separar, separarse", "t_fr": "trier, se séparer", "t_cs": "třídit, rozejít se",
        **all_x("Bei uns wird der Müll getrennt", "У нас мусор сортируют", "У нас сміття сортують",
                "We separate our rubbish", "Bizde çöpler ayrıştırılıyor", "U nas segreguje się śmieci",
                "Da noi si differenzia la spazzatura", "Aquí separamos la basura", "Chez nous, on trie les déchets",
                "U nás se třídí odpad")}),
    15972: ("«Der Dieb hat meine Tasche gestohlen» — шаблон stehlen", {**all_x(
        "Haltet den Dieb!", "Держите вора!", "Тримайте злодія!", "Stop, thief!", "Hırsızı yakalayın!",
        "Łapać złodzieja!", "Al ladro!", "¡Al ladrón!", "Au voleur!", "Chyťte zloděje!")}),
    2860: (LIST, {"t_ru": "электричество, ток", "t_uk": "електрика, струм", "t_en": "electricity, current",
                  "t_tr": "elektrik, akım", "t_pl": "prąd", "t_it": "la corrente, l'elettricità",
                  "t_es": "la electricidad, la luz", "t_fr": "le courant, l'électricité", "t_cs": "proud, elektřina"}),
    969: (EN + " («goes to the examination»)", {"x_en": "She's going for a check-up"}),
    1789: ("«Das ist die Regel» — пусто; в речи — «in der Regel»", {**all_x(
        "In der Regel komme ich um sechs nach Hause", "Как правило, я прихожу домой в шесть",
        "Як правило, я приходжу додому о шостій", "As a rule, I get home at six", "Kural olarak eve altıda gelirim",
        "Z reguły wracam do domu o szóstej", "Di regola torno a casa alle sei", "Por regla general llego a casa a las seis",
        "En règle générale, je rentre à six heures", "Zpravidla chodím domů v šest")}),
    2433: ("«Ich erlebe viele Abenteuer» — неживо", {**all_x(
        "Im Urlaub haben wir viel erlebt", "В отпуске мы многое повидали", "У відпустці ми багато чого побачили",
        "We experienced a lot on holiday", "Tatilde çok şey yaşadık", "Na urlopie dużo przeżyliśmy",
        "In vacanza abbiamo vissuto tante cose", "En las vacaciones vivimos muchas cosas",
        "En vacances, on a vécu plein de choses", "Na dovolené jsme toho hodně zažili")}),
    15412: ("«Im Wald lebt ein Wolf» — сказка", {**all_x(
        "In der Gegend gibt es wieder Wölfe", "В этих местах снова появились волки", "У цих краях знову з'явилися вовки",
        "There are wolves in the area again", "Bölgede yine kurtlar var", "W okolicy znowu są wilki",
        "Nella zona ci sono di nuovo i lupi", "En la zona vuelve a haber lobos",
        "Il y a de nouveau des loups dans la région", "V okolí jsou zase vlci")}),
    1887: ("«Der Spiegel hängt an der Wand» — шаблон Wand, hängen", {**all_x(
        "Schau mal in den Spiegel!", "Посмотри в зеркало!", "Подивись у дзеркало!", "Look in the mirror!",
        "Aynaya bak!", "Popatrz w lustro!", "Guardati allo specchio!", "¡Mírate al espejo!",
        "Regarde-toi dans le miroir!", "Podívej se do zrcadla!")}),
    6568: ("«Das Konzert war echt spitze» — двадцатый пример «Das Konzert war …»", {**all_x(
        "Du bist echt spitze!", "Ты просто супер!", "Ти просто супер!", "You're absolutely great!", "Sen harikasın!",
        "Jesteś super!", "Sei fantastico!", "¡Eres genial!", "Tu es génial!", "Jsi fakt skvělý!")}),
    2864: ("«Es gibt einen Sturm» — пусто", {**all_x(
        "Bei dem Sturm sind viele Bäume umgefallen", "Во время бури упало много деревьев", "Під час бурі впало багато дерев",
        "Lots of trees came down in the storm", "Fırtınada birçok ağaç devrildi",
        "W czasie burzy przewróciło się dużo drzew", "Con la tempesta sono caduti molti alberi",
        "Con la tormenta se cayeron muchos árboles", "Beaucoup d'arbres sont tombés pendant la tempête",
        "Při bouři spadlo hodně stromů")}),
    2192: (EN + " («Instead of studying, I play video games»)", {
        "x_en": "Instead of studying, I'd rather play video games"}),
    12112: ("«Ich will mit dir wetten» — неживо, шаблон Wette", {**all_x(
        "Ich wette, er kommt wieder zu spät", "Спорим, он опять опоздает", "Закладаюся, він знову запізниться",
        "I bet he'll be late again", "Bahse girerim yine geç kalacak", "Założę się, że znowu się spóźni",
        "Scommetto che arriva di nuovo in ritardo", "Apuesto a que vuelve a llegar tarde",
        "Je parie qu'il va encore être en retard", "Vsadím se, že zase přijde pozdě")}),
    1185: ("«Das Essen war ausgezeichnet» — шаблон prima («Das Essen war prima!»)", {**all_x(
        "Das Hotel hat ausgezeichnete Bewertungen", "У отеля отличные отзывы", "У готелю чудові відгуки",
        "The hotel has excellent reviews", "Otelin yorumları mükemmel", "Hotel ma doskonałe opinie",
        "L'hotel ha recensioni ottime", "El hotel tiene valoraciones excelentes", "L'hôtel a d'excellents avis",
        "Hotel má vynikající hodnocení")}),
    12499: ("ru «На крайний случай — звони мне» — тире лишнее", {
        "x_ru": "На крайний случай звони мне", "x_uk": "На крайній випадок дзвони мені"}),
}

SPLIT_LATER = {}
