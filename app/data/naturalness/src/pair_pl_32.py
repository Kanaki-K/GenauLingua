"""Шаг 2, pl, порция 32: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    12626: (T + "word in example", {"t_pl": "zatruć, otruć"}),
    12662: (T + "word in example", {"t_pl": "omdlenie, bezsilność, (in Ohnmacht fallen) zemdleć"}),
    12674: (T + "word in example", {"t_pl": "oddech, wdech, (in einem Atemzug) jednym tchem"}),
}

REPLACE = []
SPLIT_LATER = {}
