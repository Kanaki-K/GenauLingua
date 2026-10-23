"""Вычитка английского, порция p022 (B1), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка английского: "

FIXES = {
    14046: (T + 'нет слова карточки «to bring up»', {"example_en": "Tomorrow I'll bring it up with him"}),
    14061: (T + 'книжно', {"example_en": 'Congratulations on the exam!'}),
    14374: (T + 'повтор «behaves like» (14814)', {"example_en": 'My daughter wants a princess dress for her birthday'}),
    14390: (T + 'повтор 12141 «clapped loudly»', {"example_en": 'At the end of the show the whole audience was on its feet'}),
    14405: (T + 'калька', {"example_en": "Hang on, I'll film it!"}),
    14411: (T + 'повтор 14437 «We visited the old…»', {"example_en": 'There are temples everywhere in Thailand'}),
    14437: (T + 'повтор 14411', {"example_en": 'The monks at the monastery brew their own beer'}),
    14448: (T + 'не то значение', {"example_en": 'We visited a medieval castle'}),
    14449: (T + 'калька', {"example_en": 'I love the sound of this old guitar'}),
    14451: (T + 'калька', {"example_en": 'With three grandchildren I feel truly blessed'}),
    14456: (T + '«Berlin» — без нужды', {"example_en": 'His Holiness the Pope is visiting London'}),
    14466: (T + 'не то значение', {"example_en": 'In this book the narrator is a cat'}),
    14469: (T + 'без ситуации', {"example_en": 'This song became the hit of the summer'}),
    14481: (T + '«in Berlin» — без нужды', {"example_en": 'Her paintings hang in a gallery in London'}),
    14496: (T + '«in Berlin» — без нужды', {"example_en": 'The singer is giving a concert in Dublin next week'}),
    14502: (T + 'калька', {"example_en": 'My daughter has done ballet since she was five'}),
    14937: (T + 'повтор 14896 «Mum, where…»', {"example_en": 'The little one is crying for her mummy'}),
    14953: (T + 'калька', {"example_en": 'Our friendship goes back to primary school'}),
    14966: (T + '«to Berlin» — без нужды', {"example_en": 'After the divorce she moved to Bristol'}),
    14976: (T + 'тавтология', {"example_en": "He's a real gentleman, he always holds the door for me"}),
    15006: (T + 'калька', {"example_en": "I've got a good relationship with my neighbours"}),
    15013: (T + 'оборвано', {"example_en": "We're related, but only distantly"}),
    15034: (T + 'учебниково', {"example_en": 'The bishop is coming to bless the new church'}),
}

REPLACE = []

SPLIT_LATER = {}
