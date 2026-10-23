"""Вычитка английского, порция p004 (A2), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка английского: "

FIXES = {
    81: (T + 'без ситуации', {"example_en": 'The neighbours are building a new house'}),
    128: (T + 'оборвано', {"example_en": 'This blouse is perfect for the office'}),
    161: (T + 'без ситуации', {"example_en": "That's what I came for"}),
    170: (T + 'калька', {"example_en": 'What are you having with your pizza?'}),
    171: (T + 'повтор «That is … » (426, 963)', {"example_en": 'Is this bag yours?'}),
    186: (T + '«to Berlin» — без нужды', {"example_en": 'The train goes straight to London'}),
    216: (T + 'учебниково', {"example_en": 'Shall we go for an ice cream?'}),
    234: (T + '«in Berlin» — без нужды', {"example_en": "It's my first time in Venice"}),
    289: (T + "повтор 293 «I'm glad»", {"example_en": "I'm really looking forward to seeing you!"}),
    318: (T + 'повтор «the pharmacy»', {"example_en": 'I live right opposite the park'}),
    355: (T + 'без ситуации', {"example_en": 'Half the class has got the flu'}),
    423: (T + 'калька', {"example_en": "I've got an idea!"}),
    471: (T + 'повтор 450 «no time»', {"example_en": 'No problem at all'}),
    538: (T + 'нет слова карточки «boring»', {"example_en": 'This film is so boring'}),
    568: (T + 'повтор «cycle to work»', {"example_en": 'Sometimes I wake up in the night'}),
    582: (T + 'повтор «That is my…»', {"example_en": 'Have you seen my phone?'}),
    657: (T + 'грубовато', {"example_en": 'Can you explain it again?'}),
    662: (T + 'учебниково', {"example_en": "Tonight I'm making pasta with tomato sauce"}),
    677: (T + 'оборвано', {"example_en": 'I buy almost everything online'}),
    686: (T + 'калька', {"example_en": 'Her family comes from Eastern Europe'}),
    773: (T + 'учебниково', {"example_en": 'My back hurts'}),
    782: (T + 'повтор 573 «the market»', {"example_en": 'On Saturdays I do the shopping for the whole week'}),
    784: (T + 'учебниково', {"example_en": "What a shame, I can't come!"}),
    792: (T + 'книжно', {"example_en": 'The ferry to the island leaves at nine'}),
    814: (T + 'без ситуации', {"example_en": 'My sister is three months pregnant'}),
    840: (T + 'учебниково', {"example_en": 'He always sings in the shower'}),
    842: (T + 'повтор 1043 «go skiing»', {"example_en": "I've hired some skis"}),
    923: (T + 'учебниково', {"example_en": 'Do you play tennis?'}),
    941: (T + 'повтор «at three»', {"example_en": 'I bumped into Paul in town'}),
    963: (T + 'повтор «That is our…» (426)', {"example_en": 'Our house is at the end of the street'}),
    976: (T + 'повтор «the keys»', {"example_en": "I forgot my mum's birthday!"}),
    1011: (T + 'повтор 223 «Where is the toilet?»', {"example_en": 'The loo is at the end of the corridor'}),
}

REPLACE = []

SPLIT_LATER = {}
