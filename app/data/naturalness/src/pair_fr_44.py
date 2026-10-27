"""Шаг 2, fr, порция 44: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример fr: "

FIXES = {
    17240: (T + "в примере faire une chute", {"t_fr": "planter, s'écraser, faire une chute"}),
    17830: (T + "в примере ruiner", {"t_fr": "la ruine, (jemandes Ruin sein) ruiner"}),
}

REPLACE = []
SPLIT_LATER = {}
