"""Шаг 2, en, порция 7: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример en: "

FIXES = {
    218: (T + "natural", {"x_en": "He banged his elbow"}),
    260: (T + "word in example", {"t_en": "end of the working day, knocking-off time, (Feierabend!) work's over"}),
}

REPLACE = []
SPLIT_LATER = {}
