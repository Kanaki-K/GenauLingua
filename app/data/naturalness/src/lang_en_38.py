"""Вычитка английского, порция p038 (B2/C1), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка английского: "

FIXES = {
    18663: (T + 'повтор 18922 «rest after eating»', {"example_en": "Let him rest, he's ill"}),
    18728: (T + 'калька', {"example_en": 'In the morning I have my little routine: coffee, shower, paper'}),
    18747: (T + 'повтор 18772 «fishing at dawn»', {"example_en": 'We set off at dawn to avoid the traffic'}),
    18810: (T + '«in Berlin» — без нужды', {"example_en": 'I lived in London for a while, but in the long run the city was too loud for me'}),
    7668: (T + 'калька', {"example_en": 'Reading without glasses strains my eyes'}),
}

REPLACE = []

SPLIT_LATER = {}
