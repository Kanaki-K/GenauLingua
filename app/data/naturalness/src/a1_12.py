"""A1, блок 12: слова 441–480 по частоте. Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
TWO = "в строке два разных слова — оставлено главное, второе — отдельной строкой (блок деления)"
EN = "английский пример: так не говорят о том, что происходит сейчас / будет"
SAME = "пример совпадал с примером другого слова — у каждого свой"
MARK = "пометка «(hovor.)» в переводе"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    1946: (LIST + "; " + MARK + "; uk — порядок слов", {
        "t_ru": "тест, контрольная", "t_uk": "тест, контрольна", "t_en": "test", "t_tr": "test, sınav",
        "t_pl": "test, sprawdzian", "t_it": "il test, la verifica", "t_es": "el examen, el test",
        "t_fr": "le test, le contrôle", "t_cs": "test, písemka", "x_uk": "Завтра ми пишемо тест"}),
    925: ("четыре описания вместо слова; «Моя встреча в понедельник» — неживо", {
        "t_ru": "встреча, приём", "t_uk": "зустріч, прийом", "t_en": "appointment", "t_tr": "randevu",
        "t_pl": "termin, wizyta", "t_it": "l'appuntamento", "t_es": "la cita", "t_fr": "le rendez-vous",
        "t_cs": "termín, schůzka",
        **all_x("Ich habe morgen einen Termin beim Arzt", "Завтра у меня приём у врача", "Завтра в мене прийом у лікаря",
                "I have a doctor's appointment tomorrow", "Yarın doktordan randevum var", "Jutro mam wizytę u lekarza",
                "Domani ho un appuntamento dal medico", "Mañana tengo cita con el médico",
                "Demain, j'ai rendez-vous chez le médecin", "Zítra mám termín u lékaře")}),
    591: ("«Ich trinke Milch» — тот же шаблон, что у Wasser, Tee, Kaffee", {
        **all_x("Wir brauchen noch Milch", "Нам ещё нужно молоко", "Нам ще потрібне молоко", "We still need milk",
                "Süt de lazım", "Potrzebujemy jeszcze mleka", "Ci serve ancora il latte", "Todavía necesitamos leche",
                "Il nous faut encore du lait", "Ještě potřebujeme mléko")}),
    6483: (TWO + " (Stock — «этаж»; «палка, трость» — своя строка)", {
        "t_ru": "этаж", "t_uk": "поверх", "t_en": "floor", "t_tr": "kat", "t_pl": "piętro", "t_it": "il piano",
        "t_es": "el piso, la planta", "t_fr": "l'étage", "t_cs": "patro, poschodí"}),
    1102: (LIST, {"t_ru": "забирать, заезжать за", "t_uk": "забирати, заїжджати за", "t_en": "to pick up",
                  "t_tr": "almaya gitmek", "t_pl": "odbierać", "t_it": "passare a prendere",
                  "t_es": "recoger, ir a buscar", "t_fr": "venir chercher", "t_cs": "vyzvednout"}),
    6487: (SAME + " (Sonne: «Die Sonne scheint»); " + LIST, {
        "t_ru": "светить, казаться", "t_uk": "світити, здаватися", "t_en": "to shine, to seem",
        "t_tr": "parlamak, görünmek", "t_pl": "świecić, wydawać się", "t_it": "splendere, sembrare",
        "t_es": "brillar, parecer", "t_fr": "briller, sembler",
        **all_x("Heute scheint endlich wieder die Sonne", "Сегодня наконец снова светит солнце",
                "Сьогодні нарешті знову світить сонце", "The sun is finally shining again today",
                "Bugün nihayet yine güneş parlıyor", "Dziś wreszcie znowu świeci słońce",
                "Oggi finalmente splende di nuovo il sole", "Hoy por fin vuelve a brillar el sol",
                "Aujourd'hui, le soleil brille enfin à nouveau", "Dnes konečně zase svítí slunce")}),
    745: (LIST, {"t_ru": "курить", "t_uk": "курити", "t_en": "to smoke", "t_tr": "sigara içmek", "t_pl": "palić",
                 "x_en": "He doesn't smoke"}),
    196: (LIST, {"t_ru": "тёмный", "t_uk": "темний", "t_en": "dark", "t_tr": "karanlık, koyu", "t_pl": "ciemny",
                 "t_it": "buio, scuro", "t_es": "oscuro", "t_fr": "sombre, foncé", "t_cs": "tmavý"}),
    497: (LIST + "; «Sie kocht zum Abendessen» — по-немецки неживо", {
        "t_ru": "готовить, варить", "t_uk": "готувати, варити", "t_en": "to cook", "t_tr": "yemek yapmak, pişirmek",
        "t_pl": "gotować", "t_it": "cucinare", "t_es": "cocinar", "t_fr": "cuisiner",
        **all_x("Heute koche ich Suppe", "Сегодня я варю суп", "Сьогодні я варю суп", "I'm making soup today",
                "Bugün çorba pişiriyorum", "Dziś gotuję zupę", "Oggi cucino la zuppa", "Hoy cocino sopa",
                "Aujourd'hui, je cuisine une soupe", "Dnes vařím polévku")}),
    2403: (EN, {"x_en": "The film ends at 10 pm"}),
    1395: (SAME + " (verboten: курение); " + LIST, {
        "t_ru": "разрешать, позволять", "t_uk": "дозволяти", "t_en": "to allow", "t_tr": "izin vermek",
        "t_pl": "pozwalać", "t_it": "permettere", "t_es": "permitir, dejar", "t_fr": "permettre", "t_cs": "dovolit",
        **all_x("Meine Eltern erlauben mir das nicht", "Родители мне этого не разрешают",
                "Батьки мені цього не дозволяють", "My parents don't allow me to", "Ailem buna izin vermiyor",
                "Rodzice mi na to nie pozwalają", "I miei genitori non me lo permettono", "Mis padres no me lo permiten",
                "Mes parents ne me le permettent pas", "Rodiče mi to nedovolí")}),
    2032: (LIST, {"t_ru": "запрещено, запрещённый", "t_uk": "заборонено, заборонений", "t_en": "forbidden, not allowed",
                  "t_tr": "yasak", "t_pl": "zakazany, zabroniony", "t_it": "vietato", "t_fr": "interdit",
                  "t_cs": "zakázaný"}),
    278: (EN, {"x_en": "We're going to the airport"}),
    288: (SAME + " (Samstag: «Am … bin ich frei»)", {
        **all_x("Am Freitag gehen wir tanzen", "В пятницу мы идём танцевать", "У п'ятницю ми йдемо танцювати",
                "On Friday we're going dancing", "Cuma günü dansa gidiyoruz", "W piątek idziemy potańczyć",
                "Venerdì andiamo a ballare", "El viernes vamos a bailar", "Vendredi, on va danser",
                "V pátek jdeme tancovat")}),
    781: (EN, {"x_en": "I'm free on Saturday"}),
    309: (LIST, {"t_ru": "гость", "t_uk": "гість", "t_en": "guest", "t_tr": "misafir", "t_pl": "gość",
                 "t_it": "l'ospite", "t_es": "el invitado", "t_fr": "l'invité", "t_cs": "host"}),
    932: (SAME + " (Entschuldigung: «…, wo ist die Toilette?»)", {
        "t_ru": "туалет", "t_uk": "туалет", "t_en": "toilet", "t_tr": "tuvalet", "t_pl": "toaleta",
        **all_x("Ich muss mal auf die Toilette", "Мне нужно в туалет", "Мені треба в туалет",
                "I need to go to the toilet", "Tuvalete gitmem lazım", "Muszę iść do toalety", "Devo andare in bagno",
                "Tengo que ir al baño", "Je dois aller aux toilettes", "Musím na záchod")}),
    245: (LIST, {"t_ru": "водитель", "t_uk": "водій", "t_en": "driver", "t_tr": "şoför, sürücü", "t_pl": "kierowca"}),
    12109: (LIST + "; pl «Chętnie chodzę pływać» — калька", {
        "t_ru": "плавать", "t_uk": "плавати", "t_en": "to swim", "t_tr": "yüzmek", "t_pl": "pływać",
        "t_it": "nuotare", "t_es": "nadar", "t_fr": "nager", "t_cs": "plavat", "x_pl": "Lubię pływać"}),
    721: (LIST + "; tr — «надо», а не «иду»", {
        "t_ru": "почта", "t_uk": "пошта", "t_en": "post office, mail", "t_tr": "postane, posta", "t_pl": "poczta",
        "t_it": "la posta", "t_es": "el correo", "t_fr": "la poste", "x_tr": "Postaneye gitmem lazım"}),
    61: (LIST, {"t_ru": "высказывание, заявление", "t_uk": "висловлювання, заява", "t_en": "statement",
                "t_tr": "ifade, açıklama", "t_pl": "wypowiedź, oświadczenie", "t_it": "l'affermazione, la dichiarazione",
                "t_es": "la afirmación, la declaración", "t_fr": "la déclaration, l'affirmation",
                "t_cs": "tvrzení, výpověď"}),
    927: (LIST + "; «милый» — устаревшее значение", {"t_ru": "дорогой", "t_uk": "дорогий", "t_en": "expensive",
                                                    "t_tr": "pahalı", "t_pl": "drogi"}),
    1416: (TWO + " («скучать» — Du fehlst mir, своя строка)", {
        "t_ru": "не хватать, отсутствовать", "t_uk": "бракувати, бути відсутнім", "t_en": "to be missing, to lack",
        "t_tr": "eksik olmak", "t_pl": "brakować", "x_en": "I'm still missing a document"}),
    359: (LIST, {"t_ru": "размер, рост", "t_uk": "розмір, зріст", "t_en": "size, height", "t_tr": "beden, boy",
                 "t_pl": "rozmiar, wzrost", "t_it": "la taglia, la misura", "t_es": "la talla, el tamaño",
                 "t_fr": "la taille", "t_cs": "velikost, výška"}),
    1785: (LIST, {"t_ru": "счёт", "t_uk": "рахунок", "t_en": "bill, invoice", "t_tr": "hesap, fatura",
                  "t_pl": "rachunek", "t_it": "il conto", "t_es": "la cuenta", "t_fr": "l'addition, la facture",
                  "t_cs": "účet"}),
    853: (EN, {"x_en": "I relax on Sundays"}),
    6532: (SAME + " (Laden)", {
        "t_ru": "открыт, открытый", "t_uk": "відчинений, відкритий", "t_en": "open", "t_tr": "açık", "t_pl": "otwarty",
        **all_x("Das Museum ist bis 18 Uhr geöffnet", "Музей открыт до 18 часов", "Музей відкритий до 18:00",
                "The museum is open until 6 pm", "Müze saat 18'e kadar açık", "Muzeum jest otwarte do 18",
                "Il museo è aperto fino alle 18", "El museo está abierto hasta las 18",
                "Le musée est ouvert jusqu'à 18 heures", "Muzeum je otevřené do 18 hodin")}),
    481: (EN, {"x_en": "We're going to the cinema"}),
    1340: (LIST, {"t_ru": "нажимать, давить", "t_uk": "натискати, тиснути", "t_en": "to press, to push",
                  "t_tr": "basmak", "t_pl": "naciskać", "t_it": "premere", "t_es": "pulsar, apretar",
                  "t_fr": "appuyer", "t_cs": "stisknout, tlačit"}),
    2012: (LIST, {"t_ru": "подписывать", "t_uk": "підписувати", "t_pl": "podpisać"}),
    17489: (LIST + "; " + EN, {"t_ru": "ремонтировать, чинить", "t_uk": "ремонтувати, лагодити",
                               "t_en": "to repair, to fix", "t_tr": "tamir etmek", "t_pl": "naprawiać",
                               "x_en": "He's fixing the car"}),
    96: (LIST, {"t_ru": "профессия", "t_uk": "професія, фах", "t_en": "profession, job", "t_tr": "meslek",
                "t_pl": "zawód", "t_it": "la professione, il mestiere", "t_es": "la profesión, el oficio",
                "t_fr": "le métier, la profession", "t_cs": "povolání"}),
    1043: (EN, {"x_en": "It's cold in winter"}),
}

SPLIT_LATER = {
    6483: ["der Stock = палка, трость (Plural Stöcke)"],
    1416: ["fehlen = скучать (Du fehlst mir)"],
}
