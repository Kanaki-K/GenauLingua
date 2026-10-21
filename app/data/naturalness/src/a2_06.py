"""A2, блок 6: слова 201–240 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
TWO = "в строке два разных слова — оставлено главное, второе — отдельной строкой (блок деления)"
EN = "английский пример: так не говорят"
NEAR = "пример повторял пример другого слова — у каждого свой"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    14923: ("uk «торти» — Kuchen здесь «пироги»", {"t_ru": "тётя", "x_uk": "Моя тітка пече смачні пироги"}),
    10095: (LIST, {"t_ru": "кислый, злой", "t_uk": "кислий, злий", "t_en": "sour, annoyed", "t_tr": "ekşi, kızgın",
                   "t_pl": "kwaśny, zły", "t_it": "acido, arrabbiato", "t_es": "ácido, enfadado", "t_fr": "acide, fâché",
                   "t_cs": "kyselý, naštvaný"}),
    784: (LIST + "; «Это досадно» — книжно", {"t_ru": "жаль, жалко", "t_uk": "шкода", "t_en": "a pity, a shame",
                                             "t_tr": "yazık", "t_pl": "szkoda", "x_ru": "Жаль", "x_uk": "Шкода"}),
    2750: ("«Die Regierung tagt» — язык новостей", {
        "t_ru": "правительство", "t_uk": "уряд", "t_en": "government", "t_tr": "hükümet", "t_pl": "rząd",
        **all_x("Die neue Regierung hat viel zu tun", "У нового правительства много работы", "У нового уряду багато роботи",
                "The new government has a lot to do", "Yeni hükümetin yapacak çok işi var", "Nowy rząd ma dużo pracy",
                "Il nuovo governo ha molto da fare", "El nuevo gobierno tiene mucho trabajo",
                "Le nouveau gouvernement a beaucoup à faire", "Nová vláda má hodně práce")}),
    1965: (LIST, {"t_ru": "грустный, печальный", "t_uk": "сумний", "t_en": "sad", "t_tr": "üzgün", "t_pl": "smutny"}),
    1720: (LIST + "; «дело в том, что я болен» — книжно", {
        "t_ru": "ведь, а именно", "t_uk": "адже, а саме", "t_en": "you see, namely", "t_tr": "çünkü, yani",
        "t_pl": "bo, mianowicie", "t_it": "perché, cioè", "t_es": "es que, o sea", "t_fr": "en fait, à savoir",
        "t_cs": "totiž", "x_ru": "Я не могу, я ведь болею"}),
    501: ("«Bitte nimm Kontakt auf» — канцелярски", {
        "t_ru": "контакт, связь", "t_uk": "контакт, зв'язок", "t_en": "contact, touch", "t_tr": "iletişim, temas",
        "t_pl": "kontakt",
        **all_x("Wir bleiben in Kontakt!", "Будем на связи!", "Будьмо на зв'язку!", "Let's stay in touch!",
                "İletişimde kalalım!", "Bądźmy w kontakcie!", "Restiamo in contatto!", "¡Seguimos en contacto!",
                "On reste en contact!", "Zůstaneme v kontaktu!")}),
    318: (LIST + "; «Das Café liegt mir gegenüber» — неживо", {
        "t_ru": "напротив", "t_uk": "навпроти", "t_en": "opposite", "t_tr": "karşısında", "t_pl": "naprzeciwko",
        "t_it": "di fronte a", "t_es": "enfrente de", "t_fr": "en face de", "t_cs": "naproti",
        **all_x("Die Apotheke ist gegenüber vom Bahnhof", "Аптека напротив вокзала", "Аптека навпроти вокзалу",
                "The pharmacy is opposite the station", "Eczane istasyonun karşısında", "Apteka jest naprzeciwko dworca",
                "La farmacia è di fronte alla stazione", "La farmacia está enfrente de la estación",
                "La pharmacie est en face de la gare", "Lékárna je naproti nádraží")}),
    1475: ("порча знаний: «суд» и «блюдо» — два слова в одной строке; для A2 — «блюдо», суд — своя строка", {
        "t_ru": "блюдо", "t_uk": "страва", "t_en": "dish", "t_tr": "yemek", "t_pl": "danie, potrawa",
        "t_it": "il piatto", "t_es": "el plato", "t_fr": "le plat", "t_cs": "jídlo, pokrm",
        **all_x("Welches Gericht empfiehlst du?", "Какое блюдо ты посоветуешь?", "Яку страву ти порадиш?",
                "Which dish would you recommend?", "Hangi yemeği önerirsin?", "Jakie danie polecasz?",
                "Quale piatto mi consigli?", "¿Qué plato me recomiendas?", "Quel plat tu me conseilles?",
                "Jaké jídlo doporučuješ?")}),
    10102: (LIST, {"t_ru": "смешной, остроумный", "t_uk": "смішний, дотепний", "t_en": "funny, witty",
                   "t_tr": "komik, esprili", "t_pl": "zabawny, dowcipny"}),
    1989: (LIST, {"t_ru": "кстати", "t_uk": "до речі", "t_en": "by the way", "t_tr": "bu arada",
                  "t_pl": "przy okazji, nawiasem mówiąc"}),
    440: (NEAR + " (Buch: «… ein interessantes Buch»)", {
        "t_ru": "интересный", "t_uk": "цікавий", "t_tr": "ilginç",
        **all_x("Das klingt interessant!", "Звучит интересно!", "Звучить цікаво!", "That sounds interesting!",
                "Kulağa ilginç geliyor!", "Brzmi ciekawie!", "Sembra interessante!", "¡Suena interesante!",
                "Ça a l'air intéressant!", "To zní zajímavě!")}),
    104: (LIST + "; «наносит визит» — книжно", {
        "t_ru": "визит, гости", "t_uk": "візит, гості", "t_en": "visit, guests", "t_tr": "ziyaret, misafir",
        "t_pl": "wizyta, goście",
        **all_x("Wir bekommen heute Besuch", "Сегодня к нам придут гости", "Сьогодні до нас прийдуть гості",
                "We're having guests today", "Bugün misafirimiz gelecek", "Dziś przyjdą do nas goście",
                "Oggi abbiamo ospiti", "Hoy tenemos visita", "Aujourd'hui, on a de la visite", "Dnes k nám přijde návštěva")}),
    15944: (LIST, {"t_ru": "общество, компания", "t_uk": "суспільство, товариство", "t_en": "society, company",
                   "t_tr": "toplum", "t_pl": "społeczeństwo, towarzystwo"}),
    1665: ("«похоть» — неуместно и не A2-значение; " + LIST, {
        "t_ru": "желание, охота", "t_uk": "бажання, охота", "t_en": "desire", "t_tr": "istek, heves",
        "t_pl": "ochota, chęć", "t_it": "la voglia", "t_es": "las ganas", "t_fr": "l'envie", "t_cs": "chuť"}),
    1726: ("tr «Heyecanlıyım» — «я взволнован радостно», нервничать — «gerginim»", {
        "x_tr": "Gerginim", "x_en": "I'm nervous"}),
    1394: (LIST, {"t_ru": "получать, сохранять", "t_uk": "отримувати, зберігати", "t_en": "to receive, to preserve",
                  "t_tr": "almak", "t_pl": "otrzymywać"}),
    6382: (LIST + "; «Мы делим еду» — калька", {
        "t_ru": "делить, делиться", "t_uk": "ділити, ділитися", "t_en": "to share, to divide", "t_tr": "paylaşmak, bölmek",
        "t_pl": "dzielić, dzielić się", "x_ru": "Мы делимся едой", "x_uk": "Ми ділимося їжею"}),
    435: (EN, {"x_en": "We're going to an island"}),
    2160: (LIST, {"t_ru": "однако, правда", "t_uk": "проте, щоправда", "t_en": "however, though",
                  "t_tr": "ancak, gerçi", "t_pl": "jednak, wprawdzie"}),
    15379: ("«везение» — только в идиоме «Schwein haben»", {"t_ru": "свинья, свинина", "t_uk": "свиня, свинина",
                                                            "t_en": "pig, pork", "t_tr": "domuz"}),
    1530: (NEAR + " (rein: «Komm rein…»)", {
        "t_ru": "внутрь, сюда", "t_uk": "усередину, сюди", "t_en": "in, come in", "t_tr": "içeri", "t_pl": "do środka",
        **all_x("Wer klopft? — Herein!", "Кто стучит? — Войдите!", "Хто стукає? — Заходьте!",
                "Who's knocking? — Come in!", "Kim kapıyı çalıyor? — Girin!", "Kto puka? — Proszę wejść!",
                "Chi bussa? — Avanti!", "¿Quién llama? — ¡Adelante!", "Qui frappe? — Entrez!", "Kdo klepe? — Dále!")}),
    1575: (NEAR + " (kaputt — «… ist kaputt»); " + LIST, {
        "t_ru": "фотоаппарат, камера", "t_uk": "фотоапарат, камера", "t_tr": "fotoğraf makinesi, kamera",
        "t_pl": "aparat, kamera", "t_it": "la macchina fotografica, la videocamera", "t_cs": "fotoaparát",
        **all_x("Hast du deine Kamera dabei?", "Ты взял с собой фотоаппарат?", "Ти взяв із собою фотоапарат?",
                "Have you got your camera with you?", "Fotoğraf makineni yanına aldın mı?", "Masz przy sobie aparat?",
                "Hai portato la macchina fotografica?", "¿Llevas la cámara?", "Tu as ton appareil photo?",
                "Máš s sebou fotoaparát?")}),
    15380: (NEAR + " (Herbst: «… gehen wir gern in den Wald» — внесено мной)", {**all_x(
        "Im Wald ist es schön ruhig", "В лесу так тихо", "У лісі так тихо", "It's nice and quiet in the forest",
        "Ormanda çok sakin", "W lesie jest cudownie cicho", "Nel bosco c'è una bella quiete",
        "En el bosque hay mucha tranquilidad", "Dans la forêt, c'est bien calme", "V lese je krásně klid")}),
    322: (NEAR + " (zusammen: «Wir essen zusammen»)", {
        "t_ru": "вместе, общий", "t_uk": "разом, спільний", "t_en": "together, shared", "t_tr": "birlikte, ortak",
        "t_pl": "razem, wspólny",
        **all_x("Wir haben viele gemeinsame Freunde", "У нас много общих друзей", "У нас багато спільних друзів",
                "We have a lot of friends in common", "Birçok ortak arkadaşımız var", "Mamy wielu wspólnych przyjaciół",
                "Abbiamo tanti amici in comune", "Tenemos muchos amigos en común", "Nous avons beaucoup d'amis en commun",
                "Máme hodně společných přátel")}),
    2494: (NEAR + " (schrecklich: «Das Wetter ist schrecklich»)", {
        "t_ru": "ужасный, страшный", "t_uk": "жахливий, страшний", "t_en": "terrible, awful", "t_tr": "berbat, korkunç",
        "t_pl": "straszny, okropny",
        **all_x("Ich habe furchtbare Kopfschmerzen", "У меня ужасно болит голова", "У мене страшенно болить голова",
                "I have a terrible headache", "Başım korkunç ağrıyor", "Strasznie boli mnie głowa",
                "Ho un mal di testa terribile", "Tengo un dolor de cabeza horrible", "J'ai un mal de tête épouvantable",
                "Hrozně mě bolí hlava")}),
    488: (NEAR + " (Hose: «Sie trägt eine … Hose»); «одежда» — другое слово", {
        "t_ru": "платье", "t_uk": "сукня", "t_en": "dress", "t_tr": "elbise", "t_pl": "sukienka",
        **all_x("Das Kleid steht dir gut", "Это платье тебе идёт", "Ця сукня тобі пасує", "That dress suits you",
                "Bu elbise sana yakışıyor", "W tej sukience ci do twarzy", "Questo vestito ti sta bene",
                "Ese vestido te queda bien", "Cette robe te va bien", "Ty šaty ti sluší")}),
    13625: (LIST, {"t_ru": "кольцо", "t_uk": "каблучка, кільце", "t_en": "ring", "t_tr": "yüzük", "t_pl": "pierścionek"}),
    76: (TWO + " («бал» — омоним, своя строка)", {
        "t_ru": "мяч", "t_uk": "м'яч", "t_en": "ball", "t_tr": "top", "t_pl": "piłka", "t_it": "la palla, il pallone",
        "t_es": "la pelota, el balón", "t_fr": "le ballon, la balle", "t_cs": "míč"}),
    216: (LIST, {"t_ru": "мороженое, лёд", "t_uk": "морозиво, лід"}),
}

SPLIT_LATER = {
    1475: ["das Gericht = суд"],
    76: ["der Ball = бал"],
}
