"""Вычитка английского, порция p037 (B2), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка английского: "

FIXES = {
    17557: (T + 'калька', {"example_en": 'Push the lever to the left'}),
    17958: (T + 'повтор 17956 «scientists»', {"example_en": 'I love exploring the back streets of cities I visit'}),
    18183: (T + 'не тот смысл', {"example_en": 'He rents a little pad near the university'}),
    18217: (T + 'повтор 18385 «change the sheets»', {"example_en": 'The sheets are drying on the balcony'}),
    18235: (T + 'повтор 6519 «shelter from the rain»', {"example_en": 'The shed at the bottom of the garden is our hideout'}),
}

REPLACE = []

SPLIT_LATER = {}
