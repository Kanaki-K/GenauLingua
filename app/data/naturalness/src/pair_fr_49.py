"""Шаг 2, fr, порция 49: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример fr: "

FIXES = {
    16784: (T + "в примере légal", {"t_fr": "médico-légal, criminalistique, légal"}),
    16811: (T + "в примере récidiver", {"t_fr": "récidiviste, rechuté, (rückfällig werden) récidiver"}),
    16916: (T + "нет entrer en défilant", {"x_fr": "À huit heures pile, toute la noce entre en défilant dans la salle, en musique"}),
    16975: (T + "нет rompre une lance", {"x_fr": "À la réunion des parents, ma femme rompt une lance pour la jeune institutrice"}),
    17694: (T + "в примере patienter en ligne", {"t_fr": "l'attente téléphonique, le circuit d'attente, (in der Warteschleife) patienter en ligne"}),
    17714: (T + "в примере télécommandé", {"t_fr": "la télécommande, le radioguidage, télécommandé"}),
}

REPLACE = []
SPLIT_LATER = {}
