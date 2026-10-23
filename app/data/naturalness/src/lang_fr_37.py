"""Вычитка французского, порция p037 (B2), 23.10: техника, наука, дом — «nous» → «on», повторы, неверный смысл"""

T = "вычитка французского: "

FIXES = {
    17557: (T + "«Je dois pousser» — калька", {"example_fr": "Pousse le levier vers la gauche"}),
    17811: (T + "«nous pouvons» — книжно", {"example_fr": "Avec le capital de la vente, on peut lancer une nouvelle affaire"}),
    17857: (T + "«Mon associé et moi gérons» — книжно", {"example_fr": "Mon associé et moi, on gère l'entreprise ensemble"}),
    17958: (T + "повтор 17956 «les scientifiques…»", {"example_fr": "J'adore explorer les petites rues des villes que je visite"}),
    18183: (T + "«piaule … en désordre» — не тот смысл", {"example_fr": "Il loue une petite piaule près de la fac"}),
    18217: (T + "повтор 18385 «changer le(s) drap(s)»", {"example_fr": "Les draps sèchent sur le balcon"}),
    18235: (T + "повтор 6519 «à l'abri de la pluie»", {"example_fr": "La cabane au fond du jardin, c'est notre planque"}),
    18247: (T + "«nous avons trouvé» — книжно", {"example_fr": "Au grenier, on a trouvé des lettres de mamie dans un vieux coffre"}),
    18281: (T + "«nous avons» — книжно", {"example_fr": "Au restaurant, on a une petite réserve où il n'y a que des caisses de boissons"}),
}

REPLACE = []

SPLIT_LATER = {}
