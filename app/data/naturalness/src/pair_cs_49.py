"""Шаг 2, cs, порция 49: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    16811: (T + "в примере recidivoval", {"t_cs": "recidivní, (rückfällig werden) recidivovat"}),
    16850: (T + "в примере apel", {"t_cs": "obhajoba, závěrečná řeč, (přen.) vášnivý apel"}),
    17378: (T + "в примере zastavíme se", {"t_cs": "zastávka, mezipřistání, (einen Zwischenstopp machen) zastavit se"}),
}

REPLACE = []
SPLIT_LATER = {}
