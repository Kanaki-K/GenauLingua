"""Шаг 2, fr, порция 28: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример fr: "

FIXES = {
    7476: (T + "в примере mériter", {"t_fr": "revenir, être dû, mériter"}),
    7699: (T + "в примере parfaitement", {"t_fr": "excellent, parfait, parfaitement"}),
    8403: (T + "в примере l'un pour l'autre", {"t_fr": "l'un devant l'autre, l'un pour l'autre"}),
}

REPLACE = []
SPLIT_LATER = {}
