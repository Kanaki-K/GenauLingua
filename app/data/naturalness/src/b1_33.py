"""B1, блок 33: следующие 40 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
EN = "английский пример: так не говорят"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    1623: ("«Er trägt eine Krawatte» — шаблон одежды", {"t_en": "tie", **all_x(
        "Ohne Krawatte kommst du da nicht rein", "Без галстука тебя туда не пустят", "Без краватки тебе туди не пустять",
        "They won't let you in without a tie", "Kravatsız seni içeri almazlar", "Bez krawata cię tam nie wpuszczą",
        "Senza cravatta lì non ti fanno entrare", "Sin corbata no te dejan entrar",
        "Sans cravate, on ne te laissera pas entrer", "Bez kravaty tě tam nepustí")}),
    6844: ("ru «за твою помощь» — калька", {"x_ru": "Большое спасибо за помощь"}),
    17105: (LIST, {"t_ru": "самолёт, лётчик", "t_uk": "літак, авіатор", "t_en": "plane, pilot", "t_tr": "uçak, havacı"}),
    2798: ("«Ich brauche einen Schläger» — пусто; " + LIST, {
        "t_ru": "ракетка, драчун", "t_uk": "ракетка, бешкетник", "t_en": "racket, thug", "t_tr": "raket, kabadayı",
        "t_pl": "rakieta, bandzior", "t_it": "la racchetta, la mazza", "t_es": "la raqueta, el bate", "t_cs": "raketa, pálka",
        **all_x("Für Tennis brauchst du einen Schläger", "Для тенниса тебе нужна ракетка", "Для тенісу тобі потрібна ракетка",
                "You need a racket for tennis", "Tenis için raket lazım", "Do tenisa potrzebujesz rakiety",
                "Per il tennis ti serve una racchetta", "Para el tenis necesitas una raqueta",
                "Pour le tennis, il te faut une raquette", "Na tenis potřebuješ raketu")}),
    12546: ("убрать пометку (fam.); " + LIST, {
        "t_ru": "блевать, тошнить", "t_uk": "блювати, нудити", "t_en": "to puke, to throw up", "t_tr": "kusmak, midesi bulanmak",
        "t_pl": "rzygać, wymiotować", "t_fr": "vomir, gerber"}),
    18683: (LIST + "; ru «Тем временем я уже готовлю» — так не говорят", {
        "t_ru": "тем временем, промежуток", "t_uk": "тим часом, проміжок часу", "t_en": "meantime, interim",
        "t_tr": "bu arada, ara zaman", "t_pl": "tymczasem, czas przejściowy", "t_es": "mientras tanto, el intervalo",
        "x_ru": "Тем временем я начну готовить"}),
    11678: ("«einen Wodka oder Bier» — грамматика", {**all_x(
        "Willst du einen Wodka oder ein Bier?", "Хочешь водки или пива?", "Хочеш горілки чи пива?",
        "Do you want a vodka or a beer?", "Votka mı istersin, bira mı?", "Chcesz wódkę czy piwo?",
        "Vuoi una vodka o una birra?", "¿Quieres un vodka o una cerveza?", "Tu veux une vodka ou une bière?",
        "Chceš vodku, nebo pivo?")}),
    2683: ("ru «Я работаю попутно» — так не говорят; " + LIST, {
        "t_ru": "между делом, кстати", "t_uk": "між іншим, попутно", "t_en": "by the way, on the side",
        "t_tr": "bu arada, yan olarak", "t_pl": "przy okazji, dodatkowo", "t_it": "tra l'altro, in parallelo",
        "t_es": "por cierto, aparte", "t_fr": "au passage, à côté", "t_cs": "mimochodem, bokem",
        **all_x("Nebenbei gesagt, ich habe morgen Geburtstag", "Между прочим, у меня завтра день рождения",
                "Між іншим, у мене завтра день народження", "By the way, it's my birthday tomorrow",
                "Bu arada, yarın doğum günüm", "Przy okazji, jutro mam urodziny", "Tra l'altro, domani è il mio compleanno",
                "Por cierto, mañana es mi cumpleaños", "Au passage, c'est mon anniversaire demain",
                "Mimochodem, zítra mám narozeniny")}),
    16048: (LIST, {"t_ru": "возражение, протест", "t_uk": "заперечення, протест", "t_en": "objection, appeal",
                   "t_tr": "itiraz", "t_pl": "sprzeciw, odwołanie"}),
    18168: (LIST, {"t_ru": "подушка", "t_uk": "подушка", "t_tr": "yastık, minder", "t_pl": "poduszka"}),
    17106: ("en «Can you drive up?» — не тот смысл; " + LIST, {
        "t_ru": "проехать вперёд, подъехать", "t_uk": "проїхати вперед, під'їхати", "t_en": "to pull forward, to drive up",
        "t_tr": "öne çekmek, arabayla yaklaşmak", "t_pl": "podjechać, jechać przodem",
        **all_x("Kannst du ein Stück vorfahren?", "Можешь немного проехать вперёд?", "Можеш трохи проїхати вперед?",
                "Can you pull forward a bit?", "Biraz öne çekebilir misin?", "Możesz trochę podjechać do przodu?",
                "Puoi andare un po' avanti?", "¿Puedes avanzar un poco?", "Tu peux avancer un peu?",
                "Můžeš kousek popojet?")}),
    6847: (LIST + "; en «very stable» о стуле — так не говорят", {
        "t_ru": "прочный, устойчивый", "t_uk": "міцний, стійкий", "t_en": "sturdy, stable", "t_tr": "sağlam, dengeli",
        "t_pl": "solidny, stabilny", "t_it": "stabile, robusto", "x_en": "The chair is really sturdy"}),
    6848: ("«Sie hat eine sehr sanfte Stimme» — шаблон angenehm («Er hat eine angenehme Stimme»); " + LIST, {
        "t_ru": "нежный, мягкий", "t_uk": "ніжний, м'який", "t_en": "gentle, soft", "t_tr": "yumuşak, nazik",
        "t_pl": "delikatny, łagodny", "t_it": "delicato, dolce", "t_cs": "jemný, něžný",
        **all_x("Streichle die Katze ganz sanft", "Погладь кошку очень нежно", "Погладь кицьку дуже ніжно",
                "Stroke the cat really gently", "Kediyi çok nazikçe okşa", "Pogłaszcz kota bardzo delikatnie",
                "Accarezza il gatto con delicatezza", "Acaricia al gato con suavidad", "Caresse le chat tout doucement",
                "Pohlaď kočku hodně jemně")}),
    1883: (EN + "; " + LIST, {"t_ru": "прогулка", "t_uk": "прогулянка", "x_en": "We're going for a walk"}),
    1652: ("«Deine Leistung ist gut» — пусто; " + LIST + " (было «услуга или выплата»)", {
        "t_ru": "результат, мощность", "t_uk": "результат, потужність", "t_en": "performance, achievement",
        "t_tr": "performans, başarı", "t_pl": "wynik, osiągnięcie", "t_it": "la prestazione, la potenza",
        "t_es": "el logro, el rendimiento", "t_fr": "la performance, le résultat", "t_cs": "výkon, služba",
        **all_x("Das war eine starke Leistung!", "Это был отличный результат!", "Це був чудовий результат!",
                "That was a great performance!", "Harika bir performanstı!", "To był świetny wynik!",
                "È stata una grande prestazione!", "¡Ha sido un gran logro!", "C'était une super performance!",
                "To byl skvělý výkon!")}),
    10334: (LIST + "; en «vacation» — американское", {
        "t_ru": "расслабленный, спокойный", "t_uk": "розслаблений, спокійний", "t_en": "relaxed, laid-back",
        "t_tr": "rahat, sakin", "t_pl": "zrelaksowany, wyluzowany", "t_cs": "uvolněný, klidný",
        "x_en": "After the holiday I'm completely relaxed"}),
    13943: ("«Das ist ein kluger Spruch» — пусто; убрать пометку (hovor.); " + LIST, {
        "t_ru": "поговорка, изречение", "t_uk": "приказка, вислів", "t_en": "saying, quip", "t_tr": "söz, atasözü",
        "t_pl": "powiedzenie, hasło", "t_it": "il detto, la battuta", "t_es": "el dicho, la frase",
        "t_fr": "le dicton, la remarque", "t_cs": "rčení, hláška",
        **all_x("Hast du diesen Spruch schon mal gehört?", "Ты слышал эту поговорку?", "Ти чув цю приказку?",
                "Have you heard that saying before?", "Bu sözü daha önce duydun mu?", "Słyszałeś już to powiedzenie?",
                "Hai mai sentito questo detto?", "¿Has oído alguna vez este dicho?", "Tu connais ce dicton?",
                "Slyšel jsi už to rčení?")}),
    17514: (LIST, {"t_ru": "колонка, динамик", "t_uk": "колонка, динамік", "t_en": "speaker, loudspeaker",
                   "t_tr": "hoparlör", "t_pl": "głośnik"}),
    16049: (EN + " («Grandpa» — американское); " + LIST, {
        "t_ru": "завещание", "t_uk": "заповіт", "t_en": "will", "t_tr": "vasiyet", "t_pl": "testament",
        "x_en": "Grandad has changed his will"}),
    6849: ("ru «метод для обучения» — канцелярит", {"x_ru": "Это хороший способ учиться",
                                                   "x_en": "That's a good way to learn"}),
    10335: ("«Das Essen schmeckt ekelhaft» — снова Essen; " + LIST, {
        "t_ru": "отвратительный, мерзкий", "t_uk": "огидний, гидкий", "t_en": "disgusting, gross",
        "t_tr": "iğrenç, mide bulandırıcı", "t_pl": "obrzydliwy, wstrętny",
        **all_x("Im Kühlschrank riecht es ekelhaft", "В холодильнике отвратительно пахнет", "У холодильнику огидно пахне",
                "The fridge smells disgusting", "Buzdolabı iğrenç kokuyor", "W lodówce obrzydliwie śmierdzi",
                "Il frigo ha un odore disgustoso", "La nevera huele asqueroso", "Le frigo sent dégoûtant",
                "V lednici to odporně smrdí")}),
    6851: (LIST, {"t_ru": "расколоть, взломать", "t_uk": "розколоти, зламати", "t_en": "to crack", "t_tr": "kırmak, şifreyi çözmek",
                  "t_pl": "rozłupać, złamać szyfr", "t_it": "rompere, forzare", "t_es": "partir, descifrar",
                  "t_fr": "casser, déchiffrer", "t_cs": "rozlousknout, prolomit",
                  "x_ru": "Расколешь этот орех?", "x_en": "Can you crack this nut?"}),
    12547: ("ru «Моё давление слишком высокое» — калька", {"x_ru": "У меня слишком высокое давление"}),
    6852: (EN, {"x_en": "I need to go somewhere quiet"}),
    1936: ("«Mein Sohn ist ein Teenager» — пусто; убрать пометку (fam.)", {"t_fr": "l'adolescent, l'ado", **all_x(
        "Als Teenager war ich ziemlich schwierig", "Подростком я был довольно трудным", "Підлітком я був досить важким",
        "As a teenager I was pretty difficult", "Ergenken oldukça zor biriydim", "Jako nastolatek byłem dość trudny",
        "Da adolescente ero piuttosto difficile", "De adolescente era bastante difícil", "Ado, j'étais plutôt difficile",
        "Jako teenager jsem byl dost náročný")}),
    1741: ("«Der Ofen ist heiß» — пусто; " + LIST, {
        "t_ru": "духовка, печь", "t_uk": "духовка, піч", "t_en": "oven, stove", "t_tr": "fırın, soba", "t_cs": "trouba, kamna",
        **all_x("Der Kuchen ist noch im Ofen", "Пирог ещё в духовке", "Пиріг ще в духовці", "The cake's still in the oven",
                "Kek hâlâ fırında", "Ciasto jest jeszcze w piekarniku", "La torta è ancora in forno",
                "El pastel todavía está en el horno", "Le gâteau est encore au four", "Koláč je ještě v troubě")}),
    1397: (LIST, {"t_ru": "открывать, начинать", "t_uk": "відкривати, розпочинати", "t_en": "to open, to inaugurate",
                  "t_tr": "açmak, açılışını yapmak", "t_pl": "otwierać, zakładać"}),
    2039: (LIST + " (было восемь значений)", {
        "t_ru": "переносить, задевать куда-то", "t_uk": "переносити, кудись подіти", "t_en": "to postpone, to misplace",
        "t_tr": "ertelemek, bir yere koyup kaybetmek", "t_pl": "przenosić, gdzieś położyć", "t_it": "rinviare, smarrire",
        "t_es": "aplazar, extraviar", "t_fr": "reporter, égarer", "t_cs": "přeložit, založit"}),
    6854: (LIST, {"t_ru": "встретить, столкнуться", "t_uk": "зустріти, натрапити", "t_en": "to meet, to run into",
                  "t_tr": "rastlamak, karşılaşmak", "t_pl": "spotkać, natknąć się"}),
    10336: (LIST, {"t_pl": "nieudacznik"}),
    6855: (LIST, {"t_ru": "совершить, отмечать", "t_uk": "скоїти, святкувати", "t_en": "to commit, to celebrate",
                  "t_tr": "işlemek, kutlamak", "t_pl": "popełnić, obchodzić", "t_cs": "spáchat, oslavit"}),
    6856: ("«Das Problem müssen wir sofort angehen» — планёрка; «Das geht dich nichts an» — уже у Freundchen; " + LIST, {
        "t_ru": "взяться за, касаться", "t_uk": "взятися за, стосуватися", "t_en": "to tackle, to concern",
        "t_tr": "ele almak, ilgilendirmek", "t_pl": "zabrać się za, dotyczyć", "t_it": "affrontare, riguardare",
        "t_es": "abordar, concernir", "t_fr": "s'attaquer à, concerner", "t_cs": "pustit se do, týkat se",
        **all_x("Wie wollen wir das angehen?", "Как нам взяться за это дело?", "Як нам взятися за цю справу?",
                "How are we going to tackle this?", "Bunu nasıl ele alacağız?", "Jak się za to zabierzemy?",
                "Come affrontiamo la cosa?", "¿Cómo lo abordamos?", "Comment on s'attaque à ça?",
                "Jak se do toho pustíme?")}),
    1916: (LIST + " (было семь значений)", {
        "t_ru": "толкать, удариться", "t_uk": "штовхати, ударитися", "t_en": "to push, to bump", "t_tr": "itmek, çarpmak",
        "t_pl": "popychać, uderzyć się", "t_it": "spingere, urtare", "t_es": "empujar, golpear", "t_fr": "pousser, se cogner",
        "t_cs": "strkat, narazit"}),
    10337: ("снова Konzert; " + LIST, {
        "t_ru": "с нетерпением ждущий, напряжённый", "t_uk": "зацікавлений, напружений", "t_en": "curious, tense",
        "t_tr": "meraklı, gergin", "t_pl": "ciekawy, napięty", "t_it": "curioso, teso", "t_es": "curioso, tenso",
        "t_fr": "curieux, tendu",
        **all_x("Ich bin gespannt, was er sagt", "С нетерпением жду, что он скажет", "Мені цікаво, що він скаже",
                "I'm curious to hear what he says", "Ne diyeceğini merak ediyorum", "Ciekawe, co powie",
                "Sono curioso di sentire cosa dice", "Tengo curiosidad por saber qué dice",
                "Je suis curieux de savoir ce qu'il va dire", "Jsem zvědavý, co řekne")}),
}

SPLIT_LATER = {
    2039: ["verlegen (прил.) = смущённый"],
    1916: ["auf etwas stoßen = наткнуться; anstoßen = чокнуться"],
    6856: ["das Licht geht an = свет включается"],
}
