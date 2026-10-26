"""Шаг 2, en, порция 22: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    14934: (T + "word in example", {"t_en": "bottom, behind, bum"}),
    15022: (T + "word in example", {"x_en": "I need someone to keep me company at the doctor's"}),
}

REPLACE = []
SPLIT_LATER = {}
