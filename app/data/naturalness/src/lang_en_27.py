"""Вычитка английского, порция p027 (B2), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка английского: "

FIXES = {
    7109: (T + 'тавтология', {"example_en": 'Guess who I saw yesterday!'}),
    7129: (T + 'повтор 6990 «get through this difficult time»', {"example_en": "On one salary it's hard to get through the month"}),
    7132: (T + 'без ситуации', {"example_en": 'Put out the candles before you go to bed'}),
    7137: (T + 'без ситуации', {"example_en": 'We watch the sun set over the sea'}),
    7142: (T + 'учебниково', {"example_en": 'The flat is tiny, but right in the centre'}),
    7145: (T + 'нет слова карточки «to give way»', {"example_en": "She didn't give way, even when everyone was shouting"}),
    7161: (T + 'калька', {"example_en": 'They threw him out of the bar'}),
    7168: (T + 'повтор 15460 «eagle over the mountains»', {"example_en": 'Vultures are circling over the field'}),
    7180: (T + 'учебниково', {"example_en": "Parties, speeches and the like aren't my thing"}),
    7206: (T + 'без ситуации', {"example_en": 'Can you take the rubbish out?'}),
    7213: (T + 'книжно', {"example_en": 'That gives the whole thing a different meaning'}),
    7237: (T + 'учебниково', {"example_en": "If it doesn't get better, go and see a doctor"}),
    7245: (T + 'громоздко', {"example_en": 'Is everyone ready to go?'}),
    7262: (T + 'оборвано', {"example_en": "I'm so tired I could sleep standing up"}),
    7296: (T + 'повтор 15831 «mosquitoes this summer»', {"example_en": 'The traffic is a real nuisance in this city'}),
    7304: (T + '«Munich» — длинно', {"example_en": "We're members of the local section of the Alpine Club"}),
    7308: (T + 'книжно', {"example_en": 'That only reinforces my suspicion'}),
    7329: (T + 'учебниково', {"example_en": 'A smell of coffee floats in the air'}),
    7345: (T + '«Berlin» — без нужды', {"example_en": 'We live about twenty kilometres east of York'}),
    7398: (T + 'калька', {"example_en": "This knife doesn't cut any more, it needs sharpening"}),
    7423: (T + 'повтор «key»', {"example_en": "Have you taken an umbrella? It's going to rain"}),
}

REPLACE = []

SPLIT_LATER = {}
