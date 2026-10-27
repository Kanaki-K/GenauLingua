"""Шаг 2, fr, порция 43: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример fr: "

FIXES = {
    16422: (T + "в примере assiégé", {"t_fr": "le siège, (unter Belagerung) assiégé"}),
    16559: (T + "в примере artillerie lourde", {"t_fr": "le canon, la pièce d'artillerie, (schweres Geschütz) l'artillerie lourde"}),
}

REPLACE = []
SPLIT_LATER = {}
