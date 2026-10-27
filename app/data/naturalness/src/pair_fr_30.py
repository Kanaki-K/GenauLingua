"""Шаг 2, fr, порция 30: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример fr: "

FIXES = {
    10578: (T + "в примере глагол, нет ennuyé", {"x_fr": "Les élèves avaient l'air ennuyés en cours"}),
    10734: (T + "в примере affectueusement", {"t_fr": "affectueux, affectueusement"}),
}

REPLACE = []
SPLIT_LATER = {}
