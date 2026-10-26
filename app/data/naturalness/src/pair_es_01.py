"""Шаг 2, es, порция 1: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    29: (T + "word in example", {"t_es": "el tratamiento, el saludo, la forma de dirigirse"}),
}

REPLACE = []
SPLIT_LATER = {}
