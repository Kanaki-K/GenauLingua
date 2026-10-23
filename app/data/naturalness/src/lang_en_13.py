"""Вычитка английского, порция p013 (B1), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка английского: "

FIXES = {
    2792: (T + 'без ситуации', {"example_en": 'Switch to second gear on the hill!'}),
    2808: (T + 'без ситуации', {"example_en": "Of course I'm coming too!"}),
    2809: (T + 'нет слова карточки «to send»', {"example_en": "I'll send you the file tonight"}),
    2813: (T + 'учебниково', {"example_en": "We're watching a brilliant series"}),
    2828: (T + 'нет слова карточки «worry»', {"example_en": 'His worries keep him awake at night'}),
    2850: (T + 'без ситуации', {"example_en": "The cheese stinks, but it's delicious"}),
    2884: (T + 'без ситуации', {"example_en": "There's a trend towards working more from home"}),
    2887: (T + 'повтор 1672 «the tap is dripping»', {"example_en": "Water's dripping from the ceiling"}),
    2898: (T + 'без ситуации', {"example_en": 'You surprised me with that news'}),
    2906: (T + 'без ситуации', {"example_en": "It's customary to tip here"}),
    2944: (T + '«Berlin» — без нужды', {"example_en": 'Prices here are comparable to London'}),
    2953: (T + 'повтор 18988 «I miss you»', {"example_en": 'Do you miss your family?'}),
    2963: (T + "повтор 2041 «don't waste time»", {"example_en": "Don't waste water!"}),
    2972: (T + 'нет слова карточки «understanding»', {"example_en": 'Thank you for your understanding'}),
    2975: (T + 'повтор 2974 «breaking the rules»', {"example_en": 'Anyone breaking the ban gets a fine'}),
    2999: (T + 'коряво', {"example_en": 'The warmth of the fire is lovely'}),
    3003: (T + 'повтор 3059 «tomorrow»', {"example_en": 'When are you going away on holiday?'}),
    3006: (T + 'повтор 3005 «throw away»', {"example_en": "I'm throwing the old boxes away"}),
    3059: (T + 'оборвано', {"example_en": 'Shall we go back by train or by car?'}),
}

REPLACE = []

SPLIT_LATER = {}
