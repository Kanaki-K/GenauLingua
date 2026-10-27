"""Шаг 2, fr, порция 27: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример fr: "

FIXES = {
    7102: (T + "в примере attendre", {"t_fr": "revenir, s'approcher, (auf jemanden zukommen) attendre"}),
    7110: (T + "в примере hors de question", {"t_fr": "en question, en considération, (nicht infrage kommen) hors de question"}),
    7145: (T + "в примере ne pas quitter", {"t_fr": "reculer, céder, (nicht von der Seite weichen) ne pas quitter"}),
    7176: (T + "в примере faire des miracles", {"t_fr": "provoquer, entraîner, (Wunder bewirken) faire des miracles"}),
    7278: (T + "в примере en rester là", {"t_fr": "laisser, (es dabei belassen) en rester là"}),
    7414: (T + "нет bizarre", {"x_fr": "Notre nouveau voisin est un type bizarre, il ne dit jamais bonjour et se promène dans le jardin la nuit"}),
    7436: (T + "в примере particulièrement", {"t_fr": "particulier, particulièrement"}),
    7467: (T + "в примере passer dans", {"t_fr": "y passer, crever, (für etwas draufgehen) passer dans"}),
}

REPLACE = []
SPLIT_LATER = {}
