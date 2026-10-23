"""Вычитка итальянского, порция p036 (B2), 23.10: кальки, повторы, нет слова карточки"""

T = "вычитка итальянского: "

FIXES = {
    16320: (T + 'повтор 15424 «il giardino come territorio»', {"example_it": 'I lupi difendono il loro territorio'}),
    17146: (T + '«La mia partenza è» — калька', {"example_it": 'La partenza è prevista domani alle sette'}),
    17153: (T + '«più lunga del previsto» — без ситуации', {"example_it": 'Sulla strada del ritorno ci siamo fermati a mangiare'}),
}

REPLACE = []

SPLIT_LATER = {}
