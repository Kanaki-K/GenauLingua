"""Шаг 2, pl, порция 5: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    1262: (T + "word in example", {"t_pl": "szczególnie, zwłaszcza, wyjątkowo"}),
    1530: (T + "word in example", {"t_pl": "do środka, (herein!) proszę wejść"}),
    1634: (T + "word in example", {"t_pl": "złożyć wypowiedzenie, wypowiedzieć umowę, (z pracy) zwolnić się"}),
    1726: (T + "word in example", {"t_pl": "zdenerwowany, nerwowy, (nervös sein) denerwować się"}),
    1934: (T + "word in example", {"t_pl": "zespół, ekipa, drużyna"}),
    2295: (T + "word in example", {"x_pl": "Na festynie była połowa mieszkańców wsi"}),
}

REPLACE = []
SPLIT_LATER = {}
