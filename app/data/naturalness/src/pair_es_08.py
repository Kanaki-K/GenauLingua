"""Шаг 2, es, порция 8: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    1173: (T + "word in example", {"t_es": "el listado, la lista"}),
    1238: (T + "word in example", {"t_es": "la autoridad, la oficina pública, el organismo público"}),
    1388: (T + "word in example", {"t_es": "la relajación, (zur Entspannung) para relajarse"}),
}

REPLACE = []
SPLIT_LATER = {}
