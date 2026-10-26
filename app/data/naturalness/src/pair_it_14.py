"""Шаг 2, it, порция 14: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    6398: (T + "word in example", {"t_it": "essere giusto, votare, (die Zahlen stimmen) tornare"}),
    6486: (T + "word in example", {"t_it": "fare la guardia, sorvegliare, vegliare"}),
    6506: (T + "word in example", {"t_it": "lo sforzo, la fatica, (sich Mühe geben) sforzarsi"}),
    6692: (T + "word in example", {"t_it": "farsi vivo, comparire, ricomparire"}),
    6761: (T + "word in example", {"t_it": "implicato, intricato, coinvolto"}),
    6784: (T + "word in example", {"t_it": "impiegare, usare, mettere in servizio"}),
}

REPLACE = []
SPLIT_LATER = {}
