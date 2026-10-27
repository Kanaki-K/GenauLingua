"""Шаг 2, fr, порция 5: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример fr: "

FIXES = {
    1326: (T + "в примере c'est pour ça", {"t_fr": "c'est pourquoi, c'est pour ça"}),
    1327: (T + "в примере clairement", {"t_fr": "clair, net, clairement"}),
    1440: (T + "в примере volontairement", {"t_fr": "volontaire, volontairement"}),
    1530: (T + "в примере Entrez !", {"t_fr": "à l'intérieur, dedans, (Herein!) Entrez !"}),
    1537: (T + "в примере aller-retour", {"t_fr": "là-bas, (hin und zurück) aller-retour"}),
    2036: (T + "в примере prendre rendez-vous", {"t_fr": "fixer, convenir de, (einen Termin vereinbaren) prendre rendez-vous"}),
    2095: (T + "toujours … à l'avenir — коряво", {"x_fr": "À l'avenir aussi, je travaillerai ici"}),
}

REPLACE = []
SPLIT_LATER = {}
