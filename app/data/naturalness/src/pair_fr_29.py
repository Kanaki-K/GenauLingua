"""Шаг 2, fr, порция 29: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример fr: "

FIXES = {
    8909: (T + "в примере travailler comme", {"t_fr": "actif, employé, (tätig sein als) travailler comme"}),
    9167: (T + "в примере cadet", {"t_fr": "l'élève officier, le cadet"}),
    9266: (T + "в примере bénévolement", {"t_fr": "bénévole, bénévolement"}),
}

REPLACE = []
SPLIT_LATER = {}
