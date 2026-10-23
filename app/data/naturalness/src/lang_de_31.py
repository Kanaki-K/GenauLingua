"""Вычитка немецкого, порция p031 (B2), 23.10: заглушки → бытовые фразы"""

W = "вычитка немецкого: учебная заглушка → живая бытовая фраза"

def ex(de, ru, uk, en, tr, pl, it, es, fr, cs):
    return {"example_de": de, "example_ru": ru, "example_uk": uk, "example_en": en, "example_tr": tr,
            "example_pl": pl, "example_it": it, "example_es": es, "example_fr": fr, "example_cs": cs}

FIXES = {
    11725: (W + "; «Kellner spritzt Zitronensaft» — странно", ex("Pass auf, die Grapefruit spritzt beim Schneiden!",
        "Осторожно, грейпфрут брызгает, когда режешь!", "Обережно, грейпфрут бризкає, коли ріжеш!",
        "Careful, the grapefruit squirts when you cut it!", "Dikkat et, greyfurt keserken fışkırıyor!",
        "Uważaj, grejpfrut pryska przy krojeniu!", "Attento, il pompelmo schizza quando lo tagli!",
        "¡Cuidado, que el pomelo salpica al cortarlo!", "Attention, le pamplemousse gicle quand on le coupe !",
        "Pozor, grapefruit při krájení stříká!")),
}

REPLACE = []

SPLIT_LATER = {}
