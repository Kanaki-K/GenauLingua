"""Шаг 2, pl, порция 31: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    11263: (T + "word in example", {"t_pl": "wrażliwy, z wyczuciem, delikatnie"}),
    11410: (T + "word in example", {"t_pl": "opamiętanie, rozum, (zur Besinnung kommen) opamiętać się"}),
    11465: (T + "word in example", {"t_pl": "chętny, łasy na, (erpicht sein) bardzo chcieć"}),
    11544: (T + "word in example", {"t_pl": "dążenie, staranie, (bestrebt sein) dążyć"}),
}

REPLACE = []
SPLIT_LATER = {}
