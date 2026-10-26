"""Шаг 2, tr, порция 8: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    1226: (T + "word in example", {"t_tr": "işlemek, düzenlemek, ilgilenmek"}),
    1322: (T + "word in example", {"t_tr": "süre, süreklilik, (auf Dauer) uzun vadede"}),
    1337: (T + "word in example", {"t_tr": "döndürmek, dönmek, film çekmek"}),
}

REPLACE = []
SPLIT_LATER = {}
