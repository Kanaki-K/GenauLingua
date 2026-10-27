"""Шаг 2, fr, порция 6: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример fr: "

FIXES = {
    6324: (T + "в примере sors", {"t_fr": "dehors, hors, (komm heraus) sors"}),
    6364: (T + "в примере pile", {"t_fr": "le point, (Punkt acht) pile"}),
    7464: (T + "в примере à la tienne", {"t_fr": "le bien, le bien-être, (Zum Wohl!) à la tienne"}),
    13384: (T + "пассив без формы слова — on m'a volé", {"x_fr": "Mon vélo a été volé devant la gare hier"}),
}

REPLACE = []
SPLIT_LATER = {}
