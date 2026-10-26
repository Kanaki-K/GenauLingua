"""Шаг 2, en, порция 21: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    13429: (T + "tense", {"x_en": "He's standing in the middle of the street"}),
    13482: (T + "word in example", {"t_en": "none, not one, not any"}),
    13829: (T + "word in example", {"t_en": "er, um, uh"}),
    13884: (T + "word in example", {"t_en": "silly stuff, nonsense, rubbish"}),
}

REPLACE = []
SPLIT_LATER = {}
