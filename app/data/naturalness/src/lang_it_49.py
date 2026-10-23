"""Вычитка итальянского, порция p049 (C2), 23.10: кальки, повторы, нет слова карточки"""

T = "вычитка итальянского: "

FIXES = {
    16906: (T + '«scrivono volentieri» — калька', {"example_it": 'I giornali scandalistici scrivono spesso «pedofilo», la polizia preferisce parlare di autori di abusi'}),
    16932: (T + '«È necessaria una revisione» — канцелярит', {"example_it": "L'avvocato chiede la revisione del processo"}),
    17315: (T + 'повтор 6493 «vai avanti, ti raggiungo»', {"example_it": 'Partite pure, vi raggiungiamo in macchina'}),
    17386: (T + '«a Berlino» — без нужды', {"example_it": 'Domani torniamo in aereo a Palermo'}),
    17680: (T + 'повтор 17746 «rileva il movimento e accende la luce»', {"example_it": 'Il sensore di pioggia accende da solo i tergicristalli'}),
    17726: (T + 'учебниково', {"example_it": 'Questo canale televisivo trasmette solo serie'}),
}

REPLACE = []

SPLIT_LATER = {}
