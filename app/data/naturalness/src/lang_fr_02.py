"""Вычитка французского, порция p002 (A1), 23.10: книжное «nous» и кальки → разговорный французский"""

T = "вычитка французского: "

FIXES = {
    541: (T + "«Nous aimons» — книжно", {"example_fr": "On aime bien vivre dans cette ville"}),
    571: (T + "«a demandé après toi» — калька", {"example_fr": "L'homme là-bas t'a demandé"}),
    578: (T + "«nous» → «on»", {"example_fr": "Cet été, on part à la mer"}),
    599: (T + "повтор с 238, «nous» → «on»", {"example_fr": "À midi, on mange à la cantine"}),
    614: (T + "«Chaque matin» — книжно", {"example_fr": "Le matin, je bois du thé"}),
    621: (T + "«il fait plus chaud» — коряво", {"example_fr": "En mars, il commence à faire plus chaud"}),
    625: (T + "«Nous n'aimons pas» — книжно", {"example_fr": "On n'aime pas les oignons dans la soupe"}),
    631: (T + "«nous sortons» — книжно", {"example_fr": "Après le repas, on sort"}),
    704: (T + "«nous» → «on»", {"example_fr": "On fait une pause"}),
    715: (T + "«Quel est le plan» — книжно", {"example_fr": "C'est quoi, le plan ?"}),
    761: (T + "«nous» → «on»", {"example_fr": "Ce soir, on mange au restaurant"}),
    820: (T + "«nous» → «on»", {"example_fr": "On va à la piscine"}),
    848: (T + "«nous» → «on»", {"example_fr": "On doit venir à trois heures"}),
    861: (T + "«Nous jouons au football» — книжно", {"example_fr": "On joue au foot"}),
    872: (T + "«nous» → «on»", {"example_fr": "On mange plus tard"}),
    880: (T + "нет слова карточки «être debout»", {"example_fr": "On attend debout à l'arrêt"}),
    912: (T + "«nous» → «on»", {"example_fr": "On danse ensemble ?"}),
    970: (T + "«nous» → «on»", {"example_fr": "On part en vacances"}),
    987: (T + "«nous» → «on»", {"example_fr": "On viendra peut-être demain"}),
    1023: (T + "«Nous allons plus loin» — книжно", {"example_fr": "On continue plus loin"}),
    1059: (T + "«nous» → «on»", {"example_fr": "On veut aller nager demain"}),
    1085: (T + "«nous» → «on»", {"example_fr": "On mange ensemble ce soir ?"}),
    1266: (T + "«une eau» — коряво", {"example_fr": "Je commande une bouteille d'eau"}),
    1315: (T + "«va vous aider volontiers» — калька с gern", {"example_fr": "La dame à l'accueil se fera un plaisir de vous aider"}),
    1316: (T + "нет слова карточки «pour que»", {"example_fr": "Je révise pour que l'examen se passe bien"}),
    1317: (T + "«Je veux te remercier» — резко", {"example_fr": "Je voulais te remercier pour ton aide"}),
}

REPLACE = []

SPLIT_LATER = {}
