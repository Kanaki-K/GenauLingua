"""Шаг 2, es, порция 23: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    15467: (T + "word in example", {"x_es": "Mi conejo es muy tierno"}),
}

REPLACE = []
SPLIT_LATER = {}
