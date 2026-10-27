"""Шаг 2, fr, порция 46: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример fr: "

FIXES = {
    8689: (T + "в примере irrévocablement", {"t_fr": "irrévocable, définitif, irrévocablement"}),
    8692: (T + "в примере remarquablement", {"t_fr": "considérable, remarquable, remarquablement"}),
    11295: (T + "в примере découvrir le petit jeu", {"t_fr": "les ruses, (jemandem auf die Schliche kommen) découvrir le petit jeu de qqn"}),
    11408: (T + "в примере implacablement", {"t_fr": "implacable, impitoyable, implacablement"}),
    11449: (T + "нет dévoué", {"x_fr": "Notre chien m'est entièrement dévoué et me suit partout, même dans la salle de bain"}),
    11472: (T + "в примере impitoyablement", {"t_fr": "impitoyable, implacable, impitoyablement"}),
}

REPLACE = []
SPLIT_LATER = {}
