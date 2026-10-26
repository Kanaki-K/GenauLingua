"""Шаг 2, it, порция 15: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    6848: (T + "word in example", {"t_it": "delicato, dolce, con delicatezza"}),
    6880: (T + "word in example", {"t_it": "effettuare, svolgere, fare"}),
    6895: (T + "word in example", {"t_it": "l'opinione, la vista, (meiner Ansicht nach) a mio parere"}),
    6912: (T + "word in example", {"t_it": "il riferimento, il rapporto, la federa"}),
    6956: (T + "word in example", {"t_it": "a rischio, in pericolo, minacciato"}),
    7005: (T + "word in example", {"t_it": "sgarbato, approssimativo, (grob geschätzt) a occhio"}),
    7076: (T + "word in example", {"t_it": "storto, strano, spiovente"}),
    7124: (T + "word in example", {"t_it": "originale, iniziale, inizialmente"}),
    7291: (T + "word in example", {"t_it": "singolo, separato, singolarmente"}),
    7456: (T + "word in example", {"t_it": "non ufficiale, ufficioso, ufficiosamente"}),
    7594: (T + "word in example", {"t_it": "colorato, (farbig drucken) a colori"}),
}

REPLACE = []
SPLIT_LATER = {}
