"""Шаг 2, pl, порция 20: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    12166: (T + "word in example", {"t_pl": "kawał, psota, figiel"}),
    12208: (T + "word in example", {"t_pl": "aktywność, działalność, zajęcie"}),
    12219: (T + "word in example", {"t_pl": "remisowy, remis, niezdecydowany"}),
    12328: (T + "word in example", {"t_pl": "jazda na nartach, narciarstwo, (Ski fahren) jeździć na narty"}),
    12510: (T + "word in example", {"t_pl": "przypalony, poparzony, (verbrannt sein) przypalić się"}),
    12525: (T + "word in example", {"t_pl": "oddech, (außer Atem) zdyszany"}),
    12530: (T + "word in example", {"t_pl": "ratunek, ratowanie, (Rettungsaktion) akcja ratunkowa"}),
    12535: (T + "word in example", {"t_pl": "omdlały, bezsilny, (ohnmächtig werden) zemdleć"}),
    12922: (T + "word in example", {"t_pl": "odruch, refleks, odruchowo"}),
}

REPLACE = []
SPLIT_LATER = {}
