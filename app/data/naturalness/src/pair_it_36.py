"""Шаг 2, it, порция 36: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    16853: (T + "word in example", {"x_it": "Durante la visita al vecchio castello i bambini hanno potuto sedersi nella cella di sicurezza e spaventarsi un po'"}),
    16928: (T + "word in example", {"t_it": "commettere, compiere, (Streiche verüben) combinare"}),
    17165: (T + "word in example", {"t_it": "lo schianto, il crollo, il crash"}),
}

REPLACE = []
SPLIT_LATER = {}
