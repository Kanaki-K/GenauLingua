"""Шаг 2, fr, порция 24: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример fr: "

FIXES = {
    16025: (T + "в примере illégalement", {"t_fr": "illégal, illégalement"}),
    16230: (T + "в примере le règlement", {"t_fr": "la règle, la consigne, le règlement"}),
    16345: (T + "в примере garder une place", {"t_fr": "occuper, pourvoir, (einen Platz besetzen) garder une place"}),
}

REPLACE = []
SPLIT_LATER = {}
