"""Шаг 2, it, порция 20: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    12555: (T + "word in example", {"t_it": "l'iniezione, la siringa, la puntura"}),
    12595: (T + "word in example", {"t_it": "fisico, corporeo, fisicamente"}),
    12922: (T + "word in example", {"t_it": "il riflesso, (reflexartig) per riflesso"}),
}

REPLACE = []
SPLIT_LATER = {}
