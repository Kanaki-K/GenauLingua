"""Шаг 2, fr, порция 12: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример fr: "

FIXES = {
    2521: (T + "в примере légalement", {"t_fr": "par la loi, légal, légalement"}),
}

REPLACE = []
SPLIT_LATER = {}
