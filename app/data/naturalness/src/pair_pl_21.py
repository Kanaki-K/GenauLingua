"""Шаг 2, pl, порция 21: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    13394: (T + "word in example", {"t_pl": "na drugą stronę, tutaj, (rübergehen) skoczyć do kogoś"}),
    13483: (T + "word in example", {"t_pl": "żaden, ani trochę, najmniejszy"}),
    13631: (T + "word in example", {"t_pl": "goły, nagi, nago"}),
    13888: (T + "word in example", {"t_pl": "wiadomość, przesłanie, ambasada"}),
}

REPLACE = []
SPLIT_LATER = {}
