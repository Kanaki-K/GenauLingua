"""Шаг 2, it, порция 22: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    14945: (T + "word in example", {"t_it": "separato, diviso, separatamente"}),
    14947: (T + "word in example", {"t_it": "seppellire, (begraben sein) essere sepolto"}),
}

REPLACE = []
SPLIT_LATER = {}
