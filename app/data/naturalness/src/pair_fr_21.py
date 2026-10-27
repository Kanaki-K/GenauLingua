"""Шаг 2, fr, порция 21: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример fr: "

FIXES = {
    13342: (T + "нет dedans", {"x_fr": "Qu'est-ce qu'il y a dedans, dans le sac ?"}),
    13394: (T + "в примере passer", {"t_fr": "par ici, de l'autre côté, (rübergehen) passer"}),
    13412: (T + "в примере se parler", {"t_fr": "ensemble, l'un avec l'autre, (miteinander reden) se parler"}),
    13884: (T + "в примере idiot, нет bêtise", {"x_fr": "Quelle bêtise !"}),
}

REPLACE = []
SPLIT_LATER = {}
