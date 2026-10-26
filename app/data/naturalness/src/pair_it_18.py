"""Шаг 2, it, порция 18: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    10048: (T + "word in example", {"t_it": "onesto, sincero, (ehrlich gesagt) sinceramente"}),
    10113: (T + "word in example", {"t_it": "nauseato, cattivo, (mir ist übel) ho la nausea"}),
    10221: (T + "word in example", {"t_it": "furbo, intelligente, sveglio"}),
    10256: (T + "word in example", {"t_it": "l'idiota, lo stupido, lo scemo"}),
    10282: (T + "word in example", {"t_it": "incantevole, carino, delizioso"}),
    10294: (T + "word in example", {"t_it": "l'errore, lo sbaglio, (im Irrtum sein) sbagliarsi"}),
    10360: (T + "word in example", {"x_it": "Ho un brutto presentimento"}),
}

REPLACE = []
SPLIT_LATER = {}
