"""Шаг 2, cs, порция 25: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    17637: (T + "в примере digitálně", {"t_cs": "digitální, digitálně"}),
    17970: (T + "в примере počítá, не vypočítat", {"x_cs": "Na trhu prodavač vypočítá cenu podle hmotnosti"}),
}

REPLACE = []
SPLIT_LATER = {}
