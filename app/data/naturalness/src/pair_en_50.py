"""Шаг 2, en, порция 50: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    18859: (T + "word in example", {"t_en": "night, night-time, nocturnal"}),
    18864: (T + "word in example", {"t_en": "from then on, from now on, henceforth"}),
}

REPLACE = []
SPLIT_LATER = {}
