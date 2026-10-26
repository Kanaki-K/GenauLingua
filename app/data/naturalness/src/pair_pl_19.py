"""Шаг 2, pl, порция 19: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    11229: (T + "word in example", {"t_pl": "zwariowany, stuknięty, (gaga sein) zwariować"}),
    11719: (T + "word in example", {"t_pl": "ubijać, zarzynać, zabijać"}),
    11825: (T + "word in example", {"t_pl": "wanilia, (Vanilleeis) waniliowe"}),
}

REPLACE = []
SPLIT_LATER = {}
