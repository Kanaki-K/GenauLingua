"""Вычитка итальянского, порция p050 (C2), 23.10: кальки, повторы, нет слова карточки"""

T = "вычитка итальянского: "

FIXES = {
    18058: (T + '«legge volentieri» — калька', {"example_it": "I gialli sono l'unico genere letterario che mio padre legge"}),
    18386: (T + '«Devo ancora» — калька', {"example_it": 'Bisogna ancora sistemare la camera degli ospiti'}),
    18388: (T + 'повтор 16143 «dopo la festa la cucina sembra»', {"example_it": 'La tua camera è un vero porcile!'}),
    18908: (T + 'нет слова карточки «incessante»', {"example_it": 'Il rumore incessante dei lavori mi fa impazzire'}),
}

REPLACE = []

SPLIT_LATER = {}
