"""Шаг 2, es, порция 12: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    2502: (T + "word in example", {"t_es": "la idea, el pensamiento, (der Gedanke an) pensar en"}),
    2652: (T + "word in example", {"t_es": "animado, vivo, vivamente"}),
}

REPLACE = []
SPLIT_LATER = {}
