"""Шаг 2, tr, порция 36: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    16304: (T + "word in example", {"t_tr": "tutukluluk, gözaltı, ıslahevi cezası"}),
    17158: (T + "word in example", {"t_tr": "varmak, gelmek, gerçekleşmek"}),
}

REPLACE = []
SPLIT_LATER = {}
