"""Шаг 2, it, порция 40: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    9887: (T + "word in example", {"x_it": "La vera amicizia non è in vendita"}),
    10873: (T + "word in example", {"t_it": "la risata, (für Lacher sorgen) far ridere"}),
}

REPLACE = []
SPLIT_LATER = {}
