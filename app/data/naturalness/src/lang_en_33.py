"""Вычитка английского, порция p033 (B2), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка английского: "

FIXES = {
    12947: (T + 'учебниково', {"example_en": 'The doctor says the little one is fit as a fiddle'}),
    13519: (T + 'повтор 13552 «hour and a half»', {"example_en": 'The film lasts one and a half hours'}),
    13520: (T + 'учебниково', {"example_en": 'In autumn the birds fly towards the south'}),
    13682: (T + 'учебниково', {"example_en": 'Take a jumper, it gets chilly in the evening'}),
    13777: (T + 'повтор 13719 «pyjamas all Sunday»', {"example_en": "You can keep your coat on, it's cold in here"}),
    14010: (T + "повтор 13979 «Don't lie to me»", {"example_en": 'He lies to everyone, even his mother'}),
    14020: (T + 'повтор «cake left over» (6383)', {"example_en": 'You can keep the money left over'}),
    14060: (T + 'повтор 14055 «let me know when he arrives»', {"example_en": 'We need to notify the family about the accident'}),
    14078: (T + 'повтор 10161 «computer»', {"example_en": 'This goddamn bus is late again'}),
}

REPLACE = []

SPLIT_LATER = {}
