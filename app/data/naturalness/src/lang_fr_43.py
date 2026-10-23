"""Вычитка французского, порция p043 (C1), 23.10: нет слова карточки, «nous» → «on»"""

T = "вычитка французского: "

FIXES = {
    15703: (T + "нет слова карточки «refroidir»", {"example_fr": "Laisse refroidir la soupe avant de la donner au petit"}),
    16379: (T + "«nous avons désigné» — книжно", {"example_fr": "Au cas où, on a désigné ma sœur comme tutrice de nos enfants"}),
}

REPLACE = []

SPLIT_LATER = {}
