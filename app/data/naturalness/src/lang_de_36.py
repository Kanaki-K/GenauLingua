"""Вычитка немецкого, порция p036 (B2), 23.10: дорога — заглушки → бытовые фразы"""

W = "вычитка немецкого: учебная заглушка → живая бытовая фраза"

def ex(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"example_de": de, "example_ru": ru, "example_uk": uk, "example_en": en, "example_tr": tr,
            "example_pl": pl, "example_it": it, "example_es": es, "example_fr": fr, "example_cs": cs}

FIXES = {
    16326: (W, ex("Im Krimi findet die Spurensicherung immer irgendwo ein Haar",
        "В детективах криминалисты всегда где-нибудь находят волос", "У детективах криміналісти завжди десь знаходять волосину",
        "In crime dramas forensics always find a hair somewhere", "Polisiyelerde olay yeri inceleme ekibi hep bir yerde saç teli bulur",
        "W kryminałach technicy zawsze gdzieś znajdują włos", "Nei gialli la scientifica trova sempre un capello da qualche parte",
        "En las series policíacas la científica siempre encuentra un pelo en algún sitio", "Dans les polars, la police scientifique trouve toujours un cheveu quelque part",
        "V detektivkách technici vždycky někde najdou vlas")),
    17135: (W, ex("Das Navi hat uns schon wieder in eine Sackgasse geschickt",
        "Навигатор опять завёл нас в тупик", "Навігатор знову завів нас у глухий кут",
        "The satnav has sent us into a dead end again", "Navigasyon bizi yine çıkmaz sokağa soktu",
        "Nawigacja znowu wysłała nas w ślepą uliczkę", "Il navigatore ci ha mandati di nuovo in un vicolo cieco",
        "El GPS nos ha vuelto a meter en un callejón sin salida", "Le GPS nous a encore envoyés dans une impasse",
        "Navigace nás zase poslala do slepé ulice")),
    17186: (W, ex("Drück nicht ständig auf die Hupe, das nervt!",
        "Не дави всё время на клаксон, это раздражает!", "Не тисни весь час на клаксон, це дратує!",
        "Stop pressing the horn all the time, it's annoying!", "Sürekli kornaya basma, sinir bozucu!",
        "Nie naciskaj ciągle klaksonu, to denerwuje!", "Non suonare sempre il clacson, è fastidioso!",
        "¡No toques el claxon todo el rato, que molesta!", "Arrête d'appuyer sur le klaxon tout le temps, c'est énervant !",
        "Nemačkej pořád klakson, to leze na nervy!")),
}

REPLACE = []

SPLIT_LATER = {}
