"""Шаг 2, fr, порция 47: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример fr: "

FIXES = {
    11491: (T + "в примере глагол, нет inquiétude", {"x_fr": "Pas de motif d'inquiétude, le chien est juste dans le jardin du voisin"}),
    11511: (T + "в примере avec insistance", {"t_fr": "persévérant, tenace, avec insistance"}),
    11513: (T + "sensuel про гончарство — неуместно", {"x_fr": "La poterie est un travail très sensoriel, on sent l'argile sous ses mains"}),
    11957: (T + "в примере fourré", {"t_fr": "farci, rempli, fourré"}),
    12357: (T + "в примере à distance", {"t_fr": "la portée de tir, (außer Schussweite) à distance"}),
    13587: (T + "нет là-dessus", {"x_fr": "Là-dessus, on en reparlera, jeune homme !"}),
}

REPLACE = []
SPLIT_LATER = {}
