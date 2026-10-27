"""Шаг 2, fr, порция 37: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример fr: "

FIXES = {
    17814: (T + "в примере mettre à profit", {"t_fr": "apporter, proposer, mettre à profit"}),
    17870: (T + "par sécurité pour sa retraite — коряво", {"x_fr": "Pour assurer sa sécurité à la retraite, ma mère met chaque mois un peu d'argent de côté sur un compte à part"}),
    18239: (T + "в примере les uns contre les autres", {"t_fr": "l'un contre l'autre, les uns contre les autres"}),
    18243: (T + "пример про Boulevardpresse", {"t_fr": "le boulevard, (die Boulevardpresse) la presse à scandale"}),
}

REPLACE = []
SPLIT_LATER = {}
