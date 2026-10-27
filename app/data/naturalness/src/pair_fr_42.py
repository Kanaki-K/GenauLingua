"""Шаг 2, fr, порция 42: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример fr: "

FIXES = {
    14118: (T + "в примере trouver (un emploi)", {"t_fr": "servir de médiateur, transmettre, trouver (un emploi)"}),
    14603: (T + "в примере solennellement", {"t_fr": "solennel, solennellement"}),
}

REPLACE = []
SPLIT_LATER = {}
