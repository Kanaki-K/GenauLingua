"""Шаг 2, tr, порция 31: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    10760: (T + "word in example", {"t_tr": "zaaf, eğilim, meyil"}),
    10792: (T + "word in example", {"t_tr": "dikkatsiz, pervasız, düşüncesiz"}),
    10897: (T + "word in example", {"x_tr": "Yeni pasaportumdaki fotoğraf pek de gurur verici değil"}),
    11227: (T + "word in example", {"t_tr": "somurtmak, küsmek, surat asmak"}),
    11353: (T + "word in example", {"t_tr": "iğrenç gelmek, çekilmez gelmek"}),
    11558: (T + "word in example", {"t_tr": "nazik, düşünceli, kibarca"}),
    11725: (T + "word in example", {"t_tr": "püskürtmek, fışkırmak, iğne yapmak"}),
}

REPLACE = []
SPLIT_LATER = {}
