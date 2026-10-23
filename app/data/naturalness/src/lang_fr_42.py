"""Вычитка французского, порция p042 (C1), 23.10: нет слова карточки, «nous» → «on»"""

T = "вычитка французского: "

FIXES = {
    14118: (T + "нет слова карточки «servir de médiateur»", {"example_fr": "Le prof essaie de servir de médiateur entre les deux élèves"}),
    14835: (T + "«nous louions» — книжно", {"example_fr": "Avant, on louait un film au vidéoclub tous les vendredis"}),
}

REPLACE = []

SPLIT_LATER = {}
