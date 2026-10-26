"""Шаг 2, it, порция 37: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    17964: (T + "word in example", {"t_it": "scientifico, scientificamente"}),
    18034: (T + "word in example", {"t_it": "la scientifica, le scienze forensi"}),
    18243: (T + "word in example", {"x_it": "La sera passeggiamo lungo il viale fino al lago"}),
}

REPLACE = []
SPLIT_LATER = {}
