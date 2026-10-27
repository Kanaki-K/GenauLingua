"""Шаг 2, fr, порция 4: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример fr: "

FIXES = {
    98: (T + "в примере prévenir", {"t_fr": "la réponse, l'avis, (Bescheid sagen) prévenir"}),
    757: (T + "нет retraité", {"x_fr": "Mon père est retraité depuis l'année dernière"}),
    858: (T + "в примере amusant", {"t_fr": "le plaisir, l'amusement, (Spaß machen) être amusant"}),
}

REPLACE = []
SPLIT_LATER = {}
