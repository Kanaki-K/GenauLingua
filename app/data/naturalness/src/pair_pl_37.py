"""Шаг 2, pl, порция 37: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    17594: (T + "word in example", {"t_pl": "zapłon, (Schlüssel in der Zündung) stacyjka"}),
    17813: (T + "word in example", {"t_pl": "zbankrutowany, niewypłacalny, (bankrott gehen) zbankrutować"}),
    18076: (T + "word in example", {"t_pl": "przepowiednia, prognoza, typ (zakład)"}),
    18243: (T + "word in example", {"t_pl": "bulwar, prasa bulwarowa, brukowce"}),
}

REPLACE = []
SPLIT_LATER = {}
