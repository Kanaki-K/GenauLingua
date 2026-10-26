"""Шаг 2, pl, порция 25: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    17516: (T + "word in example", {"t_pl": "przełączyć, przestawić, narzucić"}),
    18139: (T + "word in example", {"t_pl": "toaleta, ubikacja, kibel"}),
}

REPLACE = []
SPLIT_LATER = {}
