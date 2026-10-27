"""Шаг 2, es, порция 20: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    12219: (T + "word in example", {"t_es": "empatado, indeciso, (unentschieden enden) terminar en empate"}),
    12535: (T + "word in example", {"t_es": "desmayado, impotente, (ohnmächtig werden) desmayarse"}),
    12595: (T + "word in example", {"t_es": "físico, corporal, físicamente"}),
}

REPLACE = []
SPLIT_LATER = {}
