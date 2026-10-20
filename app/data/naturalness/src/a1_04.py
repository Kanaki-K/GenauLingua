"""A1, блок 4: слова 121–160 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
TWO = "в строке два разных слова — оставлено главное, второе — отдельной строкой (блок деления)"
EN = "английский пример: так не говорят о том, что происходит сейчас / будет"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    1857: (LIST, {"t_ru": "с", "t_uk": "з", "t_tr": "-den beri", "t_pl": "od", "t_cs": "od"}),
    681: ("«Hier ist Ordnung» — так не говорят; живое — «Alles in Ordnung?»", {
        "t_ru": "порядок", "t_uk": "порядок", "t_en": "order", "t_tr": "düzen", "t_pl": "porządek",
        **all_x("Alles in Ordnung?", "Всё в порядке?", "Усе в порядку?", "Is everything all right?",
                "Her şey yolunda mı?", "Wszystko w porządku?", "Tutto a posto?", "¿Todo en orden?",
                "Tout est en ordre?", "Je všechno v pořádku?")}),
    421: (LIST, {"t_tr": "duymak, dinlemek"}),
    13314: ("«vom Papa» — диалект, по-литературному «von Papa»; пример, где vom на месте", {
        **all_x("Ich komme gerade vom Arzt", "Я как раз от врача", "Я якраз від лікаря",
                "I've just come from the doctor's", "Doktordan geliyorum", "Wracam właśnie od lekarza",
                "Torno adesso dal medico", "Vengo del médico", "Je reviens de chez le médecin",
                "Jdu zrovna od doktora")}),
    13317: (LIST + "; «with this car» — так не говорят", {
        "t_ru": "этот", "t_uk": "цей", "t_en": "this", "t_tr": "bu", "t_pl": "ten", "t_it": "questo",
        "t_es": "este", "t_fr": "ce, cette", "t_cs": "tento",
        "x_en": "We're going on holiday in this car"}),
    1666: (EN, {"t_en": "girl", "x_en": "The girl is playing in the garden"}),
    848: (LIST + "; sollen — «положено», не совет", {
        "t_ru": "должен, следует", "t_uk": "повинен, слід", "t_en": "should, to be supposed to",
        "t_tr": "-malı, gerekmek", "t_pl": "mieć, powinien", "t_es": "deber", "t_cs": "mít",
        "x_en": "We're supposed to come at three"}),
    14884: (LIST, {"t_ru": "друг, парень", "t_uk": "друг, хлопець", "t_tr": "arkadaş, erkek arkadaş",
                   "t_pl": "przyjaciel, chłopak", "t_fr": "l'ami, le copain", "t_cs": "kamarád, přítel"}),
    382: (LIST, {"t_ru": "дом", "t_en": "house, home", "t_tr": "ev", "t_pl": "dom", "x_en": "I'm at home"}),
    2: (LIST + "; night — это Nacht", {"t_en": "evening"}),
    2096: (LIST + "; «планета» — не перевод", {"t_ru": "мир, свет", "t_uk": "світ", "t_tr": "dünya"}),
    12459: ("«Цветок, к сожалению, мёртвый» — так по-русски не говорят", {
        "t_ru": "мёртвый", "t_uk": "мертвий", "t_tr": "ölü",
        **all_x("Ist die Maus tot?", "Мышь мёртвая?", "Миша мертва?", "Is the mouse dead?", "Fare ölü mü?",
                "Czy ta mysz jest martwa?", "Il topo è morto?", "¿Está muerto el ratón?", "La souris est morte?",
                "Je ta myš mrtvá?")}),
    125: (LIST + "; " + EN, {"t_ru": "оставаться, остаться", "t_uk": "залишатися, лишатися", "t_en": "to stay",
                             "t_tr": "kalmak", "t_pl": "zostać, zostawać", "x_en": "I'm staying at home today"}),
    238: (LIST, {"t_ru": "есть", "t_uk": "їсти", "t_en": "to eat", "t_tr": "yemek", "t_pl": "jeść"}),
    964: (LIST, {"t_ru": "под, среди", "t_uk": "під, серед", "t_en": "under, among", "t_tr": "altında",
                 "t_pl": "pod, wśród", "t_es": "debajo de, entre"}),
    805: (LIST, {"t_ru": "быстрый, быстро", "t_en": "fast, quick", "t_it": "veloce", "t_fr": "rapide, vite"}),
    1085: (LIST, {"t_ru": "вместе", "t_uk": "разом", "t_en": "together", "t_tr": "birlikte", "t_pl": "razem",
                  "t_cs": "spolu"}),
    649: (LIST, {"t_ru": "брать, взять", "t_uk": "брати, взяти", "t_en": "to take", "t_tr": "almak",
                 "t_pl": "brać, wziąć", "t_es": "tomar", "x_en": "I'll take the newspaper"}),
    137: (LIST, {"t_ru": "приносить, привозить", "t_uk": "приносити, привозити", "t_en": "to bring",
                 "t_tr": "getirmek", "t_pl": "przynosić, przywozić", "t_es": "traer", "t_fr": "apporter",
                 "t_cs": "přinést"}),
    345: (LIST, {"t_ru": "верить, думать", "t_uk": "вірити, думати", "t_en": "to believe, to think",
                 "t_tr": "inanmak, sanmak", "t_pl": "wierzyć, myśleć", "t_cs": "věřit, myslet si",
                 "x_en": "I think he's coming"}),
    131: (LIST + "; «уходить на что-то» — другое употребление", {
        "t_ru": "нужно, нуждаться", "t_uk": "потребувати, треба", "t_en": "to need",
        "t_tr": "ihtiyaç duymak, lazım olmak", "t_pl": "potrzebować", "t_it": "avere bisogno di"}),
    608: (LIST, {"t_ru": "момент, минутка", "t_uk": "момент, хвилинка", "t_en": "moment", "t_tr": "an",
                 "t_pl": "moment, chwila", "t_fr": "le moment, l'instant", "t_cs": "moment, chvilka"}),
    400: (LIST + "; «господь» — другое значение", {
        "t_ru": "господин", "t_uk": "пан", "t_en": "Mr, gentleman", "t_tr": "bey", "t_pl": "pan",
        "t_fr": "le monsieur"}),
    285: (LIST + "; пример — будущее время", {
        "t_ru": "спрашивать, спросить", "t_uk": "питати, запитувати", "t_en": "to ask", "t_tr": "sormak",
        "t_pl": "pytać, zapytać", "t_it": "chiedere", "t_es": "preguntar", "t_fr": "demander",
        "t_cs": "ptát se, zeptat se",
        "x_ru": "Я спрошу учителя", "x_uk": "Я запитаю вчителя", "x_en": "I'll ask the teacher",
        "x_tr": "Öğretmene sorarım", "x_pl": "Zapytam nauczyciela", "x_cs": "Zeptám se učitele"}),
    41: (LIST + "; пометка «(fam.)» в переводе", {
        "t_ru": "работа", "t_uk": "робота", "t_en": "work, job", "t_tr": "iş", "t_pl": "praca",
        "t_fr": "le travail"}),
    1004: ("порча знаний: «обслуживать технику» — омоним warten (Wartung), другое слово; " + EN, {
        "t_ru": "ждать", "t_uk": "чекати", "t_en": "to wait", "t_tr": "beklemek", "t_pl": "czekać",
        "x_en": "I'm waiting for you"}),
    1311: (LIST + "; «при этом присутствовал» — канцелярски", {
        "t_ru": "при этом, с собой", "t_uk": "при цьому, із собою", "t_en": "there, with it",
        "t_tr": "yanında, orada", "t_pl": "przy tym, ze sobą", "t_it": "presente, con sé",
        "t_es": "presente, con eso", "t_fr": "présent", "x_ru": "Я при этом был"}),
    846: (LIST + "; uk «Я прийду негайно» — книжно", {
        "t_ru": "сразу, немедленно", "t_uk": "відразу, негайно", "t_en": "right away, immediately",
        "t_tr": "hemen", "t_pl": "natychmiast, od razu", "t_es": "enseguida", "t_fr": "tout de suite",
        "t_cs": "hned", "x_uk": "Я відразу прийду"}),
    251: ("«Семья ест вместе» — неживо", {
        "t_ru": "семья",
        **all_x("Am Sonntag isst die ganze Familie zusammen", "В воскресенье вся семья обедает вместе",
                "У неділю вся родина обідає разом", "On Sundays the whole family eats together",
                "Pazar günleri bütün aile birlikte yemek yer", "W niedzielę cała rodzina je razem obiad",
                "La domenica tutta la famiglia mangia insieme", "Los domingos toda la familia come junta",
                "Le dimanche, toute la famille mange ensemble", "V neděli jí celá rodina spolu")}),
    213: (LIST, {"t_ru": "один раз, однажды", "t_uk": "один раз, колись", "t_en": "once", "t_tr": "bir kez",
                 "t_pl": "raz, kiedyś", "t_cs": "jednou"}),
    847: ("«Der Sohn ist groß» — по-немецки нужно «Mein Sohn»; groß здесь — «большой», не «высокий»", {
        **all_x("Mein Sohn ist schon groß", "Мой сын уже большой", "Мій син уже великий",
                "My son is all grown up", "Oğlum artık büyüdü", "Mój syn jest już duży",
                "Mio figlio è già grande", "Mi hijo ya es mayor", "Mon fils est déjà grand",
                "Můj syn je už velký")}),
    732: (LIST, {"t_ru": "проблема", "t_uk": "проблема", "t_en": "problem", "t_tr": "sorun",
                 "x_en": "That's no problem"}),
    10: ("«solo» по-итальянски и «tek başına, kendi kendine» — лишнее, «solo» ещё и «только»", {
        "t_tr": "yalnız, tek başına", "t_it": "da solo"}),
    867: (LIST + "; uk «говорю німецькою мовою» — книжно", {
        "t_ru": "говорить, разговаривать", "t_uk": "говорити, розмовляти", "t_tr": "konuşmak",
        "x_uk": "Я розмовляю німецькою"}),
    267: (TWO + " («измотанный» — Ich bin fertig, своя строка)", {
        "t_ru": "готовый, законченный", "t_uk": "готовий, завершений", "t_en": "ready, finished",
        "t_tr": "hazır, bitmiş", "t_pl": "gotowy, skończony", "t_it": "pronto, finito",
        "t_es": "listo, terminado", "t_fr": "prêt, fini", "t_cs": "hotový"}),
    374: (TWO + " (halten — «останавливаться, держать»; «считать» — halten für, своя строка); "
               "первым — значение из примера", {
        "t_ru": "останавливаться, держать", "t_uk": "зупинятися, тримати", "t_en": "to stop, to hold",
        "t_tr": "durmak, tutmak", "t_pl": "zatrzymywać się, trzymać", "t_it": "fermarsi, tenere",
        "t_es": "parar, sostener", "t_fr": "s'arrêter, tenir", "t_cs": "zastavovat, držet"}),
    13331: (LIST, {"t_ru": "у, при", "t_uk": "у, при", "t_en": "at the", "t_tr": "-de", "t_pl": "u, przy",
                   "t_it": "dal, da", "t_es": "en el", "t_fr": "chez le", "t_cs": "u, při"}),
    403: (LIST, {"t_ru": "помощь", "t_uk": "допомога", "t_en": "help", "t_tr": "yardım", "t_pl": "pomoc"}),
}

SPLIT_LATER = {
    1004: ["warten = обслуживать (Wartung) — B2, своя строка"],
    267: ["fertig sein = вымотан (Ich bin total fertig)"],
    374: ["halten für = считать (Ich halte das für gut)"],
}
