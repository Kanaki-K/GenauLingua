"""Вычитка английского, порция p007 (A2/B1), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка английского: "

FIXES = {
    18752: (T + 'повтор 2233 «lie-in»', {"example_en": "On Sundays we always have lunch at my grandparents'"}),
    17915: (T + 'калька', {"example_en": 'The doctor examined me thoroughly'}),
    18184: (T + 'повтор 681 «room»', {"example_en": "On Sunday we're tidying up the cellar"}),
    18216: (T + 'учебниково', {"example_en": 'The pot is too small for all the pasta'}),
    18248: (T + 'повтор 6483 «on the third floor»', {"example_en": 'Which floor do you live on?'}),
    18660: (T + 'оборвано', {"example_en": 'After lunch Grandad rests for an hour'}),
    18933: (T + 'повтор 995 «In the morning I work»', {"example_en": 'We work in the mornings and study in the afternoons'}),
    18967: (T + "повтор «the chemist's»", {"example_en": "The shop is closed on Sundays, we'll have to wait until Monday"}),
    18969: (T + '«the Müllers» — не английская фамилия', {"example_en": 'Do you know the Browns? Their son is in the same class as ours'}),
    18988: (T + '«in Berlin» — без нужды', {"example_en": "Since you moved to Australia, I've missed you a lot"}),
    44: (T + 'учебниково', {"example_en": "I've turned the spare room into a home office"}),
    85: (T + 'тавтология', {"example_en": 'I give the kids plastic cups'}),
    152: (T + 'повтор 8759 «not here today»', {"example_en": 'My boss gave me Friday off'}),
    231: (T + 'без ситуации', {"example_en": "I think I've caught a cold"}),
    241: (T + 'повтор 10 «What is your address?»', {"example_en": 'Your flat is gorgeous'}),
    333: (T + 'без ситуации', {"example_en": 'My parents have been divorced for years'}),
    412: (T + 'учебниково', {"example_en": 'A spoonful of honey in your tea?'}),
    477: (T + 'без ситуации', {"example_en": 'A kilo of apples, please'}),
    485: (T + 'нет слова карточки «gear»', {"example_en": "Grab your gear and let's go"}),
    496: (T + 'повтор 8792 «cook»', {"example_en": "The restaurant's chef is from Naples"}),
    510: (T + 'без ситуации', {"example_en": 'Grandad has been in hospital for a week'}),
    579: (T + 'калька', {"example_en": 'For the pizza you need half a kilo of flour'}),
    611: (T + 'книжно', {"example_en": "There's a full moon tonight"}),
    636: (T + "повтор 253 «What's your surname?»", {"example_en": 'My surname is spelt with two Ls'}),
    700: (T + 'повтор 717 «Is there a free … here?»', {"example_en": 'The car park under our building is always full'}),
    708: (T + 'учебниково', {"example_en": 'Put a plaster on that blister'}),
    711: (T + 'учебниково', {"example_en": 'In autumn we go mushroom picking'}),
    750: (T + 'повтор 49 «The book is on…»', {"example_en": 'The shelf is full of old newspapers'}),
}

REPLACE = []

SPLIT_LATER = {}
