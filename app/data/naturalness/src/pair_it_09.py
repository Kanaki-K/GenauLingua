"""Шаг 2, it, порция 9: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    1443: (T + "word in example", {"x_it": "Per le famiglie la città ha un'ampia offerta per il tempo libero"}),
    1576: (T + "word in example", {"t_it": "a quadri, a quadretti"}),
    1592: (T + "word in example", {"t_it": "il trifoglio, (vierblättriges Kleeblatt) il quadrifoglio"}),
    1594: (T + "word in example", {"t_it": "il piccolo mobile, il mobiletto"}),
    1645: (T + "word in example", {"x_it": "Nel suo percorso di vita mio nonno ha vissuto in cinque paesi"}),
    1699: (T + "word in example", {"x_it": "Dopo la scuola media ha iniziato un apprendistato"}),
    1700: (T + "word in example", {"t_it": "medio, di mezzo"}),
}

REPLACE = []
SPLIT_LATER = {}
