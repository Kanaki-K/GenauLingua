"""Шаг 2, es, порция 21: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    13394: (T + "word in example", {"x_es": "Voy un momento al otro lado, a casa del vecino"}),
    13412: (T + "word in example", {"t_es": "entre sí, juntos"}),
    13451: (T + "word in example", {"t_es": "el uno al otro, mutuamente, entre sí"}),
    13861: (T + "word in example", {"t_es": "sí señor, por supuesto, a sus órdenes"}),
}

REPLACE = []
SPLIT_LATER = {}
