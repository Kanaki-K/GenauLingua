"""Вычитка английского, порция p025 (B1), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка английского: "

FIXES = {
    17148: (T + 'тавтология', {"example_en": 'We take the ferry across the river'}),
    17173: (T + 'учебниково', {"example_en": 'Passengers for the Nice flight should go to gate 12'}),
    17184: (T + 'без ситуации', {"example_en": 'Shall we make a detour past the bakery?'}),
    17194: (T + 'неполно', {"example_en": 'Turn left at the next street'}),
    17209: (T + '«Müller» — не английская фамилия', {"example_en": 'I have a reservation under the name Johnson'}),
    17410: (T + 'оборвано', {"example_en": 'The fishing boat comes back to harbour full of fish'}),
    17502: (T + 'калька', {"example_en": 'My grandad is scared of new technology'}),
    17516: (T + 'калька', {"example_en": 'He put his arm around my shoulders'}),
    17533: (T + 'коряво', {"example_en": 'She has a big network of contacts in fashion'}),
    17578: (T + 'повтор «the lift is broken» (13558)', {"example_en": 'Shall we take the lift or the stairs?'}),
    17587: (T + 'оборвано', {"example_en": "We're late because the car broke down"}),
    17590: (T + 'реклама', {"example_en": 'Which platform is the film on?'}),
    17662: (T + '«spätzle … Swabian» — не английский быт', {"example_en": "Tonight we're having lentil soup"}),
    17768: (T + 'калька', {"example_en": "It's a deal!"}),
    17771: (T + 'повтор 15617 «cows in the meadow»', {"example_en": "The milk comes straight from the neighbour's cow"}),
    17779: (T + 'учебниково', {"example_en": 'In winter the livestock stay in the barn'}),
    17792: (T + 'без ситуации', {"example_en": 'The tourism industry is going through a hard time'}),
    17931: (T + 'учебниково', {"example_en": 'My son is already 120 centimetres tall'}),
    18054: (T + 'повтор 17946 «for the cake»', {"example_en": 'A kilogram of tomatoes, please'}),
    18115: (T + 'калька', {"example_en": "Right, I'm heading home"}),
    18187: (T + 'учебниково', {"example_en": 'All the residents in our building know each other'}),
    18194: (T + 'калька', {"example_en": 'In winter we spend the evenings by the fireplace'}),
}

REPLACE = []

SPLIT_LATER = {}
