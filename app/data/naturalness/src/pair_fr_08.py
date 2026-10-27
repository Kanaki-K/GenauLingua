"""Шаг 2, fr, порция 8: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример fr: "

FIXES = {
    1012: (T + "passage dans — неестественно", {"x_fr": "Le passage à la nouvelle entreprise a été le bon choix"}),
    1192: (T + "в примере suffisamment", {"t_fr": "suffisant, suffisamment"}),
    1241: (T + "в примере s'inscrire à", {"t_fr": "suivre, justifier, (einen Kurs belegen) s'inscrire à"}),
}

REPLACE = []
SPLIT_LATER = {}
