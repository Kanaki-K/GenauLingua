"""Шаг 2, es, порция 7: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    109: (T + "word in example", {"x_es": "Necesito hacer más ejercicio, me paso el día sentado"}),
    381: (T + "word in example", {"x_es": "¡Lo principal es que estés bien de salud!"}),
}

REPLACE = []
SPLIT_LATER = {}
