"""Шаг 2, it, порция 21: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    13394: (T + "word in example", {"t_it": "dall'altra parte, di là", "x_it": "Vado un attimo di là dal vicino"}),
    13412: (T + "word in example", {"t_it": "insieme, l'uno con l'altro, tra loro", "x_it": "Dopo la lite quei due non parlano più tra loro"}),
    13483: (T + "word in example", {"x_it": "Non ho nessuna voglia di andare ancora a fare la spesa oggi"}),
}

REPLACE = []
SPLIT_LATER = {}
