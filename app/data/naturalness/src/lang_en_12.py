"""Вычитка английского, порция p012 (B1), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка английского: "

FIXES = {
    2448: (T + 'оборвано', {"example_en": "That's not fair, it's my turn!"}),
    2461: (T + '«in Hamburg» — без нужды', {"example_en": 'Once a month I have to go to head office in Manchester'}),
    2490: (T + 'нет слова карточки «frustration»', {"example_en": 'Out of frustration he ate all the chocolate'}),
    2497: (T + 'повтор 1011 «end of the corridor»', {"example_en": 'Put it in first gear and go slowly'}),
    2508: (T + 'учебниково', {"example_en": "Tomorrow we're playing a really strong opponent"}),
    2586: (T + 'повтор 13392 «… the door»', {"example_en": 'Does anyone here speak German?'}),
    2618: (T + 'учебниково', {"example_en": 'Shall we watch a comedy tonight?'}),
    2620: (T + 'книжно', {"example_en": "There's always conflict between the two brothers"}),
    2626: (T + 'оборвано', {"example_en": 'The answer is correct'}),
    2658: (T + 'учебниково', {"example_en": 'He steers, I read the map'}),
}

REPLACE = []

SPLIT_LATER = {}
