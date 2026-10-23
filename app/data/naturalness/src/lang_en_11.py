"""Вычитка английского, порция p011 (B1), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка английского: "

FIXES = {
    2178: (T + 'без ситуации', {"example_en": "Don't touch, it's hot!"}),
    2192: (T + 'повтор 1903 «instead of»', {"example_en": 'Rather than complaining, help me'}),
    2205: (T + 'без ситуации', {"example_en": 'This noise is really annoying'}),
    2217: (T + 'нет слова карточки «attentive»', {"example_en": "He's very attentive in class"}),
    2220: (T + 'оборвано', {"example_en": "Write the address down or you'll forget it"}),
    2221: (T + 'повтор 6382 «share»', {"example_en": "We'll split the work between the three of us"}),
    2258: (T + 'без ситуации', {"example_en": "You can keep the book, it's a present"}),
    2286: (T + 'книжно', {"example_en": 'We beat the best team in the league'}),
    2290: (T + 'учебниково', {"example_en": "I've never set foot in that house"}),
    2309: (T + 'тавтология', {"example_en": "You're not allowed to drill on Sundays"}),
    2311: (T + 'коряво', {"example_en": 'My daughter does boxing twice a week'}),
    2335: (T + 'повтор 1397 «a new shop»', {"example_en": 'Coming soon to cinemas'}),
    2339: (T + "повтор 2093 «I'm ill»", {"example_en": "There's a strike tomorrow, that's why I'm cycling"}),
    2342: (T + 'повтор «is diabetic» (13061)', {"example_en": 'There are sugar-free sweets for diabetics'}),
    2353: (T + 'без ситуации', {"example_en": 'A last-minute ticket costs double'}),
    2385: (T + 'повтор 2184 «switch on…»', {"example_en": 'Who switched the radio on?'}),
    2426: (T + 'без ситуации', {"example_en": 'The landlord wants to raise the rent'}),
    2430: (T + 'калька', {"example_en": 'You owe me an explanation'}),
}

REPLACE = []

SPLIT_LATER = {}
