"""Шаг 2, es, порция 2: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    649: (T + "word in example", {"t_es": "tomar, (en el restaurante) querer"}),
    684: (T + "word in example", {"t_es": "el lugar, el sitio, el pueblo"}),
    763: (T + "word in example", {"t_es": "correcto, bien"}),
    1091: (T + "word in example", {"t_es": "sobre, encima de, de"}),
    1316: (T + "word in example", {"t_es": "para que, para"}),
}

REPLACE = []
SPLIT_LATER = {}
