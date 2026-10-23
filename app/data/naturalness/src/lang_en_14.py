"""Вычитка английского, порция p014 (B1), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка английского: "

FIXES = {
    3067: (T + 'книжно', {"example_en": "Living with my mother-in-law isn't always easy"}),
    13392: (T + 'повтор 6505 «knocking at the door»', {"example_en": 'Does anyone want a coffee?'}),
    6369: (T + 'нет слова карточки «distant»', {"example_en": "The station isn't far — it's only ten minutes away"}),
    6415: (T + 'оборвано', {"example_en": 'I really appreciate your help'}),
    6418: (T + 'книжно', {"example_en": "I can't grasp what he means"}),
    6481: (T + 'калька', {"example_en": "It's in her nature to help others"}),
    6486: (T + 'нет слова карточки «to guard»', {"example_en": 'The dog guards the house'}),
    6520: (T + 'коряво', {"example_en": "Come on, let's carry on!"}),
    6541: (T + 'нет слова карточки «to clear out»', {"example_en": "Come on, let's clear out!"}),
    6572: (T + 'без ситуации', {"example_en": "Hold on tight, it's going to be bumpy!"}),
    6583: (T + 'калька', {"example_en": 'Respect has to be mutual'}),
    6599: (T + 'не то значение', {"example_en": 'The wind knocked the old tree to the ground'}),
    6610: (T + 'без ситуации', {"example_en": "I'm warning you, it's very spicy"}),
    6621: (T + 'шаблон', {"example_en": 'Does that ring any bells?'}),
    6638: (T + 'калька', {"example_en": 'This job gives me a lot of satisfaction'}),
    6707: (T + 'нет слова карточки «powerful»', {"example_en": 'There was a powerful storm last night'}),
    6710: (T + 'коряво', {"example_en": 'How much stuff have you got in the car?!'}),
    6727: (T + 'повтор «my key»', {"example_en": 'I searched the whole flat for my passport'}),
    6730: (T + '«Berlin» — без нужды', {"example_en": "We're approaching London, we'll be there in ten minutes"}),
    6743: (T + 'коряво', {"example_en": 'Keep your distance from that dog'}),
    6784: (T + 'нет слова карточки «to deploy»', {"example_en": "They're deploying drones to find the missing hikers"}),
    6813: (T + 'нет слова карточки «to broadcast»', {"example_en": 'The match is being broadcast live tonight'}),
    6819: (T + 'нет слова карточки «included»', {"example_en": 'Breakfast is included in the price'}),
}

REPLACE = []

SPLIT_LATER = {}
