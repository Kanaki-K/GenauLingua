"""Вычитка французского, порция p049 (C2), 23.10: повторы «Pars devant, je te rejoins», «capteur … lumière»; «nous» → «on»"""

T = "вычитка французского: "

FIXES = {
    16932: (T + "«Une révision … est nécessaire» — канцелярит", {"example_fr": "L'avocat demande une révision du procès"}),
    17302: (T + "«Nous passons» — книжно", {"example_fr": "Cet été, on part sur la Riviera"}),
    17315: (T + "повтор 6493 «Pars devant, je te rejoins»", {"example_fr": "Partez devant, on vous rejoint en voiture"}),
    17386: (T + "«nous rentrons» — книжно", {"example_fr": "Demain, on rentre en avion à Lyon"}),
    17680: (T + "повтор 17746 «détecte le mouvement et allume la lumière»", {"example_fr": "Le capteur de pluie allume les essuie-glaces tout seul"}),
    17726: (T + "учебниково", {"example_fr": "Cette chaîne de télévision ne passe que des séries"}),
}

REPLACE = []

SPLIT_LATER = {}
