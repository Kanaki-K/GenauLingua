"""Вычитка французского, порция p013 (B1), 23.10: нет слова карточки, «nous» → «on»"""

T = "вычитка французского: "

FIXES = {
    2792: (T + "нет слова карточки «changer»", {"example_fr": "Change de vitesse avant le virage !"}),
    2909: (T + "нет слова карточки «le contact»", {"example_fr": "Il a un très bon contact avec les enfants"}),
    2972: (T + "нет слова карточки «la compréhension»", {"example_fr": "Merci pour ta compréhension"}),
    3029: (T + "«Nous partons … notre» — книжно", {"example_fr": "On part en vacances avec la caravane"}),
    3060: (T + "нет слова карточки «revenir»", {"example_fr": "Après dix ans à l'étranger, elle est revenue dans sa ville natale"}),
}

REPLACE = []

SPLIT_LATER = {}
