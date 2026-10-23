"""Вычитка французского, порция p036 (B2), 23.10: право, транспорт — «nous» → «on», повторы, нет слова карточки"""

T = "вычитка французского: "

FIXES = {
    16289: (T + "«nous avons pu» — книжно", {"example_fr": "Avant l'enterrement, on a pu dire au revoir à papi à la chambre funéraire"}),
    16320: (T + "повтор 15424 «notre jardin comme son territoire»", {"example_fr": "Les loups défendent leur territoire"}),
    17133: (T + "«Nous avons dû» — книжно", {"example_fr": "On a dû faire demi-tour à cause de la pluie"}),
    17146: (T + "«Mon départ est» — калька", {"example_fr": "Le départ est prévu demain à sept heures"}),
    17153: (T + "нет слова карточки «le chemin du retour»", {"example_fr": "Sur le chemin du retour, on s'est arrêtés manger"}),
    17171: (T + "«Nous prenons» — книжно", {"example_fr": "On prend le métro jusqu'à la gare"}),
}

REPLACE = []

SPLIT_LATER = {}
