"""Шаг 2, it, порция 1: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    96: (T + "word in example", {"t_it": "la professione, il mestiere, il lavoro"}),
    237: (T + "word in example", {"t_it": "lo, esso, (es ist kalt) fa freddo"}),
    328: (T + "word in example", {"t_it": "proprio ora, proprio adesso, appena"}),
}

REPLACE = []
SPLIT_LATER = {}
