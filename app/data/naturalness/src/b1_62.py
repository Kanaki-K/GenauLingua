"""B1, блок 62: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    18251: ("«Der Mieter zahlt die Miete pünktlich» — договор", {**all_x(
        "Die neuen Mieter sind sehr laut", "Новые жильцы очень шумные", "Нові квартиранти дуже галасливі",
        "The new tenants are very noisy", "Yeni kiracılar çok gürültücü", "Nowi lokatorzy są bardzo głośni",
        "I nuovi inquilini sono molto rumorosi", "Los nuevos inquilinos son muy ruidosos",
        "Les nouveaux locataires sont très bruyants", "Noví nájemníci jsou hodně hluční")}),
    10674: ("«Der Horror dieses Films war …» — претерит; " + LIST, {
        "t_ru": "ужас, кошмар", "t_uk": "жах, кошмар", "t_en": "horror, nightmare", "t_tr": "korku, kabus",
        "t_pl": "horror, koszmar",
        **all_x("Die Fahrt zur Arbeit ist jeden Morgen der reinste Horror", "Дорога на работу каждое утро — сущий кошмар",
                "Дорога на роботу щоранку — справжній кошмар", "Getting to work every morning is a total nightmare",
                "Her sabah işe gitmek tam bir kabus", "Dojazd do pracy każdego ranka to prawdziwy koszmar",
                "Ogni mattina andare al lavoro è un vero orrore", "Ir al trabajo cada mañana es un auténtico horror",
                "Aller au travail chaque matin, c'est l'horreur", "Cesta do práce je každé ráno hotová hrůza")}),
    2812: ("«Wir senken die Preise» — шаблон erhöhen («Wir müssen die Preise erhöhen»)", {**all_x(
        "Kannst du bitte die Stimme senken?", "Можешь, пожалуйста, понизить голос?", "Можеш, будь ласка, стишити голос?",
        "Could you lower your voice, please?", "Lütfen sesini kısar mısın?", "Możesz, proszę, obniżyć głos?",
        "Puoi abbassare la voce, per favore?", "¿Puedes bajar la voz, por favor?", "Tu peux baisser la voix, s'il te plaît?",
        "Můžeš prosím snížit hlas?")}),
    13688: ("«Er trägt eine schwarze Kappe» — шаблон одежды", {**all_x(
        "Setz dir eine Kappe auf, die Sonne ist stark", "Надень кепку, солнце сильное", "Вдягни кепку, сонце сильне",
        "Put a cap on, the sun is strong", "Şapka tak, güneş çok güçlü", "Załóż czapkę, słońce mocno grzeje",
        "Mettiti un cappellino, il sole è forte", "Ponte una gorra, que el sol pega fuerte",
        "Mets une casquette, le soleil tape fort", "Nasaď si kšiltovku, slunce silně pálí")}),
    2491: ("«Ich bin total frustriert» — пусто", {**all_x(
        "Nach drei Absagen bin ich echt frustriert", "После трёх отказов я совсем расстроен", "Після трьох відмов я зовсім розчарований",
        "After three rejections I'm really frustrated", "Üç retten sonra gerçekten bunaldım",
        "Po trzech odmowach jestem naprawdę sfrustrowany", "Dopo tre rifiuti sono davvero frustrato",
        "Después de tres rechazos estoy muy frustrado", "Après trois refus, je suis vraiment frustré",
        "Po třech odmítnutích jsem fakt frustrovaný")}),
    7353: ("ru «Забор незакреплённый» — так не говорят; " + LIST, {
        "t_ru": "шатающийся, на развес", "t_uk": "розхитаний, на вагу", "t_en": "loose, unpackaged", "t_tr": "gevşek, dökme",
        "t_pl": "luźny, na sztuki", "t_fr": "branlant, en vrac", "t_cs": "uvolněný, sypaný",
        "x_ru": "Забор шатается, его надо починить", "x_uk": "Паркан розхитаний, його треба полагодити"}),
    574: ("«Ich esse gern … zum Frühstück» — шаблон Speck", {**all_x(
        "Mit Butter und Marmelade schmeckt das Brötchen am besten", "Булочка вкуснее всего с маслом и вареньем",
        "Булочка найсмачніша з маслом і джемом", "The roll tastes best with butter and jam",
        "Çörek en çok tereyağı ve reçelle güzel", "Bułka najlepiej smakuje z masłem i dżemem",
        "Il panino è più buono con burro e marmellata", "El panecillo está más rico con mantequilla y mermelada",
        "Le petit pain est meilleur avec du beurre et de la confiture", "Rohlík je nejlepší s máslem a marmeládou")}),
    7357: ("«Sein Interesse an Sport ist gering» — шаблон Interesse", {**all_x(
        "Die Gefahr ist gering", "Опасность незначительная", "Небезпека незначна", "The risk is slight", "Tehlike az",
        "Niebezpieczeństwo jest niewielkie", "Il pericolo è minimo", "El peligro es escaso", "Le danger est faible",
        "Nebezpečí je malé")}),
    2690: (EN + " («license plate» — американское)", {"t_en": "number plate, licence plate",
                                                    "x_en": "The car's number plate is dirty"}),
    7370: ("убрать пометки (coloq.)/(fam.)/(hovor.); " + LIST + " (было шесть значений)", {
        "t_ru": "затянуть, залипнуть (на фильм)", "t_uk": "затягнути, залипнути", "t_en": "to pull in, to binge",
        "t_tr": "içeri çekmek, keyifle izlemek", "t_pl": "wciągać, oglądać z przyjemnością", "t_it": "guardarsi, trascinare dentro",
        "t_es": "tragarse, meter dentro", "t_fr": "se taper, entraîner", "t_cs": "dávat si, vtáhnout"}),
    2691: ("«Ich esse gern Nüsse» — пусто", {**all_x(
        "In dem Kuchen sind Nüsse", "В этом пироге есть орехи", "У цьому пирозі є горіхи", "There are nuts in this cake",
        "Bu kekte ceviz var", "W tym cieście są orzechy", "In questa torta ci sono le noci", "Este pastel lleva nueces",
        "Il y a des noix dans ce gâteau", "V tom koláči jsou ořechy")}),
    1960: ("«Eine Tonne wiegt 1000 Kilogramm» — учебник", {
        "t_ru": "бак, тонна", "t_uk": "бак для сміття, тонна", "t_en": "bin, ton", "t_tr": "çöp konteyneri, ton",
        "t_pl": "pojemnik na śmieci, tona", "t_it": "il bidone, la tonnellata", "t_es": "el contenedor, la tonelada",
        "t_fr": "la poubelle, la tonne", "t_cs": "popelnice, tuna",
        **all_x("Bring bitte den Müll zur Tonne", "Вынеси, пожалуйста, мусор в бак", "Винеси, будь ласка, сміття в бак",
                "Take the rubbish out to the bin, please", "Lütfen çöpü çöp konteynerine götür",
                "Wynieś, proszę, śmieci do pojemnika", "Porta la spazzatura al bidone, per favore",
                "Lleva la basura al contenedor, por favor", "Descends la poubelle, s'il te plaît",
                "Vynes prosím odpadky do popelnice")}),
    1068: ("«Er hat sich am Zeh verletzt» — пусто", {**all_x(
        "Ich habe mir den Zeh am Tisch gestoßen", "Я ударился пальцем ноги о стол", "Я вдарився пальцем ноги об стіл",
        "I stubbed my toe on the table", "Ayak parmağımı masaya çarptım", "Uderzyłem się w palec u nogi o stół",
        "Ho sbattuto il dito del piede contro il tavolo", "Me he dado un golpe en el dedo del pie con la mesa",
        "Je me suis cogné l'orteil contre la table", "Praštil jsem se do prstu u nohy o stůl")}),
    1954: ("«Ich tippe schnell» — пусто", {**all_x(
        "Ich tippe auf Bayern als Meister", "Я ставлю на «Баварию» как на чемпиона", "Я ставлю на «Баварію» як на чемпіона",
        "My bet is Bayern for the title", "Şampiyon olarak Bayern'e oynuyorum", "Typuję Bayern na mistrza",
        "Scommetto sul Bayern campione", "Apuesto por el Bayern como campeón", "Je parie sur le Bayern champion",
        "Tipuju Bayern na mistra")}),
    2338: ("«Die Demonstration war friedlich …» — претерит, шаблон friedlich", {**all_x(
        "Morgen gibt es eine große Demonstration in der Stadt", "Завтра в городе большая демонстрация",
        "Завтра в місті велика демонстрація", "There's a big demonstration in town tomorrow",
        "Yarın şehirde büyük bir gösteri var", "Jutro w mieście jest duża demonstracja",
        "Domani c'è una grande manifestazione in città", "Mañana hay una gran manifestación en la ciudad",
        "Demain, il y a une grande manifestation en ville", "Zítra je ve městě velká demonstrace")}),
    2795: ("«Der Scheinwerfer des Autos leuchtet hell» — пусто", {**all_x(
        "Mach die Scheinwerfer an, es wird dunkel", "Включи фары, темнеет", "Увімкни фари, темніє",
        "Turn your headlights on, it's getting dark", "Farları aç, hava kararıyor", "Włącz reflektory, robi się ciemno",
        "Accendi i fari, sta facendo buio", "Enciende los faros, que oscurece", "Allume les phares, il fait nuit",
        "Zapni reflektory, stmívá se")}),
    1764: ("снова Projekt", {**all_x(
        "Die Planung der Hochzeit kostet viel Zeit", "Планирование свадьбы отнимает много времени",
        "Планування весілля забирає багато часу", "Planning the wedding takes a lot of time",
        "Düğün planlaması çok zaman alıyor", "Planowanie wesela zajmuje dużo czasu",
        "La pianificazione del matrimonio richiede molto tempo", "La planificación de la boda lleva mucho tiempo",
        "La planification du mariage prend beaucoup de temps", "Plánování svatby zabere spoustu času")}),
    9819: ("«Wir gehen morgen shoppen» — шаблон «gehen»", {**all_x(
        "Am Samstag war ich mit meiner Freundin shoppen", "В субботу я ходила по магазинам с подругой",
        "У суботу я ходила по магазинах із подругою", "On Saturday I went shopping with my friend",
        "Cumartesi arkadaşımla alışverişe gittim", "W sobotę byłam z przyjaciółką na zakupach",
        "Sabato sono andata a fare shopping con la mia amica", "El sábado fui de compras con mi amiga",
        "Samedi, j'ai fait du shopping avec ma copine", "V sobotu jsem byla nakupovat s kamarádkou")}),
    2608: ("«Das Klima ändert sich» — газета; второе живое значение — «атмосфера»", {**all_x(
        "In unserem Team herrscht ein gutes Klima", "В нашей команде хорошая атмосфера", "У нашій команді гарна атмосфера",
        "There's a good atmosphere in our team", "Ekibimizde iyi bir hava var", "W naszym zespole panuje dobry klimat",
        "Nel nostro team c'è un bel clima", "En nuestro equipo hay buen clima", "Dans notre équipe, il y a un bon climat",
        "V našem týmu panuje dobré klima")}),
    14527: ("«Der Prophet sagte die Zukunft voraus» — претерит", {**all_x(
        "Ich bin doch kein Prophet!", "Я же не пророк!", "Я ж не пророк!", "I'm not a prophet!", "Ben kâhin değilim ki!",
        "Nie jestem prorokiem!", "Non sono mica un profeta!", "¡No soy profeta!", "Je ne suis pas prophète!",
        "Nejsem přece prorok!")}),
    377: ("«Ich habe einen Handschuh im Bus verloren» — шаблон Mütze («… im Bus vergessen»)", {**all_x(
        "Zieh Handschuhe an, draußen ist es eiskalt", "Надень перчатки, на улице ледяной холод", "Вдягни рукавички, надворі холоднеча",
        "Put gloves on, it's freezing outside", "Eldiven tak, dışarısı buz gibi", "Załóż rękawiczki, na dworze jest lodowato",
        "Mettiti i guanti, fuori si gela", "Ponte guantes, fuera hace un frío que pela", "Mets des gants, il fait glacial dehors",
        "Vezmi si rukavice, venku je mrazivo")}),
}

REPLACE = [{"id": 10671, "by": 2451, "lang": "de", "why": "Phantasie — старое написание Fantasie"}]

SPLIT_LATER = {
    18757: ["jedesmal — старое написание; по нынешней норме «jedes Mal»"],
}
