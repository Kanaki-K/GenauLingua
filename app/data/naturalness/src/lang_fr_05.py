"""Вычитка французского, порция p005 (A2), 23.10: «nous» → «on», нет слова карточки, кальки"""

T = "вычитка французского: "

FIXES = {
    1196: (T + "«Tout le monde est là sauf moi» — нелогично", {"example_fr": "Tout le monde est venu sauf lui"}),
    1232: (T + "нет слова карточки «terminer»", {"example_fr": "Terminons là, je dois y aller"}),
    1366: (T + "«nous» → «on»", {"example_fr": "On emménage la semaine prochaine"}),
    1537: (T + "нет слова карточки «là-bas»", {"example_fr": "Pour aller là-bas, c'est dix euros, vingt aller-retour"}),
    1685: (T + "нет слова карточки «la foule»", {"example_fr": "Il y avait une foule de gens à la fête"}),
    1865: (T + "нет слова карточки «poser»", {"example_fr": "Pose-toi là, sur le canapé"}),
    2083: (T + "«nous» → «on»", {"example_fr": "On ne parle pas pendant le repas"}),
    2111: (T + "нет слова карточки «le vœu»", {"example_fr": "C'est mon vœu le plus cher"}),
    2295: (T + "нет слова карточки «la population»", {"example_fr": "La moitié de la population du village était à la fête"}),
    2603: (T + "нет слова карточки «à peine»", {"example_fr": "J'ai à peine dormi cette nuit"}),
    6206: (T + "нет слова карточки «dedans»", {"example_fr": "Allez, tout le monde dedans, il fait froid !"}),
    6247: (T + "«nous» → «on»", {"example_fr": "On peut essayer"}),
    6309: (T + "резко, без «s'il te plaît»", {"example_fr": "Appelle au moins, s'il te plaît"}),
}

REPLACE = []

SPLIT_LATER = {}
