"""Шаг 2, it, порция 31: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    11465: (T + "word in example", {"x_it": "Mia figlia è desiderosa di prendere finalmente la patente e conta i giorni fino ai diciotto anni"}),
    11516: (T + "word in example", {"t_it": "singhiozzante, singhiozzando"}),
    11725: (T + "word in example", {"t_it": "spruzzare, schizzare, iniettare"}),
}

REPLACE = []
SPLIT_LATER = {}
