"""B1, блок 43: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    6954: ("«Kannst du meine Sachen zurückholen?» — пусто", {"t_en": "to get back, to retrieve", **all_x(
        "Ich hole mir mein Geld zurück!", "Я верну себе свои деньги!", "Я поверну собі свої гроші!",
        "I'll get my money back!", "Paramı geri alacağım!", "Odzyskam swoje pieniądze!", "Mi riprendo i miei soldi!",
        "¡Voy a recuperar mi dinero!", "Je vais récupérer mon argent!", "Vezmu si zpátky svoje peníze!")}),
    17934: ("«Die Analyse zeigt interessante Ergebnisse» — отчёт", {**all_x(
        "Die Analyse vom Blut dauert zwei Tage", "Анализ крови займёт два дня", "Аналіз крові триватиме два дні",
        "The blood analysis takes two days", "Kan analizi iki gün sürüyor", "Analiza krwi trwa dwa dni",
        "L'analisi del sangue richiede due giorni", "El análisis de sangre tarda dos días",
        "L'analyse de sang prend deux jours", "Rozbor krve trvá dva dny")}),
    10396: ("«Das Kind war verängstigt und weinte» — претерит", {**all_x(
        "Der Hund ist ganz verängstigt", "Собака совсем напугана", "Собака зовсім налякана", "The dog is really frightened",
        "Köpek çok korkmuş", "Pies jest całkiem wystraszony", "Il cane è tutto spaventato", "El perro está muy asustado",
        "Le chien est tout apeuré", "Pes je úplně vystrašený")}),
    6955: ("ru «Ты должен следовать» — калька", {"x_ru": "Тебе надо соблюдать правила",
                                               "x_uk": "Тобі треба дотримуватися правил",
                                               "x_en": "You have to follow the rules"}),
    6956: ("«Dieser Plan ist gefährdet wegen der Probleme» — так не говорят", {**all_x(
        "Diese Tierart ist stark gefährdet", "Этот вид животных под серьёзной угрозой", "Цей вид тварин під серйозною загрозою",
        "This species is highly endangered", "Bu hayvan türü ciddi tehlike altında", "Ten gatunek jest poważnie zagrożony",
        "Questa specie è fortemente minacciata", "Esta especie está muy amenazada", "Cette espèce est très menacée",
        "Tento druh je vážně ohrožený")}),
    12567: ("«Er bekam einen Schlag ins Genick» — претерит", {"t_fr": "la nuque, le cou", **all_x(
        "Pass auf, du brichst dir noch das Genick!", "Осторожно, ты ещё шею себе сломаешь!", "Обережно, ще шию собі зламаєш!",
        "Careful, you'll break your neck!", "Dikkat, boynunu kıracaksın!", "Uważaj, bo skręcisz sobie kark!",
        "Attento, ti rompi l'osso del collo!", "¡Cuidado, que te vas a romper el cuello!",
        "Attention, tu vas te rompre le cou!", "Pozor, zlomíš si vaz!")}),
    10397: ("«Sein Verhalten war egoistisch und unfair» — претерит, en «behavior»", {**all_x(
        "Er denkt nur an sich, total egoistisch", "Он думает только о себе — ужасно эгоистично",
        "Він думає тільки про себе — жахливо егоїстично", "He only thinks of himself – totally selfish",
        "Sadece kendini düşünüyor, tam bir bencil", "Myśli tylko o sobie, totalnie samolubny",
        "Pensa solo a sé, è proprio egoista", "Solo piensa en sí mismo, es un egoísta",
        "Il ne pense qu'à lui, totalement égoïste", "Myslí jen na sebe, je strašně sobecký")}),
    14450: ("«Der Pastor hielt eine Predigt» — претерит", {**all_x(
        "Unser Pastor ist im Dorf sehr beliebt", "Нашего пастора в деревне очень любят", "Нашого пастора дуже люблять у селі",
        "Our pastor is very popular in the village", "Papazımız köyde çok seviliyor", "Nasz pastor jest bardzo lubiany we wsi",
        "Il nostro pastore è molto amato in paese", "Nuestro pastor es muy querido en el pueblo",
        "Notre pasteur est très apprécié au village", "Náš pastor je ve vesnici velmi oblíbený")}),
    6957: ("ru «Мы должны устранить» — калька", {"x_ru": "Проблему надо устранить", "x_en": "We need to get rid of the problem"}),
    16098: ("«Der Räuber floh mit dem Geld» — претерит", {
        "t_tr": "soyguncu, hırsız", "t_pl": "rabuś, złodziej", "t_it": "il rapinatore, il ladro", "t_cs": "lupič, zloděj",
        **all_x("Die Kinder spielen Räuber und Gendarm", "Дети играют в казаков-разбойников", "Діти граються в козаків-розбійників",
                "The kids are playing cops and robbers", "Çocuklar polis-hırsız oynuyor",
                "Dzieci bawią się w policjantów i złodziei", "I bambini giocano a guardie e ladri",
                "Los niños juegan a policías y ladrones", "Les enfants jouent aux gendarmes et aux voleurs",
                "Děti si hrají na četníky a zloděje")}),
    16100: ("ru «ты это не можешь делать» — калька", {"x_ru": "Без разрешения этого делать нельзя"}),
    13974: ("«… unfair von dir» — шаблон «… von dir»; " + LIST, {
        "t_ru": "крайне, весьма", "t_uk": "вкрай, надзвичайно", "t_en": "extremely, decidedly", "t_tr": "son derece, oldukça",
        "t_pl": "wyjątkowo, wręcz", "t_it": "decisamente, estremamente", "t_es": "sumamente, francamente",
        "t_fr": "vraiment, franchement", "t_cs": "vyloženě, výrazně",
        **all_x("Sie ist ausgesprochen hübsch", "Она весьма хорошенькая", "Вона надзвичайно гарна", "She's extremely pretty",
                "Son derece güzel", "Jest wyjątkowo ładna", "È decisamente carina", "Es sumamente guapa",
                "Elle est vraiment jolie", "Je vyloženě hezká")}),
    10400: ("«Das Kind war echt frech zu seiner Mutter» — претерит; убрать пометку (fam.)", {
        "t_fr": "insolent, effronté",
        **all_x("Das ist ja eine freche Antwort!", "Какой дерзкий ответ!", "Яка зухвала відповідь!", "What a cheeky answer!",
                "Ne küstah bir cevap!", "Co za bezczelna odpowiedź!", "Che risposta sfacciata!",
                "¡Qué respuesta tan descarada!", "Quelle réponse insolente!", "To je ale drzá odpověď!")}),
    6961: ("«Sein Status in den sozialen Medien ist sehr privat» — бессмыслица", {**all_x(
        "Was ist der Status von meiner Bestellung?", "Какой статус у моего заказа?", "Який статус мого замовлення?",
        "What's the status of my order?", "Siparişimin durumu ne?", "Jaki jest status mojego zamówienia?",
        "Qual è lo stato del mio ordine?", "¿Cuál es el estado de mi pedido?", "Quel est le statut de ma commande?",
        "Jaký je stav mé objednávky?")}),
    2231: ("«Ich möchte es ausprobieren» — пусто", {**all_x(
        "Das musst du unbedingt mal ausprobieren!", "Это тебе обязательно надо попробовать!", "Тобі обов'язково треба це спробувати!",
        "You've absolutely got to try it out!", "Bunu mutlaka denemelisin!", "Musisz to koniecznie wypróbować!",
        "Devi assolutamente provarlo!", "¡Tienes que probarlo sí o sí!", "Tu dois absolument essayer ça!",
        "Tohle musíš určitě vyzkoušet!")}),
    17121: (EN + " («gas station» — американское); " + LIST, {
        "t_ru": "заправка, АЗС", "t_uk": "заправка, АЗС", "t_en": "petrol station, filling station",
        "t_tr": "benzin istasyonu", "x_en": "The next petrol station is another 20 km away"}),
    16104: ("ru «Полиция должна была» — калька", {"x_ru": "Полиции пришлось задержать мужчину",
                                                  "x_uk": "Поліції довелося затримати чоловіка"}),
    11688: ("«Die Würstchen waren lecker beim Grillen» — претерит, порядок слов", {**all_x(
        "Zum Grillen gibt es Würstchen und Salat", "На гриль у нас сосиски и салат", "На гриль у нас сосиски й салат",
        "We're having sausages and salad for the barbecue", "Mangalda sosis ve salata var", "Na grilla są kiełbaski i sałatka",
        "Per la grigliata ci sono würstel e insalata", "Para la barbacoa hay salchichas y ensalada",
        "Pour le barbecue, il y a des saucisses et de la salade", "Na grilování jsou párky a salát")}),
}

REPLACE = [
    {"id": 13506, "by": 13482, "lang": "de", "why": "keines — вариант keins; пример тот же"},
    {"id": 16096, "by": 16084, "lang": "de", "why": "gesperrt — причастие от sperren; пример тот же («Straße … gesperrt»)"},
]

SPLIT_LATER = {}
