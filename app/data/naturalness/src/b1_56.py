"""B1, блок 56: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    17796: ("в речи Pension — прежде всего «пансион» (пенсия — Rente)", {
        "t_ru": "пансион, пенсия", "t_uk": "пансіон, пенсія", "t_en": "guesthouse, pension", "t_tr": "pansiyon, emekli maaşı",
        "t_pl": "pensjonat, emerytura", "t_fr": "la pension, la retraite", "t_cs": "penzion, penze",
        **all_x("Wir übernachten in einer kleinen Pension", "Мы ночуем в небольшом пансионе", "Ми ночуємо в невеликому пансіоні",
                "We're staying at a small guesthouse", "Küçük bir pansiyonda kalıyoruz", "Nocujemy w małym pensjonacie",
                "Dormiamo in una piccola pensione", "Nos alojamos en una pensión pequeña", "On dort dans une petite pension",
                "Spíme v malém penzionu")}),
    2413: ("снова Projekt", {**all_x(
        "Wie ist das Missverständnis entstanden?", "Как возникло это недоразумение?", "Як виникло це непорозуміння?",
        "How did the misunderstanding arise?", "Bu yanlış anlama nasıl ortaya çıktı?", "Jak powstało to nieporozumienie?",
        "Come è nato il malinteso?", "¿Cómo surgió el malentendido?", "Comment ce malentendu est-il né?",
        "Jak vzniklo to nedorozumění?")}),
    9482: (EN + " («education» — не тот смысл)", {"x_en": "A good upbringing is important for children"}),
    17139: ("«Die Straße hat eine scharfe Kurve» — пусто", {**all_x(
        "Fahr in der Kurve langsamer!", "На повороте сбавь скорость!", "На повороті збав швидкість!", "Slow down on the bend!",
        "Virajda yavaşla!", "Zwolnij na zakręcie!", "Rallenta in curva!", "¡Reduce en la curva!", "Ralentis dans le virage!",
        "V zatáčce zpomal!")}),
    11724: ("«Wir gehen in die Kneipe» — шаблон «gehen»; убрать пометку (hovor.)", {"t_cs": "hospoda, putyka", **all_x(
        "Nach der Arbeit treffen wir uns in der Kneipe", "После работы встречаемся в пивной", "Після роботи зустрічаємося в пивній",
        "After work we meet up at the pub", "İşten sonra birahanede buluşuyoruz", "Po pracy spotykamy się w knajpie",
        "Dopo il lavoro ci vediamo al bar", "Después del trabajo quedamos en el bar", "Après le boulot, on se retrouve au bistrot",
        "Po práci se sejdeme v hospodě")}),
    7116: ("«Die Distanz ist zu groß» — пусто", {**all_x(
        "Er hält immer Distanz zu seinen Kollegen", "Он всегда держит дистанцию с коллегами", "Він завжди тримає дистанцію з колегами",
        "He always keeps his distance from colleagues", "Meslektaşlarıyla hep mesafesini korur",
        "Zawsze trzyma dystans wobec kolegów", "Mantiene sempre le distanze con i colleghi",
        "Siempre guarda las distancias con sus compañeros", "Il garde toujours ses distances avec ses collègues",
        "Vždycky si od kolegů drží odstup")}),
    2415: ("«Die Enttäuschung war groß» — пусто", {**all_x(
        "Der Film war eine echte Enttäuschung", "Фильм оказался настоящим разочарованием", "Фільм став справжнім розчаруванням",
        "The film was a real disappointment", "Film tam bir hayal kırıklığıydı", "Film był prawdziwym rozczarowaniem",
        "Il film è stato una vera delusione", "La película fue una auténtica decepción", "Le film a été une vraie déception",
        "Ten film byl opravdové zklamání")}),
    1114: (LIST + " (было семь значений)", {
        "t_ru": "поставить, выключить", "t_uk": "поставити, вимкнути", "t_en": "to park, to switch off",
        "t_tr": "park etmek, kapatmak", "t_pl": "zaparkować, wyłączyć", "t_it": "parcheggiare, spegnere",
        "t_es": "aparcar, apagar", "t_fr": "garer, éteindre", "t_cs": "zaparkovat, vypnout"}),
    7122: ("«Er ging quer über die Straße» — претерит", {**all_x(
        "Er parkt immer quer über zwei Plätze", "Он всегда паркуется поперёк двух мест", "Він завжди паркується поперек двох місць",
        "He always parks across two spaces", "Hep iki park yerine çapraz park ediyor", "Zawsze parkuje w poprzek na dwóch miejscach",
        "Parcheggia sempre di traverso su due posti", "Siempre aparca de través en dos plazas",
        "Il se gare toujours en travers sur deux places", "Vždycky parkuje napříč přes dvě místa")}),
    9483: (EN + " («Math» — американское); убрать пометки", {"t_en": "maths", "t_fr": "les maths",
                                                            "t_cs": "matematika, matika", "x_en": "Maths is sometimes hard for me"}),
    7124: ("«ein ursprüngliches Rezept aus meiner Familie» — калька; живое — «Ursprünglich wollte ich …»", {**all_x(
        "Ursprünglich wollte ich nur ein Jahr bleiben", "Изначально я хотел остаться только на год",
        "Спочатку я хотів залишитися лише на рік", "Originally I only wanted to stay for a year",
        "Aslında sadece bir yıl kalmak istiyordum", "Pierwotnie chciałem zostać tylko rok",
        "Inizialmente volevo restare solo un anno", "Originalmente solo quería quedarme un año",
        "À l'origine, je voulais rester seulement un an", "Původně jsem chtěl zůstat jen rok")}),
    12187: (EN + " («100-meter» — американское)", {"x_en": "He set a new record in the 100 metres"}),
    2863: ("«Die Studie zeigt interessante Ergebnisse» — отчёт", {**all_x(
        "Laut einer neuen Studie schlafen wir zu wenig", "Согласно новому исследованию, мы слишком мало спим",
        "Згідно з новим дослідженням, ми надто мало спимо", "According to a new study we don't sleep enough",
        "Yeni bir araştırmaya göre çok az uyuyoruz", "Według nowego badania śpimy za mało",
        "Secondo un nuovo studio dormiamo troppo poco", "Según un nuevo estudio, dormimos demasiado poco",
        "Selon une nouvelle étude, on ne dort pas assez", "Podle nové studie spíme příliš málo")}),
    7127: ("«Das sollte genügen für diese Aufgabe» — порядок слов", {**all_x(
        "Danke, das genügt", "Спасибо, этого достаточно", "Дякую, цього достатньо", "Thanks, that's enough",
        "Teşekkürler, bu yeterli", "Dzięki, to wystarczy", "Grazie, basta così", "Gracias, es suficiente",
        "Merci, ça suffit", "Díky, to stačí")}),
    1322: ("«Die Veranstaltung hat eine Dauer von …» — объявление; живое — «auf Dauer»", {
        "t_en": "duration, long run", "t_pl": "czas trwania, dłuższa meta", "t_it": "la durata, a lungo andare",
        "t_es": "la duración, a la larga", "t_fr": "la durée, à la longue",
        **all_x("Auf Dauer ist das zu teuer", "На длительный срок это слишком дорого", "На тривалий термін це задорого",
                "In the long run that's too expensive", "Uzun süre için bu çok pahalı", "Na dłuższą metę to za drogie",
                "A lungo andare è troppo caro", "A la larga es demasiado caro", "À la longue, c'est trop cher",
                "Na delší dobu je to moc drahé")}),
    785: ("«Sie trägt einen Schal» — шаблон одежды", {**all_x(
        "Nimm einen Schal mit, es ist kalt", "Возьми шарф, холодно", "Візьми шарф, холодно", "Take a scarf, it's cold",
        "Bir atkı al, hava soğuk", "Weź szalik, jest zimno", "Prendi una sciarpa, fa freddo", "Llévate una bufanda, hace frío",
        "Prends une écharpe, il fait froid", "Vezmi si šálu, je zima")}),
    8878: ("«female cook» — лишнее", {"t_en": "cook, chef", "t_tr": "aşçı"}),
    1358: (LIST + " (было семь значений); en «apartment»", {
        "t_ru": "обставлять, настраивать", "t_uk": "облаштовувати, налаштовувати", "t_en": "to furnish, to set up",
        "t_tr": "döşemek, kurmak", "t_pl": "urządzać, ustawić", "t_it": "arredare, impostare", "t_es": "amueblar, configurar",
        "t_fr": "meubler, configurer", "t_cs": "zařídit, nastavit", "x_en": "I'm furnishing my flat"}),
    14481: ("пример про Kunstgalerie, а не про Galerie", {**all_x(
        "Ihre Bilder hängen in einer Galerie in Berlin", "Её картины висят в галерее в Берлине", "Її картини висять у галереї в Берліні",
        "Her paintings hang in a gallery in Berlin", "Resimleri Berlin'de bir galeride asılı", "Jej obrazy wiszą w galerii w Berlinie",
        "I suoi quadri sono esposti in una galleria a Berlino", "Sus cuadros cuelgan en una galería de Berlín",
        "Ses tableaux sont exposés dans une galerie à Berlin", "Její obrazy visí v galerii v Berlíně")}),
    8881: ("«Die Polizistin hat den Dieb verhaftet» — шаблон verhaften", {"t_en": "policewoman", "t_tr": "kadın polis", **all_x(
        "Frag doch die Polizistin dort nach dem Weg", "Спроси дорогу у той полицейской", "Запитай дорогу в тієї поліцейської",
        "Ask the policewoman over there for directions", "Şuradaki kadın polise yolu sor", "Zapytaj tamtą policjantkę o drogę",
        "Chiedi la strada a quella poliziotta", "Pregúntale el camino a esa policía", "Demande ton chemin à la policière là-bas",
        "Zeptej se na cestu tamté policistky")}),
    7140: ("«Ich schüttle den Baum …» — пусто", {**all_x(
        "Er schüttelt nur den Kopf", "Он только качает головой", "Він лише хитає головою", "He just shakes his head",
        "Sadece başını sallıyor", "Tylko potrząsa głową", "Scuote solo la testa", "Solo sacude la cabeza",
        "Il secoue juste la tête", "Jen potřásá hlavou")}),
    18725: ("ru «должны учиться» — калька", {"x_ru": "Будущим поколениям стоит у нас поучиться"}),
    835: ("«Sie trägt ein weißes Shirt» — шаблон одежды", {**all_x(
        "Zieh dir ein frisches Shirt an", "Надень чистую футболку", "Вдягни чисту футболку", "Put on a clean T-shirt",
        "Temiz bir tişört giy", "Załóż czystą koszulkę", "Mettiti una maglietta pulita", "Ponte una camiseta limpia",
        "Mets un t-shirt propre", "Vezmi si čisté tričko")}),
    14482: (LIST, {"t_ru": "выпуск, расход", "t_uk": "випуск, витрата", "t_en": "issue, expense", "t_tr": "sayı, harcama",
                   "t_pl": "wydanie, wydatek", "t_it": "il numero, la spesa", "t_es": "el número, el gasto",
                   "t_fr": "le numéro, la dépense", "t_cs": "číslo, výdaj"}),
    1166: ("«Armut ist ein großes Problem» — газета", {**all_x(
        "In vielen Ländern leben Kinder in Armut", "Во многих странах дети живут в бедности", "У багатьох країнах діти живуть у бідності",
        "In many countries children live in poverty", "Birçok ülkede çocuklar yoksulluk içinde yaşıyor",
        "W wielu krajach dzieci żyją w ubóstwie", "In molti paesi i bambini vivono in povertà",
        "En muchos países los niños viven en la pobreza", "Dans beaucoup de pays, des enfants vivent dans la pauvreté",
        "V mnoha zemích žijí děti v chudobě")}),
}

SPLIT_LATER = {}
