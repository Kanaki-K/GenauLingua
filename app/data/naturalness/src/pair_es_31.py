"""Шаг 2, es, порция 31: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример es: "

FIXES = {
    11400: (T + "word in example", {"t_es": "bárbaro, (etwas Barbarisches) una barbaridad"}),
    11516: (T + "word in example", {"t_es": "sollozante, sollozando"}),
    11564: (T + "word in example", {"x_es": "Nuestro conductor de autobús conduce de forma tan prudente en la nieve que los niños llegan igualmente puntuales al colegio"}),
    11725: (T + "word in example", {"t_es": "rociar, salpicar, inyectar"}),
}

REPLACE = []
SPLIT_LATER = {}
