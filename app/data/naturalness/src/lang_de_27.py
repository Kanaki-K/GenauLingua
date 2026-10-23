"""Вычитка немецкого, порция p027 (B2), 23.10: заглушки и канцелярит → живые бытовые фразы"""

W = "вычитка немецкого: учебная заглушка → живая бытовая фраза"

def ex(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"example_de": de, "example_ru": ru, "example_uk": uk, "example_en": en, "example_tr": tr,
            "example_pl": pl, "example_it": it, "example_es": es, "example_fr": fr, "example_cs": cs}

FIXES = {
    7102: (W + "; «Das Geld kommt mir zu» — непонятно", ex("Mit dem Umzug kommt eine Menge Arbeit auf uns zu",
        "С переездом нас ждёт куча работы", "З переїздом на нас чекає купа роботи",
        "With the move there's a lot of work coming our way", "Taşınmayla birlikte bizi bir sürü iş bekliyor",
        "Z przeprowadzką czeka nas mnóstwo pracy", "Con il trasloco ci aspetta un sacco di lavoro",
        "Con la mudanza se nos viene encima un montón de trabajo", "Avec le déménagement, beaucoup de travail nous attend",
        "Se stěhováním nás čeká spousta práce")),
    7108: (W + "; «Ich gewähre dir» — так не говорят", ex("Der Laden gewährt Studenten zehn Prozent Rabatt",
        "Магазин предоставляет студентам скидку десять процентов", "Магазин надає студентам знижку десять відсотків",
        "The shop gives students a ten per cent discount", "Mağaza öğrencilere yüzde on indirim yapıyor",
        "Sklep daje studentom dziesięć procent zniżki", "Il negozio concede agli studenti il dieci per cento di sconto",
        "La tienda hace un diez por ciento de descuento a los estudiantes", "Le magasin accorde dix pour cent de réduction aux étudiants",
        "Obchod poskytuje studentům desetiprocentní slevu")),
    7120: (W, ex("Meine Eltern billigen meine Entscheidung nicht",
        "Мои родители не одобряют моё решение", "Мої батьки не схвалюють мого рішення",
        "My parents don't approve of my decision", "Annemle babam kararımı onaylamıyor",
        "Moi rodzice nie pochwalają mojej decyzji", "I miei genitori non approvano la mia decisione",
        "Mis padres no aprueban mi decisión", "Mes parents n'approuvent pas ma décision",
        "Moji rodiče neschvalují moje rozhodnutí")),
    7176: (W, ex("Ein ehrliches Gespräch kann manchmal Wunder bewirken",
        "Честный разговор иногда творит чудеса", "Чесна розмова іноді творить дива",
        "An honest conversation can sometimes work wonders", "Dürüst bir konuşma bazen mucizeler yaratabilir",
        "Szczera rozmowa czasem potrafi zdziałać cuda", "Una conversazione sincera a volte fa miracoli",
        "Una conversación sincera a veces hace milagros", "Une conversation honnête peut parfois faire des miracles",
        "Upřímný rozhovor někdy dokáže zázraky")),
    7216: (W, ex("Lauf schneller, sonst holen uns die anderen ein!",
        "Беги быстрее, а то другие нас догонят!", "Біжи швидше, бо інші нас доженуть!",
        "Run faster or the others will catch up with us!", "Daha hızlı koş, yoksa diğerleri bize yetişecek!",
        "Biegnij szybciej, bo inni nas dogonią!", "Corri più veloce, sennò gli altri ci raggiungono!",
        "¡Corre más, que si no nos alcanzan los otros!", "Cours plus vite, sinon les autres vont nous rattraper !",
        "Běž rychleji, nebo nás ostatní doženou!")),
}

REPLACE = []

SPLIT_LATER = {}
