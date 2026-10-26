"""Шаг 2, pl, порция 7: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    12: (T + "word in example", {"t_pl": "codzienność, dzień powszedni, (im Alltag) na co dzień"}),
    115: (T + "word in example", {"t_pl": "tworzyć, utworzyć, formować"}),
    368: (T + "word in example", {"t_pl": "pół, w połowie, (halb drei) wpół do trzeciej"}),
    449: (T + "word in example", {"t_pl": "każdy (każda, każde), (jeder zweite) co drugi"}),
    505: (T + "word in example", {"t_pl": "ból głowy, boli głowa"}),
}

REPLACE = []
SPLIT_LATER = {}
