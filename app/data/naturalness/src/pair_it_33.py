"""Шаг 2, it, порция 33: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    13674: (T + "word in example", {"t_it": "mettersi, mettere su (sul fornello)"}),
    14009: (T + "word in example", {"t_it": "dipendente, (angewiesen sein auf) dipendere da"}),
}

REPLACE = []
SPLIT_LATER = {}
