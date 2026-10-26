"""Шаг 2, it, порция 23: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    15646: (T + "word in example", {"x_it": "Quel vecchio ronzino non riesce più a tirare il carro"}),
}

REPLACE = []
SPLIT_LATER = {}
