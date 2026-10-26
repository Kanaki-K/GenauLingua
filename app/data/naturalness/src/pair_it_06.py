"""Шаг 2, it, порция 6: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    6468: (T + "word in example", {"t_it": "mettersi d'accordo, accordarsi"}),
    7464: (T + "word in example", {"t_it": "il bene, il benessere, (zum Wohl!) salute!"}),
    10266: (T + "word in example", {"t_it": "drammatico, (dramatisieren) drammatizzare"}),
    13313: (T + "word in example", {"t_it": "nel, in"}),
    13338: (T + "word in example", {"t_it": "su questo, ci, (sich darauf freuen) non vedere l'ora"}),
    13384: (T + "word in example", {"x_it": "Ieri la mia bici è stata rubata davanti alla stazione"}),
}

REPLACE = []
SPLIT_LATER = {}
