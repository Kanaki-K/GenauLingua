"""Шаг 2, es, порция 9: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    1645: (T + "word in example", {"t_es": "el camino en la vida, (auf seinem Lebensweg) a lo largo de su vida"}),
    1699: (T + "word in example", {"x_es": "Mi sobrino va a la escuela secundaria del pueblo"}),
}

REPLACE = []
SPLIT_LATER = {}
