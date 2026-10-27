"""Шаг 2, fr, порция 41: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример fr: "

FIXES = {
    11059: (T + "в примере broyer du noir", {"t_fr": "la morosité, le cafard, (Trübsal blasen) broyer du noir"}),
    11147: (T + "в примере avec zèle", {"t_fr": "zélé, assidu, avec zèle"}),
    12809: (T + "service de leucémie — калька", {"x_fr": "À la course solidaire de l'école, les enfants récoltent de l'argent pour les enfants atteints de leucémie à l'hôpital"}),
}

REPLACE = []
SPLIT_LATER = {}
