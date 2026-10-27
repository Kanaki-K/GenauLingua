"""Шаг 2, fr, порция 7: перевод слова и пример в паре — бытово, слово карточки стоит в примере"""

T = "перевод+пример fr: "

FIXES = {
    324: (T + "в примере confortablement", {"t_fr": "chaleureux, confortable, confortablement"}),
    449: (T + "в примере un sur deux", {"t_fr": "chaque, chacun, (jeder zweite) un sur deux"}),
}

REPLACE = []
SPLIT_LATER = {}
