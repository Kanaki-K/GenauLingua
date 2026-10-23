"""Вычитка французского, порция p029 (B2), 23.10: «nous» → «on», нет слова карточки"""

T = "вычитка французского: "

FIXES = {
    8886: (T + "«a fait les nouvelles chansons» — коряво", {"example_fr": "Le producteur du groupe est aussi leur manager"}),
    8909: (T + "нет слова карточки «actif»", {"example_fr": "À 80 ans, elle est encore très active"}),
    8951: (T + "повтор 8877 «vient tous les …dis»", {"example_fr": "On partage une femme de ménage avec les voisins"}),
    8954: (T + "«Je dois encore faire» — калька", {"example_fr": "C'est toujours moi qui fais le sale boulot"}),
    9789: (T + "«nous allons» — книжно", {"example_fr": "Samedi, on va au centre commercial"}),
    9805: (T + "«Nous remboursons» — книжно", {"example_fr": "On rembourse encore notre prêt immobilier pendant 20 ans"}),
    9895: (T + "«nous avons vu» — книжно", {"example_fr": "Au trésor de Vienne, on a vu l'ancienne couronne impériale"}),
    10391: (T + "«Mon bien-aimé et moi partons» — книжно", {"example_fr": "Elle attend le retour de son bien-aimé"}),
}

REPLACE = []

SPLIT_LATER = {}
