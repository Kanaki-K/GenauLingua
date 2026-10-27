"""Шаг 2, cs, порция 48: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    14320: (T + "в примере věru", {"t_cs": "vskutku, opravdu, věru"}),
    15855: (T + "в примере zkrotili", {"t_cs": "zkrocený, ochočený, (zähmen) zkrotit"}),
}

REPLACE = []
SPLIT_LATER = {}
