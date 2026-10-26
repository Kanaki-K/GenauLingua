"""Шаг 2, it, порция 11: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    2205: (T + "word in example", {"t_it": "fastidioso, irritato, (wie ärgerlich!) che fastidio"}),
    2217: (T + "word in example", {"t_it": "attento, premuroso, con attenzione"}),
    2220: (T + "word in example", {"t_it": "annotare, segnare, scrivere"}),
    2223: (T + "word in example", {"t_it": "l'incarico, l'ordine, il lavoro"}),
    2297: (T + "word in example", {"t_it": "l'abitante, il residente, l'inquilino"}),
    2438: (T + "word in example", {"t_it": "menzionare, citare, accennare"}),
}

REPLACE = []
SPLIT_LATER = {}
