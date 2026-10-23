"""Вычитка французского, порция p028 (B2), 23.10: книжные короткие примеры → разговорные"""

T = "вычитка французского: "

FIXES = {
    7476: (T + "«Un grand merci lui revient pour cela» — книжно", {"example_fr": "Tout le mérite lui revient"}),
    7509: (T + "«infliger de souffrance» — книжно", {"example_fr": "Ses mots m'ont causé beaucoup de peine"}),
    7818: (T + "«confine à la folie» — книжно", {"example_fr": "Ton idée frise la folie !"}),
    8113: (T + "«déguise sa voix quand il parle au chef» — странно", {"example_fr": "Au téléphone, il a déguisé sa voix pour me faire une blague"}),
    8116: (T + "«en toute innocence» — книжно", {"example_fr": "Je me suis retrouvé mêlé à leur dispute sans le vouloir"}),
}

REPLACE = []

SPLIT_LATER = {}
