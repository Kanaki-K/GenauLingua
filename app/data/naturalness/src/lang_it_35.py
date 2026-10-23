"""Вычитка итальянского, порция p035 (B2), 23.10: кальки, повторы, нет слова карточки"""

T = "вычитка итальянского: "

FIXES = {
    15312: (T + '«a Berlino» — без нужды', {"example_it": 'Sua figliastra ora studia a Bologna'}),
    16150: (T + 'нет слова карточки «la bandiera»', {"example_it": 'I tifosi sventolano le bandiere allo stadio'}),
    16182: (T + '«Devi firmare» — калька', {"example_it": 'Firmi qui, per favore'}),
    16183: (T + '«Vogliono accusarlo» — калька', {"example_it": 'Lo accusano di furto, ma non ha fatto niente'}),
    16186: (T + '«questo avrebbe portato» — книжно', {"example_it": "Dopo l'attacco voleva vendetta, ma così avrebbe solo creato altri problemi"}),
    16198: (T + 'повтор 16189 «passaporto falso»', {"example_it": 'Una borsa Chanel a 30 euro è per forza una contraffazione'}),
    16206: (T + '«per il suo cattivo comportamento» — книжно', {"example_it": 'Per punizione niente telefono per una settimana'}),
    16256: (T + '«Il codice regola il comportamento» — книжно', {"example_it": "Tra i motociclisti c'è un codice d'onore"}),
}

REPLACE = []

SPLIT_LATER = {}
