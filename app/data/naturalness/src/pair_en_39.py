"""Шаг 2, en, порция 39: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    7900: (T + "word in example", {"t_en": "to overflow, to boil over"}),
    7927: (T + "word in example", {"x_en": "The first-aid course for the driving licence only comprises one Saturday"}),
    7982: (T + "word in example", {"x_en": "Just the smell of hospitals causes me to feel sick"}),
}

REPLACE = []
SPLIT_LATER = {}
