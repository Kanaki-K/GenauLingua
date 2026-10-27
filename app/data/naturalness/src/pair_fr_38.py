"""Шаг 2, fr, порция 38: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример fr: "

FIXES = {
    7550: (T + "в примере avoir lieu", {"t_fr": "aboutir, (zustande kommen) avoir lieu"}),
    7608: (T + "в примере prévoir", {"t_fr": "fixer, commencer, prévoir"}),
    7663: (T + "в примере tomber mal", {"t_fr": "défavorable, mal choisi, (ungünstig sein) tomber mal"}),
    7685: (T + "в примере faire marche arrière", {"t_fr": "la reculade, (einen Rückzieher machen) faire marche arrière"}),
    7704: (T + "в примере à la rigueur", {"t_fr": "au besoin, si nécessaire, à la rigueur"}),
    18461: (T + "в примере travaux", {"t_fr": "la rénovation, la transformation, les travaux"}),
    18736: (T + "в примере jusqu'ici, не как в переводе", {"x_fr": "Jusqu'à présent, personne n'a répondu à l'annonce"}),
    18783: (T + "нет Moyen Âge", {"x_fr": "À la fête du Moyen Âge, les enfants mangent des galettes et regardent les chevaliers"}),
}

REPLACE = []
SPLIT_LATER = {}
