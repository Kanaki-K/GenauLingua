"""Шаг 2, pl, порция 23: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    15409: (T + "word in example", {"t_pl": "obszar, teren, dziedzina"}),
    15459: (T + "word in example", {"t_pl": "świnia, locha, maciora"}),
    15686: (T + "word in example", {"t_pl": "burzliwy, sztormowy, sztormowo"}),
}

REPLACE = []
SPLIT_LATER = {}
