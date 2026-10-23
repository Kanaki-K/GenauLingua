"""Вычитка немецкого, порция p028 (B2) + хвост p027 (фразы 7–8 слов), 23.10: заглушки → бытовые"""

W = "вычитка немецкого: учебная заглушка → живая бытовая фраза"

def ex(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"example_de": de, "example_ru": ru, "example_uk": uk, "example_en": en, "example_tr": tr,
            "example_pl": pl, "example_it": it, "example_es": es, "example_fr": fr, "example_cs": cs}

FIXES = {
    7189: (W + "; «Der Dieb schleicht» — штамп", ex("Nachts schleicht sich mein Sohn in die Küche und isst Schokolade",
        "Ночью мой сын крадётся на кухню и ест шоколад", "Уночі мій син крадеться на кухню й їсть шоколад",
        "At night my son sneaks into the kitchen and eats chocolate", "Geceleri oğlum gizlice mutfağa girip çikolata yiyor",
        "W nocy mój syn zakrada się do kuchni i je czekoladę", "Di notte mio figlio sgattaiola in cucina e mangia cioccolato",
        "Por la noche mi hijo se cuela en la cocina y come chocolate", "La nuit, mon fils se faufile dans la cuisine et mange du chocolat",
        "V noci se můj syn plíží do kuchyně a jí čokoládu")),
    7196: (W + "; «unsere Kräfte für dieses Projekt» — офис", ex("Das kleine Café vereint Buchladen und Kaffeebar",
        "Маленькое кафе сочетает в себе книжный магазин и кофейню", "Маленьке кафе поєднує книгарню й кав'ярню",
        "The little café combines a bookshop and a coffee bar", "Küçük kafe kitapçı ile kahve barını bir araya getiriyor",
        "Mała kawiarnia łączy księgarnię i kawiarnię", "Il piccolo caffè unisce libreria e bar",
        "La pequeña cafetería combina librería y barra de café", "Le petit café réunit librairie et bar à café",
        "Malá kavárna spojuje knihkupectví a kavárnu")),
    7276: (W, ex("Der Effekt von dem teuren Shampoo ist gleich null",
        "Эффект от дорогого шампуня — ноль", "Ефект від дорогого шампуню — нуль",
        "The effect of the expensive shampoo is zero", "Pahalı şampuanın etkisi sıfır",
        "Efekt drogiego szamponu jest zerowy", "L'effetto dello shampoo costoso è pari a zero",
        "El efecto del champú caro es nulo", "L'effet du shampooing cher est nul",
        "Efekt drahého šamponu je nulový")),
    7278: (W, ex("Belassen wir es dabei, ich will nicht mehr streiten",
        "Оставим всё как есть, я больше не хочу спорить", "Залишмо все як є, я більше не хочу сперечатися",
        "Let's leave it at that, I don't want to argue any more", "Böyle bırakalım, artık tartışmak istemiyorum",
        "Zostawmy to tak, nie chcę się już kłócić", "Lasciamo le cose come stanno, non voglio più litigare",
        "Dejémoslo así, no quiero discutir más", "Restons-en là, je ne veux plus me disputer",
        "Nechme to být, už se nechci hádat")),
    7475: (W + "; офис", ex("Für die Prüfung ist nur das dritte Kapitel relevant",
        "Для экзамена важна только третья глава", "Для іспиту важливий лише третій розділ",
        "Only the third chapter is relevant for the exam", "Sınav için sadece üçüncü bölüm önemli",
        "Na egzamin ważny jest tylko trzeci rozdział", "Per l'esame è rilevante solo il terzo capitolo",
        "Para el examen solo es relevante el tercer capítulo", "Pour l'examen, seul le troisième chapitre est pertinent",
        "Ke zkoušce je důležitá jen třetí kapitola")),
}

REPLACE = []

SPLIT_LATER = {}
