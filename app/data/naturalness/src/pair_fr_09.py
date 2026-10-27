"""Шаг 2, fr, порция 9: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример fr: "

FIXES = {
    1462: (T + "в примере contrairement à", {"t_fr": "le contraire, l'opposé, (im Gegensatz zu) contrairement à"}),
    1699: (T + "нет collège", {"x_fr": "En Bavière, le collège s'appelle aujourd'hui Mittelschule"}),
    1700: (T + "в примере du milieu", {"t_fr": "moyen, du milieu"}),
}

REPLACE = []
SPLIT_LATER = {}
