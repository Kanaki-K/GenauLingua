"""Вычитка французского, порция p050 (C2), 23.10: повтор «après la fête, la cuisine…», нет слова карточки, «nous» → «on»"""

T = "вычитка французского: "

FIXES = {
    18386: (T + "«Je dois encore» — калька", {"example_fr": "Il faut encore préparer la chambre d'amis avant l'arrivée des invités"}),
    18388: (T + "повтор 16143 «après la fête, la cuisine ressemble à»", {"example_fr": "Ta chambre, c'est un vrai foutoir !"}),
    18408: (T + "«Nous passons chaque mois d'août» — книжно", {"example_fr": "Tous les mois d'août, on part dans notre maison de vacances au bord du lac"}),
    18908: (T + "нет слова карточки «incessant»", {"example_fr": "Le bruit incessant des travaux me rend fou"}),
}

REPLACE = []

SPLIT_LATER = {}
