"""Вычитка английского, порция p030 (B2), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка английского: "

FIXES = {
    10469: (T + 'нет слова карточки «guts»', {"example_en": 'It takes guts to say no to your boss'}),
    10472: (T + 'учебниково', {"example_en": "Don't push me, I'll decide for myself"}),
    10473: (T + 'громоздко', {"example_en": "Lucky devil, he's won again!"}),
    10496: (T + 'шаблон', {"example_en": 'A bit of decency, please!'}),
    10498: (T + 'книжно', {"example_en": "He's incapable of frying an egg"}),
    10509: (T + 'тавтология', {"example_en": 'She was instantly taken with his sense of humour'}),
    10515: (T + 'калька', {"example_en": 'I felt the need to talk to someone'}),
    10521: (T + 'книжно', {"example_en": 'Come here, give me a hug!'}),
    10522: (T + 'книжно', {"example_en": 'Nature is my biggest inspiration'}),
    10523: (T + 'книжно', {"example_en": "It's a sensitive subject, careful what you say"}),
    10530: (T + 'учебниково', {"example_en": "I'm just a poor sinner, he says with a laugh"}),
    10533: (T + 'книжно', {"example_en": 'Waiting for the results is absolute agony'}),
    10555: (T + 'учебниково', {"example_en": "The baby is restless, he's probably teething"}),
    10581: (T + 'повтор 10325 «pinched my parking space»', {"example_en": "That rogue sold me a car that doesn't work"}),
    10598: (T + 'учебниково', {"example_en": 'She was sobbing on the phone'}),
    10634: (T + 'книжно', {"example_en": "Against bureaucracy we're sadly powerless"}),
    10662: (T + 'повтор 10345 «idiotic idea»', {"example_en": 'Stop asking idiotic questions'}),
    10755: (T + 'повтор 10390 «tells me something is wrong»', {"example_en": 'Trust your gut feeling'}),
}

REPLACE = []

SPLIT_LATER = {}
