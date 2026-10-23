"""Вычитка французского, порция p034 (B2), 23.10: культура и семья — повторы, кальки, «nous» → «on»"""

T = "вычитка французского: "

FIXES = {
    14465: (T + "повтор 15429 «faire voler un cerf-volant»", {"example_fr": "Dans le conte, le chevalier tue le dragon"}),
    14512: (T + "повтор 12141 «les spectateurs applaudissent fort»", {"example_fr": "Les enfants applaudissent à chaque tour du magicien"}),
    14526: (T + "учебниково", {"example_fr": "Le chapelain de l'hôpital passe voir les malades"}),
    14541: (T + "«Ma famille religieuse célèbre» — калька", {"example_fr": "Mes grands-parents sont très religieux"}),
    15043: (T + "«nous nous marions» — книжно", {"example_fr": "Mon fiancé et moi, on se marie le mois prochain"}),
    15045: (T + "«Mon enfant adopté est très heureux avec nous» — коряво", {"example_fr": "Leur fils adopté vient de Colombie"}),
    15094: (T + "«nous mélangeons» — книжно", {"example_fr": "En chimie, on mélange un acide et une base"}),
    15106: (T + "«spätzle» — не французский быт", {"example_fr": "Ma belle-mère m'a appris à faire la pâte à crêpes"}),
}

REPLACE = []

SPLIT_LATER = {}
