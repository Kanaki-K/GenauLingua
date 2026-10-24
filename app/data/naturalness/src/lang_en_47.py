"""Вычитка английского, порция p047 (C2), 23.10: кальки, повторы, нет слова карточки, голые фразы"""

T = "вычитка английского: "

FIXES = {
    11610: (T + 'повтор 10345 «stupid idea»', {"example_en": 'What a daft idea!'}),
    11613: (T + 'без ситуации', {"example_en": "He's a true philanthropist, he helps everyone"}),
    11956: (T + 'без ситуации', {"example_en": 'Shall we have an aperitif on the terrace?'}),
    11997: (T + 'повтор 11677 «after the meal we drink»', {"example_en": 'Grandad always offers guests a glass of port'}),
    12945: (T + 'учебниково', {"example_en": 'A body temperature of 37 degrees is normal'}),
    13124: (T + 'повтор 6944 «hangover»', {"example_en": 'The day after the wedding everyone was hungover'}),
    14218: (T + '«Ms Schmidt» — не английская фамилия', {"example_en": 'On the school trip Ms Green is the contact person if anything happens'}),
}

REPLACE = []

SPLIT_LATER = {}
