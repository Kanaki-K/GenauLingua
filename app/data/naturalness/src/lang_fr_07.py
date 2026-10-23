"""Вычитка французского, порция p007 (A2–B1), 23.10: «nous» → «on», нет слова карточки"""

T = "вычитка французского: "

FIXES = {
    18109: (T + "нет слова карточки «le sol»", {"example_fr": "L'assiette est tombée sur le sol"}),
    18216: (T + "нет слова карточки «la casserole»", {"example_fr": "Je fais de la soupe dans une grande casserole"}),
    18248: (T + "«nous» → «on»", {"example_fr": "On habite au troisième étage"}),
    18300: (T + "«nous» → «on»", {"example_fr": "On rénove la maison cet été"}),
    18667: (T + "«nous devons» — книжно", {"example_fr": "D'abord, il faut comprendre le problème"}),
    18750: (T + "«nous faisons toujours une fête» — книжно", {"example_fr": "À la Saint-Sylvestre, on fait toujours la fête"}),
    18933: (T + "«nous» → «on»", {"example_fr": "Le matin, on travaille au bureau"}),
    109: (T + "нет слова карточки «l'exercice»", {"example_fr": "J'ai besoin de plus d'exercice, je suis assis toute la journée"}),
    308: (T + "«nous organisons» — книжно", {"example_fr": "Samedi, on fait une fête dans le jardin"}),
    542: (T + "«La nourriture a augmenté» — коряво", {"example_fr": "Les produits alimentaires ont encore augmenté"}),
    632: (T + "«Notre voisin a réceptionné» — книжно", {"example_fr": "Le voisin a pris le colis pour nous"}),
}

REPLACE = []

SPLIT_LATER = {}
