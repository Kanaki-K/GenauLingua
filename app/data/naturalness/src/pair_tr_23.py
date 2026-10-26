"""Шаг 2, tr, порция 23: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    15243: (T + "word in example", {"x_tr": "Bu kadar küçük bir ufaklık ama ne kadar da yaramaz!"}),
    15448: (T + "word in example", {"t_tr": "cangıl, yağmur ormanı, balta girmemiş orman"}),
}

REPLACE = []
SPLIT_LATER = {}
