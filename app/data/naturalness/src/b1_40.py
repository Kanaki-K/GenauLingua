"""B1, блок 40: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    3078: ("«Der Zutritt zum Fitnessstudio kostet extra» — там говорят Eintritt", {**all_x(
        "Kinder haben hier keinen Zutritt", "Детям сюда вход запрещён", "Дітям сюди вхід заборонено",
        "No entry for children here", "Çocukların buraya girişi yasak", "Dzieci nie mają tu wstępu",
        "Qui i bambini non hanno accesso", "Aquí los niños no tienen acceso", "Ici, l'accès est interdit aux enfants",
        "Děti sem nemají přístup")}),
    6918: ("снова Ozean; " + LIST, {
        "t_ru": "глубина", "t_uk": "глибина", "t_en": "depth", "t_tr": "derinlik", "t_pl": "głębokość, głębia",
        **all_x("Das Wasser hat hier eine Tiefe von drei Metern", "Глубина воды здесь три метра", "Глибина води тут три метри",
                "The water here has a depth of three metres", "Suyun derinliği burada üç metre",
                "Głębokość wody wynosi tu trzy metry", "Qui l'acqua ha una profondità di tre metri",
                "Aquí el agua tiene una profundidad de tres metros", "Ici, l'eau a une profondeur de trois mètres",
                "Voda tu má hloubku tři metry")}),
    6919: ("убрать пометки (coloq.)/(hovor.); " + LIST, {
        "t_ru": "шум, ссора", "t_uk": "шум, сварка", "t_en": "noise, row", "t_tr": "gürültü, kavga", "t_pl": "hałas, kłótnia",
        "t_it": "il rumore, la lite", "t_es": "el ruido, la bronca", "t_fr": "le bruit, la dispute", "t_cs": "hluk, hádka"}),
    6920: ("«Das Buch ist gebunden» — пусто; " + LIST, {
        "t_ru": "связанный, занятый", "t_uk": "зв'язаний, зайнятий", "t_en": "bound, taken", "t_tr": "bağlı",
        "t_pl": "związany, zajęty", "t_it": "legato, impegnato", "t_es": "atado, comprometido", "t_fr": "lié, pris",
        "t_cs": "vázaný, zadaný",
        **all_x("Bist du noch frei oder schon gebunden?", "Ты ещё свободен или уже занят?", "Ти ще вільний чи вже зайнятий?",
                "Are you still single or already taken?", "Hâlâ bekâr mısın, yoksa birine bağlı mısın?",
                "Jesteś jeszcze wolny, czy już zajęty?", "Sei ancora libero o già impegnato?",
                "¿Sigues libre o ya estás comprometido?", "Tu es encore libre ou déjà pris?",
                "Jsi ještě volný, nebo už zadaný?")}),
    1804: ("«Er bekommt Rente» — пусто", {"t_en": "pension, retirement", **all_x(
        "Von der Rente allein kann man kaum leben", "На одну пенсию почти не проживёшь",
        "На саму пенсію майже не проживеш", "You can hardly live on your pension alone",
        "Sadece emekli maaşıyla zor geçinilir", "Z samej emerytury trudno wyżyć",
        "Con la sola pensione si vive a stento", "Solo con la pensión apenas se puede vivir",
        "On peut à peine vivre de sa seule retraite", "Ze samotného důchodu se skoro nedá žít")}),
    12559: ("ru «Ты должен принять» — калька; " + LIST, {
        "t_ru": "принимать, занимать", "t_uk": "приймати, займати", "t_en": "to take, to occupy", "t_tr": "almak, yer kaplamak",
        "t_pl": "przyjmować, zajmować", "t_it": "prendere, occupare", "t_es": "tomar, ocupar", "t_fr": "prendre, occuper",
        "t_cs": "vzít si, zaujmout", "x_ru": "Тебе надо принять это лекарство", "x_uk": "Тобі треба прийняти ці ліки"}),
    13965: (EN + " («rumor»); убрать пометку (hovor.)", {"t_cs": "fáma, drb", "t_en": "rumour, gossip",
                                                       "x_en": "That's just a rumour"}),
    1110: (EN + " («vacation»)", {"x_en": "On holiday I can finally switch off"}),
    1944: ("«Die Temperatur ist hoch» — пусто", {"t_it": "la temperatura, la febbre", "t_es": "la temperatura, la fiebre",
                                                **all_x("Hast du Temperatur?", "У тебя температура?", "У тебе температура?",
                                                        "Have you got a temperature?", "Ateşin var mı?", "Masz gorączkę?",
                                                        "Hai la febbre?", "¿Tienes fiebre?", "Tu as de la température?",
                                                        "Máš teplotu?")}),
    17117: ("«Wir folgen dieser Route» — пусто", {**all_x(
        "Das Navi berechnet eine neue Route", "Навигатор прокладывает новый маршрут", "Навігатор прокладає новий маршрут",
        "The satnav is calculating a new route", "Navigasyon yeni bir rota hesaplıyor", "Nawigacja wyznacza nową trasę",
        "Il navigatore calcola un nuovo percorso", "El GPS calcula una nueva ruta", "Le GPS calcule un nouvel itinéraire",
        "Navigace počítá novou trasu")}),
    1707: ("«Ich habe eine Münze gefunden» — пусто", {**all_x(
        "Hast du eine Münze für den Einkaufswagen?", "У тебя есть монетка для тележки?", "У тебе є монетка для візка?",
        "Have you got a coin for the trolley?", "Market arabası için bozuk paran var mı?", "Masz monetę do wózka?",
        "Hai una moneta per il carrello?", "¿Tienes una moneda para el carro?", "Tu as une pièce pour le caddie?",
        "Máš minci na vozík?")}),
    14447: ("«Die moderne Zivilisation ist kompliziert» — сочинение", {**all_x(
        "Endlich wieder Zivilisation!", "Наконец снова цивилизация!", "Нарешті знову цивілізація!", "Civilisation at last!",
        "Sonunda yine medeniyet!", "Nareszcie znowu cywilizacja!", "Finalmente di nuovo la civiltà!",
        "¡Por fin, civilización otra vez!", "Enfin la civilisation!", "Konečně zase civilizace!")}),
    16079: ("«Niemand darf morden» — пусто", {**all_x(
        "In diesem Krimi mordet der Gärtner", "В этом детективе убивает садовник", "У цьому детективі вбиває садівник",
        "In this crime novel it's the gardener who murders", "Bu polisiyede bahçıvan cinayet işliyor",
        "W tym kryminale morduje ogrodnik", "In questo giallo ad assassinare è il giardiniere",
        "En esta novela policíaca asesina el jardinero", "Dans ce polar, c'est le jardinier qui assassine",
        "V téhle detektivce vraždí zahradník")}),
    6921: (LIST, {"t_ru": "отозвать, уединиться", "t_uk": "відкликати, усамітнитися", "t_en": "to withdraw, to retreat",
                  "t_tr": "geri çekmek, inzivaya çekilmek", "t_pl": "wycofać, wycofać się"}),
    12561: ("«einen Notruf absetzen» — канцелярит; " + LIST, {
        "t_ru": "экстренный вызов, служба спасения", "t_uk": "екстрений виклик, служба порятунку",
        "t_en": "emergency call, emergency number", "t_tr": "acil çağrı, acil durum numarası",
        "t_pl": "numer alarmowy, wezwanie pomocy",
        **all_x("Ruf sofort den Notruf an!", "Немедленно звони в службу спасения!", "Негайно дзвони в службу порятунку!",
                "Call the emergency number right away!", "Hemen acil durum numarasını ara!",
                "Dzwoń natychmiast na numer alarmowy!", "Chiama subito il numero di emergenza!",
                "¡Llama ya al número de emergencias!", "Appelle tout de suite le numéro d'urgence!",
                "Okamžitě volej tísňovou linku!")}),
    6923: (EN + "; ru «Можешь ли ты» — книжно", {"x_ru": "Ты можешь их различить?", "x_en": "Can you tell them apart?"}),
    6772: ("«Das Wetter ist mir heute zu mies» — снова погода; убрать пометки", {
        "t_ru": "паршивый, подлый", "t_uk": "паршивий, підлий", "t_en": "lousy, mean", "t_tr": "berbat, alçak",
        "t_pl": "podły, parszywy", "t_it": "pessimo, meschino", "t_es": "malísimo, ruin", "t_fr": "minable, pourri",
        "t_cs": "mizerný, podlý",
        **all_x("So eine miese Aktion hätte ich von dir nicht erwartet", "Такого подлого поступка я от тебя не ожидал",
                "Такого підлого вчинку я від тебе не чекав", "I didn't expect such a lousy move from you",
                "Senden böyle alçakça bir hareket beklemezdim", "Nie spodziewałem się po tobie takiego podłego zagrania",
                "Non mi aspettavo da te una mossa così meschina", "No esperaba de ti una jugada tan ruin",
                "Je ne m'attendais pas à un coup aussi minable de ta part", "Takovou podlou akci bych od tebe nečekal")}),
    14448: ("«Die alte Burg steht auf dem Hügel» — шаблон Festung («Die alte Festung steht auf dem Berg»)", {**all_x(
        "Die Kinder bauen eine Burg aus Sand", "Дети строят замок из песка", "Діти будують замок із піску",
        "The kids are building a castle out of sand", "Çocuklar kumdan kale yapıyor", "Dzieci budują zamek z piasku",
        "I bambini costruiscono un castello di sabbia", "Los niños construyen un castillo de arena",
        "Les enfants construisent un château de sable", "Děti stavějí hrad z písku")}),
    2351: ("«Das war eine doofe Idee» — шаблон dämlich, bescheuert; убрать пометки", {
        "t_fr": "bête, idiot", "t_cs": "hloupý, pitomý", "t_ru": "глупый, дурацкий", "t_uk": "дурний, безглуздий",
        "t_en": "stupid, silly", "t_tr": "aptal, saçma", "t_pl": "głupi, durny",
        **all_x("Ach, ist das doof!", "Ой, как глупо!", "Ой, як безглуздо!", "Oh, that's so silly!", "Ah, ne saçma!",
                "Ach, ale głupio!", "Che stupido!", "¡Qué tonto!", "Oh, c'est bête!", "To je ale hloupé!")}),
    10379: ("«Ich wundere mich über deine Reaktion» — книжно; живое — «Das wundert mich nicht»", {**all_x(
        "Das wundert mich gar nicht", "Меня это совсем не удивляет", "Мене це зовсім не дивує",
        "That doesn't surprise me at all", "Buna hiç şaşırmadım", "Wcale mnie to nie dziwi", "Non mi stupisce affatto",
        "No me sorprende nada", "Ça ne m'étonne pas du tout", "To mě vůbec neudivuje")}),
    9768: ("«Nach dem Streit sind wir quitt» — не тот смысл", {**all_x(
        "Du hast mich eingeladen, jetzt lade ich dich ein – dann sind wir quitt",
        "Ты меня угостил, теперь я тебя — и мы квиты", "Ти мене пригостив, тепер я тебе — і ми квити",
        "You treated me, now I'll treat you – then we're quits",
        "Sen beni davet ettin, şimdi ben seni – böylece ödeşmiş oluruz",
        "Ty mnie zaprosiłeś, teraz ja ciebie – i jesteśmy kwita", "Tu mi hai offerto, ora offro io – così siamo pari",
        "Tú me invitaste, ahora te invito yo, y estamos en paz",
        "Tu m'as invité, maintenant c'est moi – comme ça, on est quittes", "Ty jsi pozval mě, teď já tebe – a jsme kvit")}),
    6924: ("ru «совершенно невероятно» — не тот смысл; " + LIST, {
        "t_ru": "маловероятный, невероятно", "t_uk": "малоймовірний, неймовірно", "t_en": "unlikely, incredibly",
        "t_tr": "olasılıksız, inanılmaz derecede", "t_pl": "mało prawdopodobny, niesamowicie",
        "x_ru": "Это крайне маловероятно", "x_uk": "Це вкрай малоймовірно", "x_en": "That's highly unlikely"}),
    1538: (EN, {"x_en": "We're going there tomorrow"}),
    10381: ("ru «весьма разозлён» — книжно", {"x_ru": "Он был вне себя, потому что его поезд отменили"}),
    2774: ("«Ich fahre rückwärts» — пусто", {**all_x(
        "Kannst du rückwärts einparken?", "Ты умеешь парковаться задом?", "Ти вмієш паркуватися задом?",
        "Can you park in reverse?", "Geri geri park edebiliyor musun?", "Umiesz parkować tyłem?",
        "Sai parcheggiare in retromarcia?", "¿Sabes aparcar marcha atrás?", "Tu sais te garer en marche arrière?",
        "Umíš zaparkovat pozpátku?")}),
    10382: ("«Das Wetter war düster und grau» — снова погода", {**all_x(
        "Mach mal Licht an, hier ist es so düster", "Включи свет, здесь так мрачно", "Увімкни світло, тут так похмуро",
        "Put the light on, it's so gloomy in here", "Işığı aç, burası çok kasvetli", "Zapal światło, tu jest tak ponuro",
        "Accendi la luce, qui è così cupo", "Enciende la luz, aquí está todo muy oscuro",
        "Allume la lumière, c'est tellement sombre ici", "Rozsviť, je tu tak temno")}),
}

REPLACE = [{"id": 10377, "by": 6772, "lang": "de", "why": "miese — форма слова mies"}]

SPLIT_LATER = {}
