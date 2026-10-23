"""Вычитка английского, порция p009 (B1), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка английского: "

FIXES = {
    1397: (T + 'учебниково', {"example_en": 'A new shop is opening on the high street'}),
    1445: (T + "повтор 8865 «to the hairdresser's»", {"example_en": 'The hairdresser cut my hair far too short'}),
    1447: (T + 'повтор 17481 «How does it work?»', {"example_en": 'The dishwasher has stopped working'}),
    1452: (T + 'учебниково', {"example_en": 'I bought my rucksack second-hand'}),
    1457: (T + '«Schmidt / Weber» — не английские фамилии', {"example_en": "Her maiden name is Wilson, but since the wedding she's been Clarke"}),
    1467: (T + 'повтор 151, 1707 «coin for the trolley»', {"example_en": 'Tourists throw coins into this fountain'}),
    1519: (T + 'без ситуации', {"example_en": 'The caretaker has already changed the bulb'}),
    1532: (T + 'коряво', {"example_en": "There's a path all around the lake"}),
    1566: (T + 'учебниково', {"example_en": 'The remote must be somewhere on the sofa'}),
    1572: (T + 'без ситуации', {"example_en": 'The local teenagers meet in the park'}),
    1590: (T + 'повтор 1946 «a test tomorrow»', {"example_en": 'The maths test went well'}),
    1595: (T + 'повтор 1138 «click on the link»', {"example_en": 'Double-click on the icon'}),
    1640: (T + 'повтор 2714 «has crashed again»', {"example_en": 'I take my laptop to the office every day'}),
    1663: (T + 'учебниково', {"example_en": "We'll set off as soon as it stops raining"}),
    1707: (T + 'повтор 151 «coin for the trolley»', {"example_en": 'I collect old coins'}),
    1712: (T + 'повтор 450 «call you back later»', {"example_en": 'See you later at the café'}),
    1728: (T + '«in Berlin» — без нужды', {"example_en": 'My niece is studying in Oxford'}),
    1734: (T + 'оборвано', {"example_en": "It's not necessary to bring anything"}),
    1758: (T + 'калька', {"example_en": "It's not a favour, it's your duty"}),
}

REPLACE = []

SPLIT_LATER = {}
