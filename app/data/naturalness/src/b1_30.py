"""B1, блок 30: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    17509: ("«Auf welchem Kanal läuft der Film?» — шаблон Sender; " + LIST, {
        "t_ru": "канал", "t_uk": "канал", "t_en": "channel, canal", "t_tr": "kanal", "t_pl": "kanał", "t_cs": "kanál",
        **all_x("Er hat einen eigenen YouTube-Kanal", "У него свой канал на YouTube", "У нього свій канал на YouTube",
                "He has his own YouTube channel", "Kendi YouTube kanalı var", "Ma własny kanał na YouTubie",
                "Ha un suo canale YouTube", "Tiene su propio canal de YouTube", "Il a sa propre chaîne YouTube",
                "Má vlastní kanál na YouTube")}),
    2131: ("«Ich gebe das Buch zurück» — пусто и снова Buch; " + LIST, {
        "t_ru": "возвращать, отдавать", "t_uk": "повертати, віддавати", "t_en": "to give back, to return",
        "t_pl": "oddawać, zwracać",
        **all_x("Gib mir sofort mein Handy zurück!", "Сейчас же верни мне телефон!", "Негайно поверни мені телефон!",
                "Give me my phone back right now!", "Telefonumu hemen geri ver!", "Oddaj mi natychmiast mój telefon!",
                "Ridammi subito il telefono!", "¡Devuélveme el móvil ahora mismo!", "Rends-moi tout de suite mon téléphone!",
                "Okamžitě mi vrať mobil!")}),
    12143: ("ru «плохого проигравшего» — калька; " + LIST, {
        "t_en": "loser", "t_tr": "kaybeden", "t_pl": "przegrany",
        "x_ru": "Никто не любит проигравших, которые злятся", "x_uk": "Ніхто не любить переможених, які зляться",
        "x_en": "Nobody likes a sore loser"}),
    16037: ("«Die Eltern müssen das Kind bestrafen» — учебник; ru «должны» — калька", {"t_en": "to punish", **all_x(
        "Dafür wirst du bestraft!", "За это тебя накажут!", "За це тебе покарають!", "You'll be punished for that!",
        "Bunun için cezalandırılacaksın!", "Zostaniesz za to ukarany!", "Per questo verrai punito!",
        "¡Te van a castigar por esto!", "Tu vas être puni pour ça!", "Za to budeš potrestán!")}),
    9756: (LIST + "; en «What brand is your car?» — о машине говорят make", {
        "t_ru": "марка, бренд", "t_uk": "марка, бренд", "t_en": "brand, make", "t_tr": "marka, pul",
        "t_pl": "marka, znaczek", "t_it": "la marca, il francobollo", "x_en": "What make is your car?"}),
    12540: (LIST, {"t_ru": "лекарство, средство", "t_uk": "ліки, засіб", "t_en": "remedy, cure", "t_tr": "ilaç, çare",
                   "t_pl": "lekarstwo, środek leczniczy", "t_it": "la cura, il rimedio", "t_es": "el remedio, la cura"}),
    10318: ("«Das Urteil war nicht gerecht» — суд; " + LIST, {
        "t_ru": "справедливый, честный", "t_tr": "adil, hakkaniyetli", "t_pl": "sprawiedliwy, uczciwy", "t_en": "fair, just",
        **all_x("Wir teilen den Kuchen gerecht auf", "Разделим торт по справедливости", "Поділимо торт справедливо",
                "Let's share the cake out fairly", "Pastayı adil paylaştıralım", "Podzielmy ciasto sprawiedliwie",
                "Dividiamo la torta in modo giusto", "Repartamos la tarta de forma justa",
                "Partageons le gâteau de façon équitable", "Rozdělme dort spravedlivě")}),
    1491: ("«Die Straße ist glatt» — пусто; " + LIST, {
        "t_ru": "скользкий, гладкий", "t_uk": "слизький, гладкий", "t_en": "slippery, smooth", "t_tr": "kaygan, pürüzsüz",
        "t_pl": "śliski, gładki",
        **all_x("Vorsicht, es ist glatt draußen!", "Осторожно, на улице скользко!", "Обережно, надворі слизько!",
                "Careful, it's slippery outside!", "Dikkat, dışarısı kaygan!", "Uważaj, na dworze jest ślisko!",
                "Attento, fuori è scivoloso!", "¡Cuidado, fuera está resbaladizo!", "Attention, c'est glissant dehors!",
                "Pozor, venku je kluzko!")}),
    6796: ("«Ein weiterer Grund ist das Wetter» — сочинение", {
        "t_pl": "kolejny, dalszy", "t_es": "otro, más",
        **all_x("Gibt es noch weitere Fragen?", "Есть ещё какие-нибудь вопросы?", "Є ще якісь питання?",
                "Are there any further questions?", "Başka sorusu olan var mı?", "Są jeszcze jakieś dalsze pytania?",
                "Ci sono altre domande?", "¿Hay más preguntas?", "Il y a d'autres questions?",
                "Máte ještě nějaké další otázky?")}),
    16038: (LIST, {"t_ru": "обман, мошенничество", "t_uk": "обман, шахрайство", "t_en": "fraud, cheating",
                   "t_tr": "dolandırıcılık, hile", "t_pl": "oszustwo, szachrajstwo", "t_it": "la truffa, la frode",
                   "t_es": "el fraude, la estafa", "t_fr": "la fraude, l'escroquerie"}),
    2375: ("«Es gab einen Einbruch» — пусто, шаблон Überfall; " + LIST, {
        "t_ru": "взлом, кража со взломом", "t_uk": "крадіжка зі зломом, злом", "t_en": "burglary, break-in",
        "t_tr": "hırsızlık, zorla girme", "t_pl": "włamanie", "t_es": "el robo, el allanamiento",
        **all_x("Nach dem Einbruch haben wir ein neues Schloss gekauft", "После взлома мы купили новый замок",
                "Після крадіжки зі зломом ми купили новий замок", "After the break-in we bought a new lock",
                "Hırsızlıktan sonra yeni bir kilit aldık", "Po włamaniu kupiliśmy nowy zamek",
                "Dopo il furto con scasso abbiamo comprato una serratura nuova",
                "Después del robo compramos una cerradura nueva", "Après le cambriolage, on a acheté une nouvelle serrure",
                "Po vloupání jsme koupili nový zámek")}),
    10319: (LIST, {"t_ru": "характер, персонаж", "t_uk": "характер, персонаж", "t_en": "character, personality",
                   "t_tr": "karakter, kişilik", "t_pl": "charakter, postać", "t_cs": "charakter, povaha"}),
    6798: ("ru «спонтанная акция» — калька; " + LIST, {
        "t_ru": "акция, действие", "t_uk": "акція, дія", "t_en": "special offer, campaign", "t_tr": "kampanya, eylem",
        "t_pl": "promocja, akcja", "t_it": "l'offerta, l'azione", "t_es": "la oferta, la acción",
        "t_fr": "la promotion, l'action",
        **all_x("Im Supermarkt gibt es heute eine Aktion", "В супермаркете сегодня акция", "У супермаркеті сьогодні акція",
                "There's a special offer at the supermarket today", "Bugün süpermarkette kampanya var",
                "W supermarkecie jest dziś promocja", "Oggi al supermercato c'è un'offerta", "Hoy hay una oferta en el súper",
                "Aujourd'hui, il y a une promotion au supermarché", "V supermarketu je dneska akce")}),
    2014: ("«Ich kaufe Unterwäsche» — пусто", {
        "t_ru": "нижнее бельё", "t_uk": "білизна, нижня білизна", "t_en": "underwear", "t_pl": "bielizna",
        **all_x("Ich brauche frische Unterwäsche", "Мне нужно свежее нижнее бельё", "Мені потрібна чиста білизна",
                "I need clean underwear", "Temiz iç çamaşırına ihtiyacım var", "Potrzebuję czystej bielizny",
                "Mi serve biancheria intima pulita", "Necesito ropa interior limpia",
                "J'ai besoin de sous-vêtements propres", "Potřebuju čisté spodní prádlo")}),
    6800: ("«Das Glas steht am Rand vom Tisch» — пусто; " + LIST, {
        "t_ru": "край, обочина", "t_uk": "край, узбіччя", "t_en": "edge, margin", "t_tr": "kenar, sınır",
        "t_pl": "krawędź, brzeg",
        **all_x("Stell das Glas nicht so nah an den Rand!", "Не ставь стакан так близко к краю!",
                "Не став склянку так близько до краю!", "Don't put the glass so close to the edge!",
                "Bardağı kenara bu kadar yakın koyma!", "Nie stawiaj szklanki tak blisko krawędzi!",
                "Non mettere il bicchiere così vicino al bordo!", "¡No pongas el vaso tan cerca del borde!",
                "Ne mets pas le verre si près du bord!", "Nedávej sklenici tak blízko k okraji!")}),
    2682: ("«Der Nebel ist heute sehr dicht» — снова погода; " + LIST, {
        "t_ru": "туман, дымка", "t_uk": "туман, імла", "t_en": "fog, mist", "t_tr": "sis, pus", "t_pl": "mgła",
        "t_es": "la niebla, la neblina",
        **all_x("Bei Nebel fahre ich ganz langsam", "В туман я еду очень медленно", "У туман я їжджу дуже повільно",
                "In fog I drive really slowly", "Siste çok yavaş sürüyorum", "We mgle jeżdżę bardzo powoli",
                "Con la nebbia guido pianissimo", "Con niebla conduzco muy despacio",
                "Par temps de brouillard, je roule très lentement", "V mlze jezdím hodně pomalu")}),
    10320: (LIST + "; ru «жестокая борьба» — калька", {
        "t_ru": "жестокий, грубый", "t_uk": "жорстокий, безжальний", "t_en": "brutal, cruel", "t_tr": "acımasız, vahşi",
        "t_pl": "brutalny, okrutny", "t_it": "brutale, crudele", "t_fr": "brutal, violent",
        "x_ru": "Это была жестокая драка"}),
    15448: (LIST, {"t_ru": "джунгли", "t_uk": "джунглі", "t_en": "jungle", "t_tr": "cangıl, yağmur ormanı",
                   "t_pl": "dżungla"}),
    2253: ("«Wir befragen die Teilnehmer» — анкета; " + LIST, {
        "t_ru": "опрашивать, допрашивать", "t_uk": "опитувати, допитувати", "t_en": "to question, to interview",
        "t_tr": "sormak, sorguya çekmek", "t_pl": "wypytywać, przepytać", "t_it": "intervistare, interrogare",
        "t_es": "entrevistar, interrogar", "t_fr": "interroger, sonder", "t_cs": "ptát se, vyslýchat",
        **all_x("Die Polizei hat alle Nachbarn befragt", "Полиция опросила всех соседей", "Поліція опитала всіх сусідів",
                "The police questioned all the neighbours", "Polis bütün komşuları sorguya çekti",
                "Policja przepytała wszystkich sąsiadów", "La polizia ha interrogato tutti i vicini",
                "La policía interrogó a todos los vecinos", "La police a interrogé tous les voisins",
                "Policie vyslechla všechny sousedy")}),
    13493: (LIST + "; ru «Относительно твоего вопроса» — канцелярит", {
        "t_ru": "относительно, насчёт", "t_uk": "щодо, стосовно", "t_en": "regarding, concerning",
        "t_tr": "hakkında, ile ilgili", "t_pl": "odnośnie, w sprawie", "t_it": "riguardo a, in merito a",
        "t_es": "respecto a, en cuanto a", "t_fr": "concernant, au sujet de",
        "x_ru": "Насчёт твоего вопроса ничего сказать не могу"}),
    12541: ("«Er war nach dem Unfall bewusstlos» — шаблон Bewusstsein, Koma («Nach dem Unfall …»)", {
        "t_ru": "без сознания", "t_tr": "baygın, bilinçsiz", "t_pl": "nieprzytomny", "t_it": "privo di sensi, svenuto",
        "t_fr": "inconscient, évanoui",
        **all_x("Er ist umgekippt und war kurz bewusstlos", "Он упал и ненадолго был без сознания",
                "Він упав і якийсь час був непритомний", "He keeled over and was unconscious for a moment",
                "Yere yığıldı ve kısa bir süre baygın kaldı", "Przewrócił się i był przez chwilę nieprzytomny",
                "È crollato ed è rimasto privo di sensi per un attimo", "Se desplomó y estuvo un momento inconsciente",
                "Il s'est effondré et est resté inconscient un moment", "Zhroutil se a chvíli byl v bezvědomí")}),
    1728: (EN, {"t_tr": "yeğen", "x_en": "My niece is studying in Berlin"}),
    2740: (LIST, {"t_ru": "скрипеть, визжать", "t_uk": "скрипіти, вищати", "t_en": "to squeak, to screech",
                  "t_tr": "gıcırdamak, ciyaklamak", "t_pl": "skrzypieć, piszczeć", "t_cs": "vrzat, skřípat"}),
    10322: ("«прядильщик» — другое слово; убрать пометки (colloq.)/(coloq.)/(fam.)/(hovor.)", {
        "t_ru": "псих, чудак", "t_uk": "псих, дивак", "t_en": "nutcase, weirdo", "t_tr": "deli, kaçık",
        "t_pl": "wariat, świr", "t_it": "il matto, lo svitato", "t_es": "el loco, el chiflado", "t_fr": "le fou, le cinglé",
        "t_cs": "blázen, cvok"}),
    16040: (LIST, {"t_en": "gangster"}),
    16041: ("«Die Entführung war in den Nachrichten» — пусто; " + LIST, {
        "t_ru": "похищение, угон", "t_uk": "викрадення", "t_en": "kidnapping, hijacking",
        "t_tr": "adam kaçırma, uçak kaçırma", "t_pl": "porwanie, uprowadzenie", "t_it": "il rapimento, il dirottamento",
        "t_fr": "l'enlèvement, le détournement",
        **all_x("Die Polizei geht von einer Entführung aus", "Полиция предполагает похищение", "Поліція підозрює викрадення",
                "The police suspect a kidnapping", "Polis adam kaçırma olayından şüpheleniyor", "Policja podejrzewa porwanie",
                "La polizia pensa a un rapimento", "La policía sospecha que es un secuestro",
                "La police pense à un enlèvement", "Policie předpokládá únos")}),
    2147: ("«Das war absichtlich» — пусто; " + LIST, {
        "t_ru": "нарочно, намеренно", "t_uk": "навмисно, спеціально", "t_en": "on purpose, deliberately",
        "t_tr": "bilerek, kasten", "t_pl": "celowo, specjalnie", "t_it": "apposta, di proposito",
        "t_es": "a propósito, adrede", "t_fr": "exprès, délibérément", "t_cs": "schválně, úmyslně",
        **all_x("Das hast du doch absichtlich gemacht!", "Ты же это нарочно сделал!", "Ти ж це навмисно зробив!",
                "You did that on purpose!", "Bunu bilerek yaptın!", "Zrobiłeś to celowo!", "L'hai fatto apposta!",
                "¡Lo has hecho a propósito!", "Tu l'as fait exprès!", "Udělal jsi to schválně!")}),
    2001: ("«Das ist unfair» — шаблон fair («Das ist nicht fair»); убрать пометку (hovor.)", {
        "t_cs": "nespravedlivý, nefér", "t_it": "ingiusto, scorretto",
        **all_x("Das ist unfair, du hast geschummelt!", "Это нечестно, ты жульничал!", "Це нечесно, ти шахрував!",
                "That's unfair, you cheated!", "Bu haksızlık, hile yaptın!", "To nieuczciwe, oszukiwałeś!",
                "È scorretto, hai barato!", "¡Eso es injusto, has hecho trampa!", "C'est injuste, tu as triché!",
                "To je nefér, podváděl jsi!")}),
    15450: ("«Der Esel läuft langsam» — пусто; " + LIST, {
        "t_ru": "осёл, ишак", "t_uk": "віслюк, осел", "t_en": "donkey", "t_tr": "eşek", "t_pl": "osioł",
        "t_es": "el burro",
        **all_x("Die Kinder dürfen auf dem Esel reiten", "Детям можно покататься на осле", "Дітям можна покататися на віслюку",
                "The kids are allowed to ride the donkey", "Çocuklar eşeğe binebilir", "Dzieci mogą pojeździć na ośle",
                "I bambini possono andare sull'asino", "Los niños pueden montar en burro",
                "Les enfants peuvent faire un tour à dos d'âne", "Děti se můžou svézt na oslovi")}),
    17100: ("«Der Panzer fuhr durch die Stadt» — претерит, хроника", {
        "t_ru": "панцирь, танк", "t_uk": "панцир, танк", "t_en": "shell, tank", "t_tr": "kabuk, tank",
        "t_pl": "pancerz, czołg", "t_it": "il guscio, il carro armato", "t_es": "el caparazón, el tanque",
        "t_fr": "la carapace, le char", "t_cs": "krunýř, tank",
        **all_x("Die Schildkröte hat einen harten Panzer", "У черепахи твёрдый панцирь", "У черепахи твердий панцир",
                "The tortoise has a hard shell", "Kaplumbağanın sert bir kabuğu var", "Żółw ma twardy pancerz",
                "La tartaruga ha un guscio duro", "La tortuga tiene un caparazón duro", "La tortue a une carapace dure",
                "Želva má tvrdý krunýř")}),
    6804: (LIST, {"t_ru": "прилечь, положить", "t_uk": "прилягти, покласти", "t_en": "to lie down, to put down",
                  "t_tr": "uzanmak, bir yere koymak", "t_pl": "położyć się, położyć", "t_it": "sdraiarsi, posare",
                  "t_es": "acostarse, dejar"}),
    6805: (LIST, {"t_ru": "надевать, вкладывать", "t_uk": "надягати, вкладати", "t_en": "to put on, to invest",
                  "t_tr": "takmak, yatırım yapmak", "t_pl": "zakładać, inwestować", "t_it": "mettere, investire",
                  "t_es": "poner, invertir", "t_fr": "mettre, investir", "t_cs": "nasadit, investovat",
                  "x_ru": "Можешь надеть на меня цепочку?", "x_en": "Can you put the necklace on for me?"}),
    12146: (EN + " («on the weekend» — американское)", {
        "t_ru": "рыбачить, ловить рыбу", "t_en": "to fish", "t_tr": "balık tutmak",
        "x_ru": "На выходных идём рыбачить", "x_en": "We're going fishing at the weekend"}),
    6806: ("«Sie trägt eine goldene Uhr» — шаблон одежды", {**all_x(
        "Im Herbst werden die Blätter golden", "Осенью листья становятся золотыми", "Восени листя стає золотим",
        "In autumn the leaves turn golden", "Sonbaharda yapraklar altın rengine döner", "Jesienią liście robią się złote",
        "In autunno le foglie diventano dorate", "En otoño las hojas se vuelven doradas",
        "En automne, les feuilles deviennent dorées", "Na podzim listí zezlátne")}),
    2983: ("«Ich verzichte darauf» — en «I give that up» — так не говорят; " + LIST, {
        "t_ru": "отказываться, обходиться без", "t_uk": "відмовлятися, обходитися без", "t_en": "to do without, to give up",
        "t_tr": "vazgeçmek, -sız idare etmek", "t_pl": "rezygnować, obywać się bez", "t_es": "renunciar, prescindir de",
        **all_x("Auf Fleisch verzichte ich schon seit Jahren", "Я уже много лет отказываюсь от мяса",
                "Я вже багато років відмовляюся від м'яса", "I've been doing without meat for years",
                "Yıllardır etten vazgeçtim", "Od lat rezygnuję z mięsa", "Rinuncio alla carne da anni",
                "Hace años que renuncio a la carne", "Je me passe de viande depuis des années",
                "Už roky se obejdu bez masa")}),
    6808: ("ru «потерпеть неудачу» — книжно; " + LIST, {
        "t_ru": "провалиться, отказать", "t_uk": "зазнати невдачі, відмовити", "t_en": "to fail",
        "t_tr": "başarısız olmak, bozulmak", "t_pl": "zawieść, przestać działać", "t_it": "fallire, cedere",
        "t_es": "fracasar, fallar", "t_fr": "échouer, lâcher",
        **all_x("Die Bremsen haben versagt", "Тормоза отказали", "Гальма відмовили", "The brakes failed",
                "Frenler bozuldu", "Hamulce przestały działać", "I freni hanno ceduto", "Los frenos fallaron",
                "Les freins ont lâché", "Brzdy selhaly")}),
    13939: (LIST, {"t_ru": "акцент, ударение"}),
}

REPLACE = [
    {"id": 2269, "by": 131, "lang": "de", "why": "benötigen — книжный вариант brauchen"},
    {"id": 6799, "by": 664, "lang": "de", "why": "lediglich — книжный вариант nur"},
]

SPLIT_LATER = {}
