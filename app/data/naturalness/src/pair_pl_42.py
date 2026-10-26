"""Шаг 2, pl, порция 42: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    12820: (T + "word in example", {"t_pl": "spięty, sztywny, sztywno"}),
    14118: (T + "word in example", {"t_pl": "pośredniczyć, przekazywać, załatwić"}),
    14142: (T + "word in example", {"t_pl": "nakrzyczeć, krzyczeć na"}),
    14570: (T + "word in example", {"t_pl": "katolicki, (katholisch sein) być katolikiem"}),
    15133: (T + "word in example", {"t_pl": "zbierać się, spotykać się, zjeżdżać się"}),
}

REPLACE = []
SPLIT_LATER = {}
