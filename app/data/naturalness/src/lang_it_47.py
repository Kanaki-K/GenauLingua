"""Вычитка итальянского, порция p047 (C2), 23.10: кальки, повторы, нет слова карточки"""

T = "вычитка итальянского: "

FIXES = {
    11610: (T + 'повтор 10345 «idea stupida»', {"example_it": 'Che idea scema!'}),
    11613: (T + '«volentieri» — калька', {"example_it": 'È un vero filantropo, aiuta tutti'}),
    11956: (T + 'без ситуации', {"example_it": "Prendiamo l'aperitivo in terrazza?"}),
    11997: (T + 'повтор 11677 «dopo mangiato beviamo»', {"example_it": 'Il nonno offre sempre un bicchiere di porto agli ospiti'}),
    12945: (T + 'учебниково', {"example_it": 'Una temperatura corporea di 37 gradi è normale'}),
    13124: (T + 'повтор 6944 «postumi della sbornia terribili»', {"example_it": 'Il giorno dopo il matrimonio erano tutti con i postumi della sbornia'}),
}

REPLACE = []

SPLIT_LATER = {}
