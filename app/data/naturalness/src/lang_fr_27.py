"""Вычитка французского, порция p027 (B2), 23.10: «nous» → «on», «cela» → «ça», повторы, нет слова карточки"""

T = "вычитка французского: "

FIXES = {
    7109: (T + "«deviner l'énigme» — учебниково", {"example_fr": "Devine qui j'ai vu hier !"}),
    7129: (T + "повтор 6990 «période difficile»", {"example_fr": "Avec un seul salaire, on a du mal à s'en sortir"}),
    7132: (T + "«Nous devons» — книжно", {"example_fr": "Éteins les bougies avant d'aller te coucher"}),
    7137: (T + "«Nous regardons» — книжно", {"example_fr": "On regarde le soleil se coucher sur la mer"}),
    7142: (T + "«La fourmi est minuscule» — учебниково", {"example_fr": "L'appartement est minuscule, mais très bien placé"}),
    7145: (T + "нет слова карточки «céder»", {"example_fr": "Elle n'a pas cédé, même quand tout le monde criait"}),
    7161: (T + "«Ils voulaient» — калька", {"example_fr": "On l'a mis à la porte du bar"}),
    7168: (T + "повтор 15460 «aigle au-dessus des montagnes»", {"example_fr": "Des vautours tournoient au-dessus du champ"}),
    7180: (T + "учебниково", {"example_fr": "Je n'aime pas les fêtes, les discours et ce genre de choses"}),
    7206: (T + "«sortir ça» — без ситуации", {"example_fr": "Tu peux sortir la poubelle ?"}),
    7213: (T + "«Cela donne» — книжно", {"example_fr": "Ça donne à toute l'affaire un autre sens"}),
    7237: (T + "«parce que je ne me sens pas bien» — учебниково", {"example_fr": "Si ça ne passe pas, va consulter un médecin"}),
    7245: (T + "«La voiture est prête à partir pour le voyage» — громоздко", {"example_fr": "Tout le monde est prêt à partir ?"}),
    7262: (T + "«je pourrais m'endormir» — неполно", {"example_fr": "Je suis tellement fatigué que je pourrais dormir debout"}),
    7282: (T + "«Nous échangeons» — книжно", {"example_fr": "On échange nos numéros ?"}),
    7290: (T + "«Nous pouvons» — книжно", {"example_fr": "On peut aller au cinéma, à condition que tu aies le temps"}),
    7296: (T + "повтор 15831 «moustiques … cet été»", {"example_fr": "Les embouteillages sont un vrai fléau dans cette ville"}),
    7304: (T + "«Nous sommes membres» — книжно, длинно", {"example_fr": "On est membres de la section locale du Club alpin"}),
    7308: (T + "«Cela renforce» — книжно", {"example_fr": "Ça renforce encore mes soupçons"}),
    7329: (T + "«Le ballon flotte dans l'air» — учебниково", {"example_fr": "Une odeur de café flotte dans l'air"}),
    7345: (T + "«Nous habitons» — книжно", {"example_fr": "On habite à une vingtaine de kilomètres à l'est de Lyon"}),
    7359: (T + "«Nous voulons» — книжно", {"example_fr": "On veut agrandir la cuisine"}),
    7398: (T + "«Je dois aiguiser» — калька", {"example_fr": "Ce couteau ne coupe plus, il faut l'aiguiser"}),
    7412: (T + "«Nous étions» — книжно", {"example_fr": "On était en plein milieu du film quand le courant a sauté"}),
}

REPLACE = []

SPLIT_LATER = {}
