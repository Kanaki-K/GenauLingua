"""Шаг 2, pl, порция 38: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример pl: "

FIXES = {
    7704: (T + "word in example", {"t_pl": "w razie potrzeby, w razie czego"}),
    7731: (T + "word in example", {"t_pl": "zaginiony, (verschollen sein) zaginąć"}),
    7736: (T + "word in example", {"t_pl": "wyciągnąć, wycisnąć, wyczarować"}),
    18425: (T + "word in example", {"t_pl": "osiadły, (sesshaft werden) osiąść"}),
    18736: (T + "word in example", {"t_pl": "dotychczas, jak dotąd, na razie"}),
}

REPLACE = []
SPLIT_LATER = {}
