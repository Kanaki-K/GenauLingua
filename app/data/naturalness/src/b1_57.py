"""B1, блок 57: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    1514: ("«Mein Handgelenk tut weh» — шаблон «tut weh»", {**all_x(
        "Er hat sich beim Sturz das Handgelenk gebrochen", "При падении он сломал запястье", "Під час падіння він зламав зап'ястя",
        "He broke his wrist when he fell", "Düşünce el bileğini kırdı", "Przy upadku złamał nadgarstek",
        "Cadendo si è rotto il polso", "Al caerse se rompió la muñeca", "En tombant, il s'est cassé le poignet",
        "Při pádu si zlomil zápěstí")}),
    556: ("«Sie trinkt eine Limonade» — пусто", {**all_x(
        "Im Sommer mache ich gern selbst Limonade", "Летом я люблю сам делать лимонад", "Улітку я люблю сам робити лимонад",
        "In summer I like making my own lemonade", "Yazın kendi limonatamı yapmayı severim", "Latem lubię sam robić lemoniadę",
        "D'estate mi piace fare la limonata in casa", "En verano me gusta hacer limonada casera",
        "L'été, j'aime faire de la limonade maison", "V létě rád dělám domácí limonádu")}),
    2964: ("«Das ist Verschwendung» — шаблон Zeitverschwendung", {**all_x(
        "So viel Essen wegzuwerfen ist eine echte Verschwendung", "Выбрасывать столько еды — настоящее расточительство",
        "Викидати стільки їжі — справжнє марнотратство", "Throwing away so much food is a real waste",
        "Bu kadar yemeği atmak tam bir israf", "Wyrzucanie tyle jedzenia to prawdziwe marnotrawstwo",
        "Buttare via così tanto cibo è un vero spreco", "Tirar tanta comida es un auténtico desperdicio",
        "Jeter autant de nourriture, c'est du vrai gaspillage", "Vyhazovat tolik jídla je opravdové plýtvání")}),
    12622: ("ru «Этот человек с физической инвалидностью» — канцелярит", {**all_x(
        "Der Eingang ist auch für behinderte Menschen geeignet", "Вход подходит и для людей с инвалидностью",
        "Вхід підходить і для людей з інвалідністю", "The entrance is also suitable for disabled people",
        "Giriş engelli insanlar için de uygun", "Wejście jest dostosowane także dla osób niepełnosprawnych",
        "L'ingresso è adatto anche alle persone disabili", "La entrada también es apta para personas con discapacidad",
        "L'entrée est aussi adaptée aux personnes handicapées", "Vchod je vhodný i pro postižené lidi")}),
    1899: ("«Sport stärkt die Gesundheit» — лозунг; " + LIST, {
        "t_ru": "укреплять, подкреплять силы", "t_uk": "зміцнювати, підкріплювати сили", "t_en": "to strengthen, to refresh oneself",
        "t_tr": "güçlendirmek", "t_pl": "wzmacniać, umacniać", "t_it": "rafforzare, rifocillarsi", "t_es": "fortalecer, reponer fuerzas",
        "t_fr": "renforcer, se restaurer", "t_cs": "posilovat, posilnit se",
        **all_x("Nach der Wanderung stärken wir uns mit einer Brotzeit", "После похода мы подкрепимся перекусом",
                "Після походу ми підкріпимося перекусом", "After the hike we'll refresh ourselves with a snack",
                "Yürüyüşten sonra bir atıştırmalıkla güç toplayalım", "Po wędrówce wzmocnimy się przekąską",
                "Dopo l'escursione ci rifocilliamo con uno spuntino", "Después de la caminata repondremos fuerzas con un tentempié",
                "Après la randonnée, on se restaure avec un casse-croûte", "Po túře se posilníme svačinou")}),
    3003: (EN, {"x_en": "I'm going away tomorrow"}),
    2620: ("ru «Мы должны разрешить» — калька", {"x_ru": "Нам надо разрешить этот конфликт"}),
    12625: ("убрать пометки (coloq.)/(fam.)", {"t_es": "adicto, enganchado", "t_fr": "dépendant, accro"}),
    18219: ("убрать пометку (fam.)", {"t_fr": "la climatisation, la clim"}),
    1840: ("«Er hat einen Schnurrbart» — шаблон Bart («Er hat einen langen Bart»)", {"t_en": "moustache", **all_x(
        "Mit Schnurrbart sieht er älter aus", "С усами он выглядит старше", "З вусами він виглядає старшим",
        "He looks older with a moustache", "Bıyıkla daha yaşlı görünüyor", "Z wąsami wygląda starzej",
        "Con i baffi sembra più vecchio", "Con bigote parece mayor", "Avec la moustache, il fait plus vieux",
        "S knírem vypadá starší")}),
    17948: (EN + " («analyzes» — американское)", {"x_en": "The coach analyses the game and shows the players their mistakes"}),
    2804: ("«Die Schaukel schwingt hin und her» — шаблон Schaukel", {**all_x(
        "Die Fans schwingen ihre Fahnen", "Болельщики размахивают флагами", "Уболівальники розмахують прапорами",
        "The fans are waving their flags", "Taraftarlar bayraklarını sallıyor", "Kibice wymachują flagami",
        "I tifosi agitano le bandiere", "Los aficionados agitan sus banderas", "Les supporters agitent leurs drapeaux",
        "Fanoušci mávají vlajkami")}),
    8888: (LIST, {"t_en": "reporter", "t_tr": "muhabir, haberci"}),
    2852: ("«Ich habe ein Stipendium» — пусто", {**all_x(
        "Ohne Stipendium könnte ich nicht studieren", "Без стипендии я бы не смог учиться", "Без стипендії я б не зміг навчатися",
        "Without a scholarship I couldn't study", "Burs olmadan okuyamazdım", "Bez stypendium nie mógłbym studiować",
        "Senza borsa di studio non potrei studiare", "Sin beca no podría estudiar",
        "Sans bourse, je ne pourrais pas faire mes études", "Bez stipendia bych nemohl studovat")}),
    15053: ("«Der stumme Schauspieler konnte …» — претерит", {**all_x(
        "Warum bist du heute so stumm?", "Почему ты сегодня такой молчаливый?", "Чому ти сьогодні такий мовчазний?",
        "Why are you so silent today?", "Bugün neden bu kadar suskunsun?", "Czemu jesteś dziś taki milczący?",
        "Perché oggi sei così silenzioso?", "¿Por qué estás hoy tan callado?", "Pourquoi tu es si silencieux aujourd'hui?",
        "Proč jsi dneska tak tichý?")}),
    11729: ("«Zum Dessert gab es …» — претерит", {**all_x(
        "Als Dessert empfehle ich die Schokoladenmousse", "На десерт рекомендую шоколадный мусс", "На десерт раджу шоколадний мус",
        "For dessert I recommend the chocolate mousse", "Tatlı olarak çikolatalı musu öneririm", "Na deser polecam mus czekoladowy",
        "Come dessert le consiglio la mousse al cioccolato", "De postre le recomiendo la mousse de chocolate",
        "En dessert, je vous recommande la mousse au chocolat", "Jako dezert doporučuji čokoládovou pěnu")}),
    777: ("«Sie isst Torte mit Sahne» — пусто", {**all_x(
        "Für die Soße brauchen wir noch Sahne", "Для соуса нам ещё нужны сливки", "Для соусу нам ще потрібні вершки",
        "We still need cream for the sauce", "Sos için hâlâ kremaya ihtiyacımız var", "Do sosu potrzebujemy jeszcze śmietany",
        "Per la salsa ci serve ancora la panna", "Para la salsa aún necesitamos nata",
        "Il nous faut encore de la crème pour la sauce", "Na omáčku ještě potřebujeme smetanu")}),
    15527: ("«Die Schildkröte bewegte sich …» — претерит; «Panzer» уже у Panzer", {**all_x(
        "Unsere Schildkröte schläft den ganzen Winter", "Наша черепаха спит всю зиму", "Наша черепаха спить усю зиму",
        "Our tortoise sleeps all winter", "Kaplumbağamız bütün kış uyuyor", "Nasz żółw śpi całą zimę",
        "La nostra tartaruga dorme tutto l'inverno", "Nuestra tortuga duerme todo el invierno",
        "Notre tortue dort tout l'hiver", "Naše želva prospí celou zimu")}),
    2722: ("«Das ist aus Plastik» — пусто, шаблон Metall", {**all_x(
        "Wir versuchen, weniger Plastik zu kaufen", "Мы стараемся покупать меньше пластика", "Ми намагаємося купувати менше пластику",
        "We try to buy less plastic", "Daha az plastik almaya çalışıyoruz", "Staramy się kupować mniej plastiku",
        "Cerchiamo di comprare meno plastica", "Intentamos comprar menos plástico", "On essaie d'acheter moins de plastique",
        "Snažíme se kupovat méně plastu")}),
    1278: ("«Der Bildschirm … ist kaputt» — шаблон «ist kaputt»", {**all_x(
        "Du sitzt zu viel vor dem Bildschirm", "Ты слишком много сидишь перед экраном", "Ти надто багато сидиш перед екраном",
        "You spend too much time in front of the screen", "Ekranın karşısında çok fazla oturuyorsun",
        "Za dużo siedzisz przed ekranem", "Stai troppo davanti allo schermo", "Pasas demasiado tiempo delante de la pantalla",
        "Tu passes trop de temps devant l'écran", "Moc sedíš u obrazovky")}),
    2088: ("«Der Wecker klingelt um 7 Uhr» — пусто", {**all_x(
        "Ich habe den Wecker nicht gehört", "Я не услышал будильник", "Я не почув будильника", "I didn't hear the alarm",
        "Çalar saati duymadım", "Nie usłyszałem budzika", "Non ho sentito la sveglia", "No he oído el despertador",
        "Je n'ai pas entendu le réveil", "Neslyšel jsem budík")}),
}

REPLACE = [{"id": 16209, "by": 2484, "lang": "de", "why": "Friede — книжный вариант Frieden"}]

SPLIT_LATER = {
    12622: ["behindert (молодёжн., оскорбит.) = «тупой»; не давать в примерах"],
}
