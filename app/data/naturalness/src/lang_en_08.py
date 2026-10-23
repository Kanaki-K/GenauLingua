"""Вычитка английского, порция p008 (B1), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка английского: "

FIXES = {
    831: (T + 'учебниково', {"example_en": 'We see each other very rarely these days'}),
    870: (T + '«Müller» — не английская фамилия', {"example_en": 'Mrs Jones, please come through to the consulting room'}),
    873: (T + "повтор 874 «Who's … today?»", {"example_en": "You wash up, I'll dry"}),
    883: (T + 'повтор 1068 «I bumped…»', {"example_en": "Your forehead's burning, have you got a temperature?"}),
    921: (T + 'повтор 1736 «your number»', {"example_en": "I've changed my phone number"}),
    1009: (T + 'без ситуации', {"example_en": 'The washing machine is leaking'}),
    1057: (T + '«in Munich» — без нужды', {"example_en": 'Flat hunting in London takes a lot of patience'}),
    1199: (T + 'без ситуации', {"example_en": 'You choose the restaurant'}),
    1201: (T + 'повтор 1104 «take off your coat»', {"example_en": 'Please take your shoes off'}),
    1230: (T + 'коряво', {"example_en": 'The shop assistant is serving another customer'}),
    1241: (T + 'повтор 26 «sign up for the course»', {"example_en": "At university I'm taking a Spanish course"}),
    1302: (T + '«Ms Klein» — не английская фамилия', {"example_en": 'Ms Taylor is responsible for office administration here'}),
    1308: (T + 'учебниково', {"example_en": 'My mum sings in the church choir'}),
    1337: (T + 'без ситуации', {"example_en": "Turn around, I'll fix your collar"}),
    1358: (T + 'учебниково', {"example_en": "We're still furnishing the new house"}),
    1384: (T + 'калька', {"example_en": "I can't make up my mind"}),
}

REPLACE = []

SPLIT_LATER = {}
