"""Шаг 2, fr, порция 33: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример fr: "

FIXES = {
    13516: (T + "в примере en", {"t_fr": "de cela, en"}),
    13517: (T + "в примере pour ça", {"t_fr": "ce faisant, dans ce cas, pour cela"}),
    14009: (T + "в примере dépendre de", {"t_fr": "dépendant, (angewiesen sein auf) dépendre de"}),
    14029: (T + "в примере annoncer", {"t_fr": "transmettre, remettre, annoncer"}),
    14120: (T + "в примере parler franchement", {"t_fr": "le franc-parler, (Klartext reden) parler franchement"}),
    14221: (T + "в примере parler tout seul", {"t_fr": "le monologue, (Selbstgespräche führen) parler tout seul"}),
}

REPLACE = []
SPLIT_LATER = {}
