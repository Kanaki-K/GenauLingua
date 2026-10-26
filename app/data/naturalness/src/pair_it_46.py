"""Шаг 2, it, порция 46: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    8663: (T + "word in example", {"t_it": "approfondito, dettagliato, a fondo"}),
    8689: (T + "word in example", {"t_it": "irrevocabile, definitivo, irrevocabilmente"}),
    9918: (T + "word in example", {"t_it": "ricchissimo, ricco sfondato (colloq.)"}),
    11215: (T + "word in example", {"x_it": "La mia dottoressa trova preoccupante la mia pressione alta"}),
}

REPLACE = []
SPLIT_LATER = {}
