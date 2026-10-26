"""Шаг 2, tr, порция 35: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    15229: (T + "word in example", {"t_tr": "üst beden, belden yukarısı"}),
    15311: (T + "word in example", {"t_tr": "aman Tanrım, vay canına, hay Allah"}),
    15526: (T + "word in example", {"t_tr": "uğuldamak, hışırdamak, gürültüyle akmak"}),
    15591: (T + "word in example", {"x_tr": "İkisinin evleneceğini artık serçeler bile biliyor"}),
    15961: (T + "word in example", {"t_tr": "Majesteleri, Hazretleri, egemenlik"}),
    16174: (T + "word in example", {"t_tr": "cinayet, suikast, öldürülme"}),
    16181: (T + "word in example", {"t_tr": "gözaltı, muhafaza, emanet"}),
    16190: (T + "word in example", {"t_tr": "sorgulamak, (sich verhören) yanlış duymak"}),
    16263: (T + "word in example", {"t_tr": "tanıklık etmek, şahitlik etmek"}),
}

REPLACE = []
SPLIT_LATER = {}
