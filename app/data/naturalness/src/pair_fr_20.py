"""Шаг 2, fr, порция 20: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример fr: "

FIXES = {
    12156: (T + "в примере faire de la plongée", {"t_fr": "plonger, faire de la plongée"}),
    12535: (T + "в примере s'évanouir", {"t_fr": "évanoui, impuissant, s'évanouir"}),
    12595: (T + "в примере physiquement", {"t_fr": "physique, corporel, physiquement"}),
}

REPLACE = []
SPLIT_LATER = {}
