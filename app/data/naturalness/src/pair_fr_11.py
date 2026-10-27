"""Шаг 2, fr, порция 11: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример fr: "

FIXES = {
    2217: (T + "в примере attentivement", {"t_fr": "attentif, attentionné, attentivement"}),
    2339: (T + "в примере c'est pour ça", {"t_fr": "donc, c'est pourquoi, c'est pour ça"}),
}

REPLACE = []
SPLIT_LATER = {}
