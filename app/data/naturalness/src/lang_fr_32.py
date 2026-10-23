"""Вычитка французского, порция p032 (B2), 23.10: еда, досуг, здоровье — «nous» → «on», повторы, кальки"""

T = "вычитка французского: "

FIXES = {
    11748: (T + "повтор «mamie fait … pour Noël»", {"example_fr": "Les enfants ont décoré les biscuits de Noël"}),
    11752: (T + "нет слова карточки «causer»", {"example_fr": "Le chien a causé une belle pagaille dans le salon"}),
    11762: (T + "«trop coriace pour être mangée» — книжно", {"example_fr": "La viande était coriace, impossible à couper"}),
    12188: (T + "повтор 7336 «monté en deuxième …»", {"example_fr": "Il joue dans une ligue amateur le dimanche"}),
    12209: (T + "«nous voulons juste» — книжно", {"example_fr": "Aujourd'hui, on traîne juste à la maison"}),
    12235: (T + "повтор 12282 «aller au bowling»", {"example_fr": "Le bowling est fermé le lundi"}),
    12282: (T + "«nous voulons aller» — книжно", {"example_fr": "Vendredi, on va faire du bowling avec des amis"}),
    12644: (T + "«On ne doit pas cracher» — калька", {"example_fr": "Ne crache pas par terre !"}),
    12653: (T + "«Je dois souffler» — калька", {"example_fr": "Laisse-moi souffler un peu"}),
    12686: (T + "«pas de colonne vertébrale, pas de courage» — калька", {"example_fr": "Il s'est blessé à la colonne vertébrale en tombant"}),
    12825: (T + "повтор 13067 «voir papy à la maison de retraite le dimanche»", {"example_fr": "Depuis que papy ne peut plus se lever seul, il vit en maison de retraite"}),
}

REPLACE = []

SPLIT_LATER = {}
