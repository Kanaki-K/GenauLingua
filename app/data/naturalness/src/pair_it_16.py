"""Шаг 2, it, порция 16: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    8838: (T + "word in example", {"t_it": "il consiglio di amministrazione, la direzione, il direttivo"}),
}

REPLACE = []
SPLIT_LATER = {}
