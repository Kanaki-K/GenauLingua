"""Шаг 2, fr, порция 40: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример fr: "

FIXES = {
    9887: (T + "в примере ne s'achète pas", {"t_fr": "à vendre, corruptible, (nicht käuflich) ne pas s'acheter"}),
    10873: (T + "нет éclat de rire", {"x_fr": "Avec son discours au mariage, mon frère a déclenché des éclats de rire dans toute la salle"}),
    10890: (T + "в примере s'apitoyer sur son sort", {"t_fr": "l'apitoiement sur soi-même, (in Selbstmitleid versinken) s'apitoyer sur son sort"}),
}

REPLACE = []
SPLIT_LATER = {}
