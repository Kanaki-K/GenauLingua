"""Шаг 2, it, порция 19: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    10607: (T + "word in example", {"t_it": "il rimprovero, l'accusa, (Vorwürfe machen) rimproverare"}),
    10752: (T + "word in example", {"t_it": "vano, inutile, invano"}),
    11688: (T + "word in example", {"t_it": "il würstel, la salsiccia"}),
    11705: (T + "word in example", {"t_it": "il cibo per animali, il mangime, la fodera"}),
    11719: (T + "word in example", {"t_it": "macellare, uccidere, ammazzare"}),
    11732: (T + "word in example", {"t_it": "assetato, (durstig sein) avere sete"}),
    11891: (T + "word in example", {"t_it": "il rinfresco, la bevanda fresca, (zur Erfrischung) per rinfrescarsi"}),
}

REPLACE = []
SPLIT_LATER = {}
