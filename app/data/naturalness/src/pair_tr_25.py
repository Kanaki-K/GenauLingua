"""Шаг 2, tr, порция 25: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    17247: (T + "word in example", {"t_tr": "sollamak, geçmek, bakımdan geçirmek"}),
    17370: (T + "word in example", {"t_tr": "kadın şoför, şoför"}),
    17496: (T + "word in example", {"t_tr": "kayıt, çekim, fotoğraf"}),
    17503: (T + "word in example", {"t_tr": "yerini tespit etmek, konumunu bulmak, izini sürmek"}),
    17992: (T + "word in example", {"x_tr": "On kilometre yarıçapında hiç süpermarket yok"}),
    18191: (T + "word in example", {"t_tr": "konaklama yeri, kalacak yer, mahalle"}),
}

REPLACE = []
SPLIT_LATER = {}
