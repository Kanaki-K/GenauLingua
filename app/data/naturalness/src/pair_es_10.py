"""Шаг 2, es, порция 10: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    1794: (T + "word in example", {"t_es": "de sobra, abundante, en abundancia"}),
    2039: (T + "word in example", {"x_es": "He extraviado las gafas y no las encuentro"}),
    2145: (T + "word in example", {"x_es": "Me ha llegado la cancelación del curso del sábado"}),
}

REPLACE = []
SPLIT_LATER = {}
