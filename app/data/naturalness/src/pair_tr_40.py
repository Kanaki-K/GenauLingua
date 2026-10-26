"""Шаг 2, tr, порция 40: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    9885: (T + "word in example", {"t_tr": "bolluk, fazlalık, (im Überfluss) bol"}),
    10854: (T + "word in example", {"t_tr": "hissettirmek, (sich anfühlen wie) dokununca … gibi gelmek"}),
    10983: (T + "word in example", {"t_tr": "yıldırmak, (sich nicht unterkriegen lassen) yılmamak"}),
}

REPLACE = []
SPLIT_LATER = {}
