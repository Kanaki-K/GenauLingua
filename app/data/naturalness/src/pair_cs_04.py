"""Шаг 2, cs, порция 4: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    57: (T + "в примере učit se na", {"t_cs": "vyučení, vzdělání, (eine Ausbildung machen) učit se na …"}),
    98: (T + "в примере dej vědět", {"t_cs": "odpověď, vyrozumění, (Bescheid geben) dát vědět"}),
    161: (T + "в примере kvůli tomu", {"t_cs": "za to, kvůli tomu"}),
    234: (T + "в примере poprvé", {"t_cs": "první, (zum ersten Mal) poprvé"}),
    393: (T + "в примере horko", {"t_cs": "horký, (es ist heiß) je horko"}),
    459: (T + "в примере stydne", {"t_cs": "studený, chladný, (kalt werden) stydnout"}),
    549: (T + "в примере naposledy", {"t_cs": "poslední, minulý, (das letzte Mal) naposledy"}),
    705: (T + "в примере poštou", {"t_cs": "přes, (per Post) poštou"}),
    757: (T + "в примере v důchodu, не důchodce", {"x_cs": "Táta je od loňska důchodce"}),
    789: (T + "в примере dáš", {"t_cs": "darovat, věnovat, dát (dárek)"}),
    796: (T + "в примере vážné", {"t_cs": "zlý, hrozný, vážný"}),
}

REPLACE = []
SPLIT_LATER = {}
