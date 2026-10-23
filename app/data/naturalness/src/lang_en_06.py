"""Вычитка английского, порция p006 (A2), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка английского: "

FIXES = {
    6326: (T + 'без ситуации', {"example_en": "Don't lean out, it's dangerous!"}),
    6528: (T + 'без ситуации', {"example_en": "Money's always tight at the end of the month"}),
    6585: (T + 'повтор «the keys»', {"example_en": 'Where did you hide the presents?'}),
    6646: (T + 'учебниково', {"example_en": 'She passed the exam first time'}),
    6726: (T + 'повтор «my keys»', {"example_en": "I can't find it anywhere"}),
    7057: (T + '«in Cologne» — без нужды', {"example_en": 'My husband is at a trade fair in Manchester this week'}),
    7464: (T + 'нет слова карточки «good»', {"example_en": "I'm doing it for your own good"}),
    7711: (T + 'нет слова карточки «to enter»', {"example_en": 'Enter your name on the list'}),
    8818: (T + 'повтор «the bill»', {"example_en": 'The waiter was really friendly'}),
    8868: (T + 'учебниково', {"example_en": "My colleague covers for me when I'm ill"}),
    8994: (T + 'повтор 8980 «application»', {"example_en": 'Have you applied for that job?'}),
    9460: (T + 'повтор 126 «Have you got a pencil?»', {"example_en": "This pen doesn't work any more"}),
    9591: (T + 'книжно', {"example_en": 'I get on really well with my classmates'}),
    10036: (T + 'без ситуации', {"example_en": 'Can you help me? – Gladly!'}),
    10064: (T + 'оборвано', {"example_en": 'Be careful, the road is icy'}),
    10073: (T + "повтор 13335 «I don't remember»", {"example_en": 'Do you remember me?'}),
    10077: (T + 'без ситуации', {"example_en": "That's strange, the door's open"}),
    10091: (T + 'повтор 2040', {"example_en": "She's head over heels in love with him"}),
    10102: (T + 'повтор «funny» (562)', {"example_en": 'Your dad is really witty'}),
    10129: (T + 'нет слова карточки «interest»', {"example_en": 'I have no interest in football'}),
    11772: (T + 'повтор 599 «canteen»', {"example_en": 'The university cafeteria is always full'}),
    12108: (T + 'оборвано', {"example_en": 'On Saturday nights I go out with friends'}),
    12140: (T + 'учебниково', {"example_en": 'The kids want to go to the circus'}),
    12142: (T + 'повтор 1934 «Our team won»', {"example_en": 'The team trains three times a week'}),
    12474: (T + 'без ситуации', {"example_en": 'Are you still awake?'}),
    12477: (T + 'оборвано', {"example_en": "There's been an accident on the motorway"}),
    12529: (T + 'повтор 199 «quick shower»', {"example_en": 'The kids never want to have a shower'}),
    12620: (T + 'тавтология', {"example_en": 'You smell lovely! What perfume is that?'}),
    13295: (T + 'повтор «Is that yours?» (171)', {"example_en": 'Your train leaves in ten minutes'}),
    13338: (T + 'повтор 289 «looking forward to»', {"example_en": 'You can count on it'}),
    13430: (T + "повтор 1326 «It's raining, so»", {"example_en": "The train's late, that's why I'm taking a taxi"}),
    13447: (T + 'учебниково', {"example_en": "If I won a million, I'd stop working"}),
    13843: (T + 'калька', {"example_en": "You've got a lovely voice"}),
    13853: (T + 'калька', {"example_en": 'Tell me a joke!'}),
    13901: (T + 'повтор 945 «Bye, see you tomorrow»', {"example_en": 'Bye, see you soon!'}),
    14923: (T + 'повтор «bakes delicious cakes» (904)', {"example_en": 'My aunt lives in the countryside'}),
    14944: (T + 'учебниково', {"example_en": "You're a grown-up now, you decide"}),
    14979: (T + 'без ситуации', {"example_en": 'I grew up in Leeds'}),
    15394: (T + 'учебниково', {"example_en": 'A bird has built a nest on our balcony'}),
    15926: (T + 'учебниково', {"example_en": 'The King is visiting Scotland'}),
    17483: (T + 'повтор 8448 «Check out»', {"example_en": 'I filmed a video of the concert'}),
}

REPLACE = []

SPLIT_LATER = {}
