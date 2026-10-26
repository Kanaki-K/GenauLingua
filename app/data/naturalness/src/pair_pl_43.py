"""Шаг 2, pl, порция 43: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    15648: (T + "word in example", {"t_pl": "zamarznięty, mrożony, (gefroren sein) zamarznąć"}),
    16398: (T + "word in example", {"t_pl": "danina, cena, (Tribut fordern) zbierać żniwo"}),
    16424: (T + "word in example", {"t_pl": "zabicie, uśmiercenie, zabijanie"}),
}

REPLACE = []
SPLIT_LATER = {}
