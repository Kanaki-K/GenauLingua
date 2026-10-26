"""Шаг 2, it, порция 4: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    64: (T + "word in example", {"t_it": "inoltre, in più, per di più"}),
    98: (T + "word in example", {"t_it": "la risposta, (Bescheid sagen) far sapere"}),
    170: (T + "word in example", {"t_it": "con questo, inoltre, ci"}),
    325: (T + "word in example", {"t_it": "esattamente, esatto"}),
    459: (T + "word in example", {"t_it": "freddo, (kalt werden) freddarsi"}),
    730: (T + "word in example", {"t_it": "a, per, al"}),
    757: (T + "word in example", {"t_it": "il pensionato, (Rentner sein) essere in pensione"}),
    858: (T + "word in example", {"t_it": "il divertimento, (Spaß machen) essere divertente"}),
    993: (T + "word in example", {"t_it": "accanto, finito, passato"}),
    1011: (T + "word in example", {"t_it": "il bagno, la toilette, il WC"}),
    1064: (T + "word in example", {"t_it": "augurare, desiderare, volere"}),
    1070: (T + "word in example", {"t_it": "mostrare, far vedere"}),
}

REPLACE = []
SPLIT_LATER = {}
