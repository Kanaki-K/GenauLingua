"""Шаг 2, it, порция 47: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    11938: (T + "word in example", {"x_it": "Non risucchiare quando bevi, è maleducato!"}),
    12029: (T + "word in example", {"t_it": "bollito, cotto, (gekochtes Ei) sodo"}),
    12357: (T + "word in example", {"t_it": "la portata di tiro, la gittata, (außer Schussweite bleiben) stare alla larga"}),
}

REPLACE = []
SPLIT_LATER = {}
