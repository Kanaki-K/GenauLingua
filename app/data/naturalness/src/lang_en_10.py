"""Вычитка английского, порция p010 (B1), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка английского: "

FIXES = {
    1774: (T + 'тавтология', {"example_en": 'Cheers! To the happy couple!'}),
    1791: (T + 'повтор 13659 «umbrella»', {"example_en": 'My umbrella broke in this wind'}),
    1820: (T + 'тавтология', {"example_en": 'The ticket inspector gave me a fine'}),
    1877: (T + 'нет слова карточки «careful»', {"example_en": "She's very careful in her work"}),
    1883: (T + 'повтор 857 «go for a walk»', {"example_en": 'A walk after dinner does you good'}),
    1898: (T + 'без ситуации', {"example_en": 'He interrupts me constantly'}),
    1902: (T + 'повтор 1513 «next station … main station»', {"example_en": 'Get off at the third stop'}),
    1908: (T + 'учебниково', {"example_en": 'The temperature is still rising'}),
    1944: (T + 'повтор «temperature» как болезнь', {"example_en": "What's the temperature outside?"}),
    1996: (T + 'повтор «cycle to work»', {"example_en": 'Turn off the light — think of the environment!'}),
    2070: (T + 'оборвано', {"example_en": 'Can I drop by this evening?'}),
    2080: (T + 'повтор 13931 «job interview tomorrow»', {"example_en": 'The job interview went really well'}),
    2134: (T + 'без ситуации', {"example_en": 'Mark is very reliable, you can count on him'}),
}

REPLACE = []

SPLIT_LATER = {}
