"""Шаг 2, tr, порция 19: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    10460: (T + "word in example", {"t_tr": "korkak, ürkek, endişeli"}),
    10834: (T + "word in example", {"t_tr": "ifşa etmek, söylemek, ihanet etmek"}),
    11229: (T + "word in example", {"t_tr": "çılgın, kaçık, (gaga sein) kafayı yemek"}),
    11352: (T + "word in example", {"t_tr": "sevilmeyen, (unbeliebt sein) pek sevilmemek"}),
    11673: (T + "word in example", {"t_tr": "besin, yiyecek, yem"}),
}

REPLACE = []
SPLIT_LATER = {}
