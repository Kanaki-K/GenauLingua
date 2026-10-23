"""Вычитка английского, порция p003 (A1/A2), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка английского: "

FIXES = {
    1426: (T + 'учебниково', {"example_en": "Tomorrow we're flying to Barcelona"}),
    1441: (T + 'без ситуации', {"example_en": 'In my free time I read a lot'}),
    1458: (T + 'канцелярит', {"example_en": "Don't forget to put your place of birth on the form"}),
    1463: (T + 'нет слова карточки «to belong»', {"example_en": 'Whose bag is this? – It belongs to my sister'}),
    1589: (T + 'нет слова карточки «class»', {"example_en": 'There are twenty-five of us in the class'}),
    1695: (T + 'без ситуации', {"example_en": 'Who wants to take part in the race?'}),
    1739: (T + 'повтор 1542 «shelf … high»', {"example_en": 'The blankets are upstairs'}),
    2007: (T + 'оборвано', {"example_en": "I'll wait for you downstairs by the door"}),
    2109: (T + 'повтор 1032 «The weather is…»', {"example_en": 'What a wonderful day!'}),
    2354: (T + 'учебниково', {"example_en": "I'd like a double room for two nights"}),
    2453: (T + 'устарело', {"example_en": 'Who still uses a fax?'}),
    6228: (T + 'без ситуации', {"example_en": 'Is the station far from here?'}),
    6250: (T + 'повтор 6292 «The bag is…»', {"example_en": 'The exam was harder than I expected'}),
    6252: (T + 'без ситуации', {"example_en": "Look, it's snowing!"}),
    6483: (T + 'повтор 68 «on the second floor»', {"example_en": 'The office is on the third floor'}),
    8334: (T + 'нет слова карточки «to complete»', {"example_en": 'Complete the sentences with the right words'}),
    8735: (T + 'повтор 41 «my job»', {"example_en": "I've found a new job!"}),
    8797: (T + 'учебниково', {"example_en": 'My colleague is on holiday today'}),
    9441: (T + 'повтор 8742 «My … is nice»', {"example_en": "My daughter's teacher is really young"}),
    10438: (T + 'книжно', {"example_en": 'I want to congratulate you on the promotion!'}),
    12121: (T + "повтор 2176 «The start wasn't easy»", {"example_en": 'There were a hundred runners at the start'}),
    13282: (T + 'повтор 13331 «to the doctor»', {"example_en": "I'm going to the beach with friends"}),
    13293: (T + 'учебниково', {"example_en": "Let's meet at the café at six"}),
    13314: (T + "повтор 13331 «from the doctor's»", {"example_en": "I've just come from work"}),
    13375: (T + "повтор «I'm … years old»", {"example_en": "I've got a ten-minute break"}),
    13387: (T + 'повтор 52 «I get up at…»', {"example_en": 'I work eight hours a day'}),
    13392: (T + 'повтор «my key»', {"example_en": 'Does anyone want a coffee?'}),
    13498: (T + "повтор «I'm … years old»", {"example_en": 'See you in twenty minutes'}),
    13968: (T + 'повтор «Speak soon»', {"example_en": 'Thanks for calling, goodbye!'}),
    14913: (T + 'повтор 8742 «My … is very nice»', {"example_en": 'My partner is an amazing cook'}),
    15183: (T + 'без ситуации', {"example_en": "He's still single at forty"}),
    17202: (T + 'повтор 1211 «platform three»', {"example_en": 'Excuse me, is this the platform for London?'}),
    17250: (T + 'учебниково', {"example_en": "Tomorrow we're visiting the castle"}),
    17342: (T + 'повтор 17335 «sights»', {"example_en": 'The tour guide also spoke German'}),
    17489: (T + 'учебниково', {"example_en": 'My dad fixes everything himself'}),
    18610: (T + 'повтор 595 «Wait a minute»', {"example_en": "One second, I'm coming!"}),
}

REPLACE = []

SPLIT_LATER = {}
