"""Вычитка английского, порция p019 (B1), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка английского: "

FIXES = {
    10434: (T + 'нет слова карточки «loving»', {"example_en": "She's a very loving mother"}),
    10436: (T + 'книжно', {"example_en": 'The whole hall cheers as the band comes on stage'}),
    10443: (T + 'книжно', {"example_en": "The sky looks threatening, let's head home"}),
    10459: (T + 'повтор 10233 «will work»', {"example_en": "I doubt he's telling the truth"}),
    10460: (T + 'тавтология', {"example_en": 'My son is very fearful, he sleeps with the light on'}),
    10462: (T + 'учебниково', {"example_en": 'I appreciate your honesty'}),
    10463: (T + 'повтор 10233 «I fear»', {"example_en": "I'm a bit afraid of tomorrow's meeting"}),
    10548: (T + 'книжно', {"example_en": "Be realistic, we'll never finish before Friday"}),
    10812: (T + 'повтор 8285 «whistling»', {"example_en": 'The kids are playing cheerfully in the garden'}),
    11134: (T + 'повтор «my key»', {"example_en": 'My sock has disappeared in a mysterious way'}),
    11136: (T + 'книжно', {"example_en": 'Things are quite hectic at work right now'}),
    11337: (T + 'учебниково', {"example_en": "Her brother's mask frightened the little girl"}),
    11378: (T + 'без ситуации', {"example_en": "I'd never have thought him capable of that"}),
    11542: (T + 'без ситуации', {"example_en": 'I always stand up for my friends'}),
    11708: (T + 'учебниково', {"example_en": "I can't swallow these huge tablets"}),
    11711: (T + 'повтор «Gran makes the best»', {"example_en": 'On Sundays we have pancakes with syrup'}),
    11732: (T + 'нет слова карточки «thirsty»', {"example_en": 'After the match the players are really thirsty'}),
    11816: (T + '«currywurst» — не английский быт', {"example_en": "Let's grab a sandwich at the snack bar"}),
    11850: (T + 'повтор «for your cough» (11851)', {"example_en": "Don't eat too many sweets before dinner"}),
    11854: (T + 'повтор «Gran makes her own»', {"example_en": 'In the north they eat a lot of cabbage'}),
    11891: (T + 'нет слова карточки «refreshment»', {"example_en": 'Refreshments are served at the entrance'}),
    11944: (T + 'повтор 11945 «going to … for a»', {"example_en": 'We stayed at an old inn in the mountains'}),
    11945: (T + 'повтор 11944', {"example_en": 'The little bistro on the corner does great coffee'}),
    11969: (T + 'громоздко', {"example_en": 'Still or sparkling? – Still, please'}),
    11991: (T + 'повтор 11677 «after dinner we have»', {"example_en": 'My aunt makes her own cherry liqueur'}),
    12001: (T + 'тавтология', {"example_en": "He's a regular, the waiter knows his order by heart"}),
    12007: (T + 'калька', {"example_en": 'It needs a bit more seasoning'}),
    12027: (T + 'повтор «Gran makes … every year»', {"example_en": 'Redcurrant jelly goes really well with cheese'}),
    12028: (T + 'учебниково', {"example_en": 'We have turkey at Christmas'}),
    12098: (T + 'калька', {"example_en": 'What a pleasure to see you!'}),
}

REPLACE = []

SPLIT_LATER = {}
