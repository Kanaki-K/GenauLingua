"""Шаг 2, es, порция 22: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    14945: (T + "word in example", {"t_es": "separado, por separado"}),
}

REPLACE = []
SPLIT_LATER = {}
