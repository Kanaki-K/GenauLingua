"""Шаг 2, it, порция 2: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    554: (T + "word in example", {"t_it": "stare, trovarsi, stare sdraiato"}),
    920: (T + "word in example", {"t_it": "telefonare, parlare al telefono"}),
    949: (T + "word in example", {"t_it": "l'orologio, l'ora, (drei Uhr) le tre"}),
    951: (T + "word in example", {"t_it": "a, intorno a, verso"}),
    1160: (T + "word in example", {"t_it": "il posto di lavoro, la postazione"}),
}

REPLACE = []
SPLIT_LATER = {}
