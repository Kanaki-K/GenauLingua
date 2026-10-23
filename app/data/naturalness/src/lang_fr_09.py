"""Вычитка французского, порция p009 (B1), 23.10: «nous» → «on», повтор, нет слова карточки"""

T = "вычитка французского: "

FIXES = {
    1397: (T + "«nous» → «on»", {"example_fr": "On ouvre un nouveau magasin"}),
    1400: (T + "«nous» → «on»", {"example_fr": "On attend un bébé"}),
    1449: (T + "«nous» → «on»", {"example_fr": "On cuisine au gaz"}),
    1460: (T + "«nous» → «on»", {"example_fr": "On apprend un poème par cœur"}),
    1481: (T + "«nous le facturons» — книжно", {"example_fr": "Le petit-déjeuner, on le facture séparément"}),
    1482: (T + "«Nous aménageons» — книжно", {"example_fr": "On réaménage la pièce"}),
    1532: (T + "«nous» → «on»", {"example_fr": "On roule autour de la ville"}),
    1538: (T + "«nous» → «on»", {"example_fr": "On y va demain"}),
    1590: (T + "повтор с 1946", {"example_fr": "Demain, il y a un contrôle de maths"}),
    1594: (T + "«nous» → «on»", {"example_fr": "On a encore quelques petits meubles à vendre"}),
    1645: (T + "нет слова карточки «le parcours de vie»", {"example_fr": "Le parcours de vie de mon grand-père l'a mené dans cinq pays"}),
    1663: (T + "«nous» → «on»", {"example_fr": "On part à 8 heures"}),
    1680: (T + "«Chaque matin» — книжно", {"example_fr": "Le matin, je fais dix minutes de méditation"}),
}

REPLACE = []

SPLIT_LATER = {}
