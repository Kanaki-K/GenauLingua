"""Шаг 2, fr, порция 13: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример fr: "

FIXES = {
    2792: (T + "в примере passer en mode", {"t_fr": "changer, allumer, passer (en mode)"}),
    2876: (T + "в примере terriblement", {"t_fr": "animal, terrible, terriblement"}),
    2909: (T + "в примере l'utilisation", {"t_fr": "le contact, la relation, l'utilisation (de)"}),
    2925: (T + "в примере inutilement", {"t_fr": "inutile, superflu, inutilement"}),
    3055: (T + "в примере rapidement", {"t_fr": "rapide, vif, rapidement"}),
}

REPLACE = []
SPLIT_LATER = {}
