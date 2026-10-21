"""B1, блок 45: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    6980: ("«Der Kern des Problems ist kompliziert» — пусто; " + LIST, {
        "t_ru": "суть, ядро", "t_uk": "суть, ядро", "t_en": "core, essence", "t_tr": "öz, çekirdek", "t_pl": "sedno, rdzeń",
        "t_it": "il nocciolo, il nucleo", "t_es": "el meollo, el núcleo", "t_fr": "le cœur, le noyau", "t_cs": "jádro, podstata",
        **all_x("Das ist der Kern des Problems", "Вот в чём суть проблемы", "Ось у чому суть проблеми",
                "That's the core of the problem", "Sorunun özü bu", "To jest sedno problemu",
                "Questo è il nocciolo del problema", "Ese es el meollo del problema", "C'est le cœur du problème",
                "To je jádro problému")}),
    10406: (LIST, {"t_ru": "отношение, осанка", "t_uk": "ставлення, осанка", "t_en": "attitude, posture",
                   "t_tr": "tutum, duruş", "t_pl": "postawa, nastawienie", "t_it": "l'atteggiamento, la postura",
                   "t_es": "la actitud, la postura", "t_fr": "l'attitude, la posture", "t_cs": "postoj, držení těla"}),
    16110: ("«Während des Krieges versteckten sich …» — претерит", {**all_x(
        "Im Garten haben wir einen alten Bunker gefunden", "В саду мы нашли старый бункер", "У саду ми знайшли старий бункер",
        "We found an old bunker in the garden", "Bahçede eski bir sığınak bulduk", "W ogrodzie znaleźliśmy stary bunkier",
        "In giardino abbiamo trovato un vecchio bunker", "En el jardín encontramos un búnker viejo",
        "Dans le jardin, on a trouvé un vieux bunker", "Na zahradě jsme našli starý bunkr")}),
    1923: ("«Kinder lieben Süßigkeiten» — пусто", {**all_x(
        "Vor dem Essen gibt's keine Süßigkeiten!", "До обеда никаких сладостей!", "До обіду ніяких солодощів!",
        "No sweets before dinner!", "Yemekten önce şeker yok!", "Przed obiadem żadnych słodyczy!",
        "Niente dolci prima di mangiare!", "¡Nada de golosinas antes de comer!", "Pas de sucreries avant le repas!",
        "Před jídlem žádné sladkosti!")}),
    2628: ("«Das Holz krachte, als er darauf trat» — претерит", {**all_x(
        "Draußen hat es gerade laut gekracht", "На улице только что что-то громко треснуло", "Надворі щойно щось голосно тріснуло",
        "Something just crashed loudly outside", "Dışarıda az önce yüksek sesle bir şey gümbürdedi",
        "Na zewnątrz właśnie głośno huknęło", "Fuori qualcosa si è appena schiantato con un gran rumore",
        "Afuera algo acaba de estallar con fuerza", "Dehors, quelque chose vient d'éclater avec fracas",
        "Venku to právě hlasitě prasklo")}),
    18702: ("«Die Kürze dieser Erklärung ist wichtig» — пусто; живое — «in Kürze»", {
        "t_ru": "краткость, скоро", "t_uk": "стислість, незабаром", "t_en": "brevity, shortly", "t_tr": "kısalık, kısa süre içinde",
        "t_pl": "zwięzłość, wkrótce", "t_it": "la brevità, a breve", "t_es": "la brevedad, en breve",
        "t_fr": "la brièveté, sous peu", "t_cs": "stručnost, brzy",
        **all_x("Ich melde mich in Kürze bei Ihnen", "Я скоро с вами свяжусь", "Я незабаром з вами зв'яжуся",
                "I'll be in touch shortly", "Kısa süre içinde size haber vereceğim", "Wkrótce się do Pana odezwę",
                "Mi farò sentire a breve", "Me pondré en contacto con usted en breve", "Je vous recontacte sous peu",
                "Brzy se vám ozvu")}),
    10407: ("ru «Я не колеблюсь помочь» — калька", {**all_x(
        "Zögere nicht, mich anzurufen!", "Не медли, звони мне!", "Не вагайся — дзвони!", "Don't hesitate to call me!",
        "Beni aramaktan çekinme!", "Nie wahaj się do mnie dzwonić!", "Non esitare a chiamarmi!", "¡No dudes en llamarme!",
        "N'hésite pas à m'appeler!", "Neváhej mi zavolat!")}),
    16111: (LIST + " (было пять значений)", {
        "t_ru": "болельщик, прицеп", "t_uk": "фанат, причіп", "t_en": "fan, trailer", "t_tr": "taraftar, römork",
        "t_pl": "kibic, przyczepa", "t_it": "il tifoso, il rimorchio", "t_es": "el aficionado, el remolque",
        "t_fr": "le supporter, la remorque", "t_cs": "fanoušek, přívěs",
        "x_ru": "Болельщики футбольного клуба очень преданные", "x_en": "The club's fans are very loyal"}),
    13508: (EN + " («fourth grade» — американское)", {"x_en": "He's in year four"}),
    18188: ("ru «до 6-го этажа» — не совпадает с de; шаблон Aufzug, Lift", {**all_x(
        "Ich bin im Fahrstuhl stecken geblieben", "Я застрял в лифте", "Я застряг у ліфті", "I got stuck in the lift",
        "Asansörde mahsur kaldım", "Utknąłem w windzie", "Sono rimasto bloccato in ascensore",
        "Me he quedado atrapado en el ascensor", "Je suis resté coincé dans l'ascenseur", "Zasekl jsem se ve výtahu")}),
    13979: ("«Du solltest mich nicht anlügen» — книжно", {**all_x(
        "Lüg mich nicht an!", "Не ври мне!", "Не бреши мені!", "Don't lie to me!", "Bana yalan söyleme!", "Nie okłamuj mnie!",
        "Non mentirmi!", "¡No me mientas!", "Ne me mens pas!", "Nelži mi!")}),
    6989: (EN + " («tire» — американское)", {"x_en": "The tyre is flat"}),
    13980: ("«Das Echo der Musik hallt durch die Berge» — поэзия", {**all_x(
        "Ruf mal laut, hier gibt es ein Echo!", "Крикни погромче, здесь есть эхо!", "Крикни голосно, тут є луна!",
        "Shout loud, there's an echo here!", "Yüksek sesle bağır, burada yankı var!", "Krzyknij głośno, tu jest echo!",
        "Grida forte, qui c'è l'eco!", "¡Grita fuerte, aquí hay eco!", "Crie fort, il y a de l'écho ici!",
        "Zakřič nahlas, je tu ozvěna!")}),
    12572: ("«Ich nehme jeden Morgen eine Pille …» — шаблон Tablette («Ich nehme jeden Morgen eine Tablette»)", {**all_x(
        "Nimmst du die Pille?", "Ты пьёшь противозачаточные таблетки?", "Ти п'єш протизаплідні таблетки?",
        "Are you on the pill?", "Doğum kontrol hapı kullanıyor musun?", "Bierzesz pigułkę?", "Prendi la pillola?",
        "¿Tomas la píldora?", "Tu prends la pilule?", "Bereš pilulky?")}),
    2967: ("«Ich versichere mein Auto» — пусто; живое — «уверяю»", {
        "t_ru": "уверять, страховать", "t_uk": "запевняти, страхувати", "t_en": "to assure, to insure",
        "t_tr": "temin etmek, sigortalamak", "t_pl": "zapewniać, ubezpieczać",
        **all_x("Ich versichere dir, das stimmt", "Уверяю тебя, это правда", "Запевняю тебе, це правда",
                "I assure you, it's true", "Sana temin ederim, bu doğru", "Zapewniam cię, że to prawda",
                "Ti assicuro che è vero", "Te aseguro que es verdad", "Je t'assure, c'est vrai", "Ujišťuji tě, že je to pravda")}),
    6993: ("ru «Ты должен ухватиться» — калька", {"x_ru": "Надо хвататься за этот шанс", "x_en": "You've got to seize the chance"}),
    11693: ("«Das Mittagessen war eine leckere Mahlzeit» — масло масляное; живое — «Mahlzeit!»", {**all_x(
        "Mahlzeit!", "Приятного аппетита!", "Смачного!", "Enjoy your meal!", "Afiyet olsun!", "Smacznego!",
        "Buon appetito!", "¡Buen provecho!", "Bon appétit!", "Dobrou chuť!")}),
    2417: ("«Es gab ein starkes Erdbeben» — шаблон «Es gab …»", {**all_x(
        "Bei uns gibt es fast nie Erdbeben", "У нас почти не бывает землетрясений", "У нас майже не буває землетрусів",
        "We almost never get earthquakes here", "Bizde neredeyse hiç deprem olmaz", "U nas prawie nigdy nie ma trzęsień ziemi",
        "Da noi non ci sono quasi mai terremoti", "Aquí casi nunca hay terremotos",
        "Chez nous, il n'y a presque jamais de tremblements de terre", "U nás skoro nikdy není zemětřesení")}),
    10411: ("«Sie war eine gnädige Königin …» — претерит, сказка", {**all_x(
        "Sei nicht so streng, sei gnädig mit ihm", "Не будь так строг, будь снисходительнее к нему",
        "Не будь таким суворим, будь до нього поблажливим", "Don't be so strict, be lenient with him",
        "Bu kadar sert olma, ona karşı müsamahakâr ol", "Nie bądź taki surowy, bądź dla niego pobłażliwy",
        "Non essere così severo, sii benevolo con lui", "No seas tan estricto, sé benévolo con él",
        "Ne sois pas si sévère, sois bienveillant avec lui", "Nebuď tak přísný, buď k němu shovívavý")}),
}

REPLACE = [
    {"id": 6987, "by": 13481, "lang": "de", "why": "selbe — часть слова derselbe/dasselbe"},
    {"id": 6991, "by": 7092, "lang": "de", "why": "abgeschnitten — причастие от abschneiden"},
]

SPLIT_LATER = {}
