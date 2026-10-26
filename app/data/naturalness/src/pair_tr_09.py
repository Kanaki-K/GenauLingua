"""Шаг 2, tr, порция 9: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    1485: (T + "word in example", {"t_tr": "sağlık açısından, sağlık olarak"}),
    1487: (T + "word in example", {"t_tr": "alçılı bacak, (ein Gipsbein haben) bacağı alçıda olmak"}),
    1659: (T + "word in example", {"t_tr": "kıvırcık, kıvır kıvır"}),
    1667: (T + "word in example", {"t_tr": "mail atmak, e-posta göndermek"}),
    1700: (T + "word in example", {"t_tr": "orta, ortanca"}),
}

REPLACE = []
SPLIT_LATER = {}
