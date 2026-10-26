"""Шаг 2, pl, порция 1: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    88: (T + "word in example", {"t_pl": "oba, obie, oboje"}),
    293: (T + "word in example", {"t_pl": "zadowolony, rad, (froh sein) cieszyć się"}),
    428: (T + "word in example", {"t_pl": "jej, ich, swój"}),
}

REPLACE = []
SPLIT_LATER = {}
