"""Шаг 2, en, порция 25: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    17587: (T + "word in example", {"x_en": "We're late because the car had a breakdown"}),
    17940: (T + "word in example", {"t_en": "to measure, (Fieber messen) to take (temperature)"}),
}

REPLACE = []
SPLIT_LATER = {}
