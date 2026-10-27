"""Шаг 2, fr, порция 2: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример fr: "

FIXES = {
    554: (T + "в примере être couché", {"t_fr": "être posé, se trouver, être couché"}),
    664: (T + "в примере ne… que", {"t_fr": "seulement, ne… que"}),
    951: (T + "um sieben = à sept heures, не vers", {"x_fr": "On se retrouve à sept heures ?"}),
    1123: (T + "в примере tout le monde", {"t_fr": "tous, tout le monde"}),
}

REPLACE = []
SPLIT_LATER = {}
