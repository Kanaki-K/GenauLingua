"""Вычитка английского, порция p005 (A2), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка английского: "

FIXES = {
    1222: (T + 'учебниково', {"example_en": 'My son plays basketball for the school team'}),
    1228: (T + 'повтор 1317 «to thank you»', {"example_en": "I'd like to thank everyone"}),
    1235: (T + 'без ситуации', {"example_en": 'How do you justify that expense?'}),
    1297: (T + "повтор 1805 «I'd like to book»", {"example_en": "I've booked our holiday online"}),
    1312: (T + 'без ситуации', {"example_en": "Who's against it?"}),
    1319: (T + "повтор «That's why…» (161)", {"example_en": "That's exactly why I'm calling"}),
    1342: (T + 'нет слова карточки «thin» (о предмете)', {"example_en": 'The ice is still too thin'}),
    1432: (T + 'повтор «swimming» (69)', {"example_en": 'The river runs right through the city'}),
    1479: (T + 'учебниково', {"example_en": "Tonight you're doing the dishes!"}),
    1505: (T + 'повтор 1634 «hand in your notice»', {"example_en": "There's no reason to worry"}),
    1665: (T + 'оборвано', {"example_en": 'Are you in the mood for an ice cream?'}),
    1683: (T + 'повтор 584 «usually»', {"example_en": 'On Tuesdays I mostly work from home'}),
    1685: (T + 'нет слова карточки «crowd»', {"example_en": 'There was a huge crowd at the concert'}),
    1691: (T + 'нет слова карточки «employee»', {"example_en": 'The employee of the month gets a voucher'}),
    1720: (T + "повтор 2093 «I'm ill»", {"example_en": "I'm not working tomorrow — it's a bank holiday, you see"}),
    1793: (T + 'без ситуации', {"example_en": 'She married a very rich man'}),
    1813: (T + 'нет слова карточки «role»', {"example_en": 'She has a small role in the film'}),
    1819: (T + 'повтор 1834 «I managed it»', {"example_en": 'Can you make it by eight?'}),
    1843: (T + 'повтор «The weather is…» (1032)', {"example_en": 'I had a terrible dream'}),
    1865: (T + 'нет слова карточки «to put»', {"example_en": 'Put it here next to me'}),
    1903: (T + 'повтор 10027 «tea instead of coffee»', {"example_en": 'Read a book instead of watching TV'}),
    1922: (T + 'учебниково', {"example_en": 'I spent the evening surfing the internet'}),
    1989: (T + 'коряво', {"example_en": 'By the way, have you heard from Mark?'}),
    1995: (T + '«in Cologne» — без нужды', {"example_en": 'You have to change in Birmingham'}),
    2040: (T + 'оборвано', {"example_en": "He's fallen in love with his neighbour"}),
    2041: (T + 'повтор «the key»', {"example_en": "Don't lose your phone again!"}),
    2071: (T + 'учебниково', {"example_en": "I'm getting ready for the exam"}),
    2089: (T + 'нет слова карточки «because of»', {"example_en": 'There are no trains because of the strike'}),
    2095: (T + 'не то значение', {"example_en": "From now on I'll keep working here"}),
    2216: (T + 'повтор 6355 «open the door»', {"example_en": 'Will you open the wine?'}),
    2295: (T + 'нет слова карточки «population»', {"example_en": "The city's population is growing"}),
    2458: (T + 'учебниково', {"example_en": 'This cheese is too fatty for me'}),
    2603: (T + 'нет слова карточки «barely»', {"example_en": 'Without my glasses I can barely see'}),
    2668: (T + 'повтор 631 «After the meal»', {"example_en": 'After you left, your mum called'}),
    2880: (T + 'повтор 6284 «I forgot»', {"example_en": "It's a total disaster"}),
    2950: (T + 'оборвано', {"example_en": 'I hurt my hand in the kitchen'}),
    6241: (T + "шаблон «That's … good»", {"example_en": "It's pretty cold today"}),
}

REPLACE = []

SPLIT_LATER = {}
