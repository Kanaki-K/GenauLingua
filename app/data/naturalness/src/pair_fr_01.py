"""Шаг 2, fr, порция 1: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример fr: "

FIXES = {
    254: (T + "в примере situation familiale", {"t_fr": "la situation familiale, l'état civil"}),
}

REPLACE = []
SPLIT_LATER = {}
