"""Шаг 2, fr, порция 39: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример fr: "

FIXES = {
    7756: (T + "в примере se passer", {"t_fr": "arriver, s'en sortir, se passer"}),
    7762: (T + "в примере premier rang", {"t_fr": "avant, de devant, (die vordere Reihe) le premier rang"}),
    7839: (T + "в примере coup de fouet", {"t_fr": "l'élan, la poussée, le coup de fouet"}),
    7851: (T + "в примере à l'unanimité", {"t_fr": "unanime, à l'unanimité"}),
    7965: (T + "в примере constamment", {"t_fr": "constant, stable, constamment"}),
    7968: (T + "в примере même pas de loin", {"t_fr": "en partie, un tant soit peu, (nicht ansatzweise) même pas de loin"}),
    8001: (T + "в примере force motrice", {"t_fr": "moteur, déterminant, (treibende Kraft) la force motrice"}),
    8017: (T + "в примере impeccablement", {"t_fr": "impeccable, irréprochable, impeccablement"}),
    8133: (T + "в примере futilités, нет futile", {"x_fr": "Les deux frères se disputent souvent pour des raisons futiles"}),
}

REPLACE = []
SPLIT_LATER = {}
