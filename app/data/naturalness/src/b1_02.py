"""B1, блок 2: слова 41–80 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
SKEL = "пример-скелет («Er ist im Gefängnis», «Das ist unglaublich») — пусто"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    6306: ("«Die Boxer kämpfen um den Titel» — спортивные новости; " + LIST, {
        "t_ru": "бороться, драться", "t_uk": "боротися, битися", "t_en": "to fight", "t_tr": "mücadele etmek, dövüşmek",
        "t_pl": "walczyć",
        **all_x("Wir kämpfen bis zum Schluss!", "Мы будем бороться до конца!", "Ми боротимемося до кінця!",
                "We'll fight to the end!", "Sonuna kadar mücadele edeceğiz!", "Będziemy walczyć do końca!",
                "Lotteremo fino alla fine!", "¡Lucharemos hasta el final!", "On va se battre jusqu'au bout!",
                "Budeme bojovat až do konce!")}),
    12471: ("«Mein Kopf tut mir weh» — шаблон Bauch, Bein; " + LIST, {
        "t_ru": "больно", "t_uk": "боляче", "t_en": "sore, hurting", "t_tr": "acıyan, ağrıyan", "t_pl": "boleć, bolesny",
        **all_x("Tut es noch weh?", "Ещё болит?", "Ще болить?", "Does it still hurt?", "Hâlâ acıyor mu?", "Jeszcze boli?",
                "Fa ancora male?", "¿Todavía te duele?", "Ça fait encore mal?", "Ještě to bolí?")}),
    15928: (SKEL + "; " + LIST, {
        "t_ru": "тюрьма", "t_uk": "в'язниця", "t_en": "prison, jail", "t_tr": "hapishane, cezaevi", "t_pl": "więzienie",
        **all_x("Dafür kann man ins Gefängnis kommen", "За это можно попасть в тюрьму", "За це можна потрапити до в'язниці",
                "You can go to prison for that", "Bunun için hapse girilebilir", "Za to można trafić do więzienia",
                "Per questo si può finire in prigione", "Por eso puedes acabar en la cárcel",
                "On peut aller en prison pour ça", "Za to se dá jít do vězení")}),
    1391: (LIST, {"t_ru": "узнать, опытный", "t_uk": "дізнатися, досвідчений", "t_en": "to find out, experienced",
                  "t_tr": "öğrenmek, deneyimli", "t_pl": "dowiedzieć się, doświadczony",
                  "t_it": "venire a sapere, sperimentare", "t_es": "enterarse, experimentar", "t_fr": "apprendre, découvrir",
                  "t_cs": "dozvědět se, zažít"}),
    15930: ("«покончить с собой» — не перевод слова; " + LIST, {
        "t_ru": "убить, прикончить", "t_uk": "вбити, прикінчити", "t_en": "to kill, to murder", "t_tr": "öldürmek",
        "t_pl": "zabić"}),
    510: (EN, {"x_en": "He's in hospital"}),
    6312: (LIST, {"t_ru": "вещи, барахло", "t_uk": "речі, манатки", "t_en": "stuff, things", "t_tr": "eşya, zımbırtı",
                  "t_pl": "rzeczy, graty"}),
    10068: (SKEL + "; " + LIST, {
        "t_ru": "невероятный", "t_uk": "неймовірний", "t_en": "incredible, unbelievable", "t_tr": "inanılmaz",
        "t_pl": "niewiarygodny, niesamowity",
        **all_x("Es ist unglaublich, wie schnell die Zeit vergeht", "Невероятно, как быстро летит время",
                "Неймовірно, як швидко летить час", "It's incredible how fast time flies",
                "Zamanın bu kadar hızlı geçmesi inanılmaz", "To niewiarygodne, jak szybko leci czas",
                "È incredibile come passa veloce il tempo", "Es increíble lo rápido que pasa el tiempo",
                "C'est incroyable comme le temps passe vite", "Je neuvěřitelné, jak rychle čas letí")}),
    13846: ("пример почти слово в слово повторял äh («Äh, wie heißt du nochmal?»)", {**all_x(
        "Ähm, ich weiß nicht genau", "Эм, я точно не знаю", "Ем, я точно не знаю", "Um, I'm not really sure",
        "Şey, tam bilmiyorum", "Yyy, nie wiem dokładnie", "Ehm, non so bene", "Eh, no sé muy bien",
        "Euh, je ne sais pas trop", "Ehm, nevím přesně")}),
    14908: (LIST, {"t_ru": "любимый, дорогой", "t_uk": "коханий, улюбленець", "t_en": "darling, favourite",
                   "t_tr": "sevgilim, gözde", "t_pl": "kochanie, ulubieniec", "t_it": "il tesoro, il preferito",
                   "t_es": "el cariño, el favorito", "t_fr": "le chéri, le préféré", "t_cs": "miláček, oblíbenec"}),
    15933: ("«ermittelt wegen Mordes» — язык новостей и шаблон Mörder («Die Polizei …»)", {**all_x(
        "In dem Krimi geht es um einen Mord", "В этом детективе речь идёт об убийстве", "У цьому детективі йдеться про вбивство",
        "The crime novel is about a murder", "Bu polisiye bir cinayet hakkında", "Ten kryminał jest o morderstwie",
        "Il giallo parla di un omicidio", "La novela policíaca trata de un asesinato", "Le polar parle d'un meurtre",
        "Ta detektivka je o vraždě")}),
    17910: ("«fanden» — претерит, книжно", {**all_x(
        "Im Park hat man eine Leiche gefunden", "В парке нашли труп", "У парку знайшли труп",
        "A dead body has been found in the park", "Parkta bir ceset bulunmuş", "W parku znaleziono zwłoki",
        "Nel parco hanno trovato un cadavere", "Han encontrado un cadáver en el parque",
        "On a trouvé un cadavre dans le parc", "V parku našli mrtvolu")}),
    6322: ("восьмой пример про погоду; " + LIST, {
        "t_ru": "идеальный, отличный", "t_uk": "ідеальний, бездоганний", "t_en": "perfect", "t_tr": "mükemmel, kusursuz",
        "t_pl": "idealny, doskonały",
        **all_x("Dein Deutsch ist fast perfekt", "Твой немецкий почти идеальный", "Твоя німецька майже ідеальна",
                "Your German is almost perfect", "Almancan neredeyse mükemmel", "Twój niemiecki jest prawie idealny",
                "Il tuo tedesco è quasi perfetto", "Tu alemán es casi perfecto", "Ton allemand est presque parfait",
                "Tvoje němčina je skoro dokonalá")}),
    2258: (EN + " («I keep the book»); " + LIST, {
        "t_ru": "оставить себе, запомнить", "t_uk": "залишити собі, запам'ятати", "t_en": "to keep, to remember",
        "t_tr": "saklamak, aklında tutmak", "t_pl": "zatrzymać, zapamiętać", "t_it": "tenere, ricordare",
        "t_es": "quedarse con, guardar", "t_fr": "garder", "t_cs": "nechat si",
        **all_x("Das kannst du behalten", "Можешь оставить это себе", "Можеш залишити це собі", "You can keep it",
                "Bu sende kalsın", "Możesz to zatrzymać", "Puoi tenerlo", "Te lo puedes quedar", "Tu peux le garder",
                "Můžeš si to nechat")}),
    2204: ("«Ich habe großen Ärger» — пусто; " + LIST, {
        "t_ru": "неприятности, злость", "t_uk": "неприємності, злість", "t_en": "trouble, anger", "t_tr": "sorun, öfke",
        "t_pl": "kłopoty, złość", "t_it": "i guai, la rabbia", "t_es": "los problemas, el enfado",
        "t_fr": "les ennuis, la colère", "t_cs": "potíže, zlost",
        **all_x("Wenn du zu spät kommst, gibt es Ärger", "Если опоздаешь, будут неприятности", "Якщо запізнишся, будуть неприємності",
                "If you're late, there'll be trouble", "Geç kalırsan sorun çıkar", "Jak się spóźnisz, będą kłopoty",
                "Se arrivi tardi, sono guai", "Si llegas tarde, habrá problemas",
                "Si tu es en retard, il y aura des ennuis", "Jestli přijdeš pozdě, budou potíže")}),
    8740: ("«Mein Vater ist Meister …» — шаблон Kaufmann; " + LIST, {
        "t_ru": "мастер, чемпион", "t_uk": "майстер, чемпіон", "t_en": "master, champion", "t_tr": "usta, şampiyon",
        "t_pl": "mistrz", "t_it": "il maestro, il campione", "t_es": "el maestro, el campeón",
        "t_fr": "le maître, le champion", "t_cs": "mistr",
        **all_x("Bayern ist wieder deutscher Meister", "«Бавария» снова чемпион Германии", "«Баварія» знову чемпіон Німеччини",
                "Bayern are German champions again", "Bayern yine Almanya şampiyonu", "Bayern znowu jest mistrzem Niemiec",
                "Il Bayern è di nuovo campione di Germania", "El Bayern vuelve a ser campeón de Alemania",
                "Le Bayern est de nouveau champion d'Allemagne", "Bayern je zase mistrem Německa")}),
    6330: (LIST, {"t_ru": "прочь, в отъезде", "t_uk": "геть, у від'їзді", "t_en": "away, gone", "t_tr": "uzağa, gitmiş",
                  "t_pl": "precz, z dala"}),
    10076: ("«Ты очень ловкий» — пусто; en «skillful» — без контекста", {
        "t_en": "skilful, handy",
        **all_x("Sie ist sehr geschickt mit den Händen", "У неё очень ловкие руки", "У неї дуже спритні руки",
                "She's very handy", "Elleri çok becerikli", "Ma bardzo zręczne ręce", "È molto abile con le mani",
                "Es muy hábil con las manos", "Elle est très habile de ses mains", "Je velmi šikovná")}),
    2015: ("«Ich bin unterwegs» — обрывок разговора", {**all_x(
        "Ich bin schon unterwegs, in zehn Minuten bin ich da", "Я уже в пути, через десять минут буду",
        "Я вже в дорозі, за десять хвилин буду", "I'm already on my way, I'll be there in ten minutes",
        "Yoldayım, on dakikaya oradayım", "Jestem już w drodze, za dziesięć minut będę",
        "Sono già per strada, tra dieci minuti arrivo", "Ya estoy en camino, en diez minutos llego",
        "Je suis déjà en route, j'arrive dans dix minutes", "Už jsem na cestě, za deset minut jsem tam")}),
    2749: ("«Это урегулировано» — канцелярски; " + LIST, {
        "t_ru": "уладить, регулировать", "t_uk": "залагодити, регулювати", "t_en": "to sort out, to regulate",
        "t_tr": "halletmek, düzenlemek", "t_pl": "załatwić, regulować", "t_it": "sistemare, regolare",
        "t_es": "arreglar, regular", "t_fr": "régler", "t_cs": "vyřídit, regulovat",
        **all_x("Keine Sorge, das regle ich", "Не волнуйся, я это улажу", "Не хвилюйся, я це залагоджу",
                "Don't worry, I'll sort it out", "Merak etme, ben hallederim", "Spokojnie, ja to załatwię",
                "Tranquillo, sistemo tutto io", "Tranquilo, yo lo arreglo", "T'inquiète, je règle ça",
                "Neboj, já to vyřídím")}),
    6335: ("«Pass auf, da ist Gefahr» — так не говорят; " + LIST, {
        "t_ru": "опасность, риск", "t_uk": "небезпека, ризик", "t_en": "danger, risk", "t_tr": "tehlike",
        "t_pl": "niebezpieczeństwo, zagrożenie",
        **all_x("Keine Gefahr, der Hund beißt nicht", "Никакой опасности, собака не кусается",
                "Жодної небезпеки, собака не кусається", "No danger, the dog doesn't bite", "Tehlike yok, köpek ısırmaz",
                "Nie ma niebezpieczeństwa, pies nie gryzie", "Nessun pericolo, il cane non morde",
                "No hay peligro, el perro no muerde", "Pas de danger, le chien ne mord pas", "Žádné nebezpečí, pes nekouše")}),
    255: ("«Er fängt den Ball» — скелет; " + LIST, {
        "t_ru": "ловить, поймать", "t_uk": "ловити, піймати", "t_en": "to catch", "t_tr": "yakalamak", "t_pl": "łapać, złapać",
        **all_x("Die Katze hat eine Maus gefangen", "Кошка поймала мышь", "Кішка впіймала мишу", "The cat caught a mouse",
                "Kedi bir fare yakaladı", "Kot złapał mysz", "Il gatto ha preso un topo", "El gato ha atrapado un ratón",
                "Le chat a attrapé une souris", "Kočka chytila myš")}),
    6337: ("перевод — список из пяти; «крышка ящика была сломана» — книжно", {
        "t_ru": "крышка, клапан", "t_uk": "кришка, клапан", "t_en": "flap, lid", "t_tr": "kapak", "t_pl": "klapka, pokrywa",
        "t_it": "lo sportello, il coperchio", "t_es": "la tapa, la trampilla", "t_fr": "le clapet, le couvercle",
        "t_cs": "klapka, víko",
        **all_x("Die Klappe am Briefkasten klemmt", "Крышка почтового ящика заедает", "Кришка поштової скриньки заїдає",
                "The flap on the letterbox is stuck", "Posta kutusunun kapağı sıkışıyor", "Klapka skrzynki na listy się zacina",
                "Lo sportello della cassetta della posta si incastra", "La tapa del buzón se atasca",
                "Le clapet de la boîte aux lettres coince", "Klapka u schránky se zasekává")}),
    1898: (EN, {"x_en": "He keeps calling"}),
    272: ("«Er verletzt sich am Finger» — шаблон Arm; " + LIST, {
        "t_ru": "палец", "t_uk": "палець",
        **all_x("Ich habe mir in den Finger geschnitten", "Я порезал палец", "Я порізав палець", "I've cut my finger",
                "Parmağımı kestim", "Skaleczyłem się w palec", "Mi sono tagliato un dito", "Me he cortado el dedo",
                "Je me suis coupé le doigt", "Řízl jsem se do prstu")}),
    1532: ("ru «Мы едем в объезд города» — другое значение", {"x_ru": "Мы объезжаем город"}),
}

SPLIT_LATER = {}
