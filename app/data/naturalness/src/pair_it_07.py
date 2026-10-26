"""Шаг 2, it, порция 7: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    109: (T + "word in example", {"t_it": "il movimento, l'attività fisica, (sich bewegen) muoversi"}),
    368: (T + "word in example", {"t_it": "mezzo, (halb drei) le due e mezza"}),
    449: (T + "word in example", {"t_it": "ogni, ognuno, (jeder zweite) uno su due"}),
    18109: (T + "word in example", {"t_it": "il pavimento, il terreno, (auf den Boden) per terra"}),
}

REPLACE = []
SPLIT_LATER = {}
