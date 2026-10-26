"""Шаг 2, tr, порция 33: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    12887: (T + "word in example", {"t_tr": "esrar içmek, esrar çekmek"}),
    12910: (T + "word in example", {"t_tr": "yanık, yakma"}),
    13527: (T + "word in example", {"x_tr": "Bu ise yine başka bir sorun"}),
    13543: (T + "word in example", {"t_tr": "rağmen, karşı, (wider Erwarten) beklenenin aksine"}),
    14024: (T + "word in example", {"t_tr": "aydınlatmak, çözmek"}),
}

REPLACE = []
SPLIT_LATER = {}
