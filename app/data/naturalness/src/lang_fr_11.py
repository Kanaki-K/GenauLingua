"""Вычитка французского, порция p011 (B1), 23.10: «nous» → «on», повтор, нет слова карточки"""

T = "вычитка французского: "

FIXES = {
    2221: (T + "«Nous nous partageons» — книжно", {"example_fr": "On se partage le travail"}),
    2286: (T + "«nous» → «on»", {"example_fr": "On a battu l'adversaire"}),
    2335: (T + "повтор с 1397, книжно", {"example_fr": "Le nouveau cinéma ouvre prochainement en centre-ville"}),
    2370: (T + "нет слова карточки «la propriété»", {"example_fr": "L'appartement n'est pas loué, c'est notre propriété"}),
    2426: (T + "«nous» → «on»", {"example_fr": "On doit augmenter les prix"}),
}

REPLACE = []

SPLIT_LATER = {}
