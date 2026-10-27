"""Шаг 2, fr, порция 34: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример fr: "

FIXES = {
    14318: (T + "в примере livreur, нет porteur", {"x_fr": "Le porteur du gâteau d'anniversaire a sonné à la mauvaise porte, et la voisine était ravie"}),
    14510: (T + "в примере être applaudi", {"t_fr": "les applaudissements, l'approbation, (Beifall finden) être applaudi"}),
    14539: (T + "в примере notes, нет manuscrit", {"x_fr": "Sans mon manuscrit, je ne peux pas faire de discours, sinon j'oublie tout"}),
    14542: (T + "в примере envoûter", {"t_fr": "l'envoûtement, le ban, (in den Bann ziehen) envoûter"}),
    15073: (T + "в примере vie commune", {"t_fr": "le partenariat, la relation, la vie commune"}),
}

REPLACE = []
SPLIT_LATER = {}
