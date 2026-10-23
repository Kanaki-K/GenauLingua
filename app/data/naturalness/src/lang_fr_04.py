"""Вычитка французского, порция p004 (A2), 23.10: «nous» → «on», нет слова карточки, кальки"""

T = "вычитка французского: "

FIXES = {
    162: (T + "«nous» → «on»", {"example_fr": "Après, on rentre à la maison"}),
    184: (T + "«Ce livre-ci» — книжно", {"example_fr": "Ce livre est intéressant"}),
    262: (T + "«nous» → «on»", {"example_fr": "Les jours fériés, on ne travaille pas"}),
    538: (T + "нет слова карточки «ennuyeux»", {"example_fr": "Ce film est vraiment ennuyeux"}),
    607: (T + "«aménagée de façon très moderne» — книжно", {"example_fr": "La cuisine est très moderne"}),
    858: (T + "нет слова карточки «le plaisir»", {"example_fr": "Merci, c'était un vrai plaisir !"}),
    923: (T + "«Jouons» — книжно", {"example_fr": "On joue au tennis ?"}),
    941: (T + "«Nous nous retrouvons» — книжно", {"example_fr": "On se retrouve à trois heures"}),
    993: (T + "нет слова карточки «passé»", {"example_fr": "L'été est déjà passé"}),
    1064: (T + "нет слова карточки «souhaiter»", {"example_fr": "Qu'est-ce que tu souhaites pour ton anniversaire ?"}),
    1073: (T + "«nous» → «on»", {"example_fr": "On va au centre-ville faire du shopping"}),
    1093: (T + "«Au fond, tu veux manger» — коряво", {"example_fr": "Tu n'as pas faim du tout ?"}),
    1103: (T + "«baccalauréat» → «bac»", {"example_fr": "L'année prochaine, je passe le bac"}),
    1130: (T + "«nous» → «on»", {"example_fr": "On va faire autrement"}),
}

REPLACE = []

SPLIT_LATER = {}
