"""Вычитка английского, порция p021 (B1), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка английского: "

FIXES = {
    13008: (T + 'неживо', {"example_en": "I've got an inflammation in my knee"}),
    13059: (T + 'неживо', {"example_en": 'A bit of apple went down my windpipe'}),
    13060: (T + '«in Munich» — лишнее', {"example_en": 'After the match my voice was hoarse from shouting'}),
    13067: (T + 'повтор 12807 «Grandma lives in a care home»', {"example_en": 'On Sundays we visit Grandad at the care home'}),
    13096: (T + 'повтор 12798 «tummy ache»', {"example_en": 'The little one complains of tummy ache every Monday morning'}),
    13097: (T + 'учебниково', {"example_en": 'My GP is retiring, I need to find a new one'}),
    13103: (T + 'учебниково', {"example_en": "Stop yawning, it's catching!"}),
    13141: (T + 'учебниково', {"example_en": "It's just a graze, no need for a plaster"}),
    13168: (T + 'повтор 11851 «tastes disgusting»', {"example_en": "Can you pop to the chemist's for some cough syrup?"}),
    13369: (T + 'калька', {"example_en": 'Have you got anything to eat?'}),
    13394: (T + 'без ситуации', {"example_en": "Come over here, there's room"}),
    13407: (T + 'книжно', {"example_en": 'I have neither the time nor the money'}),
    13473: (T + 'нет слова карточки «such»', {"example_en": "In such weather we're staying in"}),
    13478: (T + "повтор «First of all, I don't have time»", {"example_en": 'First of all homework, then TV'}),
    13508: (T + 'нет слова карточки «fourth»', {"example_en": 'He came fourth in the race'}),
    13511: (T + 'повтор 8182 «books on top of each other»', {"example_en": 'The plates are piled on top of each other in the sink'}),
    13558: (T + 'повтор 6838 «cup of coffee today»', {"example_en": 'I live on the seventh floor and the lift is broken'}),
    13590: (T + 'неверно', {"example_en": 'He lost by a tenth of a second'}),
    13631: (T + 'коряво', {"example_en": 'The toddler is running around the garden naked'}),
    13645: (T + 'без ситуации', {"example_en": 'Can you sew this button back on?'}),
    13660: (T + 'повтор 13703 «dressed up as a pirate»', {"example_en": 'Everyone came dressed up to the party'}),
    13662: (T + 'повтор 12339 «leave … in the changing room»', {"example_en": 'At the theatre coats go in the cloakroom'}),
    13758: (T + 'громоздко', {"example_en": "Don't forget the sun cream for the beach"}),
    13769: (T + 'повтор 13719 «on Sundays … all day»', {"example_en": 'Grandad has his coffee in his dressing gown'}),
    13770: (T + 'повтор 13746 «slippers»', {"example_en": 'At our place guests take off their shoes and put on slippers'}),
    13817: (T + 'повтор «my keys»', {"example_en": "Damn, I've missed the train!"}),
    13861: (T + 'коряво', {"example_en": 'Yes sir, right away!'}),
    13866: (T + 'оборвано', {"example_en": 'I watch series with subtitles'}),
    13881: (T + 'нет слова карточки «joke»', {"example_en": 'It was only a joke!'}),
    13884: (T + "повтор 8796 «Don't do anything stupid»", {"example_en": 'Stop talking nonsense'}),
    13893: (T + 'учебниково', {"example_en": 'The whole press is talking about the royal wedding'}),
    13911: (T + 'канцелярит', {"example_en": 'Thanks for the hint!'}),
    13924: (T + 'калька', {"example_en": 'Just ignore his stupid comments'}),
    13925: (T + 'калька', {"example_en": 'Listen to this!'}),
    13957: (T + "повтор 13877 «don't feel like it»", {"example_en": "Are you hungry? – Nah, I'm fine"}),
    13973: (T + 'без ситуации', {"example_en": "The oven's beeping is driving me mad"}),
    13983: (T + "повтор 10122 «I'm not deaf»", {"example_en": 'The lion roars in its cage'}),
    13995: (T + 'книжно', {"example_en": 'Farewell, and thanks for everything!'}),
}

REPLACE = []

SPLIT_LATER = {}
