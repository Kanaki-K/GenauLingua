"""Шаг 2, fr, порция 3: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример fr: "

FIXES = {
    10061: (T + "в примере en vouloir", {"t_fr": "fâché, méchant, (böse sein) en vouloir"}),
    12514: (T + "T'as pas — слишком разговорно для A1", {"x_fr": "Tu as une cigarette pour moi ?"}),
    13282: (T + "в примере à la", {"t_fr": "au, à la, chez le"}),
    17834: (T + "в примере le domaine", {"t_fr": "le bien, la marchandise, le domaine"}),
}

REPLACE = []
SPLIT_LATER = {}
