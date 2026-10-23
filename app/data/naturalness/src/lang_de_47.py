"""Вычитка немецкого, порция p047 (C2), 23.10: заглушки → бытовые; близнец gefüllt (7052)"""

W = "вычитка немецкого: учебная заглушка → живая бытовая фраза"

def ex(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"example_de": de, "example_ru": ru, "example_uk": uk, "example_en": en, "example_tr": tr,
            "example_pl": pl, "example_it": it, "example_es": es, "example_fr": fr, "example_cs": cs}

FIXES = {
    11938: (W, ex("Schlürf nicht so laut, das ist unhöflich!",
        "Не хлебай так громко, это невежливо!", "Не сьорбай так голосно, це неввічливо!",
        "Don't slurp so loudly, it's rude!", "Öyle sesli höpürdetme, ayıp!",
        "Nie siorb tak głośno, to niegrzeczne!", "Non fare rumore quando bevi, è maleducato!",
        "¡No sorbas tan fuerte, que es de mala educación!", "Ne fais pas autant de bruit en aspirant, c'est malpoli !",
        "Nesrkej tak nahlas, to je neslušné!")),
    11957: (W + "; почти повтор gefüllt (7052)", ex("Zum Nachtisch gibt es mit Vanillecreme gefüllte Pfannkuchen",
        "На десерт будут блинчики, наполненные ванильным кремом", "На десерт будуть млинці, наповнені ванільним кремом",
        "For dessert there are pancakes filled with vanilla cream", "Tatlı olarak vanilyalı krema dolgulu krep var",
        "Na deser są naleśniki nadziewane kremem waniliowym", "Per dessert ci sono crêpe ripiene di crema alla vaniglia",
        "De postre hay crepes rellenos de crema de vainilla", "En dessert, il y a des crêpes fourrées à la crème vanille",
        "Jako dezert jsou palačinky plněné vanilkovým krémem")),
}

REPLACE = []

SPLIT_LATER = {}
