"""Шаг 2, tr, порция 34: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    14522: (T + "word in example", {"t_tr": "saga, destan, seri"}),
    14653: (T + "word in example", {"t_tr": "yaratmak, icat etmek"}),
    15080: (T + "word in example", {"t_tr": "büyütmek, yetiştirmek, kurmak"}),
    15102: (T + "word in example", {"t_tr": "evlat edinme, sahiplenme, benimseme"}),
}

REPLACE = []
SPLIT_LATER = {}
