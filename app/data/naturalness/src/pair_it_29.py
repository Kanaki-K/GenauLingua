"""Шаг 2, it, порция 29: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    8909: (T + "word in example", {"t_it": "attivo, impiegato, (tätig sein als) lavorare come"}),
    8920: (T + "word in example", {"t_it": "la direzione, la gestione, il management"}),
}

REPLACE = []
SPLIT_LATER = {}
