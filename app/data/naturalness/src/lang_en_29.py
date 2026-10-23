"""Вычитка английского, порция p029 (B2), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка английского: "

FIXES = {
    8886: (T + 'коряво', {"example_en": "The band's producer is also their manager"}),
    8909: (T + 'нет слова карточки «active»', {"example_en": "At eighty she's still very active"}),
    8951: (T + 'повтор 8877 «comes every …day»', {"example_en": 'We share a cleaner with the neighbours'}),
    8954: (T + 'калька', {"example_en": 'The dirty work always falls to me'}),
    9210: (T + '«in Hamburg» — без нужды', {"example_en": "My husband is in Leeds for work this week, so I'm taking the kids to school on my own"}),
    10391: (T + 'книжно', {"example_en": "She's waiting for her beloved to come back"}),
}

REPLACE = []

SPLIT_LATER = {}
