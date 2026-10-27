"""Шаг 2, es, порция 29: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    8909: (T + "word in example", {"t_es": "activo, empleado, (tätig sein als) trabajar como"}),
    9800: (T + "word in example", {"t_es": "la prima, el bonus"}),
}

REPLACE = []
SPLIT_LATER = {}
