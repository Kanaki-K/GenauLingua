"""Шаг 2, fr, порция 10: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример fr: "

FIXES = {
    1827: (T + "s'est fait très chic — неестественно", {"x_fr": "Il s'est habillé très chic pour le mariage"}),
    1877: (T + "в примере soigneusement", {"t_fr": "soigneux, minutieux, soigneusement"}),
    2145: (T + "в примере annuler", {"t_fr": "le refus, l'annulation, (absagen) annuler"}),
}

REPLACE = []
SPLIT_LATER = {}
