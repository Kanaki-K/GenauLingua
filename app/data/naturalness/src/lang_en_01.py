"""Вычитка английского, порция p001 (A1), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка английского: "

FIXES = {
    41: (T + 'повтор «goes to work» (62, 72)', {"example_en": 'I really love my job'}),
    62: (T + 'повтор «to work by…» (72)', {"example_en": "I've left the car outside the house"}),
    103: (T + "«He'll definitely come» — без ситуации", {"example_en": "He'll definitely be late"}),
    105: (T + 'учебниково', {"example_en": "We're visiting Grandma this weekend"}),
    113: (T + 'без ситуации', {"example_en": 'Fancy a beer?'}),
    117: (T + 'учебниково', {"example_en": 'This pear is really sweet'}),
    127: (T + 'учебниково', {"example_en": 'What a lovely flower!'}),
    137: (T + 'без ситуации', {"example_en": 'Can you bring me my charger?'}),
    141: (T + 'повтор «breakfast» (138)', {"example_en": 'Can you get some bread rolls?'}),
    144: (T + 'оборвано', {"example_en": 'I take the bus to school'}),
    160: (T + "повтор 402 «I'm here»", {"example_en": 'Your phone is there, on the table'}),
    163: (T + 'нет слова карточки «thanks» (сущ.)', {"example_en": 'A little present to say thanks'}),
    167: (T + 'повтор 305 «That is … good»', {"example_en": 'This is my seat'}),
    189: (T + 'учебниково', {"example_en": 'The car park is there, behind the supermarket'}),
    211: (T + 'оборвано', {"example_en": "Tonight it's my treat!"}),
    238: (T + 'учебниково', {"example_en": 'What time are we eating?'}),
    244: (T + 'без ситуации', {"example_en": "Tomorrow we're driving to the seaside"}),
    248: (T + 'повтор «goes by…» (62, 72)', {"example_en": 'My daughter cycles to school'}),
    267: (T + 'повтор 11635 «dinner is ready»', {"example_en": "Are you ready? Let's go"}),
    274: (T + 'учебниково', {"example_en": 'We always have fish on Fridays'}),
    278: (T + 'учебниково', {"example_en": "I'll take you to the airport"}),
    286: (T + 'нет слова карточки «wife»', {"example_en": 'My wife works at the hospital'}),
    305: (T + 'повтор 167', {"example_en": 'The house is quite big enough for everyone'}),
    307: (T + 'учебниково', {"example_en": 'Grandad works in the garden all day'}),
    315: (T + '«Müller» — не английская фамилия', {"example_en": 'Dear Ms Smith'}),
    323: (T + 'учебниково', {"example_en": 'I buy my vegetables straight from the farmer'}),
    328: (T + 'без ситуации', {"example_en": "I'm just leaving"}),
    330: (T + 'нет слова карточки «gladly»', {"example_en": 'Can you help me? – Gladly!'}),
    348: (T + 'без ситуации', {"example_en": 'She looks really happy in her new job'}),
    374: (T + 'тавтология', {"example_en": 'Hold my bag for a sec, please'}),
    376: (T + 'без ситуации', {"example_en": "Give me your hand, we're crossing"}),
    400: (T + '«Müller» — не английская фамилия', {"example_en": 'Good afternoon, Mr Smith, please come in'}),
    402: (T + 'повтор 160', {"example_en": 'Come here!'}),
    406: (T + 'без ситуации', {"example_en": 'The kids sit at the back of the car'}),
    415: (T + 'учебниково', {"example_en": 'Our dog is called Max'}),
    428: (T + 'повтор 426 «That is her…»', {"example_en": 'The kids are playing with their friends'}),
    431: (T + 'повтор 338 «in the city»', {"example_en": "I've lived in England for two years"}),
    456: (T + 'повтор 429 «coffee every morning»', {"example_en": 'Shall we grab a coffee?'}),
    467: (T + 'учебниково', {"example_en": 'Where do you buy your bread?'}),
    481: (T + 'учебниково', {"example_en": "There's a good film on at the cinema tonight"}),
    500: (T + 'повтор 165 «at three»', {"example_en": 'Is your sister coming too?'}),
    509: (T + 'без ситуации', {"example_en": "My daughter's ill today and staying at home"}),
}

REPLACE = []

SPLIT_LATER = {}
