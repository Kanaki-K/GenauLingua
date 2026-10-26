"""Шаг 2, tr, порция 24: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    15968: (T + "word in example", {"t_tr": "dava, duruşma, süreç"}),
    15970: (T + "word in example", {"t_tr": "mecbur, zoraki, (gezwungen sein) zorunda olmak"}),
    16045: (T + "word in example", {"t_tr": "form, durum, anayasa"}),
    16101: (T + "word in example", {"t_tr": "korumak, nöbet tutmak, göz kulak olmak"}),
    16103: (T + "word in example", {"t_tr": "duruşma, ifade alma, dinlenme"}),
    16136: (T + "word in example", {"x_tr": "Burada tam bir kaos hüküm sürüyor!"}),
}

REPLACE = []
SPLIT_LATER = {}
