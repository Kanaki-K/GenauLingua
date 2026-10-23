"""Вычитка английского, порция p016 (B1), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка английского: "

FIXES = {
    8055: (T + 'повтор «the key»', {"example_en": "She's rummaging in her handbag for her phone"}),
    8056: (T + 'нет слова карточки «nimble»', {"example_en": 'The little one is as nimble as a squirrel'}),
    8058: (T + 'калька', {"example_en": "I've made a radical change: short hair!"}),
    8145: (T + 'повтор «breakfast included» (6819)', {"example_en": 'The membership includes ten yoga classes'}),
    8166: (T + 'повтор 7017 «went through a lot»', {"example_en": 'In those years he lived through some very hard times'}),
    8182: (T + 'шаблон «books on top of each other»', {"example_en": 'The boxes are stacked on top of each other in the cellar'}),
    8303: (T + 'тавтология', {"example_en": 'My grandad still cuts the grass with a scythe'}),
    8380: (T + 'книжно', {"example_en": "I'm really grateful for your help"}),
    8401: (T + 'неживо', {"example_en": 'Tie the bikes down on the car roof properly'}),
    8409: (T + 'повтор «leaves in autumn»', {"example_en": 'A button has fallen off my jacket'}),
    8440: (T + 'повтор «my key»', {"example_en": 'My charger has gone missing'}),
    8595: (T + 'калька', {"example_en": 'The kids are running around in the garden'}),
    8660: (T + 'повтор «leaves in autumn»', {"example_en": 'My daughter wants a purple bedroom'}),
    8758: (T + 'калька', {"example_en": 'For her, her career comes first'}),
    8782: (T + 'учебниково', {"example_en": 'The kids love spending the holidays on the farm'}),
    8829: (T + '«in Berlin» — без нужды', {"example_en": "Tomorrow I'm in Glasgow on business"}),
}

REPLACE = []

SPLIT_LATER = {}
