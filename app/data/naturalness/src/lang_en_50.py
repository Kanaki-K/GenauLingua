"""Вычитка английского, порция p050 (C2), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка английского: "

FIXES = {
    18386: (T + 'калька', {"example_en": 'The spare room still needs doing up before the guests arrive'}),
    18388: (T + 'повтор 16143 «kitchen after the party»', {"example_en": 'Your bedroom is a pigsty!'}),
    18474: (T + '«Hamburg» — без нужды', {"example_en": 'He is resident in Leeds'}),
    18908: (T + 'нет слова карточки «incessant»', {"example_en": 'The incessant noise from the building site is driving me mad'}),
}

REPLACE = []

SPLIT_LATER = {}
