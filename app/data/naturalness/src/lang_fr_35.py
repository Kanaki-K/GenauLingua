"""Вычитка французского, порция p035 (B2), 23.10: природа и право — повторы, нет слова карточки, «nous» → «on»"""

T = "вычитка французского: "

FIXES = {
    15549: (T + "«nous avons vu» — книжно", {"example_fr": "Dans la forêt, on a vu un grand cerf"}),
    16150: (T + "нет слова карточки «le drapeau»", {"example_fr": "Les supporters agitent des drapeaux dans le stade"}),
    16182: (T + "«Tu dois signer» — калька", {"example_fr": "Signez ici, s'il vous plaît"}),
    16183: (T + "«Ils veulent l'accuser» — калька", {"example_fr": "On l'accuse de vol, mais il n'a rien fait"}),
    16186: (T + "«cela» — книжно", {"example_fr": "Après l'attaque, il voulait sa vengeance, mais ça n'apporterait que plus de problèmes"}),
    16198: (T + "повтор 16189 «faux passeport»", {"example_fr": "Ce sac Chanel à 30 euros, c'est forcément une contrefaçon"}),
    16206: (T + "«pour sa mauvaise conduite» — книжно", {"example_fr": "Comme punition, il est privé de téléphone pendant une semaine"}),
    16256: (T + "«Le code régit le comportement» — книжно", {"example_fr": "Chez les motards, il y a un code d'honneur"}),
}

REPLACE = []

SPLIT_LATER = {}
