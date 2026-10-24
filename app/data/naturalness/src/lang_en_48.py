"""Вычитка английского, порция p048 (C2), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка английского: "

FIXES = {
    14320: (T + 'повтор 7204 «remarkable achievement»', {"example_en": 'It was truly a lovely evening'}),
    15260: (T + '«in Berlin» — без нужды', {"example_en": 'My biological father lives in Bristol'}),
    15278: (T + "повтор 12129 «won't sleep without his teddy»", {"example_en": 'My son was given a little teddy when he was born'}),
    15783: (T + 'без ситуации', {"example_en": 'At low tide you can walk out to the island'}),
    15855: (T + 'учебниково', {"example_en": 'This wild horse was tamed in a month'}),
    16694: (T + 'повтор 7028 «cards to pass the time»', {"example_en": 'To kill time at the airport, I read'}),
}

REPLACE = []

SPLIT_LATER = {}
