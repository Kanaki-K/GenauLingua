"""Шаг 2, it, порция 28: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    8403: (T + "word in example", {"t_it": "uno davanti all'altro, (Geheimnisse voreinander) l'uno con l'altro"}),
    8411: (T + "word in example", {"t_it": "inutile, inutilmente"}),
    8436: (T + "word in example", {"t_it": "spremuto, (frisch gepresster Saft) la spremuta"}),
    8490: (T + "word in example", {"t_it": "notevolmente, considerevolmente"}),
}

REPLACE = []
SPLIT_LATER = {}
