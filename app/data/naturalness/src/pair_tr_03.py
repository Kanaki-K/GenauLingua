"""Шаг 2, tr, порция 3: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример tr: "

FIXES = {
    1639: (T + "word in example", {"t_tr": "dükkân, mağaza"}),
    1937: (T + "word in example", {"t_tr": "parça, bölüm, kısım"}),
    2372: (T + "word in example", {"t_tr": "acil, (es eilig haben) acelesi olmak"}),
    10110: (T + "word in example", {"t_tr": "tebrik, (Herzlichen Glückwunsch) kutlu olsun"}),
    11668: (T + "word in example", {"t_tr": "susuzluk, (Durst haben) susamak"}),
    18564: (T + "word in example", {"t_tr": "uzun süre, (wie lange) ne zamandır"}),
}

REPLACE = []
SPLIT_LATER = {}
