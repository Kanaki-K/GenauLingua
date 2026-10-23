"""Вычитка английского, порция p028 (B2), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка английского: "

FIXES = {
    7476: (T + 'книжно', {"example_en": 'All the credit is due to him'}),
    7509: (T + 'без ситуации', {"example_en": 'His words caused me a lot of pain'}),
    7818: (T + 'книжно', {"example_en": 'Your idea borders on madness!'}),
    8113: (T + 'странно', {"example_en": 'On the phone he disguised his voice to play a joke on me'}),
    8116: (T + 'книжно', {"example_en": 'I got mixed up in their argument without meaning to'}),
}

REPLACE = []

SPLIT_LATER = {}
