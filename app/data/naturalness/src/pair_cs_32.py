"""Шаг 2, cs, порция 32: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример cs: "

FIXES = {
    11752: (T + "в примере nadělat chaos", {"t_cs": "servírovat, způsobit, (Chaos anrichten) nadělat"}),
    12597: (T + "в примере topí se, не utonout", {"x_cs": "Nikdy nenechávej malou samotnou u bazénu, děti můžou utonout úplně potichu"}),
    12662: (T + "в примере omdlít", {"t_cs": "mdloba, bezmoc, (in Ohnmacht fallen) omdlít"}),
    12723: (T + "в примере přivezla, не přijatý", {"x_cs": "Po pádu byla babička přijatá do nemocnice, ale už je jí líp"}),
}

REPLACE = []
SPLIT_LATER = {}
