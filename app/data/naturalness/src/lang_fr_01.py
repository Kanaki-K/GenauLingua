"""Вычитка французского, порция p001 (A1), 23.10: книжное «nous» и кальки → разговорный французский"""

T = "вычитка французского: "

FIXES = {
    2: (T + "«nous allons nous promener» — книжно", {"example_fr": "Le soir, on va se promener"}),
    55: (T + "«nous» → «on»", {"example_fr": "En août, on va à la mer"}),
    105: (T + "«nous rendons visite à notre» — книжно", {"example_fr": "On rend visite à mamie"}),
    116: (T + "«était très bon marché» — коряво", {"example_fr": "La veste n'était vraiment pas chère"}),
    117: (T + "«a un goût sucré» — калька", {"example_fr": "La poire est bien sucrée"}),
    141: (T + "«petit déjeuner» без дефиса, порядок", {"example_fr": "Au petit-déjeuner, ils mangent des petits pains"}),
    191: (T + "«nous préférons rester» — книжно", {"example_fr": "Il pleut dehors, alors on reste à la maison"}),
    197: (T + "«nous» → «on»", {"example_fr": "On passe par le parc"}),
    200: (T + "«nous avons le droit» — книжно", {"example_fr": "Aujourd'hui, on a le droit de rester plus longtemps"}),
    225: (T + "«Il est de Munich» — калька", {"example_fr": "Il vient de Munich"}),
    229: (T + "«Le collègue» → «Mon collègue»", {"example_fr": "Mon collègue m'a expliqué le nouveau logiciel en cinq minutes"}),
    238: (T + "«nous» → «on»", {"example_fr": "On mange à midi"}),
    261: (T + "«nous» → «on»", {"example_fr": "On fait la fête samedi"}),
    265: (T + "«la télévision» → «la télé»", {"example_fr": "Maintenant, je veux juste regarder la télé"}),
    278: (T + "«nous» → «on»", {"example_fr": "On va à l'aéroport"}),
    309: (T + "«Nous avons des invités» — книжно", {"example_fr": "On a des invités ce soir"}),
    330: (T + "«Je bois volontiers du thé» — калька с gern", {"example_fr": "Je prendrais volontiers un thé"}),
    337: (T + "нет слова карточки «l'entretien»", {"example_fr": "L'entretien avec le chef n'était pas si terrible"}),
    354: (T + "«nous aimons faire un barbecue» — книжно", {"example_fr": "L'été, on adore faire des barbecues"}),
    408: (T + "порядок слов", {"example_fr": "Son passe-temps, c'est la lecture"}),
    414: (T + "«Nous logeons» — книжно", {"example_fr": "On dort à l'hôtel"}),
    447: (T + "«la nouvelle année commence» — коряво", {"example_fr": "L'année commence en janvier"}),
    481: (T + "«nous» → «on»", {"example_fr": "On va au cinéma"}),
    527: (T + "«nous» → «on»", {"example_fr": "On peut manger ensemble demain"}),
    531: (T + "«réfrigérateur» → «frigo»", {"example_fr": "Le frigo est vide"}),
}

REPLACE = []

SPLIT_LATER = {}
