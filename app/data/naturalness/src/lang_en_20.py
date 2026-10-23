"""Вычитка английского, порция p020 (B1), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка английского: "

FIXES = {
    12163: (T + 'повтор 12378 «row across»', {"example_en": "I've lost an oar, we're going round in circles!"}),
    12378: (T + 'повтор 12163', {"example_en": 'Hold the paddle tight, the current is strong'}),
    12348: (T + 'книжно', {"example_en": 'Shall we play charades?'}),
    12485: (T + 'без ситуации', {"example_en": 'In this damp weather my bones ache'}),
    12501: (T + 'учебниково', {"example_en": "There's a virus going round the office"}),
    12518: (T + 'калька', {"example_en": "My memory isn't what it used to be"}),
    12532: (T + 'учебниково', {"example_en": 'After the race my pulse was 150'}),
    12545: (T + 'без ситуации', {"example_en": 'You need a medical certificate for the football club'}),
    12559: (T + 'без ситуации', {"example_en": 'You need to take this medicine before meals'}),
    12588: (T + 'не та идиома', {"example_en": 'I avoid people like that like the plague'}),
    12602: (T + 'учебниково', {"example_en": "At the scan you can hear the baby's heartbeat"}),
    12630: (T + 'громоздко', {"example_en": "I sweat a lot when it's hot"}),
    12646: (T + 'нет слова карточки «to look after»', {"example_en": 'She looks after her old mother every day'}),
    12727: (T + "повтор 12967 «carer at Grandma's»", {"example_en": 'The night carer is really kind to the patients'}),
}

REPLACE = []

SPLIT_LATER = {}
