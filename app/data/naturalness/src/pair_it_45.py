"""Шаг 2, it, порция 45: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример it: "

FIXES = {
    8198: (T + "word in example", {"x_it": "Come sia finito l'anello in frigo resta misterioso per tutti noi"}),
    8553: (T + "word in example", {"x_it": "A mezzanotte tutti per strada sparano i fuochi d'artificio"}),
    8564: (T + "word in example", {"x_it": "La mia gatta si avvicina in modo impercettibile e mi salta in grembo"}),
}

REPLACE = []
SPLIT_LATER = {}
