"""Шаг 2, it, порция 17: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    9220: (T + "word in example", {"x_it": "Prima del matrimonio è stata tutta la mattina al centro estetico"}),
    9781: (T + "word in example", {"t_it": "mendicare, supplicare, elemosinare"}),
}

REPLACE = []
SPLIT_LATER = {}
