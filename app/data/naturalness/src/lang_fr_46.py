"""Вычитка французского, порция p046 (C2), 23.10: «nous» → «on», повтор «parapluie»"""

T = "вычитка французского: "

FIXES = {
    8637: (T + "«nous sommes» — книжно", {"example_fr": "Au sens figuré, on est tous dans le même bateau"}),
    8656: (T + "повтор «prendre un parapluie» (8261, 11091)", {"example_fr": "Par précaution, j'ai fait une copie de mon passeport"}),
    9158: (T + "«Nous avons chargé» — книжно", {"example_fr": "On a chargé un peintre de repeindre la cage d'escalier"}),
    9920: (T + "«Nous avons déposé» — книжно", {"example_fr": "On a laissé le double des clés chez les voisins"}),
    11487: (T + "«dans le choix de la couleur» — книжно", {"example_fr": "Il est toujours indécis devant la carte du restaurant"}),
}

REPLACE = []

SPLIT_LATER = {}
