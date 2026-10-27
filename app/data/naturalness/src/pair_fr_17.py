"""Шаг 2, fr, порция 17: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример fr: "

FIXES = {
    9607: (T + "в примере fac", {"t_fr": "l'université, la fac"}),
    9770: (T + "нет gratuit", {"x_fr": "Avec le gâteau, le café est gratuit"}),
}

REPLACE = []
SPLIT_LATER = {}
