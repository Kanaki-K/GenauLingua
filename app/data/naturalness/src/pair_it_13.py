"""Шаг 2, it, порция 13: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    2763: (T + "word in example", {"t_it": "il reporter, il cronista, il giornalista"}),
    2770: (T + "word in example", {"x_it": "La polizia mi ha fermato perché il fanale posteriore della mia bici non funziona"}),
    2824: (T + "word in example", {"t_it": "il sole, la luce del sole, (affettuoso) raggio di sole"}),
    2828: (T + "word in example", {"t_it": "la preoccupazione, (sich Sorgen machen) preoccuparsi"}),
    2909: (T + "word in example", {"t_it": "il rapporto, la gestione, l'uso"}),
    2925: (T + "word in example", {"t_it": "inutile, superfluo, inutilmente"}),
}

REPLACE = []
SPLIT_LATER = {}
