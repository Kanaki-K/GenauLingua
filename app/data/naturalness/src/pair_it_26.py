"""Шаг 2, it, порция 26: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    7088: (T + "word in example", {"t_it": "introdursi, penetrare, entrare"}),
    7090: (T + "word in example", {"t_it": "infinito, infinitamente"}),
    19030: (T + "word in example", {"x_it": "La ritengo una buona idea, proviamoci!"}),
}

REPLACE = []
SPLIT_LATER = {}
