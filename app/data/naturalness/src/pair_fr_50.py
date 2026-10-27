"""Шаг 2, fr, порция 50: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример fr: "

FIXES = {
    18086: (T + "в примере testeurs", {"t_fr": "le testeur, le participant, le sujet"}),
    18440: (T + "в примере cave voûtée, не voûte", {"x_fr": "Le restaurant se trouve dans un vieux caveau, en été il y fait agréablement frais"}),
    18491: (T + "в примере les locaux", {"t_fr": "les locaux, le local, l'espace"}),
    18906: (T + "в примере repoussé, в t reporter", {"x_fr": "J'ai déjà reporté trois fois mon rendez-vous chez le dentiste"}),
}

REPLACE = []
SPLIT_LATER = {}
