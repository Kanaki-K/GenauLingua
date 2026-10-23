"""Вычитка французского, порция p039 (C1), 23.10: «Chaque matin» → «Le matin», повтор «deuxième division»"""

T = "вычитка французского: "

FIXES = {
    8007: (T + "«Chaque matin» — калька", {"example_fr": "Le matin, il se verse un demi-paquet de muesli dans son bol"}),
    8022: (T + "повтор 7336 «deuxième division»", {"example_fr": "Si on perd aujourd'hui, on est relégués"}),
}

REPLACE = []

SPLIT_LATER = {}
