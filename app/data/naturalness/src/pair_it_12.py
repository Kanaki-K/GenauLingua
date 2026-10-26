"""Шаг 2, it, порция 12: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    2573: (T + "word in example", {"t_it": "con, tramite, (+ gerundio) facendo"}),
    2596: (T + "word in example", {"t_it": "il candidato, la candidata, il concorrente"}),
    2614: (T + "word in example", {"t_it": "il commentatore (la commentatrice), l'opinionista, il telecronista"}),
}

REPLACE = []
SPLIT_LATER = {}
