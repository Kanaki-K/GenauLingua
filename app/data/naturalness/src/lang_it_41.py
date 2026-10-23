"""Вычитка итальянского, порция p041 (C1), 23.10: кальки, повторы, нет слова карточки"""

T = "вычитка итальянского: "

FIXES = {
    10772: (T + 'повтор 11883 «il caffè in ufficio»', {"example_it": 'Ha fatto un tempo orribile tutto il fine settimana'}),
    12766: (T + 'повтор 13061 «diabete … alimentazione»', {"example_it": 'Il diabete è sempre più diffuso tra i bambini'}),
}

REPLACE = []

SPLIT_LATER = {}
