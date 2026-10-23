"""Вычитка французского, порция p003 (A1–A2), 23.10: книжное «nous», нет слова карточки, кальки → разговорный французский"""

T = "вычитка французского: "

FIXES = {
    1426: (T + "«nous» → «on»", {"example_fr": "On prend l'avion pour l'Espagne"}),
    1463: (T + "«m'appartient» — книжно", {"example_fr": "Ce livre est à moi"}),
    1486: (T + "«nous» → «on»", {"example_fr": "On veut absolument gagner le match"}),
    1790: (T + "«Sous la pluie, nous avons été» — коряво", {"example_fr": "On a été complètement trempés par la pluie"}),
    1946: (T + "«nous» → «on»", {"example_fr": "Demain, on a un contrôle"}),
    1997: (T + "«nous» → «on»", {"example_fr": "On déménage le mois prochain"}),
    2084: (T + "«nous» → «on»", {"example_fr": "Le week-end, on fait de la randonnée"}),
    2140: (T + "«nous» → «on»", {"example_fr": "On doit être à l'aéroport deux heures avant le décollage"}),
    2539: (T + "«Nous réservons» — книжно", {"example_fr": "On prend la demi-pension"}),
    2895: (T + "«nous» → «on»", {"example_fr": "On passe la nuit à l'hôtel au bord du lac"}),
    6252: (T + "«Regarde ici» — калька", {"example_fr": "Regarde ça"}),
    6298: (T + "«je n'ai que peu de» — книжно", {"example_fr": "Aujourd'hui, j'ai peu de temps"}),
    6347: (T + "нет слова карточки «connu»", {"example_fr": "Cette chanson est très connue"}),
    6396: (T + "«Ça me rappelle toi» — ошибка", {"example_fr": "Cette chanson me rappelle nos vacances"}),
    6487: (T + "«enfin à nouveau» — коряво", {"example_fr": "Aujourd'hui, le soleil brille enfin"}),
    7695: (T + "«Nous avons … notre bureau» — книжно", {"example_fr": "Au bureau, on a beaucoup de collègues étrangers"}),
    8334: (T + "нет слова карточки «compléter»", {"example_fr": "Je complète la liste de courses : du lait et des œufs"}),
    10420: (T + "нет слова карточки «étranger»", {"example_fr": "Excusez-moi, je suis étranger ici, où est la gare ?"}),
    11702: (T + "«Nous nous retrouvons» — книжно", {"example_fr": "On se retrouve dans notre café préféré"}),
    11777: (T + "«Nous mangeons … au dîner» — книжно", {"example_fr": "Ce soir, on mange du poulet"}),
    12158: (T + "«nous» → «on»", {"example_fr": "Ce week-end, on va à deux fêtes"}),
    12253: (T + "«nous allons … en boîte de nuit» — книжно", {"example_fr": "Ce soir, on va danser en boîte"}),
    13317: (T + "«nous» → «on»", {"example_fr": "Avec cette voiture, on part en vacances"}),
    13354: (T + "«Nous sommes quatre» — книжно", {"example_fr": "On est quatre"}),
    15019: (T + "нет слова карточки «le parent»", {"example_fr": "Des parents éloignés viennent me rendre visite"}),
    15029: (T + "«Ma compagne et moi avons» — калька", {"example_fr": "Avec ma compagne, on a de grands projets pour l'avenir"}),
    17163: (T + "«Nous avons besoin de nos» — книжно", {"example_fr": "Pour le voyage, il nous faut nos passeports"}),
    17250: (T + "«nous» → «on»", {"example_fr": "On visite le nouvel appartement"}),
    18160: (T + "«nous» → «on»", {"example_fr": "On a loué un petit appartement"}),
    21: (T + "«nous» → «on»", {"example_fr": "On prend un autre chemin"}),
}

REPLACE = []

SPLIT_LATER = {}
