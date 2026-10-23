"""Вычитка французского, порция p038 (B2/C1), 23.10: время — «nous» → «on», повторы, кальки"""

T = "вычитка французского: "

FIXES = {
    18663: (T + "повтор 18922 «repos après le repas»", {"example_fr": "Laisse-le se reposer, il est malade"}),
    18728: (T + "«m'aide à rester organisé» — калька", {"example_fr": "Le matin, j'ai ma petite routine : café, douche, journal"}),
    18739: (T + "«Nous vivons» — книжно", {"example_fr": "On vit à l'ère du numérique"}),
    18747: (T + "повтор 18772 «pêcher à l'aube»", {"example_fr": "On est partis à l'aube pour éviter les bouchons"}),
    18769: (T + "«nous avons vu» — книжно", {"example_fr": "Avant le mariage, on a vu avec le prêtre le déroulement de la cérémonie"}),
    18779: (T + "«nous nous offrons» — книжно", {"example_fr": "La veille de Noël, on s'offre les cadeaux"}),
    18787: (T + "«nous voulons» — книжно", {"example_fr": "Après trois ans en Espagne, on veut maintenant y vivre de façon permanente"}),
    7668: (T + "«fatiguer mes yeux» — калька", {"example_fr": "Lire sans lunettes, ça me fatigue les yeux"}),
}

REPLACE = []

SPLIT_LATER = {}
