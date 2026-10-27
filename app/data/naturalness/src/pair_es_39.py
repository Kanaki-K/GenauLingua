"""Шаг 2, es, порция 39: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    7762: (T + "в примере primera fila", {"t_es": "delantero, (die vordere Reihe) la primera fila"}),
    7795: (T + "в примере peleándose", {"t_es": "esforzarse, pelearse (con algo)"}),
    7845: (T + "в примере un desastre", {"t_es": "estropeado, fastidiado, un desastre"}),
    7851: (T + "в примере por unanimidad", {"t_es": "unánime, por unanimidad"}),
    7926: (T + "в примере molestarse", {"t_es": "la circunstancia, la molestia, (sich Umstände machen) molestarse"}),
    8991: (T + "нет aumento de sueldo", {"x_es": "Después de tres años por fin me han dado un aumento de sueldo y enseguida me he comprado una lavadora nueva"}),
    9019: (T + "la obra de la vida del abuelo — неестественно", {"x_es": "El huerto de detrás de la casa es para el abuelo la obra de su vida, nadie puede coger nada sin él"}),
}

REPLACE = []
SPLIT_LATER = {}
