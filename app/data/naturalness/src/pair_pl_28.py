"""Шаг 2, pl, порция 28: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    8399: (T + "word in example", {"t_pl": "zakwaterowany, ulokowany, (bei jemandem untergekommen) mieszkać u kogoś"}),
}

REPLACE = []
SPLIT_LATER = {}
