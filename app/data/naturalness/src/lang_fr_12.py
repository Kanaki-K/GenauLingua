"""Вычитка французского, порция p012 (B1), 23.10: «nous» → «on», нет слова карточки, коряво"""

T = "вычитка французского: "

FIXES = {
    2490: (T + "нет слова карточки «la frustration», повтор с 2491", {"example_fr": "Après la dispute, toute ma frustration est sortie"}),
    2511: (T + "«nous» → «on»", {"example_fr": "On a beaucoup de points communs"}),
    2620: (T + "«Nous devons» — книжно", {"example_fr": "Il faut qu'on résolve ce conflit"}),
    2629: (T + "«La voiture a eu une rayure» — калька", {"example_fr": "Il y a une rayure sur la voiture"}),
    2643: (T + "нет слова карточки «l'entrepôt»", {"example_fr": "Les chaussures en 42, il n'y en a plus à l'entrepôt"}),
    2652: (T + "«de façon très vive» — коряво", {"example_fr": "J'en ai encore un souvenir très vif"}),
}

REPLACE = []

SPLIT_LATER = {}
