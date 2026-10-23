"""Вычитка французского, порция p048 (C2), 23.10: повторы «nounours», «tuer le temps aux cartes», «performance remarquable»; «nous» → «on»"""

T = "вычитка французского: "

FIXES = {
    14320: (T + "повтор 7204 «une performance remarquable»", {"example_fr": "C'était vraiment une belle soirée"}),
    15278: (T + "повтор 12129 «sans son nounours, il ne s'endort pas»", {"example_fr": "Mon fils a reçu un ourson en peluche à sa naissance"}),
    15783: (T + "«nous pouvons» — книжно", {"example_fr": "À marée basse, on peut marcher jusqu'à l'île"}),
    15845: (T + "«réfrigérateur» — книжно", {"example_fr": "Le vieux frigo finit à la décharge"}),
    15855: (T + "«dompté et calme» — учебниково", {"example_fr": "Ce cheval sauvage a été dompté en un mois"}),
    16681: (T + "«Nous avons lancé» — книжно", {"example_fr": "On a lancé une pétition contre la fermeture de notre bibliothèque"}),
    16694: (T + "повтор 7028 «jouer aux cartes pour passer le temps»", {"example_fr": "Pour tuer le temps à l'aéroport, je lis"}),
}

REPLACE = []

SPLIT_LATER = {}
