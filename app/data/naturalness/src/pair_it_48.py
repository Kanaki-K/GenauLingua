"""Шаг 2, it, порция 48: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    15322: (T + "word in example", {"t_it": "il concepimento, la concezione"}),
}

REPLACE = []
SPLIT_LATER = {}
