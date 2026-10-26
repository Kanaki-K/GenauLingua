"""Шаг 2, en, порция 48: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    15147: (T + "word in example", {"t_en": "to testify to, to show, to father"}),
    15774: (T + "tense", {"x_en": "We went out without an umbrella and came home completely drenched"}),
}

REPLACE = []
SPLIT_LATER = {}
