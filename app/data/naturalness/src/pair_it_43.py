"""Шаг 2, it, порция 43: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    16398: (T + "word in example", {"t_it": "il tributo, il prezzo, (seinen Tribut fordern) presentare il conto"}),
    16430: (T + "word in example", {"t_it": "impunemente, (nicht ungestraft davonkommen) non passarla liscia"}),
    16559: (T + "word in example", {"t_it": "il cannone, il pezzo d'artiglieria, (schweres Geschütz) l'artiglieria pesante"}),
}

REPLACE = []
SPLIT_LATER = {}
