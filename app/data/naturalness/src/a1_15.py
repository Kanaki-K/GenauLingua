"""A1, блок 15: слова 561–600 по частоте (+ Mai, nass — шаблонные примеры). Вычитано вручную 21.10."""

LIST = "список → главное слово и не больше одной альтернативы"
TWO = "в строке два разных слова — оставлено главное, второе — отдельной строкой (блок деления)"
EN = "английский пример: так не говорят о том, что происходит сейчас / будет"
DULL = "пример ни о чём («X ist Y») → фраза из жизни"
SAME = "пример совпадал с примером другого слова — у каждого свой"


def all_x(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"x_de": de, "x_ru": ru, "x_uk": uk, "x_en": en, "x_tr": tr, "x_pl": pl,
            "x_it": it, "x_es": es, "x_fr": fr, "x_cs": cs}


FIXES = {
    18163: ("«right around the corner» — это «прямо за углом», а в немецком «справа за углом»", {
        "x_en": "The entrance is around the corner on the right"}),
    1191: (TWO + " («договориться», «иметь значение» — свои строки); " + SAME + " (Licht: «Mach … das Licht an»)", {
        "t_ru": "выключать, гасить", "t_uk": "вимикати, гасити", "t_en": "to turn off, to switch off",
        "t_tr": "kapatmak, söndürmek", "t_pl": "wyłączać, gasić", "t_it": "spegnere", "t_es": "apagar",
        "t_fr": "éteindre", "t_cs": "zhasnout, vypnout",
        **all_x("Mach bitte den Fernseher aus", "Выключи, пожалуйста, телевизор", "Вимкни, будь ласка, телевізор",
                "Please turn off the TV", "Lütfen televizyonu kapat", "Wyłącz, proszę, telewizor",
                "Spegni la tv, per favore", "Apaga la tele, por favor", "Éteins la télé, s'il te plaît",
                "Vypni prosím televizi")}),
    832: (EN, {"x_en": "Courses start in September"}),
    780: ("пример совпал с примером mir («Gib mir bitte das Salz») — у Salz свой", {
        **all_x("Die Suppe braucht noch etwas Salz", "Супу не хватает соли", "Супу бракує солі",
                "The soup needs a bit more salt", "Çorbaya biraz daha tuz lazım", "Zupie brakuje trochę soli",
                "La zuppa ha bisogno di un po' di sale", "A la sopa le falta un poco de sal",
                "La soupe manque un peu de sel", "Polévka potřebuje ještě trochu soli")}),
    6793: (LIST + "; «оккупированный» — другое значение; " + EN, {
        "t_ru": "занято, занятый", "t_en": "taken, occupied", "t_tr": "dolu", "t_pl": "zajęty", "t_fr": "occupé, pris",
        "t_cs": "obsazený", "x_en": "Sorry, this seat is already taken"}),
    1182: (LIST + "; первым — слово из примера", {
        "t_ru": "экскурсия, поездка", "t_uk": "екскурсія, поїздка", "t_en": "trip, outing", "t_tr": "gezi",
        "t_pl": "wycieczka", "t_it": "la gita", "t_es": "la excursión", "t_fr": "l'excursion, la sortie",
        "x_uk": "Ми їдемо на екскурсію", "x_en": "We're going on a trip"}),
    116: (LIST + "; «дешёвка» — оценка, не перевод", {
        "t_ru": "дешёвый", "t_uk": "дешевий", "t_en": "cheap", "t_tr": "ucuz", "t_pl": "tani", "t_it": "economico",
        "t_fr": "bon marché, pas cher"}),
    455: (SAME + " («… beginnen die Kurse» у September)", {
        **all_x("Im Juni haben die Kinder Ferien", "В июне у детей каникулы", "У червні в дітей канікули",
                "The children are on holiday in June", "Haziranda çocuklar tatilde", "W czerwcu dzieci mają wakacje",
                "A giugno i bambini sono in vacanza", "En junio los niños están de vacaciones",
                "En juin, les enfants sont en vacances", "V červnu mají děti prázdniny")}),
    72: (LIST + "; uk «залізницею» — книжно, говорят «потягом»", {
        "t_ru": "поезд, железная дорога", "t_uk": "поїзд, залізниця", "t_en": "train, railway",
        "t_tr": "tren, demiryolu", "t_pl": "kolej, pociąg", "t_it": "il treno, la ferrovia",
        "t_es": "el tren, el ferrocarril", "t_fr": "le train", "t_cs": "vlak, železnice",
        "x_uk": "Я їжджу на роботу потягом"}),
    329: ("«вперёд без поворотов» — пояснение", {"t_ru": "прямо", "t_uk": "прямо", "t_tr": "dümdüz", "t_pl": "prosto"}),
    69: (LIST + "; " + EN, {"t_ru": "купаться", "t_uk": "купатися", "t_en": "to bathe, to take a bath",
                           "t_tr": "yüzmek, banyo yapmak", "t_pl": "kąpać się",
                           "x_en": "The children are swimming in the lake"}),
    775: ("tr «su» — это вода", {"t_tr": "meyve suyu"}),
    755: (EN, {"x_en": "I'm making rice"}),
    778: (LIST, {"t_ru": "салат", "t_uk": "салат", "t_tr": "salata"}),
    296: (SAME + " («Im … blühen» — у April и Mai)", {
        **all_x("Ich mag den Frühling am liebsten", "Больше всего я люблю весну", "Найбільше я люблю весну",
                "Spring is my favourite season", "En çok ilkbaharı severim", "Najbardziej lubię wiosnę",
                "La primavera è la mia stagione preferita", "La primavera es mi estación favorita",
                "Le printemps, c'est ma saison préférée", "Nejradši mám jaro")}),
    565: (SAME + " («Im … blühen» — у April и Frühling)", {
        **all_x("Im Mai fahren wir nach Italien", "В мае мы едем в Италию", "У травні ми їдемо до Італії",
                "We're going to Italy in May", "Mayısta İtalya'ya gidiyoruz", "W maju jedziemy do Włoch",
                "A maggio andiamo in Italia", "En mayo vamos a Italia", "En mai, on part en Italie",
                "V květnu jedeme do Itálie")}),
    12550: (LIST + "; пример «gehe in die Praxis zum Zahnarzt» — неживо и повторяет Mittwoch", {
        "t_ru": "кабинет врача, практика", "t_uk": "кабінет лікаря, практика", "t_en": "doctor's surgery, practice",
        "t_tr": "muayenehane, pratik", "t_pl": "gabinet, praktyka", "t_it": "lo studio medico, la pratica",
        "t_es": "la consulta, la práctica", "t_fr": "le cabinet, la pratique", "t_cs": "ordinace, praxe",
        **all_x("Die Praxis ist am Montag geschlossen", "Кабинет в понедельник закрыт", "Кабінет у понеділок зачинений",
                "The surgery is closed on Monday", "Muayenehane pazartesi kapalı", "Gabinet jest w poniedziałek zamknięty",
                "Lo studio è chiuso il lunedì", "La consulta está cerrada el lunes", "Le cabinet est fermé le lundi",
                "Ordinace je v pondělí zavřená")}),
    622: (LIST + "; " + DULL, {
        "t_ru": "мебель", "t_uk": "меблі", "t_en": "furniture", "t_tr": "mobilya", "t_pl": "meble",
        **all_x("Wir brauchen neue Möbel für die Küche", "Нам нужна новая мебель для кухни",
                "Нам потрібні нові меблі для кухні", "We need new furniture for the kitchen",
                "Mutfak için yeni mobilyaya ihtiyacımız var", "Potrzebujemy nowych mebli do kuchni",
                "Ci servono mobili nuovi per la cucina", "Necesitamos muebles nuevos para la cocina",
                "Il nous faut de nouveaux meubles pour la cuisine", "Potřebujeme nový nábytek do kuchyně")}),
    300: (SAME + " (spielen: «Wir spielen Fußball»); «мяч» — другое значение; пометка «(fam.)»", {
        "t_ru": "футбол", "t_uk": "футбол", "t_en": "football", "t_tr": "futbol", "t_pl": "piłka nożna",
        "t_it": "il calcio", "t_es": "el fútbol", "t_fr": "le football, le foot", "t_cs": "fotbal",
        **all_x("Am Samstag schauen wir Fußball", "В субботу мы смотрим футбол", "У суботу ми дивимося футбол",
                "We're watching football on Saturday", "Cumartesi futbol izliyoruz",
                "W sobotę oglądamy piłkę nożną", "Sabato guardiamo il calcio", "El sábado vemos el fútbol",
                "Samedi, on regarde le foot", "V sobotu se díváme na fotbal")}),
    1188: (LIST + "; pl «Chętnie jeżdżę» — калька", {
        "t_ru": "заграница, за границей", "t_uk": "закордон", "t_en": "abroad", "t_tr": "yurt dışı",
        "t_pl": "zagranica", "x_pl": "Lubię jeździć za granicę"}),
    13498: (EN, {"x_en": "I'm twenty now"}),
    661: (EN, {"x_en": "It's cool in November"}),
    464: (LIST + "; «страховая касса, наличные» — другие значения", {
        "t_ru": "касса", "t_uk": "каса", "t_en": "checkout, till", "t_tr": "kasa", "t_pl": "kasa"}),
    134: (SAME + " («Die Straße ist …» — у lang и nass)", {
        "t_ru": "широкий", "t_uk": "широкий", "t_tr": "geniş", "t_pl": "szeroki", "t_it": "largo", "t_es": "ancho",
        **all_x("Der Schrank ist zu breit für die Tür", "Шкаф слишком широкий для двери",
                "Шафа занадто широка для дверей", "The wardrobe is too wide for the door",
                "Dolap kapı için fazla geniş", "Szafa jest za szeroka na te drzwi",
                "L'armadio è troppo largo per la porta", "El armario es demasiado ancho para la puerta",
                "L'armoire est trop large pour la porte", "Skříň je moc široká na dveře")}),
    643: (SAME + " («Die Straße ist …» — у lang и breit)", {
        **all_x("Pass auf, der Boden ist nass!", "Осторожно, пол мокрый!", "Обережно, підлога мокра!",
                "Careful, the floor is wet!", "Dikkat, yer ıslak!", "Uważaj, podłoga jest mokra!",
                "Attento, il pavimento è bagnato!", "¡Cuidado, el suelo está mojado!", "Attention, le sol est mouillé!",
                "Pozor, podlaha je mokrá!")}),
    168: ("«Wie lautet das heutige Datum?» — канцелярски", {
        "t_ru": "дата, число", "t_uk": "дата, число",
        **all_x("Welches Datum haben wir heute?", "Какое сегодня число?", "Яке сьогодні число?", "What's the date today?",
                "Bugünün tarihi ne?", "Jaka jest dzisiaj data?", "Che data è oggi?", "¿Qué fecha es hoy?",
                "Quelle est la date aujourd'hui?", "Jaké je dnes datum?")}),
    2895: (LIST + "; пример — будущее", {
        "t_ru": "ночевать, переночевать", "t_uk": "ночувати", "t_en": "to stay overnight", "t_tr": "gecelemek",
        "t_pl": "nocować", "t_it": "pernottare", "t_es": "pasar la noche", "t_fr": "passer la nuit",
        "x_ru": "Мы переночуем в отеле у озера", "x_uk": "Ми переночуємо в готелі біля озера"}),
    6897: ("«Я рекомендую тебе этот ресторан» — калька", {
        "x_ru": "Советую тебе этот ресторан", "x_en": "I'd recommend this restaurant"}),
    37: (DULL, {**all_x("Möchtest du einen Apfel?", "Хочешь яблоко?", "Хочеш яблуко?", "Would you like an apple?",
                        "Elma ister misin?", "Chcesz jabłko?", "Vuoi una mela?", "¿Quieres una manzana?",
                        "Tu veux une pomme?", "Chceš jablko?")}),
    201: (LIST + "; «электронное письмо» — книжно", {
        "t_ru": "имейл, электронное письмо", "t_uk": "імейл, електронний лист", "t_en": "email", "t_tr": "e-posta",
        "t_pl": "e-mail", "t_it": "l'e-mail", "t_es": "el correo electrónico", "t_fr": "l'e-mail, le mail",
        "x_ru": "Я пишу имейл", "x_uk": "Я пишу імейл", "x_en": "I'm writing an email"}),
    13968: ("пример переводит другую фразу: «позвоню вечером» в «Auf Wiederhören» нет", {
        "t_ru": "до свидания, до связи", "t_uk": "до побачення, до зв'язку", "t_en": "goodbye",
        "t_tr": "görüşmek üzere", "t_pl": "do usłyszenia",
        "x_ru": "До связи", "x_uk": "До зв'язку", "x_en": "Speak to you soon", "x_tr": "Görüşmek üzere",
        "x_pl": "Do usłyszenia"}),
}

SPLIT_LATER = {
    1191: ["ausmachen = договориться (einen Termin ausmachen)", "Das macht nichts aus = ничего страшного"],
}
