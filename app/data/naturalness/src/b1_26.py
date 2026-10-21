"""B1, блок 26: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    6742: ("«Wir erheben uns vom Stuhl» — книжно (B2-ряд 7318 склеен с этим); " + LIST, {
        "t_ru": "поднимать, взимать", "t_uk": "піднімати, стягувати", "t_en": "to raise, to charge",
        "t_tr": "kaldırmak, tahsil etmek", "t_pl": "podnosić, pobierać", "t_it": "alzare, riscuotere",
        "t_es": "levantar, cobrar", "t_fr": "lever, percevoir", "t_cs": "zvednout, vybírat",
        **all_x("Die Stadt erhebt jetzt Gebühren fürs Parken", "Город теперь взимает плату за парковку",
                "Місто тепер стягує плату за паркування", "The city now charges a fee for parking",
                "Belediye artık otopark ücreti tahsil ediyor", "Miasto pobiera teraz opłaty za parkowanie",
                "Il comune ora riscuote una tassa sul parcheggio", "El ayuntamiento ahora cobra por aparcar",
                "La ville perçoit maintenant une taxe de stationnement", "Město teď vybírá poplatky za parkování")}),
    17775: (LIST, {"t_ru": "торговля, сделка", "t_uk": "торгівля, угода", "t_tr": "ticaret, anlaşma",
                   "t_pl": "handel, interes", "t_en": "trade, deal"}),
    14415: ("«Wir gehen zum Friedhof» — шаблон «gehen»", {**all_x(
        "Meine Oma liegt auf diesem Friedhof", "Моя бабушка похоронена на этом кладбище",
        "Моя бабуся похована на цьому кладовищі", "My gran is buried in this cemetery", "Anneannem bu mezarlıkta yatıyor",
        "Moja babcia leży na tym cmentarzu", "Mia nonna è sepolta in questo cimitero",
        "Mi abuela está enterrada en este cementerio", "Ma grand-mère est enterrée dans ce cimetière",
        "Babička leží na tomhle hřbitově")}),
    16025: ("«Das ist völlig illegal» — пусто; " + LIST, {
        "t_ru": "незаконный, нелегальный", "t_tr": "yasa dışı, kaçak",
        **all_x("Er arbeitet illegal auf dem Bau", "Он нелегально работает на стройке", "Він нелегально працює на будові",
                "He works illegally on a building site", "İnşaatta kaçak çalışıyor", "Pracuje nielegalnie na budowie",
                "Lavora illegalmente in un cantiere", "Trabaja ilegalmente en la obra",
                "Il travaille illégalement sur un chantier", "Pracuje nelegálně na stavbě")}),
    8801: (LIST, {"t_ru": "боец, борец", "t_uk": "боєць, борець", "t_en": "fighter, warrior",
                  "t_tr": "savaşçı, mücadeleci", "t_pl": "wojownik, bojownik"}),
    6743: ("ru «держи расстояние в один метр от меня» — калька; en «meter»; " + LIST, {
        "t_ru": "расстояние, интервал", "t_uk": "відстань, інтервал", "t_en": "distance, gap", "t_tr": "mesafe, ara",
        "t_pl": "odległość, odstęp", "x_ru": "Держись, пожалуйста, от меня на расстоянии метра",
        "x_uk": "Тримайся, будь ласка, від мене на відстані метра", "x_en": "Please keep a metre's distance from me"}),
    17089: ("«Er hat einen Führerschein» — пусто; убрать пометку (hovor.)", {
        "t_en": "driving licence", "t_cs": "řidičák, řidičský průkaz",
        **all_x("Seit wann hast du den Führerschein?", "Давно у тебя права?", "Давно в тебе права?",
                "How long have you had your driving licence?", "Ne zamandır ehliyetin var?", "Od kiedy masz prawo jazdy?",
                "Da quanto hai la patente?", "¿Desde cuándo tienes el carné de conducir?", "Tu as ton permis depuis quand?",
                "Odkdy máš řidičák?")}),
    1913: ("ru «Я должен платить» — калька", {"x_ru": "Мне надо платить налоги", "x_uk": "Мені треба платити податки"}),
    6745: ("«An einem bestimmten Tag werde ich zurückkommen» — так не говорят; «наверняка» — у ряда A1 (103)", {
        "t_ru": "определённый, конкретный", "t_uk": "певний, конкретний", "t_en": "certain, particular",
        "t_tr": "belirli, belli", "t_pl": "określony, konkretny", "t_it": "determinato, preciso",
        "t_es": "determinado, concreto", "t_fr": "précis, déterminé", "t_cs": "určitý, konkrétní",
        **all_x("Suchst du etwas Bestimmtes?", "Ты ищешь что-то определённое?", "Ти шукаєш щось певне?",
                "Are you looking for anything in particular?", "Belirli bir şey mi arıyorsun?",
                "Szukasz czegoś określonego?", "Cerchi qualcosa di preciso?", "¿Buscas algo en concreto?",
                "Tu cherches quelque chose de précis?", "Hledáš něco určitého?")}),
    8802: ("«Sie ist eine bekannte Schauspielerin» — пусто", {"t_tr": "aktris, oyuncu", **all_x(
        "Sie will unbedingt Schauspielerin werden", "Она очень хочет стать актрисой", "Вона дуже хоче стати акторкою",
        "She's dead set on becoming an actress", "Mutlaka oyuncu olmak istiyor", "Bardzo chce zostać aktorką",
        "Vuole a tutti i costi fare l'attrice", "Quiere ser actriz a toda costa", "Elle veut absolument devenir actrice",
        "Chce se za každou cenu stát herečkou")}),
    17090: (LIST, {
        "t_ru": "заблудиться (за рулём), поступать", "t_uk": "заблукати (за кермом), діяти",
        "t_en": "to get lost (driving), to proceed", "t_tr": "yolunu kaybetmek, hareket etmek",
        "t_pl": "zabłądzić, postąpić", "x_en": "We got completely lost on the way here"}),
    1919: ("«Die Strecke ist lang» — пусто; " + LIST, {
        "t_ru": "участок, маршрут", "t_uk": "ділянка, маршрут", "t_en": "route, stretch", "t_tr": "güzergâh, yol parçası",
        "t_pl": "trasa, odcinek", "t_it": "il percorso, il tratto", "t_es": "el trayecto, el tramo",
        "t_fr": "le trajet, le tronçon", "t_cs": "trasa, úsek",
        **all_x("Auf dieser Strecke gibt es oft Stau", "На этом участке часто пробки", "На цій ділянці часто бувають затори",
                "There are often traffic jams on this stretch", "Bu yol parçasında sık sık trafik sıkışıklığı oluyor",
                "Na tym odcinku często są korki", "Su questo tratto c'è spesso traffico", "En este tramo suele haber atascos",
                "Sur ce tronçon, il y a souvent des bouchons", "Na tomhle úseku bývají často zácpy")}),
    10293: ("«verlor er das Bewusstsein» — претерит", {
        "t_it": "la coscienza, la conoscenza", "t_fr": "la conscience, la connaissance",
        **all_x("Nach dem Unfall hat er das Bewusstsein verloren", "После аварии он потерял сознание",
                "Після аварії він втратив свідомість", "He lost consciousness after the accident",
                "Kazadan sonra bilincini kaybetti", "Po wypadku stracił przytomność",
                "Dopo l'incidente ha perso conoscenza", "Después del accidente perdió el conocimiento",
                "Après l'accident, il a perdu connaissance", "Po nehodě ztratil vědomí")}),
    13489: (LIST, {"t_ru": "та, которая", "t_uk": "та, яка", "t_en": "the one", "t_tr": "o kişi", "t_pl": "ta, która"}),
    6747: ("«Er öffnete sachte die Tür» — претерит; " + LIST, {
        "t_ru": "тихонько, осторожно", "t_uk": "тихенько, обережно", "t_en": "gently, softly", "t_tr": "usulca, yavaşça",
        "t_pl": "delikatnie, ostrożnie", "t_it": "piano, delicatamente", "t_es": "despacio, suavemente",
        "t_cs": "jemně, opatrně",
        **all_x("Mach die Tür sachte zu, das Baby schläft", "Закрой дверь тихонько, малыш спит",
                "Зачини тихенько двері, малюк спить", "Close the door gently, the baby's asleep",
                "Kapıyı usulca kapat, bebek uyuyor", "Zamknij delikatnie drzwi, dziecko śpi",
                "Chiudi piano la porta, il bambino dorme", "Cierra la puerta despacio, que el bebé duerme",
                "Ferme doucement la porte, le bébé dort", "Zavři jemně dveře, mimino spí")}),
    17503: (LIST, {"t_ru": "определить местоположение, обнаружить", "t_uk": "визначити місцезнаходження, виявити",
                   "t_en": "to locate, to track down", "t_tr": "yerini tespit etmek, izini sürmek",
                   "t_pl": "zlokalizować, namierzyć"}),
    6748: (LIST, {"t_ru": "вернуть, отнести обратно", "t_uk": "повернути, віднести назад",
                  "t_en": "to bring back, to take back", "t_tr": "geri getirmek, iade etmek", "t_pl": "oddać, zwrócić"}),
    6749: (LIST, {"t_ru": "выход, решение", "t_uk": "вихід, рішення", "t_tr": "çıkış yolu, çözüm",
                  "t_pl": "wyjście, rozwiązanie"}),
    6750: ("«In dieser Zone ist das Parken verboten» — табличка; " + LIST, {
        "t_ru": "зона, участок", "t_uk": "зона, ділянка", "t_en": "zone, area", "t_tr": "bölge, alan",
        "t_pl": "strefa, obszar",
        **all_x("Für die Fahrt brauchst du ein Ticket für zwei Zonen", "Для этой поездки нужен билет на две зоны",
                "Для цієї поїздки потрібен квиток на дві зони", "You need a two-zone ticket for this journey",
                "Bu yolculuk için iki bölgelik bilet lazım", "Na ten przejazd potrzebujesz biletu na dwie strefy",
                "Per questo viaggio ti serve un biglietto per due zone", "Para este viaje necesitas un billete de dos zonas",
                "Pour ce trajet, il te faut un ticket deux zones", "Na tuhle cestu potřebuješ jízdenku na dvě zóny")}),
    6751: ("«Wir müssen die Lampe ersetzen» — так не говорят (Birne wechseln); " + LIST, {
        "t_ru": "заменять, возмещать", "t_uk": "замінювати, відшкодовувати", "t_en": "to replace, to compensate",
        "t_tr": "değiştirmek, yerini tutmak", "t_pl": "zastąpić, wymienić", "t_it": "sostituire, risarcire",
        "t_es": "sustituir, reemplazar",
        **all_x("Kann man den Akku selbst ersetzen?", "Можно самому заменить аккумулятор?",
                "Чи можна самому замінити акумулятор?", "Can you replace the battery yourself?",
                "Pili kendin değiştirebilir misin?", "Czy można samemu wymienić baterię?",
                "Si può sostituire la batteria da soli?", "¿Se puede sustituir la batería uno mismo?",
                "On peut remplacer la batterie soi-même?", "Dá se baterie vyměnit sám?")}),
    14417: (LIST, {"t_ru": "драма, пьеса", "t_uk": "драма, п'єса", "t_en": "drama, fuss", "t_tr": "drama, facia",
                   "t_pl": "dramat, sztuka", "x_en": "All this drama with my ex is getting on my nerves"}),
    13930: (LIST, {"t_ru": "так сказать, можно сказать", "t_uk": "так би мовити, можна сказати",
                   "t_en": "so to speak, as it were", "t_tr": "tabiri caizse, bir bakıma", "t_pl": "że tak powiem, poniekąd"}),
    2569: ("ru «идём через холм» — так не говорят; " + LIST, {
        "t_ru": "холм, пригорок", "t_uk": "пагорб, горб", "t_en": "hill", "t_tr": "tepe", "t_pl": "wzgórze, pagórek",
        **all_x("Hinter dem Hügel liegt unser Dorf", "За холмом наша деревня", "За пагорбом наше село",
                "Our village is just over the hill", "Köyümüz tepenin arkasında", "Za wzgórzem jest nasza wieś",
                "Il nostro paese è dietro la collina", "Nuestro pueblo está detrás de la colina",
                "Notre village est derrière la colline", "Za kopcem je naše vesnice")}),
    1197: (LIST, {"t_ru": "вид, перспектива", "t_uk": "краєвид, перспектива", "t_en": "view, prospect",
                  "t_tr": "manzara, beklenti", "t_pl": "widok, perspektywa"}),
    2588: (LIST, {"t_ru": "годами, много лет", "t_uk": "роками, багато років", "t_en": "for years", "t_tr": "yıllarca",
                  "t_pl": "latami, przez lata"}),
    14418: ("pl «próbować» — это «пробовать», не «репетировать»", {
        "t_ru": "репетировать", "t_uk": "репетирувати", "t_en": "to rehearse", "t_pl": "mieć próbę, ćwiczyć"}),
    16027: ("«Der König saß auf seinem goldenen Thron» — претерит, сказка", {**all_x(
        "Charles ist 2022 auf den Thron gekommen", "Карл взошёл на трон в 2022 году", "Чарльз зійшов на трон у 2022 році",
        "Charles came to the throne in 2022", "Charles 2022'de tahta çıktı", "Karol wstąpił na tron w 2022 roku",
        "Carlo è salito al trono nel 2022", "Carlos subió al trono en 2022", "Charles est monté sur le trône en 2022",
        "Karel nastoupil na trůn v roce 2022")}),
    18676: (LIST, {"t_ru": "настоящее, присутствие", "t_uk": "теперішнє, присутність", "t_en": "present, presence",
                   "t_tr": "şimdiki zaman, hazır bulunma", "t_pl": "teraźniejszość, obecność"}),
    14987: ("«einen Liebhaber neben ihrem Mann» — так не говорят; " + LIST, {
        "t_ru": "любитель, любовник", "t_uk": "любитель, коханець", "t_en": "lover, enthusiast", "t_tr": "meraklı, sevgili",
        "t_pl": "miłośnik, kochanek", "t_it": "l'appassionato, l'amante", "t_es": "el aficionado, el amante",
        "t_fr": "l'amateur, l'amant", "t_cs": "milovník, milenec",
        **all_x("Er ist ein großer Liebhaber von Jazz", "Он большой любитель джаза", "Він великий любитель джазу",
                "He's a great jazz lover", "Büyük bir caz meraklısı", "Jest wielkim miłośnikiem jazzu",
                "È un grande appassionato di jazz", "Es un gran aficionado al jazz", "C'est un grand amateur de jazz",
                "Je velký milovník jazzu")}),
    10294: ("«Das war ein großer Irrtum von mir» — шаблон Versehen («Das war ein Versehen von mir»)", {**all_x(
        "Da bist du im Irrtum", "Тут ты заблуждаешься", "Тут ти помиляєшся", "You're mistaken there", "Orada yanılıyorsun",
        "Tu jesteś w błędzie", "Qui ti sbagli", "Ahí estás en un error", "Là, tu fais erreur", "V tom se mýlíš")}),
    606: ("«Das ist ein gutes Modell» — пусто; " + LIST, {
        "t_ru": "модель, макет", "t_uk": "модель, макет", "t_en": "model, design", "t_tr": "model, maket",
        "t_pl": "model, makieta",
        **all_x("Das Auto ist ein älteres Modell", "Это машина старой модели", "Це авто старої моделі",
                "The car is an older model", "Araba eski bir model", "To auto to starszy model",
                "La macchina è un modello vecchio", "El coche es un modelo antiguo", "La voiture est un modèle ancien",
                "To auto je starší model")}),
    17504: ("«Das Raumschiff landete mitten in Berlin» — претерит, фантастика", {**all_x(
        "Mein Sohn baut aus Lego ein Raumschiff", "Мой сын строит из лего космический корабль",
        "Мій син будує з лего космічний корабель", "My son is building a spaceship out of Lego",
        "Oğlum Lego'dan uzay gemisi yapıyor", "Mój syn buduje z klocków Lego statek kosmiczny",
        "Mio figlio sta costruendo un'astronave con i Lego", "Mi hijo está construyendo una nave espacial con Lego",
        "Mon fils construit un vaisseau spatial en Lego", "Syn staví z lega vesmírnou loď")}),
    1836: ("«Sie trägt schönen Schmuck» — шаблон одежды; " + LIST, {
        "t_ru": "украшения, драгоценности", "t_uk": "прикраси, коштовності", "t_en": "jewellery", "t_tr": "takı, mücevher",
        "t_pl": "biżuteria, ozdoby",
        **all_x("Den Schmuck hat sie von ihrer Oma geerbt", "Эти украшения ей достались от бабушки",
                "Ці прикраси вона успадкувала від бабусі", "She inherited the jewellery from her gran",
                "Takıları anneannesinden miras kaldı", "Biżuterię odziedziczyła po babci",
                "I gioielli li ha ereditati dalla nonna", "Las joyas las heredó de su abuela",
                "Elle a hérité les bijoux de sa grand-mère", "Šperky zdědila po babičce")}),
    924: ("«Der Teppich ist weich» — пусто", {"t_ru": "ковёр", "t_pl": "dywan", **all_x(
        "Der Hund liegt am liebsten auf dem Teppich", "Собака больше всего любит лежать на ковре",
        "Собака найбільше любить лежати на килимі", "The dog likes lying on the rug best",
        "Köpek en çok halının üstünde yatmayı seviyor", "Pies najbardziej lubi leżeć na dywanie",
        "Al cane piace stare sdraiato sul tappeto", "Al perro le encanta tumbarse en la alfombra",
        "Le chien adore se coucher sur le tapis", "Pes nejradši leží na koberci")}),
    10295: ("ru «действительно отвратительная на вкус» — калька; снова Essen; " + LIST, {
        "t_ru": "отвратительный, противный", "t_uk": "огидний, гидкий", "t_en": "disgusting, revolting",
        "t_tr": "iğrenç, mide bulandırıcı", "t_pl": "obrzydliwy, wstrętny",
        **all_x("Hör auf, das ist widerlich!", "Прекрати, это отвратительно!", "Припини, це огидно!",
                "Stop it, that's disgusting!", "Kes şunu, iğrenç!", "Przestań, to obrzydliwe!", "Smettila, è disgustoso!",
                "¡Para, es asqueroso!", "Arrête, c'est dégoûtant!", "Přestaň, to je odporné!")}),
    13932: (LIST, {"t_ru": "дневник", "t_tr": "günlük", "t_pl": "pamiętnik"}),
}

REPLACE = [{"id": 18674, "by": 328, "lang": "de", "why": "soeben — книжный вариант gerade («только что»)"}]

SPLIT_LATER = {
    17090: ["verfahren = поступать (Wie wollen wir verfahren?); das Verfahren = процедура"],
}
