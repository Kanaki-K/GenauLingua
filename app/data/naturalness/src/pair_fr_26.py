"""Шаг 2, fr, порция 26: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример fr: "

FIXES = {
    2043: (T + "в примере pour prévenir", {"t_fr": "la prévention, (zur Vermeidung) pour prévenir"}),
    6550: (T + "в примере fuir", {"t_fr": "qui fuit, percé, (leck sein) fuir"}),
    7090: (T + "в примере infiniment", {"t_fr": "infini, sans fin, infiniment"}),
}

REPLACE = []
SPLIT_LATER = {}
