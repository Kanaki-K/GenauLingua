"""Шаг 2, it, порция 10: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    1900: (T + "word in example", {"t_it": "avviarsi, partire, decollare"}),
    2039: (T + "word in example", {"t_it": "rinviare, smarrire, mettere da qualche parte"}),
    2049: (T + "word in example", {"t_it": "pazzo, folle, (verrückt werden) impazzire"}),
    2145: (T + "word in example", {"t_it": "il rifiuto, la disdetta, (eine Absage erteilen) disdire"}),
}

REPLACE = []
SPLIT_LATER = {}
