"""Вычитка французского, порция p006 (A2), 23.10: «nous» → «on», нет слова карточки, кальки"""

T = "вычитка французского: "

FIXES = {
    6324: (T + "нет слова карточки «dehors»", {"example_fr": "Allez, dehors !"}),
    6421: (T + "нет слова карточки «en avant»", {"example_fr": "Encore un peu en avant, stop !"}),
    6641: (T + "«Nous sommes assis» — книжно", {"example_fr": "On s'assoit en cercle"}),
    6696: (T + "нет слова карточки «doux»", {"example_fr": "Ce coussin est tout doux"}),
    7288: (T + "нет слова карточки «véritable»", {"example_fr": "La véritable raison, c'est que je n'ai pas envie"}),
    8839: (T + "нет слова карточки «se procurer»", {"example_fr": "Tu peux te procurer encore quelques chaises pour la fête ?"}),
    9765: (T + "«nous avons besoin» — книжно", {"example_fr": "Pour la nouvelle voiture, il nous faut un crédit"}),
    10129: (T + "нет слова карточки «l'intérêt»", {"example_fr": "Je n'ai aucun intérêt pour le foot"}),
    10266: (T + "нет слова карточки «dramatique»", {"example_fr": "Ce n'est pas si dramatique !"}),
    11772: (T + "«nous» → «on»", {"example_fr": "On déjeune à la cafétéria"}),
    12155: (T + "«a lieu un grand concours» — книжно", {"example_fr": "La semaine prochaine, il y a un grand concours"}),
    13338: (T + "«Je m'en réjouis» — книжно", {"example_fr": "J'y pense déjà avec plaisir"}),
    13346: (T + "«Ici … à la maison» — повтор", {"example_fr": "Il n'y a personne à la maison"}),
    13362: (T + "нет слова карточки «ceci»", {"example_fr": "Tu as fait quoi ce week-end ? — Oh, ceci et cela"}),
    13452: (T + "«nous allons nous promener» — книжно", {"example_fr": "Malgré la pluie, on va se promener"}),
    13843: (T + "«Ta voix est belle» — калька", {"example_fr": "Tu as une belle voix"}),
    15954: (T + "«nous» → «on»", {"example_fr": "On a signé le contrat"}),
    17075: (T + "«nous» → «on»", {"example_fr": "On fait un tour de la ville"}),
}

REPLACE = []

SPLIT_LATER = {}
